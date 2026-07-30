"""
Al Safa 2 Park — run the whole analysis end to end.

    python run_analysis.py            full run
    python run_analysis.py --fast     coarser spatial sampling, for iterating

Everything the submission quotes is produced here: the two datasets, the three
models, their metrics, and every figure. Nothing downstream types a number of
its own.
"""

from __future__ import annotations

import argparse
import json
import time

import pandas as pd

from src import climate, config as C, dataset, models, solar, viz


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true",
                    help="coarser spatial grid and fewer sampled hours")
    args = ap.parse_args()

    t0 = time.time()
    viz.apply_style()
    step = 2.0 if args.fast else 1.0
    hours = 120 if args.fast else 400

    print("=" * 72)
    print("  AL SAFA 2 PARK — ANALYSIS PIPELINE")
    print("=" * 72)

    # -- datasets ----------------------------------------------------------
    print("\n[1/5] Building the hourly dataset ...")
    hourly = dataset.build_hourly()

    normals = pd.read_csv(C.DATA_RAW / "dubai_climate_normals_ncm.csv")
    verify = climate.verify_downscaling(hourly, normals)
    print(f"      downscaling error vs NCM normals: "
          f"max |mean| {verify['err_mean_c'].abs().max():.2f} C")

    print("\n[2/5] Building the spatial dataset ...")
    grid, trees = dataset.build_spatial(step_m=step, sample_hours=hours)
    paths = dataset.save(hourly, grid, trees)
    for k, v in paths.items():
        print(f"      {k:<8} -> {v.name}")

    # -- models ------------------------------------------------------------
    print("\n[3/5] Training the shade surrogate (M1) ...")
    m1 = models.train_shade_surrogate(grid, tune=not args.fast)
    m1["_name"] = "M1_shade_surrogate"
    rf = m1["models"]["random_forest"]
    nn = m1["models"]["neural_network"]
    print(f"      random forest   test R2 {rf['test_r2']:.4f}  RMSE {rf['test_rmse']:.1f} h")
    print(f"      neural network  test R2 {nn['test_r2']:.4f}  RMSE {nn['test_rmse']:.1f} h")
    print("      top geometric drivers:")
    for row in m1["permutation_importance"][:4]:
        print(f"        {row['feature']:<22} {row['importance']:.3f}")

    print("\n[4/5] Training the comfort classifier (M2) and clustering (M3) ...")
    m2 = models.train_comfort_classifier(hourly)
    m2["_name"] = "M2_comfort_classifier"
    print(f"      accuracy {m2['test_accuracy']:.4f}  "
          f"balanced {m2['test_balanced_accuracy']:.4f}  "
          f"(temperature and humidity withheld)")

    m3 = models.cluster_microclimates(hourly)
    m3["_name"] = "M3_microclimate_regimes"
    print(f"      microclimate regimes: k={m3['best_k']} selected by silhouette")

    # -- headline results --------------------------------------------------
    print("\n[5/5] Computing headline design metrics ...")
    sol = solar.hourly_solar_position()
    frac = solar.spine_shade_fraction(sol)
    canopy_only = solar.annual_shade_summary(frac)

    # Combined canopy + flanking tree avenue, measured along the walkway itself.
    spine_cells = grid[grid["under_spine_canopy"] == 1]
    combined_pct = float(spine_cells["shade_pct"].mean())

    exposed = hourly["comfort_band"].value_counts(normalize=True) * 100
    shaded = hourly["comfort_band_shaded"].value_counts(normalize=True) * 100

    day = hourly[hourly["is_daylight"]]
    comfortable_exposed = float((day["heat_index_c"] < 32).mean() * 100)
    comfortable_shaded = float((day["heat_index_shaded_c"] < 32).mean() * 100)

    headline = {
        "generated": pd.Timestamp.now().isoformat(timespec="seconds"),
        "site_area_sqm": C.SITE["area_sqm"],
        "annual_daylight_hours": int(sol["is_daylight"].sum()),
        "spine_shade_canopy_only_pct": canopy_only["annual_shade_pct"],
        "spine_shade_canopy_plus_trees_pct": round(combined_pct, 1),
        "site_mean_shade_pct": round(float(grid["shade_pct"].mean()), 1),
        "daylight_hours_comfortable_exposed_pct": round(comfortable_exposed, 1),
        "daylight_hours_comfortable_shaded_pct": round(comfortable_shaded, 1),
        "comfort_hours_gained_pct_points": round(comfortable_shaded - comfortable_exposed, 1),
        "mean_heat_index_reduction_c": round(float(hourly["comfort_gain_c"].mean()), 2),
        "peak_heat_index_exposed_c": round(float(hourly["heat_index_c"].max()), 1),
        "peak_heat_index_shaded_c": round(float(hourly["heat_index_shaded_c"].max()), 1),
        "comfort_band_share_exposed_pct": {k: round(v, 1) for k, v in exposed.items()},
        "comfort_band_share_shaded_pct": {k: round(v, 1) for k, v in shaded.items()},
        "trees": int(len(trees)),
        "model_M1_test_r2": round(nn["test_r2"], 4),
        "model_M2_test_accuracy": round(m2["test_accuracy"], 4),
        "model_M3_regimes": m3["best_k"],
    }
    (C.MODELS / "headline_metrics.json").write_text(
        json.dumps(headline, indent=2), encoding="utf-8")

    metrics_path = models.save_metrics(m1, m2, m3)

    print("\n[6/6] Generating figures ...")
    from src import figures
    made = figures.build_all(hourly, grid, trees, m1, m2, m3, normals)
    for p in made:
        print(f"      {p.name}")

    print("\n" + "=" * 72)
    print("  HEADLINE RESULTS")
    print("=" * 72)
    print(f"  Spine shade, canopy alone            {headline['spine_shade_canopy_only_pct']:>6.1f} %")
    print(f"  Spine shade, canopy + tree avenue    {headline['spine_shade_canopy_plus_trees_pct']:>6.1f} %")
    print(f"  Site-wide mean shade                 {headline['site_mean_shade_pct']:>6.1f} %")
    print(f"  Comfortable daylight hours, exposed  {headline['daylight_hours_comfortable_exposed_pct']:>6.1f} %")
    print(f"  Comfortable daylight hours, shaded   {headline['daylight_hours_comfortable_shaded_pct']:>6.1f} %")
    print(f"  Mean heat-index reduction            {headline['mean_heat_index_reduction_c']:>6.2f} C")
    print(f"  Peak heat index exposed / shaded     "
          f"{headline['peak_heat_index_exposed_c']:.1f} / {headline['peak_heat_index_shaded_c']:.1f} C")
    print("=" * 72)
    print(f"  metrics -> {metrics_path}")
    print(f"  elapsed {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()
