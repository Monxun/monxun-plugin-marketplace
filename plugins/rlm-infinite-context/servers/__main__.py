"""
Entry point for running the RLM server as a module.

Usage:
    python -m rlm_server
"""

import asyncio
from .rlm_server import main

if __name__ == "__main__":
    asyncio.run(main())
