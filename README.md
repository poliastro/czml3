# czml3

Python 3 library to write CZML.

## Example

```
>>> from czml3 import Packet
>>> Packet()
{
    "id": "adae4d3a-7087-4fda-a70b-d18a262a890e"
}
>>> packet0 = Packet(id="Facility/AGI", name="AGI")
>>> packet0
{
    "id": "Facility/AGI",
    "name": "AGI"
}
>>> packet0.dumps()
'{"id": "Facility/AGI", "name": "AGI"}'

```
