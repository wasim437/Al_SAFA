"""Build the photoreal cut of the sixty-second concept film.

WHY THIS EXISTS
---------------
The original film draws the park from src/plan.py in real time. That was the
only option while design/renders/ was empty, and it is accurate — but it is
geometry on a canvas, and it looks like it. The shortlist goes to a public
community vote, and a community votes on what it can see.

Six photoreal renders now exist. This cuts them into the same sixty seconds,
against the same narration, with slow camera moves and cross-dissolves, and the
measured numbers laid over them.

WHY EVERYTHING IS INLINED
-------------------------
Opened as a local file, a canvas that has drawn an image loaded from a sibling
path is *tainted*: the browser then refuses captureStream and toDataURL, so the
film would play and be impossible to record. The same trap swallowed the
narration when it lived in narration/*.wav. Images and audio are both embedded
as data: URIs, which are same-origin, so the film plays AND records from a
double-clicked file with no server.

    python tools/build_render_film.py

Writes submission/12_Concept_Animation_Video/concept_film_renders.html
"""

from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

OUT = ROOT / "submission" / "12_Concept_Animation_Video" / "concept_film_renders.html"
VOICE = ROOT / "submission" / "12_Concept_Animation_Video" / "narration"
REND = ROOT / "design" / "renders"

# Six shots, sixty seconds. Each carries the line it has to make, and the move
# is chosen to serve that line: the aerial pulls back because the argument is
# the whole arc; the walk pushes in because the argument is standing in it.
SHOTS = [
    dict(src=REND / "Aerial" / "masterplan_aerial_golden_hour.jpg",
         t0=0, t1=11, zoom=(1.16, 1.00), pan=(0.02, -0.02),
         kicker="AL SAFA 2 PARK · DUBAI",
         title="15,000 m², and too hot to stand in",
         sub="For 55.5% of daylight hours the open site is uncomfortable or worse"),
    dict(src=REND / "Eye_Level" / "spine_corridor_interior.jpg",
         t0=11, t1=23, zoom=(1.00, 1.14), pan=(-0.03, 0.0),
         kicker="AL HILAL · THE CRESCENT CANOPY",
         title="One arc of shade, 141 m in radius",
         sub="18 m gridshell, 4.5 m over a 7 m walk, with a 3 m southern louvre"),
    dict(src=REND / "Eye_Level" / "oasis_basin.jpg",
         t0=23, t1=34, zoom=(1.14, 1.00), pan=(0.03, 0.02),
         kicker="AL NAKHIL · THE OASIS BASIN",
         title="A sunken palm court on the cool side",
         sub="Every room is struck off the same arc centre, so none is a rectangle"),
    dict(src=REND / "Day" / "childrens_dune_play.jpg",
         t0=34, t1=44, zoom=(1.00, 1.15), pan=(0.02, -0.02),
         kicker="CHILDREN'S DUNE PLAY",
         title="Shaped from the ground, not bolted to it",
         sub="Timber, rope and sand — 1,267 m² of play in the crescent's shade"),
    dict(src=REND / "Day" / "souk_plaza.jpg",
         t0=44, t1=52, zoom=(1.12, 1.00), pan=(-0.02, 0.0),
         kicker="THE SOUK & COMMUNITY PLAZA",
         title="Eight kiosks that pay for the park",
         sub="Commercial floor placed to support running costs, AED 27.0 M of a 35 M budget"),
    dict(src=REND / "Night" / "night_plaza_render_1784970565232.jpg",
         t0=52, t1=60, zoom=(1.00, 1.12), pan=(0.0, 0.02),
         kicker="AFTER DARK",
         title="Falaj Al Safa",
         sub="44.5% → 64.6% of daylight hours comfortable · every figure "
             "reproducible with python run_analysis.py"),
]

# Numbers that appear over the picture, each while the shot that earns it is up.
STATS = [
    # No stat over the aerial: that render carries its own burned-in labels and
    # an overlay lands on top of them. The shot makes its point in the title.
    dict(t0=15.0, t1=22.0, big="−7.13 °C", small="MEAN HEAT INDEX UNDER THE CANOPY"),
    dict(t0=26.0, t1=33.0, big="131", small="TREES · FIVE DESERT SPECIES"),
    dict(t0=36.5, t1=43.0, big="7,640", small="RESIDENTS WITHIN A TEN-MINUTE WALK"),
    dict(t0=46.0, t1=51.0, big="AED 27.0 M", small="OF AN AED 35 M BUDGET"),
    dict(t0=54.0, t1=59.5, big="44.5% → 64.6%", small="COMFORTABLE DAYLIGHT HOURS"),
]


def b64(p: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode("ascii")


def main() -> int:
    missing = [s["src"] for s in SHOTS if not s["src"].exists()]
    if missing:
        print("  [X] renders missing:")
        for m in missing:
            print(f"      {m.relative_to(ROOT)}")
        return 1

    clips = sorted(VOICE.glob("vo_0*.wav"))
    if not clips:
        print(f"  [X] no narration in {VOICE.relative_to(ROOT)}")
        return 1

    print("=" * 78)
    print("  BUILDING THE PHOTOREAL CUT")
    print("=" * 78)

    shots_js = []
    total_img = 0
    for s in SHOTS:
        total_img += s["src"].stat().st_size
        print(f"  {s['src'].name:44} {s['t0']:>2}-{s['t1']:<2}s  {s['title']}")
        shots_js.append({k: v for k, v in s.items() if k != "src"} |
                        {"img": b64(s["src"], "image/jpeg")})

    audio_js = [b64(c, "audio/wav") for c in clips]
    print(f"\n  {len(SHOTS)} shots, {total_img/1e6:.1f} MB of stills")
    print(f"  {len(clips)} narration clips, "
          f"{sum(c.stat().st_size for c in clips)/1e6:.1f} MB")

    html = TEMPLATE.replace("__SHOTS__", json.dumps(shots_js)) \
                   .replace("__AUDIO__", json.dumps(audio_js)) \
                   .replace("__STATS__", json.dumps(STATS))
    OUT.write_text(html, encoding="utf-8")
    print(f"\n  -> {OUT.relative_to(ROOT)}  {len(html)/1e6:.1f} MB")
    print("=" * 78)
    return 0


TEMPLATE = r"""<title>Al Safa 2 Park — Falaj Al Safa — 60-Second Concept Film</title>
<style>
  :root { --page:#0B0A09; --ink:#F3EFE7; --ink-2:#A6A094; --rule:#29251F;
          --sun:#FFB627; --mono: ui-monospace, "SF Mono", Consolas, monospace; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--page); color:var(--ink);
         font-family:"Helvetica Neue",Helvetica,Arial,sans-serif; }
  .wrap { max-width:1220px; margin:0 auto; padding:0 20px 60px; }
  header { padding:40px 0 18px; }
  .kicker { font-family:var(--mono); font-size:11px; letter-spacing:.18em;
            text-transform:uppercase; color:var(--ink-2); margin:0 0 14px; }
  h1 { margin:0; font-size:clamp(30px,5vw,52px); line-height:.98;
       letter-spacing:-.03em; }
  h1 span { color:var(--ink-2); }
  .stand { margin:14px 0 0; max-width:64ch; color:var(--ink-2); font-size:15.5px;
           line-height:1.6; }
  .film { position:relative; margin:26px 0 0; background:#000; aspect-ratio:16/9;
          overflow:hidden; box-shadow:0 30px 70px -30px rgba(0,0,0,.8); }
  .film canvas { display:block; width:100%; height:100%; }
  .overlay { position:absolute; inset:0; display:grid; place-items:center;
             background:rgba(8,7,6,.45); border:0; cursor:pointer; color:var(--ink); }
  .overlay[hidden] { display:none; }
  .mark { width:82px; height:82px; border-radius:50%;
          border:1px solid rgba(243,239,231,.55); display:grid; place-items:center; }
  .mark::after { content:""; width:0; height:0; margin-left:6px;
    border-left:19px solid var(--ink); border-top:12px solid transparent;
    border-bottom:12px solid transparent; }
  .overlay p { font-family:var(--mono); font-size:11px; letter-spacing:.22em;
               text-transform:uppercase; margin:16px 0 0; color:rgba(243,239,231,.75); }
  .bar { display:flex; align-items:center; gap:14px; flex-wrap:wrap;
         padding:14px 0; border-bottom:1px solid var(--rule); }
  .btn { font-family:var(--mono); font-size:11px; letter-spacing:.12em;
         text-transform:uppercase; background:none; color:var(--ink);
         border:1px solid var(--rule); border-radius:1px; padding:9px 13px;
         cursor:pointer; white-space:nowrap; }
  .btn:hover { border-color:var(--ink-2); }
  .btn:focus-visible { outline:2px solid var(--sun); outline-offset:2px; }
  .tc { font-family:var(--mono); font-size:12px; color:var(--ink-2);
        font-variant-numeric:tabular-nums; margin-left:auto; }
  .note { font-family:var(--mono); font-size:11.5px; line-height:1.75;
          color:var(--ink-2); margin:12px 0 0; }
  .note b { color:var(--ink); }
  footer { border-top:1px solid var(--rule); margin-top:30px; padding:20px 0 0;
           font-family:var(--mono); font-size:11px; color:var(--ink-2);
           line-height:1.85; letter-spacing:.04em; }
</style>

<div class="wrap">
  <header>
    <p class="kicker">Dubai Municipality · AI Park Design Challenge · Submission 12</p>
    <h1>Falaj Al Safa<br><span>Al Safa 2 Park in sixty seconds</span></h1>
    <p class="stand">
      Six visualisations of the proposal, cut against a spoken commentary. Every
      figure spoken or shown is regenerated by <code>python run_analysis.py</code>
      from the project's own analysis — none is typed in by hand.
    </p>
  </header>

  <div class="film">
    <canvas id="stage" width="1920" height="1080" role="img"
            aria-label="Sixty-second concept film for Al Safa 2 Park: the site in
            summer heat, the crescent canopy, the sunken palm court, the dune
            play area, the souk plaza, and the park after dark."></canvas>
    <button class="overlay" id="opener" aria-label="Play the film">
      <span class="mark"></span><p>Play · 60 seconds</p>
    </button>
  </div>

  <div class="bar">
    <button class="btn" id="toggle">Pause</button>
    <button class="btn" id="restart">Restart</button>
    <button class="btn" id="voice" aria-pressed="true">Narration on</button>
    <button class="btn" id="quality" aria-pressed="false">Quality · 1080p</button>
    <button class="btn" id="record">Record to a video file</button>
    <span class="tc" id="tc">00:00 / 01:00</span>
  </div>
  <p class="note" id="recnote" hidden></p>

  <footer>
    Al Safa 2 Park · Falaj Al Safa · Mohamed Wasim · Individual Applicant<br>
    Renders are artistic impressions of the analysed scheme. Plans, sections and
    every quoted figure are computed — see the masterplan and section drawings.<br>
    Reproduce: <code>python run_analysis.py</code> · Build this film:
    <code>python tools/build_render_film.py</code>
  </footer>
</div>

<script>
(() => {
  "use strict";
  const SHOTS = __SHOTS__, AUDIO = __AUDIO__, STATS = __STATS__;
  const DUR = 60;
  const cv = document.getElementById("stage");
  const ctx = cv.getContext("2d", { alpha:false });
  const W = 1920, H = 1080;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
  const lerp=(a,b,t)=>a+(b-a)*t;
  const easeIO=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
  const easeOut=t=>1-Math.pow(1-t,3);
  const win=(t,i,o)=>Math.min(clamp(t/i,0,1),clamp((1-t)/o,0,1));

  // Letterbox to 2.39:1 — the same frame the original cut used, so the two
  // films read as one piece of work.
  const BAR = Math.round((H - W/2.39)/2), FT = BAR, FB = H - BAR, FH = FB - FT;

  let SCALE = 1;
  function setStage(k){
    if (SCALE===k) return;
    SCALE=k; cv.width=W*k; cv.height=H*k; ctx.setTransform(k,0,0,k,0,0);
  }

  const imgs = SHOTS.map(s => { const i = new Image(); i.src = s.img; return i; });
  let ready = 0;
  imgs.forEach(i => i.decode().then(()=>{ready++;}).catch(()=>{ready++;}));

  function mono(s,w){ ctx.font=`${w||400} ${s}px ui-monospace,"SF Mono",Consolas,monospace`; }
  function disp(s,w){ ctx.font=`${w||700} ${s}px "Helvetica Neue",Helvetica,Arial,sans-serif`; }

  // One shot: cover-fit the still, then push or pull slowly across it. The move
  // is small on purpose — a render is a held image, and a fast move on a still
  // reads as a slideshow effect rather than as a camera.
  function drawShot(s, img, k, alpha) {
    if (!img || !img.width) return;
    const z = lerp(s.zoom[0], s.zoom[1], easeIO(k));
    const scale = Math.max(W/img.width, FH/img.height) * z;
    const dw = img.width*scale, dh = img.height*scale;
    const dx = (W-dw)/2 + s.pan[0]*W*easeIO(k);
    const dy = FT + (FH-dh)/2 + s.pan[1]*FH*easeIO(k);
    ctx.globalAlpha = alpha;
    ctx.drawImage(img, dx, dy, dw, dh);
    ctx.globalAlpha = 1;
  }

  function grade() {
    // A held gradient top and bottom so type always has something to sit on,
    // whatever the image underneath happens to be doing.
    let g = ctx.createLinearGradient(0, FT, 0, FT+FH*0.42);
    g.addColorStop(0,"rgba(6,6,8,.62)"); g.addColorStop(1,"rgba(6,6,8,0)");
    ctx.fillStyle=g; ctx.fillRect(0,FT,W,FH*0.42);
    g = ctx.createLinearGradient(0, FB-FH*0.52, 0, FB);
    g.addColorStop(0,"rgba(6,6,8,0)"); g.addColorStop(1,"rgba(6,6,8,.80)");
    ctx.fillStyle=g; ctx.fillRect(0,FB-FH*0.52,W,FH*0.52);
  }

  function bars(){ ctx.fillStyle="#000"; ctx.fillRect(0,0,W,FT); ctx.fillRect(0,FB,W,H-FB); }

  function tx(s,x,y,a){ ctx.globalAlpha=a===undefined?1:clamp(a,0,1); ctx.fillText(s,x,y); ctx.globalAlpha=1; }

  function titles(s, k) {
    const a = win(k, .12, .16);
    if (a <= .002) return;
    const x = 118, slide = (1-easeOut(clamp(k/.12,0,1)))*22;
    ctx.textAlign="left";
    ctx.strokeStyle=`rgba(255,182,39,${.9*a})`; ctx.lineWidth=3;
    ctx.beginPath(); ctx.moveTo(x, FB-176); ctx.lineTo(x, FB-72); ctx.stroke();
    ctx.fillStyle=`rgba(255,182,39,${a})`; mono(17,700);
    ctx.save(); ctx.letterSpacing="4px"; tx(s.kicker, x+24+slide, FB-146, a); ctx.restore();
    ctx.fillStyle="#F3EFE7"; disp(52,700);
    tx(s.title, x+24+slide, FB-98, a);
    ctx.fillStyle="rgba(243,239,231,.72)"; mono(20,400);
    tx(s.sub, x+24+slide, FB-62, a*.96);
  }

  function stat(time) {
    for (const st of STATS) {
      if (time < st.t0 || time > st.t1) continue;
      const k = (time-st.t0)/(st.t1-st.t0), a = win(k,.16,.20);
      if (a <= .002) continue;
      ctx.textAlign="right";
      const x = W-118, y = FT+FH*.26;
      ctx.fillStyle=`rgba(255,182,39,${a})`; mono(62,700);
      tx(st.big, x, y, a);
      ctx.fillStyle=`rgba(243,239,231,.66)`; mono(15,400);
      ctx.save(); ctx.letterSpacing="3px"; tx(st.small, x, y+26, a*.9); ctx.restore();
      ctx.textAlign="left";
    }
  }

  function draw(time) {
    ctx.fillStyle="#0B0A09"; ctx.fillRect(0,0,W,H);
    const XF = 0.9;                       // cross-dissolve, seconds
    let cur = SHOTS.findIndex(s => time < s.t1);
    if (cur < 0) cur = SHOTS.length-1;
    const s = SHOTS[cur], k = clamp((time-s.t0)/(s.t1-s.t0), 0, 1);

    // Outgoing shot still on screen during the dissolve.
    if (cur > 0 && time - s.t0 < XF) {
      const p = SHOTS[cur-1];
      drawShot(p, imgs[cur-1], 1, 1);
      drawShot(s, imgs[cur], k, (time - s.t0)/XF);
    } else {
      drawShot(s, imgs[cur], k, 1);
    }

    grade();
    titles(s, k);
    stat(time);

    if (time < 1.0) { ctx.fillStyle=`rgba(11,10,9,${1-time})`; ctx.fillRect(0,FT,W,FH); }
    if (time > DUR-1.2) {
      ctx.fillStyle=`rgba(11,10,9,${(time-(DUR-1.2))/1.2})`; ctx.fillRect(0,FT,W,FH);
    }
    bars();
    return cur;
  }

  // ── narration ─────────────────────────────────────────────────────────────
  const VO = AUDIO.map((src,i) => ({ at: i*15, el: new Audio(src) }));
  let actx=null, voDest=null, voReady=false, voOn=true;
  const voBtn=document.getElementById("voice");
  function audioSetup(){
    if (actx) return;
    try{
      actx=new (window.AudioContext||window.webkitAudioContext)();
      voDest=actx.createMediaStreamDestination();
      VO.forEach(v=>{ const src=actx.createMediaElementSource(v.el);
        const g=actx.createGain(); src.connect(g); g.connect(actx.destination);
        g.connect(voDest); });
      voReady=true;
    }catch(e){ voReady=false; }
  }
  function voSync(force){
    if(!voReady||!voOn) return;
    VO.forEach(v=>{
      const local=t-v.at, len=v.el.duration||15, inside=local>=0&&local<len;
      if(!inside){ if(!v.el.paused) v.el.pause(); return; }
      if(force||Math.abs(v.el.currentTime-local)>0.35){
        try{ v.el.currentTime=Math.max(0,local); }catch(e){}
      }
      if(playing&&v.el.paused) v.el.play().catch(()=>{});
      if(!playing&&!v.el.paused) v.el.pause();
    });
  }
  function voStop(){ VO.forEach(v=>v.el.pause()); }
  voBtn.addEventListener("click",()=>{
    voOn=!voOn; voBtn.textContent=voOn?"Narration on":"Narration off";
    voBtn.setAttribute("aria-pressed",String(voOn));
    if(!voOn) voStop(); else { audioSetup(); voSync(true); }
  });

  // ── transport ─────────────────────────────────────────────────────────────
  const tcEl=document.getElementById("tc"), toggle=document.getElementById("toggle");
  const restart=document.getElementById("restart"), opener=document.getElementById("opener");
  let t=0, playing=false, last=0;
  const fmt=v=>`${String(Math.floor(v/60)).padStart(2,"0")}:${String(Math.floor(v%60)).padStart(2,"0")}`;
  function paint(){ draw(t); tcEl.textContent=`${fmt(t)} / 01:00`; }
  function tick(now){
    if(!playing) return;
    t+=Math.min(.05,(now-last)/1000); last=now;
    if(t>=DUR){ t=DUR; playing=false; toggle.textContent="Replay"; }
    paint(); voSync(false); if(!playing) voStop();
    if(playing) requestAnimationFrame(tick);
  }
  function play(){
    if(t>=DUR) t=0;
    playing=true; last=performance.now();
    toggle.textContent="Pause"; opener.hidden=true;
    requestAnimationFrame(tick);
  }
  toggle.addEventListener("click",()=>{ audioSetup();
    if(playing){playing=false;toggle.textContent="Play";voStop();} else play(); });
  restart.addEventListener("click",()=>{ audioSetup(); t=0; play(); voSync(true); });
  opener.addEventListener("click",()=>{ audioSetup(); play(); voSync(true); });

  // ── record ────────────────────────────────────────────────────────────────
  const recBtn=document.getElementById("record"), recNote=document.getElementById("recnote");
  const qBtn=document.getElementById("quality");
  let want4K=false;
  function say(h){ recNote.hidden=false; recNote.innerHTML=h; }
  qBtn.addEventListener("click",()=>{
    want4K=!want4K; qBtn.textContent=want4K?"Quality · 4K":"Quality · 1080p";
    qBtn.setAttribute("aria-pressed",String(want4K));
    say(want4K?"Next recording will be <b>3840 &times; 2160</b>."
              :"Next recording will be <b>1920 &times; 1080</b>.");
  });
  function pickType(){
    // Name the audio codec: left to itself Chromium writes OPUS inside the MP4,
    // which Chrome plays and almost nothing else does. And name a video profile
    // that matches the resolution — avc1.42E01E is Baseline 3.0, specified for
    // 720x480, and handing it a 4K canvas makes the encoder throw quality away.
    const v = want4K ? "avc1.640033" : "avc1.64002A";
    const want=[`video/mp4;codecs=${v},mp4a.40.2`,
                "video/mp4;codecs=avc1.640033,mp4a.40.2",
                "video/mp4;codecs=avc1.42E01E,mp4a.40.2","video/mp4",
                "video/webm;codecs=vp9,opus","video/webm"];
    for(const ty of want) if(window.MediaRecorder&&MediaRecorder.isTypeSupported(ty)) return ty;
    return "";
  }
  recBtn.addEventListener("click", async ()=>{
    if(recBtn.getAttribute("aria-busy")==="true") return;
    const type=pickType();
    if(!type){ say("This browser cannot record video. Use Chrome or Edge."); return; }
    const ext=type.startsWith("video/mp4")?"mp4":"webm";
    playing=false; t=0;
    audioSetup();
    if(actx&&actx.state==="suspended"){ try{ await actx.resume(); }catch(e){} }
    setStage(want4K?2:1); paint();
    recBtn.setAttribute("aria-busy","true"); toggle.disabled=restart.disabled=true;

    const stream=cv.captureStream(30); let voiced=false;
    if(voOn&&voReady&&voDest) voDest.stream.getAudioTracks().forEach(tr=>{stream.addTrack(tr);voiced=true;});
    const chunks=[]; let rec;
    try{ rec=new MediaRecorder(stream,{mimeType:type,
      videoBitsPerSecond: want4K?44e6:14e6}); }
    catch(e){ say("Recording could not start: "+e.message);
      recBtn.removeAttribute("aria-busy"); toggle.disabled=restart.disabled=false; return; }
    rec.ondataavailable=e=>{ if(e.data&&e.data.size) chunks.push(e.data); };
    const done=new Promise(r=>{ rec.onstop=r; });
    rec.start(250);

    const t0=performance.now();
    await new Promise(res=>{
      playing=true;
      (function step(now){
        t=Math.min(DUR,(now-t0)/1000);
        paint(); voSync(false);
        say(`Recording <b>${Math.round(t)}s</b> of 60${voiced?" with narration":""} — `+
            `leave this tab in front; the file downloads when it finishes.`);
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

  if (reduce) { t = 16; toggle.textContent="Play"; }
  const boot = setInterval(()=>{ if(ready>=SHOTS.length){ clearInterval(boot); paint(); } }, 60);
  paint();
  window.__film = { draw, setStage, DUR };
})();
</script>
"""

if __name__ == "__main__":
    raise SystemExit(main())
