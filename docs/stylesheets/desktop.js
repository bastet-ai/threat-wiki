/* Progressive enhancement: original content remains intact without JavaScript. */
(() => {
  'use strict';
  function enhance() {
    const home = document.querySelector('.threat-home');
    if (!home) return;
    const heading = home.querySelector('h1');
    if (heading && !home.querySelector('.threat-hero')) {
      const hero = document.createElement('div');
      hero.className = 'threat-hero';
      heading.before(hero);
      const intro = heading.nextElementSibling;
      hero.append(heading);
      if (intro && intro.tagName === 'P') hero.append(intro);
    }
    function sectionList(id) {
      const title = home.querySelector('#' + id);
      let next = title && title.nextElementSibling;
      while (next && !/^H[12]$/.test(next.tagName)) {
        if (next.tagName === 'UL') return next;
        next = next.nextElementSibling;
      }
      return null;
    }
    // The cron block may have no blank line before its Markdown bullets.
    // In that case MkDocs emits one paragraph with links separated by newlines.
    const popularHeading = home.querySelector('#popular-this-week');
    const paragraph = popularHeading && popularHeading.nextElementSibling;
    if (paragraph && paragraph.tagName === 'P' && paragraph.querySelector('a')) {
      const list = document.createElement('ul');
      Array.from(paragraph.querySelectorAll('a')).forEach((link) => {
        const card = document.createElement('li');
        const suffix = link.nextSibling;
        card.append(link);
        if (suffix && suffix.nodeType === Node.TEXT_NODE) {
          card.append(document.createTextNode(suffix.textContent.replace(/\n-\s*$/, '').trim()));
          suffix.remove();
        }
        list.append(card);
      });
      // Preserve the analytics annotation, removing only the orphan bullet marker.
      Array.from(paragraph.childNodes).forEach((node) => {
        if (node.nodeType === Node.TEXT_NODE && /^\s*-\s*$/.test(node.textContent)) node.remove();
      });
      paragraph.after(list);
    }
    const popular = sectionList('popular-this-week');
    if (popular) popular.classList.add('threat-popular');
    const recent = sectionList('recent-entries');
    if (!recent) return;
    recent.classList.add('threat-recents');
    Array.from(recent.children).forEach((item) => {
      if (item.dataset.enhanced || item.textContent.length < 350) return;
      item.dataset.enhanced = 'true';
      const link = item.querySelector('a');
      const title = (link || item).textContent.trim();
      const details = document.createElement('details');
      details.className = 'threat-entry';
      const summary = document.createElement('summary');
      const preview = document.createElement('span');
      preview.className = 'threat-entry-title';
      preview.textContent = title.length > 200 ? title.slice(0, 197) + '…' : title;
      const action = document.createElement('span');
      action.className = 'threat-entry-action';
      action.textContent = 'Show more';
      summary.append(preview, action);
      const body = document.createElement('div');
      body.className = 'threat-entry-body';
      while (item.firstChild) body.append(item.firstChild);
      details.append(summary, body);
      details.addEventListener('toggle', () => {
        action.textContent = details.open ? 'Show less' : 'Show more';
      });
      item.append(details);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', enhance);
  else enhance();
  // Material's optional instant navigation replaces the article without a reload.
  if (typeof document$ !== 'undefined' && typeof document$.subscribe === 'function') {
    document$.subscribe(enhance);
  }
})();
