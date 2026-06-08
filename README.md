# Framewell

Framewell is a preview-first motion prompt library for website, dashboard, animation, and component ideas. It is designed to be clean enough to browse quickly, but visual enough that each prompt has an obvious shape before you open the text.

This repository is a static publishing-ready app: HTML, CSS, vanilla JavaScript, local JSON data, local media assets, and prompt text files.

## What is inside

- 195 prompt cards
- 195 local prompt texts
- 195 preview assets
- 56 canonical surfaced prompts, 59 component-pantry prompts, and 80 archive prompts
- 8 website kits that bundle prompts into buildable AI/human briefs
- 20 composition recipes, 7 prompt roles, 42 vocabulary primitives, and OD-inspired recipe contracts for structured remixing
- 5 concept-sketch SVG previews for prompts that had no usable source media
- Provenance notes for third-party/public/open prompt sources
- A minimal Framewell brand system: mark, favicon, app copy, metadata, and README

## Run locally

```bash
cd /Users/ozansozuoz/programming-files/framewell
python3 -m http.server 4173
```

Open:

```text
http://localhost:4173
```

Or use the package script:

```bash
npm run start
```

## Project structure

```text
index.html                  Static app shell
styles.css                  Visual system and responsive layout
app.js                      Filtering, modal, preview rendering, copy actions
data/posts.json             Card metadata used by the UI
data/prompts.json           Generated prompt lookup
data/curation.json          Generated taxonomy, shelves, bundles, and anti-slop rules
data/composition.json       Generated vocabulary, roles, compatibility rules, and remix recipes
prompts/*.txt               Source prompt text files
assets/previews/            Local preview videos/images
assets/previews/generated/  Concept-sketch previews for prompt-only entries
assets/thumbnails/          Local thumbnail images
assets/ui/                  Framewell logo, mark, favicon
THIRD_PARTY_PROMPTS.md      Source and license/provenance notes
```

## Add or update prompts

The composition layer borrows the useful part of Open Design's workflow contract without adding a daemon: every recipe now carries pre-flight inputs, design-direction options, generation pipeline stages, and acceptance criteria. The composer embeds those fields into the copied brief so agents must lock the brief, assign prompt roles, generate, critique, and explain source influence instead of loosely sampling one reference.

Add prompt text files to `prompts/`, then rebuild the generated JSON:

```bash
python3 scripts/build_prompts_json.py
python3 scripts/build_curation_json.py
python3 scripts/build_composition_json.py
python3 scripts/validate_composition_json.py
```

If adding a new card, update `data/posts.json` with a unique `id` and `slug`. Prefer real preview media. If no source preview exists, create a clean concept-sketch SVG in `assets/previews/generated/` and set `thumbnail` to that path.

## Preview policy

Framewell should not show blank placeholder cards. Every card needs one of:

1. source video/image preview
2. source thumbnail
3. clearly designed local concept sketch

Concept sketches are not screenshots. They are visual summaries of the prompt so the archive remains browsable.

## Publishing checklist

Before publishing:

```bash
node --check app.js
python3 scripts/build_prompts_json.py
python3 scripts/build_curation_json.py
python3 scripts/build_composition_json.py
python3 scripts/validate_composition_json.py
python3 - <<'PY'
import json
from pathlib import Path
root = Path('.')
posts = json.loads((root / 'data/posts.json').read_text())
prompts = json.loads((root / 'data/prompts.json').read_text())
curation = json.loads((root / 'data/curation.json').read_text())
composition = json.loads((root / 'data/composition.json').read_text())
ids = [p['id'] for p in posts]
slugs = [p['slug'] for p in posts]
missing_assets = []
for p in posts:
    for key in ['media', 'thumbnail']:
        value = p.get(key)
        if value and not value.startswith(('http://', 'https://')) and not (root / value).exists():
            missing_assets.append((p['slug'], key, value))
print({
    'posts': len(posts),
    'prompts': len(prompts),
    'canon': curation['summary']['canon'],
    'pantry': curation['summary']['pantry'],
    'archive': curation['summary']['archive'],
    'bundles': curation['summary']['bundles'],
    'composition_recipes': composition['summary']['recipes'],
    'composition_roles': composition['summary']['roles'],
    'vocabulary_terms': composition['summary']['vocabularyTerms'],
    'with_preview': sum(1 for p in posts if p.get('media') or p.get('thumbnail')),
    'duplicate_ids': len(ids) - len(set(ids)),
    'duplicate_slugs': len(slugs) - len(set(slugs)),
    'missing_assets': len(missing_assets),
})
PY
```

Expected current result:

```text
posts: 195
prompts: 195
canon: 56
pantry: 59
archive: 80
bundles: 8
composition_recipes: 20
composition_roles: 7
vocabulary_terms: 42
with_preview: 195
duplicate_ids: 0
duplicate_slugs: 0
missing_assets: 0
```

## Provenance

See `THIRD_PARTY_PROMPTS.md`. Framewell keeps source links near each prompt and avoids importing gated/premium private prompt text.

<!-- live-demo:start -->
## Live Demo

- Production URL: https://framewell-jri6vvisy-ozan-sozuozs-projects.vercel.app"
- Source: https://github.com/ozansozuozgit/framewell

<!-- live-demo:end -->
