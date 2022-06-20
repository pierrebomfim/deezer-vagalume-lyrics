# Geração de PDF com letras e traduções das musicas da playlist desejada

# Fuctions from the FAQ at reportlab.org/oss/rl-toolkit/faq/#1.1
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from deezer_pl import plquery
from deezer_tk import tracks_list
import vagalume
import sqlite3

conn = sqlite3.connect('mydeezer.db')
cur = conn.cursor()

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]
styles = getSampleStyleSheet()
Title = f"Playlist: {plquery}"
pageinfo = " - Lyrics of Deezer Songs. Lyrics from api.vagalume.com.br."

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

def go():
    doc = SimpleDocTemplate(f"{plquery}.pdf")
    Story = [Spacer(1, 1*inch)]
    style = styles["Normal"]

    for track in tracks_list:
        cur.execute('''SELECT id, title, artist FROM Tracks WHERE title = ?''', (track, ))
        id = cur.fetchone()[0]
        title = cur.fetchone()[1]
        artist = cur.fetchone()[2]
        cur.execute('''SELECT lyric FROM Lyrics WHERE track_id = ?''', (id, ))
        try:
            lyric = cur.fetchone()[0]
        except:
            print(' ')
        #print(id, title, lyric)
        t = Paragraph(title, style)
        l = Paragraph(lyric, style)
        a = Paragraph(artist, style)        
        Story.append(t)
        Story.append(a)
        Story.append(Spacer(1, 0.2*inch))
        Story.append(l)
        Story.append(Spacer(1, 0.2*inch))
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
    print('\nPDF gerado com sucesso!!! ')

if __name__ == "__main__":
    go()

conn.commit()
cur.close()



# Pendência: Gerar nome da música automaticamente  ok!
