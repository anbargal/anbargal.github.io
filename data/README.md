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
| `stanzas` | object | `pallavi`: string[]; `charanams`: string[][] (one array of lines per charanam) |
| `youtube` | string[] | YouTube URLs for performances of the song |

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
    "pallavi": ["தத்தன தனதன தத்தன தனதன", "தத்தன தனதன – தனதான"],
    "charanams": [
      ["கைத்தல நிறைகனி அப்பமொ டவல்பொரி", "கப்பிய கரிமுகன் – அடிபேணிக்"]
    ]
  },
  "youtube": ["https://www.youtube.com/watch?v=R5QQO1CWBas"]
}
```

## Conventions

- Lyrics are verbatim from `dist/<kaumaram>/lyrics.txt`, split into lines by blank-line-separated stanzas.
- `stanzas.pallavi` is always the opening (solfa/“tattana” line); every following stanza is a charanam.
- The final charanam ends with “… பெருமாளே.”
- Ragam/thalam follow the TIV attribution (e.g. thiruppugazh-nectar, Project Madurai).
