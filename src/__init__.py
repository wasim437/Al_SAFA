"""
Al Safa 2 Park — AI Design Challenge
Analysis package.

Python is used in this project for one thing: computation on data. Every module
here loads data, models a physical process, trains a model, or draws a figure.
No module in this package writes prose or typesets a document — the written
reports are authored in Word, by a human, as they should be.

    src.config    site constants, model settings, the validated visual system
    src.climate   thermal comfort indices and monthly-to-hourly downscaling
    src.solar     NREL SPA sun positions, canopy shading, ground-plane occlusion
    src.dataset   dataset assembly and feature engineering
    src.models    the machine learning layer
    src.viz       the one figure system every chart is built through
"""

from . import climate, config, dataset, models, solar, viz  # noqa: F401

__all__ = ["config", "climate", "solar", "dataset", "models", "viz"]
__version__ = "2.0.0"
