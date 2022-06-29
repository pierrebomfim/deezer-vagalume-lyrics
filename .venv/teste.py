import PySimpleGUI as sg                        # Part 1 - The import

# Define the window's contents
layout = [  [sg.Text("Digite o ID do perfil Deezer")],     # Part 2 - The Layout
            [sg.Input()],
            [sg.Button('Buscar')],
            [sg.Text("Digite a playlist")],     # Part 2 - The Layout
            [sg.Input()],
            [sg.Button('Buscar')]  ]

# Create the window
window = sg.Window('Buscado de letra de músicas', layout)      # Part 3 - Window Defintion

# Display and interact with the Window
event, values = window.read()                   # Part 4 - Event loop or Window.read call

# Do something with the information gathered
#print('Hello', values[0], "! Thanks for trying PySimpleGUI")
id_deezer = values[0]

# Finish up by removing from the screen
window.close()       