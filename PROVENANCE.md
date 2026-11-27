# Provenance

Every file in this repository, how it was made and under which licence.

## forja/

| Files | Made by | Licence |
|---|---|---|
| `forja/*.dxf` (7 drawings: `basic-shapes`, `blocks-and-inserts`, `curves`, `hatch-and-dimensions`, `hole`, `layers-and-linetypes`, `plate-with-text`) | `tools/generate-forja.py` with forja-cli 0.3.1 (metric drawings built from engine commands; no outside drawing was opened or copied) | CC0-1.0 |

To regenerate: `tools/generate-forja.py /path/to/forja-cli`. The output is byte for byte the same
(checked when the files were added).

## real/

Nothing yet. See `real/README.md`.
