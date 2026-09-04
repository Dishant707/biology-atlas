#!/usr/bin/env python3
"""
Reproducible extraction of the dissectable human heart from BodyParts3D.

Downloads the official BodyParts3D PART-OF tree OBJ archive, extracts the heart
element meshes, groups them into 11 anatomical parts (mapped to FMA IDs), and
writes models/manifest.json.

Run from the repo root:
    python3 scripts/fetch_heart.py

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

# FMA concept -> constituent element mesh ids (FJ<id>.obj)
# Derived from partof_element_parts.txt (concept id | name | element file id)
FMA_ELEMENTS = {
    "FMA7096": ["FJ2421", "FJ2424", "FJ2433", "FJ2436", "FJ2439"],                    # right atrium
    "FMA7097": ["FJ2420", "FJ2425", "FJ2426", "FJ2431", "FJ2432", "FJ2438"],          # left atrium
    "FMA7098": ["FJ2417", "FJ2419", "FJ2423", "FJ2427", "FJ2430", "FJ2434", "FJ2437"],  # right ventricle
    "FMA7101": ["FJ2418", "FJ2422", "FJ2429", "FJ2435"],                               # left ventricle
    "FMA3734": ["FJ1931", "FJ1932", "FJ3411", "FJ3413", "FJ3427"],                    # aorta
    "FMA8612": ["FJ2966"],                                                            # pulmonary trunk
    "FMA4720": ["FJ3645"],                                                            # superior vena cava
    "FMA10951": ["FJ3441", "FJ3659"],                                                 # inferior vena cava
}

# coronary veins (explicit FJ ids from partof_element_parts.txt)
CORONARY_VEIN_IDS = set([2656] + list(range(2678, 2692)) + list(range(2701, 2714)) + [2724, 2731])
# coronary arteries = heart vessel range 2631..2737, minus the veins
CORONARY_ARTERY_IDS = [f"FJ{i}" for i in range(2631, 2738) if i not in CORONARY_VEIN_IDS]
CORONARY_VEIN_LIST = [f"FJ{i}" for i in sorted(CORONARY_VEIN_IDS)]

# pulmonary veins: 4 trunks (many intrapulmonary segments)
PULMONARY_VEIN_IDS = [f"FJ{i}" for i in list(range(2925, 2966)) + list(range(3020, 3071))]

PARTS = {
    "right_atrium":      FMA_ELEMENTS["FMA7096"],
    "left_atrium":       FMA_ELEMENTS["FMA7097"],
    "right_ventricle":   FMA_ELEMENTS["FMA7098"],
    "left_ventricle":    FMA_ELEMENTS["FMA7101"],
    "aorta":             FMA_ELEMENTS["FMA3734"],
    "pulmonary_trunk":   FMA_ELEMENTS["FMA8612"],
    "svc":               FMA_ELEMENTS["FMA4720"],
    "ivc":               FMA_ELEMENTS["FMA10951"],
    "pulmonary_veins":   PULMONARY_VEIN_IDS,
    "coronary_arteries": CORONARY_ARTERY_IDS,
    "coronary_veins":    CORONARY_VEIN_LIST,
}


def download_zip():
    if os.path.exists(ZIP_NAME):
        print(f"Using cached {ZIP_NAME}")
    else:
        print(f"Downloading {ZIP_URL} ...")
        urllib.request.urlretrieve(ZIP_URL, ZIP_NAME)


def extract():
    z = zipfile.ZipFile(ZIP_NAME)
    manifest = {}
    for part, files in PARTS.items():
        got = []
        for f in files:
            zname = ZIP_PREFIX + f + ".obj"
            if zname in z.namelist():
                z.extract(zname, "models")
                got.append(f)
        manifest[part] = got
        print(f"{part:18s} {len(got)}/{len(files)} files")
    with open(os.path.join("models", "manifest.json"), "w") as fp:
        json.dump(manifest, fp, indent=2)
    print("wrote models/manifest.json")


if __name__ == "__main__":
    download_zip()
    extract()
