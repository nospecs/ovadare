# ovadare/conflicts/__init__.py

from .conflict import Conflict
from .conflict_detector import ConflictDetector
from .conflict_resolver import ConflictResolver
from .conflict_classifier import ConflictClassifier  # If implemented
from .resolution import Resolution
from .resolution_engine import ResolutionEngine

__all__ = [
    'Conflict',
    'ConflictDetector',
    'ConflictResolver',
    'ConflictClassifier',  # If implemented
    'Resolution',
    'ResolutionEngine'
]
