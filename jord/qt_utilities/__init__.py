from pathlib import Path

try:
    from .enums import *
except ImportError as ix:
    this_package_name = Path(__file__).parent.name
    print(f"Make sure qt module is available for {this_package_name}")
    raise ix
