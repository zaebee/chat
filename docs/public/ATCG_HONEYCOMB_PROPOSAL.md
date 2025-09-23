# Proposal: ATCG Honeycomb - A Standard for Hive Architecture Documentation

## 1. Abstract

This document proposes a minimum standard for organizing the architectural documentation of the Hive project. It describes a repository structure, a central manifest (the "Honeycomb Manifest"), and the contents of the files from which the ATCG system will assemble the final documentation. This proposal is intended for Bee-to-Peer review.

## 2. Scope

-   **Single Source of Truth:** `core/honey.md` will manage the assembly order.
-   **Minimal `docs/` Structure:** A minimal set of files in `docs/` will cover the architecture overview, component descriptions, data structures, review processes, and implementation strategy.
-   **CI/CD Support:** The structure is designed to be compatible with CI/CD for automated validation and rendering.

## 3. Repository Structure

```text
hive-architecture/
├── core/
│   └── honey.md
└── docs/
    └── 01_ARCHITECTURE/
        ├── OVERVIEW.md
        ├── COMPONENTS/
        │   └── CONNECTOR.md
        ├── DATA_STRUCTURES/
        │   └── POLLEN_EVENT.md
        ├── PROCESS/
        │   └── REVIEW.md
        └── IMPLEMENTATION/
            └── STRATEGY.md
```

## 4. Core Honey Manifest (`core/honey.md`)

The `core/honey.md` file will define the order of inclusion for the documentation sections. The ATCG assembler will parse `@include` directives to build the final document.

```markdown
# Hive Architecture Honeycomb (ATCG Assembly Manifest)

This document is the "honeycomb" (Honey).
ATCG uses it as a plan for assembling the final documentation.

---

## 1. Overview
@include: ../docs/01_ARCHITECTURE/OVERVIEW.md

---

## 2. Components

### 2.1 Connector
@include: ../docs/01_ARCHITECTURE/COMPONENTS/CONNECTOR.md

---

## 3. Data Structures

### 3.1 Pollen Event
@include: ../docs/01_ARCHITECTURE/DATA_STRUCTURES/POLLEN_EVENT.md

---

## 4. Review & Development Process
@include: ../docs/01_ARCHITECTURE/PROCESS/REVIEW.md

---

## 5. Implementation Strategy
@include: ../docs/01_ARCHITECTURE/IMPLEMENTATION/STRATEGY.md
```

## 5. Assembly Workflow (ATCG)

1.  `core/honey.md` defines the order of sections.
2.  The ATCG assembler parses `@include` directives and assembles the final Markdown document.
3.  Mermaid diagrams within the markdown files are rendered natively by GitHub or via a CI process (e.g., using `mermaid-cli`).
4.  The result is a single HTML/PDF/Markdown document for review and publication.

## 6. Decision Rationale

-   **Separation of Manifest and Content:** Separating `core/honey.md` from the content makes managing the documentation structure easier.
-   **Modular `docs/` Structure:** The `docs/` structure makes individual files readable and independently editable.
-   **Mermaid in Markdown:** Provides quick visual access to diagrams directly in the Git hosting platform.
-   **ATCG Assembler:** A universal assembly step that can be adapted for CI.

## 7. Bee-to-Peer Review Checklist

-   [ ] Is the order of sections in `core/honey.md` correct?
-   [ ] Are the examples sufficient for understanding the architecture?
-   [ ] Are additional components needed in `COMPONENTS/`?
-   [ ] Are there suggestions for adding linting or CI checks?
-   [ ] Is the Decision Rationale clear?
