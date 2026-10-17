#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 13:29:48 2026

@author: tigrangasparian
"""

import re
from pathlib import Path
from PIL import Image
import pytesseract
import pandas as pd
import matplotlib.pyplot as plt


IMAGE_DIR = Path("/Users/tigrangasparian/Saved/More/TW results")
POSITION_POINTS = {1: 14,
                   2: 11,
                   3: 9,
                   4: 7,
                   5: 6,
                   6: 5,
                   7: 4,
                   8: 3,
                   9: 2,
                   10: 1,
                   11: 0,
                   12: 0}

BEST_LAP_POINTS = {1: 0,
                   2: 0,
                   3: 0,
                   4: 0,
                   5: 0,
                   6: 0,
                   7: 0,
                   8: 0,
                   9: 0,
                   10: 0,
                   11: 0,
                   12: 0}

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def extract_section(text: str, header: str, next_headers: list[str]) -> list[str]:

    pattern = rf"{header}\s*\n(.*?)(?={'|'.join(next_headers)}|$)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)

    if not match:
        return []


    lines = match.group(1).splitlines()
    return [line.strip() for line in lines if line.strip()]

def main():
    if not IMAGE_DIR.exists():
        print(f"Error: Folder '{IMAGE_DIR}' does not exist.")
        return

    image_files = sorted([
        file
        for file in IMAGE_DIR.iterdir()
        if file.is_file() and file.suffix.lower() in VALID_EXTENSIONS
    ])
    image_files = sorted(
    image_files,
    key=lambda x: [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', x.name)]
    )
    if not image_files:
        print("No images found in the directory.")
        return

    print(f"Found {len(image_files)} image(s) to process...\n")
    all_dfs = []
    for i, image_path in enumerate(image_files, start=1):
        with Image.open(image_path) as img:
            full_text = pytesseract.image_to_string(img)

            names = extract_section(
                full_text, "Name", ["Best Lap", "Time"]
                )
            best_laps = extract_section(
                full_text, "Best Lap", ["Time", "Name"]
                )
            times = extract_section(
                full_text, "Time", ["Name", "Best Lap"]
                )
            min_len = min(len(names), len(best_laps), len(times))
            names = names[:min_len]
            best_laps = best_laps[:min_len]
            times = times[:min_len]

            df = pd.DataFrame(
                {"Name": names,
                 "Time": times, 
                 "Best Lap": best_laps}
                )
            df["Pos Pts"] = (
            (df.index+1).map(POSITION_POINTS).fillna(0).astype(int)
            )

            # Convert 'Best Lap' to timedelta temporarily for accurate sorting
            lap_times_td = pd.to_timedelta("00:" + df["Best Lap"])
            df["BL Rank"] = lap_times_td.rank(method="min").astype(int)
            df["Lap Pts"] = (
            (df["BL Rank"]).map(BEST_LAP_POINTS).fillna(0).astype(int)
            )
            df["Total Pts"] = df["Pos Pts"] + df["Lap Pts"]

            print("```")
            print(f"Processing Race {i}: {image_path.name}")
            print(df)
            print("```")
            print(" ")

            all_dfs.append(df[["Name", "Total Pts"]])
            combined_df = pd.concat(all_dfs, ignore_index=True, axis=0)
            plt.imshow(img)
            plt.axis('off')
            plt.show()

    results_df = (
        combined_df.groupby("Name", as_index=False)["Total Pts"]
        .sum()
        .sort_values(by="Total Pts", ascending=False)
    )
    results_df = results_df.reset_index(drop=True)
    results_df.index = results_df.index + 1
    results_df['Total Pts'] = results_df['Total Pts'].astype(int)

    print("```")
    for rank, row in results_df.iterrows():
        print(f"{rank:<3}{row['Name']:<{results_df['Name'].str.len().max() + 2}}{row['Total Pts']}")
    print("```")

if __name__ == "__main__":
    main()
