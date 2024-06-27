from .core import CZML_VERSION, Document, Packet, Preamble

with open("src/czml3/version.txt") as f:
    __version__ = f.read()

__all__ = ["Document", "Preamble", "Packet", "CZML_VERSION"]
