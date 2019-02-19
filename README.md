
# Download from mangareader.net
Python script to download image files from website **https://www.mangareader.net**.
It allows to download an entire manga, a specific chapter, or the last N chapters.

## Usage
```bash
usage: dlMangaReader.py [-h] [-s SHOW] [-m MANGA] [-c CHAP] [-l LAST]

optional arguments:
  -h, --help            show this help message and exit
  -s SHOW, --show SHOW  list of all available mangas that include a search
                        pattern
  -m MANGA, --manga MANGA
                        select a manga to download
  -c CHAP, --chap CHAP  select a specific chapter of a manga to download
  -l LAST, --last LAST  select a last N chapter of a manga to download
```

## File tree
```bash
.
├── dlMangaReader.py
├── README.md
├── manga-1
│   ├── manga-1_chap0001
│   │   ├── manga-1_chap0001_001.jpg
│   │   ├── manga-1_chap0001_002.jpg
│   │   ├── ...
│   ├── manga-1_chap0002
│   │   ├── manga-1_chap0002_001.jpg
│   │   ├── manga-1_chap0002_002.jpg
│   │   ├── ...
├── manga-2
│   ├── manga-2_chap0001
│   │   ├── manga-2_chap0001_001.jpg
│   │   ├── manga-2_chap0001_002.jpg
│   │   ├── ...
│   ├── manga-2_chap0002
│   │   ├── manga-2_chap0002_001.jpg
│   │   ├── manga-2_chap0002_002.jpg
│   │   ├── ...
├── ...
```

All spaces in manga name are replaced by "-" and all characters are in lowercase.
Manga folders are created only if they don't already exist.
Chapter folders are created only if they don't already exists and are in the format *mangaName_chapXXXX* (*XXXX* corresponds to chapter number, always with 4 digits, filled with 0 if needed).

## Search for manga names
```bash
python dlMangaReader.py -s [search]
```
Where *search* corresponds to a part of manga names (ex: *piece*).
It shows the list of manga where the name includes *search*.

## Download an entire manga
```bash
python dlMangaReader.py -m [mangaName]
```
Where *mangaName* corresponds to the name of wanted manga to download  (ex: *one-piece*).

## Download a specific chapter of a manga
```bash
python dlMangaReader.py -m [mangaName] -c [chapter]
```
Where *mangaName* corresponds to the name of wanted manga  (ex: *one-piece*) and *chapter* is a number that corresponds to the wanted chapter (ex: *900*).

## Download the last N chapters of a manga
```bash
python dlMangaReader.py -m [mangaName] -l [N]
```
Where *mangaName* corresponds to the name of wanted manga  (ex: *one-piece*) and *N* corresponds to the number of last chapters to download. (ex: *10*).