from ._version import get_versions
from .core import Document, Packet

__version__ = get_versions()["version"]
del get_versions

__all__ = ["Document", "Packet"]
