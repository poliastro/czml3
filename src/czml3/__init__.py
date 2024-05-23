from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

try:
    from .core import CZML_VERSION, Document, Packet, Preamble

    __all__ = ["Document", "Preamble", "Packet", "CZML_VERSION"]
except Exception:
    pass  # required for dynamic versioning using setuptools in pyproject.toml
