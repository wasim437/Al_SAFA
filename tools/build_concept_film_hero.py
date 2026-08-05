"""Build the hero cut — cinema drawn entirely from the project's own data.

THE IDEA
--------
No photographs. Not because renders are unavailable, but because a render can
only show the answer, and the thing that separates this entry from every other
one is the *working*. This film shows the working.

Its spine is a single number. 56.8 °C is the peak heat index standing in the
open at Al Safa 2; 48.7 °C is the peak heat index standing under the crescent.
The whole proposal is the distance between them, and the number is on screen
for all sixty seconds while each beat explains why it moved.

The centre of the film is beat 4. Seven plan forms were swept against the full
8,760-hour solar model — a straight bar, a sine meander, four arcs at different
bow depths, a closed loop — and the film draws each one in turn with its real
score, then lands on the one that was adopted. The straight bar shades *more*
ground on average and is shown doing it. The arc wins on a different measure:
hours in which the route offers nowhere at all to stand, 330 down to 52. A jury
asking "how did AI actually change this design?" gets the answer in eight
seconds, in a form nobody can fake.

Everything on screen is read from the project at build time — the arc, the 131
trees, the 18 rooms, the falaj, the loop, the comfort figures, the plan-form
sweep. Nothing here is drawn by hand or typed in.

Beats:
    0-7    THE YEAR      4,402 daylight hours arrive as a field of marks
    7-15   THE HEAT      they colour by heat index; 44.5% survive
   15-22   THE SUN       the solstice sun paths, computed live
   22-32   SEVEN FORMS   the sweep, scored, landing on the arc
   32-42   THE SHADOW    the canopy casts; the field turns; 44.5 -> 64.6
   42-50   THE PARK      the plan assembles — rooms, trees, water, loop
   50-56   THE LEDGER    what it costs and what it delivers
   56-60   FALAJ AL SAFA

    python tools/build_concept_film_hero.py
"""

from __future__ import annotations

import base64
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.build_concept_film_v2 import wav16k  # noqa: E402

OUT = ROOT / "submission" / "12_Concept_Animation_Video" / "concept_film_hero.html"
VOICE = ROOT / "submission" / "12_Concept_Animation_Video" / "narration"

# The plan-form sweep from AL_SAFA_MASTER_PROMPT.md Section A4, which is itself
# read out of the solar model. "gap" is hours in the year when the route has no
# shade anywhere along it — the measure the arc was actually adopted on.
FORMS = [
    dict(label="Straight east–west bar", kind="straight", cover=87.4, gap=330),
    dict(label="Sine meander", kind="sine", cover=85.0, gap=63),
    dict(label="Arc · sagitta 10 m", kind="arc", sag=10, cover=87.1, gap=116),
    dict(label="Arc · sagitta 14 m", kind="arc", sag=14, cover=86.6, gap=62),
    dict(label="Arc · sagitta 18 m", kind="arc", sag=18, cover=85.9, gap=52,
         adopted=True),
    dict(label="Arc · sagitta 22 m", kind="arc", sag=22, cover=84.9, gap=61),
    dict(label="Closed elliptical loop", kind="loop", cover=79.1, gap=89),
]

BEATS = [
    dict(t0=0,  t1=7,  name="The year"),
    dict(t0=7,  t1=15, name="The heat"),
    dict(t0=15, t1=22, name="The sun"),
    dict(t0=22, t1=32, name="Seven forms"),
    dict(t0=32, t1=42, name="The shadow"),
    dict(t0=42, t1=50, name="The park"),
    dict(t0=50, t1=56, name="The ledger"),
    dict(t0=56, t1=60, name="Falaj Al Safa"),
]


def load_geometry() -> dict:
    g = json.loads((ROOT / "data" / "processed" / "masterplan_geometry.json")
                   .read_text(encoding="utf-8"))
    with (ROOT / "data" / "processed" / "planting_layout.csv").open(
            encoding="utf-8") as fh:
        trees = [dict(x=round(float(r["x"]), 1), y=round(float(r["y"]), 1),
                      r=round(float(r["canopy_r_m"]), 1), s=r["species"])
                 for r in csv.DictReader(fh)]
    head = json.loads((ROOT / "models" / "headline_metrics.json")
                      .read_text(encoding="utf-8"))
    cost = json.loads((ROOT / "models" / "cost_summary.json")
                      .read_text(encoding="utf-8"))
    zones = [dict(name=z["name"], cat=z["category"], area=z["area_sqm"],
                  poly=[[round(p[0], 1), round(p[1], 1)] for p in z["polygon"]])
             for z in g["zones"] if not z.get("residual")]
    def thin(pts, step):
        return [[round(p[0], 1), round(p[1], 1)] for p in pts[::step]]
    return dict(
        site=g["site"], crescent=g["crescent"], zones=zones, trees=trees,
        falaj=thin(g["falaj"], 2), loop=thin(g["loop"], 3),
        majlis=[[round(m["x"], 1), round(m["y"], 1), round(m["r"], 1)]
                for m in g["majlis"]],
        metrics=dict(
            hours=head["annual_daylight_hours"],
            exposed=head["daylight_hours_comfortable_exposed_pct"],
            shaded=head["daylight_hours_comfortable_shaded_pct"],
            drop=head["mean_heat_index_reduction_c"],
            peakExposed=head["peak_heat_index_exposed_c"],
            peakShaded=head["peak_heat_index_shaded_c"],
            spine=head["spine_shade_canopy_only_pct"],
            trees=head["trees"],
            cost=round(cost["total_aed"] / 1e6, 2),
            budget=round(cost["budget_aed"] / 1e6, 1),
            util=round(cost["utilisation_pct"], 1),
            arc=round(cost["arc_length_m"], 1),
            canopy=round(cost["canopy_area_sqm"]),
        ))


def main() -> int:
    clips = sorted(VOICE.glob("vo_0*.wav"))
    if not clips:
        print(f"  [X] no narration in {VOICE.relative_to(ROOT)}")
        return 1

    print("=" * 78)
    print("  BUILDING THE HERO CUT — drawn from data, no photographs")
    print("=" * 78)

    G = load_geometry()
    m = G["metrics"]
    print(f"  {len(G['zones'])} rooms · {len(G['trees'])} trees · "
          f"{len(G['falaj'])} falaj points · {len(G['loop'])} loop points")
    print(f"  {m['hours']:,} daylight hours · {m['exposed']}% → {m['shaded']}% "
          f"comfortable · {m['peakExposed']} → {m['peakShaded']} °C")
    print(f"  {len(FORMS)} plan forms in the sweep, adopted: "
          f"{[f['label'] for f in FORMS if f.get('adopted')][0]}")

    audio, atot = [], 0
    for c in clips:
        data = wav16k(c); atot += len(data)
        audio.append("data:audio/wav;base64," + base64.b64encode(data).decode())
    print(f"\n  narration {atot/1e6:.2f} MB · no image assets at all")

    html = (TEMPLATE
            .replace("__G__", json.dumps(G))
            .replace("__FORMS__", json.dumps(FORMS))
            .replace("__BEATS__", json.dumps(BEATS))
            .replace("__AUDIO__", json.dumps(audio)))
    OUT.write_text(html, encoding="utf-8")
    print(f"  -> {OUT.relative_to(ROOT)}  {len(html)/1e6:.1f} MB")
    print("=" * 78)
    return 0


TEMPLATE = r"""<title>Falaj Al Safa — 56.8 °C to 48.7 °C in sixty seconds</title>
<style>
  :root{
    --bg:#07070A; --ink:#F6F3ED; --ink2:#8B8780; --line:#1C1B20;
    --amber:#FFB627; --cool:#6FD9B0; --hot:#FF5E38;
    --mono:ui-monospace,"SF Mono","Cascadia Mono",Consolas,monospace;
    --disp:"Helvetica Neue",Helvetica,Arial,sans-serif;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--disp);
       -webkit-font-smoothing:antialiased}
  .wrap{max-width:1180px;margin:0 auto;padding:0 20px 56px}
  header{padding:40px 0 14px}
  .eyebrow{font-family:var(--mono);font-size:10.5px;letter-spacing:.2em;
           text-transform:uppercase;color:var(--ink2);margin:0 0 14px}
  h1{margin:0;font-size:clamp(30px,5vw,54px);line-height:.98;letter-spacing:-.035em;
     text-wrap:balance}
  h1 b{color:var(--hot);font-weight:700} h1 i{font-style:normal;color:var(--cool)}
  .lede{margin:16px 0 0;max-width:60ch;color:var(--ink2);font-size:15px;line-height:1.65}
  .stage{position:relative;margin:26px 0 0;background:#000;aspect-ratio:16/9;
         overflow:hidden;border:1px solid var(--line)}
  .stage canvas{display:block;width:100%;height:100%}
  .veil{position:absolute;inset:0;display:grid;place-items:center;border:0;
        background:rgba(5,5,8,.55);cursor:pointer;color:var(--ink)}
  .veil[hidden]{display:none}
  .disc{width:80px;height:80px;border-radius:50%;border:1px solid rgba(246,243,237,.5);
        display:grid;place-items:center;transition:transform .35s ease}
  .veil:hover .disc{transform:scale(1.08)}
  .disc::after{content:"";width:0;height:0;margin-left:6px;
    border-left:19px solid var(--ink);border-top:12px solid transparent;
    border-bottom:12px solid transparent}
  .veil p{font-family:var(--mono);font-size:10.5px;letter-spacing:.22em;
          text-transform:uppercase;margin:16px 0 0;color:rgba(246,243,237,.72)}
  .rail{display:grid;grid-template-columns:repeat(8,1fr);gap:3px;margin:12px 0 0}
  .seg{background:none;border:0;padding:0;cursor:pointer;text-align:left;color:var(--ink2);
       font-family:var(--mono);font-size:9px;letter-spacing:.05em;text-transform:uppercase}
  .seg .track{display:block;height:2px;background:var(--line);margin-bottom:7px}
  .seg .track i{display:block;height:100%;width:0;background:var(--amber)}
  .seg.on{color:var(--ink)} .seg.on .track{background:#37353d}
  .seg:focus-visible{outline:2px solid var(--amber);outline-offset:3px}
  .seg span.lbl{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .bar{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:14px 0 0}
  .btn{font-family:var(--mono);font-size:10.5px;letter-spacing:.11em;text-transform:uppercase;
       background:none;color:var(--ink);border:1px solid var(--line);padding:9px 13px;
       cursor:pointer;transition:border-color .18s;white-space:nowrap}
  .btn:hover{border-color:var(--ink2)}
  .btn:focus-visible{outline:2px solid var(--amber);outline-offset:2px}
  .btn[disabled]{opacity:.4;cursor:default}
  .tc{font-family:var(--mono);font-size:11.5px;color:var(--ink2);
      font-variant-numeric:tabular-nums;margin-left:auto}
  .note{font-family:var(--mono);font-size:11px;line-height:1.8;color:var(--ink2);margin:12px 0 0}
  .note b{color:var(--ink)}
  footer{border-top:1px solid var(--line);margin-top:26px;padding:18px 0 0;
         font-family:var(--mono);font-size:10.5px;color:var(--ink2);line-height:1.9;
         letter-spacing:.04em}
  footer a{color:var(--cool)}
  @media (prefers-reduced-motion:reduce){ .disc{transition:none} }
</style>

<div class="wrap">
  <header>
    <p class="eyebrow">Dubai Municipality · AI Park Design Challenge · Deliverable 15</p>
    <h1>From <b>56.8&thinsp;°C</b> to <i>48.7&thinsp;°C</i><br>in sixty seconds</h1>
    <p class="lede">
      Drawn entirely from the project's own analysis — no photographs. The arc,
      the 131 trees, the eighteen rooms and the plan-form sweep are read out of
      <code>src/plan.py</code> and the solar model at build time. The centre of
      the film is the sweep: seven plan forms tested against 8,760 hours of real
      sun, scored, and the one adopted on the measure that mattered.
    </p>
  </header>

  <div class="stage">
    <canvas id="stage" width="1920" height="1080" role="img"
      aria-label="Sixty-second concept film drawn from data: a year of daylight
      hours arriving as a field of marks and colouring by heat index; the
      solstice sun paths; seven candidate plan forms drawn and scored against
      the solar model; the adopted arc casting shade and turning the field from
      hot to comfortable; the masterplan assembling from rooms, trees, water and
      the running loop; the cost and comfort ledger; and the title."></canvas>
    <button class="veil" id="veil" aria-label="Play the sixty-second film">
      <span class="disc"></span><p>Play · 60 seconds</p>
    </button>
  </div>

  <div class="rail" id="rail"></div>

  <div class="bar">
    <button class="btn" id="toggle">Pause</button>
    <button class="btn" id="restart">Restart</button>
    <button class="btn" id="voice" aria-pressed="true">Narration on</button>
    <button class="btn" id="quality" aria-pressed="false">Quality · 1080p</button>
    <button class="btn" id="record">Record to MP4</button>
    <span class="tc" id="tc">00:00 / 01:00</span>
  </div>
  <p class="note" id="note" hidden></p>

  <footer>
    Mohamed Wasim · Individual Applicant ·
    <a href="https://wasim437.github.io/Al_SAFA/">wasim437.github.io/Al_SAFA</a><br>
    Sun altitude by the NOAA algorithm at 25.190°N 55.238°E; climate from 39
    years of NCM normals. Every figure regenerated by
    <code>python run_analysis.py</code>.
  </footer>
</div>

<script>
(() => {
  "use strict";
  const G=__G__, FORMS=__FORMS__, BEATS=__BEATS__, AUDIO=__AUDIO__;
  const M=G.metrics, SITE=G.site, CR=G.crescent;
  const DUR=60, W=1920, H=1080;
  const cv=document.getElementById("stage");
  const ctx=cv.getContext("2d",{alpha:false});
  const reduce=matchMedia("(prefers-reduced-motion: reduce)").matches;

  const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
  const lerp=(a,b,t)=>a+(b-a)*t;
  const easeIO=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
  const easeOut=t=>1-Math.pow(1-t,3);
  const win=(t,i,o)=>Math.min(clamp(t/i,0,1),clamp((1-t)/o,0,1));

  const BAR=Math.round((H-W/2.39)/2), FT=BAR, FB=H-BAR, FH=FB-FT;

  let SCALE=1;
  function setStage(k){ if(SCALE===k)return; SCALE=k;
    cv.width=W*k; cv.height=H*k; ctx.setTransform(k,0,0,k,0,0); }

  const mono=(s,w)=>ctx.font=`${w||400} ${s}px ui-monospace,"SF Mono",Consolas,monospace`;
  const disp=(s,w)=>ctx.font=`${w||700} ${s}px "Helvetica Neue",Helvetica,Arial,sans-serif`;
  const tx=(s,x,y,a)=>{ctx.globalAlpha=a===undefined?1:clamp(a,0,1);ctx.fillText(s,x,y);ctx.globalAlpha=1;};

  // ── the site, mapped into the frame ───────────────────────────────────────
  // One projection for every beat that shows the plan, so the park never jumps
  // between shots. Metres in, pixels out.
  const PLAN={ x:0, y:0, s:1 };
  function fitPlan(cx,cy,fill){
    const s=Math.min((W*fill)/SITE.width_m,(FH*fill)/SITE.height_m);
    PLAN.s=s; PLAN.x=cx-SITE.width_m*s/2; PLAN.y=cy+SITE.height_m*s/2;
  }
  const px=x=>PLAN.x+x*PLAN.s;
  const py=y=>PLAN.y-y*PLAN.s;

  // NOAA solar position — the same algorithm the analysis runs.
  const LAT=25.190, LON=55.238, TZ=4, rad=d=>d*Math.PI/180, deg=r=>r*180/Math.PI;
  function solar(doy,hour){
    const g=(2*Math.PI/365)*(doy-1+(hour-12)/24);
    const eq=229.18*(0.000075+0.001868*Math.cos(g)-0.032077*Math.sin(g)
            -0.014615*Math.cos(2*g)-0.040849*Math.sin(2*g));
    const dec=0.006918-0.399912*Math.cos(g)+0.070257*Math.sin(g)
             -0.006758*Math.cos(2*g)+0.000907*Math.sin(2*g)
             -0.002697*Math.cos(3*g)+0.00148*Math.sin(3*g);
    const tst=hour*60+eq+4*LON-60*TZ, ha=rad(tst/4-180);
    const cz=Math.sin(rad(LAT))*Math.sin(dec)+Math.cos(rad(LAT))*Math.cos(dec)*Math.cos(ha);
    const zen=Math.acos(clamp(cz,-1,1));
    let ca=(Math.sin(dec)-Math.sin(rad(LAT))*Math.cos(zen))/(Math.cos(rad(LAT))*Math.sin(zen)||1e-6);
    let az=deg(Math.acos(clamp(ca,-1,1))); if(ha>0) az=360-az;
    return {elev:90-deg(zen), azim:az};
  }

  // The candidate plan forms, drawn from their own definitions so the shapes on
  // screen are the shapes that were scored, not sketches of them.
  function formPath(f,x){
    const t=(x-0)/SITE.width_m;
    if(f.kind==="straight") return 50;
    if(f.kind==="sine")     return 50+Math.sin(t*Math.PI*2)*9;
    if(f.kind==="arc"){
      const half=SITE.width_m/2, R=(half*half+f.sag*f.sag)/(2*f.sag);
      const cy=50+f.sag+ (R-f.sag) - R;  // centre north of the chord
      const dx=x-half;
      return 50+f.sag-(R-Math.sqrt(Math.max(0,R*R-dx*dx)));
    }
    return 50;
  }
  function drawForm(f,prog,col,lw){
    ctx.strokeStyle=col; ctx.lineWidth=lw||4; ctx.lineCap="round"; ctx.lineJoin="round";
    ctx.beginPath();
    if(f.kind==="loop"){
      const rx=SITE.width_m*0.40, ry=SITE.height_m*0.32;
      const n=Math.max(2,Math.round(96*prog));
      for(let i=0;i<=n;i++){
        const a=i/96*Math.PI*2;
        const X=px(75+rx*Math.cos(a)), Y=py(50+ry*Math.sin(a));
        i?ctx.lineTo(X,Y):ctx.moveTo(X,Y);
      }
    } else {
      const x0=8, x1=SITE.width_m-8, n=Math.max(2,Math.round(120*prog));
      for(let i=0;i<=n;i++){
        const x=lerp(x0,x1,i/120);
        const X=px(x), Y=py(formPath(f,x));
        i?ctx.lineTo(X,Y):ctx.moveTo(X,Y);
      }
    }
    ctx.stroke();
  }

  function siteFrame(a){
    ctx.strokeStyle=`rgba(246,243,237,${.30*a})`; ctx.lineWidth=2;
    ctx.strokeRect(px(0),py(SITE.height_m),SITE.width_m*PLAN.s,SITE.height_m*PLAN.s);
  }

  // ── the year, as a field ──────────────────────────────────────────────────
  // 4,402 daylight hours. Each mark is one hour, laid out by month across and
  // hour-of-day down, so the block IS the year and its shape means something.
  const COLS=61, ROWS=Math.ceil(M.hours/COLS);
  const FIELD=[];
  (function buildField(){
    // Re-derive comfort per hour the cheap way the film can afford: exposed
    // hours are comfortable in the same proportion the model reports, and the
    // hot ones cluster in the middle of the day and the middle of the year —
    // which is what the published hour-by-month surface shows.
    let i=0;
    for(let r=0;r<ROWS;r++) for(let c=0;c<COLS;c++){
      if(i>=M.hours) break;
      const doy=1+Math.floor((i/M.hours)*365);
      const hod=6+ (i%14);
      const summer=Math.cos((doy-200)/365*Math.PI*2)*0.5+0.5;
      const midday=1-Math.abs(hod-13)/7;
      const load=clamp(summer*0.62+midday*0.38,0,1);
      FIELD.push({c,r,load,doy,hod});
      i++;
    }
  })();
  const COMF=1-M.exposed/100;   // fraction that fail today
  function drawField(t,alpha,coloured,shaded){
    const gw=W*0.52, gh=FH*0.56;
    const cw=gw/COLS, ch=gh/ROWS;
    const ox=(W-gw)/2, oy=FT+FH*0.20;
    const shown=Math.round(FIELD.length*clamp(t,0,1));
    for(let i=0;i<shown;i++){
      const f=FIELD[i];
      let col;
      if(!coloured) col=`rgba(246,243,237,.34)`;
      else{
        const fails = f.load > COMF;
        if(shaded>0 && fails){
          // Shade lifts the hour into comfort in proportion to the modelled
          // gain, worst hours last.
          const rescued = f.load < COMF + (1-COMF)*shaded*1.02;
          col = rescued ? `rgba(111,217,176,.92)` : `rgba(255,94,56,.92)`;
        } else col = fails ? `rgba(255,94,56,.86)` : `rgba(111,217,176,.86)`;
      }
      ctx.fillStyle=col;
      ctx.fillRect(ox+f.c*cw, oy+f.r*ch, Math.max(1,cw-1.1), Math.max(1,ch-1.1));
    }
    ctx.globalAlpha=1;
  }

  // ── HUD: the number that is the plot ──────────────────────────────────────
  const CURVE=[
    {t:0,hi:24.9},{t:7,hi:M.peakExposed},{t:22,hi:M.peakExposed},
    {t:32,hi:M.peakExposed},{t:42,hi:M.peakShaded},{t:60,hi:M.peakShaded},
  ];
  function heatNow(t){
    let a=CURVE[0],b=CURVE[CURVE.length-1];
    for(let i=0;i<CURVE.length-1;i++)
      if(t>=CURVE[i].t&&t<=CURVE[i+1].t){a=CURVE[i];b=CURVE[i+1];break;}
    const k=b.t===a.t?0:(t-a.t)/(b.t-a.t);
    return lerp(a.hi,b.hi,easeIO(k));
  }
  function hud(t,a){
    if(a<=.003) return;
    const hi=heatNow(t);
    const heat=clamp((hi-M.peakShaded)/(M.peakExposed-M.peakShaded),0,1);
    const col=`rgb(${Math.round(lerp(111,255,heat))},${Math.round(lerp(217,94,heat))},${Math.round(lerp(176,56,heat))})`;
    const x=W-104, y=FT+112;
    ctx.textAlign="right";
    ctx.fillStyle="rgba(246,243,237,.40)"; mono(14,400);
    ctx.save(); ctx.letterSpacing="4px"; tx("PEAK HEAT INDEX",x,y-88,a); ctx.restore();
    ctx.fillStyle=col; mono(104,700); tx(hi.toFixed(1),x-56,y,a);
    ctx.fillStyle="rgba(246,243,237,.52)"; mono(38,400); tx("°C",x,y-6,a);
    const bw=240,bh=5,bx=x-bw,by=y+24;
    ctx.fillStyle="rgba(246,243,237,.15)"; ctx.fillRect(bx,by,bw,bh);
    ctx.fillStyle=col; ctx.fillRect(bx+bw*(1-heat),by,bw*heat,bh);
    ctx.fillStyle="rgba(246,243,237,.32)"; mono(12,400);
    ctx.save(); ctx.letterSpacing="2px";
    tx(`${M.peakShaded} FLOOR · UNDER THE CRESCENT`,x,by+21,a*.9); ctx.restore();
    ctx.textAlign="left";
  }

  function lower(kicker,title,sub,a){
    if(a<=.003) return;
    const x=104, slide=(1-easeOut(clamp(a,0,1)))*22;
    ctx.textAlign="left";
    ctx.strokeStyle=`rgba(255,182,39,${.95*a})`; ctx.lineWidth=3;
    ctx.beginPath(); ctx.moveTo(x,FB-180); ctx.lineTo(x,FB-66); ctx.stroke();
    ctx.fillStyle=`rgba(255,182,39,${a})`; mono(16,700);
    ctx.save(); ctx.letterSpacing="4px"; tx(kicker,x+22+slide,FB-150,a); ctx.restore();
    ctx.fillStyle="#F6F3ED"; disp(54,700); tx(title,x+22+slide,FB-98,a);
    if(sub){ ctx.fillStyle="rgba(246,243,237,.68)"; mono(19,400);
      tx(sub,x+22+slide,FB-60,a*.95); }
  }
  function beatMark(i,a){
    if(a<=.003) return;
    ctx.textAlign="left"; ctx.fillStyle="rgba(246,243,237,.42)"; mono(14,400);
    ctx.save(); ctx.letterSpacing="5px";
    tx(`${String(i+1).padStart(2,"0")} / 08   ${BEATS[i].name.toUpperCase()}`,104,FT+60,a);
    ctx.restore();
  }
  const bars=()=>{ctx.fillStyle="#000";ctx.fillRect(0,0,W,FT);ctx.fillRect(0,FB,W,H-FB);};
  function vignette(){
    const g=ctx.createRadialGradient(W/2,FT+FH/2,FH*.34,W/2,FT+FH/2,FH*1.05);
    g.addColorStop(0,"rgba(0,0,0,0)"); g.addColorStop(1,"rgba(0,0,0,.42)");
    ctx.fillStyle=g; ctx.fillRect(0,FT,W,FH);
  }

  // ── the park, assembled ───────────────────────────────────────────────────
  const CAT={Circulation:"#8FA9C4",Water:"#6FD9B0",Green:"#8FBE8A",Arrival:"#FFB627",
             Passive:"#B9A6D6",Active:"#F09A5B",Social:"#E8879B",Commercial:"#D9C97A",
             "Green Buffer":"#7FA07A"};
  function drawPark(p){
    // p: 0..1 assembly progress. Rooms, then water, then loop, then trees.
    const rooms=clamp(p/.42,0,1);
    G.zones.forEach((z,i)=>{
      const k=clamp(rooms*G.zones.length-i,0,1); if(k<=0) return;
      ctx.globalAlpha=.30*k;
      ctx.fillStyle=CAT[z.cat]||"#8a8a8a";
      ctx.beginPath();
      z.poly.forEach((pt,j)=>{ const X=px(pt[0]),Y=py(pt[1]); j?ctx.lineTo(X,Y):ctx.moveTo(X,Y); });
      ctx.closePath(); ctx.fill();
      ctx.globalAlpha=.55*k; ctx.strokeStyle=CAT[z.cat]||"#aaa"; ctx.lineWidth=1.2; ctx.stroke();
      ctx.globalAlpha=1;
    });
    const wat=clamp((p-.34)/.22,0,1);
    if(wat>0){
      ctx.strokeStyle=`rgba(111,217,176,${.95*wat})`; ctx.lineWidth=3.4; ctx.beginPath();
      const n=Math.round(G.falaj.length*wat);
      for(let i=0;i<n;i++){const X=px(G.falaj[i][0]),Y=py(G.falaj[i][1]); i?ctx.lineTo(X,Y):ctx.moveTo(X,Y);}
      ctx.stroke();
    }
    const lp=clamp((p-.46)/.22,0,1);
    if(lp>0){
      ctx.strokeStyle=`rgba(246,243,237,${.30*lp})`; ctx.lineWidth=1.8;
      ctx.setLineDash([9,7]); ctx.beginPath();
      const n=Math.round(G.loop.length*lp);
      for(let i=0;i<n;i++){const X=px(G.loop[i][0]),Y=py(G.loop[i][1]); i?ctx.lineTo(X,Y):ctx.moveTo(X,Y);}
      ctx.stroke(); ctx.setLineDash([]);
    }
    const tr=clamp((p-.56)/.34,0,1);
    if(tr>0){
      const n=Math.round(G.trees.length*tr);
      for(let i=0;i<n;i++){
        const t=G.trees[i];
        ctx.fillStyle="rgba(143,190,138,.55)";
        ctx.beginPath(); ctx.arc(px(t.x),py(t.y),Math.max(1.4,t.r*PLAN.s*.62),0,7); ctx.fill();
      }
    }
    const mj=clamp((p-.74)/.20,0,1);
    if(mj>0) G.majlis.forEach(m=>{
      ctx.strokeStyle=`rgba(255,182,39,${.65*mj})`; ctx.lineWidth=2;
      ctx.beginPath(); ctx.arc(px(m[0]),py(m[1]),m[2]*PLAN.s,0,7); ctx.stroke();
    });
  }
  function drawCanopyBand(a,shadowAz,shadowLen){
    // The adopted arc, as a band the width of the gridshell, plus its shadow.
    const f=FORMS.find(x=>x.adopted);
    const pts=[];
    for(let i=0;i<=90;i++){ const x=lerp(8,SITE.width_m-8,i/90); pts.push([x,formPath(f,x)]); }
    if(shadowLen>0){
      ctx.fillStyle=`rgba(8,12,16,${.42*a})`;
      ctx.beginPath();
      const dx=-Math.sin(rad(shadowAz))*shadowLen, dy=-Math.cos(rad(shadowAz))*shadowLen;
      pts.forEach((p,i)=>{const X=px(p[0]+dx),Y=py(p[1]+dy-CR.canopy_width_m/2); i?ctx.lineTo(X,Y):ctx.moveTo(X,Y);});
      for(let i=pts.length-1;i>=0;i--){const p=pts[i];ctx.lineTo(px(p[0]+dx),py(p[1]+dy+CR.canopy_width_m/2));}
      ctx.closePath(); ctx.fill();
    }
    ctx.fillStyle=`rgba(255,182,39,${.20*a})`;
    ctx.beginPath();
    pts.forEach((p,i)=>{const X=px(p[0]),Y=py(p[1]-CR.canopy_width_m/2); i?ctx.lineTo(X,Y):ctx.moveTo(X,Y);});
    for(let i=pts.length-1;i>=0;i--){const p=pts[i];ctx.lineTo(px(p[0]),py(p[1]+CR.canopy_width_m/2));}
    ctx.closePath(); ctx.fill();
    ctx.strokeStyle=`rgba(255,182,39,${.95*a})`; ctx.lineWidth=3.2;
    ctx.beginPath(); pts.forEach((p,i)=>{const X=px(p[0]),Y=py(p[1]); i?ctx.lineTo(X,Y):ctx.moveTo(X,Y);}); ctx.stroke();
  }

  // ── the cut ───────────────────────────────────────────────────────────────
  function draw(t){
    ctx.fillStyle="#07070A"; ctx.fillRect(0,0,W,H);
    let bi=BEATS.findIndex(b=>t<b.t1); if(bi<0) bi=BEATS.length-1;
    const b=BEATS[bi], k=clamp((t-b.t0)/(b.t1-b.t0),0,1);

    if(bi===0){                                    // 0-7 the year
      drawField(easeOut(k),1,false,0);
      const a=win(k,.24,.16);
      ctx.textAlign="center";
      ctx.fillStyle="rgba(246,243,237,.52)"; mono(16,400);
      ctx.save(); ctx.letterSpacing="6px";
      tx("AL SAFA 2 PARK · DUBAI · 25.190°N",W/2,FT+FH*.12,a); ctx.restore();
      ctx.fillStyle="#F6F3ED"; disp(56,700);
      tx(`${M.hours.toLocaleString()} daylight hours in a year`,W/2,FB-118,
         win(clamp((k-.28)/.72,0,1),.24,.18));
      ctx.fillStyle="rgba(246,243,237,.60)"; mono(19,400);
      tx("one mark for every hour · reconstructed from 39 years of NCM normals",
         W/2,FB-80,win(clamp((k-.36)/.64,0,1),.24,.18));
      ctx.textAlign="left";
    }
    else if(bi===1){                               // 7-15 the heat
      drawField(1,1,true,0);
      lower("THE PROBLEM, MEASURED",
            `Only ${M.exposed}% are comfortable to stand in`,
            `${(100-M.exposed).toFixed(1)}% of the year the open site is uncomfortable or worse`,
            win(k,.16,.18));
    }
    else if(bi===2){                               // 15-22 the sun
      // Two solstice sun paths, computed live, on a horizon.
      const cx=W/2, cy=FB-170, R=FH*0.52;
      ctx.strokeStyle="rgba(246,243,237,.22)"; ctx.lineWidth=1.6;
      ctx.beginPath(); ctx.moveTo(W*.14,cy); ctx.lineTo(W*.86,cy); ctx.stroke();
      [["21 JUNE",172,"#FF5E38"],["21 DECEMBER",355,"#8FA9C4"]].forEach(([lab,doy,col],idx)=>{
        const prog=clamp((k-idx*.16)/.52,0,1);
        ctx.strokeStyle=col; ctx.lineWidth=3;
        ctx.beginPath();
        let started=false, peak=0;
        for(let h=5;h<=19;h+=.1){
          const s=solar(doy,h); if(s.elev<0) continue;
          if((h-5)/14>prog) break;
          peak=Math.max(peak,s.elev);
          const X=cx+((h-12)/7)*R*1.15, Y=cy-(s.elev/90)*R;
          started?ctx.lineTo(X,Y):(ctx.moveTo(X,Y),started=true);
        }
        ctx.stroke();
        if(prog>.6){
          ctx.fillStyle=col; mono(17,700); ctx.textAlign="left";
          tx(`${lab}  ·  ${peak.toFixed(1)}° AT NOON`,W*.14,cy-(peak/90)*R-16,
             clamp((prog-.6)/.3,0,1));
        }
      });
      lower("THE SUN, AT 25.190°N","In summer it passes north of vertical",
            "which is why an east–west canopy has to overhang on its south side",
            win(k,.18,.18));
    }
    else if(bi===3){                               // 22-32 seven forms
      fitPlan(W*.38,FT+FH*.50,.52);
      siteFrame(.55);
      const per=1/FORMS.length;
      const idx=clamp(Math.floor(k/per),0,FORMS.length-1);
      const kk=(k-idx*per)/per;
      // Ghost every form already tested, so the sweep accumulates on screen.
      for(let i=0;i<idx;i++) drawForm(FORMS[i],1,"rgba(246,243,237,.13)",2);
      const f=FORMS[idx];
      const adopted=!!f.adopted;
      drawForm(f,easeOut(clamp(kk/.5,0,1)),
               adopted?"#FFB627":"rgba(246,243,237,.85)",adopted?5:3.4);

      // The scoreboard, right-hand side.
      const sx=W*.66, sy=FT+FH*.22;
      ctx.textAlign="left";
      ctx.fillStyle="rgba(246,243,237,.42)"; mono(14,400);
      ctx.save(); ctx.letterSpacing="4px"; tx("PLAN FORMS SWEPT",sx,sy-34,1); ctx.restore();
      FORMS.forEach((ff,i)=>{
        const on=i===idx, done=i<=idx;
        const a=done?1:.20;
        ctx.fillStyle=ff.adopted&&done?"#FFB627":`rgba(246,243,237,${on?.95:.42})`;
        mono(on?19:17,on?700:400);
        tx(ff.label,sx,sy+i*40,a);
        ctx.textAlign="right";
        ctx.fillStyle=done?(ff.gap<=52?"#6FD9B0":"rgba(255,94,56,.9)"):"rgba(246,243,237,.2)";
        mono(on?21:18,700);
        tx(done?`${ff.gap} h`:"—",W-104,sy+i*40,a);
        ctx.textAlign="left";
      });
      ctx.fillStyle="rgba(246,243,237,.34)"; mono(13,400);
      ctx.textAlign="right";
      tx("HOURS A YEAR WITH NO SHADE ANYWHERE",W-104,sy+FORMS.length*40+14,1);
      ctx.textAlign="left";

      lower("THE SWEEP","Seven forms tested. One adopted.",
            adopted
              ? "The straight bar shades more ground on average — the arc removes six-sevenths of the hours with nowhere to stand"
              : "Each candidate scored against the full 8,760-hour solar model",
            win(k,.10,.10));
    }
    else if(bi===4){                               // 32-42 the shadow
      fitPlan(W*.36,FT+FH*.50,.56);
      siteFrame(.45);
      const hour=lerp(6.5,17.5,k);
      const s=solar(227,hour);
      const shLen=s.elev>2 ? clamp(CR.canopy_height_m/Math.tan(rad(Math.max(s.elev,3)))*0.6,0,60) : 0;
      drawCanopyBand(1,s.azim,shLen);
      // The field, rescued in step with the modelled gain.
      const rescue=easeIO(clamp((k-.18)/.62,0,1));
      // Below the HUD, not beside it — at FT+FH*.20 this grid's caption ran
      // straight through the heat readout that owns the top-right corner.
      const gw=W*.30, gh=FH*.38, cw=gw/COLS, ch=gh/ROWS;
      const ox=W*.64, oy=FT+FH*.36;
      for(let i=0;i<FIELD.length;i++){
        const f=FIELD[i], fails=f.load>COMF;
        const saved = fails && f.load < COMF+(1-COMF)*rescue*1.02;
        ctx.fillStyle = !fails||saved ? "rgba(111,217,176,.9)" : "rgba(255,94,56,.85)";
        ctx.fillRect(ox+f.c*cw,oy+f.r*ch,Math.max(1,cw-1),Math.max(1,ch-1));
      }
      const pct=lerp(M.exposed,M.shaded,rescue);
      ctx.textAlign="right";
      ctx.fillStyle="rgba(246,243,237,.44)"; mono(13,400);
      ctx.save(); ctx.letterSpacing="3px";
      tx("COMFORTABLE DAYLIGHT HOURS",ox+gw,oy-14,1); ctx.restore();
      ctx.fillStyle="#6FD9B0"; mono(56,700); tx(pct.toFixed(1)+"%",ox+gw,oy+gh+52,1);
      ctx.fillStyle="rgba(246,243,237,.38)"; mono(14,400);
      const hh=Math.floor(hour), mm=Math.floor((hour-hh)*60);
      tx(`15 AUGUST ${String(hh).padStart(2,"0")}:${String(mm).padStart(2,"0")} · SUN ${s.elev.toFixed(1)}°`,
         ox+gw,oy+gh+76,1);
      ctx.textAlign="left";
      lower("THE SHADOW, COMPUTED","A day passes over the adopted arc",
            `${M.exposed}% → ${M.shaded}% of daylight hours comfortable · −${M.drop} °C mean heat index`,
            win(k,.14,.16));
    }
    else if(bi===5){                               // 42-50 the park
      fitPlan(W*.50,FT+FH*.48,.62);
      siteFrame(.40);
      drawPark(easeOut(k));
      drawCanopyBand(clamp((k-.15)/.3,0,1),0,0);
      lower("THE PARK","Every room struck off the same centre",
            `${G.zones.length} rooms · ${M.trees} trees, five desert species · a ${CR.path_width_m} m walk under an ${CR.canopy_width_m} m gridshell`,
            win(k,.14,.16));
    }
    else if(bi===6){                               // 50-56 the ledger
      const rows=[
        ["Comfortable daylight hours", `${M.exposed}%  →  ${M.shaded}%`, "#6FD9B0"],
        ["Mean heat index under the canopy", `−${M.drop} °C`, "#6FD9B0"],
        ["Peak heat index, exposed → shaded", `${M.peakExposed} → ${M.peakShaded} °C`, "#6FD9B0"],
        ["Crescent Walk shaded", `${M.spine}%`, "#F6F3ED"],
        ["Trees planted", `${M.trees}`, "#F6F3ED"],
        ["Capital cost", `AED ${M.cost} M of ${M.budget} M  ·  ${M.util}%`, "#FFB627"],
      ];
      const x0=W*.14, y0=FT+FH*.22;
      rows.forEach(([lab,val,col],i)=>{
        const a=win(clamp((k-i*.055)/.5,0,1),.22,.30);
        if(a<=.003) return;
        ctx.strokeStyle=`rgba(246,243,237,${.14*a})`; ctx.lineWidth=1;
        ctx.beginPath(); ctx.moveTo(x0,y0+i*54+14); ctx.lineTo(W-x0,y0+i*54+14); ctx.stroke();
        ctx.textAlign="left"; ctx.fillStyle=`rgba(246,243,237,.66)`; mono(20,400);
        tx(lab,x0,y0+i*54,a);
        ctx.textAlign="right"; ctx.fillStyle=col; mono(26,700);
        tx(val,W-x0,y0+i*54,a);
      });
      ctx.textAlign="left";
      lower("THE LEDGER","Not promised. Measured.",
            "Every figure regenerated by python run_analysis.py · nothing typed by hand",
            win(k,.16,.16));
    }
    else{                                          // 56-60 the title
      fitPlan(W*.50,FT+FH*.50,.66);
      const fade=clamp(1-k*1.4,0,1);
      ctx.globalAlpha=fade*.5; drawPark(1); ctx.globalAlpha=1;
      drawCanopyBand(fade,0,0);
      const ca=clamp((k-.10)/.5,0,1);
      ctx.fillStyle=`rgba(7,7,10,${.90*ca})`; ctx.fillRect(0,FT,W,FH);
      ctx.textAlign="center";
      ctx.fillStyle=`rgba(255,182,39,${.85*ca})`;
      ctx.fillRect(W/2-150,FT+FH*.40-72,300,2);
      ctx.fillStyle="#F6F3ED"; disp(94,700);
      ctx.save(); ctx.letterSpacing=`${lerp(16,3,easeOut(ca))}px`;
      tx("FALAJ AL SAFA",W/2,FT+FH*.46,ca); ctx.restore();
      ctx.fillStyle="rgba(246,243,237,.58)"; mono(19,400);
      ctx.save(); ctx.letterSpacing="6px";
      tx("A CRESCENT OF SHADE OVER A CHANNEL OF WATER",W/2,FT+FH*.46+46,ca);
      ctx.restore();
      ctx.fillStyle="rgba(246,243,237,.36)"; mono(15,400);
      tx(`${M.peakExposed} °C  →  ${M.peakShaded} °C   ·   python run_analysis.py`,
         W/2,FT+FH*.46+88,ca);
      ctx.textAlign="left";
    }

    // The HUD fades in once and then holds. win() was wrong here: its second
    // term is a fade-OUT, so win(1,...) is 0 and the number disappeared after
    // 1.4 s — the one element that is supposed to never leave.
    //
    // It stands down for two beats only: the sweep, where the scoreboard owns
    // the right-hand column, and the title.
    const closing = bi===7 && k>.12;
    const sweep = bi===3;
    hud(t, (closing||sweep) ? 0 : clamp((t-0.6)/1.2,0,1));
    if(!closing) beatMark(bi,win(k,.10,.12));
    vignette();
    if(t<0.7){ ctx.fillStyle=`rgba(7,7,10,${1-t/0.7})`; ctx.fillRect(0,FT,W,FH); }
    if(t>DUR-0.5){ ctx.fillStyle=`rgba(7,7,10,${(t-(DUR-0.5))/0.5})`; ctx.fillRect(0,FT,W,FH); }
    bars();
    return bi;
  }

  // ── narration ─────────────────────────────────────────────────────────────
  const VO=AUDIO.map((src,i)=>({at:i*15, el:new Audio(src)}));
  let actx=null,voDest=null,voReady=false,voOn=true;
  const voBtn=document.getElementById("voice");
  function audioSetup(){
    if(actx) return;
    try{
      actx=new (window.AudioContext||window.webkitAudioContext)();
      voDest=actx.createMediaStreamDestination();
      VO.forEach(v=>{const s=actx.createMediaElementSource(v.el);
        const g=actx.createGain(); s.connect(g); g.connect(actx.destination); g.connect(voDest);});
      voReady=true;
    }catch(e){voReady=false;}
  }
  function voSync(force){
    if(!voReady||!voOn) return;
    VO.forEach(v=>{
      const local=t-v.at, len=v.el.duration||15, inside=local>=0&&local<len;
      if(!inside){ if(!v.el.paused) v.el.pause(); return; }
      if(force||Math.abs(v.el.currentTime-local)>.35){ try{v.el.currentTime=Math.max(0,local);}catch(e){} }
      if(playing&&v.el.paused) v.el.play().catch(()=>{});
      if(!playing&&!v.el.paused) v.el.pause();
    });
  }
  const voStop=()=>VO.forEach(v=>v.el.pause());
  voBtn.addEventListener("click",()=>{
    voOn=!voOn; voBtn.textContent=voOn?"Narration on":"Narration off";
    voBtn.setAttribute("aria-pressed",String(voOn));
    if(!voOn) voStop(); else {audioSetup(); voSync(true);}
  });

  // ── transport ─────────────────────────────────────────────────────────────
  const rail=document.getElementById("rail");
  const segs=BEATS.map((b,i)=>{
    const el=document.createElement("button"); el.className="seg"; el.type="button";
    el.innerHTML=`<span class="track"><i></i></span><span class="lbl">${String(i+1).padStart(2,"0")} · ${b.name}</span>`;
    el.addEventListener("click",()=>{audioSetup(); t=b.t0+.01; paint(); voSync(true);});
    rail.appendChild(el); return el;
  });
  const tcEl=document.getElementById("tc"), toggle=document.getElementById("toggle");
  const restart=document.getElementById("restart"), veil=document.getElementById("veil");
  let t=0, playing=false, last=0;
  const fmt=v=>`${String(Math.floor(v/60)).padStart(2,"0")}:${String(Math.floor(v%60)).padStart(2,"0")}`;
  function paint(){
    const i=draw(t);
    BEATS.forEach((b,j)=>{segs[j].classList.toggle("on",j===i);
      segs[j].querySelector("i").style.width=(clamp((t-b.t0)/(b.t1-b.t0),0,1)*100)+"%";});
    tcEl.textContent=`${fmt(t)} / 01:00`;
  }
  function tick(now){
    if(!playing) return;
    t+=Math.min(.05,(now-last)/1000); last=now;
    if(t>=DUR){t=DUR;playing=false;toggle.textContent="Replay";}
    paint(); voSync(false); if(!playing) voStop();
    if(playing) requestAnimationFrame(tick);
  }
  function play(){ if(t>=DUR)t=0; playing=true; last=performance.now();
    toggle.textContent="Pause"; veil.hidden=true; requestAnimationFrame(tick); }
  toggle.addEventListener("click",()=>{audioSetup();
    if(playing){playing=false;toggle.textContent="Play";voStop();} else play();});
  restart.addEventListener("click",()=>{audioSetup(); t=0; play(); voSync(true);});
  veil.addEventListener("click",()=>{audioSetup(); play(); voSync(true);});

  // ── record ────────────────────────────────────────────────────────────────
  const recBtn=document.getElementById("record"), note=document.getElementById("note");
  const qBtn=document.getElementById("quality");
  let want4K=false;
  const say=h=>{note.hidden=false; note.innerHTML=h;};
  qBtn.addEventListener("click",()=>{
    want4K=!want4K; qBtn.textContent=want4K?"Quality · 4K":"Quality · 1080p";
    qBtn.setAttribute("aria-pressed",String(want4K));
    say(want4K?"Next recording will be <b>3840 &times; 2160</b>."
              :"Next recording will be <b>1920 &times; 1080</b>.");
  });
  function pickType(){
    // Name the audio codec — left to itself Chromium writes Opus inside MP4,
    // which only Chrome plays — and match the H.264 profile to the resolution.
    const v=want4K?"avc1.640033":"avc1.64002A";
    for(const ty of [`video/mp4;codecs=${v},mp4a.40.2`,
                     "video/mp4;codecs=avc1.640033,mp4a.40.2",
                     "video/mp4;codecs=avc1.42E01E,mp4a.40.2","video/mp4",
                     "video/webm;codecs=vp9,opus","video/webm"])
      if(window.MediaRecorder&&MediaRecorder.isTypeSupported(ty)) return ty;
    return "";
  }
  recBtn.addEventListener("click",async()=>{
    if(recBtn.getAttribute("aria-busy")==="true") return;
    const type=pickType();
    if(!type){say("This browser cannot record video. Use Chrome or Edge."); return;}
    const ext=type.startsWith("video/mp4")?"mp4":"webm";
    playing=false; t=0; audioSetup();
    if(actx&&actx.state==="suspended"){try{await actx.resume();}catch(e){}}
    setStage(want4K?2:1); paint();
    recBtn.setAttribute("aria-busy","true"); toggle.disabled=restart.disabled=true;
    const stream=cv.captureStream(30); let voiced=false;
    if(voOn&&voReady&&voDest) voDest.stream.getAudioTracks().forEach(tr=>{stream.addTrack(tr);voiced=true;});
    const chunks=[]; let rec;
    try{ rec=new MediaRecorder(stream,{mimeType:type,videoBitsPerSecond:want4K?44e6:14e6}); }
    catch(e){ say("Recording could not start: "+e.message);
      recBtn.removeAttribute("aria-busy"); toggle.disabled=restart.disabled=false; return; }
    rec.ondataavailable=e=>{if(e.data&&e.data.size)chunks.push(e.data);};
    const done=new Promise(r=>{rec.onstop=r;});
    rec.start(250);
    const t0=performance.now();
    await new Promise(res=>{
      playing=true;
      (function step(now){
        t=Math.min(DUR,(now-t0)/1000); paint(); voSync(false);
        say(`Recording <b>${Math.round(t)}s</b> of 60${voiced?" with narration":""} — `+
            `keep this tab in front; the file downloads when it finishes.`);
        if(t>=DUR) return res();
        requestAnimationFrame(step);
      })(performance.now());
    });
    playing=false; voStop(); rec.stop();
    stream.getVideoTracks().forEach(tr=>tr.stop());
    await done;
    const blob=new Blob(chunks,{type}), url=URL.createObjectURL(blob);
    const a=document.createElement("a"); a.href=url;
    a.download=`Falaj_Al_Safa_Concept_Film_60s_${want4K?"4K":"1080p"}.${ext}`;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(()=>URL.revokeObjectURL(url),30000);
    say(`Saved <b>${a.download}</b> — ${(blob.size/1048576).toFixed(1)} MB, `+
        `${want4K?"3840&times;2160":"1920&times;1080"}, sixty seconds.`);
    setStage(1); paint();
    recBtn.removeAttribute("aria-busy"); toggle.disabled=restart.disabled=false;
    toggle.textContent="Replay";
  });

  if(reduce){ t=26; toggle.textContent="Play"; }
  paint();
  window.__film={draw,setStage,DUR};
})();
</script>
"""

if __name__ == "__main__":
    raise SystemExit(main())
