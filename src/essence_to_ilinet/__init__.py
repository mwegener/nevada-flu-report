"""
ESSENCE → ILINet package (stand-alone).

Example
-------
python -m essence_to_ilinet --start 21May2023 --end 26Aug2023
"""
from .pipeline import run as run_essence_to_ilinet

__all__ = ["run_essence_to_ilinet"]