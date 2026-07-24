#!/usr/bin/env python3
"""Fetch useful podcast metadata from an Archive.org item.

Usage:
  python3 scripts/archive_metadata.py ARCHIVE_ID
  python3 scripts/archive_metadata.py content/programas/programa/episodio/index.md

The script prints YAML snippets that can be copied into episode front matter.
It uses only Python standard library.
"""

import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path


def die(msg):
    raise SystemExit(msg)


def archive_id_from_arg(arg):
    path = Path(arg)
    if path.exists() and path.is_file():
        text = path.read_text(encoding="utf-8")
        m = re.search(r"archive:\s*(?:\n|\r\n)(?:.*\n)*?\s+id:\s*[\"']?([^\"'\n]+)", text)
        if m:
            return m.group(1).strip()
        die(f"No encontré archive.id en {arg}")
    return arg.strip().rstrip("/").split("/")[-1]


def fetch_metadata(identifier):
    url = f"https://archive.org/metadata/{identifier}"
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.load(response)


def pick_audio(files):
    candidates = []
    for f in files:
        name = f.get("name", "")
        fmt = f.get("format", "")
        lower = name.lower()
        if lower.endswith((".mp3", ".m4a", ".ogg", ".wav")) or "mp3" in fmt.lower():
            try:
                size = int(f.get("size") or 0)
            except ValueError:
                size = 0
            candidates.append((size, f))
    if not candidates:
        return None
    return sorted(candidates, key=lambda item: item[0], reverse=True)[0][1]


def pick_image(files):
    images = []
    for f in files:
        name = f.get("name", "")
        lower = name.lower()
        if not lower.endswith((".jpg", ".jpeg", ".png", ".webp")):
            continue
        penalty = 0
        if "thumb" in lower or "spectrogram" in lower or lower.startswith("__ia_"):
            penalty = 1
        try:
            size = int(f.get("size") or 0)
        except ValueError:
            size = 0
        images.append((penalty, -size, f))
    if not images:
        return None
    return sorted(images, key=lambda item: (item[0], item[1]))[0][2]


def duration_from_seconds(value):
    if value in (None, ""):
        return ""
    seconds = int(round(float(value)))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def subjects_to_tags(subject):
    if not subject:
        return []
    if isinstance(subject, list):
        raw = subject
    else:
        # Archive sometimes returns one string. Split conservatively.
        raw = re.split(r"\s*;\s*|\s*,\s*", str(subject))
    tags = []
    seen = set()
    for tag in raw:
        tag = str(tag).strip()
        if not tag:
            continue
        key = tag.casefold()
        if key not in seen:
            seen.add(key)
            tags.append(tag)
    return tags


def quote_url(identifier, filename):
    return f"https://archive.org/download/{urllib.parse.quote(identifier)}/{urllib.parse.quote(filename)}"


def yaml_quote(value):
    return json.dumps(str(value), ensure_ascii=False)


def main():
    if len(sys.argv) != 2:
        die(__doc__)

    identifier = archive_id_from_arg(sys.argv[1])
    data = fetch_metadata(identifier)
    metadata = data.get("metadata", {})
    files = data.get("files", [])
    audio = pick_audio(files)
    image = pick_image(files)
    tags = subjects_to_tags(metadata.get("subject"))

    print(f"# Archive.org ID: {identifier}")
    print(f"# Details: https://archive.org/details/{identifier}")
    print(f"# Metadata: https://archive.org/metadata/{identifier}")
    print()

    if metadata.get("title"):
        print(f"# title: {metadata['title']}")
    if metadata.get("description"):
        desc = re.sub(r"<[^>]+>", "", str(metadata["description"]))
        desc = re.sub(r"\s+", " ", desc).strip()
        print(f"# description: {desc}")
    print()

    if image:
        image_url = quote_url(identifier, image["name"])
        print(f"image: {yaml_quote(image_url)}")
        print("archive:")
        print(f"  id: {yaml_quote(identifier)}")
        print(f"  url: {yaml_quote('https://archive.org/details/' + identifier)}")
        print(f"  image: {yaml_quote(image_url)}")
    else:
        print("archive:")
        print(f"  id: {yaml_quote(identifier)}")
        print(f"  url: {yaml_quote('https://archive.org/details/' + identifier)}")

    if audio:
        audio_url = quote_url(identifier, audio["name"])
        duration = duration_from_seconds(audio.get("length"))
        if duration:
            print(f"duration: {yaml_quote(duration)}")
        print("audio:")
        print(f"  - {yaml_quote(audio_url)}")
        print("enclosures:")
        print(f"  - url: {yaml_quote(audio_url)}")
        print('    type: "audio/mpeg"')
        if audio.get("size"):
            print(f"    length: {audio['size']}")

    if tags:
        print("tags:")
        for tag in tags:
            print(f"  - {yaml_quote(tag)}")

    print()
    print(f'body shortcode: {{{{< archive-player id="{identifier}" >}}}}')


if __name__ == "__main__":
    main()
