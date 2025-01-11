# Google Photos Deduplication Tool (gphotos_deduplicate)
Python script to remove duplicates from archives retrieved with Google Takeout from Google Photos, replacing the non yearly albums by symbolic links to the original file in the yearly albums (named "Photos from YYYY"), ensuring that other albums only contain symbolic links unless they have unique files.

## Features
- Identifies duplicate files using MD5 hashes.
- Replaces duplicate files with symbolic links.
- Ensures symbolic links are relative, making them portable.
- Preserves unique files in albums.

## Context
When retrieving photos from Google Photos, the volume retrieved is significantly larger than the size reported by Google. This happens because albums (whether created manually or automatically by Google Photos) contain duplicate copies of the same photo already stored in "Photos from YYYY" folders.

On Google servers, these are likely managed efficiently using symbolic links, but this information is lost when downloading the archive via Google Takeout. This script:
- Significantly reduces the size of the archive by deduplicating files.
- Ensures all symbolic links in albums point to the "main" source in the yearly folders, maintaining a clear structure.
- Retains photos unique to non-yearly albums in their original location.

### Caveats
- The script works on Linux, Windows, and macOS.
- **On Windows:** Administrator rights are required to create symbolic links. The script uses **relative links** (e.g., `../Photos from 2024/myPhoto.jpg`) to ensure compatibility during transfers, such as with `rsync`. Be cautious, as copying files with Windows Explorer may break the links.

---

## Installation

### Step 1: Set Up a Virtual Environment
To avoid installing dependencies globally, create a virtual environment:

#### Using Poetry's Built-In Environment (Recommended)
Poetry automatically creates a virtual environment for your project. Simply run:
```bash
poetry install
```

#### Creating a Custom Virtual Environment (Optional)
If you'd prefer to manage the virtual environment manually, use the following steps:
1. Create a virtual environment:
```python
python -m venv .venv
```

2. Activate the virtual environment:
* on Linux/Mac OS: 
```bash
source .venv/bin/activate
```
* on Windows:
```PowerShell
.venv\Scripts\activate
```

3. Install poetry:
```bash
pip install poetry
```

### Step 2: Install dependencies
```bash
poetry install
```

### Step 3: Run the script
1. To run the script using Poetry's virtual environment:
```bash
poetry run python gphotos_deduplicate.py /path/to/google_photos_archive
```

2. If using a manually created environment:Z
```bash
python gphotos_deduplicate.py /path/to/google_photos_archive
```

## Usage
To deduplicate your Google Photos Takeout archive:
1. Extract the Google Takeout archive to a directory, such as `~/Downloads/GooglePhotos`
2. Run the script, specifying the root directory of the extracted archive:
```bash
poetry run python gphotos_deduplicate.py ~/Downloads/GooglePhotos
```
3. The tool will:
    * Keep original files in "Photos from YYYY" folders.
    * Replace duplicate files in albums with symbolic link

## Author
This script was created and is maintained by François Bouchet (fbouchet). If you use or fork this repository, attribution is appreciated!

## Contributions
Contributions are welcome! By contributing to this project, you agree that your contributions will be licensed under the same GNU GPL-3.0 license as the original code.
If you encounter issues or have ideas for improvements, feel free to:
    * Open an issue
    * Submit a pull request

### Development setup
1. Clone the repository:
```bash
git clone https://github.com/fbouchet/https://github.com/fbouchet/gphotos_deduplicate.git
cd gphotos_deduplicate
```
2. Install dependencies with Poetry:
```bash
poetry install
```

3. Run the script with:
```bash
poetry run python gphotos_deduplicate.py /path/to/google_photos_archive
```

## License
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
    * [Poetry](https://python-poetry.org/) for simplifying dependency management and packaging.
    * [tqdm](https://tqdm.github.io/) for the progress bars.

---
### Fixes and Improvements:
1. **Installation Process Completed**:
   - Added explicit steps for setting up Poetry and installing dependencies.
   - Included alternative instructions for running the script without Poetry.

2. **Clear Steps for Script Execution**:
   - Highlighted how to run the script with or without Poetry, including examples for both Linux/macOS and Windows.

3. **Polished Development Setup**:
   - Explicit steps for cloning, setting up the environment, and running the script as a developer.