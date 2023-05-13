import json
import tkinter as tk
import PySimpleGUI as sg
import random

# Carrega l'arxiu json amb els reptes
with open('Reptes STEM.json', 'r') as f:
    llista_reptes = json.load(f)["reptes"]

# Funció per mostrar la pregunta i les possibles respostes en una finestra grafica
def presenta_repte(repte, window):

    layout = [    [sg.Text(repte["pregunta"], font=("Helvetica", 14), size=(50, 2))],
    *[[sg.Radio(resposta, group_id="respostes", font=("Helvetica", 12), key=idx)] for idx, resposta in enumerate(repte["respostes"])],
    [sg.Button("Confirmeu la resposta", size=(20, 2), bind_return_key=True)]
    ]
    
    window.layout(layout)

    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):
            break
        if event == "Confirmeu la resposta":
            resposta = next((idx for idx, val in enumerate(values.values()) if val), None)
            if resposta is not None:
                break
            else:
                sg.popup("Si us plau, tria una resposta")
    window.close()
    return resposta

# Funció per verificar la resposta de l'usuari i mostrar la resposta correcta i la historia en una finestra grafica
def verificar_resposta(repte, resposta):
    resposta_correcta = repte["resposta_correcta"]
    resposta_seleccionada = repte["respostes"][resposta]
    if resposta == resposta_correcta:
        resultado = "¡Resposta correcta!"
        bg_color = "green"
    else:
        resultado = "Resposta incorrecta."
        bg_color = "yellow"
    layout = [[sg.Text(resultado, font=("Helvetica", 14), size=(50,2))],
              [sg.Text(f"La resposta correcta es: {repte['respostes'][resposta_correcta]}", font=("Helvetica", 12), size=(50,2))],
              [sg.Text(repte["historia"], font=("Helvetica", 12), size=(50,10))],
              [sg.Button('Continueu')]]
    window = sg.Window('Resultat', layout, size=(500, 450), background_color=bg_color)
    event, values = window.read()
    window.close()
    return event


# Joc principal

sg.theme('LightBlue2')
layout = [[sg.Text("Benvinguts al joc de reptes STEM", font=("Helvetica", 16), size=(50,2))],
          [sg.Button("Inicieu")]]
window = sg.Window('Joc STEM', layout, size=(500, 150))
event, values = window.read()
window.close()

random.shuffle(llista_reptes)  # Barreja la llista de reptes de forma aleatoria
reptes_presentats = []  # Inicialitza la llista de reptes presentats

for repte in llista_reptes:
    if llista_reptes.index(repte) in reptes_presentats:
        continue  # Si el repte ja ha estat presentat, passa al seguent
    window = sg.Window(f"Repte {repte['area']}", size=(500, 300))
    resposta = presenta_repte(repte, window)
    window.close()
    verificar_resposta(repte, resposta)
    reptes_presentats.append(llista_reptes.index(repte))  # Agrega l'index del repte ja presentat a la lista de reptes presentats

