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

#### Blog Posts
- Format: `_posts/YYYY-MM-DD-title.markdown`
- Front matter: `layout: post`, `title`, `date`, `categories`
- Navigation shows 3 most recent posts (by date) + "..." link
- To pin posts: Update date to be more recent than others

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