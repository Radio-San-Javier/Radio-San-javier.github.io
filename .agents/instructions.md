# Agent Instructions for Radio San Javier

This repository contains the Hugo website for **Radio San Javier**, a local/community radio station.

Start by reading:

1. `.agents/project-context.json`
2. `config/_default/hugo.toml`
3. `config/_default/params.toml`
4. `data/grilla.json`
5. `layouts/partials/home/background.html`
6. `layouts/partials/hoy.html`

## Project summary

- Static site built with Hugo.
- Uses the Blowfish theme as a git submodule under `themes/blowfish/`.
- Custom behavior is implemented through project-level layouts and partial overrides under `layouts/`.
- Content lives under `content/`.
- Structured site data lives under `data/`.
- Static assets live under `static/` and `assets/`.
- The generated site output is in `public/`.

## Important conventions

- General posts use Hugo leaf bundles:
  - `content/posts/<slug>/index.md`
  - images/resources can live next to that `index.md`.
- Radio programs live under:
  - `content/programas/<program_slug>/`
- Program notes/episodes live under:
  - `content/programas/<program_slug>/<note_or_episode_slug>/index.md`
- The weekly schedule is data-driven:
  - edit `data/grilla.json`.
- Advertisers are data-driven:
  - edit `data/publicidades.json`.
- Radio metadata and stream URL are data-driven:
  - edit `data/radio.json`.
- Weather data is generated automatically:
  - `data/clima.json`
  - workflow: `.github/workflows/clima.yml`
  - script: `scripts/actualizar_clima.py`

## Do not edit unless explicitly asked

- `themes/blowfish/`
- `public/`
- `.git/`
- `.hugo_build.lock`

## Working guidelines

- Prefer changes in `content/` and `data/` before touching templates.
- Avoid modifying the theme directly; use layout overrides in this repo.
- Keep visible/user-facing text in Spanish for Argentina unless the user asks otherwise.
- If changing the schedule, preserve the day index convention:
  - `0`: Monday
  - `1`: Tuesday
  - `2`: Wednesday
  - `3`: Thursday
  - `4`: Friday
  - `5`: Saturday
  - `6`: Sunday
- If changing program links in the schedule, make sure the target page exists under `content/programas/`.
- If changing ad placements, make sure the location string matches the value passed to `layouts/partials/publicidades.html`.
- If changing the stream URL, edit `data/radio.json`; the home player and popup player page read from that file.
- If making architectural changes, update `.agents/project-context.json` so future agents have accurate context.

## Known cleanup areas

- Root `hugo.toml` contains generic Hugo values; confirm whether deployment uses it or `config/_default/hugo.toml`.
- Language config currently uses English naming/codes even though the website is Spanish.
- Some test/placeholder content exists under `content/posts/` and `content/acerca_de_la_radio.md`.
- The Decap CMS program collection in `static/admin/config.yml` should be reviewed before relying on it for program creation.
