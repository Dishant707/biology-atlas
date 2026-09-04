#!/usr/bin/env python3
"""
Reproducible extraction of the dissectable human brain from BodyParts3D.

Downloads the official BodyParts3D PART-OF tree OBJ archive, extracts the brain
element meshes, groups them into 8 anatomical parts (mapped to FMA IDs), and
writes models/brain/manifest.json.

Run from the repo root:
    python3 scripts/fetch_brain.py

Data source (CC BY-SA 2.1 JP):
    BodyParts3D, (c) The Database Center for Life Science
    https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html
    Mitsuhashi N et al. Nucleic Acids Res. 2009;37:D782-5. doi:10.1093/nar/gkn613
"""
import json
import os
import urllib.request
import zipfile

ZIP_URL = "https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/partof_BP3D_4.0_obj_99.zip"
ZIP_NAME = "partof_BP3D_4.0_obj_99.zip"
ZIP_PREFIX = "partof_BP3D_4.0_obj_99/"
OUT_DIR = os.path.join("models", "brain")

# FMA concept -> element mesh ids (FJ<id>.obj), from partof_element_parts.txt
BRAIN = {
    "frontal_lobe":    ["FJ1745", "FJ1788", "FJ1801", "FJ1834", "FJ1744", "FJ1787", "FJ1800", "FJ1833"],  # FMA72969+72970
    "parietal_lobe":   ["FJ1733", "FJ1798", "FJ1836", "FJ1842", "FJ1732", "FJ1797", "FJ1835", "FJ1841"],  # FMA72973+72974
    "temporal_lobe":   ["FJ1747", "FJ1784", "FJ1786", "FJ1790", "FJ1746", "FJ1783", "FJ1785", "FJ1789"],  # FMA72971+72972
    "occipital_lobe":  ["FJ1792", "FJ1791"],                                                               # FMA72975+72976
    "cerebellum":      ["FJ1781", "FJ1830"],                                                               # FMA67944
    "brainstem":       ["FJ1738", "FJ1762", "FJ1769", "FJ1770", "FJ1775", "FJ1779", "FJ1810", "FJ1817", "FJ1822", "FJ1826", "FJ1831"],  # FMA79876
    "diencephalon":    ["FJ1730", "FJ1743", "FJ1760", "FJ1780", "FJ1795", "FJ1808", "FJ1828"],            # FMA62001
    "deep_structures": ["FJ1731", "FJ1739", "FJ1740", "FJ1748", "FJ1749", "FJ1750", "FJ1751", "FJ1758", "FJ1759", "FJ1767", "FJ1806", "FJ1807", "FJ1814"],  # basal ganglia / limbic
}


def download_zip():
    if os.path.exists(ZIP_NAME):
        print(f"Using cached {ZIP_NAME}")
    else:
        print(f"Downloading {ZIP_URL} ...")
        urllib.request.urlretrieve(ZIP_URL, ZIP_NAME)


def extract():
    z = zipfile.ZipFile(ZIP_NAME)
    os.makedirs(OUT_DIR, exist_ok=True)
    manifest = {}
    for part, files in BRAIN.items():
        got = []
        for f in files:
            zname = ZIP_PREFIX + f + ".obj"
            if zname in z.namelist():
                z.extract(zname, OUT_DIR)
                got.append(f)
        manifest[part] = got
        print(f"{part:16s} {len(got)}/{len(files)} files")
    with open(os.path.join(OUT_DIR, "manifest.json"), "w") as fp:
        json.dump(manifest, fp, indent=2)
    print("wrote", os.path.join(OUT_DIR, "manifest.json"))


if __name__ == "__main__":
    download_zip()
    extract()
