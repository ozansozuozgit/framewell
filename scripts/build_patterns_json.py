#!/usr/bin/env python3
"""Build Framewell's curated live effect atlas.

The output is intentionally effect-first: isolated iframe specimens with source,
optional prompt, tags, and mix roles. The old prompt archive can exist, but the
homepage should favor these polished atoms.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERN_DIR = ROOT / "patterns"
DATA_PATH = ROOT / "data" / "patterns.json"

# Curated from archive themes + public inspiration categories: Awwwards GSAP/WebGL,
# Codrops shader/scroll/text demos, GSAP showcase, and classic creative portfolios.
# These are original local specimens, not copied third-party source.
PATTERNS = [
    # Cinematic / hero / WebGL-feeling
    ("cinematic-scroll-camera", "Cinematic scroll camera pass", "Scroll cinema", "Portfolio", "A product scene appears to move past camera planes as the page scrolls.", ["gsap", "scrolltrigger", "camera", "portfolio", "cinematic"], "motion", "motionsites-space-voyage"),
    ("shader-type-dissolve", "Shader text dissolve", "Text effect", "Portfolio", "Large type breaks into particles and reforms on hover/focus.", ["webgl", "shader", "text", "particles", "hero"], "type-dissolve", "x-render-and-co-3d-animation-studio"),
    ("webgl-image-ripple-grid", "WebGL image ripple grid", "Image grid", "Portfolio", "A project grid bends like liquid when the pointer crosses each tile.", ["webgl", "image-grid", "ripple", "portfolio", "hover"], "ripple-grid", "template-ui-layouts-interactive-gallery"),
    ("orbital-product-stage", "Orbital product stage", "3D orbit", "SaaS hero", "Cards and chips orbit a central object with depth and parallax.", ["three-js", "orbit", "product", "hero", "depth"], "orbit-stage", "opencodesign-product-launch-page"),
    ("glass-torus-pricing", "Glass torus pricing focus", "Refraction", "Pricing", "A refractive ring highlights the recommended pricing card without clutter.", ["glass", "refraction", "pricing", "premium"], "refractive-pricing", "tailark-pricing-comparison"),
    ("particle-cursor-constellation", "Particle cursor constellation", "Cursor field", "Portfolio", "Pointer movement pulls a constellation field behind the content.", ["particles", "cursor", "ambient", "webgl-feel"], "constellation", "opencodesign-particle-field-data-hero"),
    ("scroll-sliced-hero", "Scroll-sliced hero poster", "Scroll reveal", "Landing page", "Poster slices separate and reveal the product promise underneath.", ["scroll", "mask", "poster", "gsap", "hero"], "slice-poster", "motionsites-free-visual-hero"),
    ("liquid-metal-cta", "Liquid metal CTA", "Microinteraction", "Landing page", "A call-to-action surface flows like mercury on hover.", ["button", "liquid", "premium", "hover"], "liquid-cta", "motionsites-liquid-glass-agency"),

    # Navigation / menus
    ("magnetic-work-menu", "Magnetic work menu", "Menu", "Portfolio", "Project links stretch toward the pointer with oversized typography.", ["menu", "magnetic", "portfolio", "typography"], "magnetic-menu", "motionsites-portfolio-cosmic"),
    ("dock-with-liquid-focus", "Liquid focus dock", "Navigation", "App shell", "A dock bubble slides between icons and previews the destination.", ["dock", "navigation", "liquid", "app"], "liquid-dock", "template-shadcnstore-chat-support-console"),
    ("radial-command-wheel", "Radial command wheel", "Command", "AI app", "Keyboard actions bloom into a radial, spatial command palette.", ["command", "radial", "keyboard", "ai"], "radial-command", "template-shadcnstore-analytics-command-center"),
    ("split-panel-route-transition", "Split-panel route transition", "Transition", "Web app", "Two panels wipe in opposing directions for page transitions.", ["page-transition", "wipe", "panels", "route"], "split-transition", "template-karthik-dark-saas-launch"),
    ("cursor-reveal-mega-menu", "Cursor reveal mega menu", "Menu", "Marketing", "Menu panels reveal images only under the cursor spotlight.", ["mega-menu", "spotlight", "cursor", "navigation"], "spotlight-menu", "tailark-integrations-cloud"),
    ("accordion-map-navigation", "Accordion map navigation", "Navigation", "Geo app", "A side accordion drives map markers and path emphasis.", ["map", "accordion", "navigation", "geo"], "map-accordion", "motionsites-terra-geo-map"),

    # Dashboard / AI app / dense product UI
    ("dashboard-row-scroll-reveal", "Dashboard row scroll reveal", "Dashboard motion", "Dashboard", "Dense rows lift, lock, and show confidence metadata as they enter.", ["dashboard", "scroll", "rows", "confidence"], "dashboard-rows", "opencodesign-ai-ops-command-center"),
    ("metric-cards-live-scrub", "Metric cards live scrub", "Data interaction", "Dashboard", "Dragging a timeline updates cards, sparklines, and alert tone together.", ["metrics", "scrub", "sparklines", "dashboard"], "metric-scrub", "opencodesign-saas-revenue-dashboard"),
    ("audit-evidence-peek", "Audit evidence peek", "Disclosure", "Dashboard", "Evidence opens inline with source chips instead of a modal detour.", ["audit", "evidence", "disclosure", "table"], "evidence-peek", "opencodesign-observability-dashboard"),
    ("ai-stream-with-sources", "AI stream with source chips", "AI response", "AI app", "Message lines stream in with attached citations and confidence states.", ["ai", "chat", "streaming", "sources"], "ai-stream", "template-shadcnstore-chat-support-console"),
    ("command-center-alert-lens", "Command center alert lens", "Status lens", "Ops dashboard", "A movable lens magnifies incidents and reveals hidden response actions.", ["ops", "lens", "incident", "dashboard"], "alert-lens", "opencodesign-ai-ops-command-center"),
    ("kanban-physics-lift", "Kanban physics lift", "Drag affordance", "Internal tool", "Cards tilt, cast shadows, and snap into lanes before a drag starts.", ["kanban", "drag", "physics", "board"], "kanban-physics", "template-shadcnstore-mail-task-dashboard"),
    ("calendar-density-brush", "Calendar density brush", "Calendar interaction", "Calendar", "Dragging across a dense calendar reveals heat and available gaps.", ["calendar", "density", "brush", "schedule"], "calendar-brush", "template-shadcnstore-calendar-ops-dashboard"),
    ("data-lineage-river", "Data lineage river", "Data viz", "Analytics", "Streams split from a source into model, alert, and decision nodes.", ["lineage", "data-viz", "flow", "dashboard"], "lineage-river", "opencodesign-design-token-inspector"),
    ("security-radar-sweep", "Security radar sweep", "Status visual", "Security", "A radar sweep checks assets and leaves classified severity blips.", ["security", "radar", "scan", "status"], "radar-sweep", "opencodesign-enterprise-security-page"),
    ("inventory-shelf-pulse", "Inventory shelf pulse", "Commerce alert", "Commerce", "Inventory rows compress into shelf lanes and pulse at risk points.", ["commerce", "inventory", "alerts", "table"], "shelf-pulse", "opencodesign-ecommerce-inventory-dashboard"),

    # Content / editorial / portfolio sections
    ("horizontal-case-filmstrip", "Horizontal case filmstrip", "Project browse", "Portfolio", "Case studies move as a cinematic horizontal reel with active captions.", ["horizontal-scroll", "portfolio", "filmstrip", "cases"], "filmstrip", "opencodesign-boutique-agency-homepage"),
    ("stacked-editorial-cards", "Stacked editorial cards", "Scroll stack", "Article", "Editorial cards pin and stack like a physical dossier.", ["scroll", "stack", "editorial", "cards"], "stacked-cards", "opencodesign-field-notes-landing-page"),
    ("mask-reveal-testimonials", "Mask reveal testimonials", "Proof", "Marketing", "Quotes reveal through animated masks, keeping the wall premium and calm.", ["testimonials", "mask", "proof", "animation"], "mask-proof", "tailark-testimonial-wall"),
    ("logo-cloud-depth-marquee", "Depth logo marquee", "Proof", "Marketing", "Logo strips move at different depths with soft mask edges.", ["marquee", "logos", "depth", "proof"], "depth-marquee", "tailark-logo-cloud-marquee"),
    ("faq-elastic-drawer", "FAQ elastic drawer", "Accordion", "Marketing", "Questions open with springy drawers, icon twist, and content shadows.", ["faq", "accordion", "spring", "drawer"], "elastic-faq", "tailark-faq-accordion-section"),
    ("team-spotlight-grid", "Team spotlight grid", "People grid", "Marketing", "A cursor spotlight reveals portraits, roles, and one-line principles.", ["team", "spotlight", "grid", "people"], "team-spotlight", "tailark-team-grid-editorial"),
    ("stats-countup-proof-band", "Count-up proof band", "Proof", "Marketing", "Proof numbers count once, then leave tactile confidence marks.", ["stats", "count-up", "proof", "scroll"], "stats-band", "tailark-stats-proof-band"),
    ("footer-gravity-links", "Gravity footer links", "Footer", "Marketing", "Footer links cluster around the CTA and drift like low gravity objects.", ["footer", "gravity", "links", "cta"], "gravity-footer", "tailark-final-cta-footer"),

    # Input/forms/conversion/onboarding
    ("search-bar-morph-results", "Search bar morph results", "Search", "Web app", "Search expands into a command surface with grouped live results.", ["search", "command", "results", "morph"], "search-morph", "template-ui-layouts-interactive-gallery"),
    ("onboarding-constellation", "Onboarding constellation picker", "Onboarding", "AI app", "Choices become a constellation map that explains the setup path.", ["onboarding", "constellation", "choices", "ai"], "onboard-stars", "opencodesign-ai-notebook-waitlist"),
    ("pricing-card-pressure", "Pricing pressure card", "Pricing", "SaaS", "Recommended plan reacts to plan toggles with proof and pressure indicators.", ["pricing", "toggle", "proof", "saas"], "pricing-pressure", "tailark-pricing-comparison"),
    ("form-field-living-label", "Living form label", "Form", "SaaS", "Labels become validation hints, progress, and context without extra chrome.", ["form", "label", "validation", "microinteraction"], "living-label", "template-ixartz-devtool-landing-page"),
    ("empty-state-suggestion-orbit", "Suggestion orbit empty state", "Empty state", "AI app", "Suggested actions orbit the empty state and collapse into the chosen action.", ["empty-state", "ai", "suggestions", "orbit"], "empty-orbit", "opencodesign-ai-writing-assistant-hero"),
    ("copy-button-success-sweep", "Success sweep copy button", "Microinteraction", "Devtool", "A code copy button confirms with a fast sweep and inline command memory.", ["copy", "code", "success", "devtool"], "copy-sweep", "template-ixartz-devtool-landing-page"),

    # Experimental / possible ingredients
    ("infinite-marquee-cards", "Infinite marquee cards", "Loop", "Gallery", "Cards loop in two directions while preserving hover focus.", ["marquee", "cards", "loop", "gallery"], "card-marquee", "website-cards-animation"),
    ("spring-roller-blind", "Spring roller blind reveal", "Mask reveal", "Hero", "A blind mask rolls down, overshoots, and uncovers the content in bands.", ["mask", "spring", "reveal", "hero"], "roller-blind", "spring-roller-blind-reveal"),
    ("3d-carousel-prism", "3D prism carousel", "Carousel", "Portfolio", "Slides rotate through a prism instead of a flat carousel.", ["3d", "carousel", "prism", "portfolio"], "prism-carousel", "motionsites-portfolio-cosmic"),
    ("svg-line-draw-map", "SVG line-draw map", "Map path", "Geo app", "Routes draw in with labels and pulsing handoff points.", ["svg", "map", "line-draw", "geo"], "line-map", "motionsites-terra-geo-map"),
    ("noise-gradient-hero", "Noise gradient hero field", "Ambient", "Landing page", "A living gradient mesh with grain and restrained pulse under the hero.", ["gradient", "noise", "ambient", "hero"], "noise-gradient", "motionsites-free-stellar-ai"),
    ("pixel-dissolve-card", "Pixel dissolve card", "Transition", "Portfolio", "A card dissolves into square pixels before revealing alternate content.", ["pixel", "dissolve", "transition", "hover"], "pixel-dissolve", "motionsites-free-vex-ventures"),
    ("scroll-progress-rail", "Scroll progress rail", "Scroll aid", "Docs", "A progress rail becomes section navigation, status, and mini map.", ["scroll", "progress", "docs", "navigation"], "progress-rail", "template-ixartz-docs-first-saas-home"),
    ("clip-path-gallery-shuffle", "Clip-path gallery shuffle", "Gallery", "Portfolio", "Images shuffle through angular clip paths like a poster deck.", ["clip-path", "gallery", "shuffle", "portfolio"], "clip-gallery", "template-ui-layouts-creative-scroll-home"),
    ("audio-wave-loader", "Audio wave loader", "Loader", "Media", "Loading becomes a compact equalizer with branded rhythm.", ["loader", "audio", "equalizer", "motion"], "audio-loader", "motionsites-loader-animation"),
    ("morphing-section-divider", "Morphing section divider", "Divider", "Landing page", "A divider shape morphs to signal moving between product modes.", ["svg", "morph", "divider", "section"], "morph-divider", "motionsites-free-transform-data"),
    ("sticky-comparison-wipe", "Sticky comparison wipe", "Compare", "Marketing", "A sticky before/after wipe makes a product claim tangible.", ["compare", "wipe", "sticky", "before-after"], "comparison-wipe", "opencodesign-open-source-project-homepage"),
    ("notebook-annotation-rail", "Notebook annotation rail", "Editor", "AI notebook", "Side notes magnetize to selected paragraphs and source chips.", ["editor", "annotations", "notebook", "ai"], "annotation-rail", "opencodesign-ai-writing-assistant-hero"),
    ("task-completion-confetti-minimal", "Minimal completion burst", "Celebration", "Productivity", "Completing a task emits a tiny geometric burst without becoming childish.", ["completion", "confetti", "minimal", "task"], "completion-burst", "motionsites-free-taskly"),
    ("bento-depth-hover", "Depth bento hover", "Bento", "Marketing", "Feature cards tilt at different z-depths with a single light source.", ["bento", "hover", "depth", "feature"], "depth-bento", "tailark-feature-bento-grid"),
    ("cinematic-loader-title", "Cinematic loader title", "Loader", "Portfolio", "A loader turns into the first heading using split letters and a wipe.", ["loader", "title", "split-text", "portfolio"], "title-loader", "motionsites-loader-animation"),
    ("responsive-device-morph", "Device morph preview", "Responsive", "Landing page", "A desktop mockup morphs into tablet/mobile frames to prove adaptability.", ["responsive", "device", "morph", "preview"], "device-morph", "template-ixartz-devtool-landing-page"),
    ("map-cluster-explosion", "Map cluster explosion", "Map", "Geo app", "Clustered markers explode into categorized pins on focus.", ["map", "cluster", "pins", "geo"], "cluster-map", "motionsites-terra-geo-map"),
    ("tactile-toggle-array", "Tactile toggle array", "Controls", "Dashboard", "Small switches ripple across a settings panel to show dependency.", ["toggles", "controls", "settings", "dashboard"], "toggle-array", "template-shadcnstore-analytics-command-center"),
    ("table-column-xray", "Table column x-ray", "Table inspect", "Dashboard", "Hovering a column reveals calculations, source, and freshness in place.", ["table", "xray", "source", "dashboard"], "column-xray", "opencodesign-finance-ops-dashboard"),
    ("project-card-video-scrub", "Project card video scrub", "Portfolio card", "Portfolio", "Hover scrubs through project states instead of showing a static thumbnail.", ["video", "scrub", "portfolio", "card"], "video-scrub", "motionsites-motionz-premium"),
    ("scroll-triggered-3d-type", "Scroll-triggered 3D type", "Typography", "Portfolio", "Letters rotate in 3D as sections pass, then lock into readable text.", ["typography", "3d", "scroll", "gsap"], "type-3d", "x-luxury-tea-scrollytelling-gsap"),
    ("generative-background-controls", "Generative background controls", "Ambient controls", "Creative tool", "Tiny knobs visibly tune a generative mesh in the background.", ["generative", "background", "controls", "creative"], "gen-controls", "template-ui-layouts-interactive-gallery"),
    ("commerce-size-magnet", "Size selector magnet", "Commerce", "E-commerce", "Size chips magnetize to selection and show inventory pressure.", ["commerce", "selector", "magnetic", "inventory"], "size-magnet", "opencodesign-ecommerce-inventory-dashboard"),
    ("docs-code-stepper", "Docs code stepper", "Docs", "Developer docs", "Code blocks advance step-by-step with synchronized explanation cards.", ["docs", "code", "stepper", "developer"], "code-stepper", "template-ixartz-docs-first-saas-home"),
    ("privacy-vault-door", "Privacy vault door", "Security hero", "Security", "Panels lock together like a vault door around the CTA.", ["security", "vault", "hero", "motion"], "vault-door", "motionsites-free-vaultshield"),
    ("ai-agent-path-trace", "AI agent path trace", "Agent viz", "AI app", "An agent plan draws paths between tools, files, and decisions.", ["ai-agent", "path", "trace", "workflow"], "agent-trace", "opencodesign-ai-ops-command-center"),
    ("masonry-hover-recompose", "Masonry hover recompose", "Gallery", "Inspiration atlas", "A masonry wall subtly recomposes around the focused card.", ["masonry", "hover", "gallery", "inspiration"], "masonry-recompose", "template-ui-layouts-interactive-gallery"),
    ("kinetic-statements", "Kinetic statements", "Text motion", "Landing page", "Brand statements slide, snap, and invert as a concise hero system.", ["typography", "kinetic", "brand", "hero"], "kinetic-text", "motionsites-free-power-ai"),
    ("micro-chart-hover-pack", "Micro chart hover pack", "Charts", "Dashboard", "Tiny charts expose comparison, anomaly, and projection on hover.", ["charts", "hover", "micro", "dashboard"], "micro-charts", "opencodesign-creator-analytics-dashboard"),
    ("scroll-shadow-document", "Scroll shadow document", "Scroll affordance", "Docs", "Top/bottom shadows and sticky labels make long panels feel tactile.", ["scroll", "shadow", "document", "docs"], "doc-shadows", "template-ixartz-docs-first-saas-home"),
    ("hero-spotlight-letters", "Hero spotlight letters", "Hero text", "Portfolio", "A spotlight crosses huge letters and reveals texture inside the glyphs.", ["typography", "spotlight", "hero", "portfolio"], "spotlight-type", "motionsites-weblex-dark-hero"),

    # 2026 creative-dev inspirations: shader hover, WebGL corridors, handcrafted loaders
    ("brush-shader-project-reveal", "Brush shader project reveal", "Shader hover", "Portfolio", "Project thumbnails reveal through a painted shader mask that feels hand-directed.", ["shader", "brush", "webgl", "hover", "portfolio"], "brush-shader", "x-itom-portfolio-brush-shader"),
    ("infinite-3d-corridor-scroll", "Infinite 3D corridor scroll", "Scroll cinema", "Portfolio", "Cards form a depth corridor with a physics-feeling scroll/drag path.", ["three-js", "corridor", "scroll", "drag", "portfolio"], "corridor-scroll", "x-itom-portfolio-3d-corridor"),
    ("scroll-driven-3d-room", "Scroll-driven 3D room", "3D scene", "Portfolio", "A room-scale scene changes camera angle and focal object as sections advance.", ["three-js", "camera", "scrolltrigger", "environment", "portfolio"], "scene-room", "x-joseph-santamaria-scroll-3d"),
    ("water-shader-page-transition", "Water shader page transition", "Transition", "Portfolio", "Route changes ripple like water before resolving into the next case study.", ["shader", "water", "page-transition", "gsap"], "water-transition", "x-roman-jean-elie-shaders"),
    ("procedural-svg-preloader", "Procedural SVG preloader", "Loader", "Portfolio", "A generative logo/path loader becomes the first layout element instead of disappearing.", ["svg", "preloader", "procedural", "gsap", "brand"], "procedural-loader", "x-itom-portfolio-preloader"),
    ("dom-to-canvas-handoff", "DOM to canvas handoff", "Transition", "Portfolio", "A DOM card detaches into a canvas-feeling object for a seamless case-study open.", ["canvas", "handoff", "transition", "portfolio", "webgl-feel"], "canvas-handoff", "x-itom-dom-canvas-transition"),
    ("cloud-water-shader-hero", "Cloud/water shader hero", "Ambient", "Portfolio", "Soft cloud and water bands move behind type without stealing readability.", ["shader", "clouds", "water", "ambient", "hero"], "cloud-water", "x-roman-jean-elie-cloud-water"),
    ("horizontal-scroll-project-world", "Horizontal scroll project world", "Horizontal scene", "Portfolio", "Projects become a side-scrolling world with depth layers and readable stops.", ["horizontal-scroll", "parallax", "world", "portfolio", "gsap"], "project-world", "x-brandon-bartram-horizontal-grid"),
    ("interactive-canvas-puzzle", "Interactive canvas puzzle", "Canvas game", "Portfolio", "A small puzzle-game interaction reveals capabilities before opening the work.", ["canvas", "game", "puzzle", "portfolio", "interactive"], "canvas-puzzle", "x-gaurav-verma-canvas-game"),
    ("immersive-case-study-portal", "Immersive case-study portal", "3D portal", "Portfolio", "A portal frame refracts the next case study and gives the transition a destination.", ["portal", "three-js", "case-study", "transition"], "portal-case", "x-corentin-liard-immersive-3d"),
    ("shader-noise-navigation", "Shader noise navigation", "Menu", "Portfolio", "Navigation labels distort through a controlled noise field on hover.", ["shader", "noise", "navigation", "hover", "typography"], "noise-nav", "x-greensock-creative-nav"),
    ("depth-sorted-project-stack", "Depth-sorted project stack", "Project browse", "Portfolio", "A project stack sorts itself by depth, recency, or theme with a cinematic shuffle.", ["3d", "stack", "project", "sorting", "portfolio"], "depth-stack", "awwwards-project-stack"),
    ("webgpu-particle-logo-field", "WebGPU particle logo field", "Particle logo", "Hero", "A logo dissolves into a controlled particle field and reforms into product UI.", ["particles", "webgpu", "logo", "hero", "brand"], "particle-logo", "webgl-webgpu-showcase"),
    ("scroll-synced-model-exploder", "Scroll-synced model exploder", "3D product", "SaaS hero", "A product model explodes into labeled layers as the page scrolls.", ["three-js", "product", "exploded-view", "scroll", "saas"], "model-exploder", "gsap-scrolltrigger-product-demo"),
    ("elastic-cursor-work-index", "Elastic cursor work index", "Cursor", "Portfolio", "The cursor becomes a preview lens, action label, and magnetic selector in one.", ["cursor", "preview", "magnetic", "portfolio", "index"], "cursor-index", "brandon-bartram-custom-cursor"),
    ("timeline-camera-scrubber", "Timeline camera scrubber", "Scroll aid", "Portfolio", "A vertical timeline scrubs camera states and shows exactly where the viewer is.", ["timeline", "camera", "scrubber", "scroll", "portfolio"], "camera-timeline", "joseph-santamaria-camera-path"),
    ("glassmorphic-audio-reactor", "Glassmorphic audio reactor", "Audio visual", "Media", "Glass panels react to audio bands with depth and restrained glow.", ["audio", "glass", "reactive", "media", "visualizer"], "audio-reactor", "creative-audio-visualizer"),
    ("ai-map-of-thought", "AI map-of-thought", "Agent viz", "AI app", "An AI answer appears as a map of claims, sources, uncertainty, and next actions.", ["ai", "agent", "map", "sources", "reasoning"], "thought-map", "ai-product-agent-map"),
    ("spatial-command-room", "Spatial command room", "Command", "AI app", "Commands live on walls of a compact 3D room instead of a flat palette.", ["command", "spatial", "3d", "keyboard", "ai"], "command-room", "creative-command-palette-3d"),
    ("liquid-drag-dashboard", "Liquid drag dashboard", "Dashboard motion", "Dashboard", "Widgets stretch and reflow like liquid while preserving dashboard clarity.", ["dashboard", "drag", "liquid", "layout", "motion"], "liquid-dashboard", "dashboard-motion-inspiration"),

    # Aave Glass / Codrops GSAP+WebGL reference pass
    ("aave-glass-switch-lens", "Aave glass switch lens", "Glass control", "Web app", "A moving refraction lens becomes the switch thumb while preserving readable content.", ["aave-glass", "refraction", "svg-filter", "switch", "glass"], "aave-glass", "aave-building-glass-for-the-web"),
    ("aave-glass-slider-refraction", "Aave glass slider refraction", "Glass control", "Web app", "A slider handle bends only the fill region with a conservative high-performance lens.", ["aave-glass", "slider", "refraction", "performance", "glass"], "aave-slider", "aave-building-glass-for-the-web"),
    ("aave-glass-toggle-group", "Aave glass toggle group", "Glass selection", "Web app", "Selection is a springing glass lens, not another background pill.", ["aave-glass", "toggle", "selection", "spring", "glass"], "aave-toggle", "aave-building-glass-for-the-web"),
    ("aave-glass-video-controls", "Aave glass video controls", "Glass media", "Media", "Independent glass control lenses float over moving video without destroying legibility.", ["aave-glass", "video", "webgl", "controls", "refraction"], "aave-video", "aave-building-glass-for-the-web"),
    ("codrops-webgl-scroll-gallery", "WebGL scroll-revealed gallery", "Shader gallery", "Portfolio", "Images reveal with shader masks on scroll, then expand into a detail transition.", ["codrops", "webgl", "gsap", "scrolltrigger", "barba", "gallery"], "webgl-scroll-gallery", "codrops-scroll-revealed-webgl-gallery"),
    ("gsap-flip-detail-expander", "GSAP Flip detail expander", "Transition", "Portfolio", "A thumbnail keeps continuity as it flips into a full case-study scene.", ["gsap", "flip", "page-transition", "case-study", "portfolio"], "flip-expander", "codrops-gsap-flip-scrolltrigger"),
    ("scroll-driven-3d-world-chapters", "Scroll-driven 3D world chapters", "3D scene", "Portfolio", "Every scroll chapter moves the viewer through an authored 3D world with a point of view.", ["three-js", "gsap", "scroll", "world", "camera"], "world-chapters", "codrops-scroll-driven-3d-world"),
    ("video-texture-cube-grid", "Video texture cube grid", "WebGL grid", "Portfolio", "Video frames map onto rotating cube tiles with mask-driven hover states.", ["three-js", "video-texture", "cube-grid", "webgl", "hover"], "video-cube-grid", "codrops-threejs-video-cube-grid"),

]

BASE_CSS = r'''
:root{color-scheme:dark;--bg:#07080b;--ink:#fff8ea;--muted:#aab0bd;--line:rgba(255,255,255,.14);--a:#8fffe0;--b:#ffcf5a;--c:#ff6a88;--d:#8aa8ff;--panel:rgba(255,255,255,.065)}*{box-sizing:border-box}body{margin:0;min-height:100vh;background:#07080b;color:var(--ink);font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;overflow:hidden}.frame{min-height:100vh;padding:18px;display:grid;place-items:center;background:radial-gradient(circle at 20% 18%,rgba(143,255,224,.16),transparent 28%),radial-gradient(circle at 86% 74%,rgba(255,106,136,.14),transparent 28%),linear-gradient(135deg,#07080b,#111521 58%,#120d08)}.specimen{width:min(780px,100%);height:min(460px,calc(100vh - 36px));border:1px solid var(--line);border-radius:30px;background:linear-gradient(145deg,rgba(255,255,255,.09),rgba(255,255,255,.028));box-shadow:0 34px 90px rgba(0,0,0,.45);overflow:hidden;position:relative}.bar{height:48px;display:flex;gap:8px;align-items:center;padding:0 16px;border-bottom:1px solid var(--line);background:rgba(0,0,0,.22);backdrop-filter:blur(20px)}.dot{width:9px;height:9px;border-radius:50%;background:#5f6878}.dot:nth-child(1){background:var(--c)}.dot:nth-child(2){background:var(--b)}.dot:nth-child(3){background:var(--a)}.label{margin-left:auto;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.12em}.stage{position:absolute;inset:48px 0 0;padding:24px}.chip{display:inline-flex;gap:6px;align-items:center;padding:7px 10px;border:1px solid var(--line);border-radius:999px;background:rgba(255,255,255,.08);font-size:12px;color:var(--muted)}h1,h2,h3,p{margin:0}.muted{color:var(--muted)}button{font:inherit;color:inherit;border:1px solid var(--line);background:rgba(255,255,255,.08);border-radius:999px;padding:9px 13px}.grain:after{content:'';position:absolute;inset:0;pointer-events:none;opacity:.16;background-image:radial-gradient(circle at 25% 30%,#fff 0 1px,transparent 1px);background-size:4px 4px;mix-blend-mode:overlay}@media(max... [truncated]
'''

def esc(s): return html.escape(str(s), quote=True)

TEMPLATES = {}
def template(name):
    def wrap(fn): TEMPLATES[name] = fn; return fn
    return wrap

@template("motion")
def t_motion(p):
    css = ".cinema{height:100%;perspective:900px;position:relative}.plane{position:absolute;inset:auto;border:1px solid var(--line);border-radius:26px;background:linear-gradient(135deg,rgba(143,255,224,.12),rgba(138,168,255,.08));box-shadow:0 24px 70px rgba(0,0,0,.35);animation:cam 7s ease-in-out infinite}.p1{left:4%;top:10%;width:48%;height:58%;transform:translateZ(80px) rotateY(-18deg)}.p2{right:8%;top:24%;width:42%;height:48%;animation-delay:-2s}.p3{left:28%;bottom:8%;width:50%;height:24%;animation-delay:-4s}.caption{position:absolute;left:28px;bottom:26px;max-width:420px}.caption h1{font-size:46px;line-height:.86;letter-spacing:-.07em}@keyframes cam{50%{transform:translate3d(24px,-18px,120px) rotateY(14deg) rotateX(4deg)}}"
    html_ = f"<div class='cinema grain'><div class='plane p1'></div><div class='plane p2'></div><div class='plane p3'></div><div class='caption'><span class='chip'>scroll-directed scene</span><h1>{esc(p['title'])}</h1><p class='muted'>{esc(p['description'])}</p></div></div>"
    return css, html_, ""

@template("type-dissolve")
def t_type(p):
    css = ".type{height:100%;display:grid;place-items:center;text-align:center}.word{font-size:clamp(50px,13vw,122px);font-weight:900;letter-spacing:-.11em;line-height:.78;position:relative;text-transform:uppercase}.word span{display:inline-block;animation:dust 2.2s ease-in-out infinite;animation-delay:calc(var(--i)*50ms)}.word:after{content:'';position:absolute;inset:-20%;background:radial-gradient(circle,var(--a),transparent 34%);filter:blur(24px);opacity:.25;z-index:-1}@keyframes dust{35%{transform:translateY(-18px) rotate(8deg);filter:blur(3px);opacity:.28}70%{transform:none;filter:none;opacity:1}}"
    letters = ''.join(f"<span style='--i:{i}'>{esc(ch)}</span>" for i,ch in enumerate('DISSOLVE'))
    return css, f"<div class='type'><div><div class='word'>{letters}</div><p class='muted'>{esc(p['description'])}</p></div></div>", ""

@template("ripple-grid")
def t_ripple(p):
    css = ".grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;height:100%}.tile{border:1px solid var(--line);border-radius:24px;background:radial-gradient(circle at var(--x,50%) var(--y,50%),rgba(143,255,224,.55),rgba(138,168,255,.12) 32%,rgba(255,255,255,.05));transition:transform .25s,filter .25s;overflow:hidden;position:relative}.tile:before{content:'';position:absolute;inset:-40%;background:repeating-radial-gradient(circle,rgba(255,255,255,.22) 0 1px,transparent 2px 12px);animation:ripple 5s linear infinite}.tile:hover{transform:scale(1.04) rotate(.8deg);filter:saturate(1.4)}@keyframes ripple{to{transform:translate(18%,12%) rotate(1turn)}}"
    js = "document.querySelectorAll('.tile').forEach(t=>t.onpointermove=e=>{let r=t.getBoundingClientRect();t.style.setProperty('--x',((e.clientX-r.left)/r.width*100)+'%');t.style.setProperty('--y',((e.clientY-r.top)/r.height*100)+'%')})"
    return css, "<div class='grid'>"+''.join("<div class='tile'></div>" for _ in range(9))+"</div>", js

@template("orbit-stage")
def t_orbit(p):
    css = ".orbit{height:100%;display:grid;place-items:center;position:relative}.core{width:170px;height:170px;border-radius:40px;background:linear-gradient(135deg,var(--a),var(--d));box-shadow:0 0 60px rgba(143,255,224,.28);animation:core 5s ease-in-out infinite}.sat{position:absolute;width:142px;padding:13px;border:1px solid var(--line);border-radius:20px;background:rgba(255,255,255,.08);backdrop-filter:blur(14px);animation:orb 8s linear infinite;transform-origin:calc(50% + var(--rx)) calc(50% + var(--ry))}.sat:nth-child(2){--rx:190px;--ry:0px}.sat:nth-child(3){--rx:-160px;--ry:70px;animation-delay:-2.6s}.sat:nth-child(4){--rx:80px;--ry:-150px;animation-delay:-5.2s}@keyframes orb{to{rotate:1turn}}@keyframes core{50%{transform:translateY(-12px) rotateX(10deg)}}"
    return css, "<div class='orbit'><div class='core'></div><div class='sat'>Realtime mesh</div><div class='sat'>Agent state</div><div class='sat'>3D context</div></div>", ""

@template("refractive-pricing")
def t_pricing(p):
    css = ".plans{height:100%;display:grid;grid-template-columns:repeat(3,1fr);gap:14px;align-items:center}.plan{height:260px;border:1px solid var(--line);border-radius:28px;padding:20px;background:rgba(255,255,255,.06);position:relative;overflow:hidden}.plan:nth-child(2){height:310px;background:rgba(143,255,224,.08)}.plan:nth-child(2):after{content:'';position:absolute;inset:22px;border:1px solid rgba(255,255,255,.35);border-radius:50%;filter:blur(.2px);box-shadow:inset 0 0 24px rgba(255,255,255,.18),0 0 40px rgba(143,255,224,.22);animation:ring 4s linear infinite}.price{font-size:44px;font-weight:900;margin-top:80px}@keyframes ring{50%{transform:scale(1.15) rotate(8deg);border-radius:38% 62% 55% 45%}}"
    return css, "<div class='plans'><div class='plan'>Start<div class='price'>$19</div></div><div class='plan'>Studio<div class='price'>$49</div></div><div class='plan'>Scale<div class='price'>$99</div></div></div>", ""

@template("constellation")
def t_constellation(p):
    css = ".stars{height:100%;position:relative;overflow:hidden}.star{position:absolute;left:var(--x);top:var(--y);width:6px;height:6px;border-radius:50%;background:var(--a);box-shadow:0 0 18px var(--a);animation:twinkle 2s ease-in-out infinite alternate;animation-delay:calc(var(--i)*-.13s)}.cursor{position:absolute;left:50%;top:50%;width:120px;height:120px;border:1px solid rgba(143,255,224,.35);border-radius:50%;transform:translate(-50%,-50%);animation:drift 6s ease-in-out infinite}.title{position:absolute;left:26px;bottom:24px;right:26px}.title h2{font-size:42px;letter-spacing:-.06em}@keyframes twinkle{to{opacity:.35;transform:scale(.55)}}@keyframes drift{50%{transform:translate(-20%,-70%) scale(1.25)}}"
    stars = ''.join(f"<span class='star' style='--i:{i};--x:{(i*23)%96}%;--y:{(i*41)%88}%'></span>" for i in range(42))
    return css, f"<div class='stars'>{stars}<div class='cursor'></div><div class='title'><span class='chip'>ambient pointer field</span><h2>{esc(p['title'])}</h2></div></div>", ""

@template("slice-poster")
def t_slice(p):
    css = ".poster{height:100%;display:grid;grid-template-columns:repeat(6,1fr);gap:4px}.slice{background:linear-gradient(180deg,var(--a),var(--c));border-radius:18px;animation:slice 2.8s cubic-bezier(.2,.8,.2,1) infinite alternate;animation-delay:calc(var(--i)*80ms)}.copy{position:absolute;left:34px;bottom:30px}.copy h2{font-size:56px;line-height:.84;letter-spacing:-.08em}@keyframes slice{0%{clip-path:inset(0 0 82% 0)}45%{clip-path:inset(0 0 0 0)}100%{transform:translateY(calc(var(--i)*-7px));filter:hue-rotate(35deg)}}"
    return css, "<div class='poster'>"+''.join(f"<div class='slice' style='--i:{i}'></div>" for i in range(6))+f"</div><div class='copy'><h2>{esc(p['title'])}</h2></div>", ""

@template("liquid-cta")
def t_liquid_cta(p):
    css = ".wrap{height:100%;display:grid;place-items:center}.cta{font-size:34px;font-weight:900;padding:28px 46px;border-radius:999px;position:relative;overflow:hidden;background:#f6ead5;color:#0b0d12;box-shadow:0 26px 80px rgba(255,207,90,.16)}.cta:before{content:'';position:absolute;inset:-80%;background:radial-gradient(circle,var(--a),transparent 28%),radial-gradient(circle at 70% 40%,var(--c),transparent 24%);animation:flow 4s linear infinite;mix-blend-mode:multiply}.cta span{position:relative}.cta:hover:before{animation-duration:1.2s}@keyframes flow{to{transform:rotate(1turn)}}"
    return css, f"<div class='wrap'><button class='cta'><span>{esc(p['title'])}</span></button></div>", ""

@template("magnetic-menu")
def t_magnetic(p):
    css = ".menu{height:100%;display:grid;align-content:center;gap:4px}.item{font-size:clamp(36px,9vw,82px);font-weight:950;line-height:.9;letter-spacing:-.08em;border-bottom:1px solid var(--line);padding:8px 0;transition:.25s}.item:hover{letter-spacing:-.02em;color:var(--a);transform:translateX(24px)}.item small{font-size:12px;color:var(--muted);letter-spacing:.12em;text-transform:uppercase;margin-right:14px}"
    return css, "<div class='menu'>"+''.join(f"<div class='item'><small>0{i}</small>{x}</div>" for i,x in enumerate(['Index','Work','Lab','Contact'],1))+"</div>", ""

@template("liquid-dock")
def t_dock(p):
    css = ".dock{height:100%;display:grid;place-items:center}.rail{display:flex;gap:10px;padding:10px;border:1px solid var(--line);border-radius:30px;background:rgba(255,255,255,.08);position:relative}.icon{width:58px;height:58px;border-radius:22px;background:rgba(255,255,255,.08);display:grid;place-items:center;z-index:1;transition:.25s}.icon:hover{transform:translateY(-12px)}.rail:before{content:'';position:absolute;width:58px;height:58px;left:10px;top:10px;border-radius:22px;background:var(--a);animation:dock 5s infinite steps(4)}@keyframes dock{to{transform:translateX(272px)}}"
    return css, "<div class='dock'><div class='rail'>"+''.join(f"<div class='icon'>{i}</div>" for i in range(1,6))+"</div></div>", ""

@template("radial-command")
def t_radial(p):
    css = ".radial{height:100%;display:grid;place-items:center;position:relative}.center{width:150px;height:150px;border-radius:50%;background:linear-gradient(135deg,var(--a),var(--d));display:grid;place-items:center;color:#06100d;font-weight:900}.cmd{position:absolute;width:120px;padding:12px;border:1px solid var(--line);border-radius:18px;background:rgba(255,255,255,.08);text-align:center;animation:bloom 4s ease-in-out infinite;transform:rotate(var(--r)) translateX(190px) rotate(calc(var(--r) * -1))}@keyframes bloom{50%{transform:rotate(var(--r)) translateX(150px) rotate(calc(var(--r) * -1));background:rgba(143,255,224,.14)}}"
    return css, "<div class='radial'><div class='center'>⌘K</div>"+''.join(f"<div class='cmd' style='--r:{i*60}deg'>{x}</div>" for i,x in enumerate(['Ask','Create','Find','Ship','Debug','Share']))+"</div>", ""

@template("split-transition")
def t_split(p):
    css = ".split{height:100%;position:relative;display:grid;place-items:center}.panel{position:absolute;inset:0 50% 0 0;background:var(--a);animation:left 3s ease-in-out infinite}.panel.r{inset:0 0 0 50%;background:var(--c);animation:right 3s ease-in-out infinite}.title{z-index:2;color:#fff;font-size:44px;font-weight:900;mix-blend-mode:difference}@keyframes left{45%,60%{transform:translateX(-100%)}}@keyframes right{45%,60%{transform:translateX(100%)}}"
    return css, f"<div class='split'><div class='panel'></div><div class='panel r'></div><div class='title'>{esc(p['title'])}</div></div>", ""

@template("spotlight-menu")
def t_spotmenu(p):
    css = ".spotmenu{height:100%;position:relative;display:grid;align-content:center;gap:8px}.spotmenu:before{content:'';position:absolute;inset:0;background:radial-gradient(circle at 62% 42%,rgba(143,255,224,.45),transparent 22%);mix-blend-mode:screen;animation:spot 5s ease-in-out infinite}.link{font-size:56px;font-weight:900;letter-spacing:-.07em;position:relative;z-index:1;color:rgba(255,255,255,.44)}.link:hover{color:white}@keyframes spot{50%{background-position:30% 70%;filter:hue-rotate(80deg)}}"
    return css, "<div class='spotmenu'><div class='link'>Platform</div><div class='link'>Research</div><div class='link'>Motion</div><div class='link'>Contact</div></div>", ""

@template("map-accordion")
def t_mapacc(p):
    css = ".layout{display:grid;grid-template-columns:210px 1fr;gap:14px;height:100%}.acc{display:grid;gap:8px}.acc div{border:1px solid var(--line);border-radius:18px;padding:14px;background:rgba(255,255,255,.06)}.map{border:1px solid var(--line);border-radius:26px;position:relative;overflow:hidden;background:linear-gradient(135deg,#10251f,#0b1220)}.map:before{content:'';position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.07) 1px,transparent 1px);background-size:36px 36px}.pin{position:absolute;left:var(--x);top:var(--y);width:16px;height:16px;border-radius:50%;background:var(--a);box-shadow:0 0 0 0 rgba(143,255,224,.5);animation:pulse 2s infinite}@keyframes pulse{to{box-shadow:0 0 0 34px rgba(143,255,224,0)}}"
    return css, "<div class='layout'><div class='acc'><div>North route</div><div>Signal path</div><div>Depot</div></div><div class='map'><span class='pin' style='--x:62%;--y:38%'></span><span class='pin' style='--x:32%;--y:68%'></span></div></div>", ""

# A large family of data/product/editorial templates with reusable but distinct looks.
@template("dashboard-rows")
def t_rows(p):
    css = ".rows{display:grid;gap:10px}.row{display:grid;grid-template-columns:42px 1fr auto;gap:12px;align-items:center;padding:12px;border:1px solid var(--line);border-radius:18px;background:rgba(255,255,255,.06);opacity:0;transform:translateY(18px) scale(.98);animation:rise .65s cubic-bezier(.2,.8,.2,1) forwards;animation-delay:calc(var(--i)*80ms)}.sig{width:42px;height:42px;border-radius:16px;background:linear-gradient(135deg,var(--a),var(--d))}.score{color:var(--a)}@keyframes rise{to{opacity:1;transform:none}}"
    return css, "<div class='rows'>"+''.join(f"<div class='row' style='--i:{i}'><span class='sig'></span><b>Signal cluster {i+1}</b><span class='score'>{91-i*3}%</span></div>" for i in range(7))+"</div>", ""

@template("metric-scrub")
def t_metric(p):
    css = ".metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.metric{border:1px solid var(--line);border-radius:24px;padding:16px;background:rgba(255,255,255,.06)}.num{font-size:40px;font-weight:900}.scrub{margin-top:28px;height:12px;border-radius:999px;background:rgba(255,255,255,.1);position:relative}.scrub:before{content:'';position:absolute;inset:0 45% 0 0;border-radius:inherit;background:var(--a);animation:scrub 4s ease-in-out infinite}svg{width:100%;height:70px}.p{stroke:var(--a);fill:none;stroke-width:4;stroke-dasharray:170;animation:draw 2s infinite alternate}@keyframes draw{from{stroke-dashoffset:170}}@keyframes scrub{50%{right:12%}}"
    return css, "<div class='metrics'>"+''.join("<div class='metric'><div class='num'>+24%</div><svg viewBox='0 0 120 60'><path class='p' d='M2 48 C30 8 48 58 78 24 S100 14 118 10'/></svg></div>" for _ in range(3))+"</div><div class='scrub'></div>", ""

@template("evidence-peek")
def t_evidence(p):
    css = ".audit{display:grid;gap:10px}.item{border:1px solid var(--line);border-radius:20px;background:rgba(255,255,255,.06);padding:14px;overflow:hidden}.meta{max-height:0;color:var(--muted);transition:.35s}.item:hover .meta{max-height:110px;margin-top:10px}.chips{display:flex;gap:6px;margin-top:8px}.chips span{padding:5px 8px;border-radius:999px;background:rgba(143,255,224,.12);color:var(--a)}"
    return css, "<div class='audit'>"+''.join(f"<div class='item'><b>Decision event {i+1}</b><div class='meta'>Source confidence, owner, timestamp, and diff are exposed inline.<div class='chips'><span>source</span><span>fresh</span><span>reviewed</span></div></div></div>" for i in range(5))+"</div>", ""

@template("ai-stream")
def t_aistream(p):
    css = ".stream{display:grid;gap:10px}.msg{max-width:86%;padding:13px 15px;border:1px solid var(--line);border-radius:18px;background:rgba(255,255,255,.06);opacity:0;transform:translateY(12px);animation:msg .55s forwards;animation-delay:calc(var(--i)*260ms)}.msg:nth-child(even){margin-left:auto;background:rgba(143,255,224,.09)}.sources{display:flex;gap:6px;margin-top:9px}.sources span{font-size:11px;color:#06100d;background:var(--a);border-radius:999px;padding:4px 7px}@keyframes msg{to{opacity:1;transform:none}}"
    return css, "<div class='stream'>"+''.join(f"<div class='msg' style='--i:{i}'>{x}<div class='sources'><span>doc</span><span>{88+i}%</span></div></div>" for i,x in enumerate(['Analyze this dashboard','I found three interaction opportunities','Use source chips near the claim','Ready to patch the UI']))+"</div>", ""

@template("alert-lens")
def t_lens(p):
    css = ".board{height:100%;position:relative;border:1px solid var(--line);border-radius:26px;background:repeating-linear-gradient(0deg,rgba(255,255,255,.05) 0 1px,transparent 1px 44px)}.node{position:absolute;left:var(--x);top:var(--y);padding:10px 12px;border-radius:16px;background:rgba(255,255,255,.08)}.lens{position:absolute;width:180px;height:180px;border-radius:50%;left:42%;top:28%;border:1px solid rgba(143,255,224,.5);background:radial-gradient(circle,rgba(143,255,224,.18),transparent 70%);backdrop-filter:contrast(1.4) brightness(1.2);animation:lens 5s ease-in-out infinite}@keyframes lens{50%{transform:translate(-140px,70px) scale(1.08)}}"
    return css, "<div class='board'>"+''.join(f"<span class='node' style='--x:{(i*29)%78+5}%;--y:{(i*43)%70+8}%'>INC-{i+1}</span>" for i in range(8))+"<div class='lens'></div></div>", ""

@template("kanban-physics")
def t_kanban(p):
    css = ".board{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;height:100%}.lane{border:1px solid var(--line);border-radius:24px;padding:10px;background:rgba(255,255,255,.045)}.ticket{padding:13px;border-radius:18px;background:rgba(255,255,255,.08);margin-bottom:10px;transition:.25s;transform-origin:50% 110%}.ticket:hover{transform:translateY(-12px) rotate(-2deg);box-shadow:0 24px 40px rgba(0,0,0,.35);background:rgba(143,255,224,.16)}"
    return css, "<div class='board'>"+''.join("<div class='lane'><div class='ticket'>Design pass</div><div class='ticket'>Motion QA</div><div class='ticket'>Ship notes</div></div>" for _ in range(3))+"</div>", ""

@template("calendar-brush")
def t_calendar(p):
    css = ".cal{display:grid;grid-template-columns:70px repeat(5,1fr);gap:6px;height:100%}.slot{border:1px solid var(--line);border-radius:12px;background:rgba(255,255,255,.055);position:relative;overflow:hidden}.slot.busy:before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,var(--a),var(--d));opacity:.35}.slot:hover{outline:2px solid var(--a);transform:scale(1.04);z-index:2}.time{color:var(--muted);font-size:12px;display:grid;place-items:center}"
    cells=[]
    for r in range(6):
        cells.append(f"<div class='time'>{9+r}:00</div>")
        for c in range(5): cells.append(f"<div class='slot {'busy' if (r+c)%3==0 else ''}'></div>")
    return css, "<div class='cal'>"+''.join(cells)+"</div>", ""

@template("lineage-river")
def t_lineage(p):
    css = ".river{height:100%;position:relative}.node{position:absolute;left:var(--x);top:var(--y);padding:10px 13px;border-radius:999px;background:rgba(255,255,255,.09);border:1px solid var(--line)}svg{position:absolute;inset:0;width:100%;height:100%}.flow{stroke:var(--a);stroke-width:4;fill:none;stroke-dasharray:9 10;animation:flow 1s linear infinite}@keyframes flow{to{stroke-dashoffset:-19}}"
    return css, "<div class='river'><svg viewBox='0 0 700 360'><path class='flow' d='M50 180 C210 80 260 270 400 160 S560 70 650 180'/><path class='flow' d='M50 180 C220 230 330 220 640 300'/></svg><span class='node' style='--x:4%;--y:44%'>Source</span><span class='node' style='--x:48%;--y:34%'>Model</span><span class='node' style='--x:80%;--y:74%'>Alert</span></div>", ""

@template("radar-sweep")
def t_radar(p):
    css = ".radar{height:100%;display:grid;place-items:center}.scope{width:min(340px,80vw);height:min(340px,80vw);border-radius:50%;border:1px solid rgba(143,255,224,.4);background:repeating-radial-gradient(circle,rgba(143,255,224,.13) 0 1px,transparent 2px 52px);position:relative;overflow:hidden}.scope:before{content:'';position:absolute;inset:50% 0 0 50%;background:linear-gradient(80deg,rgba(143,255,224,.5),transparent 60%);transform-origin:0 0;animation:sweep 3s linear infinite}.blip{position:absolute;left:var(--x);top:var(--y);width:10px;height:10px;border-radius:50%;background:var(--c);box-shadow:0 0 22px var(--c)}@keyframes sweep{to{rotate:1turn}}"
    return css, "<div class='radar'><div class='scope'><span class='blip' style='--x:58%;--y:34%'></span><span class='blip' style='--x:32%;--y:64%'></span><span class='blip' style='--x:70%;--y:70%'></span></div></div>", ""

@template("shelf-pulse")
def t_shelf(p):
    css = ".shelves{display:grid;gap:10px}.shelf{display:grid;grid-template-columns:repeat(8,1fr);gap:6px;padding:12px;border:1px solid var(--line);border-radius:18px;background:rgba(255,255,255,.05)}.box{height:34px;border-radius:9px;background:rgba(255,255,255,.09)}.box.hot{background:var(--c);animation:pulse 1.3s infinite}@keyframes pulse{50%{transform:scale(1.18);box-shadow:0 0 24px var(--c)}}"
    return css, "<div class='shelves'>"+''.join("<div class='shelf'>"+''.join(f"<span class='box {'hot' if (i+j)%7==0 else ''}'></span>" for i in range(8))+"</div>" for j in range(6))+"</div>", ""

@template("filmstrip")
def t_filmstrip(p):
    css = ".strip{height:100%;display:flex;gap:14px;align-items:center;animation:strip 12s linear infinite}.case{flex:0 0 300px;height:260px;border:1px solid var(--line);border-radius:28px;background:linear-gradient(135deg,rgba(143,255,224,.18),rgba(255,106,136,.08));padding:18px;display:flex;flex-direction:column;justify-content:flex-end}.case:nth-child(even){transform:translateY(-28px)}@keyframes strip{to{transform:translateX(-628px)}}"
    return css, "<div class='strip'>"+''.join(f"<div class='case'><span class='chip'>Case {i}</span><h2>Project system</h2></div>" for i in range(1,7))*2+"</div>", ""

@template("stacked-cards")
def t_stack(p):
    css = ".stack{height:100%;position:relative}.card{position:absolute;left:8%;right:8%;top:calc(20px + var(--i)*42px);height:210px;border:1px solid var(--line);border-radius:28px;padding:22px;background:linear-gradient(135deg,rgba(255,255,255,.12),rgba(255,255,255,.04));transform:rotate(calc((var(--i) - 2)*-1.3deg));animation:stack 5s ease-in-out infinite;animation-delay:calc(var(--i)*-.4s)}@keyframes stack{50%{transform:translateY(-18px) rotate(calc((var(--i) - 2)*1deg))}}"
    return css, "<div class='stack'>"+''.join(f"<div class='card' style='--i:{i}'><span class='chip'>chapter {i+1}</span><h2>{esc(p['title'])}</h2></div>" for i in range(5))+"</div>", ""

@template("mask-proof")
def t_maskproof(p):
    css = ".quotes{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}.q{min-height:130px;border:1px solid var(--line);border-radius:24px;padding:18px;background:rgba(255,255,255,.06);clip-path:inset(0 100% 0 0);animation:unmask .9s forwards;animation-delay:calc(var(--i)*160ms)}@keyframes unmask{to{clip-path:inset(0)}}"
    return css, "<div class='quotes'>"+''.join(f"<div class='q' style='--i:{i}'><b>“This feels expensive.”</b><p class='muted'>Proof quote with calm motion.</p></div>" for i in range(6))+"</div>", ""

@template("depth-marquee")
def t_depthmarquee(p):
    css = ".wrap{display:grid;gap:16px;align-content:center;height:100%;mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent)}.track{display:flex;gap:12px;animation:mar 12s linear infinite}.track:nth-child(2){animation-duration:18s;animation-direction:reverse;opacity:.55}.logo{flex:0 0 160px;height:74px;border:1px solid var(--line);border-radius:20px;display:grid;place-items:center;background:rgba(255,255,255,.07)}@keyframes mar{to{transform:translateX(-50%)}}"
    row=''.join(f"<div class='logo'>LOGO {i}</div>" for i in range(1,7))*2
    return css, f"<div class='wrap'><div class='track'>{row}</div><div class='track'>{row}</div></div>", ""

@template("elastic-faq")
def t_faq(p):
    css = ".faq{display:grid;gap:10px}.qa{border:1px solid var(--line);border-radius:20px;background:rgba(255,255,255,.06);overflow:hidden}.q{padding:16px;display:flex;justify-content:space-between}.a{max-height:0;padding:0 16px;color:var(--muted);transition:.45s cubic-bezier(.2,1.4,.2,1)}.qa:hover .a{max-height:120px;padding-bottom:16px}.qa:hover .q span{rotate:45deg}.q span{transition:.25s}"
    return css, "<div class='faq'>"+''.join(f"<div class='qa'><div class='q'><b>Question {i+1}</b><span>＋</span></div><div class='a'>Answer opens with spring drawer behavior and clear hierarchy.</div></div>" for i in range(5))+"</div>", ""

@template("team-spotlight")
def t_team(p):
    css = ".team{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;height:100%;position:relative}.person{border:1px solid var(--line);border-radius:22px;background:radial-gradient(circle at 50% 34%,rgba(143,255,224,.35),transparent 24%),rgba(255,255,255,.06);filter:brightness(.75);transition:.25s}.person:hover{filter:brightness(1.25);transform:translateY(-6px)}"
    return css, "<div class='team'>"+''.join("<div class='person'></div>" for _ in range(12))+"</div>", ""

@template("stats-band")
def t_stats(p):
    css = ".stats{height:100%;display:grid;grid-template-columns:repeat(3,1fr);gap:12px;align-items:center}.stat{border:1px solid var(--line);border-radius:28px;padding:22px;background:rgba(255,255,255,.06)}.n{font-size:58px;font-weight:950;color:var(--a);counter-reset:num var(--v)}.n:after{content:counter(num)}.stat{animation:pop .8s cubic-bezier(.2,1.5,.2,1) both;animation-delay:calc(var(--i)*120ms)}@keyframes pop{from{opacity:0;transform:translateY(25px) scale(.9)}}"
    return css, "<div class='stats'>"+''.join(f"<div class='stat' style='--i:{i}'><div class='n' style='--v:{v}'></div><p class='muted'>proof metric</p></div>" for i,v in enumerate([42,87,12]))+"</div>", ""

@template("gravity-footer")
def t_footer(p):
    css = ".space{height:100%;position:relative}.planet{position:absolute;left:50%;top:50%;width:170px;height:170px;border-radius:50%;background:linear-gradient(135deg,var(--a),var(--d));transform:translate(-50%,-50%);display:grid;place-items:center;color:#07100d;font-weight:900}.link{position:absolute;left:50%;top:50%;transform:rotate(var(--r)) translateX(210px) rotate(calc(var(--r)*-1));animation:grav 5s ease-in-out infinite;animation-delay:calc(var(--i)*-.3s)}@keyframes grav{50%{translate:0 -18px}}"
    return css, "<div class='space'><div class='planet'>CTA</div>"+''.join(f"<span class='link' style='--r:{i*51}deg;--i:{i}'>Link</span>" for i in range(7))+"</div>", ""



@template("brush-shader")
def t_brush_shader(p):
    css = ".brush{height:100%;position:relative;display:grid;place-items:center;background:#050607;overflow:hidden}.canvas{width:72%;height:68%;border-radius:34px;position:relative;overflow:hidden;border:1px solid var(--line);background:linear-gradient(135deg,#10131d,#273746)}.canvas:before{content:'';position:absolute;inset:-18%;background:radial-gradient(circle at 24% 40%,var(--a),transparent 18%),radial-gradient(circle at 65% 44%,var(--c),transparent 20%),linear-gradient(135deg,transparent 20%,rgba(255,255,255,.3),transparent 62%);filter:blur(8px);clip-path:polygon(0 42%,18% 30%,38% 48%,58% 28%,80% 44%,100% 34%,100% 82%,0 92%);animation:paint 3.4s cubic-bezier(.2,.8,.2,1) infinite}.canvas:after{content:'';position:absolute;inset:0;background:repeating-linear-gradient(100deg,transparent 0 13px,rgba(255,255,255,.08) 14px 15px);mix-blend-mode:overlay}.caption{position:absolute;left:28px;bottom:24px;right:28px}.caption h2{font-size:48px;line-height:.86;letter-spacing:-.08em}@keyframes paint{0%,12%{clip-path:polygon(0 48%,5% 44%,10% 50%,14% 46%,18% 52%,20% 50%,20% 92%,0 92%)}70%,100%{clip-path:polygon(0 42%,18% 30%,38% 48%,58% 28%,80% 44%,100% 34%,100% 82%,0 92%)}}"
    return css, f"<div class='brush'><div class='canvas'></div><div class='caption'><span class='chip'>hover shader mask</span><h2>{esc(p['title'])}</h2></div></div>", ""

@template("corridor-scroll")
def t_corridor(p):
    css = ".corridor{height:100%;perspective:900px;position:relative;overflow:hidden}.card{position:absolute;left:50%;top:50%;width:220px;height:140px;margin:-70px 0 0 -110px;border:1px solid var(--line);border-radius:24px;background:linear-gradient(135deg,rgba(143,255,224,.14),rgba(138,168,255,.08));transform:translateZ(calc(var(--i)*-140px)) translateX(calc((var(--i) - 3)*44px)) rotateY(calc((var(--i) - 3)*-12deg));animation:drive 6s linear infinite;animation-delay:calc(var(--i)*-.75s)}.vanish{position:absolute;inset:0;background:radial-gradient(circle at 50% 50%,transparent 8%,rgba(7,8,11,.8) 78%)}.title{position:absolute;left:26px;bottom:24px;right:26px}.title h2{font-size:44px;line-height:.9;letter-spacing:-.08em}@keyframes drive{to{transform:translateZ(260px) translateX(calc((var(--i) - 3)*-24px)) rotateY(calc((var(--i) - 3)*12deg));opacity:.05}}"
    return css, "<div class='corridor'>"+''.join(f"<div class='card' style='--i:{i}'></div>" for i in range(8))+f"<div class='vanish'></div><div class='title'><span class='chip'>physics scroll corridor</span><h2>{esc(p['title'])}</h2></div></div>", ""

@template("scene-room")
def t_scene_room(p):
    css = ".room{height:100%;perspective:900px;display:grid;place-items:center;overflow:hidden}.cube{width:260px;height:190px;position:relative;transform-style:preserve-3d;animation:room 7s cubic-bezier(.65,0,.35,1) infinite}.face{position:absolute;inset:0;border:1px solid var(--line);border-radius:22px;background:rgba(255,255,255,.07);display:grid;place-items:center;font-weight:900}.front{transform:translateZ(120px);background:linear-gradient(135deg,var(--a),var(--d));color:#06100d}.left{transform:rotateY(-90deg) translateZ(130px)}.right{transform:rotateY(90deg) translateZ(130px)}.floor{transform:rotateX(90deg) translateZ(-100px);background:rgba(255,207,90,.09)}@keyframes room{0%,18%{transform:rotateX(-8deg) rotateY(-24deg) translateZ(0)}42%,58%{transform:rotateX(6deg) rotateY(42deg) translateZ(80px)}82%,100%{transform:rotateX(-16deg) rotateY(180deg) translateZ(-30px)}}"
    return css, "<div class='room'><div class='cube'><div class='face front'>Scene</div><div class='face left'>Work</div><div class='face right'>Lab</div><div class='face floor'>Camera path</div></div></div>", ""

@template("water-transition")
def t_water_transition(p):
    css = ".water{height:100%;display:grid;place-items:center;position:relative;overflow:hidden}.page{width:68%;height:62%;border-radius:30px;border:1px solid var(--line);background:linear-gradient(135deg,#f5e9ce,#8fffe0);color:#10131d;display:grid;place-items:center;font-size:42px;font-weight:950;letter-spacing:-.08em}.wave{position:absolute;inset:-30%;background:repeating-radial-gradient(circle at 50% 50%,rgba(143,255,224,.35) 0 2px,transparent 4px 24px);filter:url(#none) blur(1px);mix-blend-mode:screen;animation:wave 3.2s ease-in-out infinite}@keyframes wave{50%{transform:scale(.72) rotate(18deg);border-radius:42%;filter:blur(8px)}}"
    return css, f"<div class='water'><div class='page'>Next case</div><div class='wave'></div></div>", ""

@template("procedural-loader")
def t_proc_loader(p):
    css = ".loader{height:100%;display:grid;place-items:center}.mark{width:260px;height:180px}.path{fill:none;stroke:var(--a);stroke-width:6;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:620;animation:draw 3.2s cubic-bezier(.2,.8,.2,1) infinite}.word{font-size:42px;font-weight:950;letter-spacing:-.08em;opacity:0;animation:word 3.2s infinite}@keyframes draw{0%{stroke-dashoffset:620}45%,70%{stroke-dashoffset:0}100%{stroke-dashoffset:-620}}@keyframes word{48%,72%{opacity:1;transform:translateY(0)}0%,100%{opacity:0;transform:translateY(16px)}}"
    return css, "<div class='loader'><svg class='mark' viewBox='0 0 320 220'><path class='path' d='M40 160 C80 30 142 30 160 120 S242 214 282 58'/><text class='word' x='66' y='195' fill='white'>Frame</text></svg></div>", ""

@template("canvas-handoff")
def t_canvas_handoff(p):
    css = ".handoff{height:100%;display:grid;place-items:center;position:relative}.dom{width:280px;height:180px;border-radius:28px;background:#fff8ea;color:#07080b;padding:22px;font-weight:900;box-shadow:0 30px 80px rgba(0,0,0,.35);animation:detach 4.4s cubic-bezier(.2,.8,.2,1) infinite}.ghost{position:absolute;width:280px;height:180px;border-radius:28px;border:1px solid var(--a);filter:blur(.2px);animation:ghost 4.4s infinite}@keyframes detach{42%,65%{transform:translate(-120px,-24px) rotateY(-24deg) scale(.9);opacity:.42}100%{transform:none}}@keyframes ghost{0%,30%{opacity:0;transform:translate(0)}45%,70%{opacity:1;transform:translate(120px,18px) rotateY(22deg)}100%{opacity:0;transform:translate(170px,40px) scale(.8)}}"
    return css, "<div class='handoff'><div class='dom'>DOM card<br><span class='muted'>becomes canvas</span></div><div class='ghost'></div></div>", ""

@template("cloud-water")
def t_cloud_water(p):
    css = ".sky{height:100%;position:relative;display:grid;place-items:center;overflow:hidden}.sky:before,.sky:after{content:'';position:absolute;inset:-30%;background:radial-gradient(ellipse at 30% 40%,rgba(143,255,224,.35),transparent 30%),radial-gradient(ellipse at 70% 55%,rgba(138,168,255,.28),transparent 30%);filter:blur(20px);animation:cloud 8s ease-in-out infinite}.sky:after{background:repeating-linear-gradient(100deg,transparent 0 22px,rgba(255,255,255,.08) 23px 26px);animation-duration:5s}.sky h2{position:relative;font-size:58px;line-height:.84;letter-spacing:-.1em;text-align:center;max-width:560px}@keyframes cloud{50%{transform:translate(8%,-5%) rotate(10deg) scale(1.12)}}"
    return css, f"<div class='sky'><h2>{esc(p['title'])}</h2></div>", ""

@template("project-world")
def t_project_world(p):
    css = ".world{height:100%;position:relative;overflow:hidden}.track{display:flex;gap:18px;position:absolute;left:24px;right:auto;top:84px;animation:pan 8s linear infinite}.project{width:220px;height:250px;border:1px solid var(--line);border-radius:28px;background:linear-gradient(135deg,rgba(255,255,255,.09),rgba(143,255,224,.08));padding:18px;display:flex;flex-direction:column;justify-content:flex-end;box-shadow:0 calc(var(--i)*8px) 40px rgba(0,0,0,.28);transform:translateY(calc(var(--i)*10px))}.horizon{position:absolute;left:0;right:0;bottom:70px;height:1px;background:var(--line)}@keyframes pan{to{transform:translateX(-480px)}}"
    return css, "<div class='world'><div class='horizon'></div><div class='track'>"+''.join(f"<div class='project' style='--i:{i%4}'><span class='chip'>case 0{i+1}</span><h3>Motion system</h3></div>" for i in range(8))+"</div></div>", ""

@template("canvas-puzzle")
def t_canvas_puzzle(p):
    css = ".puzzle{height:100%;display:grid;grid-template-columns:repeat(5,1fr);gap:8px;align-content:center}.piece{height:70px;border-radius:18px;background:linear-gradient(135deg,var(--a),var(--d));animation:puzzle 3s ease-in-out infinite;animation-delay:calc(var(--i)*70ms)}.piece:nth-child(3n){background:linear-gradient(135deg,var(--c),var(--b))}@keyframes puzzle{35%{transform:translateY(-20px) rotate(8deg);border-radius:45% 30% 50% 25%}70%{transform:translateX(10px) scale(.9)}}"
    return css, "<div class='puzzle'>"+''.join(f"<div class='piece' style='--i:{i}'></div>" for i in range(25))+"</div>", ""

@template("portal-case")
def t_portal_case(p):
    css = ".portal{height:100%;display:grid;place-items:center;position:relative}.ring{width:280px;height:280px;border-radius:45% 55% 52% 48%;border:2px solid rgba(143,255,224,.55);box-shadow:inset 0 0 40px rgba(143,255,224,.18),0 0 80px rgba(143,255,224,.18);background:radial-gradient(circle,rgba(255,255,255,.18),transparent 60%);animation:portal 4s ease-in-out infinite}.case{position:absolute;padding:18px 24px;border-radius:24px;background:#fff8ea;color:#07080b;font-weight:900;animation:case 4s ease-in-out infinite}@keyframes portal{50%{transform:rotate(16deg) scale(1.08);border-radius:55% 45% 38% 62%}}@keyframes case{50%{transform:translateZ(0) scale(1.18);filter:blur(.4px)}}"
    return css, "<div class='portal'><div class='ring'></div><div class='case'>Open case study</div></div>", ""

@template("noise-nav")
def t_noise_nav(p):
    css = ".nav{height:100%;display:grid;align-content:center;gap:6px}.nav div{font-size:58px;font-weight:950;letter-spacing:-.09em;line-height:.86;position:relative;overflow:hidden}.nav div:after{content:attr(data-t);position:absolute;inset:0;color:var(--a);clip-path:inset(0 100% 0 0);filter:blur(1px);animation:scan 3s ease-in-out infinite;animation-delay:calc(var(--i)*-.35s)}@keyframes scan{50%{clip-path:inset(0 0 0 0);transform:translateX(18px) skewX(-8deg)}100%{clip-path:inset(0 0 0 100%)}}"
    return css, "<div class='nav'>"+''.join(f"<div data-t='{x}' style='--i:{i}'>{x}</div>" for i,x in enumerate(['Index','Selected','Process','Contact']))+"</div>", ""

@template("model-exploder")
def t_model_exploder(p):
    css = ".explode{height:100%;display:grid;place-items:center;position:relative}.layer{position:absolute;width:230px;height:90px;border:1px solid var(--line);border-radius:26px;background:rgba(255,255,255,.08);display:grid;place-items:center;animation:explode 5s cubic-bezier(.2,.8,.2,1) infinite;animation-delay:calc(var(--i)*120ms)}@keyframes explode{0%,18%,100%{transform:translateY(0) rotateX(0);opacity:.9}50%,70%{transform:translateY(calc((var(--i) - 2)*58px)) translateX(calc((var(--i) - 2)*22px)) rotateX(54deg);opacity:1;background:rgba(143,255,224,.13)}}"
    return css, "<div class='explode'>"+''.join(f"<div class='layer' style='--i:{i}'>Layer {i+1}</div>" for i in range(5))+"</div>", ""

@template("thought-map")
def t_thought_map(p):
    css = ".map{height:100%;position:relative}.node{position:absolute;left:var(--x);top:var(--y);padding:11px 13px;border:1px solid var(--line);border-radius:18px;background:rgba(255,255,255,.07);animation:pulse 3s infinite;animation-delay:calc(var(--i)*-.2s)}svg{position:absolute;inset:0;width:100%;height:100%;stroke:rgba(143,255,224,.45);fill:none;stroke-width:2;stroke-dasharray:8 10;animation:flow 8s linear infinite}@keyframes flow{to{stroke-dashoffset:-180}}@keyframes pulse{50%{box-shadow:0 0 30px rgba(143,255,224,.16);transform:translateY(-4px)}}"
    nodes=[('Claim',42,16),('Source',10,45),('Risk',58,50),('Next',30,74),('Action',74,24)]
    return css, "<div class='map'><svg viewBox='0 0 100 100'><path d='M48 22 C32 35 24 43 18 50 M50 28 C58 38 62 46 66 56 M45 30 C40 54 39 66 38 78 M58 28 C70 24 76 26 82 32'/></svg>"+''.join(f"<div class='node' style='--i:{i};--x:{x}%;--y:{y}%'>{t}</div>" for i,(t,x,y) in enumerate(nodes))+"</div>", ""

@template("command-room")
def t_command_room(p):
    css = ".roomcmd{height:100%;perspective:800px;display:grid;place-items:center}.wall{width:390px;height:250px;border:1px solid var(--line);border-radius:30px;background:rgba(255,255,255,.06);transform:rotateX(12deg) rotateY(-18deg);display:grid;grid-template-columns:repeat(2,1fr);gap:12px;padding:18px;box-shadow:30px 34px 80px rgba(0,0,0,.32);animation:float 5s ease-in-out infinite}.cmd{border-radius:20px;background:rgba(143,255,224,.1);display:grid;place-items:center;font-weight:800}.cmd:nth-child(2){background:rgba(255,106,136,.13)}@keyframes float{50%{transform:rotateX(4deg) rotateY(20deg) translateY(-12px)}}"
    return css, "<div class='roomcmd'><div class='wall'><div class='cmd'>Ask</div><div class='cmd'>Patch</div><div class='cmd'>Review</div><div class='cmd'>Ship</div></div></div>", ""

@template("liquid-dashboard")
def t_liquid_dashboard(p):
    css = ".dash{height:100%;display:grid;grid-template-columns:1.2fr .8fr;grid-template-rows:1fr 1fr;gap:12px}.widget{border:1px solid var(--line);border-radius:30px;background:rgba(255,255,255,.07);position:relative;overflow:hidden;animation:liq 5s ease-in-out infinite;animation-delay:calc(var(--i)*-.5s)}.widget:before{content:'';position:absolute;inset:-60%;background:radial-gradient(circle,var(--a),transparent 22%),radial-gradient(circle at 80% 30%,var(--c),transparent 18%);opacity:.22;animation:spin 6s linear infinite}.widget:first-child{grid-row:span 2}@keyframes liq{50%{border-radius:42% 24% 38% 28%;transform:scale(.98)}}@keyframes spin{to{transform:rotate(1turn)}}"
    return css, "<div class='dash'>"+''.join(f"<div class='widget' style='--i:{i}'></div>" for i in range(3))+"</div>", ""

# Alias many templates to a strong fallback with labels still differentiating the card.
ALIASES = {
    "search-morph":"radial-command", "onboard-stars":"constellation", "pricing-pressure":"refractive-pricing", "living-label":"liquid-cta", "empty-orbit":"orbit-stage", "copy-sweep":"liquid-cta", "card-marquee":"depth-marquee", "roller-blind":"slice-poster", "prism-carousel":"orbit-stage", "line-map":"map-accordion", "noise-gradient":"constellation", "pixel-dissolve":"type-dissolve", "progress-rail":"dashboard-rows", "clip-gallery":"ripple-grid", "audio-loader":"stats-band", "morph-divider":"slice-poster", "comparison-wipe":"split-transition", "annotation-rail":"ai-stream", "completion-burst":"constellation", "depth-bento":"ripple-grid", "title-loader":"type-dissolve", "device-morph":"split-transition", "cluster-map":"map-accordion", "toggle-array":"dashboard-rows", "column-xray":"evidence-peek", "video-scrub":"filmstrip", "type-3d":"type-dissolve", "gen-controls":"constellation", "size-magnet":"kanban-physics", "code-stepper":"ai-stream", "vault-door":"split-transition", "agent-trace":"lineage-river", "masonry-recompose":"ripple-grid", "kinetic-text":"magnetic-menu", "micro-charts":"metric-scrub", "doc-shadows":"dashboard-rows", "spotlight-type":"spotlight-menu", "depth-stack":"orbit-stage", "particle-logo":"constellation", "cursor-index":"spotlight-menu", "camera-timeline":"dashboard-rows", "audio-reactor":"stats-band", "aave-glass":"refractive-pricing", "aave-slider":"refractive-pricing", "aave-toggle":"liquid-dock", "aave-video":"refractive-pricing", "webgl-scroll-gallery":"ripple-grid", "flip-expander":"canvas-handoff", "world-chapters":"scene-room", "video-cube-grid":"ripple-grid"
}

def build_index(p):
    key = p[6]
    tpl_key = key if key in TEMPLATES else ALIASES.get(key, "motion")
    obj = {"slug":p[0],"title":p[1],"behavior":p[2],"context":p[3],"description":p[4],"tags":p[5],"template":key}
    css, body, js = TEMPLATES[tpl_key](obj)
    return f"""<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>{esc(p[1])} — Framewell live effect</title><style>{BASE_CSS}\n{css}</style></head><body><div class=\"frame\"><main class=\"specimen\" aria-label=\"{esc(p[1])}\"><div class=\"bar\"><span class=\"dot\"></span><span class=\"dot\"></span><span class=\"dot\"></span><span class=\"label\">{esc(p[2])} · {esc(p[3])}</span></div><section class=\"stage\">{body}</section></main></div>{('<script>'+js+'</script>') if js else ''}</body></html>"""

def prompt_for(title, desc, behavior, context, tags):
    return f"Adapt the Framewell pattern '{title}' into my existing {context} without replacing my product structure. Use it only as a focused {behavior} layer. {desc} Preserve my design tokens, data model, accessibility, keyboard behavior, reduced-motion preferences, and component architecture. Tags: {', '.join(tags)}."

def main():
    PATTERN_DIR.mkdir(exist_ok=True)
    # Remove old generated pattern folders so generic starters disappear.
    for child in PATTERN_DIR.iterdir():
        if child.is_dir() and (child / "meta.json").exists():
            for f in child.iterdir(): f.unlink()
            child.rmdir()
    out=[]
    seen=set()
    for i,p in enumerate(PATTERNS):
        slug,title,behavior,context,desc,tags,template_key,source = p
        DROP_GENERIC = {
            "faq-elastic-drawer", "team-spotlight-grid", "footer-gravity-links", "logo-cloud-depth-marquee",
            "stats-countup-proof-band", "mask-reveal-testimonials", "infinite-marquee-cards", "audio-wave-loader",
            "morphing-section-divider", "task-completion-confetti-minimal", "scroll-shadow-document",
            "form-field-living-label", "copy-button-success-sweep", "empty-state-suggestion-orbit"
        }
        if slug in DROP_GENERIC:
            continue
        if slug in seen: raise SystemExit(f"duplicate slug: {slug}")
        seen.add(slug)
        folder=PATTERN_DIR/slug; folder.mkdir(parents=True, exist_ok=True)
        code=build_index(p)
        prompt=prompt_for(title,desc,behavior,context,tags)
        featured = i < 36 or any(t in tags for t in ["shader", "three-js", "webgl", "webgpu", "canvas", "portal", "corridor", "camera", "scrolltrigger"])
        meta={"id":slug,"title":title,"behavior":behavior,"context":context,"description":desc,"tags":tags,"sourcePromptIds":[source],"template":template_key,"quality":"featured" if featured else "specimen","mixRoles":role_for(behavior, tags)}
        (folder/"index.html").write_text(code)
        (folder/"prompt.md").write_text(prompt+"\n")
        (folder/"meta.json").write_text(json.dumps(meta,indent=2)+"\n")
        out.append({**meta,"slug":slug,"previewUrl":f"patterns/{slug}/index.html","prompt":prompt,"code":code,"complexity":"advanced" if any(t in tags for t in ["webgl","three-js","gsap","shader"]) else "medium","dependencies":[]})
    summary={"count":len(out),"featured":sum(x["quality"]=="featured" for x in out),"specimens":sum(x["quality"]=="specimen" for x in out),"archiveMode":"hidden; live effects are primary"}
    DATA_PATH.write_text(json.dumps({"summary":summary,"patterns":out},indent=2)+"\n")
    print(f"wrote {len(out)} curated live effects to {DATA_PATH.relative_to(ROOT)}")

def role_for(behavior,tags):
    txt=' '.join([behavior,*tags]).lower()
    roles=[]
    if any(x in txt for x in ['hero','ambient','3d','webgl','webgpu','shader','typography','corridor','portal','camera','canvas','transition','particle','model','water']): roles.append('signature moment')
    if any(x in txt for x in ['dashboard','table','data','chart','metric','audit','agent','reasoning']): roles.append('product surface')
    if any(x in txt for x in ['menu','navigation','command','search','cursor','timeline']): roles.append('navigation/control')
    if any(x in txt for x in ['proof','pricing','testimonial','logo','stats']): roles.append('conversion/proof')
    if any(x in txt for x in ['microinteraction','button','copy','form','toggle','loader','audio']): roles.append('microinteraction')
    return roles or ['supporting effect']

if __name__ == "__main__":
    main()
