# Implementation Strategy

- Store diagrams in Markdown with Mermaid blocks.
- Use GitHub/GitLab for Mermaid rendering or an external renderer in CI.
- The assembly process (ATCG) parses `core/honey.md` and collects the final document using `@include` directives.
- Possible: programmatic generation of Mermaid from metadata (Python scripts).
- Recommendation: add linting for `core/honey.md` (checking links and order).
