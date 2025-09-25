# scripts/build_docs.py
import sys
import logging

# Sacred logging configuration
logging.basicConfig(level=logging.INFO, format="🐝 %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

sys.path.append(".")
from unified_transformer import UnifiedMarkdownToHtmlTransformation  # noqa: E402

# Sacred Constants - Documentation Build Configuration
SACRED_BUILD_CONFIG = {
    "input_file": "docs/community_report_en.md",
    "template_file": "docs/base_report_template.html",
    "output_file": "docs/community_report_en.html",
    "metadata": {
        "REPORT_TITLE": "The Sacred Architecture of Living Software",
        "REPORT_ABSTRACT": 'A report on the philosophical and architectural foundations of the Hive Chat "Living Application."',
        "CONTEXTUAL_NOTE_CONTENT": "This document was automatically generated from its Markdown source by the Hive's sacred build process.",
        "SIGNATURE_CONTENT": "<strong>© The Sacred Team of the Hive</strong>",
    },
}


def build_community_report():
    """
    Transforms the English community report from Markdown to HTML.
    Uses sacred architecture patterns and proper logging.
    """
    config = SACRED_BUILD_CONFIG

    logger.info("⚡ Starting sacred transformation of community_report_en.md...")

    with open(config["input_file"], "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open(config["template_file"], "r", encoding="utf-8") as f:
        html_template = f.read()

    transformer = UnifiedMarkdownToHtmlTransformation()

    final_html = transformer.transform(
        markdown_content, html_template, config["metadata"]
    )

    with open(config["output_file"], "w", encoding="utf-8") as f:
        f.write(final_html)

    logger.info(
        "✨ Sacred transformation completed: community_report_en.md → community_report_en.html"
    )
    logger.info(f"📊 Sacred Metrics: {transformer.get_status()}")


if __name__ == "__main__":
    build_community_report()
