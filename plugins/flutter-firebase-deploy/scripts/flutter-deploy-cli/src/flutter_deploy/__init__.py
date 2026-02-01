"""
Flutter Deploy CLI
==================

A beautiful CLI tool for fully automated Flutter app deployment to iOS and Android.
"""

__version__ = "1.0.0"
__author__ = "Flutter Deploy CLI"

from .cli import main, FlutterDeployCLI

__all__ = ["main", "FlutterDeployCLI", "__version__"]
