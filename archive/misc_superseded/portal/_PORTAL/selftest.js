/* ==========================================================================
   selftest.js — portal smoke test.  Run:  node _PORTAL/selftest.js
   --------------------------------------------------------------------------
   Checks the three things most likely to break silently in a browser:
     1. the NOAA solar engine agrees with the project's pvlib output
     2. every element id portal.js reaches for actually exists in index.html
     3. the figures the portal renders match the source data files
   Exits non-zero on failure so it can gate a rebuild.
   ========================================================================== */
'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const HERE = __dirname;
const ROOT = path.dirname(HERE);

let failures = 0, passes = 0;

function check(name, ok, detail) {
    if (ok) { passes++; console.log(`  ok    ${name}`); }
    else { failures++; console.log(`  FAIL  ${name}${detail ? '\n          ' + detail : ''}`); }
}

function section(title) { console.log(`\n${title}`); }

/* -------------------------------------------------------------------------
   Load the generated data exactly as the browser would.
   ------------------------------------------------------------------------- */
const sandbox = { window: {} };
vm.createContext(sandbox);
vm.runInContext(fs.readFileSync(path.join(HERE, 'portal_data.js'), 'utf8'), sandbox);
const D = sandbox.window.AS2;

const portalSrc = fs.readFileSync(path.join(HERE, 'portal.js'), 'utf8');
const htmlSrc = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');

/* -------------------------------------------------------------------------
   1. Solar engine — re-declared here from portal.js so the test exercises the
      shipped implementation rather than a copy.
   ------------------------------------------------------------------------- */
section('1. Solar engine vs. the project\'s pvlib NREL SPA output');

const engineSrc = portalSrc.slice(
    portalSrc.indexOf('const rad = d =>'),
    portalSrc.indexOf('const compassPoint'));

const solarCtx = {
    D, SITE: D.solar.site, TZ: 4, Math, console,
};
vm.createContext(solarCtx);
vm.runInContext(engineSrc, solarCtx);

const MONTHS = { Jan: 1, Feb: 2, Mar: 3, Apr: 4, May: 5, Jun: 6,
                 Jul: 7, Aug: 8, Sep: 9, Oct: 10, Nov: 11, Dec: 12 };

D.solar.keyDates.forEach(k => {
    const m = k.date.match(/\((\d+)\s+(\w+)/);
    if (!m) return;
    const day = Number(m[1]), month = MONTHS[m[2]];
    const computed = solarCtx.peakElevation(2026, month, day);
    const delta = Math.abs(computed - k.maxElev);
    check(`peak elevation ${k.date} — pvlib ${k.maxElev}°, engine ${computed.toFixed(2)}°`,
          delta < 0.5, `differs by ${delta.toFixed(3)}°, tolerance 0.5°`);

    // Day length carries a looser tolerance than elevation, for two documented
    // reasons: the engine uses the NOAA 90.833° zenith (refraction + solar disc)
    // while the project's figures use a tighter horizon, and every one of the
    // project's sunrise/sunset values is rounded to a 10-minute step — which on
    // its own can move day length by up to 20 minutes. Peak elevation, which is
    // what actually drives the shade model, is checked to 0.5°.
    const pos = solarCtx.solarPosition(2026, month, day, 12);
    const dayDelta = Math.abs(pos.dayLength - k.dayLength);
    check(`day length ${k.date} — pvlib ${k.dayLength} h, engine ${pos.dayLength.toFixed(2)} h`,
          dayDelta < 0.35,
          `differs by ${dayDelta.toFixed(3)} h, tolerance 0.35 h (horizon convention + 10-min rounding)`);
});

// Sanity properties that must hold anywhere on Earth.
const june = solarCtx.solarPosition(2026, 6, 21, 12);
check('solar noon falls between 12:00 and 13:00 local for Dubai',
      june.solarNoon > 12 && june.solarNoon < 13,
      `got ${june.solarNoon.toFixed(3)}`);
check('sunrise precedes sunset', june.sunrise < june.sunset);
check('midnight sun elevation is negative',
      solarCtx.solarPosition(2026, 6, 21, 0).elevation < 0);
check('declination at the June solstice is near +23.44°',
      Math.abs(june.declination - 23.44) < 0.2, `got ${june.declination.toFixed(3)}°`);
check('declination at the December solstice is near −23.44°',
      Math.abs(solarCtx.solarPosition(2026, 12, 21, 12).declination + 23.44) < 0.2);
check('azimuth stays within 0–360° across a full day',
      Array.from({ length: 96 }, (_, i) =>
          solarCtx.solarPosition(2026, 3, 20, i / 4).azimuth)
          .every(a => a >= 0 && a <= 360));
check('morning sun is east of south, afternoon sun is west of south',
      solarCtx.solarPosition(2026, 3, 20, 9).azimuth < 180 &&
      solarCtx.solarPosition(2026, 3, 20, 15).azimuth > 180);

/* -------------------------------------------------------------------------
   2. HTML / JS contract — ids portal.js addresses must exist in index.html
   ------------------------------------------------------------------------- */
section('2. Element ids referenced by portal.js exist in index.html');

const htmlIds = new Set();
for (const m of htmlSrc.matchAll(/\sid="([^"]+)"/g)) htmlIds.add(m[1]);

const referenced = new Set();
for (const m of portalSrc.matchAll(/\$\('#([A-Za-z0-9_-]+)'/g)) referenced.add(m[1]);
for (const m of portalSrc.matchAll(/getElementById\('([A-Za-z0-9_-]+)'\)/g)) referenced.add(m[1]);

// Ids created at runtime: the concept weight sliders, and the "view full
// bibliography" link injected into the provenance drawer's innerHTML only
// when the metric being viewed carries at least one reference.
const runtime = new Set(['w0', 'w1', 'w2', 'w3', 'w4', 'wo0', 'wo1', 'wo2', 'wo3', 'wo4',
                          'drawerRefsLink']);

const missing = [...referenced].filter(id => !htmlIds.has(id) && !runtime.has(id));
check(`all ${referenced.size} referenced ids are present`,
      missing.length === 0, missing.length ? 'missing: ' + missing.join(', ') : '');

// Every canvas that gets a chart factory must exist too.
const chartIds = [...portalSrc.matchAll(/chart\('([A-Za-z0-9_]+)'/g)].map(m => m[1]);
const missingCanvas = chartIds.filter(id => !htmlIds.has(id));
check(`all ${chartIds.length} chart canvases exist`,
      missingCanvas.length === 0,
      missingCanvas.length ? 'missing: ' + missingCanvas.join(', ') : '');

// Every page the router knows about must have a section, and vice versa.
const pagesInJs = (portalSrc.match(/const PAGES = \[([\s\S]*?)\]/) || [])[1] || '';
const pageList = [...pagesInJs.matchAll(/'([a-z0-9]+)'/g)].map(m => m[1]);
const missingPages = pageList.filter(p => !htmlIds.has('page-' + p));
check(`all ${pageList.length} routed pages have a section`,
      missingPages.length === 0,
      missingPages.length ? 'missing: ' + missingPages.join(', ') : '');

const navPages = [...htmlSrc.matchAll(/data-page="([a-z0-9]+)"/g)].map(m => m[1]);
const orphanNav = navPages.filter(p => !pageList.includes(p));
check('every sidebar link routes to a known page',
      orphanNav.length === 0, orphanNav.join(', '));

// Local assets referenced by index.html must be on disk.
const assets = [...htmlSrc.matchAll(/(?:src|href)="(_PORTAL\/[^"]+)"/g)].map(m => m[1]);
const missingAssets = assets.filter(a => !fs.existsSync(path.join(ROOT, a)));
check(`all ${assets.length} local assets exist`,
      missingAssets.length === 0, missingAssets.join(', '));

const missingRenders = D.renders.filter(r => !fs.existsSync(path.join(ROOT, r.src)));
check(`all ${D.renders.length} render images exist`,
      missingRenders.length === 0, missingRenders.map(r => r.src).join(', '));

/* -------------------------------------------------------------------------
   3. Rendered figures still match the source data files
   ------------------------------------------------------------------------- */
section('3. Portal data matches the phase output files');

const readJson = (p) => JSON.parse(fs.readFileSync(path.join(ROOT, p), 'utf8'));

const carbon = readJson('07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/carbon_comfort_results.json');
const provOf = (k) => (D.provenance.find(p => p.key === k) || {}).value;

check('carbon sequestration matches the Phase 7 model',
      provOf('carbon_seq') === carbon.carbon.total_annual_tonnes,
      `portal ${provOf('carbon_seq')} vs source ${carbon.carbon.total_annual_tonnes}`);

const shade = readJson('07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/annual_shade_hours_results.json');
check('spine shade percentage matches the Phase 7 model',
      provOf('spine_shade') === shade.annual_shade_pct['Shaded Spine (path)']);

const om = readJson('07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/om_cost_results.json');
check('construction cost matches the Phase 7 O&M model build cost',
      provOf('capex') === om.build_cost_AED);
check('annual O&M cost matches the Phase 7 model',
      provOf('opex') === om.total_annual_om_AED);

const zoning = readJson('05_PHASE5_MASTERPLAN_DEVELOPMENT/outputs/zoning_area_schedule.json');
check('every zone in the schedule is carried into the portal',
      D.zoning.zones.length === zoning.zones.length,
      `portal ${D.zoning.zones.length} vs source ${zoning.zones.length}`);
check('zone areas sum to the site area',
      Math.abs(D.zoning.allocated - D.zoning.siteArea) < 1,
      `${D.zoning.allocated} vs ${D.zoning.siteArea}`);

const planting = readJson('06_PHASE6_DETAILED_DESIGN/outputs/planting_schedule.json');
check('tree count matches the planting schedule',
      D.planting.totalTrees === planting.total_trees);

/* -------------------------------------------------------------------------
   3c. Advanced LCC/energy/carbon model — reconciliation actually holds
   ------------------------------------------------------------------------- */
section('3c. Advanced LCC model is reconciled with the primary Phase 7 pipeline');

const adv = D.advanced;
check('advanced LCC model output exists', !!adv, 'D.advanced is missing — was ' +
      '08_advanced_lca_sustainability_master.py run?');

if (adv) {
    check('advanced model capex total equals the elemental take-off exactly',
          adv.capexTotal === D.cost.elemental.total,
          `advanced ${adv.capexTotal} vs elemental ${D.cost.elemental.total}`);
    check('advanced model opex total equals the O&M model exactly',
          adv.opexTotal === D.cost.om.total,
          `advanced ${adv.opexTotal} vs O&M ${D.cost.om.total}`);
    check('capex_breakdown.csv (package view) sums to the same total as the elemental take-off',
          D.cost.capexPackage.total === D.cost.elemental.total,
          `package ${D.cost.capexPackage.total} vs elemental ${D.cost.elemental.total}`);
    check('opex_breakdown.csv (package view) sums to the same total as the O&M model',
          D.cost.opexPackage.total === D.cost.om.total,
          `package ${D.cost.opexPackage.total} vs O&M ${D.cost.om.total}`);

    const embodiedCarbon = readJson(
        '07_PHASE7_PERFORMANCE_AND_SUSTAINABILITY/outputs/advanced_lcc_energy_carbon_results.json');
    check('embodied ETFE mass is sized to the real canopy area, not a leftover placeholder',
          embodiedCarbon.carbon.embodied_etfe_tCO2e > 200,
          `${embodiedCarbon.carbon.embodied_etfe_tCO2e} tCO2e — the retired placeholder ` +
          '(200 m2 instead of the real 1,592 m2) would give ~40 tCO2e, not >200');
    check('sequestration in the advanced model matches the verified 131-tree Phase 6 figure',
          Math.abs(adv.carbon.annual_sequestration_tCO2e - D.planting.carbonTotalTonnes) < 0.05,
          `advanced ${adv.carbon.annual_sequestration_tCO2e} vs verified ${D.planting.carbonTotalTonnes}`);

    check('solar energy deficit is stated as a deficit, not mislabelled as a surplus export',
          adv.energy.net_kWh < 0 && adv.energy.is_net_exporter === false,
          `net_kWh=${adv.energy.net_kWh}, is_net_exporter=${adv.energy.is_net_exporter} — ` +
          'the canopy array is well short of covering the assumed lighting/systems load');
    check('solar load-coverage percentage is internally consistent with yield and consumption',
          Math.abs(adv.energy.load_covered_pct -
              (adv.energy.annual_solar_yield_kWh / adv.energy.annual_consumption_kWh * 100)) < 0.5,
          `stated ${adv.energy.load_covered_pct}%`);

    check('30-year NPV yearly series starts at year 0 and runs the full 30 years',
          adv.lcc.yearly && adv.lcc.yearly.year.length === 31 &&
          adv.lcc.yearly.year[0] === 0 && adv.lcc.yearly.year[30] === 30);
    check('cumulative cost series starts at the capex total (year 0, before any O&M)',
          adv.lcc.yearly.cum_cost_AED[0] === adv.capexTotal,
          `year-0 cost ${adv.lcc.yearly.cum_cost_AED[0]} vs capex ${adv.capexTotal}`);
    check('cumulative cost and benefit series are monotonically non-decreasing',
          adv.lcc.yearly.cum_cost_AED.every((v, i) => i === 0 || v >= adv.lcc.yearly.cum_cost_AED[i - 1]) &&
          adv.lcc.yearly.cum_benefit_AED.every((v, i) => i === 0 || v >= adv.lcc.yearly.cum_benefit_AED[i - 1]));
}

/* -------------------------------------------------------------------------
   3b. Bibliography — every citation resolves, every reference is used
   ------------------------------------------------------------------------- */
section('3b. Reference bibliography is internally consistent');

const refs = D.references || [];
check('at least one external reference is declared', refs.length > 0, `found ${refs.length}`);

const refIds = new Set(refs.map(r => r.id));
const dangling = D.provenance.flatMap(p => p.refs || []).filter(id => !refIds.has(id));
check('every metric.refs id resolves to a declared reference',
      dangling.length === 0, 'dangling ids: ' + dangling.join(', '));

const cited = new Set(D.provenance.flatMap(p => p.refs || []));
const unused = refs.filter(r => !cited.has(r.id)).map(r => r.id);
check('every declared reference is cited by at least one metric',
      unused.length === 0, 'unused: ' + unused.join(', '));

const missingFields = refs.filter(r => !r.org || !r.title || !r.usedFor).map(r => r.id);
check('every reference has org, title and usedFor filled in',
      missingFields.length === 0, missingFields.join(', '));

const badUrls = refs.filter(r => r.url && !/^https:\/\//.test(r.url)).map(r => r.id);
check('every reference URL (where given) is a well-formed https link',
      badUrls.length === 0, badUrls.join(', '));

// The cost-rate honesty caveat specifically must survive into the portal —
// this is the fix for the "Dubai Municipality unit rates" overclaim.
const capexEntry = D.provenance.find(p => p.key === 'capex');
check('capex provenance does not overclaim municipal tender pricing',
      !/Dubai Municipality unit rates/.test(capexEntry.method),
      `method reads: "${capexEntry.method}"`);
check('capex provenance carries the villa/residential-rate caveat',
      /villa|residential/i.test(capexEntry.note),
      `note reads: "${capexEntry.note}"`);

/* -------------------------------------------------------------------------
   4. The site layout used by the plan and the 3D model preserves real areas
   ------------------------------------------------------------------------- */
section('4. Drawn layout preserves the scheduled areas');

const layoutSrc = portalSrc.slice(
    portalSrc.indexOf('const SITE_W = 150'),
    portalSrc.indexOf('const LAYOUT = computeLayout();'));
const layoutCtx = { D, Math };
vm.createContext(layoutCtx);
vm.runInContext(layoutSrc, layoutCtx);
const layout = layoutCtx.computeLayout();

check('every drawn block matches its scheduled area within 0.5 m²',
      layout.every(b => Math.abs(b.w * b.h - b.zone.area) < 0.5),
      layout.filter(b => Math.abs(b.w * b.h - b.zone.area) >= 0.5)
            .map(b => `${b.zone.name}: drawn ${(b.w * b.h).toFixed(1)} vs ${b.zone.area}`).join('; '));

check('every block sits inside the 150 × 100 m envelope',
      layout.every(b => b.x >= -0.01 && b.y >= -0.01 &&
                        b.x + b.w <= 150.01 && b.y + b.h <= 100.01),
      layout.filter(b => b.x < -0.01 || b.y < -0.01 || b.x + b.w > 150.01 || b.y + b.h > 100.01)
            .map(b => b.zone.name).join('; '));

// Blocks may not overlap — an overlap would mean the plan double-counts area.
const overlaps = [];
for (let i = 0; i < layout.length; i++) {
    for (let j = i + 1; j < layout.length; j++) {
        const a = layout[i], b = layout[j];
        const ox = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x);
        const oy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
        if (ox > 0.01 && oy > 0.01) overlaps.push(`${a.zone.name} / ${b.zone.name}`);
    }
}
check('no two drawn blocks overlap', overlaps.length === 0, overlaps.join('; '));

const drawnArea = layout.reduce((sum, b) => sum + b.w * b.h, 0);
check('drawn blocks cover the non-circulation programme',
      drawnArea > 11000 && drawnArea < 15001,
      `${drawnArea.toFixed(0)} m² drawn of ${D.zoning.siteArea} m²; the balance is the ` +
      'circulation network, which is shown as the gaps between blocks');

/* -------------------------------------------------------------------------
   5. The portal declares no analysis constants of its own
   ------------------------------------------------------------------------- */
section('5. No hard-coded analysis numbers leaked back into the portal');

// Figures that used to be typed into index.html and were wrong. If any of them
// reappears as a literal in the portal source, the regression is caught here.
const banned = [
    ['147', /\b147\s*(tCO|t\b)/i],
    ['-8.5 °C PET claim', /−8\.5|-8\.5\s*°C/],
    ['94.3 comfort days', /\b94\.3\b/],
    ['1.5 km catchment radius', /1\.5\s*km/i],
];
banned.forEach(([label, re]) => {
    check(`retired claim absent from portal.js: ${label}`, !re.test(portalSrc));
    check(`retired claim absent from index.html: ${label}`, !re.test(htmlSrc));
});

/* ------------------------------------------------------------------------- */
console.log(`\n${passes} passed, ${failures} failed\n`);
process.exit(failures ? 1 : 0);
