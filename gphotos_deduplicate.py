# MyScript.py
# Original source: https://github.com/fbouchet/gphotos_deduplicate
# Copyright (C) 2025 François Bouchet (fbouchet@pm.me)
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import os
import hashlib
from pathlib import Path
from tqdm import tqdm

def calculate_md5(file_path):
    """Calculate the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def find_files(directory):
    """Find all files and group them by MD5 hash."""
    md5_to_files = {}
    all_files = []

    # Collect all files for progress tracking
    for root, _, files in os.walk(directory):
        for file in files:
            all_files.append(os.path.join(root, file))

    # Calculate MD5 for each file with progress bar
    for file_path in tqdm(all_files, desc="Scanning files"):
        file_md5 = calculate_md5(file_path)
        if file_md5 not in md5_to_files:
            md5_to_files[file_md5] = []
        md5_to_files[file_md5].append(file_path)

    return md5_to_files

def replace_album_copies(md5_to_files, main_folder_identifier="Photos from"):
    """Replace album copies with symbolic links to originals in 'Photos from YYYY' folders."""
    total_duplicates = sum(len(paths) - 1 for paths in md5_to_files.values() if len(paths) > 1)

    with tqdm(total=total_duplicates, desc="Replacing duplicates") as pbar:
        for md5, file_paths in md5_to_files.items():
            if len(file_paths) > 1:
                # Identify the main file in "Photos from YYYY"
                main_file = next((f for f in file_paths if main_folder_identifier in Path(f).parent.name), None)

                if main_file:
                    # For all other files, replace them with symbolic links to the main file
                    for file_path in file_paths:
                        if file_path != main_file:
                            try:
                                original = Path(main_file).resolve()
                                duplicate = Path(file_path).resolve()
                                duplicate.unlink()
                                duplicate.symlink_to(original.relative_to(duplicate.parent))
                                pbar.update(1)
                            except Exception as e:
                                print(f"Error replacing {file_path}: {e}")
                else:
                    # If no main file exists, keep the first file as the original
                    original = Path(file_paths[0]).resolve()
                    for file_path in file_paths[1:]:
                        try:
                            duplicate = Path(file_path).resolve()
                            duplicate.unlink()
                            duplicate.symlink_to(original.relative_to(duplicate.parent))
                            pbar.update(1)
                        except Exception as e:
                            print(f"Error replacing {file_path}: {e}")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Deduplicate Google Photos Takeout archive by replacing duplicates with symbolic links.")
    parser.add_argument("directory", help="The root directory of your Google Photos archive.")
    args = parser.parse_args()

    directory = Path(args.directory).resolve()

    if not directory.is_dir():
        print("The provided path is not a directory.")
        return

    print("Scanning files and grouping by MD5 hash...")
    md5_to_files = find_files(directory)

    print("Replacing album copies with symbolic links...")
    replace_album_copies(md5_to_files, main_folder_identifier="Photos from")

    print("Cleanup complete.")
