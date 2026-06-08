import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { gsap } from 'gsap';
import * as THREE from 'three';
import {
  Activity,
  AlertTriangle,
  ArrowRight,
  BarChart3,
  Box,
  Check,
  ChevronLeft,
  ChevronRight,
  CircleDollarSign,
  Command,
  Database,
  Film,
  GalleryHorizontalEnd,
  Gauge,
  GitBranch,
  Layers,
  Lock,
  MousePointer2,
  PanelTop,
  Play,
  Radar,
  Search,
  Shield,
  SlidersHorizontal,
  Sparkles,
  TerminalSquare,
  Wand2,
  Zap,
} from 'lucide-react';
import './styles.css';

const fallbackMeta = {
  id: 'spatial-command-room',
  title: 'Spatial command room',
  behavior: 'Command surface',
  context: 'AI dashboard',
  description: 'A command center with live state, evidence, and action routing.',
  tags: ['command', 'dashboard', 'interactive'],
  template: 'command-room',
};

const routeMeta = window.__FRAMEWELL_PATTERN_META__ || null;
const clampProgress = raw => Math.max(0, Math.min(1, Number(raw) || 0));

const specimenKindById = {
  'spatial-command-room': 'command-room',
  'radial-command-wheel': 'radial-command',
  'search-bar-morph-results': 'search',
  'command-center-alert-lens': 'alert-lens',
  'ai-map-of-thought': 'thought-map',
  'ai-agent-path-trace': 'agent-trace',
  'data-lineage-river': 'lineage',
  'audit-evidence-peek': 'evidence',
  'dashboard-row-scroll-reveal': 'dashboard',
  'metric-cards-live-scrub': 'metrics',
  'liquid-drag-dashboard': 'dashboard',
  'calendar-density-brush': 'calendar',
  'security-radar-sweep': 'security',
  'inventory-shelf-pulse': 'inventory',
  'table-column-xray': 'table-xray',
  'kanban-physics-lift': 'kanban',
  'glass-torus-pricing': 'pricing',
  'pricing-card-pressure': 'pricing',
  'aave-glass-switch-lens': 'glass-switch',
  'aave-glass-slider-refraction': 'glass-slider',
  'aave-glass-toggle-group': 'glass-toggle',
  'aave-glass-video-controls': 'video-controls',
  'three-scroll-product-stage': 'three-product',
  'gsap-scroll-cascade-stack': 'gsap-cascade',
  'webgl-shader-gallery-wall': 'shader-gallery',
  'fluid-cursor-lens-index': 'fluid-cursor',
  'scroll-mask-story-panels': 'scroll-mask',
  'three-particle-command-field': 'particle-field',
  'gsap-flip-board-recompose': 'flip-board',
  'split-text-control-deck': 'split-text',
  'dock-with-liquid-focus': 'dock',
  'gallery-hover-scrub': 'gallery',
  'horizontal-case-filmstrip': 'gallery',
  'masonry-hover-recompose': 'masonry',
  '3d-carousel-prism': 'carousel',
  'clip-path-gallery-shuffle': 'clip-gallery',
  'sticky-comparison-wipe': 'compare',
  'responsive-device-morph': 'device',
  'notebook-annotation-rail': 'annotation',
  'docs-code-stepper': 'code-stepper',
  'onboarding-constellation': 'onboarding',
  'hero-spotlight-letters': 'type-hero',
  'kinetic-statements': 'type-hero',
  'shader-noise-navigation': 'shader-nav',
  'spring-roller-blind': 'roller',
  'commerce-size-magnet': 'size-magnet',
  'elastic-cursor-work-index': 'cursor-index',
  'timeline-camera-scrubber': 'timeline',
  'project-card-video-scrub': 'video-card',
  'glassmorphic-audio-reactor': 'audio',
  'svg-line-draw-map': 'map',
  'codrops-webgl-scroll-gallery': 'gallery',
  'gsap-flip-detail-expander': 'case-flip',
  'scroll-driven-3d-world-chapters': 'world',
  'video-texture-cube-grid': 'video-grid',
};

function App(){
  if(!routeMeta) return <AtlasApp />;
  const meta = routeMeta || fallbackMeta;
  const kind = specimenKindById[meta.id] || specimenKindById[meta.slug] || meta.template || 'dashboard';
  const routeText = `${kind} ${meta.behavior || ''} ${(meta.tags || []).join(' ')}`.toLowerCase();
  const isScrollRoute = /scroll|scrolltrigger|sticky|camera/.test(routeText) || kind === 'three-product' || kind === 'gsap-cascade';
  const Specimen = components[kind] || DashboardSurface;
  return (
    <main className={`fw-root ${isScrollRoute ? 'scroll-specimen-root' : ''}`}>
      <section className="specimen-shell">
        <div className="shell-bar">
          <span className="traffic" />
          <span className="traffic" />
          <span className="traffic" />
          <span className="shell-title">{meta.title}</span>
          <span className="shell-meta"><span>{meta.behavior}</span><span>{meta.context}</span></span>
        </div>
        <Specimen meta={meta} />
      </section>
    </main>
  );
}

function AtlasApp(){
  const [items, setItems] = useState([]);
  const [activeId, setActiveId] = useState('');
  const [query, setQuery] = useState('');
  const [view, setView] = useState('Stage');
  const iframeRef = useRef(null);
  useEffect(() => {
    let alive = true;
    fetch('data/patterns.json')
      .then(r => r.json())
      .then(data => {
        if(!alive) return;
        const patterns = data.patterns || [];
        setItems(patterns);
        setActiveId(patterns[0]?.id || '');
      })
      .catch(err => console.error('Could not load patterns', err));
    return () => { alive = false; };
  }, []);
  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if(!q) return items;
    return items.filter(item => [item.title, item.behavior, item.context, item.description, ...(item.tags || [])].join(' ').toLowerCase().includes(q));
  }, [items, query]);
  const active = items.find(item => item.id === activeId) || filtered[0] || items[0];
  const activeKind = active ? (specimenKindById[active.id] || active.template || '') : '';
  const activeTags = active?.tags || [];
  const isScrollExample = /scroll|gsap|three-product|scroll-mask/.test(`${activeKind} ${active?.behavior || ''} ${activeTags.join(' ')}`.toLowerCase());
  useEffect(() => {
    if(!filtered.some(item => item.id === activeId)) setActiveId(filtered[0]?.id || items[0]?.id || '');
  }, [filtered, activeId, items]);
  if(!active) return <div className="motion-lab loading">Loading Framewell motion lab</div>;
  return (
    <main className="motion-lab">
      <aside className="motion-rail">
        <div className="motion-brand">
          <span>Framewell</span>
          <b>premium motion lab</b>
        </div>
        <label className="motion-search">
          <Search size={15} />
          <input value={query} onChange={event => setQuery(event.target.value)} placeholder="gsap, three, scroll, shader..." />
        </label>
        <div className="motion-count">{filtered.length} working examples</div>
        <nav className="motion-list" aria-label="Live motion examples">
          {filtered.map((item, index) => (
            <button key={item.id} className={item.id === active.id ? 'active' : ''} onClick={() => setActiveId(item.id)}>
              <small>{String(index + 1).padStart(2, '0')} · {item.behavior}</small>
              <span>{item.title}</span>
            </button>
          ))}
        </nav>
      </aside>
      <section className="motion-stage-shell">
        <div className="motion-stage-top">
          <div>
            <div className="eyebrow">{active.behavior} · {active.context}</div>
            <h1>{active.title}</h1>
          </div>
          <div className="tabs">
            {['Stage','Prompt','Code'].map(tab => <button key={tab} className={`tab ${view===tab?'active':''}`} onClick={() => setView(tab)}>{tab}</button>)}
          </div>
        </div>
        {view === 'Stage' ? (
          <div className={`motion-stage-live ${isScrollExample ? 'is-scroll-example' : ''}`}>
            <iframe
              ref={iframeRef}
              className="motion-stage-frame"
              src={active.previewUrl}
              title={`${active.title} live preview`}
              onLoad={() => {
                try {
                  const doc = iframeRef.current?.contentDocument;
                  if(isScrollExample) doc?.documentElement.classList.add('framewell-stage-embedded');
                } catch(_) {}
              }}
            />
          </div>
        ) : (
          <pre className="motion-readable">{view === 'Prompt' ? active.prompt : active.code}</pre>
        )}
      </section>
      <aside className="motion-detail">
        <div className="panel">
          <div className="eyebrow">Why it matters</div>
          <p>{active.description}</p>
        </div>
        <div className="panel">
          <div className="eyebrow">Stack / behavior</div>
          <div className="tag-cloud">{(active.tags || []).map(tag => <span key={tag}>{tag}</span>)}</div>
        </div>
        <div className="panel">
          <div className="eyebrow">Use it in a build</div>
          <p>Inspect it at full size first. Then copy the prompt or code and adapt the motion as one focused layer, not as an entire template.</p>
        </div>
      </aside>
    </main>
  );
}

function Header({ meta, icon: Icon = Sparkles, action }){
  return (
    <div className="header-row">
      <div>
        <div className="eyebrow">{meta.behavior}</div>
        <h2>{meta.title}</h2>
      </div>
      {action || <span className="specimen-hint"><Icon size={15} /> interactive specimen</span>}
    </div>
  );
}

function useFramewellDriver(apply, deps = []){
  useEffect(() => {
    const driver = raw => apply(clampProgress(raw));
    window.__FRAMEWELL_SET_PROGRESS__ = driver;
    let frame = 0;
    const startedAt = performance.now();
    const tick = now => {
      const p = (Math.sin((now - startedAt) / 1350) + 1) / 2;
      driver(p);
      frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => {
      cancelAnimationFrame(frame);
      if(window.__FRAMEWELL_SET_PROGRESS__ === driver) delete window.__FRAMEWELL_SET_PROGRESS__;
    };
  }, deps);
}

function useRouteScrollProgress(enabled){
  const [progress, setProgress] = useState(0);
  useEffect(() => {
    if(!enabled) return undefined;
    const update = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      setProgress(max > 0 ? clampProgress(window.scrollY / max) : 0);
    };
    update();
    window.addEventListener('scroll', update, { passive:true });
    window.addEventListener('resize', update);
    return () => {
      window.removeEventListener('scroll', update);
      window.removeEventListener('resize', update);
    };
  }, [enabled]);
  return progress;
}

function CommandRoom({ meta }){
  const [active, setActive] = useState('Build');
  const rows = ['Patch preview cards', 'Verify modal iframe', 'Ship Vercel build', 'Archive weak specimens'];
  return (
    <div className="surface dark noise">
      <Header meta={meta} icon={Command} action={<button className="btn" type="button"><Command size={16}/>⌘ K</button>} />
      <div className="grid-2">
        <div className="panel" style={{padding:16}}>
          <div className="field" style={{display:'flex',gap:10,alignItems:'center'}}><Search size={17}/><span style={{color:'rgba(255,246,229,.72)'}}>Ask Framewell to improve previews...</span><span className="kbd">Enter</span></div>
          <div className="tabs" style={{marginTop:14}}>
            {['Build','Audit','Deploy','Review'].map(x => <button key={x} className={`tab ${active===x?'active':''}`} onClick={() => setActive(x)}>{x}</button>)}
          </div>
          <div className="list" style={{marginTop:14}}>
            {rows.map((row, i) => (
              <div className="row" key={row} style={{transform:`translateX(${active==='Deploy' && i>1 ? -8 : 0}px)`}}>
                <span className="avatar">{i+1}</span>
                <div style={{flex:1}}><h3>{row}</h3><p>{active} route · source checked · ready to run</p></div>
                <span className={i<2?'badge good':'badge warn'}>{i<2?'live':'queued'}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="panel" style={{padding:16,display:'grid',gridTemplateRows:'auto 1fr',gap:14}}>
          <div className="grid-3">
            <div className="metric"><span>Latency</span><b>184ms</b></div>
            <div className="metric"><span>Coverage</span><b>96%</b></div>
            <div className="metric"><span>Risk</span><b>Low</b></div>
          </div>
          <div className="panel" style={{padding:18,background:'rgba(120,240,208,.10)',position:'relative',overflow:'hidden'}}>
            <GitBranch size={34} />
            <h1 style={{marginTop:18}}>Route the work, then prove it.</h1>
            <p style={{maxWidth:320,marginTop:10}}>Each action has state, evidence, and an explicit next command instead of a decorative motion loop.</p>
            <span className="floating" style={{right:18,bottom:18}}>interactive command surface</span>
          </div>
        </div>
      </div>
    </div>
  );
}

function SearchMorph({ meta }){
  const [query, setQuery] = useState('glass');
  const items = ['Glass switch lens', 'Pricing pressure card', 'Evidence hover drawer', 'Command menu route'];
  const visible = items.filter(x => x.toLowerCase().includes(query.toLowerCase()) || !query);
  return (
    <div className="surface clean">
      <Header meta={meta} icon={Search} />
      <div className="panel" style={{padding:18}}>
        <div className="field" style={{display:'flex',alignItems:'center',gap:10,borderRadius:24}}>
          <Search size={19}/><input value={query} onChange={e=>setQuery(e.target.value)} style={{border:0,background:'transparent',outline:0,flex:1,fontSize:20,fontWeight:760}} aria-label="Search patterns" />
          <span className="badge good">{visible.length} results</span>
        </div>
        <div className="grid-2" style={{marginTop:18}}>
          {visible.map((item, i) => (
            <button className="panel" key={item} style={{padding:16,textAlign:'left',cursor:'pointer',transform:`translateY(${i*4}px)`}}>
              <div className="eyebrow">Result {i+1}</div><h3>{item}</h3><p>Live state, keyboard focus, source metadata, and adaptation prompt.</p>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

function ThreeProductStage({ meta }){
  const mountRef = useRef(null);
  const [chapter, setChapter] = useState(0);
  useEffect(() => {
    const mount = mountRef.current;
    if(!mount) return;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(38, mount.clientWidth / mount.clientHeight, 0.1, 100);
    camera.position.set(0, 0.25, 5.6);
    const renderer = new THREE.WebGLRenderer({ antialias:true, alpha:true });
    renderer.setSize(mount.clientWidth, mount.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.8));
    mount.appendChild(renderer.domElement);
    const group = new THREE.Group();
    scene.add(group);
    const geo = new THREE.IcosahedronGeometry(1.15, 3);
    const mat = new THREE.MeshStandardMaterial({ color:0x79f4d3, roughness:0.38, metalness:0.72 });
    const core = new THREE.Mesh(geo, mat);
    group.add(core);
    const ringMat = new THREE.MeshBasicMaterial({ color:0xf5c76a, transparent:true, opacity:.46 });
    for(let i=0;i<3;i++){
      const ring = new THREE.Mesh(new THREE.TorusGeometry(1.55 + i*.28, .012, 16, 128), ringMat);
      ring.rotation.set(i*.7, i*.42, i*.2);
      group.add(ring);
    }
    const light = new THREE.PointLight(0xffffff, 4, 20);
    light.position.set(2.5, 3, 4);
    scene.add(light, new THREE.AmbientLight(0x8aa8ff, 1.2));
    let frame = 0;
    const applyProgress = raw => {
      const p = Math.max(0, Math.min(1, Number(raw) || 0));
      setChapter(Math.min(3, Math.floor(p * 4)));
      gsap.to(group.rotation, { x: p * 1.2, y: p * Math.PI * 1.4, duration:.35, overwrite:true });
      gsap.to(camera.position, { z: 5.6 - p * 1.4, y: .25 + p * .8, duration:.35, overwrite:true });
    };
    window.__FRAMEWELL_SET_PROGRESS__ = applyProgress;
    const onScroll = () => {
      const max = document.documentElement.scrollHeight - innerHeight || 1;
      applyProgress(scrollY / max);
    };
    const tick = () => {
      frame = requestAnimationFrame(tick);
      core.rotation.y += .006;
      renderer.render(scene, camera);
    };
    const resize = () => {
      camera.aspect = mount.clientWidth / mount.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(mount.clientWidth, mount.clientHeight);
    };
    addEventListener('scroll', onScroll, { passive:true });
    addEventListener('resize', resize);
    tick(); onScroll();
    return () => {
      cancelAnimationFrame(frame);
      removeEventListener('scroll', onScroll);
      removeEventListener('resize', resize);
      if(window.__FRAMEWELL_SET_PROGRESS__ === applyProgress) delete window.__FRAMEWELL_SET_PROGRESS__;
      mount.removeChild(renderer.domElement);
      renderer.dispose(); geo.dispose(); mat.dispose(); ringMat.dispose();
    };
  }, []);
  return (
    <div className="surface dark scroll-cinema">
      <div className="scroll-stage">
        <div className="three-stage" ref={mountRef} />
        <div className="scroll-copy">
          <Header meta={meta} icon={Box} />
          <h1>Scroll drives the camera, labels, and object state.</h1>
          <p>This is a real Three.js render loop, not a CSS approximation. Scroll inside the example to move through the product chapters.</p>
          <div className="chapter-tabs">{['Form','Layers','Signals','Ship'].map((x,i)=><span className={chapter===i?'active':''} key={x}>{x}</span>)}</div>
        </div>
      </div>
      <div className="scroll-spacer" />
    </div>
  );
}

function GsapCascade({ meta }){
  const rootRef = useRef(null);
  useEffect(() => {
    const root = rootRef.current;
    if(!root) return;
    const cards = gsap.utils.toArray(root.querySelectorAll('.cascade-card'));
    const applyProgress = raw => {
      const p = Math.min(1, Math.max(.2, Number(raw) || 0));
      cards.forEach((card, i) => {
        gsap.to(card, {
          x: (i - 2) * 112 * p,
          y: (i - 2) * 22 * p + i * 26,
          rotate: (-8 + i * 4) * p,
          scale: 1 - Math.abs(i - 2) * .018 * p,
          duration:.28,
          overwrite:true,
          ease:'power3.out',
        });
      });
    };
    window.__FRAMEWELL_SET_PROGRESS__ = applyProgress;
    const onScroll = () => {
      const rect = root.getBoundingClientRect();
      applyProgress(-rect.top / (root.scrollHeight - innerHeight || 1));
    };
    addEventListener('scroll', onScroll, { passive:true });
    applyProgress(.62);
    onScroll();
    return () => {
      removeEventListener('scroll', onScroll);
      if(window.__FRAMEWELL_SET_PROGRESS__ === applyProgress) delete window.__FRAMEWELL_SET_PROGRESS__;
    };
  }, []);
  return (
    <div className="surface clean scroll-cinema" ref={rootRef}>
      <div className="scroll-stage light">
        <Header meta={meta} icon={Layers} />
        <div className="cascade-stack">
          {['Discover','Frame','Animate','Inspect','Ship'].map((x,i)=><div className="cascade-card panel" key={x}><span>0{i+1}</span><h2>{x}</h2><p>GSAP scrubbed stack transition with stable cards and readable stops.</p></div>)}
        </div>
      </div>
      <div className="scroll-spacer" />
    </div>
  );
}

function ShaderGallery({ meta }){
  const [active, setActive] = useState(2);
  useFramewellDriver(p => setActive(Math.min(4, Math.floor(p * 5))), []);
  return (
    <div className="surface ink">
      <Header meta={meta} icon={GalleryHorizontalEnd} />
      <div className="shader-gallery">
        {[0,1,2,3,4].map(i => (
          <button key={i} onClick={()=>setActive(i)} className={active===i?'active':''}>
            <span>Case {i+1}</span>
            <b>{['Ripple','Frost','Plasma','Glass','Time'][i]}</b>
          </button>
        ))}
      </div>
    </div>
  );
}

function FluidCursor({ meta }){
  const [pos, setPos] = useState({x:58,y:52});
  useFramewellDriver(p => setPos({ x: 18 + p * 70, y: 42 + Math.sin(p * Math.PI * 2) * 22 }), []);
  return (
    <div className="surface ink" onPointerMove={event => {
      const r = event.currentTarget.getBoundingClientRect();
      setPos({ x: ((event.clientX-r.left)/r.width)*100, y: ((event.clientY-r.top)/r.height)*100 });
    }}>
      <Header meta={meta} icon={MousePointer2} />
      <div className="fluid-index" style={{'--x':`${pos.x}%`,'--y':`${pos.y}%`}}>
        {['Atlas','Motion','Systems','Deploy'].map((item,i)=><button key={item}><small>0{i+1}</small>{item}</button>)}
        <div className="cursor-orb" />
      </div>
    </div>
  );
}

function ScrollMaskPanels({ meta }){
  const [amount, setAmount] = useState(55);
  useEffect(() => {
    const applyProgress = raw => setAmount(Math.round(12 + Math.max(0, Math.min(1, Number(raw) || 0)) * 80));
    window.__FRAMEWELL_SET_PROGRESS__ = applyProgress;
    return () => {
      if(window.__FRAMEWELL_SET_PROGRESS__ === applyProgress) delete window.__FRAMEWELL_SET_PROGRESS__;
    };
  }, []);
  return (
    <div className="surface clean">
      <Header meta={meta} icon={Film} action={<input type="range" min="12" max="92" value={amount} onChange={e=>setAmount(Number(e.target.value))} />} />
      <div className="mask-story">
        <div className="mask-before"><h1>Static claim</h1><p>Looks fine, but says nothing about the product behavior.</p></div>
        <div className="mask-after" style={{clipPath:`inset(0 ${100-amount}% 0 0)`}}><h1>Motion proof</h1><p>The interaction makes the transformation inspectable.</p></div>
      </div>
    </div>
  );
}

function ParticleField({ meta }){
  const mountRef = useRef(null);
  useEffect(() => {
    const mount = mountRef.current;
    if(!mount) return;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, mount.clientWidth/mount.clientHeight, .1, 100);
    camera.position.z = 5;
    const renderer = new THREE.WebGLRenderer({ antialias:true, alpha:true });
    renderer.setSize(mount.clientWidth, mount.clientHeight);
    renderer.setPixelRatio(Math.min(devicePixelRatio, 1.8));
    mount.appendChild(renderer.domElement);
    const count = 900;
    const positions = new Float32Array(count*3);
    for(let i=0;i<count;i++){ positions[i*3]=(Math.random()-.5)*5; positions[i*3+1]=(Math.random()-.5)*3; positions[i*3+2]=(Math.random()-.5)*2; }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions,3));
    const points = new THREE.Points(geo, new THREE.PointsMaterial({ color:0x78f0d0, size:.035, transparent:true, opacity:.94 }));
    scene.add(points);
    let frame=0;
    const tick=()=>{ frame=requestAnimationFrame(tick); points.rotation.y+=.003; points.rotation.x=Math.sin(performance.now()/1600)*.1; renderer.render(scene,camera); };
    tick();
    return()=>{ cancelAnimationFrame(frame); mount.removeChild(renderer.domElement); renderer.dispose(); geo.dispose(); };
  }, []);
  return (
    <div className="surface dark">
      <Header meta={meta} icon={Sparkles} />
      <div className="particle-stage" ref={mountRef}><div><h1>Particle command field</h1><p>Three.js points react as a product-grade ambient hero layer.</p></div></div>
    </div>
  );
}

function FlipBoard({ meta }){
  const [mode, setMode] = useState('Priority');
  useFramewellDriver(p => setMode(p > .5 ? 'Timeline' : 'Priority'), []);
  const cards = mode === 'Priority' ? ['Incident','Review','Patch','Ship'] : ['Research','Prototype','Probe','Publish'];
  return (
    <div className="surface clean">
      <Header meta={meta} icon={Layers} action={<div className="tabs">{['Priority','Timeline'].map(x=><button className={`tab ${mode===x?'active':''}`} onClick={()=>setMode(x)} key={x}>{x}</button>)}</div>} />
      <div className="flip-board">
        {cards.map((card,i)=><div className="panel" key={card}><span>{String(i+1).padStart(2,'0')}</span><h2>{card}</h2><p>Layout recomposes without losing continuity.</p></div>)}
      </div>
    </div>
  );
}

function SplitTextDeck({ meta }){
  const [style, setStyle] = useState('Stagger');
  useFramewellDriver(p => setStyle(p < .34 ? 'Stagger' : p < .67 ? 'Blur' : 'Invert'), []);
  return (
    <div className="surface ink">
      <Header meta={meta} icon={Sparkles} action={<div className="tabs">{['Stagger','Blur','Invert'].map(x=><button className={`tab ${style===x?'active':''}`} onClick={()=>setStyle(x)} key={x}>{x}</button>)}</div>} />
      <div className={`split-deck ${style.toLowerCase()}`}>
        {'Premium motion should explain the product'.split(' ').map((word,i)=><span key={`${word}-${i}`} style={{'--i':i}}>{word}</span>)}
      </div>
    </div>
  );
}

function DashboardSurface({ meta }){
  const [range, setRange] = useState(62);
  useFramewellDriver(p => setRange(Math.round(20 + p * 74)), []);
  const cards = [['Revenue','$128k'],['Orders','1,482'],['AOV','$86'],['Risk','12']];
  return (
    <div className="surface blue">
      <Header meta={meta} icon={BarChart3} action={<input type="range" min="20" max="94" value={range} onChange={e=>setRange(e.target.value)} aria-label="Scrub metrics" />} />
      <div className="grid-3">
        {cards.map(([label,value], i) => <div className="metric" key={label}><span>{label}</span><b>{i===0 ? `$${Math.round(range*2.1)}k` : value}</b></div>)}
      </div>
      <div className="grid-2" style={{marginTop:14}}>
        <div className="panel" style={{padding:16}}>
          <h3>Forecast line</h3>
          <svg className="chart" viewBox="0 0 420 130" role="img" aria-label="Forecast chart">
            <path className="fill" d={`M10 110 C90 ${120-range} 130 80 190 ${108-range/2} S310 ${40+range/3} 410 ${102-range} L410 130 L10 130 Z`} />
            <path d={`M10 110 C90 ${120-range} 130 80 190 ${108-range/2} S310 ${40+range/3} 410 ${102-range}`} />
          </svg>
        </div>
        <div className="panel" style={{padding:16}}>
          <h3>Operations queue</h3>
          <div className="list" style={{marginTop:12}}>
            {['Restock ceramic mug','Review fraud hold','Release pre-order'].map((x,i)=><div className="row" key={x}><span className="avatar">{i+1}</span><span style={{flex:1}}>{x}</span><span className={i===1?'badge warn':'badge good'}>{i===1?'watch':'clear'}</span></div>)}
          </div>
        </div>
      </div>
    </div>
  );
}

function PricingWorkbench({ meta }){
  const [plan, setPlan] = useState('Studio');
  useFramewellDriver(p => setPlan(['Starter','Studio','Scale'][Math.min(2, Math.floor(p * 3))]), []);
  return (
    <div className="surface clean">
      <Header meta={meta} icon={CircleDollarSign} />
      <div className="grid-3" style={{height:400,alignItems:'center'}}>
        {['Starter','Studio','Scale'].map((name, i) => (
          <button key={name} onClick={()=>setPlan(name)} className="panel" style={{height:plan===name?330:280,padding:18,textAlign:'left',cursor:'pointer',borderColor:plan===name?'#15120d':'rgba(20,17,12,.10)',background:plan===name?'#15120d':'rgba(255,255,255,.74)',color:plan===name?'#fff8eb':'#15120d'}}>
            <div className="eyebrow">{i===1?'Recommended':'Plan'}</div>
            <h2 style={{marginTop:10}}>{name}</h2>
            <h1 style={{marginTop:24}}>${[19,49,99][i]}</h1>
            <p style={{marginTop:12,color:plan===name?'rgba(255,246,229,.66)':'#716756'}}>Pressure hover, clear comparison, and a real selected state.</p>
            <div className="progress" style={{marginTop:24}}><b style={{width:`${[35,68,92][i]}%`}} /></div>
          </button>
        ))}
      </div>
    </div>
  );
}

function GlassControls({ meta, mode='switch' }){
  const [value, setValue] = useState(58);
  const [active, setActive] = useState('Flow');
  useFramewellDriver(p => {
    setValue(Math.round(12 + p * 70));
    setActive(['Risk','Flow','Cost','Live'][Math.min(3, Math.floor(p * 4))]);
  }, []);
  return (
    <div className="surface dark" style={{background:'radial-gradient(circle at 22% 20%,#293d67,#101114 36%,#09090b)'}}>
      <Header meta={meta} icon={SlidersHorizontal} />
      <div className="panel" style={{height:390,padding:22,position:'relative',overflow:'hidden'}}>
        <div className="glass" style={{position:'absolute',left:60+value*3,top:90,width:150,height:118,borderRadius:44,transition:'left .22s ease'}} />
        <div className="grid-2" style={{position:'relative',zIndex:1}}>
          <div>
            <h1>Readable glass controls</h1>
            <p style={{marginTop:12}}>The lens moves over real labels and controls while preserving contrast.</p>
          </div>
          <div className="panel" style={{padding:18}}>
            {mode === 'toggle' ? (
              <div className="tabs">{['Risk','Flow','Cost','Live'].map(x=><button key={x} onClick={()=>setActive(x)} className={`tab ${active===x?'active':''}`}>{x}</button>)}</div>
            ) : (
              <input type="range" value={value} min="12" max="82" onChange={e=>setValue(Number(e.target.value))} style={{width:'100%'}} aria-label="Glass refraction amount" />
            )}
            <div className="list" style={{marginTop:16}}>
              {['Health score','Borrow capacity','Liquidation buffer'].map((x,i)=><div className="row" key={x}><span className="live-dot"/><span style={{flex:1}}>{x}</span><b>{Math.round(value+i*8)}%</b></div>)}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function GallerySurface({ meta }){
  const [active, setActive] = useState(2);
  useFramewellDriver(p => setActive(Math.min(4, Math.floor(p * 5))), []);
  return (
    <div className="surface ink">
      <Header meta={meta} icon={GalleryHorizontalEnd} />
      <div style={{display:'flex',gap:12,height:400,alignItems:'stretch'}}>
        {[0,1,2,3,4].map(i => (
          <button key={i} onClick={()=>setActive(i)} className="panel" style={{flex:active===i?2.3:1,padding:0,overflow:'hidden',cursor:'pointer',transition:'flex .28s ease',background:`linear-gradient(135deg,hsl(${190+i*28} 70% 54%),hsl(${28+i*24} 80% 62%))`}}>
            <div style={{height:'100%',padding:18,display:'flex',flexDirection:'column',justifyContent:'flex-end',background:'linear-gradient(0deg,rgba(0,0,0,.54),transparent 62%)'}}>
              <span className="badge">{String(i+1).padStart(2,'0')}</span>
              {active===i && <h2 style={{marginTop:12,color:'#fff8eb'}}>Case study frame</h2>}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

function EvidenceSurface({ meta }){
  const [open, setOpen] = useState(1);
  useFramewellDriver(p => setOpen(Math.min(3, Math.floor(p * 4))), []);
  const rows = ['Launch copy changed','Model selector added','Preview route deployed','Accessibility pass'];
  return (
    <div className="surface clean">
      <Header meta={meta} icon={Shield} />
      <div className="grid-2">
        <div className="list">
          {rows.map((row,i)=>(
            <button key={row} className="row" onClick={()=>setOpen(i)} style={{cursor:'pointer',textAlign:'left',background:open===i?'#15120d':'rgba(255,255,255,.72)',color:open===i?'#fff8eb':'#15120d'}}>
              <span className="avatar"><Check size={16}/></span><span style={{flex:1}}>{row}</span><span className="badge good">source</span>
            </button>
          ))}
        </div>
        <div className="panel" style={{padding:20}}>
          <div className="eyebrow">Evidence drawer</div>
          <h1 style={{marginTop:8}}>{rows[open]}</h1>
          <p style={{marginTop:12}}>Owner, timestamp, source URL, diff summary, and confidence sit in the same surface as the decision.</p>
          <div className="grid-3" style={{marginTop:22}}>
            <div className="metric"><span>Fresh</span><b>Now</b></div><div className="metric"><span>Files</span><b>4</b></div><div className="metric"><span>Risk</span><b>2</b></div>
          </div>
        </div>
      </div>
    </div>
  );
}

function AgentTrace({ meta }){
  const [step, setStep] = useState(2);
  useFramewellDriver(p => setStep(Math.min(4, Math.floor(p * 5))), []);
  const tools = ['Read','Patch','Build','Probe','Push'];
  return (
    <div className="surface dark">
      <Header meta={meta} icon={GitBranch} />
      <div className="panel" style={{height:395,padding:22,position:'relative'}}>
        <svg style={{position:'absolute',inset:0,width:'100%',height:'100%',opacity:.65}} viewBox="0 0 860 390">
          <path d="M70 280 C180 72 300 250 420 124 S650 42 780 245" fill="none" stroke="#78f0d0" strokeWidth="4" strokeDasharray="8 12" />
        </svg>
        {tools.map((tool,i)=><button key={tool} onClick={()=>setStep(i)} className="panel" style={{position:'absolute',left:`${8+i*18}%`,top:`${64-(i%2)*34}%`,padding:14,cursor:'pointer',borderColor:step===i?'#f5c76a':'rgba(255,255,255,.12)'}}><div className="eyebrow">Tool</div><h3>{tool}</h3></button>)}
        <div className="floating" style={{left:28,bottom:24}}>Current step: {tools[step]} · output verified</div>
      </div>
    </div>
  );
}

function DeviceMorph({ meta }){
  const [device, setDevice] = useState('Desktop');
  useFramewellDriver(p => setDevice(p < .34 ? 'Desktop' : p < .67 ? 'Tablet' : 'Mobile'), []);
  const dims = {Desktop:[560,300],Tablet:[350,330],Mobile:[190,350]}[device];
  return (
    <div className="surface clean">
      <Header meta={meta} icon={PanelTop} action={<div className="tabs">{['Desktop','Tablet','Mobile'].map(x=><button key={x} onClick={()=>setDevice(x)} className={`tab ${device===x?'active':''}`}>{x}</button>)}</div>} />
      <div style={{display:'grid',placeItems:'center',height:400}}>
        <div className="panel" style={{width:dims[0],height:dims[1],padding:16,transition:'width .28s ease,height .28s ease',borderRadius:device==='Mobile'?30:22}}>
          <div className="grid-2" style={{gridTemplateColumns:device==='Mobile'?'1fr':'1.2fr .8fr'}}>
            <div><h2>Responsive product proof</h2><p style={{marginTop:10}}>The same hierarchy adapts, not just the frame.</p></div>
            <div className="list">{['Nav','Hero','Actions'].map(x=><div key={x} className="row">{x}</div>)}</div>
          </div>
        </div>
      </div>
    </div>
  );
}

function CodeStepper({ meta }){
  const [step, setStep] = useState(1);
  useFramewellDriver(p => setStep(Math.min(3, Math.floor(p * 4))), []);
  return (
    <div className="surface dark">
      <Header meta={meta} icon={TerminalSquare} />
      <div className="grid-2">
        <div className="panel" style={{padding:18,background:'#050607'}}>
          {['const plan = inspect(repo)','applyPatch(files)','npm run validate','browser.probe(previews)'].map((line,i)=><div key={line} onClick={()=>setStep(i)} style={{padding:12,borderRadius:12,cursor:'pointer',background:step===i?'rgba(120,240,208,.16)':'transparent',color:step===i?'#78f0d0':'rgba(255,246,229,.72)'}}>{line}</div>)}
        </div>
        <div className="panel" style={{padding:20}}>
          <div className="eyebrow">Step {step+1}</div>
          <h1 style={{marginTop:10}}>Executable docs</h1>
          <p style={{marginTop:12}}>Click each step to reveal the exact state transition the example is teaching.</p>
          <div className="progress" style={{marginTop:28}}><b style={{width:`${(step+1)*25}%`}} /></div>
        </div>
      </div>
    </div>
  );
}

function TypeHero({ meta }){
  const [mode, setMode] = useState('Focus');
  useFramewellDriver(p => setMode(p > .5 ? 'Audit' : 'Focus'), []);
  const words = (mode === 'Focus' ? 'Build real components' : 'Inspect every state').split(' ');
  return (
    <div className="surface ink noise">
      <Header meta={meta} icon={Sparkles} action={<div className="tabs">{['Focus','Audit'].map(x=><button key={x} onClick={()=>setMode(x)} className={`tab ${mode===x?'active':''}`}>{x}</button>)}</div>} />
      <div style={{height:390,display:'grid',placeItems:'center',textAlign:'center'}}>
        <div>
          <h1 style={{fontSize:82,color:'#fff8eb'}}>{words.map((w,i)=><span key={w} style={{display:'inline-block',marginRight:16,transform:`translateY(${i%2?12:-4}px)`,color:i===1?'#f5c76a':'inherit'}}>{w}</span>)}</h1>
          <p style={{fontSize:16,margin:'18px auto 0',maxWidth:520}}>Typography has selectable states and content variants, not a repeating dissolve.</p>
        </div>
      </div>
    </div>
  );
}

function ComparisonSurface({ meta }){
  const [value,setValue]=useState(54);
  useFramewellDriver(p => setValue(Math.round(12 + p * 76)), []);
  return (
    <div className="surface clean">
      <Header meta={meta} icon={Layers} action={<input type="range" value={value} min="12" max="88" onChange={e=>setValue(e.target.value)} aria-label="Comparison wipe" />} />
      <div className="panel" style={{height:400,position:'relative',overflow:'hidden',background:'#15120d'}}>
        <div style={{position:'absolute',inset:0,background:'linear-gradient(135deg,#355cff,#78f0d0)',padding:26,color:'#fff'}}><h1>Before</h1><p style={{color:'rgba(255,255,255,.72)'}}>Generic animated thumbnail.</p></div>
        <div style={{position:'absolute',inset:0,width:`${value}%`,background:'linear-gradient(135deg,#fff8eb,#f5c76a)',padding:26,overflow:'hidden'}}><h1>After</h1><p>Real control, real state, clear inspection.</p></div>
        <div style={{position:'absolute',top:0,bottom:0,left:`${value}%`,width:3,background:'#fff'}} />
      </div>
    </div>
  );
}

function SecuritySurface({ meta }){
  const [scan,setScan]=useState(72);
  useFramewellDriver(p => setScan(Math.round(42 + p * 58)), []);
  return (
    <div className="surface dark">
      <Header meta={meta} icon={Radar} action={<button className="btn" onClick={()=>setScan(scan>80?54:scan+12)}><Radar size={16}/> Sweep</button>} />
      <div className="grid-2">
        <div className="panel" style={{padding:22,display:'grid',placeItems:'center'}}>
          <div style={{width:270,height:270,borderRadius:'50%',border:'1px solid rgba(255,255,255,.16)',background:`conic-gradient(from ${scan}deg, rgba(120,240,208,.55), rgba(120,240,208,0) 35%, rgba(255,255,255,.05) 36%)`,display:'grid',placeItems:'center'}}>
            <Shield size={62}/><b style={{position:'absolute',fontSize:42,marginTop:122}}>{scan}</b>
          </div>
        </div>
        <div className="list">{['Dependency drift','Exposed token','Runtime error','Policy check'].map((x,i)=><div className="row" key={x}><AlertTriangle size={16}/><span style={{flex:1}}>{x}</span><span className={i===1?'badge bad':'badge good'}>{i===1?'fix':'clear'}</span></div>)}</div>
      </div>
    </div>
  );
}

function KanbanBoard({ meta }){
  const [active,setActive]=useState('Build');
  const [lift,setLift]=useState({ col: 1, card: 1, progress: .64 });
  const columns = {
    Plan:['Audit weak previews','Choose component roles','Name the motion'],
    Build:['React specimen app','Pattern page wrapper','Card scaling'],
    Verify:['Modal route probe','Screenshot montage','Ship proof'],
  };
  const columnNames = Object.keys(columns);
  useFramewellDriver(p => {
    const col = Math.min(2, Math.floor(p * 3));
    setActive(columnNames[col]);
    setLift({ col, card: Math.min(2, Math.floor((p * 9) % 3)), progress: p });
  }, []);
  const runLift = () => {
    const next = (lift.progress + .34) % 1;
    const col = Math.min(2, Math.floor(next * 3));
    setActive(columnNames[col]);
    setLift({ col, card: Math.min(2, Math.floor((next * 9) % 3)), progress: next });
  };
  return (
    <div className="surface clean kanban-physics-surface">
      <Header meta={meta} icon={Layers} action={<button className="btn" onClick={runLift}><Layers size={16}/> Run</button>} />
      <div className="kanban-path">
        <span style={{left:`${16 + lift.progress * 68}%`}}>lift path</span>
        <b style={{width:`${20 + lift.progress * 62}%`}} />
      </div>
      <div className="grid-3 kanban-board">
        {Object.entries(columns).map(([col,cards], colIndex)=>(
          <div key={col} className={`panel kanban-column ${active===col?'active':''}`} onPointerEnter={() => setActive(col)}>
            <button className={`tab ${active===col?'active':''}`} onClick={()=>setActive(col)}>{col}</button>
            <div className="list" style={{marginTop:14}}>
              {cards.map((card,i)=>{
                const isLifted = lift.col === colIndex && lift.card === i;
                return (
                  <button
                    key={card}
                    className={`row kanban-card ${isLifted ? 'lifted' : ''}`}
                    onPointerEnter={() => { setActive(col); setLift({ col: colIndex, card: i, progress: (colIndex + i / 3) / 3 }); }}
                  >
                    <span className="avatar">{i+1}</span>
                    <span>{card}</span>
                    {isLifted && <b>lift</b>}
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function DockSurface({ meta }){
  const [active,setActive]=useState(2);
  useFramewellDriver(p => setActive(Math.min(4, Math.floor(p * 5))), []);
  const apps=[Command,BarChart3,GalleryHorizontalEnd,Shield,TerminalSquare];
  return (
    <div className="surface clean">
      <Header meta={meta} icon={MousePointer2} />
      <div style={{height:390,display:'grid',placeItems:'center'}}>
        <div className="panel" style={{padding:18}}>
          <div style={{display:'flex',gap:12,alignItems:'end'}}>
            {apps.map((Icon,i)=>(
              <button key={i} className="panel" onClick={()=>setActive(i)} style={{width:active===i?92:68,height:active===i?92:68,borderRadius:active===i?28:22,display:'grid',placeItems:'center',cursor:'pointer',transition:'all .22s ease',background:active===i?'#15120d':'#fffaf1',color:active===i?'#f5c76a':'#15120d'}}>
                <Icon size={active===i?34:24}/>
              </button>
            ))}
          </div>
          <div className="panel" style={{marginTop:18,padding:16,textAlign:'center'}}><h2>{['Command','Metrics','Gallery','Security','Code'][active]}</h2><p>Focus preview follows the selected dock item.</p></div>
        </div>
      </div>
    </div>
  );
}

function AnnotationSurface({ meta }){
  const [note,setNote]=useState(0);
  useFramewellDriver(p => setNote(Math.min(3, Math.floor(p * 4))), []);
  const notes=['Tighten headline','Add source chip','Expose keyboard state','Reduce decorative motion'];
  return (
    <div className="surface clean">
      <Header meta={meta} icon={PanelTop} />
      <div className="grid-2">
        <article className="panel" style={{padding:24}}>
          <div className="eyebrow">Review document</div>
          <h1 style={{marginTop:8}}>Every claim needs a visible source.</h1>
          <p style={{marginTop:14,fontSize:15}}>Framewell examples should show behavior and interaction details in the surface itself.</p>
          <div style={{height:110,marginTop:22,borderRadius:18,background:'linear-gradient(135deg,#f5c76a,#fff5d6)'}} />
        </article>
        <aside className="list">
          {notes.map((n,i)=><button key={n} className="row" onClick={()=>setNote(i)} style={{cursor:'pointer',background:note===i?'#15120d':'rgba(255,255,255,.72)',color:note===i?'#fff8eb':'#15120d'}}><span className="avatar">{i+1}</span><span>{n}</span></button>)}
        </aside>
      </div>
    </div>
  );
}

function ShaderNavigation({ meta }){
  const [active,setActive]=useState('Work');
  useFramewellDriver(p => setActive(['Studio','Work','Systems','Contact'][Math.min(3, Math.floor(p * 4))]), []);
  return (
    <div className="surface ink noise">
      <Header meta={meta} icon={Wand2} />
      <nav style={{height:390,display:'grid',alignContent:'center',gap:8}}>
        {['Studio','Work','Systems','Contact'].map((item,i)=>(
          <button key={item} onClick={()=>setActive(item)} style={{border:0,background:'transparent',color:active===item?'#f5c76a':'rgba(255,248,235,.36)',fontSize:active===item?78:62,fontWeight:950,lineHeight:.82,letterSpacing:'-.08em',textAlign:'left',cursor:'pointer',transition:'all .22s ease',filter:active===item?'drop-shadow(0 0 22px rgba(245,199,106,.22))':'none'}}>
            {String(i+1).padStart(2,'0')} {item}
          </button>
        ))}
      </nav>
    </div>
  );
}

function SizeMagnet({ meta }){
  const [size,setSize]=useState('M');
  useFramewellDriver(p => setSize(['XS','S','M','L','XL'][Math.min(4, Math.floor(p * 5))]), []);
  return (
    <div className="surface clean">
      <Header meta={meta} icon={Box} />
      <div style={{height:390,display:'grid',placeItems:'center'}}>
        <div>
          <div style={{display:'flex',gap:12,alignItems:'center'}}>
            {['XS','S','M','L','XL'].map(s=><button key={s} onClick={()=>setSize(s)} className="panel" style={{width:size===s?96:72,height:size===s?96:72,borderRadius:24,cursor:'pointer',background:size===s?'#15120d':'#fffaf1',color:size===s?'#f5c76a':'#15120d',fontWeight:900}}>{s}</button>)}
          </div>
          <div className="panel" style={{marginTop:22,padding:18,textAlign:'center'}}><h2>{size} selected</h2><p>Nearby sizes keep their position while the selected target expands.</p></div>
        </div>
      </div>
    </div>
  );
}

function CursorIndex({ meta }){
  const [active,setActive]=useState(1);
  useFramewellDriver(p => setActive(Math.min(3, Math.floor(p * 4))), []);
  const items=['Atlas','Specimens','Sources','Deploy'];
  return (
    <div className="surface ink">
      <Header meta={meta} icon={MousePointer2} />
      <div style={{position:'relative',height:390}}>
        <div className="glass" style={{position:'absolute',width:150,height:150,borderRadius:'50%',left:active*145+60,top:90,transition:'left .25s ease'}} />
        {items.map((item,i)=><button key={item} onMouseEnter={()=>setActive(i)} onClick={()=>setActive(i)} style={{display:'block',position:'relative',zIndex:1,border:0,background:'transparent',color:active===i?'#fff8eb':'rgba(255,248,235,.34)',fontSize:64,fontWeight:950,letterSpacing:'-.08em',lineHeight:.92,cursor:'pointer'}}>{item}</button>)}
      </div>
    </div>
  );
}

function TimelineSurface({ meta }){
  const [frame,setFrame]=useState(2);
  useFramewellDriver(p => setFrame(Math.min(3, Math.floor(p * 4))), []);
  return (
    <div className="surface dark">
      <Header meta={meta} icon={Film} action={<div className="tabs">{[0,1,2,3].map(i=><button key={i} className={`tab ${frame===i?'active':''}`} onClick={()=>setFrame(i)}>F{i+1}</button>)}</div>} />
      <div className="panel" style={{height:390,padding:18,position:'relative'}}>
        {[0,1,2,3].map(i=><div key={i} className="panel" style={{position:'absolute',left:80+i*165,top:90+(i%2)*70,width:132,height:94,background:frame===i?'#f5c76a':'rgba(255,255,255,.08)',transition:'all .22s ease'}} />)}
        <div style={{position:'absolute',left:90,right:90,bottom:70,height:5,borderRadius:99,background:'rgba(255,255,255,.16)'}}><b style={{display:'block',height:'100%',width:`${25+frame*22}%`,background:'#78f0d0',borderRadius:99}} /></div>
        <div className="floating" style={{left:120+frame*165,bottom:88}}>Camera {frame+1}</div>
      </div>
    </div>
  );
}

function AudioMixer({ meta }){
  const [gain,setGain]=useState(60);
  useFramewellDriver(p => setGain(Math.round(18 + p * 74)), []);
  return (
    <div className="surface dark">
      <Header meta={meta} icon={Activity} action={<input type="range" min="18" max="92" value={gain} onChange={e=>setGain(e.target.value)} aria-label="Audio gain" />} />
      <div className="panel" style={{height:390,padding:22,display:'grid',placeItems:'center'}}>
        <div style={{width:210,height:210,borderRadius:'50%',background:`radial-gradient(circle,#78f0d0 ${gain/2}%,rgba(120,240,208,.10) ${gain/2+1}%)`,boxShadow:'0 0 80px rgba(120,240,208,.22)'}} />
        <div style={{display:'flex',gap:8,alignItems:'end',position:'absolute',bottom:70}}>
          {Array.from({length:26},(_,i)=><span key={i} style={{width:9,height:18+((i*13+Number(gain))%86),borderRadius:99,background:i%3?'#78f0d0':'#f5c76a'}} />)}
        </div>
      </div>
    </div>
  );
}

function MapSurface({ meta }){
  const [pin,setPin]=useState(1);
  useFramewellDriver(p => setPin(Math.min(3, Math.floor(p * 4))), []);
  return (
    <div className="surface dark">
      <Header meta={meta} icon={Database} />
      <div className="panel" style={{height:390,position:'relative',overflow:'hidden',backgroundImage:'linear-gradient(rgba(255,255,255,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.06) 1px,transparent 1px)',backgroundSize:'34px 34px'}}>
        <svg style={{position:'absolute',inset:40,width:'calc(100% - 80px)',height:'calc(100% - 80px)'}} viewBox="0 0 760 280"><path d="M40 220 C140 40 250 200 360 92 S590 34 720 190" fill="none" stroke="#78f0d0" strokeWidth="5" strokeLinecap="round"/></svg>
        {[[18,64],[42,38],[61,56],[78,28]].map(([x,y],i)=><button key={i} onClick={()=>setPin(i)} className="floating" style={{left:`${x}%`,top:`${y}%`,background:pin===i?'#f5c76a':'#15120d',color:pin===i?'#15120d':'#fff8eb'}}>Node {i+1}</button>)}
      </div>
    </div>
  );
}

function OnboardingSurface({ meta }){
  const [done,setDone]=useState([true,false,true,false]);
  useFramewellDriver(p => {
    const cutoff = Math.floor(p * 5);
    setDone([0,1,2,3].map(i => i < cutoff));
  }, []);
  return (
    <div className="surface blue">
      <Header meta={meta} icon={Sparkles} />
      <div className="grid-2">
        <div className="panel" style={{padding:22}}><h1>Choose your launch path.</h1><p style={{marginTop:12}}>Each step is selectable and reflected in the constellation map.</p></div>
        <div className="list">{['Connect store','Import catalog','Design preview','Go live'].map((x,i)=><button key={x} className="row" onClick={()=>setDone(d=>d.map((v,j)=>j===i?!v:v))}><span className={`avatar ${done[i]?'':'warn'}`}>{done[i]?<Check size={16}/>:i+1}</span><span style={{flex:1}}>{x}</span></button>)}</div>
      </div>
    </div>
  );
}

function SimpleWorkbench({ meta }){
  const [n,setN]=useState(1);
  useFramewellDriver(p => setN(Math.min(2, Math.floor(p * 3))), []);
  return (
    <div className="surface clean">
      <Header meta={meta} icon={Wand2} action={<button className="btn" onClick={()=>setN((n+1)%3)}><Zap size={16}/> Change state</button>} />
      <div className="grid-3" style={{height:390}}>
        {[0,1,2].map(i=><div key={i} className="panel" style={{padding:18,transform:n===i?'translateY(-12px)':'none',background:n===i?'#15120d':'rgba(255,255,255,.74)',color:n===i?'#fff8eb':'#15120d'}}><div className="eyebrow">State {i+1}</div><h2 style={{marginTop:12}}>{['Plan','Preview','Ship'][i]}</h2><p style={{marginTop:12,color:n===i?'rgba(255,246,229,.66)':'#716756'}}>A polished component state with explicit controls.</p></div>)}
      </div>
    </div>
  );
}

function PremiumEffectSurface({ meta }){
  const [progress, setProgress] = useState(.48);
  const isScrollDriven = /scroll|scrolltrigger|sticky|camera/.test(`${meta.behavior || ''} ${(meta.tags || []).join(' ')}`.toLowerCase());
  const scrollProgress = useRouteScrollProgress(isScrollDriven);
  useFramewellDriver(setProgress, [meta.id]);
  const p = isScrollDriven ? scrollProgress : clampProgress(progress);
  const step = Math.min(4, Math.floor(p * 5));
  const template = meta.template;
  const sceneTitle = meta.title;
  const header = icon => <Header meta={meta} icon={icon || Sparkles} />;

  if(template === 'radial-command'){
    const commands = ['Ask','Patch','Trace','Ship','Share','Undo'];
    return (
      <div className="surface dark premium-radial">
        {header(Command)}
        <div className="radial-stage">
          <div className="radial-core" style={{transform:`scale(${1 + p * .16}) rotate(${p * 90}deg)`}}>⌘K</div>
          {commands.map((cmd,i) => (
            <button key={cmd} className={i===step?'active':''} style={{'--angle':`${i * 60 + p * 24}deg`}}>
              <span>{cmd}</span>
            </button>
          ))}
        </div>
      </div>
    );
  }

  if(template === 'motion'){
    return (
      <div className="surface dark premium-cinema">
        {header(Film)}
        <div className="cinema-depth" style={{'--p':p}}>
          {[0,1,2,3].map(i => <div key={i} className="cinema-plane" style={{'--i':i}}><b>{String(i+1).padStart(2,'0')}</b></div>)}
          <h1>{sceneTitle}</h1>
        </div>
      </div>
    );
  }

  if(template === 'type-dissolve'){
    return (
      <div className="surface ink premium-type-dissolve">
        {header(Sparkles)}
        <div className="dissolve-word">
          {'DISSOLVE'.split('').map((ch,i) => <span key={i} style={{'--i':i,'--p':p}}>{ch}</span>)}
        </div>
      </div>
    );
  }

  if(template === 'ripple-grid'){
    return (
      <div className="surface ink premium-ripple">
        {header(GalleryHorizontalEnd)}
        <div className="ripple-grid" style={{'--p':p}}>
          {Array.from({length:9},(_,i)=><button key={i} className={i===step+2?'active':''}><span>Case {i+1}</span></button>)}
        </div>
      </div>
    );
  }

  if(template === 'orbit-stage' || template === 'constellation' || template === 'empty-orbit'){
    return (
      <div className="surface dark premium-orbit">
        {header(template === 'orbit-stage' ? Box : Sparkles)}
        <div className="orbit-core" style={{'--p':p}}><span>{template === 'orbit-stage' ? '3D' : 'AI'}</span></div>
        {['Intent','Source','Motion','Proof','Ship'].map((x,i)=><div key={x} className="orbit-chip" style={{'--i':i,'--p':p}}>{x}</div>)}
      </div>
    );
  }

  if(template === 'slice-poster' || template === 'roller-blind'){
    return (
      <div className="surface clean premium-slices">
        {header(Film)}
        <div className="slice-wall" style={{'--p':p}}>
          {Array.from({length:8},(_,i)=><span key={i} style={{'--i':i}} />)}
          <h1>{template === 'slice-poster' ? 'Poster splits reveal product proof' : 'Spring blind reveals the hero'}</h1>
        </div>
      </div>
    );
  }

  if(template === 'liquid-cta'){
    return (
      <div className="surface dark premium-liquid-cta">
        {header(Zap)}
        <button className="liquid-button" style={{'--p':p}}><span>Start the motion system</span></button>
      </div>
    );
  }

  if(template === 'magnetic-menu' || template === 'spotlight-menu' || template === 'noise-nav'){
    const labels = ['Studio','Work','Systems','Contact'];
    return (
      <div className="surface ink premium-menu">
        {header(MousePointer2)}
        <nav style={{'--p':p}}>
          {labels.map((label,i)=><button key={label} className={i===Math.min(3, Math.floor(p*4))?'active':''}>{String(i+1).padStart(2,'0')} {label}</button>)}
        </nav>
      </div>
    );
  }

  if(template === 'split-transition' || template === 'water-transition'){
    return (
      <div className="surface dark premium-transition">
        {header(PanelTop)}
        <div className="transition-panels" style={{'--p':p}}>
          <span />
          <span />
          <h1>{template === 'water-transition' ? 'Liquid page handoff' : 'Split route handoff'}</h1>
        </div>
      </div>
    );
  }

  if(template === 'calendar-brush'){
    return (
      <div className="surface clean premium-calendar">
        {header(BarChart3)}
        <div className="calendar-grid" style={{'--p':p}}>
          {Array.from({length:35},(_,i)=><button key={i} className={i <= p*34 && i % 3 !== 1 ? 'active' : ''}>{i % 7 === 0 ? '9a' : ''}</button>)}
        </div>
      </div>
    );
  }

  if(template === 'metric-scrub' || template === 'micro-charts'){
    return (
      <div className="surface blue premium-metrics">
        {header(BarChart3)}
        <div className="grid-3">
          {['Revenue','Risk','Velocity'].map((label,i)=>(
            <div className="metric" key={label}><span>{label}</span><b>{Math.round((p + .2) * [180,74,112][i])}</b><svg viewBox="0 0 160 70"><path d={`M5 58 C40 ${52-p*34} 74 ${18+i*12} 112 ${48-p*28} S140 ${22+p*18} 155 ${16+i*8}`} /></svg></div>
          ))}
        </div>
      </div>
    );
  }

  if(template === 'ai-stream'){
    const lines = ['Reading source set','Finding contradictions','Attaching citations','Ready to adapt'];
    return (
      <div className="surface dark premium-stream">
        {header(Command)}
        <div className="stream-lines">
          {lines.map((line,i)=><div key={line} className={i<=step?'visible':''}><span>{line}</span><b>{82+i*4}%</b></div>)}
        </div>
      </div>
    );
  }

  if(template === 'shelf-pulse'){
    return (
      <div className="surface clean premium-shelves">
        {header(Database)}
        {Array.from({length:5},(_,row)=><div className="shelf-row" key={row}>{Array.from({length:10},(_,i)=><span key={i} className={(i+row+step)%7===0?'hot':''} />)}</div>)}
      </div>
    );
  }

  if(template === 'stacked-cards' || template === 'mask-proof'){
    return (
      <div className="surface clean premium-stack">
        {header(Layers)}
        {[0,1,2,3,4].map(i=><article key={i} style={{'--i':i,'--p':p}}><span>0{i+1}</span><h2>{template === 'mask-proof' ? 'Masked proof quote' : 'Pinned dossier card'}</h2></article>)}
      </div>
    );
  }

  if(template === 'depth-marquee'){
    return (
      <div className="surface dark premium-marquee">
        {header(ArrowRight)}
        {[0,1].map(row=><div className="marquee-track" key={row} style={{'--p':p,'--dir':row?1:-1}}>{Array.from({length:8},(_,i)=><span key={i}>Partner {i+1}</span>)}</div>)}
      </div>
    );
  }

  if(template === 'elastic-faq'){
    return (
      <div className="surface clean premium-faq">
        {header(ChevronRight)}
        {[0,1,2,3,4].map(i=><section key={i} className={i===step?'open':''}><b>How does this motion help?</b><p>It exposes state, hierarchy, and timing without asking the viewer to guess.</p></section>)}
      </div>
    );
  }

  if(template === 'team-spotlight'){
    return (
      <div className="surface ink premium-team">
        {header(MousePointer2)}
        <div className="team-grid" style={{'--p':p}}>{Array.from({length:12},(_,i)=><button key={i} className={i===step+3?'active':''}><span>Role {i+1}</span></button>)}</div>
      </div>
    );
  }

  if(template === 'stats-band'){
    return (
      <div className="surface clean premium-stats">
        {header(Gauge)}
        {['42','87','12'].map((n,i)=><div key={n} className="stat-card" style={{'--i':i,'--p':p}}><b>{Math.round(Number(n) * (.45 + p))}</b><span>proof metric</span></div>)}
      </div>
    );
  }

  return <SimpleWorkbench meta={meta} />;
}

const components = {
  'three-product': ThreeProductStage,
  'gsap-cascade': GsapCascade,
  'shader-gallery': ShaderGallery,
  'fluid-cursor': FluidCursor,
  'scroll-mask': ScrollMaskPanels,
  'particle-field': ParticleField,
  'flip-board': FlipBoard,
  'split-text': SplitTextDeck,
  motion: PremiumEffectSurface,
  'type-dissolve': PremiumEffectSurface,
  'ripple-grid': PremiumEffectSurface,
  'orbit-stage': PremiumEffectSurface,
  constellation: PremiumEffectSurface,
  'slice-poster': PremiumEffectSurface,
  'liquid-cta': PremiumEffectSurface,
  'magnetic-menu': PremiumEffectSurface,
  'radial-command': PremiumEffectSurface,
  'split-transition': PremiumEffectSurface,
  'spotlight-menu': PremiumEffectSurface,
  'calendar-brush': PremiumEffectSurface,
  'metric-scrub': PremiumEffectSurface,
  'ai-stream': PremiumEffectSurface,
  'shelf-pulse': PremiumEffectSurface,
  'stacked-cards': PremiumEffectSurface,
  'mask-proof': PremiumEffectSurface,
  'depth-marquee': PremiumEffectSurface,
  'elastic-faq': PremiumEffectSurface,
  'team-spotlight': PremiumEffectSurface,
  'stats-band': PremiumEffectSurface,
  'command-room': CommandRoom,
  search: SearchMorph,
  'alert-lens': CommandRoom,
  'thought-map': AgentTrace,
  'agent-trace': AgentTrace,
  lineage: MapSurface,
  evidence: EvidenceSurface,
  dashboard: DashboardSurface,
  metrics: DashboardSurface,
  calendar: DashboardSurface,
  inventory: DashboardSurface,
  'table-xray': DashboardSurface,
  security: SecuritySurface,
  kanban: KanbanBoard,
  pricing: PricingWorkbench,
  'glass-switch': props => <GlassControls {...props} mode="switch" />,
  'glass-slider': props => <GlassControls {...props} mode="slider" />,
  'glass-toggle': props => <GlassControls {...props} mode="toggle" />,
  'video-controls': props => <GlassControls {...props} mode="video" />,
  dock: DockSurface,
  gallery: GallerySurface,
  masonry: GallerySurface,
  carousel: GallerySurface,
  'clip-gallery': GallerySurface,
  compare: ComparisonSurface,
  device: DeviceMorph,
  annotation: AnnotationSurface,
  'code-stepper': CodeStepper,
  onboarding: OnboardingSurface,
  'type-hero': TypeHero,
  'shader-nav': ShaderNavigation,
  roller: SimpleWorkbench,
  'size-magnet': SizeMagnet,
  'cursor-index': CursorIndex,
  timeline: TimelineSurface,
  'video-card': GallerySurface,
  audio: AudioMixer,
  map: MapSurface,
  'case-flip': GallerySurface,
  world: GallerySurface,
  'video-grid': GallerySurface,
};

createRoot(document.getElementById('root')).render(<App />);
