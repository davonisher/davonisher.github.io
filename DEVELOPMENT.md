## Development Documentation

This information is only really useful for the site owner.

### Build, Test, Local-Dev

#### Install

`bundle install`

#### Run Locally

`bundle exec jekyll server`

Preview drafts locally:

`bundle exec jekyll serve --drafts`

#### Verify Build

`bundle exec jekyll build`

### Blog: Write and Publish (Markdown in Repo)

Posts live in `collections/_posts/` as `YYYY-MM-DD-slug-from-title.md`.
Drafts live in `collections/_drafts/` and are not published unless you pass `--drafts` to Jekyll.

#### Create a new post

```bash
python tools/new_post.py "Your Post Title"
```

Optional flags:

```bash
python tools/new_post.py "Your Post Title" --date 2026-07-02 --category tools
```

This creates a dated file with front matter (`layout`, `title`, `date`, `summary`, `categories`).
Edit the file, replace the `summary` placeholder, and write the body in Markdown.

#### Publish a draft

```bash
python tools/publish_draft.py 2024-01-14-computing-cultural-literacy.md
```

Optional publish date:

```bash
python tools/publish_draft.py my-draft-slug --date 2026-07-02
```

This moves the draft into `collections/_posts/`, sets `date` in front matter to match the filename, and deletes the draft file.

#### Front matter template

See `collections/_posts/_template.md` for the expected fields and comments.

### Library Pages

Library, anti-library, and book review pages are controlled by `show_library` in `_config.yml`.
Set `show_library: true` to re-enable the nav link and published reading pages.
