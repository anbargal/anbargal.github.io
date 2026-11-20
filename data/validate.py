#!/usr/bin/env python3
"""Validate data/thiruppugazh.jsonl against the schema documented in data/README.md.

Usage:
    python3 data/validate.py            # grouped summary
    python3 data/validate.py --verbose  # one line per finding
    python3 data/validate.py --strict   # warnings also fail the run

Exit status: 0 when there are no errors, 1 otherwise.
Stdlib only, so it runs anywhere without a build step.
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "thiruppugazh.jsonl"

REQUIRED_KEYS = {
    "kaumaram": int,
    "tiv": int,
    "title": str,
    "title_en": (str, type(None)),
    "ragam": (str, type(None)),
    "thalam": (str, type(None)),
    "kshetram": (str, type(None)),
    "stanzas": dict,
    "youtube": list,
}

# Keys from the one-off scrape that produced TIV 442-451. They are not part of
# the schema and must never come back: the site reads `stanzas`, not `charanam`,
# and `youtube`, not `youtubeId`.
FORBIDDEN_KEYS = {"charanam", "youtubeId"}

ALLOWED_STANZA_KEYS = {"santham", "charanams"}

# Text that only appears when a whole blog page (instead of the lyrics) was stored.
JUNK_PATTERNS = [
    re.compile(r"Skip to main content", re.I),
    re.compile(r"Search This Blog", re.I),
    re.compile(r"\bGet link\b", re.I),
    re.compile(r"adsbygoogle"),
    re.compile(r"&(?:#\d+|#x[0-9a-f]+|[a-z]+);", re.I),
    re.compile(r"</?[a-z][^>]*>", re.I),
    re.compile(r"\.{3,}\s*பாடல்\s*\.{3,}"),
    re.compile(r"^\s*(?:ராகம்|தாளம்)\s*:"),
    re.compile(r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}\b"),
]

# "NNN. <title>" is the blog post heading, not the song title.
NUMBERED_TITLE = re.compile(r"^\s*\d+\.\s")

YOUTUBE_URL = re.compile(
    r"^https://(?:www\.)?(?:"
    r"youtube\.com/watch\?v=[A-Za-z0-9_-]{11}"
    r"|youtu\.be/[A-Za-z0-9_-]{11}"
    r")(?:[?&][^\s]*)?$"
)

# Legitimate values top out at 29 chars for ragam and 52 for thalam (a thalam may
# carry its akshara signature). Anything much longer means song text leaked in.
MAX_RAGAM_LEN = 50
MAX_THALAM_LEN = 80

# Tala vocabulary that must never appear in the ragam field.
TALA_WORDS = ("தாளம்", "நடை", "ஜம்பை", "சாபு", "திச்ர", "மிஸ்ர", "கண்ட")


class Report:
    def __init__(self):
        self.findings = []  # (severity, rule, tiv, message)

    def add(self, severity, rule, tiv, message):
        self.findings.append((severity, rule, tiv, message))

    def error(self, rule, tiv, message):
        self.add("ERROR", rule, tiv, message)

    def warn(self, rule, tiv, message):
        self.add("WARN", rule, tiv, message)

    def count(self, severity):
        return sum(1 for f in self.findings if f[0] == severity)


def is_blank(value):
    return not isinstance(value, str) or not value.strip()


def display_path(path):
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def junk_hit(text):
    for pattern in JUNK_PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group(0)
    return None


def iter_lyrics(record):
    stanzas = record.get("stanzas")
    if not isinstance(stanzas, dict):
        return
    for line in stanzas.get("santham") or []:
        yield "santham", line
    for index, charanam in enumerate(stanzas.get("charanams") or []):
        if not isinstance(charanam, list):
            continue
        for line in charanam:
            yield "charanams[%d]" % index, line


def check_record(report, record, tiv):
    # Unknown / forbidden keys.
    present = set(record)
    for key in sorted(present & FORBIDDEN_KEYS):
        report.error(
            "forbidden-legacy-key",
            tiv,
            "`%s` is not in the schema (use `%s`)"
            % (key, "stanzas" if key == "charanam" else "youtube"),
        )
    for key in sorted(present - set(REQUIRED_KEYS)):
        if key not in FORBIDDEN_KEYS:
            report.warn("unknown-key", tiv, "unexpected key `%s`" % key)

    # Missing keys and types. An absent `youtube` is a warning, not an error:
    # some songs genuinely have no performance video (see remarks.md).
    for key, expected in REQUIRED_KEYS.items():
        if key not in record:
            if key == "youtube":
                report.warn("youtube-missing", tiv, "no `youtube` key")
            else:
                report.error("missing-key", tiv, "missing `%s`" % key)
            continue
        value = record[key]
        if not isinstance(value, expected) or isinstance(value, bool):
            names = (
                expected.__name__
                if isinstance(expected, type)
                else "/".join(t.__name__ for t in expected)
            )
            report.error(
                "field-type", tiv, "`%s` must be %s, got %s" % (key, names, type(value).__name__)
            )

    for key in ("tiv", "kaumaram"):
        value = record.get(key)
        if isinstance(value, int) and not isinstance(value, bool) and value <= 0:
            report.error("field-type", tiv, "`%s` must be positive" % key)

    # Title.
    title = record.get("title")
    if isinstance(title, str):
        if is_blank(title):
            report.error("title-invalid", tiv, "title is empty")
        elif NUMBERED_TITLE.match(title):
            report.error("title-invalid", tiv, "title carries the blog heading number: %r" % title)
        else:
            hit = junk_hit(title)
            if hit:
                report.error("lyrics-junk", tiv, "title contains %r" % hit)

    # Romanised title: presence is mandatory because the site renders it
    # unconditionally, so a null here shows up as " - None" in the table.
    title_en = record.get("title_en")
    if "title_en" in record and (title_en is None or is_blank(title_en)):
        report.error("title-en-missing", tiv, "title_en is empty/null")
    elif isinstance(title_en, str):
        if re.search(r"[\u0B80-\u0BFF]", title_en):
            report.error("title-en-invalid", tiv, "title_en contains Tamil script")
        elif junk_hit(title_en):
            report.error("title-en-invalid", tiv, "title_en looks like page text")

    # Ragam / thalam must not contain lyrics or header labels.
    for key, limit in (("ragam", MAX_RAGAM_LEN), ("thalam", MAX_THALAM_LEN)):
        value = record.get(key)
        if not isinstance(value, str):
            continue
        if len(value) > limit:
            report.error(
                "ragam-thalam-suspicious",
                tiv,
                "`%s` is %d chars (limit %d): %r" % (key, len(value), limit, value[:40] + "..."),
            )
            continue
        hit = junk_hit(value)
        if hit:
            report.error("ragam-thalam-suspicious", tiv, "`%s` contains %r" % (key, hit))
        if key == "ragam" and any(word in value for word in TALA_WORDS):
            report.error(
                "ragam-thalam-suspicious",
                tiv,
                "`ragam` contains tala vocabulary: %r" % value,
            )

    # Kshetram: the key must exist; null is allowed for non-kshetram songs.
    if "kshetram" in record and isinstance(record["kshetram"], str) and is_blank(record["kshetram"]):
        report.warn("kshetram-empty", tiv, "kshetram is an empty string; use null instead")
    if "kshetram" in record and isinstance(record["kshetram"], str):
        hit = junk_hit(record["kshetram"])
        if hit:
            report.error("kshetram-invalid", tiv, "kshetram contains %r" % hit)

    # Stanzas.
    stanzas = record.get("stanzas")
    if isinstance(stanzas, dict):
        for key in sorted(set(stanzas) - ALLOWED_STANZA_KEYS):
            report.warn("unknown-key", tiv, "unexpected stanzas key `%s`" % key)
        charanams = stanzas.get("charanams")
        if not isinstance(charanams, list) or not charanams:
            report.error("stanzas-shape", tiv, "stanzas.charanams is missing or empty")
        else:
            for index, charanam in enumerate(charanams):
                if not isinstance(charanam, list) or not charanam:
                    report.error(
                        "stanzas-shape", tiv, "stanzas.charanams[%d] is not a non-empty list" % index
                    )
        if "santham" in stanzas and stanzas["santham"] == []:
            report.warn("empty-santham", tiv, "stanzas.santham is []; omit the key instead")

        for where, line in iter_lyrics(record):
            if not isinstance(line, str) or not line.strip():
                report.error("stanzas-shape", tiv, "%s has an empty line" % where)
                continue
            hit = junk_hit(line)
            if hit:
                report.error("lyrics-junk", tiv, "%s contains %r" % (where, hit))

    # YouTube.
    youtube = record.get("youtube")
    if isinstance(youtube, list):
        if not youtube:
            report.warn("youtube-missing", tiv, "no YouTube link recorded")
        for url in youtube:
            if not isinstance(url, str) or not YOUTUBE_URL.match(url):
                report.error("youtube-invalid", tiv, "not a YouTube URL: %r" % (url,))


def main(argv):
    if "--help" in argv or "-h" in argv:
        print(__doc__.strip())
        return 0

    verbose = "--verbose" in argv
    strict = "--strict" in argv

    global DATA_FILE
    if "--file" in argv:
        index = argv.index("--file")
        try:
            DATA_FILE = Path(argv[index + 1]).resolve()
        except IndexError:
            print("--file needs a path", file=sys.stderr)
            return 2

    report = Report()
    records = []

    if not DATA_FILE.exists():
        print("ERROR: %s not found" % DATA_FILE, file=sys.stderr)
        return 1

    text = DATA_FILE.read_text(encoding="utf-8")
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            if line != "":
                report.warn("blank-line", number, "line %d is whitespace only" % number)
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            report.error("jsonl-parse", number, "line %d: %s" % (number, exc))
            continue
        if not isinstance(record, dict):
            report.error("jsonl-parse", number, "line %d is not an object" % number)
            continue
        records.append((number, record))
        check_record(report, record, record.get("tiv", "line %d" % number))
    if text and not text.endswith("\n"):
        report.warn("file-shape", 0, "file does not end with a newline")

    # Uniqueness.
    seen_tiv = defaultdict(list)
    seen_kaumaram = defaultdict(list)
    for _, record in records:
        if isinstance(record.get("tiv"), int):
            seen_tiv[record["tiv"]].append(record)
        if isinstance(record.get("kaumaram"), int):
            seen_kaumaram[record["kaumaram"]].append(record)
    for tiv, dupes in sorted(seen_tiv.items()):
        if len(dupes) > 1:
            report.error("duplicate-tiv", tiv, "%d records share this tiv" % len(dupes))
    for kaumaram, dupes in sorted(seen_kaumaram.items()):
        if len(dupes) > 1:
            report.error(
                "duplicate-kaumaram",
                dupes[0].get("tiv"),
                "%d records share kaumaram index %d" % (len(dupes), kaumaram),
            )

    # Output: grouped by rule unless --verbose.
    grouped = defaultdict(list)
    for severity, rule, tiv, message in report.findings:
        grouped[(severity, rule)].append((tiv, message))

    print("%s - %d records" % (display_path(DATA_FILE), len(records)))
    if report.findings:
        print("%-5s %-24s %3s  %s" % ("LEVEL", "RULE", "N", "AFFECTED TIV"))
    for (severity, rule), items in sorted(grouped.items(), key=lambda kv: (kv[0][0] != "ERROR", kv[0][1])):
        tivs = sorted({str(tiv) for tiv, _ in items}, key=lambda t: (len(t), t))
        shown = ", ".join(tivs[:12]) + (" ..." if len(tivs) > 12 else "")
        print("%-5s %-24s %3d  %s" % (severity, rule, len(tivs), shown))
        if verbose:
            for tiv, message in items:
                print("        tiv %s: %s" % (tiv, message))

    errors = report.count("ERROR")
    warnings = report.count("WARN")
    error_records = len({tiv for severity, _, tiv, _ in report.findings if severity == "ERROR"})
    warning_records = len({tiv for severity, _, tiv, _ in report.findings if severity == "WARN"})
    print()
    print("%d error(s) across %d record(s), %d warning(s) across %d record(s)"
          % (errors, error_records, warnings, warning_records))
    if errors:
        return 1
    if strict and warnings:
        print("--strict: warnings are treated as errors")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
