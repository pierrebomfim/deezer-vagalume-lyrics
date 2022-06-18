# Geração de PDF com letras e traduções das musicas da playlist desejada

# Fuctions from the FAQ at reportlab.org/oss/rl-toolkit/faq/#1.1
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from deezer_pl import pl_name
import sqlite3

#   **** **** Ultima versão  ********
conn = sqlite3.connect('mylyrics.db')
cur = conn.cursor()

cur.execute('''SELECT song, lyric, id FROM Lyrics''')
lyrics = cur.fetchall()
for l in lyrics:
    id = l[2]
    #print(id)
    cur.execute('''SELECT artist FROM Artist WHERE id = ?''', (id,))
    artists = cur.fetchall()
    for a in artists:
        artist = a[0]
    #print(artist)


PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]
styles = getSampleStyleSheet()
Title = "Lyrics"
pageinfo = " - Lyrics from Deezer Songs"


def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Bold', 16)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, Title)
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)
    canvas.restoreState()


def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo))
    canvas.restoreState()


def go(lyrics):
    doc = SimpleDocTemplate(f"{pl_name}.pdf")
    Story = [Spacer(1, 2*inch)]
    style = styles["Normal"]
    for l in lyrics:
        song = l[0]
        lyric = l[1]
        id = l[2]
        s = Paragraph(song, style)
        p = Paragraph(lyric, style)

        cur.execute('''SELECT artist FROM Artist WHERE id = ?''', (id,))
        artists = cur.fetchall()
        for a in artists:
            artist = a[0]
        a = Paragraph(artist, style)

        Story.append(s)
        Story.append(a)
        Story.append(Spacer(1, 0.2*inch))
        Story.append(p)
        Story.append(Spacer(1, 0.2*inch))
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


if __name__ == "__main__":
    go(lyrics)

cur.close()

print(songs)
# Pendência: Gerar nome da música automaticamente  ok!
