import json, re, os, sys, time, urllib.request, shutil

DB_PATH = "/Users/aa/src/anbargal.github.io/data/thiruppugazh.jsonl"
DIST_BASE = "/Users/aa/src/anbargal.github.io/dist"

def fetch(url):
    for _ in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            return urllib.request.urlopen(req, timeout=15).read().decode('utf-8', errors='replace')
        except: time.sleep(1)
    return ""

def extract_kaumaram_lyrics(km):
    html = fetch(f"https://www.kaumaram.com/thiru/nnt{km:04d}_u.html")
    
    m = re.search(r'<td[^>]*class="[^"]*ttxt[^"]*"[^>]*>(.*?)</td>', html, re.DOTALL)
    if not m:
        return [], []
    
    content = m.group(1)
    content = re.sub(r'<[^>]+>', '\n', content)
    content = content.replace('&nbsp;', ' ')
    content = content.replace('&amp;', '&')
    
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    tamil_lines = [l for l in lines if re.search(r'[\u0B80-\u0BFF]', l)]
    
    # Find the பாடல் marker
    padal_idx = -1
    for i, l in enumerate(tamil_lines):
        if 'பாடல்' in l:
            padal_idx = i
            break
    
    # Find the சொல் விளக்கம் marker (end of lyrics)
    end_idx = len(tamil_lines)
    for i, l in enumerate(tamil_lines):
        if 'சொல் விளக்கம்' in l or 'Meaning' in l:
            end_idx = i
            break
    
    santham = []
    charanams = []
    
    if padal_idx >= 0:
        santham = [l for l in tamil_lines[:padal_idx] if re.search(r'[\u0B80-\u0BFF]', l)]
        lyrics_text = tamil_lines[padal_idx+1:end_idx]
    else:
        lyrics_text = tamil_lines[:end_idx]
    
    # Group charanams: each ends with ...... or பெருமாளே.
    current = []
    for line in lyrics_text:
        stripped = line.strip()
        if not stripped:
            if current:
                charanams.append(list(current))
                current = []
        else:
            current.append(stripped)
            if '......' in stripped or stripped.endswith('பெருமாளே.'):
                charanams.append(list(current))
                current = []
    
    return santham, charanams

def extract_blog_ragam_thalam(url):
    html = fetch(url)
    # Join all lines to handle the case where HTML has no line breaks
    text = ' '.join(html.split())
    
    ragam = ""
    thalam = ""
    
    # Try to find pattern: ராகம்: <text> தாளம்: <text>
    m = re.search(r'ராகம்[:\s]*([^\s<][^<]*?)(?=தாளம்|$)', text)
    if m:
        ragam = m.group(1).strip().rstrip(',').rstrip(':').strip()
    
    m = re.search(r'தாளம்[:\s]*([^<]*?)(?=ராகம்|Learn|$)', text)
    if m:
        thalam = m.group(1).strip().rstrip(',').rstrip(':').strip()
    
    # Clean up
    ragam = re.sub(r'\s+', ' ', ragam).strip()
    thalam = re.sub(r'\s+', ' ', thalam).strip()
    
    return ragam, thalam

SONGS = [
    (94, 203, "ஆனாத பிருதிவி", "Anadha Piruthivi", "சுவாமிமலை", "http://thiruppugazh-nectar.blogspot.com/2015/01/aanaathapiruthvi.html", "EOKDIsYuUSY"),
    (95, 205, "இருவினை புனைந்து", "Iruvinai Punaindhu", "சுவாமிமலை", "http://thiruppugazh-nectar.blogspot.com/2015/02/iruvinai-punaindhu.html", "wilvdzfwNso"),
    (96, 206, "எந்தத் திகையினும்", "Endhath Thigaiyinum", "சுவாமிமலை", "http://thiruppugazh-nectar.blogspot.com/2015/02/endhathigaiyinum.html", "ZRroPlS0Kv0"),
    (97, 207, "ஒருவரையும் ஒருவர்", "Oruvaraiyum Oruvar", "சுவாமிமலை", "http://thiruppugazh-nectar.blogspot.com/2015/02/oruvaraiyumoruvar.html", "lp5lmb9v-bQ"),
    (98, 208, "கடாவினிடை", "Kadaavinidai", "சுவாமிமலை", "http://thiruppugazh-nectar.blogspot.com/2015/02/kadavinidai.html", "xd67KanwGf8"),
    (99, 209, "கடிமா மலர்க்குள்", "Kadima Malarkkul", "சுவாமிமலை", "http://thiruppugazh-nectar.blogspot.com/2015/02/kadimamalar.html", "KIJ0Xlrbdbc"),
    (100, 210, "கதிரவனெ ழுந்து", "Kathiravane Zhundhu", "சுவாமிமலை", "http://thiruppugazh-nectar.blogspot.com/2015/02/100-kadiravan.html", "SOdKgvEB-ss"),
    (101, 211, "கறை படும் உடம்பு", "Karai Padum Udambu", "சுவாமிமலை", "https://thiruppugazh-nectar.blogspot.com/2015/03/101.karaipadum.html", "zHcuryJ8PIM"),
    (102, 212, "காமியத் தழுந்தி", "Kamiyath Thazhundhi", "சுவாமிமலை", "http://thiruppugazh-nectar.blogspot.com/2015/03/102-kaamiyaththu.html", "BnZi2823NT8"),
    (103, 213, "குமரகுருபர முருக குகனே", "Kumaragurubara Muruga Gugnane", "சுவாமிமலை", "http://thiruppugazh-nectar.blogspot.com/2015/03/103-kumaragurupara.html", "qXDliT8wbAE"),
    (104, 216, "சரண கமலாலயத்தை", "Sarana Kamalalayaththai", "சுவாமிமலை", "http://thiruppugazh-nectar.blogspot.com/2015/03/charanakamalalayaththai.html", "Hd6UTuLxN10"),
    (105, 217, "சுத்திய நரப்புடன்", "Suththiya Narappudan", "சுவாமிமலை", "http://thiruppugazh-nectar.blogspot.com/2015/03/suththiyanarappudan.html", "QRueW88bJLY"),
    (106, 218, "செகமாயை உற்று", "Segamayai Utru", "சுவாமிமலை", "http://thiruppugazh-nectar.blogspot.com/2015/03/Jegamayai.html", "JPisLo0bC1U"),
    (107, 221, "தெருவினில் நடவா", "Theruvinil Nadava", "சுவாமிமலை", "http://thiruppugazh-nectar.blogspot.com/2015/03/theruvinil.html", "KD5JTfJAyfc"),
    (108, 222, "நாசர்தங் கடை", "Nasarthang Kadai", "சுவாமிமலை", "http://thiruppugazh-nectar.blogspot.com/2015/03/naasartham.html", "Bx_qdYv4kPo"),
    (109, 223, "நாவேறு பா மணத்த", "Naveru Pa Manaththa", "சுவாமிமலை", "http://thiruppugazh-nectar.blogspot.com/2015/03/naaverupaamanaththa.html", "RWj24s0qoTs"),
    (110, 225, "நிறைமதி முகமெனும்", "Niraimathi Mugamenum", "சுவாமிமலை", "http://thiruppugazh-nectar.blogspot.com/2015/03/niraimathi.html", "W_H-M5mG708"),
    (111, 228, "பாதி மதிநதி", "Paadhi Mathinadhi", "சுவாமிமலை", "http://thiruppugazh-nectar.blogspot.com/2015/03/111.html", "SrXDKelZPXo"),
    (112, 229, "மகர கேதனத்தன்", "Makarakedhanaththan", "சுவாமிமலை", "http://thiruppugazh-nectar.blogspot.com/2015/03/magaraketanaththan.html", "Q3-yVqhZf-4"),
    (114, 239, "அமைவுற்று அடைய", "Amaivutru Adaiya", "திருத்தணிகை", "http://thiruppugazh-nectar.blogspot.com/2015/03/amaivutradaiya.html", "bzfPltsoDo0"),
    (115, 240, "அரகர சிவன் அரி", "Arahara Sivan Ari", "திருத்தணிகை", "http://thiruppugazh-nectar.blogspot.com/2015/03/araharasiva.html", "MdHVSL6M9dY"),
]

def process():
    for song in SONGS:
        tiv, km, title, title_en, kshetram, blog_url, yt_id = song
        
        print(f"\n=== TIV {tiv} (km {km}) ===", flush=True)
        
        santham, charanams = extract_kaumaram_lyrics(km)
        print(f"  Santham: {len(santham)}")
        print(f"  Charanams: {len(charanams)}")
        
        if not charanams:
            print(f"  ERROR: No charanams!")
            continue
        
        ragam, thalam = extract_blog_ragam_thalam(blog_url)
        print(f"  Ragam: '{ragam}' Thalam: '{thalam}'")
        
        yt_url = f"https://www.youtube.com/watch?v={yt_id}" if yt_id else ""
        
        stanzas = {}
        if santham:
            stanzas["santham"] = santham
        stanzas["charanams"] = charanams
        
        record = {
            "kaumaram": km, "tiv": tiv,
            "title": title, "title_en": title_en,
            "ragam": ragam or None,
            "thalam": thalam or None,
            "kshetram": kshetram,
            "stanzas": stanzas,
            "youtube": [yt_url] if yt_url else []
        }
        
        with open(DB_PATH, 'a') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
        
        print(f"  ✓ {title_en}")
        
        km_dir = f"{DIST_BASE}/{km}"
        os.makedirs(km_dir, exist_ok=True)
        with open(f"{km_dir}/lyrics.txt", 'w') as f:
            for l in santham:
                f.write(l + '\n')
            f.write('\n')
            for ch in charanams:
                for l in ch:
                    f.write(l + '\n')
                f.write('\n')
        shutil.rmtree(km_dir, ignore_errors=True)

if __name__ == '__main__':
    process()