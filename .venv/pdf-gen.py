# Geração de PDF com letras e traduções das musicas da playlist desejada

# Fuctions from the FAQ at reportlab.org/oss/rl-toolkit/faq/#1.1
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from deezer_pl import pl_name
from vagalume import song_name, artist_name, lyric
import sqlite3




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


def go(lyric):
    doc = SimpleDocTemplate(f"{pl_name}.pdf")
    Story = [Spacer(1, 2*inch)]
    style = styles["Normal"]
    s = Paragraph(song_name, style)
    p = Paragraph(lyric, style)
    a = Paragraph(artist_name, style)

    Story.append(s)
    Story.append(a)
    Story.append(Spacer(1, 0.2*inch))
    Story.append(p)
    Story.append(Spacer(1, 0.2*inch))
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)


if __name__ == "__main__":
    go(lyric)


