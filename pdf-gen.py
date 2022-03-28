from reportlab.pdfgen import canvas
import sqlite3

conn = sqlite3.connect('mylyrics.db')
cur = conn.cursor()

cur.execute('''SELECT lyric FROM Lyrics''')
lyrics = cur.fetchone()
for letra in lyrics:
    print(letra)


def GeneratePDF(lyrics):
    try:
        nome_pdf = input('Informe o nome do PDF: ')
        pdf = canvas.Canvas('{}.pdf'.format(nome_pdf))
        x = 720
        for lyric in lyrics:
            x -= 20
            pdf.drawString(247, x, '{}'.format(lyric))
        #pdf.drawString(247, x, lista.items())
        pdf.setTitle(nome_pdf)
        pdf.setFont("Helvetica-Oblique", 14)
        pdf.drawString(245, 750, 'Lyrics')
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(245, 724, 'Song')
        pdf.save()
        print('{}.pdf criado com sucesso!'.format(nome_pdf))
    except:
        print('Erro ao gerar {}.pdf'.format(nome_pdf))


lyrics = lyrics

GeneratePDF(lyrics)
