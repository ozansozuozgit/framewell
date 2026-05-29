let posts = [];
let prompts = {};
let filtered = [];
let shuffleMode = false;
const state = { query: '', source: '', type: '', tag: '' };

const els = {
  grid: document.getElementById('grid'),
  trend: document.getElementById('trendingTrack'),
  modal: document.getElementById('modal'),
  modalBody: document.getElementById('modalBody'),
  count: document.getElementById('count'),
  navCount: document.getElementById('navCount'),
  activeFilters: document.getElementById('activeFilters'),
  search: document.getElementById('searchInput'),
  sourceSelect: document.getElementById('sourceSelect'),
  typeSelect: document.getElementById('typeSelect'),
  sourceFacet: document.getElementById('sourceFacet'),
  tagFacet: document.getElementById('tagFacet'),
  quickChips: document.getElementById('quickChips'),
  scoutList: document.getElementById('scoutList'),
  heroStage: document.getElementById('heroStage'),
  heroReel: document.getElementById('heroReel'),
  theatreSpotlight: document.getElementById('theatreSpotlight'),
  theatrePills: document.getElementById('theatrePills'),
  patternLanes: document.getElementById('patternLanes')
};

async function loadJson(path, fallback){
  try { const r = await fetch(path); if(!r.ok) throw new Error(r.status); return await r.json(); }
  catch(e) { console.warn('Could not load', path, e); return fallback; }
}
function esc(s){ return String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
function sourceOf(p){ return p.sourceName || p.author || 'Local archive'; }
function typeOf(p){ return p.sectionType || 'Prompt'; }
function hasPrompt(p){ return Boolean(prompts[p.slug] || prompts[p.id]); }
function getPrompt(p){ return prompts[p.slug] || prompts[p.id] || ''; }
function hasPreview(p){ return Boolean(p.media || p.thumbnail); }
function mediaEl(p, cls=''){
  const src = p.media || p.thumbnail || '';
  const poster = p.thumbnail || '';
  if((p.mimeType||'').includes('video') && src){ return `<video class="${cls}" src="${esc(src)}" poster="${esc(poster)}" muted loop playsinline preload="metadata"></video>`; }
  if(poster || src){ return `<img class="${cls}" src="${esc(poster || src)}" alt="">`; }
  const tool = esc((p.aiTools || [])[0] || 'Prompt');
  const title = esc(p.title || 'Curated prompt');
  const source = esc(sourceOf(p));
  return `<div class="${cls} prompt-placeholder"><span>${tool}</span><strong>${title}</strong><em>${source}</em></div>`;
}
function stillMediaEl(p, cls=''){
  const src = p.thumbnail || p.media || '';
  if(src) return `<img class="${cls}" src="${esc(src)}" alt="">`;
  return mediaEl(p, cls);
}
function countBy(items, fn){
  const map = new Map();
  items.forEach(item => { const key = fn(item); if(key) map.set(key, (map.get(key)||0)+1); });
  return [...map.entries()].sort((a,b)=>b[1]-a[1] || a[0].localeCompare(b[0]));
}
function normalize(s){ return String(s||'').toLowerCase(); }
function optionHtml(values){ return values.map(v => `<option value="${esc(v)}">${esc(v)}</option>`).join(''); }
const typeOptions = [
  ['', 'All types'],
  ['hero', 'Hero motion'],
  ['landing|website|agency|saas|marketing', 'Landing pages'],
  ['dashboard|analytics|command|ops|console|finance|revenue', 'Dashboards'],
  ['component|button|card|dock|popover|bento|carousel|form', 'Components'],
  ['animation|motion|gsap|scroll|transition|marquee', 'Animation systems'],
  ['3d|glass|particle|space|cosmic|liquid', '3D / glass'],
  ['onboarding|waitlist|login|signup', 'Onboarding / forms']
];
function typeOptionsHtml(){ return typeOptions.map(([value,label]) => `<option value="${esc(value)}">${esc(label)}</option>`).join(''); }
function typeLabel(value){ return (typeOptions.find(([v]) => v === value) || [value,value])[1]; }
function matchesFilterGroup(value, hay){ return !value || value.split('|').some(token => hay.includes(normalize(token))); }
function setupControls(){
  const sources = countBy(posts, sourceOf).map(([k])=>k);
  els.sourceSelect.innerHTML = '<option value="">All sources</option>' + optionHtml(sources);
  els.typeSelect.innerHTML = typeOptionsHtml();
  renderQuickChips();
}
function renderQuickChips(){
  if(!els.quickChips) return;
  const chips = [
    ['Hero motion','hero'],
    ['Glass / 3D','3D'],
    ['Dashboards','dashboard'],
    ['Components','component'],
    ['Scroll stories','scroll'],
    ['Magic UI','Magic UI'],
    ['Onboarding','onboarding']
  ];
  els.quickChips.innerHTML = chips.map(([label,value]) => `<button type="button" class="${state.query===value?'active':''}" data-chip="${esc(value)}">${esc(label)}</button>`).join('');
}
function applyFilters(){
  const q = normalize(state.query);
  filtered = posts.filter(p => {
    const hay = normalize([p.title, p.sectionType, sourceOf(p), p.author, ...(p.tags||[]), ...(p.aiTools||[])].join(' '));
    if(q && !q.split(/\s+/).every(token => hay.includes(token))) return false;
    if(state.source && sourceOf(p) !== state.source) return false;
    if(state.type && !matchesFilterGroup(state.type, hay)) return false;
    if(state.tag && !hay.includes(normalize(state.tag))) return false;
    return true;
  });
  if(shuffleMode) filtered = [...filtered].sort(() => Math.random() - 0.5).slice(0, 36);
}
function renderStats(){
  const curated = posts.filter(p => p.promptOnly).length;
  const previews = posts.filter(hasPreview).length;
  const sources = new Set(posts.map(sourceOf)).size;
  document.getElementById('statTotal').textContent = posts.length;
  document.getElementById('statCurated').textContent = curated;
  document.getElementById('statPreviews').textContent = previews;
  document.getElementById('statSources').textContent = sources;
  document.getElementById('promptTotal').textContent = `${Object.keys(prompts).length} prompts`;
  els.navCount.textContent = `${posts.length} cards`;
  const latest = posts.slice(-5).reverse();
  els.scoutList.innerHTML = latest.map(p => `<button type="button" data-open="${esc(p.id)}"><span>${esc(sourceOf(p))}</span><b>${esc(p.title)}</b></button>`).join('');
}
function renderFacets(){
  if(!els.sourceFacet || !els.tagFacet) return;
  const srcCounts = countBy(posts, sourceOf).slice(0, 12);
  els.sourceFacet.innerHTML = srcCounts.map(([name,n]) => `<button type="button" class="${state.source===name?'active':''}" data-source="${esc(name)}"><span>${esc(name)}</span><b>${n}</b></button>`).join('');
  const tagCounts = countBy(posts.flatMap(p => (p.tags||[]).map(t => ({tag:t}))), x => x.tag).slice(0, 22);
  els.tagFacet.innerHTML = tagCounts.map(([name,n]) => `<button type="button" class="${state.tag===name?'active':''}" data-tag="${esc(name)}"><span>${esc(name)}</span><b>${n}</b></button>`).join('');
}
function card(p, i){
  const copyLabel = hasPrompt(p) ? 'Copy prompt' : 'Open source';
  const tags = (p.tags||[]).slice(0,2).map(t=>`<span class="tag">${esc(t)}</span>`).join('');
  const tools = (p.aiTools||[]).slice(0,1).map(t=>`<span class="pill">${esc(t)}</span>`).join('');
  const generated = p.previewGenerated ? '<span class="preview-note">concept sketch</span>' : '';
  return `<article class="card atlas-card browse-card" data-id="${esc(p.id)}" style="--i:${i%24}">
    <div class="thumb atlas-thumb browse-thumb">${mediaEl(p)}<button class="copy ${hasPrompt(p)?'has-prompt':''}" type="button">${copyLabel}</button>${generated}</div>
    <div class="card-body atlas-card-body browse-card-body"><div class="browse-meta"><span>${esc(sourceOf(p))}</span>${tools}</div><h3>${esc(p.title)}</h3><p>${esc(typeOf(p))}</p><div class="tags">${tags}</div></div>
  </article>`;
}
function visualText(p){ return [p.title, typeOf(p), sourceOf(p), ...(p.tags||[]), ...(p.aiTools||[])].join(' '); }
function uniquePosts(items){ return [...new Map(items.filter(Boolean).map(p => [p.id, p])).values()]; }
function laneCard(p, i, cls='lane-card'){
  return `<article class="${cls}" data-id="${esc(p.id)}" style="--i:${i}">
    <div class="lane-media-wrap">${mediaEl(p, 'lane-media')}</div>
    <div class="lane-copy"><span>${esc(sourceOf(p))}</span><b>${esc(p.title)}</b><small>${esc(typeOf(p))}</small></div>
  </article>`;
}
function pickByRegex(rx, limit=10){
  return posts.filter(p => hasPreview(p) && rx.test(visualText(p))).sort((a,b)=> (b.media?1:0) - (a.media?1:0)).slice(0, limit);
}
function renderShowcase(){
  const picks = heroCandidates();
  if(els.theatrePills){
    const pills = [['hero motion','hero'],['glass + 3D','glass'],['dashboards','dashboard'],['component tricks','component']];
    els.theatrePills.innerHTML = pills.map(([label,value])=>`<button type="button" data-chip="${esc(value)}">${esc(label)}</button>`).join('');
  }
  if(els.theatreSpotlight){
    const main = picks[1] || picks[0];
    const side = picks.slice(2,5);
    els.theatreSpotlight.innerHTML = main ? `<article class="spotlight-main" data-id="${esc(main.id)}">
      ${mediaEl(main, 'spotlight-media')}
      <div class="spotlight-copy"><span>${esc(sourceOf(main))}</span><h3>${esc(main.title)}</h3><p>${esc(typeOf(main))}</p><button class="copy ${hasPrompt(main)?'has-prompt':''}" type="button">Copy prompt</button></div>
    </article><div class="spotlight-stack">${side.map((p,i)=>laneCard(p,i,'spotlight-mini')).join('')}</div>` : '';
  }
  const strip = uniquePosts([...picks, ...pickByRegex(/animation|motion|gsap|scroll|3d|glass|hero|video/i, 12)]).slice(0,10);
  els.trend.innerHTML = strip.map((p,i)=>laneCard(p,i,'theatre-card')).join('');
  renderPatternLanes();
}
function renderPatternLanes(){
  if(!els.patternLanes) return;
  const lanes = [
    ['Hero motion', 'hero', /hero|landing|agency|website/i],
    ['Animation systems', 'animation', /animation|motion|gsap|scroll|transition|typewriter|marquee|trail|scramble/i],
    ['Glass, 3D, space', 'glass', /glass|3d|cosmic|space|particle|liquid|collectible|globe|orbit/i],
    ['Dashboards that feel alive', 'dashboard', /dashboard|command|analytics|ops|console|finance|revenue/i],
    ['Component tricks', 'component', /component|button|card|dock|carousel|popover|terminal|bento|beam/i]
  ];
  els.patternLanes.innerHTML = lanes.map(([title,filter,rx],idx)=>{
    const items = pickByRegex(rx, 9);
    return `<section class="pattern-lane" style="--lane:${idx}"><div class="lane-head"><h3>${esc(title)}</h3><button type="button" data-chip="${esc(filter)}">Filter</button></div><div class="lane-row">${items.map((p,i)=>laneCard(p,i)).join('')}</div></section>`;
  }).join('');
}
function heroCandidates(){
  const wanted = ['motionsites-liquid-glass-agency','motionsites-space-voyage','motionsites-framelix-3d-studios','website-cards-animation','synex','motionsites-ai-designer-agency','motionsites-buzzentic-agency','motionsites-terra-geo-map','motionsites-weblex-dark-hero'];
  const bySlug = new Map(posts.map(p => [p.slug, p]));
  const handPicked = wanted.map(slug => bySlug.get(slug)).filter(Boolean);
  const backup = posts
    .filter(p => hasPreview(p) && /hero|motion|animation|video|3d|glass|space|agency|gsap|scroll|interactive/i.test([p.title, typeOf(p), sourceOf(p), ...(p.tags||[])].join(' ')))
    .sort((a,b) => (b.media?1:0) - (a.media?1:0));
  return [...new Map([...handPicked, ...backup].map(p => [p.id, p])).values()].slice(0, 9);
}
function renderHeroLab(){
  if(!els.heroStage || !els.heroReel) return;
  const picks = heroCandidates();
  const primary = picks[0];
  if(!primary) return;
  els.heroStage.innerHTML = `<article class="hero-feature" data-id="${esc(primary.id)}">
    ${stillMediaEl(primary, 'hero-feature-media')}
    <div class="hero-feature-copy"><span>${esc(sourceOf(primary))}</span><h2>${esc(primary.title)}</h2><p>${esc(typeOf(primary))}</p></div>
  </article>
  <div class="hero-orbit" aria-hidden="true"><span>GSAP</span><span>liquid glass</span><span>3D</span><span>dashboards</span></div>`;
  els.heroReel.innerHTML = picks.slice(1, 7).map((p,i)=>`<article class="hero-reel-card" data-id="${esc(p.id)}" style="--i:${i}">
    ${stillMediaEl(p, 'hero-reel-media')}
    <div><span>${esc(sourceOf(p))}</span><b>${esc(p.title)}</b></div>
  </article>`).join('');
}
let revealObserver;
function applyReveals(){
  const items = document.querySelectorAll('.showreel-opening, .director-board, .catalog-lab, .atlas-card, .pattern-lane, .lens-group');
  if(!('IntersectionObserver' in window)){ items.forEach(el=>el.classList.add('is-visible')); return; }
  if(!revealObserver){
    revealObserver = new IntersectionObserver(entries => entries.forEach(entry => {
      if(entry.isIntersecting){ entry.target.classList.add('is-visible'); revealObserver.unobserve(entry.target); }
    }), { threshold: .08, rootMargin: '0px 0px -8% 0px' });
  }
  items.forEach(el => { if(!el.classList.contains('is-visible')) revealObserver.observe(el); });
}
function render(){
  applyFilters();
  renderStats();
  renderFacets();
  renderHeroLab();
  renderQuickChips();
  const promptCount = Object.keys(prompts).length;
  const curatedCount = posts.filter(p => p.promptOnly).length;
  const curatedWithPreview = posts.filter(p => p.promptOnly && hasPreview(p)).length;
  els.count.textContent = `${filtered.length} shown · ${posts.length} cards · ${curatedCount} curated (${curatedWithPreview} with previews) · ${promptCount} local prompts`;
  const active = [state.query && `search: ${state.query}`, state.source && `source: ${state.source}`, state.type && `type: ${typeLabel(state.type)}`, state.tag && `tag: ${state.tag}`, shuffleMode && 'random set'].filter(Boolean);
  els.activeFilters.textContent = active.join(' · ');
  els.grid.innerHTML = filtered.length ? filtered.map(card).join('') : `<div class="empty-state"><h3>No matching cards</h3><p>Clear filters or try a broader search like dashboard, hero, animation, or Magic UI.</p></div>`;
  document.querySelectorAll('video').forEach(v=>{ v.addEventListener('mouseenter',()=>v.play().catch(()=>{})); v.addEventListener('mouseleave',()=>{ if(!v.closest('.trend-card,.hero-feature,.hero-reel-card,.spotlight-main,.spotlight-mini,.theatre-card,.lane-card')){ v.pause(); v.currentTime=0; } }); if(v.closest('.trend-card,.hero-feature,.hero-reel-card,.spotlight-main,.spotlight-mini,.theatre-card,.lane-card')) v.play().catch(()=>{}); });
  applyReveals();
}
async function copyPrompt(p){
  const text = getPrompt(p);
  if(!text){ openModal(p); return; }
  try{ await navigator.clipboard.writeText(text); }
  catch(e){
    const ta = document.createElement('textarea');
    ta.value = text; ta.style.position = 'fixed'; ta.style.left = '-9999px';
    document.body.appendChild(ta); ta.focus(); ta.select(); document.execCommand('copy'); ta.remove();
  }
  const btn = document.querySelector(`[data-id="${CSS.escape(p.id)}"] .copy`);
  if(btn){ const old = btn.textContent; btn.textContent = 'Copied'; setTimeout(()=>btn.textContent=old, 1400); }
}
function openModal(p){
  const prompt = getPrompt(p);
  const source = p.sourceUrl || p.sourcePreview || '';
  els.modalBody.innerHTML = `${mediaEl(p,'modal-media')}<div class="modal-content">
    <span class="eyebrow">${esc(sourceOf(p))}</span><h2>${esc(p.title)}</h2><p>${esc(typeOf(p))}</p>
    <div class="modal-tags">${(p.tags||[]).map(t=>`<span class="tag">${esc(t)}</span>`).join('')}</div>
    <div class="modal-actions">${prompt?`<button id="copyFromModal" type="button">Copy local prompt</button>`:''}${source?`<a href="${esc(source)}" target="_blank" rel="noreferrer">Open source</a>`:''}</div>
    ${prompt?`<pre class="prompt-preview">${esc(prompt.slice(0,7000))}</pre>`:`<div class="notice"><b>No local prompt yet.</b><br><code>python3 scripts/add_prompt.py ${esc(p.slug)} --from-clipboard</code></div>`}
  </div>`;
  els.modal.showModal();
  const b = document.getElementById('copyFromModal');
  if(b) b.onclick = () => copyPrompt(p);
}
function findPostFromEvent(e){
  const item = e.target.closest('[data-id], [data-open]');
  if(!item) return null;
  const id = item.dataset.id || item.dataset.open;
  return posts.find(x => x.id === id);
}

document.addEventListener('click', e => {
  if(e.target.closest('.copy')){ const p = findPostFromEvent(e); if(p) copyPrompt(p); return; }
  const p = findPostFromEvent(e); if(p) openModal(p);
  const sourceBtn = e.target.closest('[data-source]');
  if(sourceBtn){ state.source = sourceBtn.dataset.source === state.source ? '' : sourceBtn.dataset.source; els.sourceSelect.value = state.source; shuffleMode = false; render(); }
  const tagBtn = e.target.closest('[data-tag]');
  if(tagBtn){ state.tag = tagBtn.dataset.tag === state.tag ? '' : tagBtn.dataset.tag; shuffleMode = false; render(); }
  const chipBtn = e.target.closest('[data-chip]');
  if(chipBtn){ state.query = chipBtn.dataset.chip; els.search.value = state.query; shuffleMode = false; render(); }
});
document.getElementById('closeModal').onclick = () => els.modal.close();
els.modal.addEventListener('click', e => { if(e.target === els.modal) els.modal.close(); });
els.search.addEventListener('input', e => { state.query = e.target.value.trim(); shuffleMode = false; render(); });
els.sourceSelect.addEventListener('change', e => { state.source = e.target.value; shuffleMode = false; render(); });
els.typeSelect.addEventListener('change', e => { state.type = e.target.value; shuffleMode = false; render(); });
document.getElementById('clearFilters').onclick = () => { state.query=''; state.source=''; state.type=''; state.tag=''; shuffleMode=false; els.search.value=''; els.sourceSelect.value=''; els.typeSelect.value=''; render(); };
document.getElementById('shuffleButton').onclick = () => { shuffleMode = !shuffleMode; render(); document.getElementById('library').scrollIntoView({behavior:'smooth'}); };
document.addEventListener('keydown', e => { if(e.key === '/' && document.activeElement !== els.search){ e.preventDefault(); els.search.focus(); } });

(async function init(){
  posts = await loadJson('data/posts.json', []);
  prompts = await loadJson('data/prompts.json', {});
  filtered = posts;
  setupControls();
  render();
})();
