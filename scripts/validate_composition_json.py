#!/usr/bin/env python3
"""Validate Framewell composition metadata.

This is intentionally strict: remix quality depends on the app having a real
composition contract, not only raw prompts and loose bundle metadata.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSITION_PATH = ROOT / 'data' / 'composition.json'
CURATION_PATH = ROOT / 'data' / 'curation.json'
POSTS_PATH = ROOT / 'data' / 'posts.json'

REQUIRED_VOCAB_CATEGORIES = {
    'motion',
    'layout',
    'aesthetic',
    'quality',
    'content',
}
REQUIRED_ROLES = {
    'dominant-structure',
    'hero-concept',
    'visual-skin',
    'motion-layer',
    'section-pattern',
    'component-accent',
    'anti-pattern-guardrail',
}
REQUIRED_RECIPES = {
    'ai-saas-editorial-motion',
    'devtool-command-center',
    'luxury-motion-commerce',
    'portfolio-studio-casework',
    'dashboard-trust-product',
    'conversion-page-proof-stack',
    'mobile-app-launch-flow',
    'docs-learning-hub',
    'ai-workflow-dashboard',
    'brutalist-infra-launch',
    'playful-consumer-onboarding',
    'gallery-archive-experience',
    'pricing-comparison-page',
    'changelog-release-notes',
    'investor-narrative-deck-page',
    'marketplace-community-launch',
    'location-map-experience',
    'cinematic-launch-hero',
    'settings-admin-console',
    'case-study-proof-page',
}


def fail(message):
    print(f'composition validation failed: {message}', file=sys.stderr)
    raise SystemExit(1)


def load(path):
    if not path.exists():
        fail(f'missing {path.relative_to(ROOT)}')
    return json.loads(path.read_text())


def main():
    composition = load(COMPOSITION_PATH)
    curation = load(CURATION_PATH)
    posts = load(POSTS_PATH)
    post_slugs = {post['slug'] for post in posts}

    if composition.get('version') != 1:
        fail('version must be 1')

    vocab = composition.get('vocabulary') or {}
    missing_vocab = REQUIRED_VOCAB_CATEGORIES - set(vocab)
    if missing_vocab:
        fail(f'missing vocabulary categories: {sorted(missing_vocab)}')
    for category, terms in vocab.items():
        if len(terms) < 6:
            fail(f'vocabulary category {category} needs at least 6 terms')
        for term in terms:
            if not all(term.get(k) for k in ('id', 'label', 'definition', 'promptInstruction')):
                fail(f'vocabulary term in {category} is missing required fields: {term}')

    roles = composition.get('roles') or []
    role_ids = {role.get('id') for role in roles}
    missing_roles = REQUIRED_ROLES - role_ids
    if missing_roles:
        fail(f'missing composition roles: {sorted(missing_roles)}')

    items = composition.get('items') or {}
    if set(items) != post_slugs:
        fail(f'composition items must cover every post exactly ({len(items)} vs {len(post_slugs)})')
    multi_role_count = 0
    for slug, item in items.items():
        if item.get('slug') != slug:
            fail(f'item {slug} has mismatched slug')
        item_roles = item.get('roles') or []
        if not item_roles:
            fail(f'item {slug} has no composition roles')
        if not set(item_roles).issubset(role_ids):
            fail(f'item {slug} has unknown roles {sorted(set(item_roles)-role_ids)}')
        if len(item_roles) >= 2:
            multi_role_count += 1
        if not item.get('vocabularyTerms'):
            fail(f'item {slug} has no vocabulary terms')
        if not item.get('mixUse') or not item.get('mixAvoid'):
            fail(f'item {slug} needs mixUse and mixAvoid guidance')
    if multi_role_count < 50:
        fail('at least 50 prompts should have multiple composition roles')

    recipes = composition.get('recipes') or []
    recipe_ids = {recipe.get('id') for recipe in recipes}
    missing_recipes = REQUIRED_RECIPES - recipe_ids
    if missing_recipes:
        fail(f'missing recipes: {sorted(missing_recipes)}')
    for recipe in recipes:
        if not recipe.get('selectionRules'):
            fail(f"recipe {recipe.get('id')} needs selectionRules")
        required_slots = {'structure', 'style', 'motion', 'sections'}
        if required_slots - set(recipe['selectionRules']):
            fail(f"recipe {recipe.get('id')} missing slot rules")
        if len(recipe.get('inputs') or []) < 4:
            fail(f"recipe {recipe.get('id')} needs pre-flight inputs")
        input_names = {item.get('name') for item in recipe.get('inputs') or []}
        if {'surface', 'audience', 'product_promise'} - input_names:
            fail(f"recipe {recipe.get('id')} missing required input names")
        if len(recipe.get('designDirections') or []) < 2:
            fail(f"recipe {recipe.get('id')} needs at least 2 design directions")
        for direction in recipe.get('designDirections') or []:
            if not all(direction.get(k) for k in ('id', 'label', 'tokens', 'useWhen', 'avoid')):
                fail(f"recipe {recipe.get('id')} has incomplete design direction {direction}")
        if len(recipe.get('pipeline') or []) < 5:
            fail(f"recipe {recipe.get('id')} needs a generation pipeline")
        pipeline_ids = {stage.get('id') for stage in recipe.get('pipeline') or []}
        if {'discover', 'assign-roles', 'generate', 'critique', 'handoff'} - pipeline_ids:
            fail(f"recipe {recipe.get('id')} missing pipeline stages")
        if len(recipe.get('acceptanceCriteria') or []) < 5:
            fail(f"recipe {recipe.get('id')} needs acceptance criteria")
        if len(recipe.get('promptSlugs') or []) < 4:
            fail(f"recipe {recipe.get('id')} needs at least 4 selected prompts")
        unknown = set(recipe.get('promptSlugs') or []) - post_slugs
        if unknown:
            fail(f"recipe {recipe.get('id')} references unknown prompts {sorted(unknown)}")
        if not recipe.get('briefTemplate') or 'Mix grammar' not in recipe['briefTemplate']:
            fail(f"recipe {recipe.get('id')} needs a Mix grammar briefTemplate")

    compatibility = composition.get('compatibility') or {}
    if len(compatibility.get('goodPairs') or []) < 8:
        fail('needs at least 8 good compatibility pairs')
    if len(compatibility.get('badPairs') or []) < 8:
        fail('needs at least 8 bad compatibility pairs')

    expected_bundles = len(curation.get('bundles') or [])
    if composition.get('summary', {}).get('curationBundles') != expected_bundles:
        fail('summary.curationBundles must match curation bundle count')

    print('composition validation passed:', {
        'terms': sum(len(v) for v in vocab.values()),
        'roles': len(roles),
        'items': len(items),
        'recipes': len(recipes),
        'multiRoleItems': multi_role_count,
    })


if __name__ == '__main__':
    main()
