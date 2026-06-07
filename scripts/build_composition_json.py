#!/usr/bin/env python3
"""Build Framewell composition metadata.

Curation answers "what is worth surfacing?" Composition answers "how should
multiple prompts be combined?" The generated JSON gives the UI and AI agents a
controlled vocabulary, prompt roles, compatibility rules, and ready remix
recipes so mix-and-match does not collapse into picking one prompt.
"""
import json
import pathlib
import re
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]
POSTS_PATH = ROOT / 'data' / 'posts.json'
PROMPTS_PATH = ROOT / 'data' / 'prompts.json'
CURATION_PATH = ROOT / 'data' / 'curation.json'
OUT_PATH = ROOT / 'data' / 'composition.json'

VOCABULARY = {
    'motion': [
        ('stagger', 'Animate related items one after another with small delays.', 'Use a staggered entrance for grouped cards, nav links, or proof items.'),
        ('scroll-reveal', 'Reveal elements as they enter the viewport.', 'Use scroll reveal only for section handoff and hierarchy, not every object.'),
        ('layout-animation', 'Animate position/size changes so layout changes do not snap.', 'Use layout animation when cards expand, filters change, or panels rearrange.'),
        ('direction-aware-transition', 'Move content according to navigation direction.', 'Make forward/back transitions move in opposite directions to preserve orientation.'),
        ('shared-element-transition', 'Carry a visual element between states.', 'Connect a thumbnail/card to its detail view using a shared element transition.'),
        ('crossfade', 'Fade between two states in the same spatial location.', 'Crossfade alternate media/states when motion should feel quiet and continuous.'),
        ('origin-aware-pop', 'Scale or reveal from the trigger point.', 'Open menus, popovers, and cards from their trigger origin instead of center screen.'),
        ('parallax-depth', 'Move foreground/background at different scroll rates.', 'Use shallow parallax for atmosphere only when it supports comprehension.'),
        ('press-feedback', 'Physical tap/click feedback.', 'Add subtle scale/opacity feedback to primary buttons and draggable cards.'),
        ('kinetic-type', 'Typography moves as a meaningful visual object.', 'Use kinetic typography for the headline or section labels, not body copy.'),
    ],
    'layout': [
        ('split-hero', 'Hero with copy and product/visual proof side by side.', 'Use split hero when the product needs immediate explanation and visual proof.'),
        ('dashboard-proof', 'Hero or section anchored by realistic app/dashboard surfaces.', 'Use dashboard proof with supplied or honest placeholder data, never fake metrics.'),
        ('editorial-stack', 'Magazine-like vertical rhythm with strong type and image pacing.', 'Use editorial stack for calm premium pages and portfolio/studio narratives.'),
        ('asymmetric-bento', 'Uneven grid of feature cards with clear hierarchy.', 'Use asymmetric bento for product features when one or two ideas need dominance.'),
        ('proof-band', 'Compact row of customer/logos/metrics/trust indicators.', 'Use proof band directly after the hero to ground claims.'),
        ('workflow-timeline', 'Ordered steps showing how the product/process works.', 'Use workflow timeline for AI/productivity products where sequence matters.'),
        ('sticky-scrollytelling', 'One sticky visual paired with changing text.', 'Use sticky scrollytelling for complex products; keep it short and purposeful.'),
        ('comparison-frame', 'Before/after or alternative comparison layout.', 'Use comparison frame when the value is clearer by contrast.'),
        ('gallery-rhythm', 'Repeating image/card rhythm with controlled variation.', 'Use gallery rhythm for portfolios, commerce, and visual archives.'),
        ('command-console', 'Dense command/product surface with filters, logs, or terminal affordances.', 'Use command console for devtools, dashboards, and operational products.'),
    ],
    'aesthetic': [
        ('warm-editorial', 'Paper, ink, precise type, quiet premium surfaces.', 'Apply warm editorial tokens when the page should feel calm, designed, and trustworthy.'),
        ('technical-minimal', 'Sparse, legible, tool-like, low ornament.', 'Apply technical minimalism for devtools and B2B apps.'),
        ('cinematic-3d', 'Depth, staged lighting, hero object, spatial drama.', 'Use cinematic 3D as one focal moment, not a whole-page decoration flood.'),
        ('luxury-monochrome', 'High contrast, restrained color, gallery-like pacing.', 'Use luxury monochrome for premium commerce, studio, and editorial launches.'),
        ('playful-tactile', 'Soft shapes, toy-like feedback, approachable interactions.', 'Use playful tactile details for consumer or onboarding flows.'),
        ('brutalist-utility', 'Raw mechanical typography, visible structure, utilitarian edges.', 'Use brutalist utility when clarity and force matter more than polish.'),
        ('glass-luminous', 'Translucent surfaces, blur, glow, layered light.', 'Use glass/luminous styling sparingly with readable contrast.'),
        ('dense-dashboard', 'Information-rich, compact, controlled hierarchy.', 'Use dense dashboard styling when many states must remain visible.'),
    ],
    'quality': [
        ('hierarchy', 'Clear first, second, and third attention targets.', 'Make the first viewport explain product, audience, and value before decorative detail.'),
        ('spatial-consistency', 'Related objects keep consistent spacing, alignment, and motion paths.', 'Preserve spacing and movement logic across sections.'),
        ('affordance', 'Interactive elements look and behave like they can be used.', 'Buttons, filters, and cards need clear hover/focus/press states.'),
        ('contrast', 'Text and controls remain readable against their surfaces.', 'Keep accessible contrast; do not sacrifice legibility for glow or glass.'),
        ('rhythm', 'Repeated spacing/type/media patterns create readable flow.', 'Use repeated section rhythm, then break it intentionally for emphasis.'),
        ('content-density', 'Amount of information matches the product and viewport.', 'Avoid sparse dashboard cards or overstuffed hero copy.'),
        ('information-scent', 'Users can predict what clicking/scanning will reveal.', 'Name sections and CTAs specifically, not with generic marketing filler.'),
        ('mobile-composition', 'Mobile is intentionally redesigned, not accidentally collapsed.', 'Define mobile order, sticky areas, and motion reductions explicitly.'),
    ],
    'content': [
        ('specific-promise', 'Concrete value proposition instead of generic adjectives.', 'Write the hero around a specific product promise and user outcome.'),
        ('credible-proof', 'Evidence that supports claims.', 'Use real screenshots, workflow examples, customer logos, or honest placeholders.'),
        ('section-contract', 'Each section has a distinct job.', 'Assign every section a purpose: explain, prove, compare, convert, or support.'),
        ('anti-filler-copy', 'No vague AI-powered/next-gen wording unless expanded.', 'Replace broad slogans with concrete product behavior and user benefit.'),
        ('implementation-constraints', 'Output format, framework, accessibility, and responsiveness rules.', 'State exact deliverable constraints so agents produce usable code.'),
        ('source-attribution', 'References remain named and traceable.', 'Mention Framewell references by title and role in the generated brief.'),
    ],
}

ROLES = [
    ('dominant-structure', 'Defines the full page skeleton or primary section order.', 'Use as the main blueprint; other prompts should support it.'),
    ('hero-concept', 'Defines the above-the-fold idea, headline/visual relationship, or hero motion.', 'Use for first impression only unless it is also a full-page structure.'),
    ('visual-skin', 'Defines color, typography, texture, atmosphere, or brand feel.', 'Borrow its surface language without copying unrelated layout.'),
    ('motion-layer', 'Defines animation behavior, timing, transitions, or scroll/hover system.', 'Borrow motion vocabulary and orchestration, not all visuals.'),
    ('section-pattern', 'Defines a reusable page section such as features, proof, pricing, FAQ, workflow.', 'Slot into the dominant structure where that section belongs.'),
    ('component-accent', 'Defines a small component or microinteraction.', 'Use as accent detail only; never let it dominate a page.'),
    ('anti-pattern-guardrail', 'Useful mainly as something to constrain, avoid, or demote.', 'Use as a warning when it conflicts with the selected outcome or vibe.'),
]

COMPATIBILITY = {
    'goodPairs': [
        ['warm-editorial', 'editorial-stack', 'Quiet premium pages with readable rhythm.'],
        ['technical-minimal', 'command-console', 'Devtool pages need dense clarity before decoration.'],
        ['cinematic-3d', 'split-hero', 'One hero object can anchor a product promise.'],
        ['dashboard-proof', 'proof-band', 'Metrics and proof should reinforce each other.'],
        ['workflow-timeline', 'scroll-reveal', 'Sequential content benefits from staged reveal.'],
        ['asymmetric-bento', 'layout-animation', 'Bento grids feel better when rearrangement is animated.'],
        ['luxury-monochrome', 'gallery-rhythm', 'Premium commerce/studio pages rely on pacing and restraint.'],
        ['playful-tactile', 'press-feedback', 'Consumer flows benefit from physical interaction feedback.'],
        ['shared-element-transition', 'gallery-rhythm', 'Cards expanding into detail views keep spatial continuity.'],
        ['specific-promise', 'credible-proof', 'A claim should be followed by believable evidence.'],
    ],
    'badPairs': [
        ['dense-dashboard', 'cinematic-3d', 'Too much spectacle can make operational UI feel fake.'],
        ['glass-luminous', 'contrast', 'Glass effects often damage readability unless tightly constrained.'],
        ['brutalist-utility', 'luxury-monochrome', 'Raw utility and quiet luxury need a deliberate bridge, not a direct mashup.'],
        ['component-accent', 'dominant-structure', 'Small components should not define a whole website.'],
        ['kinetic-type', 'content-density', 'Moving type conflicts with dense reading tasks.'],
        ['parallax-depth', 'mobile-composition', 'Parallax often breaks mobile unless reduced or disabled.'],
        ['cinematic-3d', 'credible-proof', 'Abstract 3D cannot replace concrete product proof.'],
        ['glass-luminous', 'dense-dashboard', 'Blurred translucent layers make dashboards hard to scan.'],
        ['stagger', 'content-density', 'Long stagger sequences slow down dense interfaces.'],
        ['anti-filler-copy', 'cinematic-3d', 'Spectacle can hide weak copy; force specificity first.'],
    ],
}

DESIGN_DIRECTIONS = {
    'editorial-monocle': {
        'label': 'Editorial Monocle',
        'tokens': 'paper/ink neutrals, serif display, hairline rules, one restrained accent',
        'useWhen': 'source-first, premium, editorial, learning, studio, or gallery experiences',
        'avoid': 'do not use for dense dashboards unless paired with compact technical surfaces',
    },
    'modern-minimal': {
        'label': 'Modern Minimal',
        'tokens': 'software-native neutrals, crisp borders, system sans, visible product accent',
        'useWhen': 'SaaS, conversion, docs, and general product pages that need trust',
        'avoid': 'do not let everything become greyscale or anonymous',
    },
    'warm-soft': {
        'label': 'Warm Soft',
        'tokens': 'soft surfaces, rounded controls, approachable color, tactile feedback',
        'useWhen': 'consumer, onboarding, mobile, and habit-forming products',
        'avoid': 'avoid childish visuals unless the product explicitly needs them',
    },
    'tech-utility': {
        'label': 'Tech Utility',
        'tokens': 'compact surfaces, mono metadata, command-console panels, tabular numbers',
        'useWhen': 'devtools, infra, dashboards, docs, and operational interfaces',
        'avoid': 'avoid decorative terminal cosplay that does not explain the product',
    },
    'brutalist-experimental': {
        'label': 'Brutalist Experimental',
        'tokens': 'raw grid, high contrast, mechanical typography, deliberate roughness',
        'useWhen': 'infra/security launches, campaigns, and sharp positioning moments',
        'avoid': 'do not sacrifice readability or trust for attitude',
    },
    'cinematic-spatial': {
        'label': 'Cinematic Spatial',
        'tokens': 'deep stage, dramatic light, one hero object, controlled depth and shadow',
        'useWhen': 'hero campaigns, launches, 3D/video-led products, and immersive product stories',
        'avoid': 'do not let spectacle replace proof, copy, or navigation clarity',
    },
    'finance-trust': {
        'label': 'Finance Trust',
        'tokens': 'calm blue/green neutrals, tabular numbers, restrained charts, formal spacing',
        'useWhen': 'fintech, pricing, investor, analytics, and high-trust conversion surfaces',
        'avoid': 'avoid casino-like gradients, fake revenue, or overexcited financial claims',
    },
    'community-energy': {
        'label': 'Community Energy',
        'tokens': 'expressive accent color, avatar clusters, event rhythm, approachable cards',
        'useWhen': 'marketplaces, communities, launches, social proof, and creator/product ecosystems',
        'avoid': 'avoid noisy social clutter that hides the core action',
    },
}

DEFAULT_PIPELINE = [
    {'id': 'discover', 'label': 'Lock brief inputs', 'instruction': 'State audience, surface, product promise, constraints, and chosen design direction before selecting references.'},
    {'id': 'assign-roles', 'label': 'Assign reference roles', 'instruction': 'Name the dominant structure, visual skin, motion layer, and accent references before writing code.'},
    {'id': 'generate', 'label': 'Generate cohesive artifact', 'instruction': 'Implement one cohesive page or component system using the selected recipe slot rules.'},
    {'id': 'critique', 'label': 'Self-critique against contract', 'instruction': 'Check structure/style/motion/accent usage, mobile composition, accessibility, and content specificity.'},
    {'id': 'handoff', 'label': 'Explain source influence', 'instruction': 'Return the artifact plus a short mapping of which references influenced each section.'},
]

DEFAULT_ACCEPTANCE = [
    'The output names which reference supplied structure, visual skin, motion layer, section patterns, and component accents.',
    'The first viewport explains what the product is, who it is for, and why it matters.',
    'Every section has a distinct job: explain, prove, compare, convert, or support.',
    'Motion is implemented intentionally and reduced for dense/mobile contexts.',
    'No fake metrics, generic AI copy, unreadable glass, or collage-like mixing.',
]

RECIPE_INPUTS = [
    {'name': 'surface', 'label': 'Surface', 'type': 'select', 'required': True, 'options': ['landing page', 'dashboard page', 'mobile app page', 'docs page', 'gallery/archive', 'component section']},
    {'name': 'audience', 'label': 'Audience', 'type': 'string', 'required': True},
    {'name': 'product_promise', 'label': 'Product promise', 'type': 'string', 'required': True},
    {'name': 'brand_constraints', 'label': 'Brand constraints', 'type': 'string', 'required': False},
]

DIRECTION_HINTS = {
    'ai-saas-editorial-motion': ['modern-minimal', 'editorial-monocle', 'tech-utility'],
    'devtool-command-center': ['tech-utility', 'modern-minimal', 'brutalist-experimental'],
    'luxury-motion-commerce': ['editorial-monocle', 'modern-minimal'],
    'portfolio-studio-casework': ['editorial-monocle', 'brutalist-experimental', 'modern-minimal'],
    'dashboard-trust-product': ['tech-utility', 'modern-minimal'],
    'conversion-page-proof-stack': ['modern-minimal', 'editorial-monocle', 'warm-soft'],
    'mobile-app-launch-flow': ['warm-soft', 'modern-minimal'],
    'docs-learning-hub': ['editorial-monocle', 'modern-minimal', 'tech-utility'],
    'ai-workflow-dashboard': ['tech-utility', 'modern-minimal', 'editorial-monocle'],
    'brutalist-infra-launch': ['brutalist-experimental', 'tech-utility'],
    'playful-consumer-onboarding': ['warm-soft', 'modern-minimal'],
    'gallery-archive-experience': ['editorial-monocle', 'modern-minimal'],
    'pricing-comparison-page': ['finance-trust', 'modern-minimal', 'tech-utility'],
    'changelog-release-notes': ['tech-utility', 'modern-minimal', 'editorial-monocle'],
    'investor-narrative-deck-page': ['finance-trust', 'editorial-monocle', 'modern-minimal'],
    'marketplace-community-launch': ['community-energy', 'warm-soft', 'modern-minimal'],
    'location-map-experience': ['community-energy', 'editorial-monocle', 'modern-minimal'],
    'cinematic-launch-hero': ['cinematic-spatial', 'modern-minimal', 'editorial-monocle'],
    'settings-admin-console': ['tech-utility', 'modern-minimal'],
    'case-study-proof-page': ['editorial-monocle', 'modern-minimal', 'finance-trust'],
}

RECIPES = [
    {
        'id': 'ai-saas-editorial-motion',
        'title': 'AI SaaS: editorial structure + motion proof',
        'outcome': 'premium AI SaaS landing page',
        'vibe': 'warm editorial with restrained motion',
        'bundleHints': ['ai-product-launch-kit', 'saas-landing-kit', 'motion-first-hero-kit'],
        'query': r'\bai\b|saas|workflow|software|landing page|hero|waitlist|automation|bento|pricing|feature',
        'avoid': r'loader|popover|dock|button|fashion|portfolio cosmic',
        'selectionRules': {
            'structure': 'Choose one SaaS/AI full-page or landing reference as the dominant structure.',
            'style': 'Borrow warm/editorial or clean product aesthetics; demote dark futuristic effects.',
            'motion': 'Use stagger + scroll reveal + one layout animation moment for product proof.',
            'sections': 'Add proof band, feature bento, workflow, pricing/FAQ, and final CTA.',
        },
    },
    {
        'id': 'devtool-command-center',
        'title': 'Devtool: command-center clarity',
        'outcome': 'developer tool or infrastructure product page',
        'vibe': 'technical minimal / command console',
        'bundleHints': ['devtool-open-source-kit', 'dashboard-product-kit', 'component-pantry'],
        'query': r'devtool|docs|open source|terminal|code|api|dashboard|command|console|github|security',
        'avoid': r'fashion|tea|luxury|cosmic portfolio|particle',
        'selectionRules': {
            'structure': 'Use docs/devtool references for page order and trust framing.',
            'style': 'Use technical minimalism with compact command-console surfaces.',
            'motion': 'Use origin-aware popovers, layout animation for filters, and subtle press feedback.',
            'sections': 'Include terminal/API demo, feature grid, docs preview, community proof, and CTA.',
        },
    },
    {
        'id': 'luxury-motion-commerce',
        'title': 'Luxury/editorial: product atmosphere + restrained motion',
        'outcome': 'premium commerce, fashion, or editorial product page',
        'vibe': 'luxury monochrome / warm editorial',
        'bundleHints': ['luxury-editorial-kit', 'motion-first-hero-kit', 'component-pantry'],
        'query': r'luxury|fashion|tea|commerce|automotive|editorial|gallery|museum|hero|motion|scroll',
        'avoid': r'dashboard|terminal|ops|security|pricing comparison',
        'selectionRules': {
            'structure': 'Use editorial/gallery references for page rhythm and content pacing.',
            'style': 'Borrow luxury monochrome or warm editorial visual skin.',
            'motion': 'Use crossfade, shallow parallax, and slow scroll reveal; avoid hyperactive animation.',
            'sections': 'Include editorial hero, product story, gallery rhythm, provenance, and soft CTA.',
        },
    },
    {
        'id': 'portfolio-studio-casework',
        'title': 'Studio portfolio: casework narrative',
        'outcome': 'portfolio or creative studio website',
        'vibe': 'editorial studio with memorable but useful motion',
        'bundleHints': ['portfolio-studio-kit', 'luxury-editorial-kit', 'motion-first-hero-kit'],
        'query': r'portfolio|studio|agency|creative|case study|designer|editorial|gallery|motion|hero',
        'avoid': r'pricing|dashboard|security|finance|inventory',
        'selectionRules': {
            'structure': 'Use portfolio/studio references for selected work and case-study flow.',
            'style': 'Borrow editorial typography, gallery pacing, and confident negative space.',
            'motion': 'Use shared-element transitions between work cards and detail states.',
            'sections': 'Include editorial hero, selected work, case-study cards, services, about, and contact.',
        },
    },
    {
        'id': 'dashboard-trust-product',
        'title': 'Dashboard product: proof-first interface story',
        'outcome': 'dashboard-heavy product landing page',
        'vibe': 'dense but calm product interface',
        'bundleHints': ['dashboard-product-kit', 'saas-landing-kit', 'devtool-open-source-kit'],
        'query': r'dashboard|analytics|command|ops|console|finance|revenue|inventory|observability|saas',
        'avoid': r'fashion|tea|portfolio|cosmic|loader',
        'selectionRules': {
            'structure': 'Use dashboard references for app surfaces and workflow states.',
            'style': 'Use dense dashboard hierarchy with clear surfaces and honest data labels.',
            'motion': 'Use layout animation for state changes, not decorative scroll theatrics.',
            'sections': 'Include dashboard hero, live metrics preview, workflow panels, alerts, integrations, and trust.',
        },
    },
    {
        'id': 'conversion-page-proof-stack',
        'title': 'Conversion page: proof stack + clear CTA',
        'outcome': 'high-conversion landing page for a product, waitlist, or campaign',
        'vibe': 'clean minimal SaaS with strong evidence density',
        'bundleHints': ['saas-landing-kit', 'ai-product-launch-kit', 'component-pantry'],
        'query': r'landing page|waitlist|pricing|testimonial|proof|stats|logo cloud|cta|signup|feature|saas|marketing|conversion',
        'avoid': r'portfolio|fashion|cosmic|loader|heavy particle',
        'selectionRules': {
            'structure': 'Use a conversion-oriented landing reference as the dominant structure.',
            'style': 'Borrow clean SaaS or warm editorial styling; keep claims legible and trust-first.',
            'motion': 'Use short staggered proof/feature reveals and press feedback on CTAs only.',
            'sections': 'Include promise hero, proof band, benefit stack, comparison/problem-solution, testimonials, FAQ, and final CTA.',
        },
    },
    {
        'id': 'mobile-app-launch-flow',
        'title': 'Mobile app: launch flow + tactile interactions',
        'outcome': 'mobile app launch page or onboarding-focused product page',
        'vibe': 'playful tactile consumer product with clean conversion flow',
        'bundleHints': ['ai-product-launch-kit', 'component-pantry', 'motion-first-hero-kit'],
        'query': r'mobile|app|onboarding|signup|login|form|cards|swipe|tap|ripple|playful|consumer|waitlist|hero',
        'avoid': r'dashboard|terminal|docs|brutalist|heavy 3d|finance',
        'selectionRules': {
            'structure': 'Use launch/onboarding references for a simple linear story.',
            'style': 'Borrow playful tactile surfaces while keeping product copy adult and specific.',
            'motion': 'Use press feedback, swipe/direction-aware transitions, and origin-aware popovers.',
            'sections': 'Include app promise hero, screen sequence, onboarding steps, social proof, install/waitlist CTA, and privacy/trust note.',
        },
    },
    {
        'id': 'docs-learning-hub',
        'title': 'Docs / learning hub: source-first knowledge page',
        'outcome': 'documentation, learning library, or source-first knowledge hub',
        'vibe': 'calm editorial / technical minimal',
        'bundleHints': ['devtool-open-source-kit', 'portfolio-studio-kit', 'saas-landing-kit'],
        'query': r'docs|documentation|learning|academy|course|notes|blog|field notes|source|library|guide|api|open source',
        'avoid': r'fashion|commerce|heavy particle|gaming|luxury product',
        'selectionRules': {
            'structure': 'Use docs/devtool or editorial references for navigation and reading hierarchy.',
            'style': 'Borrow calm editorial typography with technical minimal UI controls.',
            'motion': 'Use subtle scroll reveal and layout animation for navigation/filter changes only.',
            'sections': 'Include overview hero, topic map, featured sources, reading paths, search/filter, and contribution/source ledger.',
        },
    },
    {
        'id': 'ai-workflow-dashboard',
        'title': 'AI workflow: dashboard + agent process story',
        'outcome': 'AI workflow or agent product with dashboard proof',
        'vibe': 'credible AI product with dense but understandable workflow surfaces',
        'bundleHints': ['ai-product-launch-kit', 'dashboard-product-kit', 'devtool-open-source-kit'],
        'query': r'\bai\b|agent|automation|workflow|dashboard|command|notebook|chat|mail|calendar|ops|process|model',
        'avoid': r'fashion|tea|portfolio|luxury commerce|random particles|loader',
        'selectionRules': {
            'structure': 'Use AI/product references for promise and dashboard references for proof.',
            'style': 'Borrow dense dashboard clarity, not generic purple AI spectacle.',
            'motion': 'Use workflow-timeline reveals and layout animation to explain state changes.',
            'sections': 'Include AI promise hero, agent workflow, live dashboard proof, trust/security, use cases, and CTA.',
        },
    },
    {
        'id': 'brutalist-infra-launch',
        'title': 'Infra launch: brutalist utility + trust proof',
        'outcome': 'infrastructure, security, or systems product launch page',
        'vibe': 'brutalist utility with technical trust and restrained motion',
        'bundleHints': ['devtool-open-source-kit', 'dashboard-product-kit', 'saas-landing-kit'],
        'query': r'infra|infrastructure|security|ops|observability|terminal|api|code|command|dashboard|devtool|enterprise|trust',
        'avoid': r'fashion|tea|playful|consumer|luxury|cosmic portfolio',
        'selectionRules': {
            'structure': 'Use devtool/infra references for architecture, proof, and docs flow.',
            'style': 'Borrow brutalist utility only for structure and force; keep typography readable.',
            'motion': 'Use minimal press feedback and command-console state transitions; avoid decorative animation.',
            'sections': 'Include technical hero, architecture/proof panel, reliability/security claims, docs/API preview, use cases, and CTA.',
        },
    },
    {
        'id': 'playful-consumer-onboarding',
        'title': 'Consumer onboarding: playful but clear',
        'outcome': 'consumer onboarding, signup, or habit-forming app page',
        'vibe': 'playful tactile with high clarity and low friction',
        'bundleHints': ['component-pantry', 'ai-product-launch-kit', 'saas-landing-kit'],
        'query': r'playful|duolingo|onboarding|signup|login|form|ripple|blob|cards|swipe|consumer|waitlist|interactive',
        'avoid': r'dashboard|terminal|finance|security|brutalist|enterprise',
        'selectionRules': {
            'structure': 'Use simple launch/onboarding references for a low-friction funnel.',
            'style': 'Borrow playful tactile components, but keep layout and copy calm enough to trust.',
            'motion': 'Use press feedback, direction-aware progression, and small celebratory reveals.',
            'sections': 'Include friendly promise hero, steps/screens, benefit cards, social proof, form, and confirmation state.',
        },
    },
    {
        'id': 'gallery-archive-experience',
        'title': 'Gallery/archive: browseable visual collection',
        'outcome': 'visual archive, inspiration gallery, or prompt/source library',
        'vibe': 'editorial gallery with useful filtering and source provenance',
        'bundleHints': ['portfolio-studio-kit', 'luxury-editorial-kit', 'component-pantry'],
        'query': r'gallery|archive|library|portfolio|case study|cards|filter|search|source|collection|museum|field notes|visual',
        'avoid': r'pricing|finance|security|terminal-only|heavy dashboard',
        'selectionRules': {
            'structure': 'Use gallery/portfolio references for browsing rhythm and detail views.',
            'style': 'Borrow editorial gallery pacing with compact source-first metadata.',
            'motion': 'Use shared-element transitions, layout animation for filters, and quiet scroll reveal.',
            'sections': 'Include collection hero, filter/search console, featured shelves, card grid, detail modal, and source ledger.',
        },
    },
    {
        'id': 'pricing-comparison-page',
        'title': 'Pricing/comparison: trust-first decision page',
        'outcome': 'pricing, plan comparison, or buy/upgrade decision page',
        'vibe': 'finance trust with clear comparison hierarchy',
        'bundleHints': ['saas-landing-kit', 'dashboard-product-kit', 'component-pantry'],
        'query': r'pricing|plan|comparison|compare|tier|checkout|subscription|finance|revenue|saas|cta|faq|trust',
        'avoid': r'portfolio|fashion|cosmic|particle|gallery-only',
        'selectionRules': {
            'structure': 'Use pricing/comparison references for decision flow and tier hierarchy.',
            'style': 'Borrow finance-trust or modern minimal tokens with tabular numbers and restrained emphasis.',
            'motion': 'Use small layout animation for plan toggles and press feedback for CTAs only.',
            'sections': 'Include pricing hero, billing toggle, plan cards, comparison table, proof/security, FAQ, and final CTA.',
        },
    },
    {
        'id': 'changelog-release-notes',
        'title': 'Changelog: release story + product momentum',
        'outcome': 'changelog, release notes, or product update page',
        'vibe': 'technical utility with editorial product storytelling',
        'bundleHints': ['devtool-open-source-kit', 'saas-landing-kit', 'component-pantry'],
        'query': r'changelog|release|update|version|docs|timeline|roadmap|github|open source|feature|product|notes',
        'avoid': r'fashion|commerce|luxury|heavy 3d|pricing-only',
        'selectionRules': {
            'structure': 'Use timeline/docs references for chronological scanning and version grouping.',
            'style': 'Borrow technical minimal surfaces with editorial release summaries.',
            'motion': 'Use scroll reveal for release groups and layout animation for filters/search.',
            'sections': 'Include update hero, latest release card, timeline, filter/search, feature detail panels, and subscription CTA.',
        },
    },
    {
        'id': 'investor-narrative-deck-page',
        'title': 'Investor narrative: metrics + market story',
        'outcome': 'investor, fundraising, or strategic narrative page',
        'vibe': 'formal finance trust with editorial pacing',
        'bundleHints': ['dashboard-product-kit', 'saas-landing-kit', 'luxury-editorial-kit'],
        'query': r'investor|deck|metrics|revenue|finance|market|growth|traction|dashboard|chart|story|enterprise',
        'avoid': r'playful|duolingo|fashion|loader|cosmic particles',
        'selectionRules': {
            'structure': 'Use editorial/deck-like references for narrative order and dashboard references for proof.',
            'style': 'Borrow formal finance-trust styling with precise charts and calm typography.',
            'motion': 'Use restrained chart reveal and crossfade between narrative chapters.',
            'sections': 'Include thesis hero, market context, traction proof, product workflow, business model, roadmap, and contact CTA.',
        },
    },
    {
        'id': 'marketplace-community-launch',
        'title': 'Marketplace/community: supply + demand launch',
        'outcome': 'marketplace, community, or ecosystem launch page',
        'vibe': 'community energy with trustworthy product structure',
        'bundleHints': ['saas-landing-kit', 'ai-product-launch-kit', 'component-pantry'],
        'query': r'marketplace|community|creator|social|member|profile|avatar|event|launch|waitlist|gallery|cards|proof',
        'avoid': r'terminal-only|security|finance dashboard|brutalist infra',
        'selectionRules': {
            'structure': 'Use launch/SaaS references for conversion and gallery/card references for ecosystem proof.',
            'style': 'Borrow community energy with avatar clusters, expressive accents, and clear action surfaces.',
            'motion': 'Use staggered member/card reveals and shared-element transitions into profile/detail states.',
            'sections': 'Include two-sided hero, participant proof, how it works, featured members/items, trust rules, and join CTA.',
        },
    },
    {
        'id': 'location-map-experience',
        'title': 'Map/location: spatial product story',
        'outcome': 'map-led local, travel, logistics, or location intelligence page',
        'vibe': 'spatial editorial with clear map/data affordances',
        'bundleHints': ['dashboard-product-kit', 'portfolio-studio-kit', 'component-pantry'],
        'query': r'map|location|route|travel|city|logistics|globe|geography|dashboard|filter|search|gallery|local',
        'avoid': r'pricing-only|fashion commerce|terminal-only|loader',
        'selectionRules': {
            'structure': 'Use dashboard/gallery references for map-plus-list interaction and editorial references for place narrative.',
            'style': 'Borrow spatial editorial styling with readable map controls and strong information scent.',
            'motion': 'Use direction-aware transitions for route/state changes and subtle shared-element map/list linking.',
            'sections': 'Include spatial hero, map/list explorer, route or place detail, proof/data layer, use cases, and CTA.',
        },
    },
    {
        'id': 'cinematic-launch-hero',
        'title': 'Cinematic launch: hero spectacle + proof floor',
        'outcome': 'cinematic product launch page anchored by one memorable hero moment',
        'vibe': 'cinematic spatial with proof-led product sections',
        'bundleHints': ['motion-first-hero-kit', 'ai-product-launch-kit', 'saas-landing-kit'],
        'query': r'cinematic|3d|video|hero|particle|space|globe|motion|launch|product|animation|scroll|reveal',
        'avoid': r'pricing-only|docs-only|dense dashboard|terminal-only',
        'selectionRules': {
            'structure': 'Use a launch/landing reference as page skeleton and a cinematic reference only for the hero moment.',
            'style': 'Borrow cinematic spatial atmosphere but keep downstream product surfaces credible.',
            'motion': 'Use one memorable hero/scroll moment, then reduce motion to proof and microinteractions.',
            'sections': 'Include cinematic hero, product proof band, workflow or feature sections, comparison/trust, and CTA.',
        },
    },
    {
        'id': 'settings-admin-console',
        'title': 'Settings/admin: operational clarity',
        'outcome': 'settings, admin, account, or operations console interface',
        'vibe': 'technical utility with compact interaction states',
        'bundleHints': ['dashboard-product-kit', 'devtool-open-source-kit', 'component-pantry'],
        'query': r'settings|admin|account|permissions|team|security|table|dashboard|console|form|filter|tabs|controls',
        'avoid': r'fashion|luxury|cosmic|cinematic hero|gallery-only',
        'selectionRules': {
            'structure': 'Use dashboard/devtool references for navigation, forms, tables, and status panels.',
            'style': 'Borrow technical utility with compact controls, clear labels, and visible state hierarchy.',
            'motion': 'Use layout animation for panel changes and origin-aware popovers for menus/tooltips.',
            'sections': 'Include settings shell, nav rail, account/team/security panels, audit/status area, table/forms, and empty/error states.',
        },
    },
    {
        'id': 'case-study-proof-page',
        'title': 'Case study: before/after proof narrative',
        'outcome': 'case study, customer story, or proof-led marketing page',
        'vibe': 'editorial proof narrative with concrete outcomes',
        'bundleHints': ['portfolio-studio-kit', 'saas-landing-kit', 'dashboard-product-kit'],
        'query': r'case study|customer|testimonial|proof|before|after|workflow|dashboard|portfolio|story|results|metrics',
        'avoid': r'loader|particle|fashion-only|terminal-only|generic waitlist',
        'selectionRules': {
            'structure': 'Use case-study/portfolio references for narrative and dashboard references for credible proof.',
            'style': 'Borrow editorial typography with trustworthy metrics and explicit source/proof framing.',
            'motion': 'Use comparison-frame reveals and shared-element transitions between summary and detail.',
            'sections': 'Include customer/problem hero, before state, solution workflow, evidence/results, implementation details, and CTA.',
        },
    },
]


def norm(s):
    return re.sub(r'\s+', ' ', str(s or '').strip().lower())


def text_blob(post, prompt='', meta=None):
    meta = meta or {}
    parts = [post.get('slug'), post.get('title'), post.get('sectionType'), post.get('sourceName'), post.get('author')]
    parts += post.get('tags') or []
    parts += post.get('aiTools') or []
    parts += [meta.get('useCase'), meta.get('siteType'), meta.get('aesthetic'), meta.get('motionLevel'), meta.get('tier')]
    parts += meta.get('normalizedTags') or []
    parts += [prompt[:2200]]
    return norm(' '.join(str(x or '') for x in parts))


def role_ids_for(post, prompt, meta):
    blob = text_blob(post, prompt, meta)
    roles = []
    use_case = meta.get('useCase', '')
    if use_case in {'full page', 'dashboard'} or re.search(r'landing page|homepage|website|saas|portfolio|dashboard|docs-first|multi-section|pricing|faq', blob):
        roles.append('dominant-structure')
    if use_case == 'hero' or re.search(r'\bhero\b|waitlist|above.the.fold|headline', blob):
        roles.append('hero-concept')
    if re.search(r'editorial|luxury|glass|cinematic|3d|monochrome|brutalist|playful|minimal|fashion|tea|museum|space|cosmic|aesthetic', blob):
        roles.append('visual-skin')
    if use_case == 'motion system' or re.search(r'motion|animation|gsap|scroll|transition|stagger|parallax|marquee|hover|kinetic|loader|video|reveal', blob):
        roles.append('motion-layer')
    if use_case == 'section' or re.search(r'pricing|faq|testimonial|feature|bento|proof|workflow|integrations|logo cloud|stats|team|footer', blob):
        roles.append('section-pattern')
    if use_case == 'component' or re.search(r'button|dock|popover|card|carousel|form|terminal|loader|typewriter|scramble|beam|globe|map|ripple', blob):
        roles.append('component-accent')
    if re.search(r'particle|glass|cosmic|loader|heavy|fake|experimental|brutalist|glow', blob) or (meta.get('motionLevel') == 'heavy' and meta.get('useCase') == 'component'):
        roles.append('anti-pattern-guardrail')
    if not roles:
        roles = ['visual-skin']
    # Keep role order stable and unique.
    ordered = [r[0] for r in ROLES]
    return [role for role in ordered if role in set(roles)]


def vocab_terms_for(post, prompt, meta):
    blob = text_blob(post, prompt, meta)
    term_rules = {
        'stagger': r'stagger|cascade|sequence|cards|list|grid',
        'scroll-reveal': r'scroll|reveal|viewport|gsap|scrolltrigger',
        'layout-animation': r'layout|bento|grid|rearrange|filter|dashboard|cards',
        'direction-aware-transition': r'direction|navigation|carousel|slide|swipe',
        'shared-element-transition': r'card|gallery|detail|modal|thumbnail|expand',
        'crossfade': r'fade|crossfade|gallery|image|video',
        'origin-aware-pop': r'popover|menu|dock|button|modal|tooltip',
        'parallax-depth': r'parallax|depth|3d|space|cosmic|hero',
        'press-feedback': r'button|tap|press|hover|ripple|interactive',
        'kinetic-type': r'type|headline|scramble|typewriter|kinetic|text',
        'split-hero': r'hero|landing|homepage|waitlist',
        'dashboard-proof': r'dashboard|analytics|metrics|command|ops|console|finance',
        'editorial-stack': r'editorial|portfolio|studio|fashion|tea|museum|field notes',
        'asymmetric-bento': r'bento|feature|grid|cards|saas',
        'proof-band': r'proof|logos|stats|testimonial|trust|customer',
        'workflow-timeline': r'workflow|process|timeline|steps|automation|agent',
        'sticky-scrollytelling': r'sticky|scroll|scrollytelling|story',
        'comparison-frame': r'compare|before|after|pricing|problem|solution',
        'gallery-rhythm': r'gallery|portfolio|case study|fashion|commerce|museum',
        'command-console': r'terminal|command|console|devtool|docs|api|dashboard',
        'warm-editorial': r'warm|editorial|paper|field notes|portfolio|studio',
        'technical-minimal': r'technical|devtool|docs|minimal|api|code',
        'cinematic-3d': r'cinematic|3d|space|cosmic|particle|globe|video',
        'luxury-monochrome': r'luxury|fashion|tea|automotive|museum|monochrome|premium',
        'playful-tactile': r'playful|duolingo|ripple|blob|swipe|cards|toy',
        'brutalist-utility': r'brutalist|raw|utility|industrial|mechanical',
        'glass-luminous': r'glass|glow|luminous|liquid|aurora|blur|metal',
        'dense-dashboard': r'dashboard|analytics|ops|console|finance|inventory|dense',
        'hierarchy': r'hero|headline|typography|section|landing|website',
        'spatial-consistency': r'layout|grid|cards|motion|animation|transition',
        'affordance': r'button|form|dock|popover|interactive|hover|tap',
        'contrast': r'glass|dark|light|editorial|luxury|dashboard',
        'rhythm': r'gallery|editorial|section|cards|scroll|portfolio',
        'content-density': r'dashboard|command|console|pricing|feature|docs',
        'information-scent': r'cta|navigation|search|filter|docs|source|archive',
        'mobile-composition': r'responsive|mobile|landing|website|dashboard',
        'specific-promise': r'ai|saas|product|workflow|automation|tool|app',
        'credible-proof': r'dashboard|proof|metrics|testimonial|source|github|logos',
        'section-contract': r'pricing|faq|feature|workflow|hero|footer|cta|section',
        'anti-filler-copy': r'ai|marketing|landing|saas|hero|product',
        'implementation-constraints': r'react|tailwind|css|html|responsive|code|component',
        'source-attribution': r'magic ui|animata|tailark|cult ui|motionsites|source|github',
    }
    terms = [term for term, rx in term_rules.items() if re.search(rx, blob, re.I)]
    if len(terms) < 4:
        defaults = ['hierarchy', 'spatial-consistency', 'section-contract', 'implementation-constraints']
        for term in defaults:
            if term not in terms:
                terms.append(term)
            if len(terms) >= 4:
                break
    return terms[:12]


def mix_guidance(roles, terms, meta):
    if 'dominant-structure' in roles:
        use = 'Use as the page skeleton and section order; let other references modify style, motion, or specific sections.'
        avoid = 'Do not combine with another full-page structure without choosing one as dominant.'
    elif 'hero-concept' in roles:
        use = 'Use for first-screen concept, headline/visual relationship, or hero motion.'
        avoid = 'Do not let hero spectacle overwrite product clarity or downstream sections.'
    elif 'component-accent' in roles:
        use = 'Use as a small interaction/component accent inside a stronger page recipe.'
        avoid = 'Do not ask it to define the whole website.'
    elif 'motion-layer' in roles:
        use = 'Borrow timing, transitions, and choreography as a motion layer.'
        avoid = 'Do not copy every visual surface just because the motion is useful.'
    else:
        use = 'Use as a style/reference ingredient when it matches the desired outcome.'
        avoid = 'Do not merge incompatible aesthetics without an explicit bridge.'
    if 'glass-luminous' in terms:
        avoid += ' Constrain glass/blur so contrast stays readable.'
    if meta.get('motionLevel') == 'heavy':
        avoid += ' Reduce motion for mobile and dense content.'
    return use, avoid


def term_payload():
    return {
        category: [
            {'id': term_id, 'label': term_id.replace('-', ' ').title(), 'definition': definition, 'promptInstruction': instruction}
            for term_id, definition, instruction in entries
        ]
        for category, entries in VOCABULARY.items()
    }


def score_item_for_recipe(item, meta, recipe):
    blob = norm(' '.join([item['title'], ' '.join(item['roles']), ' '.join(item['vocabularyTerms']), meta.get('useCase',''), meta.get('siteType',''), meta.get('aesthetic','')]))
    if re.search(recipe['avoid'], blob, re.I):
        return -20
    score = float(meta.get('qualityScore') or 2.5)
    if re.search(recipe['query'], blob, re.I):
        score += 3
    role_bonus = {
        'dominant-structure': 1.4,
        'hero-concept': 1.0,
        'visual-skin': .7,
        'motion-layer': .8,
        'section-pattern': .8,
        'component-accent': .2,
        'anti-pattern-guardrail': -1.2,
    }
    score += sum(role_bonus.get(role, 0) for role in item['roles'])
    return score


def pick_recipe_slugs(recipe, items, curation_items):
    scored = []
    for slug, item in items.items():
        score = score_item_for_recipe(item, curation_items.get(slug, {}), recipe)
        if score > 0:
            scored.append((score, slug, item))
    scored.sort(key=lambda x: x[0], reverse=True)

    chosen = []
    required_roles = ['dominant-structure', 'hero-concept', 'visual-skin', 'motion-layer', 'section-pattern', 'component-accent']
    for role in required_roles:
        for _, slug, item in scored:
            if slug not in chosen and role in item['roles']:
                chosen.append(slug)
                break
    for _, slug, _ in scored:
        if slug not in chosen:
            chosen.append(slug)
        if len(chosen) >= 10:
            break
    return chosen[:10]


def recipe_template(recipe, slugs, items):
    role_lines = []
    for slug in slugs[:7]:
        item = items[slug]
        role_lines.append(f"- {item['title']}: {', '.join(item['roles'][:3])}; use it for {item['mixUse']}")
    terms = []
    for slug in slugs:
        for term in items[slug]['vocabularyTerms']:
            if term not in terms:
                terms.append(term)
    term_line = ', '.join(terms[:10])
    directions = [DESIGN_DIRECTIONS[d] for d in DIRECTION_HINTS.get(recipe['id'], ['modern-minimal'])]
    direction_lines = '\n'.join(
        f"- {d['label']}: {d['tokens']}. Use when {d['useWhen']}; avoid: {d['avoid']}."
        for d in directions
    )
    pipeline_lines = '\n'.join(f"- {stage['label']}: {stage['instruction']}" for stage in DEFAULT_PIPELINE)
    acceptance_lines = '\n'.join(f"- {criterion}" for criterion in DEFAULT_ACCEPTANCE)
    return (
        f"Build a {recipe['outcome']} with a {recipe['vibe']} vibe.\n\n"
        "Pre-flight inputs to lock before designing:\n"
        "- Surface, audience, product promise, and brand constraints.\n"
        "- Pick one design direction from the recipe options before selecting references.\n\n"
        "Design direction options:\n"
        f"{direction_lines}\n\n"
        "Mix grammar:\n"
        "1. Pick one dominant-structure reference as the page skeleton.\n"
        "2. Pick one visual-skin reference for typography, color, and atmosphere.\n"
        "3. Pick one motion-layer reference for choreography only.\n"
        "4. Add section-pattern and component-accent references as supporting ingredients.\n"
        "5. Resolve conflicts by demoting incompatible references to accents or anti-pattern guardrails.\n\n"
        f"Recipe rules:\n- Structure: {recipe['selectionRules']['structure']}\n"
        f"- Style: {recipe['selectionRules']['style']}\n"
        f"- Motion: {recipe['selectionRules']['motion']}\n"
        f"- Sections: {recipe['selectionRules']['sections']}\n\n"
        "Generation pipeline:\n"
        f"{pipeline_lines}\n\n"
        f"Vocabulary to use explicitly: {term_line}.\n\n"
        "Selected Framewell references and roles:\n"
        + '\n'.join(role_lines)
        + "\n\nAcceptance checks:\n"
        + acceptance_lines
        + "\n\nQuality bar:\n- The page must feel cohesive, not like a collage.\n- First viewport must explain product, user, and value.\n- Motion must clarify hierarchy or product behavior.\n- Mobile composition must be intentional.\n- Avoid fake dashboards, meaningless metrics, and generic AI copy."
    )


def main():
    posts = json.loads(POSTS_PATH.read_text())
    prompts = json.loads(PROMPTS_PATH.read_text()) if PROMPTS_PATH.exists() else {}
    curation = json.loads(CURATION_PATH.read_text()) if CURATION_PATH.exists() else {'items': {}, 'bundles': []}
    curation_items = curation.get('items') or {}

    items = {}
    role_counter = Counter()
    term_counter = Counter()
    for post in posts:
        slug = post['slug']
        meta = curation_items.get(slug, {})
        prompt = prompts.get(slug) or prompts.get(post['id']) or ''
        roles = role_ids_for(post, prompt, meta)
        terms = vocab_terms_for(post, prompt, meta)
        mix_use, mix_avoid = mix_guidance(roles, terms, meta)
        item = {
            'id': post['id'],
            'slug': slug,
            'title': post['title'],
            'roles': roles,
            'primaryRole': roles[0],
            'vocabularyTerms': terms,
            'mixUse': mix_use,
            'mixAvoid': mix_avoid,
            'dominance': 'dominant' if 'dominant-structure' in roles else ('supporting' if any(r in roles for r in ['hero-concept', 'visual-skin', 'motion-layer', 'section-pattern']) else 'accent'),
            'compatibleWith': [pair[1] for pair in COMPATIBILITY['goodPairs'] if pair[0] in terms][:5],
            'watchConflicts': [pair[1] for pair in COMPATIBILITY['badPairs'] if pair[0] in terms][:5],
        }
        items[slug] = item
        role_counter.update(roles)
        term_counter.update(terms)

    recipes = []
    for recipe in RECIPES:
        slugs = pick_recipe_slugs(recipe, items, curation_items)
        recipes.append({
            'id': recipe['id'],
            'title': recipe['title'],
            'outcome': recipe['outcome'],
            'vibe': recipe['vibe'],
            'bundleHints': recipe['bundleHints'],
            'inputs': RECIPE_INPUTS,
            'designDirections': [
                {'id': direction_id, **DESIGN_DIRECTIONS[direction_id]}
                for direction_id in DIRECTION_HINTS.get(recipe['id'], ['modern-minimal'])
            ],
            'pipeline': DEFAULT_PIPELINE,
            'acceptanceCriteria': DEFAULT_ACCEPTANCE,
            'selectionRules': recipe['selectionRules'],
            'promptSlugs': slugs,
            'briefTemplate': recipe_template(recipe, slugs, items),
        })

    out = {
        'version': 1,
        'generatedBy': 'scripts/build_composition_json.py',
        'summary': {
            'total': len(items),
            'vocabularyTerms': sum(len(v) for v in VOCABULARY.values()),
            'roles': len(ROLES),
            'recipes': len(recipes),
            'curationBundles': len(curation.get('bundles') or []),
            'roleCounts': role_counter.most_common(),
            'topVocabularyTerms': term_counter.most_common(24),
        },
        'vocabulary': term_payload(),
        'roles': [{'id': rid, 'label': rid.replace('-', ' ').title(), 'definition': definition, 'usage': usage} for rid, definition, usage in ROLES],
        'compatibility': COMPATIBILITY,
        'items': items,
        'recipes': recipes,
    }
    OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    print(f"wrote {len(items)} composition records, {len(recipes)} recipes, and {out['summary']['vocabularyTerms']} vocabulary terms to data/composition.json")


if __name__ == '__main__':
    main()
