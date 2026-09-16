#!/usr/bin/env python3
"""Build the CV and keep website preprints synchronized.

The editable LaTeX project remains outside this repository by default at
~/Desktop/CV.  This script is the single orchestration point for updating a
preprint in both that project and the website, rebuilding the PDF, and copying
the verified result to both the CV project and website root.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ElementTree
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, Iterable, NamedTuple, Optional, Sequence, Tuple


REPO_ROOT = Path(__file__).resolve().parents[1]
ABOUT_PAGE = REPO_ROOT / "_pages" / "about.md"
WEBSITE_PDF = REPO_ROOT / "Lai_Lexiao_CV.pdf"
CV_TEX_NAME = "Lai_Lexiao_CV.tex"
CV_PDF_NAME = "Lai_Lexiao_CV.pdf"
CV_CLASS_NAME = "res.cls"
CV_LINK = "[[Curriculum Vitae](/Lai_Lexiao_CV.pdf)]"
CV_OWNER = "Lexiao Lai"
CODEX_PDF_TOOLS = (
    Path.home()
    / ".cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override"
)
ARXIV_ID_RE = re.compile(
    r"(?:https?://arxiv\.org/(?:abs|pdf)/)?(\d{4}\.\d{4,5})(?:v\d+)?(?:\.pdf)?$"
)
YEAR_SUFFIX_RE = re.compile(r",\s+\d{4}\s*$")
LATEX_WARNING_RE = re.compile(
    r"(?:! LaTeX Error|Undefined control sequence|LaTeX Warning:|"
    r"Overfull \\hbox|Underfull \\hbox)"
)


class PipelineError(RuntimeError):
    """A user-actionable pipeline failure."""


class ArxivMetadata(NamedTuple):
    arxiv_id: str
    title: str
    authors: Tuple[str, ...]
    year: int


class _ArxivMetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.values: Dict[str, list[str]] = {}

    def handle_starttag(
        self, tag: str, attributes: Sequence[Tuple[str, Optional[str]]]
    ) -> None:
        if tag.casefold() != "meta":
            return
        values = {name.casefold(): value for name, value in attributes if value}
        name = values.get("name", "").casefold()
        content = values.get("content")
        if name.startswith("citation_") and content is not None:
            self.values.setdefault(name, []).append(content)


def normalize_arxiv_id(value: str) -> str:
    candidate = value.strip().rstrip("/")
    match = ARXIV_ID_RE.fullmatch(candidate)
    if not match:
        raise PipelineError(
            f"Invalid arXiv identifier or URL: {value!r}. "
            "Expected a value such as 2605.14345 or "
            "https://arxiv.org/abs/2605.14345."
        )
    return match.group(1)


def normalize_text(value: str) -> str:
    return unicodedata.normalize("NFC", " ".join(value.split()))


def _metadata_year(value: str, label: str) -> int:
    match = re.match(r"^(\d{4})[-/]", value.strip())
    if not match:
        raise PipelineError(f"arXiv {label} has an invalid date: {value!r}.")
    return int(match.group(1))


def _citation_name_to_display(value: str) -> str:
    name = normalize_text(value)
    if name.count(",") == 1:
        family, given = (part.strip() for part in name.split(",", 1))
        if family and given:
            return f"{given} {family}"
    return name


def parse_arxiv_html(document: str, expected_id: str) -> ArxivMetadata:
    parser = _ArxivMetaParser()
    parser.feed(document)

    identifiers = parser.values.get("citation_arxiv_id", [])
    titles = parser.values.get("citation_title", [])
    dates = parser.values.get("citation_date", [])
    authors = parser.values.get("citation_author", [])
    if len(identifiers) != 1 or len(titles) != 1 or len(dates) != 1 or not authors:
        raise PipelineError("The arXiv abstract page did not contain complete citation metadata.")
    arxiv_id = normalize_arxiv_id(identifiers[0])
    if arxiv_id != expected_id:
        raise PipelineError(
            f"The arXiv abstract page returned ID {arxiv_id}, expected {expected_id}."
        )
    return ArxivMetadata(
        arxiv_id=arxiv_id,
        title=normalize_text(titles[0]),
        authors=tuple(_citation_name_to_display(author) for author in authors),
        year=_metadata_year(dates[0], "abstract page"),
    )


def parse_arxiv_atom(document: str, expected_id: str) -> ArxivMetadata:
    try:
        root = ElementTree.fromstring(document)
    except ElementTree.ParseError as error:
        raise PipelineError("The arXiv API returned malformed XML.") from error
    namespace = {"atom": "http://www.w3.org/2005/Atom"}
    entries = root.findall("atom:entry", namespace)
    if len(entries) != 1:
        raise PipelineError(f"The arXiv API returned {len(entries)} records, expected 1.")
    entry = entries[0]
    identifier = entry.findtext("atom:id", default="", namespaces=namespace)
    title = entry.findtext("atom:title", default="", namespaces=namespace)
    published = entry.findtext("atom:published", default="", namespaces=namespace)
    authors = tuple(
        normalize_text(author.findtext("atom:name", default="", namespaces=namespace))
        for author in entry.findall("atom:author", namespace)
    )
    arxiv_id = normalize_arxiv_id(identifier)
    if arxiv_id != expected_id:
        raise PipelineError(f"The arXiv API returned ID {arxiv_id}, expected {expected_id}.")
    if not normalize_text(title) or not authors or any(not author for author in authors):
        raise PipelineError("The arXiv API returned incomplete title or author metadata.")
    return ArxivMetadata(
        arxiv_id=arxiv_id,
        title=normalize_text(title),
        authors=authors,
        year=_metadata_year(published, "API record"),
    )


def _download_text(url: str, timeout: int = 15) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "cv-pipeline/1.0 (personal academic website updater)"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = response.read(2_000_001)
        if len(data) > 2_000_000:
            raise PipelineError("The arXiv metadata response was unexpectedly large.")
        charset = response.headers.get_content_charset() or "utf-8"
        return data.decode(charset)


def fetch_arxiv_metadata(arxiv_id: str) -> ArxivMetadata:
    query = urllib.parse.urlencode({"id_list": arxiv_id})
    attempts = (
        (f"https://arxiv.org/abs/{arxiv_id}", parse_arxiv_html),
        (f"https://export.arxiv.org/api/query?{query}", parse_arxiv_atom),
    )
    failures = []
    for url, parser in attempts:
        try:
            return parser(_download_text(url), arxiv_id)
        except (OSError, UnicodeError, PipelineError) as error:
            failures.append(f"{url}: {error}")
    details = "; ".join(failures)
    raise PipelineError(
        "Could not retrieve complete metadata from official arXiv sources. "
        "Retry online, or provide every coauthor with a repeated --coauthor flag "
        "(use --solo for a sole-authored paper) and optionally --year. "
        f"Details: {details}"
    )


def format_name_list(names: Sequence[str]) -> str:
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return ", ".join(names[:-1]) + f", and {names[-1]}"


def _year_from_arxiv_id(arxiv_id: str) -> int:
    return 2000 + int(arxiv_id[:2])


def resolve_new_preprint_metadata(
    arguments: argparse.Namespace, arxiv_id: str, title: str
) -> Tuple[Tuple[str, ...], int, str]:
    explicit_coauthors = arguments.coauthor
    if explicit_coauthors and arguments.solo:
        raise PipelineError("Use either --coauthor or --solo, not both.")

    if explicit_coauthors is not None or arguments.solo:
        coauthors = tuple(normalize_text(name) for name in (explicit_coauthors or []))
        if any(not name for name in coauthors):
            raise PipelineError("Coauthor names must not be empty.")
        if len(set(coauthors)) != len(coauthors):
            raise PipelineError("Each coauthor must be listed exactly once.")
        if any(name.casefold() == CV_OWNER.casefold() for name in coauthors):
            raise PipelineError(f"Do not include {CV_OWNER!r} in --coauthor flags.")
        year = arguments.year or _year_from_arxiv_id(arxiv_id)
        return coauthors, year, "command-line metadata"

    metadata = fetch_arxiv_metadata(arxiv_id)
    if metadata.title != title:
        raise PipelineError(
            "The supplied title does not match the current arXiv title. "
            f"Supplied: {title!r}; arXiv: {metadata.title!r}."
        )
    owner_positions = [
        index
        for index, author in enumerate(metadata.authors)
        if author.casefold() == CV_OWNER.casefold()
    ]
    if len(owner_positions) != 1:
        raise PipelineError(
            f"Expected arXiv metadata to list {CV_OWNER!r} exactly once; "
            f"authors were {list(metadata.authors)!r}."
        )
    if arguments.year is not None and arguments.year != metadata.year:
        raise PipelineError(
            f"--year {arguments.year} disagrees with arXiv's year {metadata.year}."
        )
    coauthors = tuple(
        author for index, author in enumerate(metadata.authors) if index != owner_positions[0]
    )
    return coauthors, metadata.year, "official arXiv metadata"


def latex_escape_title(title: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(character, character) for character in title)


def latex_title_to_plain(title: str) -> str:
    replacements = {
        r"\textbackslash{}": "\\",
        r"\textasciitilde{}": "~",
        r"\textasciicircum{}": "^",
        r"\&": "&",
        r"\%": "%",
        r"\$": "$",
        r"\#": "#",
        r"\_": "_",
        r"\{": "{",
        r"\}": "}",
    }
    plain = title
    for escaped, character in replacements.items():
        plain = plain.replace(escaped, character)
    return plain


def _title_bounds(line: str, prefix: str, link_position: int) -> Tuple[int, int]:
    try:
        title_start = line.index(prefix) + len(prefix)
    except ValueError as error:
        raise PipelineError(
            f"Entry does not contain expected prefix {prefix!r}: {line!r}"
        ) from error

    before_link = line[:link_position].rstrip()
    author_position = before_link.rfind(" (with ")
    if author_position >= title_start:
        return title_start, author_position

    year_match = YEAR_SUFFIX_RE.search(before_link)
    if not year_match or year_match.start() < title_start:
        raise PipelineError(f"Could not separate title from authors/year in entry: {line!r}")
    return title_start, year_match.start()


def replace_title_for_url(
    text: str,
    *,
    url: str,
    title: str,
    prefix: str,
    link_token: str,
    label: str,
) -> Tuple[str, str]:
    lines = text.splitlines(keepends=True)
    target = re.compile(re.escape(url) + r"(?:v\d+)?(?:\.pdf)?(?=[)}]|$)")
    matches = [(index, line) for index, line in enumerate(lines) if target.search(line)]
    if len(matches) != 1:
        raise PipelineError(
            f"Expected exactly one {label} entry containing {url}, found {len(matches)}."
        )

    index, line = matches[0]
    if link_token not in line:
        raise PipelineError(f"The matched {label} line is not a preprint entry: {line!r}")
    link_position = line.index(link_token)
    title_start, title_end = _title_bounds(line, prefix, link_position)
    old_title = line[title_start:title_end]
    lines[index] = line[:title_start] + title + line[title_end:]
    return "".join(lines), old_title


def _section_bounds(
    text: str, start_marker: str, end_marker: str, label: str
) -> Tuple[int, int]:
    try:
        start = text.index(start_marker) + len(start_marker)
        end = text.index(end_marker, start)
    except ValueError as error:
        raise PipelineError(f"Could not locate the {label} section boundaries.") from error
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        raise PipelineError(f"Expected unique {label} section boundaries.")
    return start, end


def _section(text: str, start_marker: str, end_marker: str, label: str) -> str:
    start, end = _section_bounds(text, start_marker, end_marker, label)
    return text[start:end]


def replace_title_in_section(
    text: str,
    *,
    start_marker: str,
    end_marker: str,
    url: str,
    title: str,
    prefix: str,
    link_token: str,
    label: str,
) -> Tuple[str, str]:
    start, end = _section_bounds(text, start_marker, end_marker, label)
    updated, old_title = replace_title_for_url(
        text[start:end],
        url=url,
        title=title,
        prefix=prefix,
        link_token=link_token,
        label=label,
    )
    return text[:start] + updated + text[end:], old_title


def _preprint_map(
    text: str,
    *,
    start_marker: str,
    end_marker: str,
    prefix: str,
    link_token: str,
    latex: bool,
    label: str,
) -> Dict[str, str]:
    section = _section(text, start_marker, end_marker, label)
    entries: Dict[str, str] = {}
    for line in section.splitlines():
        if "arxiv.org/abs/" not in line or link_token not in line:
            continue
        id_match = re.search(r"arxiv\.org/abs/(\d{4}\.\d{4,5})(?!\d)", line)
        if not id_match:
            continue
        arxiv_id = id_match.group(1)
        link_position = line.index(link_token)
        title_start, title_end = _title_bounds(line, prefix, link_position)
        title = line[title_start:title_end]
        if latex:
            title = latex_title_to_plain(title)
        if arxiv_id in entries:
            raise PipelineError(f"Duplicate arXiv ID {arxiv_id} in {label}.")
        entries[arxiv_id] = title
    return entries


def website_preprints(text: str) -> Dict[str, str]:
    return _preprint_map(
        text,
        start_marker="## Preprints",
        end_marker="## Publications",
        prefix="1. ",
        link_token="[[preprint](",
        latex=False,
        label="website Preprints",
    )


def cv_preprints(text: str) -> Dict[str, str]:
    return _preprint_map(
        text,
        start_marker=r"\cvsection{Preprints}",
        end_marker=r"\cvsection{Talks}",
        prefix=r"\item ",
        link_token=r"\paperlink{",
        latex=True,
        label="CV Preprints",
    )


def validate_preprint_documents(website_text: str, cv_text: str) -> Dict[str, str]:
    website_entries = website_preprints(website_text)
    cv_entries = cv_preprints(cv_text)
    if website_entries.keys() != cv_entries.keys():
        missing_from_cv = sorted(website_entries.keys() - cv_entries.keys())
        missing_from_site = sorted(cv_entries.keys() - website_entries.keys())
        raise PipelineError(
            "Website/CV preprint IDs differ. "
            f"Missing from CV: {missing_from_cv}; missing from website: {missing_from_site}."
        )
    website_ids = list(website_entries)
    cv_ids = list(cv_entries)
    if website_ids != cv_ids:
        raise PipelineError(
            "Website/CV preprint order differs. "
            f"Website: {website_ids}; CV: {cv_ids}."
        )
    mismatches = {
        arxiv_id: (website_entries[arxiv_id], cv_entries[arxiv_id])
        for arxiv_id in website_entries
        if website_entries[arxiv_id] != cv_entries[arxiv_id]
    }
    if mismatches:
        details = "; ".join(
            f"{arxiv_id}: website={site!r}, CV={cv!r}"
            for arxiv_id, (site, cv) in sorted(mismatches.items())
        )
        raise PipelineError(f"Website/CV title mismatch: {details}")
    return website_entries


def _arxiv_order_key(arxiv_id: str) -> Tuple[int, int]:
    month, sequence = arxiv_id.split(".", 1)
    return int(month), int(sequence)


def insert_ordered_preprint(
    text: str,
    *,
    arxiv_id: str,
    entry_line: str,
    start_marker: str,
    end_marker: str,
    link_token: str,
    label: str,
) -> str:
    start, end = _section_bounds(text, start_marker, end_marker, label)
    section_lines = text[start:end].splitlines(keepends=True)
    located = []
    for index, line in enumerate(section_lines):
        if link_token not in line or "arxiv.org/abs/" not in line:
            continue
        match = re.search(r"arxiv\.org/abs/(\d{4}\.\d{4,5})(?!\d)", line)
        if not match:
            raise PipelineError(f"Could not read an arXiv ID in {label}: {line!r}")
        located.append((index, match.group(1)))

    existing_ids = [existing_id for _, existing_id in located]
    expected_order = sorted(existing_ids, key=_arxiv_order_key, reverse=True)
    if existing_ids != expected_order:
        raise PipelineError(
            f"The {label} entries are not in descending arXiv order: {existing_ids}."
        )
    if arxiv_id in existing_ids:
        raise PipelineError(f"arXiv {arxiv_id} is already present in {label}.")
    if not entry_line.endswith("\n"):
        entry_line += "\n"

    new_key = _arxiv_order_key(arxiv_id)
    insertion_index = None
    for line_index, existing_id in located:
        if new_key > _arxiv_order_key(existing_id):
            insertion_index = line_index
            break
    if insertion_index is None and located:
        insertion_index = located[-1][0] + 1
    if insertion_index is None:
        if label.startswith("CV"):
            anchors = [
                index
                for index, line in enumerate(section_lines)
                if line.strip() == r"\begin{cvnumbered}"
            ]
            if len(anchors) != 1:
                raise PipelineError("Could not locate the empty CV preprint list.")
            insertion_index = anchors[0] + 1
        else:
            insertion_index = 1 if section_lines and not section_lines[0].strip() else 0

    section_lines.insert(insertion_index, entry_line)
    updated_section = "".join(section_lines)
    return text[:start] + updated_section + text[end:]


def require_tool(name: str, fallback: Optional[Path] = None) -> str:
    executable = shutil.which(name)
    if not executable and fallback and fallback.exists():
        executable = str(fallback)
    if not executable:
        raise PipelineError(
            f"Required tool {name!r} was not found. Install a full TeX Live/MacTeX "
            "distribution and Poppler before running this pipeline."
        )
    return executable


def run_checked(command: Sequence[str], *, cwd: Optional[Path] = None) -> str:
    result = subprocess.run(
        list(command),
        cwd=str(cwd) if cwd else None,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if result.returncode != 0:
        rendered = " ".join(command)
        raise PipelineError(f"Command failed ({rendered}):\n{result.stdout.strip()}")
    return result.stdout


def contains_arxiv_url(url_listing: str, arxiv_id: str) -> bool:
    url = re.escape(f"https://arxiv.org/abs/{arxiv_id}")
    return bool(re.search(url + r"(?:v\d+)?(?:\.pdf)?(?=\s|$)", url_listing))


def verify_pdf(
    pdf_path: Path,
    *,
    expected_ids: Iterable[str],
    render_dir: Path,
) -> int:
    data = pdf_path.read_bytes()
    if not data.startswith(b"%PDF-") or b"%%EOF" not in data[-2048:]:
        raise PipelineError(f"Built file is not a structurally recognizable PDF: {pdf_path}")

    pdfinfo = require_tool("pdfinfo", CODEX_PDF_TOOLS / "pdfinfo")
    pdftoppm = require_tool("pdftoppm", CODEX_PDF_TOOLS / "pdftoppm")
    information = run_checked([pdfinfo, str(pdf_path)])
    pages_match = re.search(r"^Pages:\s+(\d+)\s*$", information, flags=re.MULTILINE)
    if not pages_match or int(pages_match.group(1)) < 1:
        raise PipelineError("pdfinfo did not report a positive page count.")
    page_count = int(pages_match.group(1))

    urls = run_checked([pdfinfo, "-url", str(pdf_path)])
    for arxiv_id in expected_ids:
        expected_url = f"https://arxiv.org/abs/{arxiv_id}"
        if not contains_arxiv_url(urls, arxiv_id):
            raise PipelineError(f"Built PDF is missing hyperlink {expected_url}.")

    render_dir.mkdir(parents=True, exist_ok=True)
    run_checked([pdftoppm, "-png", "-r", "120", str(pdf_path), str(render_dir / "page")])
    rendered_pages = sorted(render_dir.glob("page-*.png"))
    if len(rendered_pages) != page_count:
        raise PipelineError(
            f"Rendered {len(rendered_pages)} pages, but pdfinfo reported {page_count}."
        )
    return page_count


def build_cv(
    *,
    cv_dir: Path,
    tex_text: str,
    keep_dir: Optional[Path] = None,
) -> Tuple[bytes, int]:
    class_path = cv_dir / CV_CLASS_NAME
    if not class_path.is_file():
        raise PipelineError(f"CV class file not found: {class_path}")
    latexmk = require_tool("latexmk", Path("/Library/TeX/texbin/latexmk"))

    with tempfile.TemporaryDirectory(prefix="cv-pipeline-") as temporary:
        temporary_path = Path(temporary)
        source_dir = temporary_path / "source"
        output_dir = temporary_path / "output"
        render_dir = temporary_path / "render"
        source_dir.mkdir()
        output_dir.mkdir()
        (source_dir / CV_TEX_NAME).write_text(tex_text, encoding="utf-8")
        shutil.copy2(class_path, source_dir / CV_CLASS_NAME)

        output = run_checked(
            [
                latexmk,
                "-pdf",
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-file-line-error",
                f"-outdir={output_dir}",
                CV_TEX_NAME,
            ],
            cwd=source_dir,
        )
        log_path = output_dir / "Lai_Lexiao_CV.log"
        log_text = (
            log_path.read_text(encoding="utf-8", errors="replace")
            if log_path.exists()
            else output
        )
        warning = LATEX_WARNING_RE.search(log_text)
        if warning:
            raise PipelineError(f"LaTeX reported a layout/build warning: {warning.group(0)}")

        built_pdf = output_dir / CV_PDF_NAME
        if not built_pdf.is_file():
            raise PipelineError(f"latexmk completed without producing {CV_PDF_NAME}.")
        expected_ids = cv_preprints(tex_text).keys()
        page_count = verify_pdf(
            built_pdf,
            expected_ids=expected_ids,
            render_dir=render_dir,
        )
        pdf_bytes = built_pdf.read_bytes()

        if keep_dir:
            keep_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(built_pdf, keep_dir / built_pdf.name)
            for rendered_page in render_dir.glob("page-*.png"):
                shutil.copy2(rendered_page, keep_dir / rendered_page.name)
    return pdf_bytes, page_count


def atomic_write_text(path: Path, text: str) -> None:
    mode = stat.S_IMODE(path.stat().st_mode)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as stream:
            stream.write(text)
        temporary_path.chmod(mode)
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def atomic_write_bytes(path: Path, data: bytes) -> None:
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
        temporary_path.chmod(mode)
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def git_output(arguments: Sequence[str]) -> str:
    return run_checked(["git", *arguments], cwd=REPO_ROOT)


def ensure_repo_targets_clean(paths: Sequence[Path]) -> None:
    relative_paths = [str(path.relative_to(REPO_ROOT)) for path in paths]
    status = git_output(["status", "--porcelain", "--", *relative_paths]).strip()
    if status:
        raise PipelineError(
            "Refusing to overwrite website targets that already have changes:\n"
            f"{status}\nCommit, stash, or restore those specific files first."
        )


def ensure_snapshot_unchanged(path: Path, expected: bytes) -> None:
    if path.read_bytes() != expected:
        raise PipelineError(
            f"{path} changed while the CV was building; no generated files were installed."
        )


def ensure_optional_snapshot_unchanged(path: Path, expected: Optional[bytes]) -> None:
    if expected is None:
        if path.exists():
            raise PipelineError(
                f"{path} appeared while the CV was building; no generated files were installed."
            )
        return
    ensure_snapshot_unchanged(path, expected)


def restore_optional_snapshot(path: Path, expected: Optional[bytes]) -> None:
    if expected is None:
        if path.exists():
            path.unlink()
        return
    atomic_write_bytes(path, expected)


def staged_paths() -> set[str]:
    return {
        line for line in git_output(["diff", "--cached", "--name-only"]).splitlines() if line
    }


def ensure_staging_clear() -> None:
    staged = staged_paths()
    if staged:
        raise PipelineError(
            "Refusing to stage while other files are already staged: "
            + ", ".join(sorted(staged))
        )


def stage_exact(paths: Sequence[Path]) -> set[str]:
    ensure_staging_clear()
    relative_paths = [str(path.relative_to(REPO_ROOT)) for path in paths]
    git_output(["add", "--", *relative_paths])
    staged = staged_paths()
    expected = set(relative_paths)
    if not staged.issubset(expected):
        git_output(["restore", "--staged", "--", *relative_paths])
        raise PipelineError(
            f"Unexpected staged scope. Allowed {sorted(expected)}, got {sorted(staged)}."
        )
    return staged


def validate_keep_dir(keep_dir: Path, cv_dir: Path) -> Path:
    resolved = keep_dir.expanduser().resolve()
    retained_pdf = (resolved / CV_PDF_NAME).resolve()
    protected_outputs = {
        WEBSITE_PDF.resolve(),
        (cv_dir / CV_PDF_NAME).resolve(),
    }
    if retained_pdf in protected_outputs:
        raise PipelineError("--keep-dir must not target the live website or CV output.")
    if resolved.exists():
        if not resolved.is_dir():
            raise PipelineError("--keep-dir must name a directory.")
        if any(resolved.iterdir()):
            raise PipelineError("--keep-dir must be a new or empty directory.")
    return resolved


def check_consistency(*, cv_dir: Path, require_pdf: bool = True) -> int:
    cv_tex_path = cv_dir / CV_TEX_NAME
    cv_pdf_path = cv_dir / CV_PDF_NAME
    if not cv_tex_path.is_file():
        raise PipelineError(f"CV source not found: {cv_tex_path}")
    website_text = ABOUT_PAGE.read_text(encoding="utf-8")
    cv_text = cv_tex_path.read_text(encoding="utf-8")
    if website_text.count(CV_LINK) != 1:
        raise PipelineError(f"Expected the homepage CV link exactly once: {CV_LINK}")

    website_entries = validate_preprint_documents(website_text, cv_text)

    if require_pdf:
        if not WEBSITE_PDF.is_file():
            raise PipelineError(f"Downloadable website CV not found: {WEBSITE_PDF}")
        if not cv_pdf_path.is_file():
            raise PipelineError(f"Compiled CV PDF not found: {cv_pdf_path}")
        if cv_pdf_path.read_bytes() != WEBSITE_PDF.read_bytes():
            raise PipelineError(
                "The compiled CV PDF and downloadable website PDF are not identical."
            )
        with tempfile.TemporaryDirectory(prefix="cv-pipeline-check-") as temporary:
            page_count = verify_pdf(
                WEBSITE_PDF,
                expected_ids=website_entries.keys(),
                render_dir=Path(temporary),
            )
    else:
        page_count = 0
    return page_count


def update_preprint(arguments: argparse.Namespace) -> None:
    arxiv_id = normalize_arxiv_id(arguments.arxiv)
    title = normalize_text(arguments.title)
    if not title:
        raise PipelineError("The new title must not be empty.")
    latex_title = arguments.latex_title or latex_escape_title(title)
    if arguments.latex_title and latex_title_to_plain(latex_title) != title:
        raise PipelineError(
            "--latex-title must have the same text as --title after standard LaTeX "
            "character escapes are removed."
        )
    cv_dir = arguments.cv_dir.expanduser().resolve()
    cv_tex_path = cv_dir / CV_TEX_NAME
    cv_pdf_path = cv_dir / CV_PDF_NAME
    if not cv_tex_path.is_file():
        raise PipelineError(f"CV source not found: {cv_tex_path}")

    url = f"https://arxiv.org/abs/{arxiv_id}"
    website_snapshot = ABOUT_PAGE.read_bytes()
    cv_snapshot = cv_tex_path.read_bytes()
    website_original = website_snapshot.decode("utf-8")
    cv_original = cv_snapshot.decode("utf-8")
    existing_entries = validate_preprint_documents(website_original, cv_original)
    if arxiv_id in existing_entries:
        if arguments.coauthor is not None or arguments.solo or arguments.year is not None:
            raise PipelineError(
                "--coauthor, --solo, and --year are only used when adding a new preprint."
            )
        website_updated, website_old_title = replace_title_in_section(
            website_original,
            start_marker="## Preprints",
            end_marker="## Publications",
            url=url,
            title=title,
            prefix="1. ",
            link_token="[[preprint](",
            label="website Preprints",
        )
        cv_updated, cv_old_title = replace_title_in_section(
            cv_original,
            start_marker=r"\cvsection{Preprints}",
            end_marker=r"\cvsection{Talks}",
            url=url,
            title=latex_title,
            prefix=r"\item ",
            link_token=r"\paperlink{",
            label="CV Preprints",
        )
        if latex_title_to_plain(cv_old_title) != website_old_title:
            raise PipelineError(
                "The existing website and CV titles already disagree; run the check "
                "command and resolve that mismatch before updating."
            )
        unchanged = website_updated == website_original and cv_updated == cv_original
        print(f"Update existing preprint: arXiv {arxiv_id}")
        print(f"Old title: {website_old_title}")
        print(f"New title: {title}")
    else:
        coauthors, year, metadata_source = resolve_new_preprint_metadata(
            arguments, arxiv_id, title
        )
        coauthor_text = format_name_list(coauthors)
        website_author_suffix = f" (with {coauthor_text})" if coauthor_text else ""
        cv_author_suffix = latex_escape_title(website_author_suffix)
        website_line = (
            f"1. {title}{website_author_suffix}, {year} "
            f"[[preprint]({url})]\n"
        )
        cv_line = (
            f"  \\item {latex_title}{cv_author_suffix}, {year} "
            f"\\paperlink{{{url}}}{{preprint}}\n"
        )
        website_updated = insert_ordered_preprint(
            website_original,
            arxiv_id=arxiv_id,
            entry_line=website_line,
            start_marker="## Preprints",
            end_marker="## Publications",
            link_token="[[preprint](",
            label="website Preprints",
        )
        cv_updated = insert_ordered_preprint(
            cv_original,
            arxiv_id=arxiv_id,
            entry_line=cv_line,
            start_marker=r"\cvsection{Preprints}",
            end_marker=r"\cvsection{Talks}",
            link_token=r"\paperlink{",
            label="CV Preprints",
        )
        validate_preprint_documents(website_updated, cv_updated)
        unchanged = False
        all_authors = format_name_list((CV_OWNER, *coauthors))
        print(f"Add new preprint: arXiv {arxiv_id}")
        print(f"Title: {title}")
        print(f"Authors: {all_authors}")
        print(f"Year: {year} ({metadata_source})")

    if arguments.dry_run:
        if unchanged:
            print("Dry run complete; both files already use this title.")
        else:
            print("Dry run complete; no files were changed and no PDF was built.")
        return
    if unchanged:
        raise PipelineError(f"arXiv {arxiv_id} already has the requested title in both files.")

    if arguments.stage:
        ensure_staging_clear()
    ensure_repo_targets_clean([ABOUT_PAGE, WEBSITE_PDF])
    pdf_original = WEBSITE_PDF.read_bytes()
    cv_pdf_original = cv_pdf_path.read_bytes() if cv_pdf_path.exists() else None
    pdf_bytes, page_count = build_cv(cv_dir=cv_dir, tex_text=cv_updated)
    ensure_snapshot_unchanged(cv_tex_path, cv_snapshot)
    ensure_snapshot_unchanged(ABOUT_PAGE, website_snapshot)
    ensure_snapshot_unchanged(WEBSITE_PDF, pdf_original)
    ensure_optional_snapshot_unchanged(cv_pdf_path, cv_pdf_original)

    try:
        atomic_write_text(cv_tex_path, cv_updated)
        atomic_write_text(ABOUT_PAGE, website_updated)
        atomic_write_bytes(cv_pdf_path, pdf_bytes)
        atomic_write_bytes(WEBSITE_PDF, pdf_bytes)
        check_consistency(cv_dir=cv_dir)
    except BaseException:
        atomic_write_text(cv_tex_path, cv_original)
        atomic_write_text(ABOUT_PAGE, website_original)
        restore_optional_snapshot(cv_pdf_path, cv_pdf_original)
        atomic_write_bytes(WEBSITE_PDF, pdf_original)
        raise

    print(f"Updated website, CV source, and both {page_count}-page CV PDFs.")
    if arguments.stage:
        try:
            staged = stage_exact([ABOUT_PAGE, WEBSITE_PDF])
        except PipelineError as error:
            raise PipelineError(
                "The content update succeeded, but automatic staging failed. "
                f"Review and stage the website files manually. Details: {error}"
            ) from error
        if staged:
            print("Staged only " + ", ".join(sorted(staged)) + ".")
        else:
            print("The generated website files are unchanged; there was nothing to stage.")


def build_command(arguments: argparse.Namespace) -> None:
    cv_dir = arguments.cv_dir.expanduser().resolve()
    cv_tex_path = cv_dir / CV_TEX_NAME
    cv_pdf_path = cv_dir / CV_PDF_NAME
    if not cv_tex_path.is_file():
        raise PipelineError(f"CV source not found: {cv_tex_path}")
    if arguments.keep_dir:
        arguments.keep_dir = validate_keep_dir(arguments.keep_dir, cv_dir)
    check_consistency(cv_dir=cv_dir, require_pdf=False)
    if not arguments.check_only:
        if arguments.stage:
            ensure_staging_clear()
        ensure_repo_targets_clean([WEBSITE_PDF])
    website_snapshot = ABOUT_PAGE.read_bytes()
    cv_snapshot = cv_tex_path.read_bytes()
    pdf_original = WEBSITE_PDF.read_bytes() if WEBSITE_PDF.exists() else None
    cv_pdf_original = cv_pdf_path.read_bytes() if cv_pdf_path.exists() else None
    tex_text = cv_snapshot.decode("utf-8")
    pdf_bytes, page_count = build_cv(
        cv_dir=cv_dir,
        tex_text=tex_text,
        keep_dir=arguments.keep_dir,
    )
    if arguments.check_only:
        print(f"Scratch build passed ({page_count} pages); website PDF was not changed.")
        if arguments.keep_dir:
            print(f"Kept verification artifacts in {arguments.keep_dir}.")
        return

    ensure_snapshot_unchanged(cv_tex_path, cv_snapshot)
    ensure_snapshot_unchanged(ABOUT_PAGE, website_snapshot)
    ensure_optional_snapshot_unchanged(WEBSITE_PDF, pdf_original)
    ensure_optional_snapshot_unchanged(cv_pdf_path, cv_pdf_original)
    try:
        atomic_write_bytes(cv_pdf_path, pdf_bytes)
        atomic_write_bytes(WEBSITE_PDF, pdf_bytes)
        check_consistency(cv_dir=cv_dir)
    except BaseException:
        restore_optional_snapshot(cv_pdf_path, cv_pdf_original)
        restore_optional_snapshot(WEBSITE_PDF, pdf_original)
        raise
    print(f"Installed and verified both {page_count}-page CV PDFs.")
    if arguments.stage:
        try:
            staged = stage_exact([WEBSITE_PDF])
        except PipelineError as error:
            raise PipelineError(
                "The PDF update succeeded, but automatic staging failed. "
                f"Review and stage the website PDF manually. Details: {error}"
            ) from error
        if staged:
            print("Staged only " + ", ".join(sorted(staged)) + ".")
        else:
            print("The rebuilt PDF is unchanged; there was nothing to stage.")


def check_command(arguments: argparse.Namespace) -> None:
    cv_dir = arguments.cv_dir.expanduser().resolve()
    page_count = check_consistency(cv_dir=cv_dir)
    entries = website_preprints(ABOUT_PAGE.read_text(encoding="utf-8"))
    print(
        f"Consistency check passed: {len(entries)} preprints, homepage CV link, "
        f"and identical {page_count}-page CV PDFs."
    )


def parser() -> argparse.ArgumentParser:
    default_cv_dir = Path.home() / "Desktop" / "CV"
    argument_parser = argparse.ArgumentParser(
        description="Update the LaTeX CV and website together, then build and verify the PDF."
    )
    subparsers = argument_parser.add_subparsers(dest="command", required=True)

    preprint = subparsers.add_parser(
        "preprint", help="add a new preprint or update an existing preprint title."
    )
    preprint.add_argument("arxiv", help="arXiv ID or canonical abs/pdf URL")
    preprint.add_argument("--title", required=True, help="verified current title from arXiv")
    preprint.add_argument(
        "--latex-title",
        help="optional LaTeX-form title override for titles containing mathematics",
    )
    preprint.add_argument(
        "--coauthor",
        action="append",
        metavar="NAME",
        help="coauthor for an offline new-paper addition; repeat in arXiv author order",
    )
    preprint.add_argument(
        "--solo",
        action="store_true",
        help="declare an offline new-paper addition to be sole-authored",
    )
    preprint.add_argument(
        "--year",
        type=int,
        choices=range(2007, 2100),
        metavar="YYYY",
        help="optional year override for a new preprint",
    )
    preprint.add_argument("--cv-dir", type=Path, default=default_cv_dir)
    preprint.add_argument("--dry-run", action="store_true")
    preprint.add_argument(
        "--stage",
        action="store_true",
        help="stage only _pages/about.md and Lai_Lexiao_CV.pdf after success",
    )
    preprint.set_defaults(function=update_preprint)

    build = subparsers.add_parser(
        "build", help="rebuild the website PDF after other CV source changes."
    )
    build.add_argument("--cv-dir", type=Path, default=default_cv_dir)
    build.add_argument(
        "--check-only",
        action="store_true",
        help="build and validate in scratch space without replacing the website PDF",
    )
    build.add_argument(
        "--keep-dir",
        type=Path,
        help="with --check-only, retain the scratch PDF and page PNGs here",
    )
    build.add_argument(
        "--stage", action="store_true", help="stage only Lai_Lexiao_CV.pdf after success"
    )
    build.set_defaults(function=build_command)

    check = subparsers.add_parser(
        "check", help="verify preprint titles, homepage link, PDF links, and rendering."
    )
    check.add_argument("--cv-dir", type=Path, default=default_cv_dir)
    check.set_defaults(function=check_command)
    return argument_parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = parser().parse_args(argv)
    if getattr(arguments, "keep_dir", None) and not getattr(arguments, "check_only", False):
        raise PipelineError("--keep-dir requires --check-only.")
    if getattr(arguments, "stage", False) and (
        getattr(arguments, "dry_run", False) or getattr(arguments, "check_only", False)
    ):
        raise PipelineError("--stage cannot be combined with --dry-run or --check-only.")
    arguments.function(arguments)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PipelineError as error:
        print(f"CV pipeline error: {error}", file=sys.stderr)
        raise SystemExit(1)
