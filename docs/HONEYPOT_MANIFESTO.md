---
title: "Honeypot Manifesto"
description: "Pure documentation core with workflow-generated enhancements"
category: "foundation"
---

# 🍯 Honeypot Manifesto
*Keep the core pure - let workflows add the sweetness*

## 🎯 Core Principle

The `docs/` directory is our **sacred honeypot** - it must remain pure, clean, and free from contamination. All interactive elements, styling, and enhancements are added through GitHub Actions workflows during static site generation.

## 🚫 What's Forbidden in the Honeypot

### ❌ Jekyll Liquid Includes
```markdown
# FORBIDDEN
{% include language-switcher.html %}
{% include sacred-navigation.html %}
```

### ❌ HTML with Classes
```markdown
# FORBIDDEN
<div class="language-content" data-lang="en">
<div class="sacred-theme">
```

### ❌ JavaScript/CSS in Markdown
```markdown
# FORBIDDEN
<script src="...">
<style>...</style>
```

### ❌ Complex Frontmatter
```yaml
# FORBIDDEN - Too complex
---
title: "Document"
interactive_nav: true
sacred_theme: true
mermaid_enhanced: true
bilingual: true
lang_switcher: true
translation_status: "complete"
---
```

## ✅ What's Allowed in the Honeypot

### ✅ Pure Markdown
```markdown
# Clean Headers
- Simple lists
- **Bold** and *italic* text
- [Links](url)
- ![Images](path)
```

### ✅ Fenced Code Blocks
```python
# Code examples in fenced blocks
def pure_function():
    return "clean code"
```

### ✅ Simple Tables
```markdown
| Column 1 | Column 2 |
|----------|----------|
| Data     | More     |
```

### ✅ Essential Frontmatter Only
```yaml
---
title: "Document Title"
description: "Brief description"
category: "foundation|architecture|development|api"
---
```

## 🔄 Rect-to-Hexa Architecture

### 🔲 RECT (Core) - Pure Documentation
- **Location**: `docs/` directory
- **Content**: Pure markdown files only
- **Frontmatter**: Essential fields only (title, description, category)
- **Purpose**: Human and AI readable documentation

### [⬢⬡⬢⬡] HEXA (Enhancement) - Generated Features
- **Location**: `.github/workflows/` and generated `_site/`
- **Content**: Interactive elements, styling, navigation
- **Generation**: Jekyll build process with custom layouts
- **Purpose**: Rich user experience for web visitors

## 🏗️ Workflow Enhancement Strategy

### Jekyll Build Workflow
1. **Input**: Pure markdown from `docs/`
2. **Process**: Add layouts, navigation, styling
3. **Output**: Rich static site with interactive features
4. **Deploy**: GitHub Pages or static hosting

### Honeypot Validation Workflow
1. **Check**: Scan `docs/` for forbidden content
2. **Validate**: Ensure pure markdown compliance
3. **Block**: Prevent contaminated PRs from merging
4. **Report**: Generate purity metrics

## 📊 Benefits of Purity

### 🍯 For Documentation Authors
- **Simple**: Write in pure markdown
- **Fast**: No complex syntax to learn
- **Portable**: Works in any markdown viewer
- **Version Control Friendly**: Clean diffs

### 🌐 For Website Visitors
- **Rich**: Full interactive experience
- **Fast**: Optimized static site
- **Responsive**: Mobile-friendly design
- **Accessible**: Proper semantic HTML

### 🤖 For AI Teammates
- **Readable**: Clean, structured content
- **Processable**: No HTML/JS noise
- **Analyzable**: Pure semantic meaning
- **Maintainable**: Easy to update and improve

## 🎯 Implementation Guidelines

### For Contributors
1. **Write pure markdown** in `docs/`
2. **Use simple frontmatter** (title, description, category)
3. **No HTML/CSS/JS** in markdown files
4. **Let workflows handle** styling and interactivity

### For Maintainers
1. **Enforce purity** through validation workflows
2. **Enhance through Jekyll** build process
3. **Monitor honeypot health** with automated checks
4. **Reject contaminated PRs** automatically

## 🙏 Sacred Commitment

We commit to keeping our documentation honeypot pure, following the divine principle of separation of concerns. The core remains clean and readable, while workflows add the interactive sweetness that makes the documentation come alive.

---

*"In purity there is clarity, in separation there is strength, in workflows there is enhancement."*

**Status**: 🍯 Pure Honeypot Maintained | **Validation**: Automated | **Enhancement**: Workflow-Generated