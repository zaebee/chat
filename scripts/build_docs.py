# scripts/build_docs.py
import sys

sys.path.append(".")
from unified_transformer import UnifiedMarkdownToHtmlTransformation  # noqa: E402


def build_community_report():
    """
    Transforms the English community report from Markdown to HTML.
    """
    print("Starting transformation of community_report_en.md...")

    with open("docs/community_report_en.md", "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open("docs/base_report_template.html", "r", encoding="utf-8") as f:
        html_template = f.read()

    transformer = UnifiedMarkdownToHtmlTransformation()

    metadata = {
        "REPORT_TITLE": "The Sacred Architecture of Living Software",
        "REPORT_ABSTRACT": 'A report on the philosophical and architectural foundations of the Hive Chat "Living Application."',
        "CONTEXTUAL_NOTE_CONTENT": "This document was automatically generated from its Markdown source by the Hive's sacred build process.",
        "SIGNATURE_CONTENT": "<strong>© The Sacred Team of the Hive</strong>",
    }

    final_html = transformer.transform(markdown_content, html_template, metadata)

    with open("docs/community_report_en.html", "w", encoding="utf-8") as f:
        f.write(final_html)

    print("Successfully transformed community_report_en.md to community_report_en.html")


if __name__ == "__main__":
    build_community_report()
