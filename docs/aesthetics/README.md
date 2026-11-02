# Aesthetic exploration

`explore.html` renders five candidate directions × two frames (hook, mechanism) with identical content at 1080×1920. `node render.mjs` (needs Playwright) writes `frames/<direction>-<frame>.jpg` and `frames/contact-sheet.jpg`.

Directions: `blueprint` · `instrument` · `midnight` · `clinical` · `signal`. Tokens are mirrored in the media library (`assets/brand/techsplained/tokens.css`); keep the two in sync until a direction is chosen, after which the library is the source of truth.

Add a sixth direction by adding a `.t-<id>` block in `explore.html` and the id to the `themes` array in `render.mjs`. The research behind the candidates: `../research/aesthetic-directions.md`.
