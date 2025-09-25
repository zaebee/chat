import bleach
import time
import logging
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, Any

from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.tasklists import tasklists_plugin

from hive.events import PollenEvent

logger = logging.getLogger(__name__)


@dataclass
class SacredMetrics:
    """Sacred Metrics (τ, φ, σ) for Documentation System"""

    tau: float = 0.0  # System complexity/stress
    phi: float = 0.0  # Code quality/maintainability
    sigma: float = 0.0  # Collaboration efficiency
    trinity_score: float = 0.0  # f(τ,φ,σ)
    timestamp: str = ""


class UnifiedMarkdownToHtmlTransformation:
    """
    ATCG-aligned documentation transformer with Sacred Metrics.

    Architecture:
    - Aggregate: State management for transformation pipeline
    - Transformation: Pure markdown processing functions
    - Connector: File I/O and template system
    - Genesis: Event emission for documentation updates
    """

    def __init__(self, name: str = "DocTransformer"):
        # Aggregate State
        self.name = name
        self.transformation_count = 0
        self.error_count = 0
        self.total_processing_time = 0.0
        self.created_at = datetime.now().isoformat()

        # Transformation Configuration
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

        logger.info(f"🐝 Sacred Documentation Transformer '{self.name}' initialized")

    def transform(
        self, markdown_content: str, html_template: str, metadata: Dict[str, str]
    ) -> str:
        """
        ATCG Transformation Pipeline with Sacred Metrics tracking.

        Genesis Event: documentation_transformed will be emitted.
        """
        start_time = time.time()

        try:
            # Transformation: Pure markdown processing
            html_content = self._render_markdown(markdown_content)

            # Transformation: Security sanitization
            sanitized_html = self._sanitize_html(html_content)

            # Connector: Template population
            output_html = self._populate_template(
                html_template, metadata, sanitized_html
            )

            # Update Sacred Metrics
            processing_time = time.time() - start_time
            self.transformation_count += 1
            self.total_processing_time += processing_time

            # Genesis Event: Emit transformation success
            self._emit_genesis_event(
                "documentation_transformed",
                {
                    "input_length": len(markdown_content),
                    "output_length": len(output_html),
                    "processing_time": processing_time,
                    "transformation_id": self.transformation_count,
                },
            )

            logger.info(
                f"📄 Documentation transformed: {len(markdown_content)} → {len(output_html)} chars in {processing_time:.3f}s"
            )

            return output_html

        except Exception as e:
            self.error_count += 1
            processing_time = time.time() - start_time
            self.total_processing_time += processing_time

            logger.error(f"🚫 Documentation transformation failed: {e}")
            self._emit_genesis_event(
                "documentation_transform_failed",
                {"error": str(e), "processing_time": processing_time},
            )
            raise

    def _render_markdown(self, markdown_content: str) -> str:
        """Transformation: Pure markdown to HTML conversion"""
        return self.md.render(markdown_content)

    def _sanitize_html(self, html_content: str) -> str:
        """Transformation: Security sanitization"""
        return bleach.clean(
            html_content,
            tags=self.allowed_tags,
            attributes=self.allowed_attrs,
        )

    def _populate_template(
        self, template: str, metadata: Dict[str, str], content: str
    ) -> str:
        """Connector: Template population and metadata injection"""
        output_html = template
        for key, value in metadata.items():
            output_html = output_html.replace(f"{{{key}}}", value)
        output_html = output_html.replace("{REPORT_CONTENT}", content)
        return output_html

    def _emit_genesis_event(self, event_type: str, payload: Dict[str, Any]):
        """Genesis Event: Pollen Protocol event emission"""
        try:
            PollenEvent(
                event_type=event_type,
                aggregate_id=self.name,
                payload=payload,
                source_component="DocumentationTransformer",
            )
            logger.debug(f"🌸 Genesis Event: {event_type}")
        except Exception as e:
            logger.warning(f"Genesis event emission failed: {e}")

    def calculate_sacred_metrics(self) -> SacredMetrics:
        """Calculate Sacred Metrics (τ, φ, σ) for system health"""
        if self.transformation_count == 0:
            return SacredMetrics(timestamp=datetime.now().isoformat())

        # τ (tau): System complexity based on error rate and processing time
        error_rate = self.error_count / self.transformation_count
        avg_processing_time = self.total_processing_time / self.transformation_count
        tau = min(1.0, error_rate * 2.0 + (avg_processing_time * 0.1))

        # φ (phi): Code quality based on success rate and efficiency
        success_rate = 1.0 - error_rate
        phi = success_rate * max(0.0, 1.0 - (avg_processing_time * 0.05))

        # σ (sigma): Collaboration efficiency based on throughput
        sigma = min(1.0, self.transformation_count * 0.1) * success_rate

        # Trinity Safety Score: f(τ,φ,σ) = (φ + σ) * (1 - τ/2) / 2
        trinity_score = (phi + sigma) * (1.0 - tau / 2.0) / 2.0

        return SacredMetrics(
            tau=tau,
            phi=phi,
            sigma=sigma,
            trinity_score=trinity_score,
            timestamp=datetime.now().isoformat(),
        )

    def get_status(self) -> Dict[str, Any]:
        """Sacred observability: Complete system status"""
        metrics = self.calculate_sacred_metrics()

        return {
            "name": self.name,
            "architecture": "ATCG",
            "transformations": self.transformation_count,
            "errors": self.error_count,
            "success_rate": 1.0
            - (self.error_count / max(1, self.transformation_count)),
            "avg_processing_time": self.total_processing_time
            / max(1, self.transformation_count),
            "sacred_metrics": {
                "tau": round(metrics.tau, 3),
                "phi": round(metrics.phi, 3),
                "sigma": round(metrics.sigma, 3),
                "trinity_score": round(metrics.trinity_score, 3),
            },
            "created_at": self.created_at,
            "sage_wisdom": "🐝 Documentation is the bridge between vision and understanding",
        }
