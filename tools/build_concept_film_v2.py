"""Build the presentation cut of the sixty-second concept film.

WHY THIS EXISTS
---------------
concept_film.html draws the park live from src/plan.py — accurate, and it
looks like geometry on a canvas. An earlier cut of the six renders on their
own looked like a place and said nothing about how the place was arrived at;
it was dropped in favour of this one, which does both.

This one is the argument. It moves between the renders and the analysis that
produced them, because that movement *is* the entry: every other proposal will
show a beautiful park, and almost none can show the ray-traced comfort surface
underneath it, the section solved against real solstice angles, and a comfort
figure that rises because the geometry was swept rather than styled.

Seven beats in sixty seconds:

    0-8    the site        the aerial, and the name
    8-16   the problem     the comfort surface, 56.8 °C climbing
   16-24   the move        the section drawn against real sun angles
   24-34   beneath it      standing under the canopy, -7.13 °C
   34-42   the rooms       the oasis basin and the dune play
   42-50   life            the souk, and what pays for the park
   50-60   the proof       44.5% -> 64.6%, then the park after dark

Assets are downsampled and inlined. A canvas that has drawn an image fetched
from a sibling path is tainted and cannot be recorded, and an artifact has a
16 MB ceiling — so images go in at 1920 px wide and quality 82, narration at
16 kHz mono, which is 3.9 MB before base64 rather than 9.2 MB.

    python tools/build_concept_film_v2.py

Writes submission/12_Concept_Animation_Video/concept_film_presentation.html
"""

from __future__ import annotations

import base64
import io
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

OUT = ROOT / "submission" / "12_Concept_Animation_Video" / "concept_film_presentation.html"
VOICE = ROOT / "submission" / "12_Concept_Animation_Video" / "narration"

# name -> (path, target width). Renders stay at native width; the drawings are
# read close-up so they get more pixels than they are shown at.
ASSETS = {
    "aerial":  ("design/renders/Aerial/masterplan_aerial_golden_hour.jpg", 1920),
    "walk":    ("design/renders/Eye_Level/spine_corridor_interior.jpg", 1920),
    "oasis":   ("design/renders/Eye_Level/oasis_basin.jpg", 1920),
    "play":    ("design/renders/Day/childrens_dune_play.jpg", 1920),
    "souk":    ("design/renders/Day/souk_plaza.jpg", 1920),
    "night":   ("design/renders/Night/night_plaza_render_1784970565232.jpg", 1920),
    "plan":    ("figures/fig10_masterplan.png", 1800),
    "section": ("design/visuals/section_crescent.png", 1800),
    "heatmap": ("figures/fig04_site_comfort_map.png", 1800),
}

CHAPTERS = [
    dict(t0=0,  t1=8,  name="The site"),
    dict(t0=8,  t1=16, name="The problem"),
    dict(t0=16, t1=24, name="The move"),
    dict(t0=24, t1=34, name="Beneath it"),
    dict(t0=34, t1=42, name="The rooms"),
    dict(t0=42, t1=50, name="Life"),
    dict(t0=50, t1=60, name="The proof"),
]


def jpeg(rel: str, width: int) -> bytes:
    from PIL import Image
    with Image.open(ROOT / rel) as im:
        im = im.convert("RGB")
        if im.width > width:
            im = im.resize((width, round(im.height * width / im.width)),
                           Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=82, optimize=True, progressive=True)
        return buf.getvalue()


def wav16k(src: Path) -> bytes:
    """Resample to 16 kHz mono in the browser — no audio library needed, and
    the same engine that will play it back does the conversion."""
    from playwright.sync_api import sync_playwright
    JS = """
    async (b64) => {
      const bin=atob(b64); const a=new Uint8Array(bin.length);
      for(let i=0;i<bin.length;i++)a[i]=bin.charCodeAt(i);
      const ac=new AudioContext(); const ab=await ac.decodeAudioData(a.buffer);
      const R=16000;
      const off=new OfflineAudioContext(1, Math.ceil(ab.duration*R), R);
      const s=off.createBufferSource(); s.buffer=ab; s.connect(off.destination); s.start();
      const out=await off.startRendering(); const ch=out.getChannelData(0);
      let pk=0; for(let i=0;i<ch.length;i++) pk=Math.max(pk,Math.abs(ch[i]));
      const g = pk>0 ? Math.min(3, 0.90/pk) : 1;
      const pcm=new Int16Array(ch.length);
      for(let i=0;i<ch.length;i++){ let v=Math.max(-1,Math.min(1,ch[i]*g));
        pcm[i]= v<0?v*0x8000:v*0x7fff; }
      const by=new Uint8Array(pcm.buffer); let s2='';
      for(let i=0;i<by.length;i+=0x8000) s2+=String.fromCharCode.apply(null,by.subarray(i,i+0x8000));
      return btoa(s2);
    }"""
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(); pg.goto("about:blank")
        raw = base64.b64decode(
            pg.evaluate(JS, base64.b64encode(src.read_bytes()).decode()))
        b.close()
    return (b"RIFF" + struct.pack("<I", 36 + len(raw)) + b"WAVEfmt " +
            struct.pack("<IHHIIHH", 16, 1, 1, 16000, 32000, 2, 16) +
            b"data" + struct.pack("<I", len(raw)) + raw)


def main() -> int:
    for _n, (rel, _w) in ASSETS.items():
        if not (ROOT / rel).exists():
            print(f"  [X] missing asset: {rel}")
            return 1
    clips = sorted(VOICE.glob("vo_0*.wav"))
    if not clips:
        print(f"  [X] no narration in {VOICE.relative_to(ROOT)}")
        return 1

    print("=" * 78)
    print("  BUILDING THE PRESENTATION CUT")
    print("=" * 78)

    imgs, tot = {}, 0
    for name, (rel, w) in ASSETS.items():
        data = jpeg(rel, w)
        tot += len(data)
        imgs[name] = "data:image/jpeg;base64," + base64.b64encode(data).decode()
        print(f"  {name:9} {len(data)/1024:6.0f} KB   {rel}")

    print()
    audio, atot = [], 0
    for c in clips:
        data = wav16k(c)
        atot += len(data)
        audio.append("data:audio/wav;base64," + base64.b64encode(data).decode())
        print(f"  {c.name:9} {len(data)/1024:6.0f} KB   16 kHz mono")

    print(f"\n  images {tot/1e6:.2f} MB · audio {atot/1e6:.2f} MB")

    html = (TEMPLATE
            .replace("__IMG__", json.dumps(imgs))
            .replace("__AUDIO__", json.dumps(audio))
            .replace("__CHAPTERS__", json.dumps(CHAPTERS)))
    OUT.write_text(html, encoding="utf-8")
    print(f"  -> {OUT.relative_to(ROOT)}  {len(html)/1e6:.1f} MB")
    print("=" * 78)
    return 0


TEMPLATE = r"""<title>Falaj Al Safa — Al Safa 2 Park in sixty seconds</title>
<style>
  :root{
    --bg:#0A0A0C; --panel:#111114; --ink:#F4F1EC; --ink2:#9A958C; --line:#232227;
    --amber:#FFB627; --cool:#7FB8A4; --hot:#E8712F;
    --mono:ui-monospace,"SF Mono","Cascadia Mono",Consolas,monospace;
    --disp:"Helvetica Neue",Helvetica,Arial,sans-serif;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--disp);
       -webkit-font-smoothing:antialiased}
  .wrap{max-width:1180px;margin:0 auto;padding:0 20px 56px}
  header{padding:38px 0 16px}
  .eyebrow{font-family:var(--mono);font-size:10.5px;letter-spacing:.2em;
           text-transform:uppercase;color:var(--ink2);margin:0 0 12px}
  h1{margin:0;font-size:clamp(28px,4.6vw,46px);line-height:1;letter-spacing:-.03em;
     text-wrap:balance}
  h1 em{font-style:normal;color:var(--ink2)}
  .lede{margin:14px 0 0;max-width:62ch;color:var(--ink2);font-size:15px;line-height:1.62}
  .stage{position:relative;margin:24px 0 0;background:#000;aspect-ratio:16/9;
         overflow:hidden;border:1px solid var(--line)}
  .stage canvas{display:block;width:100%;height:100%}
  .veil{position:absolute;inset:0;display:grid;place-items:center;border:0;
        background:rgba(8,8,10,.5);cursor:pointer;color:var(--ink)}
  .veil[hidden]{display:none}
  .disc{width:78px;height:78px;border-radius:50%;border:1px solid rgba(244,241,236,.5);
        display:grid;place-items:center;transition:transform .35s ease}
  .veil:hover .disc{transform:scale(1.07)}
  .disc::after{content:"";width:0;height:0;margin-left:6px;
    border-left:18px solid var(--ink);border-top:11px solid transparent;
    border-bottom:11px solid transparent}
  .veil p{font-family:var(--mono);font-size:10.5px;letter-spacing:.22em;
          text-transform:uppercase;margin:15px 0 0;color:rgba(244,241,236,.72)}
  .rail{display:grid;grid-template-columns:repeat(7,1fr);gap:3px;margin:12px 0 0}
  .seg{background:none;border:0;padding:0;cursor:pointer;text-align:left;color:var(--ink2);
       font-family:var(--mono);font-size:9.5px;letter-spacing:.06em;text-transform:uppercase}
  .seg .track{display:block;height:2px;background:var(--line);margin-bottom:7px}
  .seg .track i{display:block;height:100%;width:0;background:var(--amber)}
  .seg.on{color:var(--ink)} .seg.on .track{background:#3a3840}
  .seg:focus-visible{outline:2px solid var(--amber);outline-offset:3px}
  .seg span.lbl{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .bar{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:14px 0 0}
  .btn{font-family:var(--mono);font-size:10.5px;letter-spacing:.11em;text-transform:uppercase;
       background:none;color:var(--ink);border:1px solid var(--line);padding:9px 13px;
       cursor:pointer;white-space:nowrap;transition:border-color .18s}
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
  @media (prefers-reduced-motion: reduce){ .disc{transition:none} }
</style>

<div class="wrap">
  <header>
    <p class="eyebrow">Dubai Municipality · AI Park Design Challenge · Deliverable 15</p>
    <h1>Falaj Al Safa<br><em>Al Safa 2 Park in sixty seconds</em></h1>
    <p class="lede">
      A crescent of shade over a channel of water. This cut moves between the
      proposal and the analysis that produced it — the ray-traced comfort
      surface, the section solved against real solstice angles, and a comfort
      figure that rises because the geometry was swept rather than styled.
      Every number shown is regenerated by the project's own pipeline.
    </p>
  </header>

  <div class="stage">
    <canvas id="stage" width="1920" height="1080" role="img"
      aria-label="Sixty-second concept film: an aerial of the proposed park, the
      site's measured heat, the canopy section solved against solstice sun
      angles, the shaded walk beneath it, the oasis basin and dune play, the
      souk plaza, the measured comfort result, and the park after dark."></canvas>
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
    Renders are artistic impressions of the analysed scheme. Plans, sections,
    the comfort surface and every quoted figure are computed —
    <code>python run_analysis.py</code>.
  </footer>
</div>

<script>
(() => {
  "use strict";
  const IMG = __IMG__, AUDIO = __AUDIO__, CH = __CHAPTERS__;
  const DUR = 60, W = 1920, H = 1080;
  const cv = document.getElementById("stage");
  const ctx = cv.getContext("2d", { alpha:false });
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
  const lerp=(a,b,t)=>a+(b-a)*t;
  const easeIO=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
  const easeOut=t=>1-Math.pow(1-t,3);
  const win=(t,i,o)=>Math.min(clamp(t/i,0,1),clamp((1-t)/o,0,1));

  // 2.39:1 inside a 16:9 canvas — the same frame as the other two cuts.
  const BAR=Math.round((H-W/2.39)/2), FT=BAR, FB=H-BAR, FH=FB-FT;

  let SCALE=1;
  function setStage(k){ if(SCALE===k)return; SCALE=k;
    cv.width=W*k; cv.height=H*k; ctx.setTransform(k,0,0,k,0,0); }

  const im = {}; let pending = Object.keys(IMG).length;
  for (const [k,src] of Object.entries(IMG)) {
    const i = new Image(); i.src = src;
    i.decode().then(()=>{pending--;}).catch(()=>{pending--;});
    im[k] = i;
  }

  const mono=(s,w)=>ctx.font=`${w||400} ${s}px ui-monospace,"SF Mono",Consolas,monospace`;
  const disp=(s,w)=>ctx.font=`${w||700} ${s}px "Helvetica Neue",Helvetica,Arial,sans-serif`;
  function tx(s,x,y,a){ ctx.globalAlpha=a===undefined?1:clamp(a,0,1); ctx.fillText(s,x,y); ctx.globalAlpha=1; }

  // Cover-fit a photo into the frame with a slow move across it.
  function photo(img,k,z0,z1,px,py,alpha){
    if(!img||!img.width) return;
    const z=lerp(z0,z1,easeIO(k));
    const s=Math.max(W/img.width,FH/img.height)*z;
    const dw=img.width*s, dh=img.height*s;
    ctx.globalAlpha=alpha===undefined?1:alpha;
    ctx.drawImage(img,(W-dw)/2+px*W*easeIO(k), FT+(FH-dh)/2+py*FH*easeIO(k), dw, dh);
    ctx.globalAlpha=1;
  }

  // Fit a drawing whole, on a paper field. Drawings are documents: they must
  // never be cropped, which is the opposite of what a photo wants.
  // A drawing is a document: never cropped, and never allowed to collide with
  // the caption. The lower third takes 210 px, so the plate is fitted into what
  // is left rather than into the whole frame — otherwise the figure's own
  // source line ends up printed underneath the film's title.
  function plate(img,k,alpha,wipe){
    if(!img||!img.width) return;
    ctx.globalAlpha=alpha===undefined?1:alpha;
    ctx.fillStyle="#F7F5F0"; ctx.fillRect(0,FT,W,FH);
    const pad=56, reserve=210, aw=W-pad*2, ah=FH-pad-reserve;
    const s=Math.min(aw/img.width, ah/img.height)*lerp(1.0,1.04,easeIO(k));
    const dw=img.width*s, dh=img.height*s;
    const dx=(W-dw)/2, dy=FT+pad+(ah-dh)/2;
    if(wipe!==undefined){
      ctx.save(); ctx.beginPath();
      ctx.rect(0,FT,W*clamp(wipe,0,1),FH); ctx.clip();
      ctx.drawImage(img,dx,dy,dw,dh); ctx.restore();
      if(wipe>0.002&&wipe<0.999){
        ctx.fillStyle="rgba(255,182,39,.9)"; ctx.fillRect(W*wipe-3,FT,3,FH);
      }
    } else ctx.drawImage(img,dx,dy,dw,dh);
    ctx.globalAlpha=1;
  }

  function grade(top,bot){
    let g=ctx.createLinearGradient(0,FT,0,FT+FH*.40);
    g.addColorStop(0,`rgba(6,6,9,${top===undefined?.60:top})`); g.addColorStop(1,"rgba(6,6,9,0)");
    ctx.fillStyle=g; ctx.fillRect(0,FT,W,FH*.40);
    g=ctx.createLinearGradient(0,FB-FH*.55,0,FB);
    g.addColorStop(0,"rgba(6,6,9,0)"); g.addColorStop(1,`rgba(6,6,9,${bot===undefined?.82:bot})`);
    ctx.fillStyle=g; ctx.fillRect(0,FB-FH*.55,W,FH*.55);
  }

  function lower(kicker,title,sub,a){
    if(a<=.003) return;
    const x=112, slide=(1-easeOut(clamp(a,0,1)))*20;
    ctx.textAlign="left";
    ctx.strokeStyle=`rgba(255,182,39,${.92*a})`; ctx.lineWidth=3;
    ctx.beginPath(); ctx.moveTo(x,FB-178); ctx.lineTo(x,FB-70); ctx.stroke();
    ctx.fillStyle=`rgba(255,182,39,${a})`; mono(16,700);
    ctx.save(); ctx.letterSpacing="4px"; tx(kicker,x+22+slide,FB-148,a); ctx.restore();
    ctx.fillStyle="#F4F1EC"; disp(50,700); tx(title,x+22+slide,FB-100,a);
    if(sub){ ctx.fillStyle="rgba(244,241,236,.70)"; mono(19,400); tx(sub,x+22+slide,FB-64,a*.95); }
  }

  function figure(big,small,a,colour){
    if(a<=.003) return;
    ctx.textAlign="right"; const x=W-112, y=FT+FH*.27;
    ctx.fillStyle=colour||`rgba(255,182,39,${a})`; mono(66,700); tx(big,x,y,a);
    ctx.fillStyle="rgba(244,241,236,.62)"; mono(14,400);
    ctx.save(); ctx.letterSpacing="3px"; tx(small,x,y+26,a*.9); ctx.restore();
    ctx.textAlign="left";
  }

  function chapterMark(i,a,onPaper){
    if(a<=.003) return;
    ctx.textAlign="left";
    ctx.fillStyle = onPaper ? `rgba(30,28,26,.52)` : `rgba(244,241,236,.48)`;
    mono(14,400);
    ctx.save(); ctx.letterSpacing="5px";
    tx(`${String(i+1).padStart(2,"0")} / 07   ${CH[i].name.toUpperCase()}`,112,FT+66,a);
    ctx.restore();
  }

  function bars(){ ctx.fillStyle="#000"; ctx.fillRect(0,0,W,FT); ctx.fillRect(0,FB,W,H-FB); }

  // ── the cut ───────────────────────────────────────────────────────────────
  function draw(t){
    ctx.fillStyle="#0A0A0C"; ctx.fillRect(0,0,W,H);
    let ci = CH.findIndex(c=>t<c.t1); if(ci<0) ci=CH.length-1;
    const c = CH[ci], k = clamp((t-c.t0)/(c.t1-c.t0),0,1);

    if(ci===0){                                    // 0-8  the site
      photo(im.aerial,k,1.14,1.00,.02,-.015);
      grade(.55,.80);
      const a=win(k,.14,.20);
      ctx.textAlign="center"; ctx.fillStyle="#F4F1EC"; disp(96,700);
      ctx.save(); ctx.letterSpacing=`${lerp(16,3,easeOut(clamp(k/.30,0,1)))}px`;
      tx("FALAJ AL SAFA",W/2,FT+FH*.44,a); ctx.restore();
      ctx.fillStyle="rgba(244,241,236,.62)"; mono(19,400);
      ctx.save(); ctx.letterSpacing="7px";
      tx("AL SAFA 2 PARK  ·  DUBAI  ·  15,000 m²",W/2,FT+FH*.44+46,a); ctx.restore();
      ctx.textAlign="left";
    }
    else if(ci===1){                               // 8-16 the problem
      plate(im.heatmap,k,1);
      // Paper needs the opposite grade — dark type on light ground.
      let g=ctx.createLinearGradient(0,FB-FH*.5,0,FB);
      g.addColorStop(0,"rgba(10,10,12,0)"); g.addColorStop(1,"rgba(10,10,12,.88)");
      ctx.fillStyle=g; ctx.fillRect(0,FB-FH*.5,W,FH*.5);
      const climb=easeOut(clamp((k-.10)/.45,0,1));
      figure((24.9+(56.8-24.9)*climb).toFixed(1)+" °C","PEAK HEAT INDEX, EXPOSED",
             win(k,.12,.22),`rgba(232,113,47,${win(k,.12,.22)})`);
      lower("THE PROBLEM, MEASURED","For 55.5% of daylight hours, unusable",
            "8,760 hours reconstructed from 39 years of NCM normals",win(k,.14,.18));
    }
    else if(ci===2){                               // 16-24 the move
      plate(im.section,k,1,easeIO(clamp(k/.55,0,1)));
      let g=ctx.createLinearGradient(0,FB-FH*.5,0,FB);
      g.addColorStop(0,"rgba(10,10,12,0)"); g.addColorStop(1,"rgba(10,10,12,.88)");
      ctx.fillStyle=g; ctx.fillRect(0,FB-FH*.5,W,FH*.5);
      lower("AL HILAL · THE CRESCENT CANOPY","One arc, 141 m in radius",
            "18 m gridshell 4.5 m over a 7 m walk · 3 m southern louvre · "+
            "solved against real solstice angles, not drawn by eye",win(k,.18,.16));
    }
    else if(ci===3){                               // 24-34 beneath it
      const xf=clamp((t-c.t0)/1.0,0,1);
      if(xf<1) plate(im.section,1,1);
      photo(im.walk,k,1.00,1.13,-.03,0,xf);
      grade(.42,.80);
      figure("−7.13 °C","MEAN HEAT INDEX UNDER THE CANOPY",win(k,.16,.20));
      lower("BENEATH IT · 15 AUGUST","Shade you can stand in",
            "8.1 °C off the peak in the hottest month in the record",win(k,.14,.18));
    }
    else if(ci===4){                               // 34-42 the rooms
      const half=clamp((t-c.t0)/(c.t1-c.t0),0,1);
      if(half<.52){ photo(im.oasis,half/.52,1.12,1.00,.03,.015); }
      else{
        photo(im.oasis,1,1.12,1.00,.03,.015);
        photo(im.play,(half-.52)/.48,1.00,1.12,.02,-.015,clamp((half-.52)/.10,0,1));
      }
      grade(.42,.80);
      figure("131","TREES · FIVE DESERT SPECIES",win(k,.16,.20));
      lower("THE ROOMS","Every room struck off the same centre",
            "No room is a rectangle; every room faces the crescent square-on",
            win(k,.14,.18));
    }
    else if(ci===5){                               // 42-50 life
      photo(im.souk,k,1.10,1.00,-.02,0);
      grade(.42,.80);
      figure("AED 27.0 M","OF AN AED 35 M BUDGET",win(k,.16,.20));
      lower("LIFE, AND WHAT PAYS FOR IT","Eight kiosks on the convex face",
            "Commercial floor placed to support running costs · 77% of budget",
            win(k,.14,.18));
    }
    else{                                          // 50-60 the proof
      const p = clamp((t-c.t0)/(c.t1-c.t0),0,1);
      if(p<.46){
        plate(im.plan,p/.46,1);
        let g=ctx.createLinearGradient(0,FB-FH*.5,0,FB);
        g.addColorStop(0,"rgba(10,10,12,0)"); g.addColorStop(1,"rgba(10,10,12,.90)");
        ctx.fillStyle=g; ctx.fillRect(0,FB-FH*.5,W,FH*.5);
        // The counter goes in the band the plate already reserves, not over the
        // drawing. Set on top of the plan it covered the room schedule and the
        // arrow between the two figures vanished into the linework.
        const rise=easeOut(clamp((p-.06)/.30,0,1));
        const a2=win(p/.46,.14,.20);
        ctx.textAlign="right";
        const rx=W-112, ry=FB-150;
        ctx.fillStyle=`rgba(244,241,236,.55)`; mono(14,400);
        ctx.save(); ctx.letterSpacing="5px";
        tx("COMFORTABLE DAYLIGHT HOURS",rx,ry-58,a2); ctx.restore();
        ctx.fillStyle=`rgba(127,184,164,${a2})`; mono(76,700);
        tx((44.5+20.1*rise).toFixed(1)+"%",rx,ry,a2);
        const gw=ctx.measureText((44.5+20.1*rise).toFixed(1)+"%").width;
        ctx.fillStyle=`rgba(244,241,236,.45)`; mono(34,400);
        tx("→",rx-gw-26,ry-8,a2);
        const aw2=ctx.measureText("→").width;
        ctx.fillStyle=`rgba(232,113,47,${a2})`; mono(76,700);
        tx("44.5%",rx-gw-aw2-52,ry,a2);
        ctx.textAlign="left";
        lower("THE PROOF","Not promised. Measured.",
              "Swept against 8,760 hours of real sun positions, one square metre "+
              "at a time",win(p/.46,.16,.18));
      } else {
        const q=(p-.46)/.54;
        photo(im.night,q,1.00,1.10,0,.015,clamp(q/.10,0,1));
        grade(.40,.86);
        const ca=clamp((q-.52)/.34,0,1);
        if(ca>.003){
          ctx.fillStyle=`rgba(8,8,10,${.88*ca})`; ctx.fillRect(0,FT,W,FH);
          ctx.textAlign="center";
          ctx.fillStyle=`rgba(255,182,39,${.8*ca})`; ctx.fillRect(W/2-140,FT+FH*.40-70,280,2);
          ctx.fillStyle="#F4F1EC"; disp(88,700);
          ctx.save(); ctx.letterSpacing=`${lerp(14,3,easeOut(ca))}px`;
          tx("FALAJ AL SAFA",W/2,FT+FH*.44,ca); ctx.restore();
          ctx.fillStyle="rgba(244,241,236,.58)"; mono(18,400);
          ctx.save(); ctx.letterSpacing="6px";
          tx("A CRESCENT OF SHADE OVER A CHANNEL OF WATER",W/2,FT+FH*.44+44,ca);
          ctx.restore();
          ctx.fillStyle="rgba(244,241,236,.34)"; mono(15,400);
          tx("Every figure reproducible:  python run_analysis.py",W/2,FT+FH*.44+86,ca);
          ctx.textAlign="left";
        } else {
          lower("AFTER DARK","The park does not close at sunset",
                "Nineteen lamps along the walk · the crescent lit from within",
                win(q,.14,.20));
        }
      }
    }

    // Beats 2 and 3 are drawings on paper, and so is the first half of beat 7.
    const onPaper = ci===1 || ci===2 || (ci===6 && k<.46);
    if(!(ci===6&&k>.75)) chapterMark(ci,win(k,.10,.12),onPaper);
    if(t<0.9){ ctx.fillStyle=`rgba(10,10,12,${1-t/0.9})`; ctx.fillRect(0,FT,W,FH); }
    if(t>DUR-0.7){ ctx.fillStyle=`rgba(10,10,12,${(t-(DUR-0.7))/0.7})`; ctx.fillRect(0,FT,W,FH); }
    bars();
    return ci;
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
  function voStop(){ VO.forEach(v=>v.el.pause()); }
  voBtn.addEventListener("click",()=>{
    voOn=!voOn; voBtn.textContent=voOn?"Narration on":"Narration off";
    voBtn.setAttribute("aria-pressed",String(voOn));
    if(!voOn) voStop(); else {audioSetup(); voSync(true);}
  });

  // ── transport ─────────────────────────────────────────────────────────────
  const rail=document.getElementById("rail");
  const segs=CH.map((c,i)=>{
    const b=document.createElement("button"); b.className="seg"; b.type="button";
    b.innerHTML=`<span class="track"><i></i></span><span class="lbl">${String(i+1).padStart(2,"0")} · ${c.name}</span>`;
    b.addEventListener("click",()=>{ audioSetup(); t=c.t0+.01; paint(); voSync(true); });
    rail.appendChild(b); return b;
  });
  const tcEl=document.getElementById("tc"), toggle=document.getElementById("toggle");
  const restart=document.getElementById("restart"), veil=document.getElementById("veil");
  let t=0, playing=false, last=0;
  const fmt=v=>`${String(Math.floor(v/60)).padStart(2,"0")}:${String(Math.floor(v%60)).padStart(2,"0")}`;
  function paint(){
    const i=draw(t);
    CH.forEach((c,j)=>{ segs[j].classList.toggle("on",j===i);
      segs[j].querySelector("i").style.width=(clamp((t-c.t0)/(c.t1-c.t0),0,1)*100)+"%"; });
    tcEl.textContent=`${fmt(t)} / 01:00`;
  }
  function tick(now){
    if(!playing) return;
    t+=Math.min(.05,(now-last)/1000); last=now;
    if(t>=DUR){ t=DUR; playing=false; toggle.textContent="Replay"; }
    paint(); voSync(false); if(!playing) voStop();
    if(playing) requestAnimationFrame(tick);
  }
  function play(){ if(t>=DUR)t=0; playing=true; last=performance.now();
    toggle.textContent="Pause"; veil.hidden=true; requestAnimationFrame(tick); }
  toggle.addEventListener("click",()=>{ audioSetup();
    if(playing){playing=false;toggle.textContent="Play";voStop();} else play(); });
  restart.addEventListener("click",()=>{ audioSetup(); t=0; play(); voSync(true); });
  veil.addEventListener("click",()=>{ audioSetup(); play(); voSync(true); });

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
    // Name the audio codec — left to itself Chromium writes Opus inside the
    // MP4, which only Chrome plays. And match the H.264 profile to the
    // resolution: avc1.42E01E is Baseline 3.0, specified for 720x480.
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
    if(!type){ say("This browser cannot record video. Use Chrome or Edge."); return; }
    const ext=type.startsWith("video/mp4")?"mp4":"webm";
    playing=false; t=0; audioSetup();
    if(actx&&actx.state==="suspended"){ try{await actx.resume();}catch(e){} }
    setStage(want4K?2:1); paint();
    recBtn.setAttribute("aria-busy","true"); toggle.disabled=restart.disabled=true;
    const stream=cv.captureStream(30); let voiced=false;
    if(voOn&&voReady&&voDest) voDest.stream.getAudioTracks().forEach(tr=>{stream.addTrack(tr);voiced=true;});
    const chunks=[]; let rec;
    try{ rec=new MediaRecorder(stream,{mimeType:type,videoBitsPerSecond:want4K?44e6:14e6}); }
    catch(e){ say("Recording could not start: "+e.message);
      recBtn.removeAttribute("aria-busy"); toggle.disabled=restart.disabled=false; return; }
    rec.ondataavailable=e=>{ if(e.data&&e.data.size) chunks.push(e.data); };
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

  if(reduce){ t=18; toggle.textContent="Play"; }
  const boot=setInterval(()=>{ if(pending<=0){ clearInterval(boot); paint(); } },60);
  paint();
  window.__film={draw,setStage,DUR};
})();
</script>
"""

if __name__ == "__main__":
    raise SystemExit(main())
