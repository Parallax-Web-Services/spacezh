# SpaceЖ — Static landing page

One-page, dependency-free static site. No build step, framework, analytics, external fonts, or backend required.

## Deploy

Upload `index.html` and the `assets` folder together to any static web host, such as Cloudflare Pages, GitHub Pages, Netlify, Apache, or nginx. Keep the folder structure intact.

For a local preview, open `index.html` in a browser, or run:

```bash
python -m http.server 8080
```

Then visit http://localhost:8080.

## Before announcing a production domain

- Add absolute `og:url` and `og:image` URLs in `index.html` once the domain is known. Social platforms often require an absolute URL for link preview images.
- Update the external launch link (currently points to the X post provided in the conversation) if a dedicated official SpaceЖ channel is launched.
- Add actual repository and contribution links only when public repos exist.
- Update R&D claims, corporate footer, and the project status as necessary. The page intentionally does not claim any operational detection or alert capabilities.
- The hero artwork is a web-optimized crop of the artwork supplied by the site owner. Its original footer was excluded to avoid conflicting company language, and the HTML footer contains the requested product/company hierarchy.

## Customization

Color, spacing, and typography variables live at the top of the embedded `<style>` block. Every section is ordinary semantic HTML. The tiny animated scanner is explicitly a synthetic interface graphic and automatically respects the visitor's reduced-motion settings.

## Legal / branding note

The site includes an independence/parody disclaimer. It has not been reviewed for trademark, advertising, or other legal compliance; including a disclaimer does not itself settle those questions.
