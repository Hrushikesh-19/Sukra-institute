import json
import re

with open('ocr_raw.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# Manual overrides / corrections
overrides = {
    'cert-17.jpg': {'name': 'D. UPENDRA CHARY', 'slno': '20', 'batch': '19', 'course': 'NAVARATNA COURSE'},
    'cert-55.jpg': {'name': 'DR. V. KRISHNA MOHAN', 'slno': '01', 'batch': '18', 'course': 'NAVARATNA COURSE'},
    'cert-58.jpg': {'name': 'ANIL CHINTHALA', 'slno': '04', 'batch': '18', 'course': 'NAVARATNA COURSE'},
    'cert-60.jpg': {'name': 'VEMULA MAHENDER', 'slno': '02', 'batch': '18', 'course': 'NAVARATNA COURSE'},
    'cert-54.jpg': {'name': 'MANOHAR. CH', 'slno': '07', 'batch': '18', 'course': 'NAVARATNA COURSE'},
    'cert-62.jpg': {'name': 'THEJAASWINI. KOTIKA', 'slno': '16', 'batch': '18', 'course': 'JYOTHISHA VIGNANAM COURSE'},
    'cert-65.jpg': {'name': 'THEJAASWINI. KOTIKA', 'slno': '16', 'batch': '18', 'course': 'NUMEROLOGY COURSE'},
}

def clean_name(n):
    n = re.sub(r'[\d:]', '', n)
    n = n.replace('o ', '').replace('O ', '').replace('4 ', '')
    n = re.sub(r'\s+', ' ', n).strip()
    return n

results = []

for cert_file, lines in raw_data.items():
    full_text = '\n'.join(lines)
    
    # 1. Course determination
    course = 'NAVARATNA COURSE'
    if 'NUMMEROLOGY' in full_text.upper() or 'NUMEROLOGY' in full_text.upper():
        course = 'NUMEROLOGY COURSE'
    elif 'JYOTHISHA VIGNANAM' in full_text.upper() or 'JYOTHISHA' in full_text.upper():
        course = 'JYOTHISHA VIGNANAM COURSE'
    elif 'NAVARATNA' in full_text.upper():
        course = 'NAVARATNA COURSE'
    elif 'GEMOLOGY' in full_text.upper():
        course = 'GEMOLOGY COURSE'
    elif 'DIAMOND' in full_text.upper():
        course = 'DIAMOND GRADING COURSE'
        
    # 2. Batch No
    batch_m = re.search(r'Batch\s*No[:\s]*([A-Za-z0-9\-]+)', full_text, re.I)
    batch = batch_m.group(1).strip() if batch_m else '19'
    
    # 3. Sl.No
    slno_m = re.search(r'S[il1]\.?\s*No[:\s]*([0-9]+)', full_text, re.I)
    slno = slno_m.group(1).strip() if slno_m else ''
    
    # 4. Date
    date_m = re.search(r'(\d{2}/\d{2}/\d{4})', full_text)
    if not date_m:
        date_m = re.search(r'([0-8]0/08/2026)', full_text)
    date = date_m.group(1) if date_m else '06/09/2026'
    if date.startswith('80/'):
        date = '30/08/2026'
    
    # 5. Place
    place = 'PEDAKURAPADU'
    if 'GUNTUR' in full_text.upper():
        place = 'GUNTUR'
        
    # 6. Name extraction
    name = ''
    
    # Find lines between "presented to" and "FOR SUCCESSFUL"
    start_idx = -1
    for idx, l in enumerate(lines):
        if 'PRESENTED' in l.upper():
            start_idx = idx
            break
            
    if start_idx != -1:
        for l in lines[start_idx+1:start_idx+7]:
            c = l.strip()
            if any(k in c.upper() for k in ['BATCH', 'SI.NO', 'SL.NO', 'S1.NO', 'DATE', 'PLACE', 'PRESENTED', 'SUCCESSFUL', 'COMPLETION', 'REQUIREMENTS', 'THEORETICAL', 'PRACTICAL', 'SHRI', 'TRUST', 'GURUKULA', 'VEDHA', 'VIDHYAPEETAM', 'SMARTHHAGAMA', 'ISO', 'MSME']):
                continue
            cleaned = clean_name(c)
            if len(cleaned) >= 3:
                name = cleaned
                break
                
    if not name:
        for idx, l in enumerate(lines):
            if 'SUCCESSFUL' in l.upper():
                for prev in reversed(lines[max(0, idx-4):idx]):
                    c = prev.strip()
                    if any(k in c.upper() for k in ['BATCH', 'SI.NO', 'SL.NO', 'S1.NO', 'DATE', 'PLACE', 'PRESENTED', 'CERTIFICATE']):
                        continue
                    cleaned = clean_name(c)
                    if len(cleaned) >= 3:
                        name = cleaned
                        break
                break

    # Apply manual overrides if present
    if cert_file in overrides:
        if 'name' in overrides[cert_file]: name = overrides[cert_file]['name']
        if 'slno' in overrides[cert_file]: slno = overrides[cert_file]['slno']
        if 'batch' in overrides[cert_file]: batch = overrides[cert_file]['batch']
        if 'course' in overrides[cert_file]: course = overrides[cert_file]['course']

    # Format name nicely
    name = name.strip().upper()
    if name.startswith('G.') and not name.startswith('G. '):
        name = name.replace('G.', 'G. ')
    if name.startswith('P.') and not name.startswith('P. '):
        name = name.replace('P.', 'P. ')
    if name.startswith('M.') and not name.startswith('M. '):
        name = name.replace('M.', 'M. ')
    if name.startswith('N.') and not name.startswith('N. '):
        name = name.replace('N.', 'N. ')
    if name.startswith('D.') and not name.startswith('D. '):
        name = name.replace('D.', 'D. ')
    if name.startswith('S.') and not name.startswith('S. '):
        name = name.replace('S.', 'S. ')
    if name.startswith('R.') and not name.startswith('R. '):
        name = name.replace('R.', 'R. ')
    if name.startswith('DR.') and not name.startswith('DR. '):
        name = name.replace('DR.', 'DR. ')
        
    # Normalize course display name
    if 'NUMMEROLOGY' in course.upper():
        course = 'NUMEROLOGY COURSE'
        
    # Normalize Sl. No format
    if slno and len(slno) == 1:
        slno = '0' + slno

    results.append({
        'file': f'certificates/{cert_file}',
        'name': name,
        'slno': slno,
        'batch': batch,
        'course': course,
        'date': date,
        'place': place
    })

results.sort(key=lambda x: int(re.search(r'\d+', x['file']).group()))

with open('certificates_data.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Successfully generated certificates_data.json with {len(results)} items.")
