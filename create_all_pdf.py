#!/usr/bin/env python3
"""
Extract ALL questions from all 14 DEĞERLENDİRME SORULARI sections and create comprehensive PDF
"""
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Read extracted text
with open('extracted_text.txt', 'r', encoding='utf-8') as f:
    full_text = f.read()

# Find all DEĞERLENDİRME SORULARI sections
section_starts = [m.start() for m in re.finditer('DEĞERLENDİRME SORULARI', full_text)]

# Unit names for each section
unit_names = [
    "SAĞLIK SİSTEMİ VE SAĞLIK HİZMETLERİNİN ÖRGÜTLENMESİ",
    "SAĞLIK KURUMLARININ TÜRLERİ VE ÖZELLİKLERİ",
    "SAĞLIK KURUMLARINDA YÖNETİM FONKSİYONLARI",
    "SAĞLIK KURUMLARI YÖNETİMİ EĞİTİMİ",
    "SAĞLIK KURUMLARI YÖNETİCİLERİNİN ROL VE BECERİLERİ",
    "SAĞLIK KURUMLARINDA POLİKLİNİK VE KLİNİK HİZMETLERİ",
    "SAĞLIK KURUMLARINDA GÖRÜNTÜLEME VE LABORATUVAR HİZMETLERİ",
    "SAĞLIK KURUMLARINDA ACİL VE YOĞUN BAKIM HİZMETLERİ",
    "SAĞLIK KURUMLARINDA İLAÇ VE TIBBİ MALZEME HİZMETLERİ",
    "SAĞLIK KURUMLARINDA GENEL DESTEK HİZMETLERİ",
    "SAĞLIK KURUMLARINDA TEKNİK VE TIBBİ CİHAZ HİZMETLERİ",
    "SAĞLIK KURUMLARINDA HASTA BAKIM HİZMETLERİ",
    "SAĞLIK KURUMLARINDA EVDE BAKIM HİZMETLERİ",
    "SAĞLIK KURUMLARINDA KARAR DESTEK SİSTEMLERİ",
]

all_questions = []  # List of (unit_idx, unit_name, question_dict)

for idx, start in enumerate(section_starts):
    unit_name = unit_names[idx] if idx < len(unit_names) else f"ÜNİTE {idx+1}"
    
    # Find end of this section (next DEĞERLENDİRME or major break)
    if idx + 1 < len(section_starts):
        end = section_starts[idx + 1]
    else:
        end = start + 10000
    
    section_text = full_text[start:end]
    
    # Find answer key for this section
    answer_match = re.search(r'Cevap Anahtarı\s*(.+?)(?:\n\s*\d+\.|YARARLANILAN|ÜNİTE|Atatürk|Sağlık\s+[A-Z]|$)', section_text, re.DOTALL)
    answers = {}
    if answer_match:
        answer_text = answer_match.group(1).strip()
        for ans in re.finditer(r'(\d+)\.([a-e])', answer_text, re.IGNORECASE):
            answers[int(ans.group(1))] = ans.group(2).upper()
    
    # Parse questions - split by question number
    # Remove the "DEĞERLENDİRME SORULARI" header
    section_text = re.sub(r'^DEĞERLENDİRME SORULARI\s*', '', section_text)
    
    # Split by question pattern
    q_parts = re.split(r'\n(\d+)\.\s', section_text)
    
    # q_parts[0] is empty or intro, then pairs of (num, content)
    for i in range(1, len(q_parts), 2):
        if i + 1 >= len(q_parts):
            break
        q_num = int(q_parts[i])
        q_content = q_parts[i + 1].strip()
        
        # Stop if we hit answer key or next section
        if 'Cevap Anahtarı' in q_content or 'YARARLANILAN' in q_content:
            break
        
        lines = [l.strip() for l in q_content.split('\n') if l.strip()]
        if not lines:
            continue
        
        question_text = lines[0]
        options = []
        for line in lines[1:]:
            opt_match = re.match(r'([a-e])\)\s*(.+)', line, re.IGNORECASE)
            if opt_match:
                options.append(opt_match.group(2).strip())
        
        if options:
            all_questions.append({
                'unit_idx': idx,
                'unit_name': unit_name,
                'number': q_num,
                'text': question_text,
                'options': options,
                'answer': answers.get(q_num, '?')
            })

# Group by unit
from collections import defaultdict
by_unit = defaultdict(list)
for q in all_questions:
    by_unit[q['unit_idx']].append(q)

print(f"Total questions: {len(all_questions)}")
for idx in sorted(by_unit.keys()):
    print(f"  {unit_names[idx]}: {len(by_unit[idx])} questions")

# Find Arial font
font_path = None
for path in [
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/ARIAL.TTF",
]:
    if os.path.exists(path):
        font_path = path
        break

if font_path:
    pdfmetrics.registerFont(TTFont("ArialUnicode", font_path))
    FONT_NAME = "ArialUnicode"
else:
    FONT_NAME = "Helvetica"
    print("Warning: Arial not found, using Helvetica")

# Create output PDF
output_path = "tum_degerlendirme_sorulari.pdf"
c = canvas.Canvas(output_path, pagesize=A4)
width, height = A4

margin = 2 * cm
font_size = 11
leading = font_size * 1.4
y = height - margin

c.setFont(FONT_NAME, font_size)

# Title page
c.setFont(FONT_NAME, 18)
c.drawString(margin, height - 5*cm, "ATATÜRK ÜNİVERSİTESİ AÇIKÖĞRETİM FAKÜLTESİ")
c.drawString(margin, height - 6*cm, "SAĞLIK KURUMLARI YÖNETİMİ I")
c.setFont(FONT_NAME, 14)
c.drawString(margin, height - 7.5*cm, "TÜM DEĞERLENDİRME SORULARI")
c.drawString(margin, height - 8.5*cm, f"Toplam {len(all_questions)} Soru - 14 ÜNİTE")
c.showPage()

# Reset font
c.setFont(FONT_NAME, font_size)

for idx in sorted(by_unit.keys()):
    unit_name = unit_names[idx]
    questions = by_unit[idx]
    
    # Unit header
    if y < height - 3*cm:
        c.showPage()
        y = height - margin
    
    c.setFont(FONT_NAME, 13)
    c.drawString(margin, y, unit_name)
    y -= leading * 1.5
    c.setFont(FONT_NAME, font_size)
    
    for q in questions:
        if y < margin + leading * 3:
            c.showPage()
            y = height - margin
        
        # Question number and text
        q_text = f"{q['number']}. {q['text']}"
        c.drawString(margin, y, q_text)
        y -= leading
        
        # Options
        for i, opt in enumerate(q['options']):
            if y < margin + leading:
                c.showPage()
                y = height - margin
            opt_letter = chr(ord('A') + i)
            c.drawString(margin + 1*cm, y, f"{opt_letter}) {opt}")
            y -= leading
        
        y -= leading * 0.4  # Space between questions

# Answer key section
c.showPage()
y = height - margin
c.setFont(FONT_NAME, 14)
c.drawString(margin, y, "CEVAP ANAHTARI")
y -= leading * 2
c.setFont(FONT_NAME, font_size)

for idx in sorted(by_unit.keys()):
    unit_name = unit_names[idx]
    questions = by_unit[idx]
    
    if y < margin + leading * 3:
        c.showPage()
        y = height - margin
    
    c.setFont(FONT_NAME, 12)
    c.drawString(margin, y, unit_name)
    y -= leading * 1.5
    c.setFont(FONT_NAME, font_size)
    
    for q in questions:
        if y < margin + leading:
            c.showPage()
            y = height - margin
        ans = q['answer']
        c.drawString(margin, y, f"{q['number']}. {ans}")
        y -= leading

c.save()
print(f"\nPDF created: {output_path}")