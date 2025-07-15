#!/bin/bash

# Simple script to create a new blog post
# Usage: ./new-post.sh "Your Post Title"

if [ $# -eq 0 ]; then
    echo "Usage: $0 \"Your Post Title\""
    echo "Example: $0 \"My Amazing Blog Post\""
    exit 1
fi

TITLE="$1"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M:%S)
FILENAME="_posts/${DATE}-$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g').md"

cat > "$FILENAME" << EOF
---
layout: post
title: "$TITLE"
date: $DATE $TIME +0200
categories: blog
---

# $TITLE

Write your content here...

## Getting Started

- Use Markdown syntax
- Add images to /assets/ folder
- Push to GitHub when ready

Your post will be automatically deployed to GitHub Pages!
EOF

echo "Created new post: $FILENAME"
echo "Edit the file and push to GitHub to publish!"