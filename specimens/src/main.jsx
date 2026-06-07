import React, { useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
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

const routeMeta = window.__FRAMEWELL_PATTERN_META__ || fallbackMeta;

const specimenKindById = {
  'spatial-command-room': 'command-room',
  'radial-command-wheel': 'command-room',
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
  const meta = routeMeta;
  const kind = specimenKindById[meta.id] || specimenKindById[meta.slug] || meta.template || 'dashboard';
  const Specimen = components[kind] || DashboardSurface;
  return (
    <main className="fw-root">
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

function Header({ meta, icon: Icon = Sparkles, action }){
  return (
    <div className="header-row">
      <div>
        <div className="eyebrow">{meta.behavior}</div>
        <h2>{meta.title}</h2>
      </div>
      {action || <button className="btn light" type="button"><Icon size={16} /> Live specimen</button>}
    </div>
  );
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

function DashboardSurface({ meta }){
  const [range, setRange] = useState(62);
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
  const columns = {
    Plan:['Audit weak previews','Choose component roles'],
    Build:['React specimen app','Pattern page wrapper','Card scaling'],
    Verify:['Modal route probe','Screenshot montage'],
  };
  return (
    <div className="surface clean">
      <Header meta={meta} icon={Layers} />
      <div className="grid-3" style={{height:400}}>
        {Object.entries(columns).map(([col,cards])=>(
          <div key={col} className="panel" style={{padding:14,background:active===col?'#15120d':'rgba(255,255,255,.72)',color:active===col?'#fff8eb':'#15120d'}}>
            <button className={`tab ${active===col?'active':''}`} onClick={()=>setActive(col)}>{col}</button>
            <div className="list" style={{marginTop:14}}>
              {cards.map((card,i)=><div key={card} className="row" style={{transform:active===col?`translateY(${-4+i*2}px)`:'none'}}><span className="avatar">{i+1}</span><span>{card}</span></div>)}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function DockSurface({ meta }){
  const [active,setActive]=useState(2);
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
  return (
    <div className="surface clean">
      <Header meta={meta} icon={Wand2} action={<button className="btn" onClick={()=>setN((n+1)%3)}><Zap size={16}/> Change state</button>} />
      <div className="grid-3" style={{height:390}}>
        {[0,1,2].map(i=><div key={i} className="panel" style={{padding:18,transform:n===i?'translateY(-12px)':'none',background:n===i?'#15120d':'rgba(255,255,255,.74)',color:n===i?'#fff8eb':'#15120d'}}><div className="eyebrow">State {i+1}</div><h2 style={{marginTop:12}}>{['Plan','Preview','Ship'][i]}</h2><p style={{marginTop:12,color:n===i?'rgba(255,246,229,.66)':'#716756'}}>A polished component state with explicit controls.</p></div>)}
      </div>
    </div>
  );
}

const components = {
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
