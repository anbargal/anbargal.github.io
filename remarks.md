# Remarks

## Pending

- [ ] Check from 340

### TIV 347 — Vizhaiyum Manidharai

- [ ] Check TIV 347 — blogspot lists this song as "எழுதரிய" (5 charanams, no santham) but kaumaram 1278 is "விழையும் மனிதரை" (santham + 8 charanams). Recorded the full kaumaram 1278 text under title "விழையும் மனிதரை"; confirm whether the "எழுதரிய" subset should be stored instead.

### TIV 204 — IravAmal

- [ ] Kaumaram index 943 — is the title "iravAmal" or "iravAmar"? Check lyrics with book.

### TIV 160 — Bumi Adhanil

- [ ] Spelling and lyrics need verification.
- [ ] Check whether the word is "boomi" (பூமி) or "puvi" (புவி) - currently shows "புமி" in database.
- [ ] Verify accuracy of all charanams.

### TIV 166-190 Batch

- [ ] Check song 172.

### TIV 226-235 Batch

- [ ] Ragam spellings for TIV 227 (பிருந்தாவன சாரங்கா) and TIV 230 (சிந்து பைரவி) were aligned to the DB's existing conventions (blogspot renders them ஸாரங்கா / சிந்துபைரவி). Confirm these are as intended.
- [ ] Verify lyrics accuracy in all charanams for the batch.

### TIV 239 — Uiriyadhava Neri

- [ ] Lyrics need verification — the thiruppugazh-nectar blogspot page (239.uriyathava.html) appears to contain lines from two different songs:
  - "உரியதவ நெறியில்..." (main, ends பெருமாளே)
  - "இரவினிடை துயிலுகினும்... யருள்வாயே"
  - The TIV 239 page pairs "உரிய தவநெறி" with the "அருள்வாயே" refrain — verify which lyrics actually belong to this song.

### TIV 216-225 Batch

- [ ] **TIV 218** — ragam "சநதிரகெளன்ஸ்" is how thiruppugazh-nectar renders it — looks like a typo (likely சந்திரகௌளை). Verify/correct.
- [ ] **TIV 223** — kshetram set to "கோடி" (kaumaram lists "கோடி..குழகர் கோயில்").
- [ ] Verify lyrics accuracy in all charanams for the batch.

### TIV 200

- [ ] **TIV 200 (தூதாளரோடு)** — skipped during onboarding of TIV 191-215.
  - Not present in the kaumaram.com numbered database; kaumaram index could not be derived by title matching.
  - விராலிமலை (VirAlimalai) song about Yama (காலன்) and his messengers being frightened.
  - Ragam: சஹானா, Thalam: 7½ (2½ + 1½ + 1½ + 2).
  - Lyrics available on the blogspot page: http://thiruppugazh-nectar.blogspot.com/2015/12/200.thoothalaodu.html
  - Needs kaumaram index confirmed from an alternate source before onboarding.

---

## Resolved

### TIV 47 — Munaichang Kolidu

- [x] Was silently skipped during the manual TIV 45-50 onboarding (Aug 2026): the commits went 45+46 → 48 → 49+50, and no validator rule checks for gaps in the TIV sequence.
- [x] Onboarded 2026-11-28 from the thiruppugazh-nectar page for TIV 47 (`2013/02/munaichchangolidu.html`), cross-checked line by line against kaumaram.
- [x] Kaumaram index resolved: **29** (`nnt0029_u.html`). Note kaumaram files this song under a different opening line ("அனிச்சம் கார்முகம்") and prepends two charanams (அனிச்சங் கார்முகம் … நெறிபாரா) that the nectar page marks `(நீக்குக)` — those are **not** part of TIV 47 and are not stored.
- [x] Charanam order follows the TIV source (முனைச்சங், முளைக்குஞ், தினைச்செங், சிறக்குந், வினைச்சண், விகற்பங்). Kaumaram orders them as வினைச்சண், விகற்பங், முனைச்சங் … சிறக்குந் (which ends on பெருமாளே); the nectar page underlines the last two, suggesting an editorial addition. Worth a book check.
- [x] Ragam காபி / thalam `1½ + 6` from the nectar header; kshetram திருச்செந்தூர் (kaumaram 29 is a thiruchchendhUr song).
- [x] YouTube: "Amudha Thirupugaz padalgal 047" — https://www.youtube.com/watch?v=9HFRuq9cY20

### TIV 110 — Niraimathi Mugamenum

- [x] No dedicated performance video exists on the Kalakad Thiruppugazh N.S. Mani channel.
- [x] The YouTube link points to a multi-song compilation that includes TIV 110:
  https://youtu.be/h-9wywkiCZ8?t=1531 (timestamped to the song).
- Fix applied 2026-08-24 after batch onboarding of TIV 91-115.

### TIV 113 — Oru Uruvagiya

- [x] YouTube link was missing after batch onboarding of TIV 91-115.
- [x] Added link to dedicated performance video: https://www.youtube.com/watch?v=CCqdWeTVNNA
- Fix applied 2026-08-24.
- [x] Record was accidentally deleted in `c4bff10` ("Onboard TIV 432-441") and restored from git on 2026-11-28.
- [x] Kaumaram index resolved: **1326** (`nnt1326_u.html`, "ஓருரு வாகி — திருவெழுகூற்றிருக்கை"). All 28 stored lines match the kaumaram text verbatim (9 charanams, no santham); the trailing period on the last line was added to match the source.
- [x] Ragam (தர்பாரி கானடா) and Thalam (ஆதி - எடுப்பு 3/4 இடம்) confirmed against the thiruppugazh-nectar page (`2015/03/oruruvaagiya.html`).
- [x] Kshetram சுவாமிமலை confirmed — kaumaram files the song under ஏரகம் / திருவெழுகூற்றிருக்கை, i.e. Swamimalai.
- [x] YouTube video confirmed: "Amudha Thirupugaz padalgal 113" on the Kalakad Thiruppugazh N.S. Mani channel.

### TIV 117 — IrumalurOga

- [x] YouTube link previously pointed to a 1-50 compilation video.
- [x] Corrected to dedicated performance video: https://www.youtube.com/watch?v=u5bRhO5hu1k
- Fix applied 2026-08-24.

### TIV 131 — Sinaththavar

- [x] YouTube link previously pointed to a TIV 001 (Kaithala) video.
- [x] Corrected to dedicated performance video: https://www.youtube.com/watch?v=jw9M0g6zq-c
- Fix applied 2026-08-24.

### TIV 132 — Sinaththilaththinai

- [x] YouTube link previously pointed to a wrong video.
- [x] Corrected to dedicated performance video: https://www.youtube.com/watch?v=S3oRWmknZn8
- Fix applied 2026-08-24.

### TIV 140 — Porpathaththinai

- [x] YouTube link previously pointed to a wrong video.
- [x] Corrected to dedicated performance video: https://www.youtube.com/watch?v=IgNx8qebMRM
- Fix applied 2026-08-24.

### TIV 141 — MuththuththeRikka

- [x] YouTube link was pointing to wrong video: https://www.youtube.com/watch?v=t6Qo3iYPQc8
- [x] Corrected to dedicated performance video: https://www.youtube.com/watch?v=ctOaoOI7crc
- Fix applied 2026-08-25.

### TIV 161 — Adhirum Kazhal

- [x] YouTube link was pointing to wrong video: https://www.youtube.com/watch?v=2oUO_OYwMck
- [x] Corrected to dedicated performance video: https://www.youtube.com/watch?v=N6E3lIUxuP8
- Fix applied 2026-08-25.

### TIV 162 — Ezhudhigazh Buvana

- [x] YouTube link was pointing to wrong video: https://www.youtube.com/watch?v=gC1raFc-hho
- [x] Corrected to dedicated performance video: https://www.youtube.com/watch?v=JaV3RwtN7Ec
- Fix applied 2026-08-25.

### TIV 163 — ThaRaiyin Manudar

- [x] YouTube link was pointing to wrong video: https://www.youtube.com/watch?v=iCD6mYE4gt0
- [x] Corrected to dedicated performance video: https://www.youtube.com/watch?v=lXjwD-5thGk
- Fix applied 2026-08-25.

### TIV 164 — Vanjaga Loba Muda

- [x] YouTube link was pointing to wrong video: https://www.youtube.com/watch?v=apz_NjgNGUY
- [x] Corrected to dedicated performance video: https://www.youtube.com/watch?v=BXF8poEZT_w
- Fix applied 2026-08-25.

### TIV 165 — Aingkaranai

- [x] No YouTube link available in database.
- [x] Added link to dedicated performance video: https://www.youtube.com/watch?v=8F5k5qt-Mcg
- Fix applied 2026-08-25.

### TIV 62 — Orupozhuthum

- [x] `thalam` was `"தாளம் : 1+1½+1+1½+1½+3"` — the `தாளம் :` label was included in the value. Fixed in the 2026-11-20 data rebuild.

### TIV 432–441 — Commentary prose in lyrics

- [x] These 10 songs had Tamil commentary (சொல் விளக்கம்) in `stanzas.charanams` instead of the actual lyrics. Ragam/thalam were also partly wrong (copied from unrelated songs), and `kshetram` was `null`.
- [x] Rebuilt from kaumaram.com lyrics + thiruppugazh-nectar header rows. Correct ragam/thalam/kshetram now stored.
- [x] English titles (`title_en`) were already present from the earlier batch onboarding; verified they match the transliterated Tamil title.

### TIV 442–451 — One-off scrape artifacts, missing fields

- [x] These 10 songs were onboarded with a one-off schema: `"charanam"` (singular, whole-page blog text as a single string) and `"youtubeId"` instead of `"stanzas"` and `"youtube"`. `title_en`, `kshetram`, and the proper `stanzas` structure were all missing.
- [x] Rebuilt: `stanzas.charanams` = 1 line array per charanam (2–8 lines each), `title_en` set, `kshetram` set from kaumaram, `youtube` → `[]` for later backfill.
- [x] TIV 443 title corrected from `குருத்தி புழல்` to `குருதி புலால்`.
- [x] English titles (`title_en`) for 452–461 were added in the same pass.

### TIV 432–461 — YouTube links

- [x] These 30 songs had no YouTube links (or, for 452–461, were in the `[]` state). Mapped from channel upload enumeration (611 videos from `@KalakadThiruppugazhNSMani`) by matching `Amudha Thirupugaz padalgal nnn` titles.
- [x] Each link confirmed via oEmbed API (channel + title) before storing.
- [x] TIV 494: corrected from the "Padalgal 1 to 50" compilation (`nhMmIlz6Suc`) to its dedicated performance video (`HHd_1ZOZVps`).

### TIV 402–431 — Normalised santham omission

- [x] These 30 songs had `"santham": []` in `stanzas`. Removed the key entirely (the schema treats `santham` as optional; `[]` is not a valid empty-state).
