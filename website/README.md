# Domain Park website

An Astro static website for `https://www.domain-park.org`, maintained separately
from the Python DNS service inside this repository. The current Jekyll site in
`../docs/` stays live until launch. No Pages settings are changed by adding this
directory or its workflows.

## Develop and review

Use Node **24** (`nvm use` if you use nvm). From this directory:

```sh
npm ci
npm run dev
```

Open the local address printed by Astro (normally `http://localhost:4321`).
To check and preview the actual static output:

```sh
npm run check
npm run build
npm run verify
npm run preview
```

The default build is for review. It includes all guide outlines, adds `noindex`
metadata, disallows crawling in `robots.txt`, and generates no sitemap. Outlines
have visible notices and are labelled on homepage cards. These signals are for
search engines, not access control: keep review builds local or on private hosts.

## How the stack fits together

- **Astro** renders `.astro` templates and Markdown to HTML at build time.
- **HTML** supplies semantic structure; **CSS** handles layout and appearance.
- **Tailwind 4** is integrated through Vite; the design mainly uses ordinary CSS.
- **TypeScript** types configuration and component properties and validates content.
- **Node/npm/Vite** run development and build tooling; GitHub Pages serves only
  the generated `dist/` files. No Node server is needed in production.
- Small browser scripts handle theme preferences and copying nameservers. The
  content and links work without JavaScript. No React, Vue, MDX, CMS, analytics,
  or third-party browser scripts are required.

## Edit content and appearance

Guide outlines live in `src/content/guides/`. Their filenames determine URLs,
for example `setup.md` becomes `/guides/setup/`. Each file needs:

```yaml
title: How to set up Domain Park
description: A short description used on cards and in page metadata.
order: 2
outline: true
```

Keep orders positive and unique. Cards are sorted by order and their colours
cycle through lime, cyan, lavender, and mint. Article headings create the table
of contents automatically. Write the final prose, verify the facts and external
links, then change `outline` to `false`. Omitting it defaults to an outline.
Use `/guides/setup/`-style links with trailing slashes for internal pages.

The setup outline intentionally reserves registrar-specific links for the writing
stage. Choose relevant providers and link to their official instructions for
changing authoritative nameservers, rather than instructions for adding zone
records. The technical examples come from `../src/domain_park/server.py`; verify
them against the public service before publishing. Software reporting options
must not be described as public-service features without checking deployment.

`src/config/site.ts` centralises nameservers, production URL, author, and project
links. `src/styles/global.css` contains colours, fonts, spacing, responsive rules,
and article styles. Layouts and small reusable UI components live in `src/layouts/`
and `src/components/`. Manrope is self-hosted through the Fontsource package;
fonts are bundled at build time, not fetched from a browser font service.

The theme follows the system colour preference unless a visitor switches modes.
Only this preference is saved in localStorage (`domain-park-theme`). If storage
is blocked, switching still works for the current page. With JavaScript disabled,
CSS follows the system preference and the inactive toggle/copy controls are hidden.

## CI and launch

`website-check.yml` checks, builds, verifies links/metadata, and uploads a review
artifact for relevant pull requests and pushes to `master`. It has no deployment
permissions.

`website-deploy.yml` runs only by manual dispatch on `master`. Its production
build refuses to publish while any guide is marked as an outline. To launch:

1. Finish all four guides and set each `outline: false`. Check registrar links,
   live nameservers/DNS answers, content accuracy, and security limitations.
2. Run `npm run check` and `npm run build:production`. Confirm the sitemap,
   canonical URLs, social image, custom 404, and all links in a local preview.
3. Review mobile and desktop layouts, both themes, keyboard navigation, focus
   visibility, reduced motion, copy success/failure, and JavaScript-disabled use.
4. Merge the reviewed website changes to `master`.
5. In repository **Settings → Pages**, change the source to **GitHub Actions**.
   Keep the custom domain `www.domain-park.org` and HTTPS enabled. Do not change
   the domain's DNS if the existing GitHub Pages mapping is still correct.
6. Run **Deploy website (manual)** from Actions, selecting `master`.
7. Check the live homepage, guide URLs, missing-page response, HTTPS, sitemap,
   and social preview. Later releases also require manual dispatch.

The production build enables indexing and generates a sitemap. The custom
domain is served at `/`; do not add a `/domain-park` Astro base path. `public/CNAME`
records the domain for the build; the repository's Pages settings must also be
configured explicitly when deploying with Actions.

For rollback, change Pages back to **Deploy from a branch**, selecting `master`
and `/docs`, and allow its Jekyll deployment to complete. The previous site's
source is preserved unchanged. Do not dispatch the Astro deployment workflow
again until the issue is fixed.

## Theme provenance and licensing

Adapted from [xocothemes/maria](https://github.com/xocothemes/maria), upstream commit
`98174a69792deb675272e4eb52ae88cfa6204600` (Maria 2.0.0). The adapted pieces are
its shared layout approach, Manrope typography, light/dark colour tokens,
responsive grid, and coloured portfolio cards. The portfolio pages, images,
cookie-consent system, and Netlify/Vercel configuration are not included.

Maria's MIT copyright and permission notice are preserved in `LICENSE-MARIA`.
The site remains covered by the repository's MIT licence. Fontsource's Manrope
package carries the font's own licence. Treat this as a customised copy rather
than an automatically synchronised fork; review upstream changes before applying
them. The social image is a locally rendered graphic derived from the site's
colours and typography; its source is `public/og-image.svg`.
