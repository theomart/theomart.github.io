# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Jekyll-based personal blog and portfolio site for Theo Martin, deployed on GitHub Pages. The site features a custom homepage, AI services page, and blog functionality.

## Development Commands

### Local Development Setup
```bash
# Install dependencies
bundle install

# Serve the site locally with auto-reload
bundle exec jekyll serve

# Build the site for production
bundle exec jekyll build
```

The site runs on `http://localhost:4000` when served locally.

### Important Notes
- Changes to `_config.yml` require restarting the Jekyll server
- All other files auto-reload when changed during development
- The site uses GitHub Pages for deployment (automatic on push to gh-pages branch)

## Architecture

### Core System
- **Single Layout**: `_layouts/unified.html` - unified layout for all pages with sidebar navigation
- **Pages**: `index.html` (Home/Contact), `blog.html` (Blog listing), `aiservices.html` (AI Services)
- **Posts**: `_posts/YYYY-MM-DD-title.markdown` format with Jekyll front matter
- **Styles**: Single `assets/unified.scss` file compiles to `/assets/unified.css`

### Navigation System
- **Sidebar**: Fixed left sidebar with main navigation (Home/Contact, Blog, AI Services)
- **Contextual Submenus**: Show automatically based on current page
  - Blog pages: Show 3 most recent posts + "..." link
  - AI Services pages: Show 4 service sections with URL hash routing
- **Active States**: CSS classes automatically applied via Jekyll conditionals

### Key Files
- `_layouts/unified.html` - Main layout template with navigation logic
- `assets/unified.scss` - All CSS styling (IBM Plex Mono font, dark theme)
- `aiservices.html` - Contains all AI service sections, JavaScript switches between them
- `_config.yml` - Jekyll configuration, GitHub Pages settings

### Content Management

#### Pages
- All pages use `layout: unified` in front matter
- `index.html` - Home/Contact page with intro + contact sections
- `blog.html` - Blog listing page
- `aiservices.html` - AI services with multiple content sections
- `team.html` - Team page showcasing both consultants

#### Blog Posts
- Format: `_posts/YYYY-MM-DD-title.markdown`
- Front matter: `layout: post`, `title`, `date`, `categories`

#### Featured Posts in Navigation
The blog submenu shows 3 handpicked posts instead of the most recent ones. To change featured posts:

1. Open `_config.yml`
2. Find the `featured_posts` section
3. Update the filenames with your desired posts:
```yaml
featured_posts:
  - "2024-08-26-colbert.markdown"
  - "2024-09-21-developers-who-dont-use-ai-assisted-coding-are-already-falli.markdown"
  - "2025-03-31-rewriting-from-scratch-is-increasingly-viable-due-to-ai-assi.markdown"
```
4. Restart Jekyll server (changes to `_config.yml` require restart)

Note: Use the exact filename from the `_posts` directory, including the date prefix and `.markdown` extension.

#### AI Services Sections
- Single page with multiple `<div class="content-section" id="sectionname">` blocks
- JavaScript shows/hides sections based on URL hash (`#strategy`, `#ml`, etc.)
- Navigation links use `/aiservices#sectionname` format
- Sections: strategy, ml, genai, automation

## GitHub Pages Configuration
- Domain: `theomart.in` (configured in CNAME and _config.yml)
- Uses `github-pages` gem for deployment compatibility
- Automatic deployment on push to gh-pages branch

## Website Development Considerations

### Simplicity and Content Management
- Goal: Create the simplest possible personal website with easy content management
- Key Requirements:
  - Markdown-based content creation
  - Lightweight framework or no framework
  - GitHub Pages deployment
  - Minimal setup for non-technical users
  - Beautiful rendering of Markdown content

### Design Principles
- **Minimalistic but aesthetic UI**: Avoid unnecessary separators, dividers, or decorative elements
- Focus on clean typography and thoughtful spacing
- Let content breathe with whitespace rather than visual separators
- Use subtle design elements (like gradient text) sparingly for emphasis

### Tone and Writing Style
Our content uses a direct, no-BS tone that prioritizes clarity and value:

- **Cut through the noise**: No corporate jargon, buzzwords, or filler content. Every sentence should deliver value.
- **Problem-first approach**: Lead with the customer's pain points, not our capabilities. "Your models never made it past PowerPoint" vs "We offer MLOps services"
- **Concrete over abstract**: Use specific examples, numbers, and scenarios. "Block crooks in 50ms" vs "Real-time fraud detection"
- **Conversational but authoritative**: Write like you're explaining to a smart colleague who doesn't have time for fluff
- **Action-oriented**: Focus on what gets done, not what could be done. "We've fixed it" vs "We can help"
- **Minimalistic**: If it can be said in 5 words instead of 20, use 5. Remove any sentence that doesn't add new information
- **Technical honesty**: Don't oversimplify technical concepts, but explain them in accessible terms
- **Show, don't tell**: Instead of claiming expertise, demonstrate it through specific use cases and results

Example transformations:
- ❌ "We leverage cutting-edge artificial intelligence solutions to transform your business"
- ✅ "Your board wants an AI roadmap that actually delivers ROI, not another pilot graveyard"

- ❌ "Our comprehensive suite of services includes..."
- ✅ "From fashion marketplaces struggling with search accuracy to B2B platforms bleeding money on invoice mismatches—we deliver solutions that ship"

## Localization Guidelines

The site supports both English and French versions with a language switcher in the bottom-left sidebar.

### File Structure
- English pages: Root directory (`/`)
- French pages: `/fr/` directory
- Blog: English only (`/blog`) - shared across languages

### Language Switching
- Language switcher preserves current page path
- English: `/page` ↔ French: `/fr/page`
- Blog always redirects to English version

### Content Synchronization
**IMPORTANT**: When updating any English content, always update the corresponding French version if it exists:

1. **Homepage**: `index.html` ↔ `fr/index.html`
2. **AI Services**: `aiservices.html` ↔ `fr/aiservices.html`
3. **Team**: `team.html` ↔ `fr/team.html`
4. **Case Studies**: `success.html` ↔ `fr/success.html`
5. **Let's Talk**: `talk.html` ↔ `fr/talk.html`
6. **Blog**: English only - no French version

### French Translation Guidelines
- Keep useful business anglicisms for clarity: "roadmap", "board", "data", "tools", "dashboard"
- Maintain direct, no-BS tone adapted for French business culture
- Use tech slang where appropriate: "shipper", "scaler", "mapper"
- Mix French/English naturally: "engineered depuis le boardroom"

### Navigation Updates
When adding new pages or sections:
1. Add English version to main navigation
2. Add French version to conditional French navigation in `_layouts/unified.html`
3. Ensure language switcher works for new pages