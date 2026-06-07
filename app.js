let posts = [];
let prompts = {};
let patternCatalog = { summary: {}, patterns: [] };
let patterns = [];
let curation = { summary: {}, items: {}, bundles: [], antiSlopRules: [] };
let composition = { summary: {}, vocabulary: {}, roles: [], compatibility: { goodPairs: [], badPairs: [] }, items: {}, recipes: [] };
let filtered = [];
let shuffleMode = false;
const patternState = { query: '', behavior: '', context: '', role: '' };
const selectedPatterns = new Set();
const state = { query: '', source: '', type: '', tag: '', tier: 'canon' };
let previewObserver;

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
  tierSelect: document.getElementById('tierSelect'),
  sourceFacet: document.getElementById('sourceFacet'),
  tagFacet: document.getElementById('tagFacet'),
  quickChips: document.getElementById('quickChips'),
  scoutList: document.getElementById('scoutList'),
  heroStage: document.getElementById('heroStage'),
  heroReel: document.getElementById('heroReel'),
  theatreSpotlight: document.getElementById('theatreSpotlight'),
  theatrePills: document.getElementById('theatrePills'),
  patternLanes: document.getElementById('patternLanes'),
  bundleGrid: document.getElementById('bundleGrid'),
  bundleSelect: document.getElementById('bundleSelect'),
  outcomeInput: document.getElementById('outcomeInput'),
  vibeSelect: document.getElementById('vibeSelect'),
  composeBrief: document.getElementById('composeBrief'),
  copyBrief: document.getElementById('copyBrief'),
  briefOutput: document.getElementById('briefOutput'),
  recipeSelect: document.getElementById('recipeSelect'),
  recipeGrid: document.getElementById('recipeGrid'),
  vocabularyBoard: document.getElementById('vocabularyBoard'),
  patternGrid: document.getElementById('patternGrid'),
  patternCount: document.getElementById('patternCount'),
  patternSearch: document.getElementById('patternSearch'),
  behaviorSelect: document.getElementById('behaviorSelect'),
  contextSelect: document.getElementById('contextSelect'),
  roleSelect: document.getElementById('roleSelect'),
  mixIntent: document.getElementById('mixIntent'),
  kitTray: document.getElementById('kitTray'),
  kitBrief: document.getElementById('kitBrief')
};

async function loadJson(path, fallback){
  try { const r = await fetch(path); if(!r.ok) throw new Error(r.status); return await r.json(); }
  catch(e) { console.warn('Could not load', path, e); return fallback; }
}
function esc(s){ return String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
function sourceOf(p){ return p.sourceName || p.author || 'Local archive'; }
function typeOf(p){ return p.sectionType || 'Prompt'; }
function metaOf(p){ return curation.items?.[p.slug] || curation.items?.[p.id] || {}; }
function compOf(p){ return composition.items?.[p.slug] || composition.items?.[p.id] || {}; }
function selectedRecipe(){ return composition.recipes?.find(r => r.id === els.recipeSelect?.value) || composition.recipes?.[0]; }
function tierOf(p){ return metaOf(p).tier || 'useful'; }
function hasPrompt(p){ return Boolean(prompts[p.slug] || prompts[p.id]); }
function getPrompt(p){ return prompts[p.slug] || prompts[p.id] || ''; }
function hasPreview(p){ return Boolean(p.media || p.thumbnail); }
function postBySlug(slug){ return posts.find(p => p.slug === slug || p.id === slug); }
function bundleById(id){ return curation.bundles.find(b => b.id === id) || curation.bundles[0]; }
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
  ['landing|website|agency|saas|marketing|full page', 'Landing pages'],
  ['dashboard|analytics|command|ops|console|finance|revenue', 'Dashboards'],
  ['component|button|card|dock|popover|bento|carousel|form|pantry', 'Components'],
  ['animation|motion|gsap|scroll|transition|marquee', 'Animation systems'],
  ['3d|glass|particle|space|cosmic|liquid', '3D / glass'],
  ['onboarding|waitlist|login|signup', 'Onboarding / forms']
];
function typeOptionsHtml(){ return typeOptions.map(([value,label]) => `<option value="${esc(value)}">${esc(label)}</option>`).join(''); }
function typeLabel(value){ return (typeOptions.find(([v]) => v === value) || [value,value])[1]; }
function tierLabel(value){ return ({canon:'Canon', pantry:'Component pantry', archive:'Archive'})[value] || value; }
function matchesFilterGroup(value, hay){ return !value || value.split('|').some(token => hay.includes(normalize(token))); }
function visualText(p){
  const m = metaOf(p);
  const c = compOf(p);
  return [p.title, typeOf(p), sourceOf(p), p.author, ...(p.tags||[]), ...(p.aiTools||[]), m.tier, m.useCase, m.siteType, m.aesthetic, m.motionLevel, ...(m.normalizedTags||[]), ...(c.roles||[]), c.primaryRole, c.dominance, ...(c.vocabularyTerms||[])].join(' ');
}
function uniquePosts(items){ return [...new Map(items.filter(Boolean).map(p => [p.id, p])).values()]; }

function setupControls(){
  const sources = countBy(posts, sourceOf).map(([k])=>k);
  if(els.sourceSelect) els.sourceSelect.innerHTML = '<option value="">All sources</option>' + optionHtml(sources);
  if(els.typeSelect) els.typeSelect.innerHTML = typeOptionsHtml();
  if(els.tierSelect) els.tierSelect.value = state.tier;
  if(els.bundleSelect){
    els.bundleSelect.innerHTML = curation.bundles.map(b => `<option value="${esc(b.id)}">${esc(b.title)}</option>`).join('');
  }
  if(els.recipeSelect){
    els.recipeSelect.innerHTML = (composition.recipes || []).map(r => `<option value="${esc(r.id)}">${esc(r.title)}</option>`).join('');
  }
  if(els.behaviorSelect){
    const behaviors = [...new Set(patterns.map(p => p.behavior).filter(Boolean))].sort();
    els.behaviorSelect.innerHTML = '<option value="">All behaviors</option>' + optionHtml(behaviors);
  }
  if(els.contextSelect){
    const contexts = [...new Set(patterns.map(p => p.context).filter(Boolean))].sort();
    els.contextSelect.innerHTML = '<option value="">All contexts</option>' + optionHtml(contexts);
  }
  if(els.roleSelect){
    const roles = [...new Set(patterns.flatMap(p => p.mixRoles || []).filter(Boolean))].sort();
    els.roleSelect.innerHTML = '<option value="">All roles</option>' + optionHtml(roles);
  }
  renderQuickChips();
}
function renderQuickChips(){
  if(!els.quickChips) return;
  const chips = [
    ['Canon','canon','tier'],
    ['Pantry','pantry','tier'],
    ['Hero motion','hero','chip'],
    ['SaaS','saas','chip'],
    ['Dashboards','dashboard','chip'],
    ['Studio / portfolio','portfolio','chip'],
    ['Glass / 3D','3D','chip'],
    ['All shelves','','tier']
  ];
  els.quickChips.innerHTML = chips.map(([label,value,kind]) => {
    const active = kind === 'tier' ? state.tier === value : state.query === value;
    const attr = kind === 'tier' ? `data-tier="${esc(value)}"` : `data-chip="${esc(value)}"`;
    return `<button type="button" class="${active?'active':''}" ${attr}>${esc(label)}</button>`;
  }).join('');
}
function applyFilters(){
  const q = normalize(state.query);
  filtered = posts.filter(p => {
    const hay = normalize(visualText(p));
    if(q && !q.split(/\s+/).every(token => hay.includes(token))) return false;
    if(state.source && sourceOf(p) !== state.source) return false;
    if(state.type && !matchesFilterGroup(state.type, hay)) return false;
    if(state.tag && !hay.includes(normalize(state.tag))) return false;
    if(state.tier && tierOf(p) !== state.tier) return false;
    return true;
  }).sort((a,b) => {
    const ma = metaOf(a), mb = metaOf(b);
    return (mb.qualityScore || 0) - (ma.qualityScore || 0) || a.title.localeCompare(b.title);
  });
  if(shuffleMode) filtered = [...filtered].sort(() => Math.random() - 0.5).slice(0, 36);
}
function renderStats(){
  const featured = patterns.filter(p => p.quality === 'featured').length;
  const contexts = new Set(patterns.map(p => p.context).filter(Boolean)).size;
  const roles = new Set(patterns.flatMap(p => p.mixRoles || [])).size;
  document.getElementById('statTotal').textContent = patterns.length || posts.length;
  document.getElementById('statCurated').textContent = featured || (curation.summary?.canon ?? 0);
  document.getElementById('statPreviews').textContent = contexts || posts.filter(hasPreview).length;
  document.getElementById('statSources').textContent = roles || (curation.bundles?.length || 0);
  document.getElementById('promptTotal').textContent = `${patterns.length || 0} live effects`;
  els.navCount.textContent = `${patterns.length || 0} effects · ${featured || 0} featured`;
  const latest = patterns.slice(0,5);
  if(els.scoutList) els.scoutList.innerHTML = latest.map(p => `<button type="button" data-open-pattern="${esc(p.id)}"><span>${esc(p.behavior)}</span><b>${esc(p.title)}</b></button>`).join('');
}
function renderFacets(){
  if(!els.sourceFacet || !els.tagFacet) return;
  const srcCounts = countBy(posts, sourceOf).slice(0, 12);
  els.sourceFacet.innerHTML = srcCounts.map(([name,n]) => `<button type="button" class="${state.source===name?'active':''}" data-source="${esc(name)}"><span>${esc(name)}</span><b>${n}</b></button>`).join('');
  const tagCounts = countBy(posts.flatMap(p => (metaOf(p).normalizedTags || p.tags || []).map(t => ({tag:t})) ), x => x.tag).slice(0, 22);
  els.tagFacet.innerHTML = tagCounts.map(([name,n]) => `<button type="button" class="${state.tag===name?'active':''}" data-tag="${esc(name)}"><span>${esc(name)}</span><b>${n}</b></button>`).join('');
}
function card(p, i){
  const m = metaOf(p);
  const copyLabel = hasPrompt(p) ? 'Copy prompt' : 'Open source';
  const tags = (m.normalizedTags || p.tags || []).slice(0,3).map(t=>`<span class="tag">${esc(t)}</span>`).join('');
  const tools = (p.aiTools||[]).slice(0,1).map(t=>`<span class="pill">${esc(t)}</span>`).join('');
  const generated = p.previewGenerated ? '<span class="preview-note">concept sketch</span>' : '';
  const score = m.qualityScore ? `<span class="score-chip">${esc(m.qualityScore)}/5</span>` : '';
  return `<article class="card atlas-card browse-card tier-${esc(tierOf(p))}" data-id="${esc(p.id)}" style="--i:${i%24}">
    <div class="thumb atlas-thumb browse-thumb">${mediaEl(p)}<button class="copy ${hasPrompt(p)?'has-prompt':''}" type="button">${copyLabel}</button><span class="tier-chip">${esc(tierLabel(tierOf(p)))}</span>${score}${generated}</div>
    <div class="card-body atlas-card-body browse-card-body"><div class="browse-meta"><span>${esc(sourceOf(p))}</span>${tools}</div><h3>${esc(p.title)}</h3><p>${esc(m.useCase || typeOf(p))} · ${esc(m.aesthetic || typeOf(p))}</p><div class="tags">${tags}</div></div>
  </article>`;
}
function laneCard(p, i, cls='lane-card'){
  const m = metaOf(p);
  return `<article class="${cls}" data-id="${esc(p.id)}" style="--i:${i}">
    <div class="lane-media-wrap">${mediaEl(p, 'lane-media')}</div>
    <div class="lane-copy"><span>${esc(tierLabel(m.tier || 'useful'))}</span><b>${esc(p.title)}</b><small>${esc(m.useCase || typeOf(p))}</small></div>
  </article>`;
}
function pickByRegex(rx, limit=10){
  return posts.filter(p => hasPreview(p) && rx.test(visualText(p))).sort((a,b)=> (metaOf(b).qualityScore || 0) - (metaOf(a).qualityScore || 0)).slice(0, limit);
}
function heroCandidates(){
  const firstBundle = curation.bundles.find(b => b.id === 'motion-first-hero-kit') || curation.bundles[0];
  const wanted = firstBundle?.promptSlugs || ['motionsites-framelix-3d-studios','website-cards-animation','motionsites-space-voyage','synex'];
  const handPicked = wanted.map(postBySlug).filter(Boolean);
  const backup = posts
    .filter(p => hasPreview(p) && /hero|motion|animation|video|3d|glass|space|agency|gsap|scroll|interactive/i.test(visualText(p)))
    .sort((a,b) => (metaOf(b).qualityScore || 0) - (metaOf(a).qualityScore || 0));
  return [...new Map([...handPicked, ...backup].map(p => [p.id, p])).values()].slice(0, 9);
}
function renderHeroLab(){
  if(!els.heroStage || !els.heroReel) return;
  if(patterns.length){
    const picks = patterns.filter(p => p.quality === 'featured').slice(0, 7);
    const primary = picks[0];
    els.heroStage.innerHTML = `<article class="hero-feature pattern-hero-feature" data-pattern="${esc(primary.id)}">
      <iframe src="${esc(primary.previewUrl)}" title="${esc(primary.title)} hero preview" loading="eager"></iframe>
      <div class="hero-feature-copy"><span>Featured live effect · ${esc(primary.behavior)}</span><h2>${esc(primary.title)}</h2><p>${esc(primary.description)}</p></div>
    </article>`;
    els.heroReel.innerHTML = picks.slice(1, 7).map((p,i)=>`<article class="hero-reel-card pattern-hero-reel" data-pattern="${esc(p.id)}" style="--i:${i}">
      <iframe src="${esc(p.previewUrl)}" title="${esc(p.title)} mini preview" loading="lazy"></iframe>
      <div><span>${esc(p.behavior)}</span><b>${esc(p.title)}</b></div>
    </article>`).join('');
    return;
  }
  const picks = heroCandidates();
  const primary = picks[0];
  if(!primary) return;
  const m = metaOf(primary);
  els.heroStage.innerHTML = `<article class="hero-feature" data-id="${esc(primary.id)}">
    ${stillMediaEl(primary, 'hero-feature-media')}
    <div class="hero-feature-copy"><span>Canon reference · ${esc(m.aesthetic || sourceOf(primary))}</span><h2>${esc(primary.title)}</h2><p>${esc(m.useCase || typeOf(primary))}</p></div>
  </article>`;
  els.heroReel.innerHTML = picks.slice(1, 7).map((p,i)=>`<article class="hero-reel-card" data-id="${esc(p.id)}" style="--i:${i}">
    ${stillMediaEl(p, 'hero-reel-media')}
    <div><span>${esc(metaOf(p).useCase || sourceOf(p))}</span><b>${esc(p.title)}</b></div>
  </article>`).join('');
}
function renderBundleGrid(){
  if(!els.bundleGrid) return;
  els.bundleGrid.innerHTML = curation.bundles.map((bundle, idx) => {
    const refs = (bundle.promptSlugs || []).map(postBySlug).filter(Boolean).slice(0,4);
    const hero = postBySlug(bundle.heroSlug) || refs[0];
    const sectionList = (bundle.sections || []).slice(0,5).map(s => `<li>${esc(s)}</li>`).join('');
    return `<article class="bundle-card" data-bundle="${esc(bundle.id)}" style="--i:${idx}">
      <div class="bundle-media">${hero ? stillMediaEl(hero) : ''}<span>${esc(bundle.count || refs.length)} refs</span></div>
      <div class="bundle-body"><span class="bundle-kicker">Website kit</span><h3>${esc(bundle.title)}</h3><p>${esc(bundle.subtitle)}</p><ul>${sectionList}</ul>
      <div class="bundle-actions"><button type="button" data-bundle-compose="${esc(bundle.id)}">Compose brief</button><button type="button" data-bundle-filter="${esc(bundle.id)}">View refs</button></div></div>
    </article>`;
  }).join('');
}
function renderRecipeGrid(){
  if(!els.recipeGrid) return;
  els.recipeGrid.innerHTML = (composition.recipes || []).map((recipe, idx) => {
    const refs = (recipe.promptSlugs || []).map(postBySlug).filter(Boolean).slice(0,3);
    const slotList = Object.entries(recipe.selectionRules || {}).map(([slot, rule]) => `<li><b>${esc(slot)}</b><span>${esc(rule)}</span></li>`).join('');
    const directions = (recipe.designDirections || []).slice(0,3).map(d => `<span>${esc(d.label)}</span>`).join('');
    const pipelineCount = (recipe.pipeline || []).length;
    const thumbStack = refs.map(p => `<div>${stillMediaEl(p)}</div>`).join('');
    return `<article class="recipe-card" style="--i:${idx}">
      <div class="recipe-media">${thumbStack}</div>
      <div class="recipe-body"><span class="bundle-kicker">Mix recipe · ${esc(pipelineCount)} stage contract</span><h3>${esc(recipe.title)}</h3><p>${esc(recipe.outcome)} · ${esc(recipe.vibe)}</p><div class="direction-chips">${directions}</div><ul>${slotList}</ul>
      <div class="bundle-actions"><button type="button" data-recipe-compose="${esc(recipe.id)}">Use recipe</button><button type="button" data-recipe-filter="${esc(recipe.id)}">View ingredients</button></div></div>
    </article>`;
  }).join('');
}
function renderVocabularyBoard(){
  if(!els.vocabularyBoard) return;
  const categories = Object.entries(composition.vocabulary || {});
  els.vocabularyBoard.innerHTML = categories.map(([category, terms]) => `<article class="vocab-card">
    <h3>${esc(category)}</h3>
    <div>${terms.slice(0,8).map(term => `<button type="button" data-vocab="${esc(term.id)}"><b>${esc(term.label)}</b><span>${esc(term.definition)}</span></button>`).join('')}</div>
  </article>`).join('');
}
function selectedBundle(){
  return bundleById(els.bundleSelect?.value);
}
function vocabularyInstruction(termId){
  for(const terms of Object.values(composition.vocabulary || {})){
    const match = terms.find(t => t.id === termId);
    if(match) return `${match.label}: ${match.promptInstruction}`;
  }
  return termId;
}
function composeBrief(bundle = selectedBundle(), recipe = selectedRecipe()){
  if(!bundle || !els.briefOutput) return '';
  const outcome = els.outcomeInput?.value?.trim() || recipe?.outcome || 'premium website';
  const vibe = els.vibeSelect?.value || recipe?.vibe || 'calm editorial';
  const recipeRefs = (recipe?.promptSlugs || []).map(postBySlug).filter(Boolean);
  const bundleRefs = (bundle.promptSlugs || []).map(postBySlug).filter(Boolean);
  const refs = uniquePosts([...recipeRefs, ...bundleRefs]).slice(0,9);
  const referenceLines = refs.map((p, i) => {
    const m = metaOf(p);
    const c = compOf(p);
    const roles = (c.roles || []).slice(0,3).join(', ') || (m.useCase || typeOf(p));
    return `${i+1}. ${p.title} — role: ${roles}. Use: ${c.mixUse || `${m.useCase || typeOf(p)} / ${m.aesthetic || 'visual direction'}`} (${sourceOf(p)})`;
  }).join('\n');
  const avoidLines = refs.map(p => compOf(p).mixAvoid).filter(Boolean).slice(0,7).map(x => `- ${x}`).join('\n');
  const recipeRules = recipe?.selectionRules ? Object.entries(recipe.selectionRules).map(([slot, rule]) => `- ${slot}: ${rule}`).join('\n') : '';
  const termIds = [];
  refs.forEach(p => (compOf(p).vocabularyTerms || []).forEach(t => { if(!termIds.includes(t)) termIds.push(t); }));
  const vocabularyLines = termIds.slice(0,10).map(t => `- ${vocabularyInstruction(t)}`).join('\n');
  const rules = (curation.antiSlopRules || []).map(r => `- ${r}`).join('\n');
  const sections = (bundle.sections || []).map(s => `- ${s}`).join('\n');
  const inputLines = (recipe?.inputs || []).map(input => `- ${input.label || input.name}${input.required ? ' (required)' : ''}: ${input.type || 'string'}${input.options ? ` — ${input.options.join(', ')}` : ''}`).join('\n');
  const directionLines = (recipe?.designDirections || []).map(d => `- ${d.label}: ${d.tokens}. Use when ${d.useWhen}; avoid: ${d.avoid}.`).join('\n');
  const pipelineLines = (recipe?.pipeline || []).map(stage => `- ${stage.label}: ${stage.instruction}`).join('\n');
  const acceptanceLines = (recipe?.acceptanceCriteria || []).map(x => `- ${x}`).join('\n');
  const brief = `Build a ${outcome}.\n\nDirection:\n- Use the Framewell ${bundle.title}.\n- Remix recipe: ${recipe?.title || 'custom mix'}.\n- Vibe: ${vibe}.\n- Tone: ${bundle.tone}.\n- Combine references into one cohesive website; do not make a collage.\n\nPre-flight inputs to lock before designing:\n${inputLines || '- Surface, audience, product promise, and brand constraints.'}\n\nDesign direction options:\n${directionLines || '- Choose a clear visual direction before selecting references.'}\n\nMix grammar:\n1. Pick one dominant-structure reference as the page skeleton.\n2. Pick one visual-skin reference for typography, color, and atmosphere.\n3. Pick one motion-layer reference for choreography only.\n4. Add section-pattern and component-accent references as supporting ingredients.\n5. If references conflict, choose a dominant direction and demote the weaker idea to an accent or guardrail.\n\nRecipe slot rules:\n${recipeRules || '- Choose structure, style, motion, and sections separately before writing code.'}\n\nGeneration pipeline:\n${pipelineLines || '- Discover inputs.\n- Assign reference roles.\n- Generate the artifact.\n- Critique against the contract.\n- Explain source influence.'}\n\nRequired structure:\n${sections}\n\nSelected Framewell references:\n${referenceLines}\n\nVocabulary to use explicitly:\n${vocabularyLines}\n\nPer-reference avoid notes:\n${avoidLines}\n\nQuality rules:\n${rules}\n\nImplementation requirements:\n- Create production-ready responsive code.\n- Use a clear design system: color tokens, typography scale, spacing scale, states.\n- Build the hero first, then make every section support the same concept.\n- Include accessible contrast, keyboard-friendly controls, and mobile-specific composition.\n- Use motion sparingly: one memorable hero/scroll moment plus useful microinteractions.\n- Replace filler copy with specific, believable product language.\n\nAcceptance criteria:\n${acceptanceLines || '- Explain which reference supplied structure, style, motion, and component accents.\n- First viewport says what the product is, who it is for, and why it matters.\n- No fake metrics, no generic AI gradient cliché, no unreadable glassmorphism.\n- Motion terms are implemented intentionally, not merely mentioned.'}\n\nDeliverable:\nReturn the finished page/component plus a short note explaining the design choices and which references influenced each section.`;
  els.briefOutput.textContent = brief;
  return brief;
}
async function copyText(text){
  try{ await navigator.clipboard.writeText(text); }
  catch(e){
    const ta = document.createElement('textarea');
    ta.value = text; ta.style.position = 'fixed'; ta.style.left = '-9999px';
    document.body.appendChild(ta); ta.focus(); ta.select(); document.execCommand('copy'); ta.remove();
  }
}
async function copyPrompt(p){
  const text = getPrompt(p);
  if(!text){ openModal(p); return; }
  await copyText(text);
  const btn = document.querySelector(`[data-id="${CSS.escape(p.id)}"] .copy`);
  if(btn){ const old = btn.textContent; btn.textContent = 'Copied'; setTimeout(()=>btn.textContent=old, 1400); }
}
async function copyCurrentBrief(){
  const text = els.briefOutput?.textContent || composeBrief();
  await copyText(text);
  if(els.copyBrief){ const old = els.copyBrief.textContent; els.copyBrief.textContent = 'Copied'; setTimeout(()=>els.copyBrief.textContent=old, 1400); }
}
function openModal(p){
  const prompt = getPrompt(p);
  const source = p.sourceUrl || p.sourcePreview || '';
  const m = metaOf(p);
  const c = compOf(p);
  const metaBits = [m.tier && tierLabel(m.tier), m.useCase, m.siteType, m.aesthetic, m.motionLevel && `${m.motionLevel} motion`, c.primaryRole, m.qualityScore && `${m.qualityScore}/5`].filter(Boolean);
  const roleChips = (c.roles || []).map(t=>`<span class="tag role-tag">${esc(t)}</span>`).join('');
  const vocabChips = (c.vocabularyTerms || []).slice(0,10).map(t=>`<span class="tag vocab-tag">${esc(t)}</span>`).join('');
  els.modalBody.innerHTML = `${mediaEl(p,'modal-media')}<div class="modal-content">
    <span class="eyebrow">${esc(sourceOf(p))}</span><h2>${esc(p.title)}</h2><p>${esc(metaBits.join(' · ') || typeOf(p))}</p>
    <div class="modal-tags">${roleChips}${vocabChips}${(m.normalizedTags || p.tags || []).map(t=>`<span class="tag">${esc(t)}</span>`).join('')}</div>
    ${c.mixUse ? `<div class="mix-notes"><b>Mix use</b><p>${esc(c.mixUse)}</p><b>Avoid</b><p>${esc(c.mixAvoid)}</p></div>` : ''}
    <div class="modal-actions">${prompt?`<button id="copyFromModal" type="button">Copy local prompt</button>`:''}<button id="briefFromModal" type="button">Use in website brief</button>${source?`<a href="${esc(source)}" target="_blank" rel="noreferrer">Open source</a>`:''}</div>
    ${prompt?`<pre class="prompt-preview">${esc(prompt.slice(0,7000))}</pre>`:`<div class="notice"><b>No local prompt yet.</b><br><code>python3 scripts/add_prompt.py ${esc(p.slug)} --from-clipboard</code></div>`}
  </div>`;
  els.modal.showModal();
  const b = document.getElementById('copyFromModal');
  if(b) b.onclick = () => copyPrompt(p);
  const brief = document.getElementById('briefFromModal');
  if(brief) brief.onclick = () => {
    const match = curation.bundles.find(bundle => (bundle.promptSlugs || []).includes(p.slug)) || curation.bundles[0];
    if(match && els.bundleSelect) els.bundleSelect.value = match.id;
    composeBrief(match);
    els.modal.close();
    document.getElementById('composer')?.scrollIntoView({behavior:'smooth'});
  };
}
function findPostFromEvent(e){
  const item = e.target.closest('[data-id], [data-open]');
  if(!item) return null;
  const id = item.dataset.id || item.dataset.open;
  return posts.find(x => x.id === id);
}
function applyBundleFilter(bundleId){
  const bundle = bundleById(bundleId);
  const slugs = new Set(bundle?.promptSlugs || []);
  state.query = '';
  state.source = '';
  state.type = '';
  state.tag = '';
  state.tier = '';
  shuffleMode = false;
  if(els.search) els.search.value = '';
  if(els.sourceSelect) els.sourceSelect.value = '';
  if(els.typeSelect) els.typeSelect.value = '';
  if(els.tierSelect) els.tierSelect.value = '';
  filtered = posts.filter(p => slugs.has(p.slug));
  renderStats(); renderFacets(); renderQuickChips();
  els.count.textContent = `${filtered.length} shown · ${bundle.title}`;
  els.activeFilters.textContent = `kit: ${bundle.title}`;
  els.grid.innerHTML = filtered.map(card).join('');
  applyVideoBehavior(); applyReveals();
  document.getElementById('library')?.scrollIntoView({behavior:'smooth'});
}
function applyRecipeFilter(recipeId){
  const recipe = (composition.recipes || []).find(r => r.id === recipeId);
  const slugs = new Set(recipe?.promptSlugs || []);
  state.query = '';
  state.source = '';
  state.type = '';
  state.tag = '';
  state.tier = '';
  shuffleMode = false;
  if(els.search) els.search.value = '';
  if(els.sourceSelect) els.sourceSelect.value = '';
  if(els.typeSelect) els.typeSelect.value = '';
  if(els.tierSelect) els.tierSelect.value = '';
  filtered = posts.filter(p => slugs.has(p.slug));
  renderStats(); renderFacets(); renderQuickChips();
  els.count.textContent = `${filtered.length} shown · ${recipe?.title || 'recipe ingredients'}`;
  els.activeFilters.textContent = `recipe: ${recipe?.title || recipeId}`;
  els.grid.innerHTML = filtered.map(card).join('');
  applyVideoBehavior(); applyReveals();
  document.getElementById('library')?.scrollIntoView({behavior:'smooth'});
}
let revealObserver;
function applyReveals(){
  const items = document.querySelectorAll('.kit-lab, .brief-composer, .composition-lab, .vocabulary-lab, .showreel-opening, .director-board, .catalog-lab, .atlas-card, .pattern-lane, .lens-group, .bundle-card, .recipe-card, .vocab-card');
  if(!('IntersectionObserver' in window)){ items.forEach(el=>el.classList.add('is-visible')); return; }
  if(!revealObserver){
    revealObserver = new IntersectionObserver(entries => entries.forEach(entry => {
      if(entry.isIntersecting){ entry.target.classList.add('is-visible'); revealObserver.unobserve(entry.target); }
    }), { threshold: .08, rootMargin: '0px 0px -8% 0px' });
  }
  items.forEach(el => { if(!el.classList.contains('is-visible')) revealObserver.observe(el); });
}
function applyVideoBehavior(){
  document.querySelectorAll('video').forEach(v=>{
    v.addEventListener('mouseenter',()=>v.play().catch(()=>{}));
    v.addEventListener('mouseleave',()=>{ if(!v.closest('.trend-card,.hero-feature,.hero-reel-card,.spotlight-main,.spotlight-mini,.theatre-card,.lane-card,.bundle-media')){ v.pause(); v.currentTime=0; } });
    if(v.closest('.trend-card,.hero-feature,.hero-reel-card,.spotlight-main,.spotlight-mini,.theatre-card,.lane-card,.bundle-media')) v.play().catch(()=>{});
  });
}
function filteredPatterns(){
  const q = normalize(patternState.query);
  return patterns.filter(p => {
    const hay = normalize([p.title, p.behavior, p.context, p.description, ...(p.tags || []), ...(p.sourcePromptIds || [])].join(' '));
    if(q && !q.split(/\s+/).every(token => hay.includes(token))) return false;
    if(patternState.behavior && p.behavior !== patternState.behavior) return false;
    if(patternState.context && p.context !== patternState.context) return false;
    if(patternState.role && !(p.mixRoles || []).includes(patternState.role)) return false;
    return true;
  });
}
function patternCard(p, i){
  const selected = selectedPatterns.has(p.id);
  const tags = (p.tags || []).slice(0,4).map(t => `<span class="tag">${esc(t)}</span>`).join('');
  const roles = (p.mixRoles || []).slice(0,2).map(t => `<span class="role-pill">${esc(t)}</span>`).join('');
  const sources = (p.sourcePromptIds || []).slice(0,2).map(id => `<span>${esc(id)}</span>`).join('');
  return `<article class="live-pattern-card ${selected ? 'is-selected' : ''}" data-pattern="${esc(p.id)}" style="--i:${i}">
    <div class="pattern-frame live-preview-slot" data-preview-src="${esc(p.previewUrl)}" data-preview-title="${esc(p.title)} live effect">
      <div class="preview-loading"><span>${esc(p.behavior)}</span><b>${esc(p.title)}</b><small>Loading actual live specimen…</small></div>
    </div>
    <div class="pattern-body"><div class="browse-meta"><span>${esc(p.behavior)}</span><span>${esc(p.context)}</span><span>${esc(p.quality || 'specimen')}</span></div><h3>${esc(p.title)}</h3><p>${esc(p.description)}</p><div class="role-row">${roles}</div><div class="tags">${tags}</div><div class="pattern-source">Lineage ${sources || '<span>local specimen</span>'}</div>
    <div class="pattern-actions"><button type="button" data-open-pattern="${esc(p.id)}">Open large</button><button type="button" data-copy-pattern="${esc(p.id)}">Copy code</button><button type="button" data-copy-pattern-prompt="${esc(p.id)}">Copy prompt</button><button type="button" data-toggle-pattern="${esc(p.id)}">${selected ? 'Selected' : 'Add to mix'}</button></div></div>
  </article>`;
}
function renderKitTray(){
  if(!els.kitTray) return;
  const picked = [...selectedPatterns].map(id => patterns.find(p => p.id === id)).filter(Boolean);
  if(!picked.length){
    els.kitTray.innerHTML = '<span>Mix kit empty</span><p>Select live patterns to generate a combined AI instruction.</p>';
    if(els.kitBrief) els.kitBrief.hidden = true;
    return;
  }
  els.kitTray.innerHTML = `<span>${picked.length} selected</span><p>${picked.map(p => esc(p.title)).join(' · ')}</p><button type="button" data-copy-live-kit>Copy mix brief</button><button type="button" data-clear-live-kit>Clear</button>`;
  if(els.kitBrief){ els.kitBrief.hidden = false; els.kitBrief.textContent = liveKitBrief(picked); }
}
function applyMixPreset(name){
  const rules = {
    portfolio: {
      intent: 'a high-end interactive portfolio with shader transitions and cinematic case studies',
      ids: ['brush-shader-project-reveal','infinite-3d-corridor-scroll','scroll-driven-3d-room','dom-to-canvas-handoff','horizontal-scroll-project-world','elastic-cursor-work-index']
    },
    'ai-dashboard': {
      intent: 'an AI product dashboard with command surfaces, agent reasoning, and dense evidence views',
      ids: ['spatial-command-room','ai-map-of-thought','command-center-alert-lens','data-lineage-river','audit-evidence-peek','liquid-drag-dashboard']
    },
    'saas-hero': {
      intent: 'a premium SaaS landing page with a memorable 3D product hero and conversion proof',
      ids: ['scroll-synced-model-exploder','orbital-product-stage','glass-torus-pricing','liquid-metal-cta','stats-countup-proof-band','copy-button-success-sweep']
    },
    wild: {
      intent: 'a distinctive but usable product site with one weird signature interaction',
      ids: ['webgpu-particle-logo-field','water-shader-page-transition','interactive-canvas-puzzle','shader-noise-navigation','immersive-case-study-portal','glassmorphic-audio-reactor']
    }
  }[name];
  if(!rules) return;
  selectedPatterns.clear();
  rules.ids.filter(id => patterns.some(p => p.id === id)).forEach(id => selectedPatterns.add(id));
  if(els.mixIntent) els.mixIntent.value = rules.intent;
  patternState.query = '';
  patternState.behavior = '';
  patternState.context = '';
  patternState.role = '';
  if(els.patternSearch) els.patternSearch.value = '';
  if(els.behaviorSelect) els.behaviorSelect.value = '';
  if(els.contextSelect) els.contextSelect.value = '';
  if(els.roleSelect) els.roleSelect.value = '';
  renderPatternStudio();
  document.getElementById('kitTray')?.scrollIntoView({behavior:'smooth', block:'center'});
}
function liveKitBrief(picked){
  const intent = els.mixIntent?.value?.trim() || 'my existing product';
  return `Goal: build ${intent}.\n\nIntegrate these Framewell live UI patterns without replacing the app structure. Combine them as atoms: one signature moment, one navigation/control idea, supporting product-surface effects, and only the microinteractions that genuinely help. Keep one coherent art direction; do not collage styles.\n\nSelected patterns:\n${picked.map((p,i)=>`${i+1}. ${p.title} — ${p.description} Behavior: ${p.behavior}. Context: ${p.context}. Mix role: ${(p.mixRoles||[]).join(', ') || 'supporting effect'}. Tags: ${(p.tags||[]).join(', ')}.`).join('\n')}\n\nImplementation rules:\n- Treat each pattern as an isolated behavior/specimen, not a full page template.\n- First assign each pattern a job: structure, signature motion, data surface, control, proof, or microinteraction.\n- Reuse my existing data model, components, typography, and color tokens.\n- Add the smallest necessary HTML/CSS/JS or framework code.\n- Use real states: loading, hover/focus, keyboard, empty/error, mobile, reduced motion.\n- If two effects compete, keep the stronger one and demote the other to a subtle detail.\n- Explain which pattern influenced each change.`;
}
function renderPatternStudio(){
  if(!els.patternGrid) return;
  const items = filteredPatterns();
  if(els.patternCount) els.patternCount.textContent = `${items.length} shown · ${patterns.length} live effects · open any card for full specimen`;
  els.patternGrid.innerHTML = items.length ? items.map(patternCard).join('') : `<div class="empty-state"><h3>No live patterns found</h3><p>Try scroll, dashboard, hover, proof, AI, or clear the filters.</p></div>`;
  hydrateVisiblePreviews();
  renderKitTray();
}
function hydrateVisiblePreviews(){
  const slots = [...document.querySelectorAll('.live-preview-slot[data-preview-src]')];
  if(previewObserver) previewObserver.disconnect();
  const mount = slot => {
    if(slot.dataset.loaded) return;
    slot.dataset.loaded = 'true';
    const iframe = document.createElement('iframe');
    iframe.src = slot.dataset.previewSrc;
    iframe.title = slot.dataset.previewTitle || 'Live effect preview';
    iframe.loading = 'lazy';
    iframe.setAttribute('sandbox','allow-scripts allow-same-origin');
    iframe.addEventListener('load', () => slot.classList.add('is-loaded'), { once:true });
    slot.appendChild(iframe);
  };
  if(!('IntersectionObserver' in window)){
    slots.slice(0, 16).forEach(mount);
    return;
  }
  previewObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if(entry.isIntersecting){ mount(entry.target); previewObserver.unobserve(entry.target); }
    });
  }, { rootMargin: '420px 0px', threshold: 0.01 });
  slots.forEach(slot => previewObserver.observe(slot));
}
async function copyPatternCode(id){
  const p = patterns.find(x => x.id === id); if(!p) return;
  await copyText(p.code || '');
}
async function copyPatternPrompt(id){
  const p = patterns.find(x => x.id === id); if(!p) return;
  await copyText(p.prompt || '');
}
function openPatternModal(id){
  const p = patterns.find(x => x.id === id); if(!p || !els.modalBody) return;
  const tags = (p.tags || []).map(t=>`<span class="tag">${esc(t)}</span>`).join('');
  const sourceLinks = (p.sourcePromptIds || []).map(src => {
    const sourcePost = postBySlug(src);
    return sourcePost ? `<button type="button" data-open="${esc(sourcePost.id)}">${esc(sourcePost.title)}</button>` : `<span>${esc(src)}</span>`;
  }).join('');
  els.modalBody.innerHTML = `<div class="pattern-modal-preview"><iframe src="${esc(p.previewUrl)}" title="${esc(p.title)} live preview"></iframe></div><div class="modal-content pattern-modal-content">
    <span class="eyebrow">Live pattern · ${esc(p.behavior)} · ${esc(p.context)}</span><h2>${esc(p.title)}</h2><p>${esc(p.description)}</p><div class="modal-tags">${tags}</div>
    <div class="modal-actions"><button type="button" id="copyPatternCode">Copy code</button><button type="button" id="copyPatternPrompt">Copy prompt</button><button type="button" id="selectPatternForMix">${selectedPatterns.has(p.id) ? 'Remove from mix' : 'Add to mix'}</button></div>
    <div class="mix-notes"><b>Archive lineage</b><p class="source-buttons">${sourceLinks || 'Local live specimen'}</p><b>Prompt</b><p>${esc(p.prompt || '')}</p></div>
    <pre class="prompt-preview">${esc((p.code || '').slice(0,9000))}</pre>
  </div>`;
  els.modal.showModal();
  document.getElementById('copyPatternCode').onclick = () => copyPatternCode(p.id);
  document.getElementById('copyPatternPrompt').onclick = () => copyPatternPrompt(p.id);
  document.getElementById('selectPatternForMix').onclick = (event) => {
    selectedPatterns.has(p.id) ? selectedPatterns.delete(p.id) : selectedPatterns.add(p.id);
    event.currentTarget.textContent = selectedPatterns.has(p.id) ? 'Remove from mix' : 'Add to mix';
    renderPatternStudio();
  };
}

function render(){
  applyFilters();
  renderStats();
  renderFacets();
  renderHeroLab();
  renderPatternStudio();
  renderBundleGrid();
  renderRecipeGrid();
  renderVocabularyBoard();
  renderQuickChips();
  const promptCount = Object.keys(prompts).length;
  const counts = curation.summary || {};
  els.count.textContent = `${filtered.length} shown · ${counts.canon || 0} canon · ${counts.pantry || 0} pantry · ${counts.archive || 0} archive · ${promptCount} local prompts`;
  const active = [state.query && `search: ${state.query}`, state.source && `source: ${state.source}`, state.type && `type: ${typeLabel(state.type)}`, state.tier && `shelf: ${tierLabel(state.tier)}`, state.tag && `tag: ${state.tag}`, shuffleMode && 'random set'].filter(Boolean);
  els.activeFilters.textContent = active.join(' · ');
  els.grid.innerHTML = filtered.length ? filtered.map(card).join('') : `<div class="empty-state"><h3>No matching cards</h3><p>Clear filters or try a broader search like dashboard, hero, animation, or Magic UI.</p></div>`;
  applyVideoBehavior();
  composeBrief();
  applyReveals();
}

document.addEventListener('click', e => {
  const openPatternBtn = e.target.closest('[data-open-pattern]');
  if(openPatternBtn){ openPatternModal(openPatternBtn.dataset.openPattern); return; }
  const copyPatternBtn = e.target.closest('[data-copy-pattern]');
  if(copyPatternBtn){ copyPatternCode(copyPatternBtn.dataset.copyPattern); return; }
  const copyPatternPromptBtn = e.target.closest('[data-copy-pattern-prompt]');
  if(copyPatternPromptBtn){ copyPatternPrompt(copyPatternPromptBtn.dataset.copyPatternPrompt); return; }
  const togglePatternBtn = e.target.closest('[data-toggle-pattern]');
  if(togglePatternBtn){ const id = togglePatternBtn.dataset.togglePattern; selectedPatterns.has(id) ? selectedPatterns.delete(id) : selectedPatterns.add(id); renderPatternStudio(); return; }
  if(e.target.closest('[data-copy-live-kit]')){ const picked = [...selectedPatterns].map(id => patterns.find(p => p.id === id)).filter(Boolean); copyText(liveKitBrief(picked)); return; }
  if(e.target.closest('[data-clear-live-kit]')){ selectedPatterns.clear(); renderPatternStudio(); return; }
  const presetBtn = e.target.closest('[data-mix-preset]');
  if(presetBtn){ applyMixPreset(presetBtn.dataset.mixPreset); return; }
  const patternCardEl = e.target.closest('[data-pattern]');
  if(patternCardEl && !e.target.closest('iframe,button,a')){ openPatternModal(patternCardEl.dataset.pattern); return; }
  if(e.target.closest('.copy')){ const p = findPostFromEvent(e); if(p) copyPrompt(p); return; }
  const composeBtn = e.target.closest('[data-bundle-compose]');
  if(composeBtn){ const id = composeBtn.dataset.bundleCompose; if(els.bundleSelect) els.bundleSelect.value = id; composeBrief(bundleById(id)); document.getElementById('composer')?.scrollIntoView({behavior:'smooth'}); return; }
  const recipeComposeBtn = e.target.closest('[data-recipe-compose]');
  if(recipeComposeBtn){ const id = recipeComposeBtn.dataset.recipeCompose; if(els.recipeSelect) els.recipeSelect.value = id; composeBrief(selectedBundle(), selectedRecipe()); document.getElementById('composer')?.scrollIntoView({behavior:'smooth'}); return; }
  const filterBtn = e.target.closest('[data-bundle-filter]');
  if(filterBtn){ applyBundleFilter(filterBtn.dataset.bundleFilter); return; }
  const recipeFilterBtn = e.target.closest('[data-recipe-filter]');
  if(recipeFilterBtn){ applyRecipeFilter(recipeFilterBtn.dataset.recipeFilter); return; }
  const vocabBtn = e.target.closest('[data-vocab]');
  if(vocabBtn){ state.query = vocabBtn.dataset.vocab; if(els.search) els.search.value = state.query; shuffleMode = false; render(); document.getElementById('library')?.scrollIntoView({behavior:'smooth'}); return; }
  const p = findPostFromEvent(e); if(p){ openModal(p); return; }
  const sourceBtn = e.target.closest('[data-source]');
  if(sourceBtn){ state.source = sourceBtn.dataset.source === state.source ? '' : sourceBtn.dataset.source; els.sourceSelect.value = state.source; shuffleMode = false; render(); return; }
  const tagBtn = e.target.closest('[data-tag]');
  if(tagBtn){ state.tag = tagBtn.dataset.tag === state.tag ? '' : tagBtn.dataset.tag; shuffleMode = false; render(); return; }
  const tierBtn = e.target.closest('[data-tier]');
  if(tierBtn){ state.tier = tierBtn.dataset.tier; if(els.tierSelect) els.tierSelect.value = state.tier; shuffleMode = false; render(); return; }
  const chipBtn = e.target.closest('[data-chip]');
  if(chipBtn){ state.query = chipBtn.dataset.chip; els.search.value = state.query; shuffleMode = false; render(); }
});
if(document.getElementById('closeModal')) document.getElementById('closeModal').onclick = () => els.modal.close();
els.modal.addEventListener('click', e => { if(e.target === els.modal) els.modal.close(); });
els.search.addEventListener('input', e => { state.query = e.target.value.trim(); shuffleMode = false; render(); });
els.sourceSelect.addEventListener('change', e => { state.source = e.target.value; shuffleMode = false; render(); });
els.typeSelect.addEventListener('change', e => { state.type = e.target.value; shuffleMode = false; render(); });
if(els.tierSelect) els.tierSelect.addEventListener('change', e => { state.tier = e.target.value; shuffleMode = false; render(); });
if(els.bundleSelect) els.bundleSelect.addEventListener('change', () => composeBrief());
if(els.recipeSelect) els.recipeSelect.addEventListener('change', () => composeBrief());
if(els.outcomeInput) els.outcomeInput.addEventListener('input', () => composeBrief());
if(els.vibeSelect) els.vibeSelect.addEventListener('change', () => composeBrief());
if(els.composeBrief) els.composeBrief.onclick = () => composeBrief();
if(els.copyBrief) els.copyBrief.onclick = () => copyCurrentBrief();
if(els.patternSearch) els.patternSearch.addEventListener('input', e => { patternState.query = e.target.value.trim(); renderPatternStudio(); });
if(els.behaviorSelect) els.behaviorSelect.addEventListener('change', e => { patternState.behavior = e.target.value; renderPatternStudio(); });
if(els.contextSelect) els.contextSelect.addEventListener('change', e => { patternState.context = e.target.value; renderPatternStudio(); });
if(els.roleSelect) els.roleSelect.addEventListener('change', e => { patternState.role = e.target.value; renderPatternStudio(); });
if(els.mixIntent) els.mixIntent.addEventListener('input', () => renderKitTray());
document.getElementById('clearFilters').onclick = () => { state.query=''; state.source=''; state.type=''; state.tag=''; state.tier=''; shuffleMode=false; els.search.value=''; els.sourceSelect.value=''; els.typeSelect.value=''; if(els.tierSelect) els.tierSelect.value=''; render(); };
document.getElementById('shuffleButton').onclick = () => { shuffleMode = !shuffleMode; render(); document.getElementById('patterns').scrollIntoView({behavior:'smooth'}); };
document.addEventListener('keydown', e => { if(e.key === '/' && document.activeElement !== els.patternSearch){ e.preventDefault(); (els.patternSearch || els.search).focus(); } });

(async function init(){
  posts = await loadJson('data/posts.json', []);
  prompts = await loadJson('data/prompts.json', {});
  patternCatalog = await loadJson('data/patterns.json', patternCatalog);
  patterns = patternCatalog.patterns || [];
  curation = await loadJson('data/curation.json', curation);
  composition = await loadJson('data/composition.json', composition);
  filtered = posts;
  setupControls();
  render();
})();
