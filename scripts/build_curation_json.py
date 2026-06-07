#!/usr/bin/env python3
"""Build Framewell curation metadata.

The app keeps all raw prompts, but this generated file makes the experience
bundle-first: normalized taxonomy, quality tiers, canon/archive flags, and
ready-to-copy website-building recipes.
"""
import json
import pathlib
import re
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]
POSTS_PATH = ROOT / 'data' / 'posts.json'
PROMPTS_PATH = ROOT / 'data' / 'prompts.json'
OUT_PATH = ROOT / 'data' / 'curation.json'

TAG_ALIASES = {
    'hero section': 'hero',
    'Hero Section': 'hero',
    'Hero': 'hero',
    'AI website': 'ai website',
    '3D Website': '3d',
    '3D': '3d',
    'GSAP': 'gsap',
    'SaaS': 'saas',
    'Portfolio': 'portfolio',
    'MotionSites': 'motionsites',
    'Magic UI': 'magic ui',
    'Cult UI': 'cult ui',
    'Tailark': 'tailark',
}

USE_CASE_RULES = [
    ('hero', r'\bhero\b|waitlist|homepage|landing page|website'),
    ('full page', r'landing page|homepage|website|portfolio|agency|saas|ecommerce|commerce|waitlist|docs-first|launch'),
    ('dashboard', r'dashboard|analytics|command|ops|console|finance|revenue|inventory|observability'),
    ('section', r'pricing|faq|testimonial|stats|team|footer|feature|bento|integrations|logo cloud'),
    ('component', r'button|card|dock|popover|carousel|form|terminal|loader|typewriter|scramble|marquee|beam|grid|globe|map'),
    ('motion system', r'animation|motion|gsap|scroll|transition|kinetic|particle|trail|reveal'),
]

SITE_RULES = [
    ('ai product', r'\bai\b|workflow|image generator|notebook|writing assistant|automation|agent'),
    ('saas', r'saas|software|product|pricing|revenue|enterprise|security|ops|dashboard'),
    ('agency / studio', r'agency|studio|creative|designer|portfolio|case study'),
    ('devtool / docs', r'devtool|docs|open source|coding|terminal|file tree|code|api'),
    ('dashboard app', r'dashboard|analytics|command|ops|console|finance|inventory|observability'),
    ('commerce / luxury', r'ecommerce|commerce|fashion|tea|luxury|automotive|jets|collectible'),
    ('content / education', r'blog|academy|course|notes|field notes|styleguide'),
]

AESTHETIC_RULES = [
    ('cinematic 3d', r'3d|space|cosmic|voyage|collectible|globe|orbit|particle|cinematic'),
    ('glass / luminous', r'glass|liquid|glow|aurora|metal|backlight|shine|blur'),
    ('editorial / luxury', r'fashion|tea|editorial|luxury|museum|automotive|portfolio|field notes'),
    ('technical / command', r'dashboard|command|terminal|code|security|ops|docs|devtool|data'),
    ('playful / tactile', r'duolingo|pixel|ripple|swipe|dynamic island|blob|dithering|cards'),
    ('minimal marketing', r'tailark|pricing|faq|testimonial|logo cloud|feature|stats|final cta'),
]

BUNDLES = [
    {
        'id': 'saas-landing-kit',
        'title': 'SaaS Landing Page Kit',
        'subtitle': 'Product proof, feature bento, pricing, FAQ, and final CTA.',
        'query': r'saas|software|landing page|pricing|feature|bento|integrations|testimonial|faq|stats|final cta|product launch|revenue',
        'avoid': r'fashion|portfolio|cosmic portfolio|loader',
        'tone': 'clean product marketing with strong proof and restrained visual drama',
        'sections': ['hero', 'proof band', 'feature bento', 'workflow/product preview', 'pricing', 'FAQ', 'final CTA'],
    },
    {
        'id': 'ai-product-launch-kit',
        'title': 'AI Product Launch Kit',
        'subtitle': 'Hero, workflow visual, trust layer, and waitlist/launch copy.',
        'query': r'\bai\b|workflow|automation|image generator|notebook|writing assistant|agent|waitlist|bloom|neural|sentinel|stellar|power ai',
        'avoid': r'button|dock|popover|footer',
        'tone': 'credible AI product, not generic purple-gradient slop',
        'sections': ['clear promise hero', 'workflow visual', 'model/process explanation', 'trust/security', 'use cases', 'CTA'],
    },
    {
        'id': 'portfolio-studio-kit',
        'title': 'Portfolio / Studio Kit',
        'subtitle': 'Editorial hero, selected work, case studies, services, and contact.',
        'query': r'portfolio|agency|studio|creative|designer|case study|fashion|field notes|museum',
        'avoid': r'dashboard|pricing comparison|security page',
        'tone': 'tasteful editorial studio with confident spacing and memorable motion',
        'sections': ['editorial hero', 'selected work', 'case-study cards', 'services', 'about', 'contact CTA'],
    },
    {
        'id': 'dashboard-product-kit',
        'title': 'Dashboard Product Kit',
        'subtitle': 'Command center, analytics panels, app states, and workflow surfaces.',
        'query': r'dashboard|analytics|command|ops|console|finance|revenue|inventory|observability|mail|calendar|chat support|data',
        'avoid': r'fashion|tea|portfolio cosmic',
        'tone': 'dense but calm product interface that feels real and operable',
        'sections': ['dashboard hero', 'live metrics preview', 'workflow panels', 'alerts/states', 'integrations', 'security/trust'],
    },
    {
        'id': 'motion-first-hero-kit',
        'title': 'Motion-First Hero Kit',
        'subtitle': '3D, video, particle, kinetic type, and scroll-driven hero ideas.',
        'query': r'hero|motion|animation|gsap|scroll|video|3d|particle|kinetic|cards animation|liquid metal|space voyage|automotive',
        'avoid': r'faq|pricing|footer|team grid',
        'tone': 'one memorable above-the-fold idea with motion that explains the product',
        'sections': ['motion concept', 'headline system', 'visual proof object', 'CTA pair', 'scroll handoff'],
    },
    {
        'id': 'luxury-editorial-kit',
        'title': 'Luxury / Editorial Kit',
        'subtitle': 'Refined typography, slow reveals, product atmosphere, and gallery rhythm.',
        'query': r'luxury|fashion|tea|editorial|museum|automotive|jets|wanderful|portfolio|field notes|neo museum',
        'avoid': r'ops|dashboard|terminal|security',
        'tone': 'quiet premium editorial, image-led and typography-led',
        'sections': ['editorial hero', 'image rhythm', 'story/provenance', 'collection grid', 'soft CTA'],
    },
    {
        'id': 'devtool-open-source-kit',
        'title': 'Open Source / Devtool Kit',
        'subtitle': 'Docs-first product pages, terminal demos, GitHub proof, and API sections.',
        'query': r'devtool|docs|open source|coding|terminal|file tree|code|api|github|codenest|ixartz',
        'avoid': r'fashion|luxury|portfolio cosmic',
        'tone': 'technical, legible, trustworthy; useful before flashy',
        'sections': ['devtool hero', 'terminal/API demo', 'feature grid', 'docs preview', 'community proof', 'CTA'],
    },
    {
        'id': 'component-pantry',
        'title': 'Component Pantry',
        'subtitle': 'Buttons, loaders, beams, cards, docks, and other accents to remix into pages.',
        'query': r'button|card|dock|popover|loader|typewriter|scramble|beam|grid|marquee|carousel|globe|map|ripple|sparkles|terminal',
        'avoid': r'full page|landing page|homepage',
        'tone': 'small reusable interaction patterns, not standalone websites',
        'sections': ['accent motion', 'microinteraction', 'supporting component', 'implementation note'],
    },
]

ANTI_SLOP_RULES = [
    'No generic purple-blue AI gradients unless the brand explicitly calls for them.',
    'No fake dashboards or meaningless metrics; use supplied data or label placeholders honestly.',
    'Motion must clarify hierarchy or product behavior, not decorate every element.',
    'First viewport must explain what the product is, who it is for, and why it matters.',
    'Typography needs visible hierarchy: display, body, labels, and actions cannot all feel equal.',
    'Mobile layout must be intentionally composed, not merely collapsed.',
]


def norm(s):
    return re.sub(r'\s+', ' ', str(s or '').strip().lower())


def text_blob(post):
    return ' '.join(str(x or '') for x in [
        post.get('slug'), post.get('title'), post.get('sectionType'), post.get('sourceName'),
        post.get('author'), *(post.get('tags') or []), *(post.get('aiTools') or [])
    ])


def first_match(rules, blob, fallback):
    for label, rx in rules:
        if re.search(rx, blob, re.I):
            return label
    return fallback


def normalized_tags(post):
    raw = list(post.get('tags') or [])
    raw += [post.get('sectionType') or '']
    out = []
    for tag in raw:
        tag = TAG_ALIASES.get(tag, tag)
        tag = norm(tag)
        if not tag:
            continue
        replacements = {
            'hero section': 'hero',
            '3d website': '3d',
            'ai website': 'ai website',
            'landing page': 'landing page',
            'glass effect': 'glass',
            'glassmorphism': 'glass',
            'framer motion': 'motion',
        }
        tag = replacements.get(tag, tag)
        if tag not in out:
            out.append(tag)
    # Promote inferred tags.
    blob = norm(text_blob(post))
    inferred = []
    for tag, rx in [
        ('hero', r'\bhero\b'), ('dashboard', r'dashboard|command|analytics|ops|console'),
        ('component', r'button|card|dock|popover|loader|carousel'), ('motion', r'motion|animation|gsap|scroll'),
        ('3d', r'\b3d\b|space|cosmic|globe|particle'), ('saas', r'saas|software|pricing'),
        ('portfolio', r'portfolio|studio|agency'), ('open source', r'open source|github|magic ui|animata|cult ui|tailark'),
    ]:
        if re.search(rx, blob, re.I):
            inferred.append(tag)
    for tag in inferred:
        if tag not in out:
            out.append(tag)
    return out[:12]


def complexity(post, prompt):
    blob = norm(text_blob(post) + ' ' + prompt[:2000])
    score = 1
    if len(prompt) > 3500 or re.search(r'gsap|three|3d|shader|canvas|framer motion|scrolltrigger', blob):
        score += 1
    if len(prompt) > 8000 or re.search(r'dashboard|multi-section|full page|workflow|pricing|responsive', blob):
        score += 1
    return ['simple', 'medium', 'advanced'][min(score - 1, 2)]


def motion_level(post, prompt):
    blob = norm(text_blob(post) + ' ' + prompt[:1200])
    hits = len(re.findall(r'motion|animation|gsap|scroll|transition|video|3d|particle|hover|marquee|loader|reveal', blob))
    if hits >= 5:
        return 'heavy'
    if hits >= 2:
        return 'medium'
    if hits >= 1:
        return 'subtle'
    return 'none'


def quality_score(post, prompt):
    blob = norm(text_blob(post) + ' ' + prompt[:2000])
    score = 2.4
    if post.get('media') or post.get('thumbnail') or post.get('sourcePreview'):
        score += .45
    if post.get('sourceUrl'):
        score += .3
    if post.get('sourceName'):
        score += .2
    if 1200 <= len(prompt) <= 9000:
        score += .45
    elif len(prompt) > 9000:
        score += .25
    if re.search(r'landing page|homepage|hero|dashboard|portfolio|website|pricing|feature|workflow|agency|saas', blob):
        score += .35
    if re.search(r'gsap|3d|video|scroll|motion|animation|liquid|glass|cinematic|bento|editorial', blob):
        score += .25
    if re.search(r'button|dock|popover|loader|typewriter|scramble|ripple', blob):
        score -= .25
    if post.get('previewGenerated'):
        score -= .05
    return max(1, min(5, round(score, 1)))


def best_for(use_case):
    if use_case in {'component', 'motion system'}:
        return ['AI agent remix', 'visual inspiration']
    if use_case == 'dashboard':
        return ['AI agent', 'product designer']
    return ['AI agent', 'person']


def tier_from(score, use_case, canonical_cutoff):
    if score >= canonical_cutoff and use_case != 'component':
        return 'canon'
    if use_case in {'component', 'motion system'}:
        return 'pantry'
    if score < 3:
        return 'archive'
    return 'useful'


def make_item(post, prompt):
    blob = norm(text_blob(post) + ' ' + prompt[:1200])
    use_case = first_match(USE_CASE_RULES, blob, 'reference')
    site_type = first_match(SITE_RULES, blob, 'general website')
    aesthetic = first_match(AESTHETIC_RULES, blob, 'clean product')
    score = quality_score(post, prompt)
    return {
        'id': post['id'],
        'slug': post['slug'],
        'title': post['title'],
        'qualityScore': score,
        'useCase': use_case,
        'siteType': site_type,
        'aesthetic': aesthetic,
        'complexity': complexity(post, prompt),
        'motionLevel': motion_level(post, prompt),
        'bestFor': best_for(use_case),
        'normalizedTags': normalized_tags(post),
        'sourceName': post.get('sourceName') or post.get('author') or 'Local archive',
        'hasPreview': bool(post.get('media') or post.get('thumbnail') or post.get('sourcePreview')),
        'promptLength': len(prompt),
    }


def bundle_score(item, post, bundle):
    blob = norm(text_blob(post) + ' ' + ' '.join(item['normalizedTags']))
    if re.search(bundle['avoid'], blob, re.I):
        return -10
    score = item['qualityScore']
    score += 2.0 if re.search(bundle['query'], blob, re.I) else -3.0
    if item['useCase'] in {'full page', 'hero', 'dashboard'}:
        score += .7
    if item['useCase'] == 'component' and bundle['id'] != 'component-pantry':
        score -= 1.3
    if bundle['id'] == 'component-pantry' and item['useCase'] == 'component':
        score += 1.0
    if item['motionLevel'] in {'medium', 'heavy'} and 'motion' in bundle['id']:
        score += .8
    return score


def main():
    posts = json.loads(POSTS_PATH.read_text())
    prompts = json.loads(PROMPTS_PATH.read_text()) if PROMPTS_PATH.exists() else {}
    by_slug = {p['slug']: p for p in posts}
    items = [make_item(p, prompts.get(p['slug']) or prompts.get(p['id']) or '') for p in posts]
    ranked = sorted(items, key=lambda x: (x['qualityScore'], x['hasPreview'], x['promptLength']), reverse=True)
    # Keep a compact, strong default shelf: top 56 non-component prompts.
    canon_slugs = {x['slug'] for x in [i for i in ranked if i['useCase'] != 'component'][:56]}
    for item in items:
        if item['slug'] in canon_slugs:
            item['tier'] = 'canon'
        elif item['useCase'] in {'component', 'motion system'}:
            item['tier'] = 'pantry'
        else:
            item['tier'] = 'archive'
        item['canonical'] = item['tier'] == 'canon'
        item['archived'] = item['tier'] == 'archive'

    meta_by_slug = {item['slug']: item for item in items}
    bundles = []
    for bundle in BUNDLES:
        scored = []
        for item in items:
            score = bundle_score(item, by_slug[item['slug']], bundle)
            if score > 0:
                scored.append((score, item))
        scored.sort(key=lambda pair: (pair[0], pair[1]['qualityScore'], pair[1]['hasPreview']), reverse=True)
        chosen = [item['slug'] for _, item in scored[:12]]
        hero = chosen[0] if chosen else None
        bundles.append({
            'id': bundle['id'],
            'title': bundle['title'],
            'subtitle': bundle['subtitle'],
            'tone': bundle['tone'],
            'sections': bundle['sections'],
            'promptSlugs': chosen,
            'heroSlug': hero,
            'count': len(chosen),
            'briefTemplate': (
                f"Build a premium website using the {bundle['title']}. Tone: {bundle['tone']}. "
                f"Structure: {', '.join(bundle['sections'])}. Combine the selected Framewell references, "
                "but do not copy them literally. Produce a cohesive responsive site with real hierarchy, "
                "accessible contrast, restrained motion, and production-ready code."
            ),
        })

    tag_counts = Counter(tag for item in items for tag in item['normalizedTags'])
    tier_counts = Counter(item['tier'] for item in items)
    out = {
        'version': 1,
        'generatedBy': 'scripts/build_curation_json.py',
        'summary': {
            'total': len(items),
            'canon': tier_counts.get('canon', 0),
            'pantry': tier_counts.get('pantry', 0),
            'archive': tier_counts.get('archive', 0),
            'bundles': len(bundles),
            'topTags': tag_counts.most_common(24),
        },
        'antiSlopRules': ANTI_SLOP_RULES,
        'items': meta_by_slug,
        'bundles': bundles,
    }
    OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    print(f"wrote {len(items)} curation records and {len(bundles)} bundles to data/curation.json")


if __name__ == '__main__':
    main()
