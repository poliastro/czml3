from ._version import get_versions
from .core import CZML_VERSION, Document, Packet, Preamble

__version__ = get_versions()["version"]
del get_versions

__all__ = ["Document", "Preamble", "Packet", "CZML_VERSION"]
