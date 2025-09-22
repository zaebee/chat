# Implementation Strategy

- Store diagrams in Markdown with Mermaid blocks.
- Use GitHub/GitLab for Mermaid rendering or an external renderer in CI.
- The assembly process (ATCG) parses `core/honey.md` and collects the final document using `@include` directives.
- Possible: programmatic generation of Mermaid from metadata (Python scripts).
- Recommendation: add linting for `core/honey.md` (checking links and order).

## How to Assemble Documentation (ATCG Workflow)

To assemble the complete Hive architectural documentation, follow these steps:

1.  **Ensure `core/honey.md` is up-to-date:** This file acts as the manifest, defining the order and content of the final document.
2.  **Run the ATCG Assembly Tool:** Execute the designated script (e.g., `python tools/assemble_docs.py`) that parses `core/honey.md` and concatenates the included files.
3.  **Generate Output:** The tool will produce a single Markdown file (e.g., `final_hive_docs.md`) containing the assembled documentation.
4.  **Render Diagrams (Optional):** If a visual output (HTML, PDF) is desired, use a Mermaid renderer (e.g., `mermaid-cli`) to convert the assembled Markdown file into the desired format.

This process ensures that the documentation is always consistent and reflects the latest architectural state.
