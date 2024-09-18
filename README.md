# Theo Martin's Blog

This is the repository for Theo Martin's personal blog, built with Jekyll.

## Local Development Setup

To render this website locally, follow these steps:

1. **Install Ruby**: Make sure you have Ruby installed on your system. Jekyll requires Ruby version 2.5.0 or higher.

2. **Install Bundler**: If you haven't already, install Bundler by running:
   ```
   gem install bundler
   ```

3. **Clone the repository**: 
   ```
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

4. **Install dependencies**: Run the following command to install the required gems:
   ```
   bundle install
   ```

5. **Serve the site locally**: Start the Jekyll server with:
   ```
   bundle exec jekyll serve
   ```

6. **View the site**: Open your browser and go to `http://localhost:4000`

## Making Changes

- Edit the files in the repository as needed.
- Jekyll will automatically regenerate the site when you save changes (except for `_config.yml`).
- Refresh your browser to see the changes.

## Configuration

- Site settings can be modified in `_config.yml`.
- If you change `_config.yml`, you'll need to restart the Jekyll server for the changes to take effect.

## Creating New Posts

- Add new post files in the `_posts` directory.
- Use the format `YYYY-MM-DD-title.markdown` for the file name.
- Include the necessary front matter at the top of each post file.

## Deployment

This site is configured to be hosted on GitHub Pages. Simply push your changes to the main branch, and GitHub will automatically build and deploy your site.

## Additional Information

For more details on using Jekyll, refer to the [Jekyll documentation](https://jekyllrb.com/docs/).