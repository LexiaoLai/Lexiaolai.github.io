import importlib.util
import io
import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "cv_pipeline.py"
SPEC = importlib.util.spec_from_file_location("cv_pipeline", SCRIPT)
assert SPEC and SPEC.loader
cv_pipeline = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cv_pipeline)


class CvPipelineTests(unittest.TestCase):
    def test_normalize_arxiv_id(self):
        self.assertEqual(cv_pipeline.normalize_arxiv_id("2605.14345"), "2605.14345")
        self.assertEqual(
            cv_pipeline.normalize_arxiv_id("https://arxiv.org/abs/2605.14345v2"),
            "2605.14345",
        )
        with self.assertRaises(cv_pipeline.PipelineError):
            cv_pipeline.normalize_arxiv_id("not-an-arxiv-id")
        self.assertEqual(
            cv_pipeline.normalize_arxiv_id("https://arxiv.org/pdf/2605.14345.pdf"),
            "2605.14345",
        )

    def test_replace_website_title_preserves_suffix(self):
        source = (
            "1. Old title (with A. Author), 2026 "
            "[[preprint](https://arxiv.org/abs/2605.14345)]\n"
        )
        updated, old = cv_pipeline.replace_title_for_url(
            source,
            url="https://arxiv.org/abs/2605.14345",
            title="New title",
            prefix="1. ",
            link_token="[[preprint](",
            label="website",
        )
        self.assertEqual(old, "Old title")
        self.assertEqual(
            updated,
            "1. New title (with A. Author), 2026 "
            "[[preprint](https://arxiv.org/abs/2605.14345)]\n",
        )

    def test_replace_cv_title_preserves_latex_suffix(self):
        source = (
            r"  \item Old title (with C\'edric Josz), 2026 "
            r"\paperlink{https://arxiv.org/abs/2605.14345}{preprint}"
            "\n"
        )
        updated, old = cv_pipeline.replace_title_for_url(
            source,
            url="https://arxiv.org/abs/2605.14345",
            title=r"New \& improved title",
            prefix=r"\item ",
            link_token=r"\paperlink{",
            label="CV",
        )
        self.assertEqual(old, "Old title")
        self.assertIn(r"\item New \& improved title (with C\'edric Josz)", updated)

    def test_rejects_ambiguous_matches(self):
        source = (
            "1. First (with A), 2026 [[preprint](https://arxiv.org/abs/2605.14345)]\n"
            "1. Second (with B), 2026 [[preprint](https://arxiv.org/abs/2605.14345)]\n"
        )
        with self.assertRaises(cv_pipeline.PipelineError):
            cv_pipeline.replace_title_for_url(
                source,
                url="https://arxiv.org/abs/2605.14345",
                title="New",
                prefix="1. ",
                link_token="[[preprint](",
                label="website",
            )

    def test_does_not_match_a_longer_arxiv_id(self):
        source = (
            "1. Different paper (with A), 2026 "
            "[[preprint](https://arxiv.org/abs/1234.56789)]\n"
        )
        with self.assertRaises(cv_pipeline.PipelineError):
            cv_pipeline.replace_title_for_url(
                source,
                url="https://arxiv.org/abs/1234.5678",
                title="Wrongly selected",
                prefix="1. ",
                link_token="[[preprint](",
                label="website",
            )

    def test_latex_title_round_trip(self):
        title = r"Rates for A&B_1 at 50%: #2 costs $5"
        self.assertEqual(
            cv_pipeline.latex_title_to_plain(cv_pipeline.latex_escape_title(title)),
            title,
        )

    def test_pdf_url_check_respects_id_boundary(self):
        listing = "https://arxiv.org/abs/1234.56789\n"
        self.assertFalse(cv_pipeline.contains_arxiv_url(listing, "1234.5678"))
        self.assertTrue(cv_pipeline.contains_arxiv_url(listing, "1234.56789"))
        self.assertTrue(
            cv_pipeline.contains_arxiv_url(
                "https://arxiv.org/abs/1234.5678v3.pdf\n", "1234.5678"
            )
        )

    def test_keep_dir_rejects_live_outputs_and_nonempty_directories(self):
        cv_dir = Path.home() / "Desktop" / "CV"
        with self.assertRaises(cv_pipeline.PipelineError):
            cv_pipeline.validate_keep_dir(cv_pipeline.REPO_ROOT, cv_dir)
        with tempfile.TemporaryDirectory() as temporary:
            occupied = Path(temporary) / "occupied"
            occupied.mkdir()
            (occupied / "existing.txt").write_text("keep", encoding="utf-8")
            with self.assertRaises(cv_pipeline.PipelineError):
                cv_pipeline.validate_keep_dir(occupied, cv_dir)

    def test_snapshot_guard_detects_a_concurrent_edit(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "source.tex"
            path.write_bytes(b"before")
            cv_pipeline.ensure_snapshot_unchanged(path, b"before")
            path.write_bytes(b"after")
            with self.assertRaises(cv_pipeline.PipelineError):
                cv_pipeline.ensure_snapshot_unchanged(path, b"before")

    def test_parses_official_arxiv_html_metadata(self):
        document = """
        <meta name="citation_title" content="Nonsmooth Optimization via Orthogonalized Momentum">
        <meta name="citation_author" content="Lai, Lexiao">
        <meta name="citation_author" content="Lin, Tianyi">
        <meta name="citation_author" content="Zhang, Jiayu">
        <meta name="citation_date" content="2026/09/12">
        <meta name="citation_arxiv_id" content="2609.13677">
        """
        metadata = cv_pipeline.parse_arxiv_html(document, "2609.13677")
        self.assertEqual(metadata.title, "Nonsmooth Optimization via Orthogonalized Momentum")
        self.assertEqual(metadata.authors, ("Lexiao Lai", "Tianyi Lin", "Jiayu Zhang"))
        self.assertEqual(metadata.year, 2026)

    def test_inserts_new_preprint_in_descending_arxiv_order(self):
        source = (
            "## Preprints\n"
            "1. May paper (with A), 2026 "
            "[[preprint](https://arxiv.org/abs/2605.14345)]\n"
            "1. January paper (with B), 2026 "
            "[[preprint](https://arxiv.org/abs/2601.21487)]\n\n"
            "## Publications\n"
        )
        new_line = (
            "1. September paper (with C and D), 2026 "
            "[[preprint](https://arxiv.org/abs/2609.13677)]\n"
        )
        updated = cv_pipeline.insert_ordered_preprint(
            source,
            arxiv_id="2609.13677",
            entry_line=new_line,
            start_marker="## Preprints",
            end_marker="## Publications",
            link_token="[[preprint](",
            label="website Preprints",
        )
        self.assertLess(updated.index("2609.13677"), updated.index("2605.14345"))
        self.assertLess(updated.index("2605.14345"), updated.index("2601.21487"))

    def test_offline_coauthors_bypass_metadata_fetch(self):
        arguments = Namespace(
            coauthor=["Tianyi Lin", "Jiayu Zhang"],
            solo=False,
            year=None,
        )
        with mock.patch.object(
            cv_pipeline,
            "fetch_arxiv_metadata",
            side_effect=AssertionError("network should not be used"),
        ):
            coauthors, year, source = cv_pipeline.resolve_new_preprint_metadata(
                arguments,
                "2609.13677",
                "Nonsmooth Optimization via Orthogonalized Momentum",
            )
        self.assertEqual(coauthors, ("Tianyi Lin", "Jiayu Zhang"))
        self.assertEqual(year, 2026)
        self.assertEqual(source, "command-line metadata")

    def test_new_preprint_dry_run_uses_metadata_without_writes(self):
        website = (
            "[[Curriculum Vitae](/Lai_Lexiao_CV.pdf)]\n\n"
            "## Preprints\n"
            "1. Older paper (with A), 2026 "
            "[[preprint](https://arxiv.org/abs/2605.14345)]\n\n"
            "## Publications\n"
        )
        cv_source = (
            r"\cvsection{Preprints}" "\n"
            r"\begin{cvnumbered}" "\n"
            r"  \item Older paper (with A), 2026 "
            r"\paperlink{https://arxiv.org/abs/2605.14345}{preprint}" "\n"
            r"\end{cvnumbered}" "\n\n"
            r"\cvsection{Talks}" "\n"
        )
        metadata = cv_pipeline.ArxivMetadata(
            "2609.13677",
            "Nonsmooth Optimization via Orthogonalized Momentum",
            ("Lexiao Lai", "Tianyi Lin", "Jiayu Zhang"),
            2026,
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            about = root / "about.md"
            cv_dir = root / "CV"
            cv_dir.mkdir()
            cv_tex = cv_dir / cv_pipeline.CV_TEX_NAME
            about.write_text(website, encoding="utf-8")
            cv_tex.write_text(cv_source, encoding="utf-8")
            arguments = Namespace(
                arxiv="2609.13677",
                title="Nonsmooth Optimization via Orthogonalized Momentum",
                latex_title=None,
                cv_dir=cv_dir,
                dry_run=True,
                stage=False,
                coauthor=None,
                solo=False,
                year=None,
            )
            output = io.StringIO()
            with mock.patch.object(cv_pipeline, "ABOUT_PAGE", about), mock.patch.object(
                cv_pipeline, "fetch_arxiv_metadata", return_value=metadata
            ), redirect_stdout(output):
                cv_pipeline.update_preprint(arguments)
            self.assertEqual(about.read_text(encoding="utf-8"), website)
            self.assertEqual(cv_tex.read_text(encoding="utf-8"), cv_source)
            self.assertIn("Add new preprint: arXiv 2609.13677", output.getvalue())


if __name__ == "__main__":
    unittest.main()
