from importlib.metadata import version, PackageNotFoundError

from .parse import parser
from .ai_read import analyze_document
from .processing import run_processing
from .token_cost import TokenCostTracker

try:
    __version__ = version("dbnl_bear")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = [
    'parser',
    'analyze_document',
    'run_processing',
    'TokenCostTracker',
    '__version__',
]

