# Hosting CAT Mastery on GitHub Pages

## Before you upload: one decision

Open `data/config.js` and set `includePYQ`.

- Repository **private** → leave it `true`. The Past Papers page works.
- Repository **public** → set it to `false`. CAT papers belong to the IIMs, and the
  site then ships 1,767 original questions with no extracted material.

Everything else works either way.

## Upload

1. Create a repository, for example `cat-mastery`.
2. Upload the **contents** of this folder, not the zip:
   `index.html`, `.nojekyll`, `README.md`, `HOSTING.md`, `assets/`, `data/`, `build/`.
3. Commit.
4. Settings → Pages → Build and deployment:
   - Source: **Deploy from a branch**
   - Branch: **main**, folder: **/(root)**
5. Save.

The site appears at `https://YOUR-USERNAME.github.io/cat-mastery/`.

`build/` is optional on the server. It contains the scripts that generate the question
bank, not anything the site loads. Keep it in the repository so the bank is
reproducible; the browser never fetches it.

## If you see a 404

- `index.html` must be at the root of the publishing source
- Pages set to `main` + `/(root)`
- the upload was actually committed
- repository visibility supports Pages on your plan

## Updating later

Edit and commit; Pages republishes automatically.

| To change | Edit |
|---|---|
| PYQ on/off, daily question count, integrity panel | `data/config.js` |
| Questions | run the build scripts, commit the regenerated `data/*.js` |
| Behaviour | `assets/app.js`, design in `assets/theme.css` |
| Design | `assets/styles.css` |

Do not hand-edit `data/practice-bank.js`, `data/pyq-bank.js` or `data/integrity.js`.
They are build output and the next build overwrites them. Add questions through the
generators in `build/`, or through the JSON importer inside the app, which stores them
in the browser.

## Custom domain

Settings → Pages → Custom domain.

## Limitation

GitHub Pages is static hosting. No login, no cross-device sync, no shared leaderboard,
no real percentile against other candidates. Those need a backend such as Supabase or
Firebase.
