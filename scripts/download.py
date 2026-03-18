"""
Download PIT and HIC data files from HUD User (huduser.gov).

Files are hosted as single workbooks spanning all available years (2007-present).
Run this script to populate data/raw/ before running compile.py.
"""

import os
import requests
from tqdm import tqdm

BASE_URL = "https://www.huduser.gov"

FILES = {
    "pit": [
        {
            "url": "/portal/sites/default/files/xls/2007-2024-PIT-Counts-by-CoC.xlsb",
            "filename": "2007-2024-PIT-Counts-by-CoC.xlsb",
        },
        {
            "url": "/portal/sites/default/files/xls/2007-2024-PIT-Counts-by-State.xlsb",
            "filename": "2007-2024-PIT-Counts-by-State.xlsb",
        },
        {
            "url": "/portal/sites/default/files/xls/2011-2024-PIT-Veteran-Counts-by-CoC.xlsx",
            "filename": "2011-2024-PIT-Veteran-Counts-by-CoC.xlsx",
        },
    ],
    "hic": [
        {
            "url": "/portal/sites/default/files/xls/2007-2024-HIC-Counts-by-CoC.xlsx",
            "filename": "2007-2024-HIC-Counts-by-CoC.xlsx",
        },
        {
            "url": "/portal/sites/default/files/xls/2007-2024-HIC-Counts-by-State.xlsx",
            "filename": "2007-2024-HIC-Counts-by-State.xlsx",
        },
    ],
}

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def download_file(url, dest_path):
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()
    total = int(response.headers.get("content-length", 0))
    with open(dest_path, "wb") as f, tqdm(
        desc=os.path.basename(dest_path),
        total=total,
        unit="B",
        unit_scale=True,
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            bar.update(len(chunk))


def main():
    for folder, files in FILES.items():
        dest_dir = os.path.join(RAW_DIR, folder)
        os.makedirs(dest_dir, exist_ok=True)
        for file in files:
            dest_path = os.path.join(dest_dir, file["filename"])
            if os.path.exists(dest_path):
                print(f"Already exists, skipping: {file['filename']}")
                continue
            print(f"Downloading: {file['filename']}")
            download_file(BASE_URL + file["url"], dest_path)

    print("\nAll files downloaded to data/raw/")


if __name__ == "__main__":
    main()
