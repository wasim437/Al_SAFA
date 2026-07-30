// Actually EXECUTE the film across all 60 seconds against a mock canvas.
// Static linting cannot catch a null deref inside a scene that only happens at
// t=43.25; running every frame can.
const fs = require("fs");
const vm = require("vm");

const path = "c:\\Users\\LENOVO\\Downloads\\AL SAFA\\submission\\12_Concept_Animation_Video\\concept_film.html";
const src = fs.readFileSync(path, "utf8");
const js = src.match(/<script>([\s\S]*)<\/script>/)[1];

// Expose the internals so we can drive draw() directly.
const patched = js.replace(
  /if \(reduce\) \{ t = 36; toggle\.textContent = "Play"; \}\s*paint\(\);/,
  'globalThis.__film = { draw, SCENES, paint, cam, EXISTING, TREES,\n' +
  '    probe: () => ({ fov: cam.fov, pos: cam.pos.slice(), tgt: cam.tgt.slice(),\n' +
  '                    FOCAL, BX, BY, BZ, sample: proj([12,10,3.2]) }) };\n  paint();'
);
if (patched === js) { console.log("  [FAIL] could not patch entry point"); process.exit(1); }

// ---- mock canvas ------------------------------------------------------
let warnings = [];
function mkCtx() {
  const grad = { addColorStop(o, c) {
    if (typeof c !== "string" || /NaN|undefined/.test(c))
      warnings.push(`gradient stop ${o} = ${c}`);
  }};
  const c = {
    canvas: { width: 1920, height: 1080 },
    createLinearGradient: () => grad,
    createRadialGradient: () => grad,
    measureText: () => ({ width: 100 }),
    getImageData: () => ({ data: new Uint8ClampedArray(4) }),
  };
  for (const m of ["fillRect","strokeRect","clearRect","beginPath","moveTo","lineTo",
                   "closePath","fill","stroke","arc","ellipse","save","restore",
                   "translate","rotate","scale","clip","rect","fillText","strokeText",
                   "setTransform","drawImage","setLineDash","bezierCurveTo","quadraticCurveTo"])
    c[m] = () => {};
  // Trap bad colour / geometry values as they are assigned.
  const store = {};
  for (const p of ["fillStyle","strokeStyle","font","globalAlpha","lineWidth",
                   "textAlign","textBaseline","letterSpacing","lineCap","lineJoin","filter"]) {
    Object.defineProperty(c, p, {
      get: () => store[p],
      set: v => {
        if ((p === "fillStyle" || p === "strokeStyle") &&
            typeof v === "string" && /NaN|undefined/.test(v))
          warnings.push(`${p} = ${v}`);
        if ((p === "globalAlpha" || p === "lineWidth") &&
            (typeof v !== "number" || !isFinite(v))) {
          if (process.env.THROW_ON_BAD) {
            const st = new Error().stack.split("\n")
              .filter(l => l.includes("evalmachine")).slice(0, 4).join("\n");
            console.log(`\n  >>> ${p} = ${v}\n${st}\n`);
            process.exit(2);
          }
          warnings.push(`${p} = ${v}`);
        }
        store[p] = v;
      },
    });
  }
  return c;
}
const el = () => {
  const e = {
    // The canvas element's own width/height. Omitting these made W and H
    // undefined inside the film and every derived number cascaded to NaN —
    // a fault in this harness that looked exactly like a fault in the film.
    width: 1920, height: 1080,
    style: {}, classList: { toggle(){}, add(){}, remove(){}, contains(){return false} },
    dataset: {}, hidden: false, textContent: "", innerHTML: "",
    addEventListener(){}, appendChild(){}, setAttribute(){}, getAttribute(){return null},
    querySelector: () => el(), querySelectorAll: () => [],
    getContext: () => mkCtx(),
  };
  return e;
};

const sandbox = {
  console,
  document: { getElementById: () => el(), createElement: () => el(),
              documentElement: { setAttribute(){}, getAttribute(){return null} } },
  matchMedia: () => ({ matches: false, addEventListener(){} }),
  requestAnimationFrame: () => 0,
  performance: { now: () => 0 },
  localStorage: { getItem(){return null}, setItem(){} },
  Math, Date, JSON, Object, Array, String, Number, isFinite, parseInt, parseFloat,
  Uint8ClampedArray,
};
sandbox.globalThis = sandbox;
sandbox.window = sandbox;

console.log("=".repeat(72));
console.log("  FILM RUNTIME TEST — every frame, mocked canvas");
console.log("=".repeat(72));

try {
  vm.createContext(sandbox);
  new vm.Script(patched).runInContext(sandbox);
  console.log("  [ok  ] script executes and initialises");
} catch (e) {
  console.log("  [FAIL] init threw: " + e.message + "\n" + (e.stack||"").split("\n").slice(0,4).join("\n"));
  process.exit(1);
}

const film = sandbox.__film;
if (!film) { console.log("  [FAIL] internals not exposed"); process.exit(1); }

// Drive every frame at 30 fps, plus scene boundaries exactly.
const times = [];
for (let t = 0; t <= 60.0001; t += 1/30) times.push(+t.toFixed(4));
for (const s of film.SCENES) times.push(s.t0, s.t0 + .001, s.t1 - .001, s.t1);
times.push(0, 59.999, 60);

let errs = [];
for (const t of times) {
  warnings = [];
  try {
    film.draw(t);
  } catch (e) {
    errs.push({ t, msg: e.message, stack: (e.stack||"").split("\n")[1] || "" });
    if (errs.length > 6) break;
    continue;
  }
  if (warnings.length) {
    errs.push({ t, msg: "bad value: " + [...new Set(warnings)].slice(0,3).join(" | ") });
    if (errs.length > 6) break;
  }
}

if (!errs.length) {
  console.log(`  [ok  ] ${times.length} frames drawn, no exceptions`);
  console.log(`  [ok  ] no NaN/undefined colours, alphas or line widths`);
} else {
  console.log(`  [FAIL] ${errs.length} problem frame(s):`);
  for (const e of errs.slice(0, 8)) {
    console.log(`         t=${String(e.t).padStart(8)}  ${e.msg}`);
    if (e.stack) console.log(`                    ${String(e.stack).trim()}`);
  }
}

// Scene coverage: every scene must be reached and cover its full span.
const covered = film.SCENES.map(s => ({ n: s.name, t0: s.t0, t1: s.t1 }));
console.log("\n  scene spans:");
let prev = 0, gap = false;
for (const s of covered) {
  if (Math.abs(s.t0 - prev) > 1e-6) { gap = true; }
  prev = s.t1;
  console.log(`    ${s.n.padEnd(12)} ${String(s.t0).padStart(4)} – ${String(s.t1).padStart(4)} s`);
}
console.log(`  [${!gap && prev === 60 ? "ok  " : "FAIL"}] scenes tile 0–60 s with no gaps (ends at ${prev})`);

process.exit(errs.length || gap || prev !== 60 ? 1 : 0);
