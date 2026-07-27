# Triple Crown Group

Marketing site for Triple Crown Group, built from `triple-crown-group-website-brief.md`.

Plain HTML/CSS/JS, no build step. Six pages: Home, What We Support, How We Work, About, Results, Contact.

## Structure

- `/index.html`, `/what-we-support/`, `/how-we-work/`, `/about/`, `/results/`, `/contact/` — one folder per page for clean URLs
- `/css/style.css` — shared design system (brand colors, typography, components)
- `/js/main.js` — sticky header, mobile menu, scroll reveal, contact modal
- `/assets/brand/` — official logo files (`tcg-full-logo.png`, `tcg-monogram.png`) and generated favicon sizes
- `CNAME` — custom domain for GitHub Pages (triplecrown.group)

## Adding a page

Copy an existing page folder's `index.html`, update the header nav active state, hero content, and footer links. No restructuring needed.

## Deployment

GitHub Pages, serving from this repo, with DNS managed through Cloudflare pointing at `triplecrown.group`.

## Contact form

The contact page currently has a placeholder form (no backend). Swap the `<form class="contact-form">` block in `contact/index.html` for the real form/embed when available.
