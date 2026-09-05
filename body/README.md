# Human Body — Dissectable 3D Atlas

A full-body, dissectable human anatomy viewer built from **BodyParts3D**
(CC BY-SA 2.1 JP) element meshes. Explore the skeletal, muscular,
cardiovascular, nervous and organ systems; isolate individual structures.

## Layout

- `scripts/build_body.py` — downloads metadata, classifies ~2,200 anatomical
  elements into body systems, and merges each part into a single OBJ.
- `models/parts/<system>/<part>.obj` — merged meshes (generated).
- `models/manifest.json` — system → part → file mapping (generated).
- `web/index.html` — the Three.js viewer.

## Rebuild

```bash
python3 scripts/build_body.py --dry-run   # inspect classification
python3 scripts/build_body.py             # classify + extract + merge
bash scripts/compress.sh                  # Draco-compress meshes (62MB -> ~5MB)
```

Serve from the repository root (`r22/`) and open `body/web/index.html`:

```bash
python3 -m http.server 8000
# → http://localhost:8000/body/web/
```

## Data & license

Meshes: **BodyParts3D** — `(c) The Database Center for Life Science`,
licensed under CC BY-SA 2.1 JP. See `models/LICENSE.md`.
Citation: Mitsuhashi N, et al. *Nucleic Acids Res.* 2009;37:D782-5.
doi:10.1093/nar/gkn613
