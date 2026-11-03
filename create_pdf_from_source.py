#!/usr/bin/env python3
"""
Create PDF with proper Turkish characters from the DEĞERLENDİRME SORULARI
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Questions with correct Turkish characters (from the source PDF)
questions = [
    {
        'number': 1,
        'text': 'İnsanların sağlıkla ilgili tutumları hakkında genel olarak hangisi doğrudur?',
        'options': [
            'Sağlıklarını aşırı önemserler.',
            'Sağlıklı yaşamak için aşırı çaba harcarlar.',
            'Sağlığı bozan birçok alışkanlığı isteyerek edinirler.',
            'Sağlığı bozan şeylerden kaçınırlar.',
            'Organik ürünleri tercih ederler.'
        ]
    },
    {
        'number': 2,
        'text': 'Dünya Sağlık Örgütünün sağlık tanımında hangi kavram yer almamaktadır?',
        'options': [
            'Sakatlık',
            'Hastalık',
            'Beden',
            'Psikoloji',
            'Sosyal yön'
        ]
    },
    {
        'number': 3,
        'text': 'İnsanların kendilerinin kazandığı sağlık bileşeni hangisidir?',
        'options': [
            'Alışkanlıklar',
            'Genetik',
            'Çevre',
            'Sağlık hizmetleri',
            'Doğuştan gelen sakatlıklar'
        ]
    },
    {
        'number': 4,
        'text': 'Hangi hastalık tamamıyla genetik yapıyla açıklanır?',
        'options': [
            'Kanser',
            'Şeker',
            'Tifo',
            'Tüberküloz',
            'Hemofili'
        ]
    },
    {
        'number': 5,
        'text': 'Sağlık sistemiyle ilgili aşağıdakilerden hangisi yanlıştır?',
        'options': [
            'Sosyal bir sistemdir.',
            'Birçok sistemle etkileşim halindedir.',
            'Alt sistemlerden oluşur.',
            'Kapalı sistemdir.',
            'Negatif entropiye maruz kalır.'
        ]
    },
    {
        'number': 6,
        'text': 'Bir sistemin dağılmasına ne ad verilir?',
        'options': [
            'Sinerji',
            'Entropi',
            'Negatif entropi',
            'Çevre',
            'Çözülme'
        ]
    },
    {
        'number': 7,
        'text': 'Hangisi tasarım alt sisteminin bir parçası değildir?',
        'options': [
            'Sağlık, Aile, Çalışma ve Sosyal İşler Komisyonu',
            'Anayasa Mahkemesi',
            'Hükümet',
            'Sağlık Okulları',
            'Sağlık Bakanlığı'
        ]
    },
    {
        'number': 8,
        'text': 'Aşağıdakilerden hangisi sağlık sisteminin finansmanında, genel bir kamu sağlık sigorta sistemi oluşturmayı öngörür?',
        'options': [
            'İngiliz',
            'Amerikan',
            'Alman',
            'Rus',
            'Türk'
        ]
    },
    {
        'number': 9,
        'text': 'Türkiye sağlık sisteminin finansmanında hangisi rol oynamaz?',
        'options': [
            'Mevduatlar',
            'Vergiler',
            'Primler',
            'Cepten ödemeler',
            'Katılım payları'
        ]
    },
    {
        'number': 10,
        'text': 'Tedavi edici sağlık hizmeti hangi aşamada devreye girer?',
        'options': [
            'Erken tanı',
            'Belirtiler',
            'Tanılama',
            'Tedavi',
            'Tıbbi rehabilitasyon'
        ]
    },
]

answers = {
    1: 'C', 2: 'D', 3: 'A', 4: 'E', 5: 'D',
    6: 'B', 7: 'D', 8: 'C', 9: 'A', 10: 'B'
}

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
output_path = "degerlendirme_sorulari.pdf"
c = canvas.Canvas(output_path, pagesize=A4)
width, height = A4

margin = 2 * cm
font_size = 12
leading = font_size * 1.5
y = height - margin

c.setFont(FONT_NAME, font_size)

# Header
c.drawString(margin, y, "SAĞLIK SİSTEMİ VE SAĞLIK HİZMETLERİNİN ÖRGÜTLENMESİ")
y -= leading
c.drawString(margin, y, "DEĞERLENDİRME SORULARI")
y -= leading * 2

for q in questions:
    if y < margin + leading * 3:
        c.showPage()
        c.setFont(FONT_NAME, font_size)
        y = height - margin
    
    # Question number and text
    q_text = f"{q['number']}. {q['text']}"
    c.drawString(margin, y, q_text)
    y -= leading
    
    # Options
    for i, opt in enumerate(q['options']):
        if y < margin + leading:
            c.showPage()
            c.setFont(FONT_NAME, font_size)
            y = height - margin
        opt_letter = chr(ord('A') + i)
        c.drawString(margin + 1*cm, y, f"{opt_letter}) {opt}")
        y -= leading
    
    y -= leading * 0.5  # Extra space between questions

# Add answer key on new page
c.showPage()
c.setFont(FONT_NAME, font_size)
y = height - margin
c.drawString(margin, y, "CEVAP ANAHTARI")
y -= leading * 2

for q in questions:
    if y < margin + leading:
        c.showPage()
        c.setFont(FONT_NAME, font_size)
        y = height - margin
    q_num = q['number']
    ans_letter = answers.get(q_num, '?')
    c.drawString(margin, y, f"{q_num}. {ans_letter}")
    y -= leading

c.save()
print(f"PDF created: {output_path}")