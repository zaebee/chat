# 🍯 Honeypot Separation Strategy
*Clean rect-to-hexa core with no dirty mixing*

## 🎯 Core Principle: "No Dirty in the Honeypot"

The documentation core (`docs/`) must remain **pure markdown** with minimal Jekyll-compatible frontmatter. All interactive elements, JavaScript, and complex HTML should be generated through `.github` workflows for static site building.

## 📐 Rect-to-Hexa Architecture

### 🔲 RECT (Rectangular) - Core Documentation
**Pure Markdown Content Only**
```
docs/
├── README.md                    # Pure MD with minimal frontmatter
├── 00_FOUNDATION/              # Core principles, pure text
├── 01_ARCHITECTURE/            # System design, diagrams as MD
├── 02_DEVELOPMENT/             # Setup guides, pure instructions
├── 03_API/                     # API docs, code examples in fenced blocks
├── sacred-team/                # Team docs, pure narratives
└── _config.yml                 # Jekyll config only
```

### [⬢⬡⬢⬡] HEXA (Hexagonal) - Generated Enhancements
**Built via .github Workflows**
```
.github/workflows/
├── jekyll-build.yml            # Static site generation
├── docs-enhancement.yml        # Add interactive elements
├── mermaid-generation.yml      # Convert text diagrams to SVG
└── honeypot-validation.yml     # Ensure core purity
```

## 🚫 What Must Be Removed from Core

### ❌ Jekyll Liquid Includes
```markdown
# REMOVE from docs/
{% include language-switcher.html %}
{% include sacred-navigation.html %}
<div class="language-content" data-lang="en">
```

### ❌ HTML/CSS in Markdown
```markdown
# REMOVE from docs/
<div class="sacred-theme">
<script src="...">
<style>...</style>
```

### ❌ JavaScript Files
```
# MOVE OUT of docs/
docs/assets/js/hive-interactive-navigation.js
docs/archive/temporary/tales_v2_implementation.ts
```

### ❌ Complex Frontmatter
```yaml
# SIMPLIFY in docs/
# Remove: interactive_nav, sacred_theme, mermaid_enhanced, etc.
# Keep only: title, description, category
```

## ✅ What Stays in Core

### ✅ Pure Markdown Content
```markdown
# Clean Documentation
- Plain text narratives
- Fenced code blocks
- Simple tables
- Basic links and images
```

### ✅ Minimal Frontmatter
```yaml
---
title: "Document Title"
description: "Brief description"
category: "foundation|architecture|development|api"
---
```

### ✅ Text-Based Diagrams
```markdown
# Convert to plain text, let workflows generate visuals
```

## 🔄 Transformation Strategy

### Phase 1: Core Purification
1. **Strip Jekyll Liquid** from all MD files
2. **Remove HTML/CSS** embedded in markdown
3. **Simplify frontmatter** to essential fields only
4. **Convert complex elements** to plain text descriptions

### Phase 2: Workflow Enhancement
1. **Jekyll build workflow** for static site generation
2. **Mermaid conversion** workflow for diagrams
3. **Interactive enhancement** workflow for UI elements
4. **Validation workflow** to ensure core purity

### Phase 3: Honeypot Validation
1. **Automated checks** for dirty content in core
2. **Pure markdown validation** in CI/CD
3. **Separation enforcement** via GitHub Actions
4. **Clean build verification** for static site

## 🏗️ .github Workflow Architecture

### `jekyll-build.yml`
```yaml
# Generate static site from pure markdown
# Add navigation, styling, interactive elements
# Deploy to GitHub Pages or static hosting
```

### `docs-enhancement.yml`
```yaml
# Process pure markdown
# Add language switchers, navigation
# Generate interactive elements
# Inject JavaScript for functionality
```

### `honeypot-validation.yml`
```yaml
# Validate docs/ contains only pure markdown
# Check for forbidden HTML/JS/CSS
# Ensure frontmatter simplicity
# Block PRs with dirty content
```

## 📊 Benefits of Separation

### 🍯 Pure Honeypot Core
- **Clean documentation** that's readable in any markdown viewer
- **Version control friendly** with minimal noise
- **AI-friendly** for processing and analysis
- **Platform independent** - works anywhere

### ⚡ Enhanced Static Site
- **Rich interactive features** generated at build time
- **Fast loading** with optimized assets
- **SEO friendly** with proper meta tags
- **Responsive design** without cluttering source

### 🔧 Maintainable Architecture
- **Clear separation** of concerns
- **Easy to modify** core content without breaking UI
- **Testable workflows** for enhancement generation
- **Scalable approach** for future features

## 🎯 Implementation Priority

1. **Immediate**: Remove Jekyll Liquid and HTML from core docs
2. **Next**: Simplify frontmatter to essential fields
3. **Then**: Create Jekyll build workflow
4. **Finally**: Add honeypot validation workflow

---

*"Keep the honeypot pure - let the workflows add the sweetness."*