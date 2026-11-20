# Thiruppugazh database

`thiruppugazh.jsonl` is the song database for this site. One JSON object per line, one line per song. Load it in the browser with `fetch()` and split on newlines / `JSON.parse` each line.

## Record schema

| Field | Type | Description |
| --- | --- | --- |
| `kaumaram` | int | Index number on kaumaram.com |
| `tiv` | int | Song number in the TIV (Thiruppugazh Isai Vazhipadu) numbering |
| `title` | string | Song title in Tamil (first line of the lyrics) |
| `title_en` | string | Romanised title |
| `ragam` | string \| null | Ragam, in Tamil |
| `thalam` | string \| null | Thalam, in Tamil |
| `kshetram` | string \| null | Murugan kshetram, in Tamil; `null` for non-kshetram songs (e.g. the Vinayagar invocation) |
| `stanzas` | object | `santham`: string[] (optional); `charanams`: string[][] (one array of lines per charanam) |
| `youtube` | string[] | YouTube URLs for performances of the song; `[]` when none is known |

Schema rules enforced by the validator (`data/validate.py`):

- `title_en` is required and non-empty — the catalog renders it after every title, so `null` shows up as “ — None”. It is Title Case with no diacritics (`Ola Maraigal`, not `Ola maraigaL`).
- `stanzas.charanams` must be a non-empty list of non-empty line arrays.
- `stanzas.santham` is optional. **Omit the key entirely** when the song has no opening solfa line; do not store `[]`.
- Never store `charanam` (singular) or `youtubeId`; those were one-off scrape artifacts, not schema.
- Lyrics must be the song only. The kaumaram page also carries Tamil commentary under `......... சொல் விளக்கம் .........` — that section is not lyrics.

## Example

```json
{
  "kaumaram": 1,
  "tiv": 1,
  "title": "கைத்தல நிறைகனி",
  "title_en": "Kaithala Niraikani",
  "ragam": "நாட்டை",
  "thalam": "ஆதி",
  "kshetram": null,
  "stanzas": {
    "santham": ["தத்தன தனதன தத்தன தனதன", "தத்தன தனதன – தனதான"],
    "charanams": [
      ["கைத்தல நிறைகனி அப்பமொ டவல்பொரி", "கப்பிய கரிமுகன் – அடிபேணிக்"]
    ]
  },
  "youtube": ["https://www.youtube.com/watch?v=QwZ4HGgcFz8"]
}
```

## Conventions

- **Lyrics** are verbatim from the kaumaram.com song page (`https://www.kaumaram.com/thiru/nntNNNN_u.html`) in the `<table class="tbl04b">` cell. Split on `<br>`; the song starts after the `......... பாடல் .........` marker and ends at `......... சொல் விளக்கம் .........`. Everything after that marker is commentary and must not be stored.
- **Ragam/thalam** come from the first `<tr>` of the post's `<table lang="ta">` on [thiruppugazh-nectar](https://thiruppugazh-nectar.blogspot.com/p/index.html). The Tamil text is HTML-entity encoded, so unescape before parsing. The schema-level description in the page's JSON-LD is truncated — do not parse ragam/thalam from it.
- `stanzas.santham` is the opening (solfa/“tattana”) line; every following stanza is a charanam. Repeated santham lines are verbatim and stay as-is (the source prints the line, then repeats it with the closing `...... தனதான`).
- The final charanam normally ends with `… பெருமாளே.` Some songs legitimately end differently (e.g. TIV 432 ends `… தம்பிரானே.`); match the source rather than forcing the formula.
- **YouTube links** are the `Amudha Thirupugaz padalgal nnn` videos on the [Kalakad Thiruppugazh N.S. Mani](https://www.youtube.com/@KalakadThiruppugazhNSMani) channel, where `nnn` is the TIV number.
  - Prefer enumerating the channel's uploads (`/@KalakadThiruppugazhNSMani/videos` + the `youtubei/v1/browse` continuation API) and matching `^Amudha Thirupugazh? padalgal\s*nnn`. YouTube's search page is unreliable — it returns the same generic results for different queries.
  - Exclude the `Amudha Thiruppugazh Padalgal - 503 Padalgal - 401 to 450` style compilation videos; every song has its own dedicated upload.
  - Confirm each link with the oEmbed API before storing: `https://www.youtube.com/oembed?url=https%3A//www.youtube.com/watch%3Fv%3D<id>&format=json` should return `author_name` = “Kalakad Thiruppugazh N.S. Mani”.

## Validator

`data/validate.py` checks every record against the schema above (stdlib only, no build step):

```bash
python3 data/validate.py            # grouped summary, exit 1 on errors
python3 data/validate.py --verbose  # one line per finding
python3 data/validate.py --strict   # warnings also fail
python3 data/validate.py --file other.jsonl
```

It reports `forbidden-legacy-key`, `missing-key`, `field-type`, `title-en-missing`, `title-en-invalid`, `lyrics-junk`, `ragam-thalam-suspicious`, `stanzas-shape`, `youtube-invalid`, `duplicate-tiv`, `duplicate-kaumaram`, plus warnings such as `youtube-missing`, `empty-santham`, and `unknown-key`. A healthy database is **0 errors, 0 warnings**.
