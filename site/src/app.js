// 資料の一覧を、分類とキーワードで絞り込む。
// - JavaScript が無いときは、絞り込みの欄を出さず、一覧をすべて見せる
// - 絞り込みの状態は URL（?category=…&q=…）に入れる。言語を切り替えても同じ状態で開く
// - キーワードは空白で区切ったすべての語を含むものを残す。NFKC と小文字でそろえて比べる（scripts/build_site.py と同じ）
(() => {
  const finder = document.querySelector('[data-finder]');
  if (!finder) return;
  const controls = finder.querySelector('[data-controls]');
  const input = finder.querySelector('#q');
  const chips = Array.from(finder.querySelectorAll('[data-category-chip]'));
  const cards = Array.from(finder.querySelectorAll('.card'));
  const count = finder.querySelector('[data-count]');
  const empty = finder.querySelector('[data-empty]');
  const langLink = document.querySelector('[data-lang-link]');
  const messages = JSON.parse(finder.dataset.messages);
  const total = cards.length;
  const norm = (s) => s.normalize('NFKC').toLowerCase();
  const categories = new Set(chips.map((chip) => chip.dataset.categoryChip));

  const params = new URLSearchParams(location.search);
  let category = categories.has(params.get('category') || '') ? params.get('category') || '' : '';
  input.value = params.get('q') || '';

  function apply(updateUrl) {
    const terms = norm(input.value).split(/\s+/).filter(Boolean);
    let shown = 0;
    for (const card of cards) {
      const ok =
        (!category || card.dataset.category === category) &&
        terms.every((term) => card.dataset.search.includes(term));
      card.hidden = !ok;
      if (ok) shown += 1;
    }
    for (const chip of chips) {
      chip.setAttribute('aria-pressed', String(chip.dataset.categoryChip === category));
    }
    count.textContent = messages.count.replace('{shown}', shown).replace('{total}', total);
    empty.hidden = shown !== 0;

    const next = new URLSearchParams();
    if (category) next.set('category', category);
    if (input.value.trim()) next.set('q', input.value.trim());
    const query = next.toString();
    if (updateUrl) history.replaceState(null, '', query ? `?${query}` : location.pathname);
    if (langLink) langLink.search = query;
  }

  for (const chip of chips) {
    chip.addEventListener('click', () => {
      category = chip.dataset.categoryChip;
      apply(true);
    });
  }
  input.addEventListener('input', () => apply(true));
  controls.hidden = false;
  apply(false);
})();
