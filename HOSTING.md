# How to host CAT Mastery on GitHub Pages

## Fastest method

1. Sign in to GitHub.
2. Click **New repository**.
3. Name it something like:
   `cat-mastery`
4. Choose **Public** if you are using GitHub Free Pages.
5. Create the repository.
6. Extract `CAT_Mastery_GitHub_Package.zip` on your computer.
7. Upload **the contents of the extracted folder**, not the ZIP itself:
   - `index.html`
   - `.nojekyll`
   - `README.md`
   - `HOSTING.md`
   - `assets/`
   - `data/`
8. Commit the files.
9. In the repository, open **Settings**.
10. In the left sidebar, open **Pages**.
11. Under **Build and deployment**:
    - Source: **Deploy from a branch**
    - Branch: **main**
    - Folder: **/(root)**
12. Click **Save**.

Your project site will normally be available at:

`https://YOUR-USERNAME.github.io/cat-mastery/`

GitHub's official documentation says branch-based Pages deployments can use a selected branch and either the repository root or `/docs` folder as the publishing source. `index.html` needs to be at the top of that publishing source.

## If the page shows 404

Check:
- `index.html` is in repository root
- Pages is set to `main` + `/(root)`
- your latest upload was committed
- repository visibility supports Pages on your GitHub plan

## Updating the site later

Edit or replace:
- `data/questions.js` for bundled questions
- `assets/app.js` for functionality
- `assets/styles.css` for design

Then commit the change. GitHub Pages republishes the site.

## Custom domain

You can later attach a custom domain from:
**Settings → Pages → Custom domain**

## Important limitation

GitHub Pages is static hosting. It does not run server-side PHP/Python and cannot by itself maintain a shared leaderboard.

For:
- login
- sync across devices
- real participant rank
- percentile among all users
- shared leaderboard

add a backend such as Supabase/Firebase.
