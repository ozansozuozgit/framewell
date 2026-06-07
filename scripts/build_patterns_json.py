#!/usr/bin/env python3
"""Build Framewell live pattern catalog and static iframe previews."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERN_DIR = ROOT / "patterns"
DATA_PATH = ROOT / "data" / "patterns.json"

PATTERNS = [
    ("scroll-row-reveal", "Scroll row reveal", "Reveal", "Dashboard", "Rows lift into place as a dense activity feed enters the viewport.", ["scroll", "dashboard", "feed", "intersection-observer"], "opencodesign-ai-ops-command-center"),
    ("sticky-metric-strip", "Sticky metric strip", "Navigate", "Dashboard", "A compact KPI strip pins while panels move underneath.", ["sticky", "metrics", "dashboard", "status"], "opencodesign-saas-revenue-dashboard"),
    ("audit-row-expand", "Audit row expansion", "Details", "Dashboard", "Dense table rows open into evidence without leaving the table.", ["table", "expand", "audit", "details"], "opencodesign-observability-dashboard"),
    ("hover-source-peek", "Hover source peek", "Inspect", "Dashboard", "Metadata slides in only when the user needs provenance.", ["hover", "metadata", "source", "provenance"], "opencodesign-design-token-inspector"),
    ("command-palette-orbit", "Command palette orbit", "Navigate", "AI app", "A soft command surface with orbiting shortcut chips.", ["command", "keyboard", "ai", "overlay"], "template-shadcnstore-chat-support-console"),
    ("segmented-filter-morph", "Segmented filter morph", "Filter", "SaaS app", "Filter pills share one moving active background.", ["filter", "tabs", "morph", "controls"], "template-shadcnstore-analytics-command-center"),
    ("bento-card-tilt", "Bento card tilt", "Emphasize", "Marketing", "Feature cards react to pointer position without looking gamey.", ["bento", "hover", "feature", "tilt"], "tailark-feature-bento-grid"),
    ("glass-sidebar-rail", "Glass sidebar rail", "Navigate", "Dashboard", "A translucent left rail reveals labels and active context.", ["sidebar", "glass", "navigation", "dashboard"], "opencodesign-finance-ops-dashboard"),
    ("timeline-scrubber", "Timeline scrubber", "Compare", "Analytics", "Milestones become a draggable-feeling horizontal timeline.", ["timeline", "analytics", "history", "scrub"], "opencodesign-creator-analytics-dashboard"),
    ("skeleton-signal-loader", "Signal skeleton loader", "Load", "Data app", "Loading rows shimmer with tiny source/signal placeholders.", ["loading", "skeleton", "data", "status"], "motionsites-loader-animation"),
    ("empty-next-actions", "Empty state next actions", "Empty", "SaaS app", "A zero state offers three concrete next moves instead of dead space.", ["empty-state", "onboarding", "actions", "cards"], "opencodesign-ai-notebook-waitlist"),
    ("pricing-toggle-proof", "Pricing toggle proof", "Convert", "Marketing", "Pricing cards animate proof points when billing mode changes.", ["pricing", "toggle", "proof", "saas"], "tailark-pricing-comparison"),
    ("logo-cloud-marquee", "Logo cloud marquee", "Proof", "Marketing", "A restrained logo belt loops with masked edges.", ["marquee", "logos", "social-proof", "motion"], "tailark-logo-cloud-marquee"),
    ("testimonial-wall-focus", "Testimonial wall focus", "Proof", "Marketing", "Hovering a quote lifts it while the wall stays calm.", ["testimonials", "hover", "proof", "grid"], "tailark-testimonial-wall"),
    ("faq-accordion-rhythm", "FAQ accordion rhythm", "Reveal", "Marketing", "Answers open with measured height and icon rotation.", ["faq", "accordion", "motion", "content"], "tailark-faq-accordion-section"),
    ("hero-word-rotation", "Hero word rotation", "Hero", "Landing page", "One hero noun rotates while the layout stays stable.", ["hero", "copy", "rotation", "landing"], "template-karthik-dark-saas-launch"),
    ("liquid-glass-card", "Liquid glass card", "Surface", "Marketing", "A glass panel uses gradient blur, shine, and parallax depth.", ["glass", "surface", "hero", "premium"], "motionsites-liquid-glass-agency"),
    ("particle-field-hero", "Particle field hero", "Ambient", "Landing page", "Tiny particles drift behind a product promise without stealing attention.", ["particle", "hero", "ambient", "canvas"], "opencodesign-particle-field-data-hero"),
    ("scroll-shadow-panel", "Scroll shadow panel", "Scroll", "Docs", "A scrollable panel earns top/bottom shadows only when useful.", ["scroll", "shadow", "docs", "panel"], "template-ixartz-docs-first-saas-home"),
    ("inline-copy-confirm", "Inline copy confirm", "Confirm", "Devtool", "Copy buttons confirm in place with a tiny success sweep.", ["copy", "confirm", "code", "microinteraction"], "template-ixartz-devtool-landing-page"),
    ("draggable-chip-cloud", "Draggable chip cloud", "Filter", "AI app", "Filter chips feel tactile through press, lift, and snap feedback.", ["chips", "filter", "drag", "tactile"], "template-ui-layouts-interactive-gallery"),
    ("kanban-card-lift", "Kanban card lift", "Manipulate", "Internal tool", "Cards lift with shadow hierarchy before moving across a board.", ["kanban", "drag", "card", "board"], "template-shadcnstore-mail-task-dashboard"),
    ("calendar-density-hover", "Calendar density hover", "Inspect", "Calendar", "A dense schedule exposes details through focused hover lanes.", ["calendar", "density", "hover", "schedule"], "template-shadcnstore-calendar-ops-dashboard"),
    ("chat-message-stream", "Chat message stream", "AI app", "Chat", "Assistant messages enter with line-by-line cadence and source chips.", ["chat", "stream", "ai", "sources"], "template-shadcnstore-chat-support-console"),
    ("notebook-side-notes", "Notebook side notes", "Editor", "AI app", "Inline notes anchor to selected paragraphs in a calm editor layout.", ["notebook", "editor", "annotations", "ai"], "opencodesign-ai-writing-assistant-hero"),
    ("map-pulse-marker", "Map pulse marker", "Map", "Geo app", "Markers pulse with confidence rings and labels on focus.", ["map", "marker", "pulse", "geo"], "motionsites-terra-geo-map"),
    ("space-depth-cards", "Space depth cards", "3D", "Portfolio", "Cards float in depth with soft starfield movement.", ["space", "3d", "portfolio", "depth"], "motionsites-space-voyage"),
    ("agency-case-reveal", "Agency case reveal", "Portfolio", "Agency", "Case study tiles reveal role, stack, and outcome on hover.", ["agency", "case-study", "hover", "portfolio"], "opencodesign-boutique-agency-homepage"),
    ("inventory-alert-row", "Inventory alert row", "Status", "Commerce", "Low-stock rows pulse once, then settle into clear severity color.", ["inventory", "alert", "commerce", "table"], "opencodesign-ecommerce-inventory-dashboard"),
    ("security-scan-radar", "Security scan radar", "Status", "Security", "A radar sweep visualizes background protection checks.", ["security", "radar", "status", "scan"], "opencodesign-enterprise-security-page"),
    ("revenue-sparkline-stack", "Revenue sparkline stack", "Data", "Analytics", "Tiny sparklines animate into a compact metric stack.", ["sparkline", "revenue", "metrics", "chart"], "opencodesign-saas-revenue-dashboard"),
    ("feature-flow-steps", "Feature flow steps", "Explain", "SaaS app", "A three-step flow highlights one step at a time.", ["steps", "feature", "flow", "explain"], "template-karthik-framer-motion-feature-flow"),
    ("footer-orbital-links", "Footer orbital links", "Navigate", "Marketing", "Footer links orbit around one final CTA without clutter.", ["footer", "links", "cta", "motion"], "tailark-final-cta-footer"),
    ("team-grid-spotlight", "Team grid spotlight", "People", "Marketing", "Team portraits receive a soft cursor-follow spotlight.", ["team", "grid", "spotlight", "hover"], "tailark-team-grid-editorial"),
    ("stats-proof-countup", "Stats proof count-up", "Proof", "Marketing", "Proof metrics count up once as the band enters view.", ["stats", "countup", "proof", "scroll"], "tailark-stats-proof-band"),
    ("spring-roller-reveal", "Spring roller reveal", "Reveal", "Hero", "A roller-blind mask uncovers content with springy overshoot.", ["reveal", "spring", "mask", "hero"], "spring-roller-blind-reveal"),
]

CSS = r'''
:root{color-scheme:dark;--bg:#0b0d12;--panel:#121722;--ink:#f7f3e8;--muted:#9ea7b7;--line:rgba(255,255,255,.12);--accent:#8be9d5;--accent2:#ffcf70;--danger:#ff796f}*{box-sizing:border-box}body{margin:0;min-height:100vh;background:radial-gradient(circle at 20% 10%,rgba(139,233,213,.18),transparent 32%),linear-gradient(135deg,#08090d,#111827 56%,#161008);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.frame{min-height:100vh;padding:22px;display:grid;place-items:center}.specimen{width:min(760px,100%);min-height:390px;border:1px solid var(--line);border-radius:28px;background:linear-gradient(145deg,rgba(255,255,255,.08),rgba(255,255,255,.025));box-shadow:0 24px 80px rgba(0,0,0,.38);overflow:hidden;position:relative}.bar{display:flex;gap:8px;padding:16px 18px;border-bottom:1px solid var(--line);align-items:center}.dot{width:9px;height:9px;border-radius:999px;background:#536072}.dot:nth-child(1){background:#ff796f}.dot:nth-child(2){background:#ffcf70}.dot:nth-child(3){background:#8be9d5}.label{margin-left:auto;color:var(--muted);font-size:12px;letter-spacing:.08em;text-transform:uppercase}.stage{padding:26px}.chip{display:inline-flex;align-items:center;gap:7px;padding:7px 10px;border:1px solid var(--line);border-radius:999px;background:rgba(255,255,255,.06);font-size:12px;color:var(--muted)}button,.button{font:inherit;color:inherit;border:1px solid var(--line);background:rgba(255,255,255,.07);border-radius:14px;padding:10px 13px}button:hover,.button:hover{background:rgba(255,255,255,.12)}.grid{display:grid;gap:12px}.muted{color:var(--muted)}@media(max-width:560px){.frame{padding:10px}.specimen{border-radius:20px}.stage{padding:18px}}
'''

TEMPLATE_CSS = {
"Reveal": ".rows{display:grid;gap:12px}.row{display:grid;grid-template-columns:auto 1fr auto;gap:14px;align-items:center;padding:14px;border:1px solid var(--line);border-radius:18px;background:rgba(255,255,255,.055);opacity:0;transform:translateY(18px);animation:rise .7s cubic-bezier(.2,.8,.2,1) forwards;animation-delay:calc(var(--i)*90ms)}.row b{font-size:14px}.avatar{width:34px;height:34px;border-radius:12px;background:linear-gradient(135deg,var(--accent),#758bff)}@keyframes rise{to{opacity:1;transform:none}}",
"Navigate": ".navdemo{display:flex;gap:18px}.rail{width:78px;padding:12px;border:1px solid var(--line);border-radius:24px;background:rgba(255,255,255,.07);backdrop-filter:blur(18px)}.rail span{display:block;margin:10px auto;width:38px;height:38px;border-radius:14px;background:rgba(255,255,255,.09);transition:.25s}.rail span:nth-child(2){background:var(--accent);box-shadow:0 0 24px rgba(139,233,213,.45)}.panel{flex:1;min-height:250px;border:1px solid var(--line);border-radius:24px;padding:18px;background:rgba(0,0,0,.16)}.pills{display:flex;gap:8px;flex-wrap:wrap}.pill{padding:9px 12px;border-radius:999px;background:rgba(255,255,255,.07)}",
"Details": ".table{display:grid;gap:10px}.audit{border:1px solid var(--line);border-radius:18px;overflow:hidden;background:rgba(255,255,255,.055)}.audit summary{cursor:pointer;list-style:none;padding:14px 16px;display:flex;justify-content:space-between}.audit summary::-webkit-details-marker{display:none}.audit[open]{background:rgba(139,233,213,.08)}.detail{padding:0 16px 16px;color:var(--muted);display:grid;gap:8px}.detail code{color:var(--accent)}",
"Inspect": ".peekgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.peek{position:relative;min-height:180px;border:1px solid var(--line);border-radius:22px;background:linear-gradient(145deg,rgba(255,255,255,.08),rgba(139,233,213,.05));padding:14px;overflow:hidden}.peek div{position:absolute;left:10px;right:10px;bottom:10px;padding:12px;border-radius:16px;background:rgba(0,0,0,.55);transform:translateY(115%);transition:.3s}.peek:hover div{transform:none}@media(max-width:560px){.peekgrid{grid-template-columns:1fr}}",
"Filter": ".seg{position:relative;display:inline-grid;grid-template-columns:repeat(3,1fr);padding:6px;border:1px solid var(--line);border-radius:999px;background:rgba(255,255,255,.06)}.seg button{border:0;background:transparent;position:relative;z-index:1}.seg:before{content:'';position:absolute;inset:6px auto 6px 6px;width:31%;border-radius:999px;background:var(--accent);transition:.35s}.seg:hover:before{transform:translateX(105%)}.cards{margin-top:24px;display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.mini{height:120px;border:1px solid var(--line);border-radius:18px;background:rgba(255,255,255,.06)}",
"Emphasize": ".bento{display:grid;grid-template-columns:1.2fr .8fr;gap:14px}.tile{min-height:132px;border:1px solid var(--line);border-radius:24px;padding:18px;background:linear-gradient(135deg,rgba(255,255,255,.08),rgba(255,207,112,.06));transition:.25s}.tile:hover{transform:translateY(-8px) rotateX(4deg);box-shadow:0 24px 44px rgba(0,0,0,.28)}.tile.big{grid-row:span 2}@media(max-width:560px){.bento{grid-template-columns:1fr}}",
"Load": ".skeleton{display:grid;gap:13px}.sk{height:54px;border-radius:17px;background:linear-gradient(90deg,rgba(255,255,255,.06),rgba(255,255,255,.16),rgba(255,255,255,.06));background-size:220% 100%;animation:shine 1.4s infinite}.sk:nth-child(2){width:82%}.sk:nth-child(3){width:68%}@keyframes shine{to{background-position:-220% 0}}",
"Empty": ".empty{text-align:center;padding:28px}.empty h2{font-size:30px;margin:8px 0}.actions{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:22px}.act{text-align:left;padding:14px;border:1px solid var(--line);border-radius:18px;background:rgba(255,255,255,.06)}@media(max-width:560px){.actions{grid-template-columns:1fr}}",
"Convert": ".price{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.plan{padding:18px;border:1px solid var(--line);border-radius:22px;background:rgba(255,255,255,.055)}.plan:nth-child(2){background:rgba(139,233,213,.09);transform:translateY(-8px)}.toggle{margin-bottom:18px}.proof{color:var(--accent);font-size:13px}@media(max-width:560px){.price{grid-template-columns:1fr}}",
"Proof": ".marquee{overflow:hidden;mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent)}.track{display:flex;gap:12px;animation:mar 14s linear infinite}.logo{flex:0 0 140px;height:70px;border:1px solid var(--line);border-radius:18px;display:grid;place-items:center;background:rgba(255,255,255,.06);color:var(--muted)}@keyframes mar{to{transform:translateX(-50%)}}",
"Hero": ".hero h1{font-size:clamp(38px,8vw,72px);line-height:.9;margin:0}.rot{display:inline-block;color:var(--accent);animation:swap 3s infinite}.hero p{max-width:460px;color:var(--muted)}@keyframes swap{0%,28%{transform:translateY(0);filter:blur(0)}35%,55%{transform:translateY(-8px);filter:blur(2px)}65%,100%{transform:translateY(0);filter:blur(0)}}",
"Surface": ".glass{min-height:260px;border:1px solid rgba(255,255,255,.22);border-radius:30px;padding:26px;background:linear-gradient(145deg,rgba(255,255,255,.18),rgba(255,255,255,.035));backdrop-filter:blur(20px);position:relative;overflow:hidden}.glass:before{content:'';position:absolute;inset:-40%;background:radial-gradient(circle,rgba(255,255,255,.32),transparent 35%);animation:glide 5s infinite linear}.glass>*{position:relative}@keyframes glide{to{transform:translate(20%,18%) rotate(1turn)}}",
"Ambient": ".field{height:270px;position:relative;border:1px solid var(--line);border-radius:26px;overflow:hidden;background:#070910}.particle{position:absolute;width:5px;height:5px;border-radius:50%;background:var(--accent);left:var(--x);top:var(--y);animation:float calc(5s + var(--d)*1s) infinite alternate}.center{position:absolute;inset:0;display:grid;place-items:center;text-align:center}@keyframes float{to{transform:translate(18px,-24px);opacity:.35}}",
"Scroll": ".scrollbox{height:260px;overflow:auto;border:1px solid var(--line);border-radius:22px;background:linear-gradient(#0d111a,#0d111a) padding-box}.scrollbox:before{content:'scroll shadows appear when content moves';position:sticky;top:0;display:block;padding:12px;background:linear-gradient(#0d111a,rgba(13,17,26,.2));color:var(--muted);font-size:12px}.scrollbox p{margin:0;padding:16px;border-bottom:1px solid var(--line)}",
"Confirm": ".code{background:#05070b;border:1px solid var(--line);border-radius:22px;padding:18px}.line{height:16px;margin:10px 0;border-radius:8px;background:rgba(255,255,255,.1)}.copybtn{margin-top:14px;position:relative;overflow:hidden}.copybtn:focus:after,.copybtn:hover:after{content:'Copied';position:absolute;inset:0;display:grid;place-items:center;background:var(--accent);color:#07100d}",
"Manipulate": ".board{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.lane{min-height:240px;border:1px solid var(--line);border-radius:22px;padding:10px;background:rgba(255,255,255,.04)}.ticket{padding:13px;border-radius:16px;background:rgba(255,255,255,.08);margin-bottom:10px;transition:.25s}.ticket:hover{transform:translateY(-8px) rotate(-1deg);box-shadow:0 18px 34px rgba(0,0,0,.28)}@media(max-width:560px){.board{grid-template-columns:1fr}}",
"AI app": ".stream{display:grid;gap:12px}.msg{max-width:86%;padding:13px 15px;border:1px solid var(--line);border-radius:18px;background:rgba(255,255,255,.06);opacity:0;animation:type .55s forwards;animation-delay:calc(var(--i)*220ms)}.msg:nth-child(even){margin-left:auto;background:rgba(139,233,213,.08)}@keyframes type{to{opacity:1;transform:none}}",
"Editor": ".editor{display:grid;grid-template-columns:1fr 180px;gap:14px}.doc,.notes{border:1px solid var(--line);border-radius:22px;padding:18px;background:rgba(255,255,255,.05)}mark{background:rgba(139,233,213,.25);color:inherit;border-radius:6px}.note{padding:10px;border-radius:14px;background:rgba(255,207,112,.09);margin-bottom:10px}@media(max-width:560px){.editor{grid-template-columns:1fr}}",
"Map": ".map{height:270px;border:1px solid var(--line);border-radius:26px;position:relative;overflow:hidden;background:linear-gradient(135deg,#10251f,#0b1220)}.map:before{content:'';position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.06) 1px,transparent 1px);background-size:38px 38px}.marker{position:absolute;left:52%;top:45%;width:18px;height:18px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 0 rgba(139,233,213,.5);animation:pulse 1.8s infinite}@keyframes pulse{to{box-shadow:0 0 0 42px rgba(139,233,213,0)}}",
"3D": ".space{height:270px;perspective:800px;position:relative}.float{position:absolute;width:42%;height:150px;border:1px solid var(--line);border-radius:24px;background:linear-gradient(135deg,rgba(139,233,213,.16),rgba(255,255,255,.06));transform:rotateY(-16deg) rotateX(8deg);animation:orb 4s ease-in-out infinite}.float:nth-child(2){right:10%;top:60px;animation-delay:-1.5s}.float:nth-child(3){left:24%;bottom:0;animation-delay:-.6s}@keyframes orb{50%{transform:translateY(-18px) rotateY(14deg) rotateX(5deg)}}",
"Portfolio": ".cases{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}.case{height:170px;border:1px solid var(--line);border-radius:24px;padding:16px;background:linear-gradient(135deg,rgba(255,255,255,.08),rgba(139,233,213,.05));display:flex;flex-direction:column;justify-content:flex-end;overflow:hidden}.case p{transform:translateY(38px);transition:.3s;color:var(--muted)}.case:hover p{transform:none}@media(max-width:560px){.cases{grid-template-columns:1fr}}",
"Status": ".statusrow{display:flex;align-items:center;justify-content:space-between;padding:15px;border:1px solid var(--line);border-radius:18px;background:rgba(255,255,255,.055);margin-bottom:10px}.sev{width:10px;height:10px;border-radius:50%;background:var(--danger);animation:blink 1.6s infinite}.statusrow:nth-child(2) .sev{background:var(--accent2)}.statusrow:nth-child(3) .sev{background:var(--accent)}@keyframes blink{50%{transform:scale(1.8);opacity:.45}}",
"Data": ".metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.metric{padding:18px;border:1px solid var(--line);border-radius:22px;background:rgba(255,255,255,.055)}svg{width:100%;height:62px}.path{stroke:var(--accent);stroke-width:4;fill:none;stroke-dasharray:180;stroke-dashoffset:180;animation:draw 1.4s forwards}@keyframes draw{to{stroke-dashoffset:0}}@media(max-width:560px){.metrics{grid-template-columns:1fr}}",
"Explain": ".steps{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.step{padding:18px;border:1px solid var(--line);border-radius:22px;background:rgba(255,255,255,.055);position:relative}.step:before{content:attr(data-n);display:grid;place-items:center;width:34px;height:34px;border-radius:12px;background:var(--accent);color:#07100d;margin-bottom:40px}.step:nth-child(2){transform:translateY(-10px);background:rgba(139,233,213,.09)}@media(max-width:560px){.steps{grid-template-columns:1fr}}",
"People": ".people{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.person{height:150px;border:1px solid var(--line);border-radius:22px;background:radial-gradient(circle at 50% 35%,rgba(139,233,213,.36),transparent 24%),rgba(255,255,255,.06);transition:.25s}.person:hover{filter:brightness(1.25);transform:translateY(-5px)}@media(max-width:560px){.people{grid-template-columns:repeat(2,1fr)}}",
}

HTML_SNIPPETS = {
"Reveal": '<div class="rows">' + ''.join(f'<div class="row" style="--i:{i}"><span class="avatar"></span><b>Event {i+1} synchronized</b><span class="muted">{90+i*7}%</span></div>' for i in range(6)) + '</div>',
"Navigate": '<div class="navdemo"><div class="rail"><span></span><span></span><span></span><span></span></div><div class="panel"><div class="pills"><span class="pill">Overview</span><span class="pill">Signals</span><span class="pill">Exports</span></div><h2>Navigation surface</h2><p class="muted">Labels, panels, and shortcuts stay close to the working context.</p></div></div>',
"Details": '<div class="table"><details class="audit" open><summary><b>Source confidence changed</b><span>Open</span></summary><div class="detail"><code>confidence +12%</code><span>Three pieces of evidence are attached inline.</span></div></details><details class="audit"><summary><b>Reviewer added note</b><span>Closed</span></summary><div class="detail">Follow-up, owner, and timestamp live here.</div></details></div>',
"Inspect": '<div class="peekgrid"><div class="peek"><b>Dataset</b><div>Source: public API<br>Freshness: 4m</div></div><div class="peek"><b>Model</b><div>Confidence: high<br>Drift: low</div></div><div class="peek"><b>Owner</b><div>Team: growth<br>Status: reviewed</div></div></div>',
"Filter": '<div class="seg"><button>All</button><button>Open</button><button>Done</button></div><div class="cards"><div class="mini"></div><div class="mini"></div><div class="mini"></div></div>',
"Emphasize": '<div class="bento"><div class="tile big"><h2>Primary idea</h2><p class="muted">The important card gets scale and motion.</p></div><div class="tile">Signal</div><div class="tile">Proof</div></div>',
"Load": '<div class="skeleton"><div class="sk"></div><div class="sk"></div><div class="sk"></div><div class="sk"></div></div>',
"Empty": '<div class="empty"><span class="chip">Nothing here yet</span><h2>Start with one useful action.</h2><p class="muted">Empty states should make the next move obvious.</p><div class="actions"><div class="act">Import data</div><div class="act">Create sample</div><div class="act">Read guide</div></div></div>',
"Convert": '<div class="toggle"><button>Monthly</button> <button>Annual</button></div><div class="price"><div class="plan">Starter<br><b>$19</b></div><div class="plan">Pro<br><b>$49</b><p class="proof">Best fit</p></div><div class="plan">Team<br><b>$99</b></div></div>',
"Proof": '<div class="marquee"><div class="track">' + ''.join(f'<div class="logo">LOGO {i}</div>' for i in range(1,9))*2 + '</div></div>',
"Hero": '<div class="hero"><span class="chip">Live specimen</span><h1>Design better <span class="rot">interfaces</span>.</h1><p>Keep the composition stable while one word carries motion and meaning.</p></div>',
"Surface": '<div class="glass"><span class="chip">Glass surface</span><h2>Layered depth without clutter.</h2><p class="muted">Use for one hero/control panel, not every card.</p></div>',
"Ambient": '<div class="field">' + ''.join(f'<span class="particle" style="--x:{(i*17)%95}%;--y:{(i*29)%90}%;--d:{i%5}"></span>' for i in range(24)) + '<div class="center"><div><span class="chip">Ambient only</span><h2>Particle background</h2></div></div></div>',
"Scroll": '<div class="scrollbox">' + ''.join(f'<p>Scrollable content row {i+1}: keep the shadows functional and subtle.</p>' for i in range(12)) + '</div>',
"Confirm": '<div class="code"><div class="line" style="width:70%"></div><div class="line" style="width:94%"></div><div class="line" style="width:55%"></div><button class="copybtn">Copy snippet</button></div>',
"Manipulate": '<div class="board"><div class="lane"><div class="ticket">Design pass</div><div class="ticket">Copy review</div></div><div class="lane"><div class="ticket">Prototype</div></div><div class="lane"><div class="ticket">Ship</div></div></div>',
"AI app": '<div class="stream"><div class="msg" style="--i:0">Analyze this dashboard.</div><div class="msg" style="--i:1">I found three interaction opportunities.</div><div class="msg" style="--i:2">Source chips can stay attached inline.</div></div>',
"Editor": '<div class="editor"><div class="doc"><p>Selected paragraphs can carry <mark>anchored notes</mark> without turning the editor into a dashboard.</p><p class="muted">The note rail is calm until needed.</p></div><div class="notes"><div class="note">Clarify claim</div><div class="note">Add source</div></div></div>',
"Map": '<div class="map"><span class="marker"></span></div>',
"3D": '<div class="space"><div class="float"></div><div class="float"></div><div class="float"></div></div>',
"Portfolio": '<div class="cases"><div class="case"><b>Case 01</b><p>Role, stack, and outcome reveal here.</p></div><div class="case"><b>Case 02</b><p>Keep hover readable and useful.</p></div></div>',
"Status": '<div><div class="statusrow"><b>Critical sync drift</b><span class="sev"></span></div><div class="statusrow"><b>Queue pressure rising</b><span class="sev"></span></div><div class="statusrow"><b>Healthy ingestion</b><span class="sev"></span></div></div>',
"Data": '<div class="metrics">' + ''.join('<div class="metric"><b>+24%</b><svg viewBox="0 0 120 60"><path class="path" d="M4 48 C28 18, 46 54, 72 24 S100 18, 116 10"/></svg></div>' for _ in range(3)) + '</div>',
"Explain": '<div class="steps"><div class="step" data-n="1"><b>Input</b><p class="muted">Lock constraints.</p></div><div class="step" data-n="2"><b>Compose</b><p class="muted">Pick the role.</p></div><div class="step" data-n="3"><b>Ship</b><p class="muted">Verify states.</p></div></div>',
"People": '<div class="people">' + ''.join('<div class="person"></div>' for _ in range(8)) + '</div>',
}

def fallback_kind(kind: str) -> str:
    return kind if kind in TEMPLATE_CSS else "Reveal"

def prompt_for(title, description, tags):
    return f"Implement a focused UI specimen called '{title}'. {description} Keep it isolated, reusable, accessible, responsive, and easy to adapt into an existing product. Use minimal dependencies. Tags: {', '.join(tags)}."

def build_index(pattern):
    slug, title, behavior, context, desc, tags, source = pattern
    kind = fallback_kind(behavior)
    if behavior not in TEMPLATE_CSS and context in TEMPLATE_CSS:
        kind = context
    css = CSS + "\n" + TEMPLATE_CSS[kind]
    body = HTML_SNIPPETS[kind]
    return f"""<!doctype html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>{html.escape(title)} — Framewell pattern</title>
<style>{css}</style>
</head>
<body>
<div class=\"frame\"><main class=\"specimen\" aria-label=\"{html.escape(title)}\"><div class=\"bar\"><span class=\"dot\"></span><span class=\"dot\"></span><span class=\"dot\"></span><span class=\"label\">{html.escape(behavior)} · {html.escape(context)}</span></div><section class=\"stage\">{body}</section></main></div>
<script>document.documentElement.dataset.pattern={json.dumps(slug)};</script>
</body></html>"""

def main():
    PATTERN_DIR.mkdir(exist_ok=True)
    out = []
    for i, p in enumerate(PATTERNS):
        slug, title, behavior, context, desc, tags, source = p
        folder = PATTERN_DIR / slug
        folder.mkdir(parents=True, exist_ok=True)
        index = build_index(p)
        (folder / "index.html").write_text(index)
        code_html = HTML_SNIPPETS[fallback_kind(behavior) if fallback_kind(behavior) in HTML_SNIPPETS else fallback_kind(context)] if False else "See iframe source for full isolated specimen."
        prompt = prompt_for(title, desc, tags)
        (folder / "prompt.md").write_text(prompt + "\n")
        (folder / "meta.json").write_text(json.dumps({"id": slug, "title": title, "behavior": behavior, "context": context, "description": desc, "tags": tags, "sourcePromptIds": [source]}, indent=2) + "\n")
        out.append({
            "id": slug,
            "slug": slug,
            "title": title,
            "behavior": behavior,
            "context": context,
            "description": desc,
            "tags": tags,
            "sourcePromptIds": [source],
            "previewUrl": f"patterns/{slug}/index.html",
            "prompt": prompt,
            "code": index,
            "complexity": "simple" if i % 3 else "medium",
            "dependencies": [],
        })
    DATA_PATH.write_text(json.dumps({"summary": {"count": len(out)}, "patterns": out}, indent=2) + "\n")
    print(f"wrote {len(out)} live patterns to {DATA_PATH.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
