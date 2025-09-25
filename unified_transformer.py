import bleach
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from typing import Dict


class UnifiedMarkdownToHtmlTransformation:
    def __init__(self):
        self.md = (
            MarkdownIt(
                "gfm-like",
                {
                    "linkify": True,
                    "typographer": True,
                    "html": True,
                },
            )
            .use(front_matter_plugin)
            .use(footnote_plugin)
            .use(tasklists_plugin)
        )
        self.allowed_tags = [
            "p",
            "strong",
            "em",
            "code",
            "pre",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "ul",
            "ol",
            "li",
            "a",
            "blockquote",
            "hr",
            "br",
            "img",
            "table",
            "thead",
            "tbody",
            "tr",
            "th",
            "td",
            "span",
            "div",
            "sup",
            "sub",
        ]
        self.allowed_attrs = {
            "*": ["class", "id"],
            "a": ["href", "title", "target", "rel"],
            "img": ["src", "alt", "title"],
        }

    def transform(
        self, markdown_content: str, html_template: str, metadata: Dict[str, str]
    ) -> str:
        # Render markdown to HTML
        html_content = self.md.render(markdown_content)

        # Sanitize the HTML content
        sanitized_html = bleach.clean(
            html_content,
            tags=self.allowed_tags,
            attributes=self.allowed_attrs,
        )

        # Populate template
        output_html = html_template
        for key, value in metadata.items():
            output_html = output_html.replace(f"{{{key}}}", value)
        output_html = output_html.replace("{REPORT_CONTENT}", sanitized_html)

        return output_html
