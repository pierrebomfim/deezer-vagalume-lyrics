# img_viewer.py

import PySimpleGUI as sg

#import pdfgenerator as pdfgen
import os.path

# First the window layout in 2 columns

file_list_column = [
    [
        sg.Text("ID do perfil Deezer"),
        sg.In(size=(25, 1), enable_events=True, key="-ID DEEZER-"),
        sg.Button(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-PL LIST-"
        )
    ],
]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Finder", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    teste = values[0]

# Folder name was filled in, make a list of files in the folder
if event == "-ID DEEZER-":
    id_deezer = values["-ID DEEZER-"]
    try:
        # Get list of files in folder
        import deezer_pl as pl
        file_list = pl.usuario(id_deezer)
    except:
        file_list = []

    fnames = [
        teste
    ]
    window["-FILE LIST-"].update(fnames)

elif event == "-FILE LIST-":  # A file was chosen from the listbox
    try:
        filename = os.path.join(
            values["-FOLDER-"], values["-FILE LIST-"][0]
        )
        window["-TOUT-"].update(filename)
        window["-IMAGE-"].update(filename=filename)
    except:
        pass

window.close()