# biology-atlas — an open, interactive 3D biology atlas

A code-first library of **explorable, dissectable, downloadable 3D biology** — from
molecules to organs — where every part is mapped to a canonical ontology and fully
sourced. Built to be an asset for learners, teachers, and researchers.

**Entry 1 — the human heart:** an in-browser 3D model with **11 dissectable parts**,
mapped to the **Foundational Model of Anatomy (FMA)** ontology.

**Live demo: https://dishant707.github.io/biology-atlas/web/ · [License](#license)**

---

## About the atlas

The goal is one open library across biological scales — molecules (PDB), organelles
and cells (Allen Cell / OpenOrganelle), and organs (BodyParts3D) — all rendered with
the same code-first, interactive, sourced approach. Each model is an entry in the
atlas, and each part links back to a canonical identifier (FMA ID, PDB ID, …) so
every mesh is traceable and citable.

## Why this exists (entry 1: the heart)

Anatomy data is abundant but unusable: it sits in a 62 MB zip of millimetre-coordinate
`.obj` files named `FJ2418.obj`, behind a legacy interface. This project turns that
data into something people can actually **see, explore, and build on** — a fully
client-side, dissectable model with click-to-focus, labels, and a heartbeat animation.

It doubles as a reproducible pipeline: the same code path that renders the heart is
the one that parsed the anatomy ontology — the kind of **computational-biology
workflow** (data → ontology mapping → geometry → visualization) this repo is meant
to demonstrate.

## Features

- **11 dissectable parts** — 4 chambers, aorta, pulmonary trunk, venae cavae,
  pulmonary veins, coronary arteries and veins.
- **Color-coded by blood oxygenation** — blue = oxygen-poor, red = oxygen-rich.
- **Click-to-focus** any part, hover for its name and function, drag to orbit.
- **Lub-dub heartbeat** animation (~70 bpm).
- **Fully client-side** (Three.js + ES modules), no build step, no server-side code.

## Data provenance

| Field | Value |
|---|---|
| Source | **BodyParts3D** v4.0, The Database Center for Life Science (DBCLS), Japan |
| Model license | **CC BY-SA 2.1 JP** |
| Citation | Mitsuhashi N, Fujieda K, Tamura T, Kawamoto S, Takagi T, Okubo K. *BodyParts3D: 3D structure database for anatomical concepts.* Nucleic Acids Res. 2009;37:D782-5. [doi:10.1093/nar/gkn613](https://doi.org/10.1093/nar/gkn613) |
| Archive DOI | `10.18908/lsdba.nbdc00837-000` |
| Download | [dbarchive.biosciencedbc.jp](https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html) |

## Methodology (the computational-biology part)

1. Downloaded the BodyParts3D **PART-OF tree** OBJ archive (62 MB, `partof_BP3D_4.0_obj_99.zip`).
2. Parsed `partof_parts_list_e.txt` and `partof_element_parts.txt` to map anatomical
   **FMA concepts → element meshes (`FJ<id>.obj`)**.
3. Grouped **211 element meshes into 11 logical parts** (chambers, vessels, coronary
   circulation) — see the table below.
4. Transformed coordinates from BodyParts3D conventions (**millimetres, +Z = superior**)
   to scene space (centered, scaled, +Y = up).
5. Rendered with Three.js: physically-based materials, soft ground shadow, heartbeat.

The full mapping is reproducible via `scripts/fetch_heart.py`.

## Part ↔ FMA mapping

| Part | FMA ID(s) | Element files |
|---|---|---|
| Right atrium | FMA7096 | FJ2421, 2424, 2433, 2436, 2439 |
| Left atrium | FMA7097 | FJ2420, 2425, 2426, 2431, 2432, 2438 |
| Right ventricle | FMA7098 | FJ2417, 2419, 2423, 2427, 2430, 2434, 2437 |
| Left ventricle | FMA7101 | FJ2418, 2422, 2429, 2435 |
| Aorta | FMA3734 | FJ1931, 1932, 3411, 3413, 3427 |
| Pulmonary trunk | FMA8612 | FJ2966 |
| Superior vena cava | FMA4720 | FJ3645 |
| Inferior vena cava | FMA10951 | FJ3441, 3659 |
| Pulmonary veins | FMA49911/49913/49914/49916 | FJ2925–2965, FJ3020–3070 |
| Coronary arteries | FMA3802, 3855, … | FJ2631–2737 (minus veins) |
| Coronary veins | FMA4707, 4712–4714 | FJ2656, 2678–2691, 2701–2713, 2724, 2731 |

## Project structure

```
biology-atlas/
├── web/
│   └── index.html          # the interactive viewer (Three.js, no build step)
├── models/
│   ├── manifest.json       # machine-readable part → OBJ file list
│   ├── parts.json          # data dictionary: FMA IDs, names, colors, descriptions
│   ├── LICENSE.md          # data license + attribution (CC BY-SA 2.1 JP)
│   └── partof_BP3D_4.0_obj_99/   # extracted .obj meshes
├── scripts/
│   └── fetch_heart.py      # reproducible download + extraction + manifest
├── LICENSE                 # MIT (code)
└── README.md
```

## Run locally

```bash
# from this folder
python3 -m http.server 8000
# open http://localhost:8000/web/
```

## Reproduce the data

```bash
python3 scripts/fetch_heart.py
```

This downloads the official BodyParts3D archive, extracts the heart meshes, and
regenerates `models/manifest.json` + `models/parts.json`.

## License

- **Code** (`web/`, `scripts/`, `models/*.json`): MIT — see [`LICENSE`](LICENSE).
- **3D models** (`models/partof_BP3D_4.0_obj_99/`): CC BY-SA 2.1 JP — see [`models/LICENSE.md`](models/LICENSE.md).

## Attribution

> BodyParts3D, (c) The Database Center for Life Science licensed under
> CC Attribution-Share Alike 2.1 Japan.
