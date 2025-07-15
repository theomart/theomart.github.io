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

### Site Structure
- **Homepage**: Custom layout (`homepage.html`) with profile image and navigation
- **AI Services**: Custom layout (`aiservices.html`) with service descriptions and gradients
- **Blog**: Standard Jekyll blog with posts in `_posts/` directory using default layout

### Key Components
- **Layouts**: `_layouts/homepage.html` and `_layouts/aiservices.html` for custom pages
- **Posts**: Blog posts in `_posts/` following `YYYY-MM-DD-title.markdown` format
- **Assets**: Custom SCSS files in `assets/` directory:
  - `homepage.scss` - Homepage styling
  - `aiservices.scss` - AI services page styling with gradients and animations
- **Configuration**: `_config.yml` contains site settings, theme (minima), and plugins

### Styling System
- Uses Jekyll's built-in Sass processing
- Custom SCSS files compiled to CSS automatically
- Minima theme as base with custom overrides
- Custom layouts include specific CSS files

### Content Management
- Blog posts use standard Jekyll front matter with layout, title, date, and categories
- Pages use custom layouts specified in front matter
- Site uses jekyll-feed plugin for RSS generation

#### Navigation Blog Posts
The sidebar navigation shows the 3 most recent blog posts under the "Blog" menu item. These are automatically selected by Jekyll using `{% for post in site.posts limit:3 %}` based on the post date.

**To control which posts appear in the navigation:**
- Posts are ordered by date (newest first)
- The 3 most recent posts will automatically appear in the sidebar
- To "pin" specific posts to the top of the navigation, update their date to be more recent
- Post dates are set in the filename (`YYYY-MM-DD-title.markdown`) and the `date:` field in the front matter

**Example:**
```yaml
---
layout: post
title: "Important Post"
date: 2025-01-15
categories: AI
---
```

If you want a specific post to always appear in the navigation, you can set its date to be in the future or simply more recent than other posts.

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