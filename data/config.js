/* ------------------------------------------------------------------
   CAT Mastery - site configuration
   Edit this file, commit, and GitHub Pages republishes with the change.
   ------------------------------------------------------------------ */
window.SITE_CONFIG = {

  /* Publication control for previous-year questions.
     CAT papers are the intellectual property of the IIMs. Extracted PYQs
     are fine for your own study; republishing them on a public site is a
     different matter.

       true  -> PYQ bank is loaded and the Past Papers page is active
       false -> PYQ bank is ignored everywhere; the site ships original
                practice only, and the Past Papers page shows a notice

     Recommended: keep true if the repository is PRIVATE, set false if the
     repository is PUBLIC. */
  includePYQ: true,

  /* Show the integrity panel (counts, verification status, quarantine).
     Keeping this on is the point of the rebuild: the numbers the site
     displays should be the numbers that are actually true. */
  showIntegrityPanel: true,

  /* Daily practice rotation. With rotation on, each calendar day advances
     through the bank instead of sampling randomly, so questions do not
     repeat until the pool has been exhausted. */
  nonRepeatingDaily: true,

  /* Questions served per section per day. */
  dailyPerSection: 5
};
