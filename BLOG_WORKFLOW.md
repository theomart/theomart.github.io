# Super Simple Blog Workflow

## Adding a New Blog Post (3 methods)

### Method 1: Use the Script (Easiest)
```bash
./new-post.sh "Your Amazing Post Title"
```
This creates a new post file with the correct name and front matter.

### Method 2: Copy Template
1. Copy `_posts/TEMPLATE.md`
2. Rename to `_posts/YYYY-MM-DD-your-title.md`
3. Update the front matter (title, date)
4. Write your content

### Method 3: Manual Creation
Create a file in `_posts/` with this format:
```
_posts/2024-07-15-my-post.md
```

## Front Matter (Required)
```yaml
---
layout: post
title: "Your Post Title"
date: 2024-07-15 12:00:00 +0200
categories: blog
---
```

## Publishing
1. Write your post in Markdown
2. Push to GitHub
3. GitHub Actions automatically builds and deploys
4. Your post appears on your site!

## That's It!
- No local Jekyll setup required
- No manual building
- Just write Markdown and push to GitHub
- Everything else is automatic