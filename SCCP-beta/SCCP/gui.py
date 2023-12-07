
from pathlib import Path
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

#------------------------------------------------------------------------------------------
#Importando arquivos
from back import *
#importando thread
from threading import Thread
#importando função para abrir arquivo pdf
import os
#importando aleatoriedade para escolha do exercicio da pausa
import random

#Notificação (curta, longa)(sonora, visual)
#botão confirmar aplicar
camera = 0
tempoTrab = 50 #50 min pausa 10
User = "Gabriel"
#Botão confirmar
setup(User, tempoTrab*60, camera)

#botão realizar pausa       (Adianta momento da pausa)
def pause():
    global window
    pausar()
    exercicio = random.choice(['punho','pescoço','membrosSup','colunaEInferiores'])
    if exercicio == 'punho':
        exPunho()
    elif exercicio == 'pescoço':
        exPescoco()
    elif exercicio == 'membrosSup':
        exSuperiores()
    elif exercicio == 'colunaEInferiores':
        exColuna()


#botão informações. falar angulos, falar para que serve e como funciona o app.
#-----------------------------------------------------------------------------------------
configs = {}
def adjusts():
    global User, tempoTrab, camera
    aux = 0
    if configs['entry_1'].get():
        User = str(configs['entry_1'].get())
        aux = 1
    else:
        User = "Gabriel"
    if configs['entry_3'].get()!='':
        tempoTrab = int(configs['entry_3'].get())
        aux = 1
    else:
        tempoTrab = 50
    if configs['entry_2'].get()!='':
        camera = int(configs['entry_2'].get())
        aux = 1
    else:
        camera = 0
        #print(User, tempoTrab*60, camera)
        setup(User, tempoTrab*60, camera)
    if aux:
        notificacao = Notification(app_id='Sistema de classificação e correção postural', title='Informações atualizadas', msg='Usuário: '+User+'\nTempo até pausa definido: '+str(tempoTrab)+' minuto(s)\n'+'Camera selecionada: '+str(camera))
        notificacao.show()

def infos():
    os.startfile('saiba_mais.pdf')


#abre a cartilha completa
def cartilha_completa():
    os.startfile('ALONGAMENTO.pdf')


OUTPUT_PATH = Path(__file__).parent
#ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\T-Gamer\Desktop\py\SCCP\build\assets\frame0")
ASSETS_PATH = os.path.join(OUTPUT_PATH, r"assets\frame0")
#(r"\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

#janela incial, botões, funções
def janela_inicial():
    global window
    for i in window.winfo_children():
        i.destroy()

    window.geometry("670x330")
    window.configure(bg = "#FFFFFF")

    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 330,
        width = 670,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("inicial_fundo.png"))
    image_1 = canvas.create_image(
        335.0,
        165.0,
        image=image_image_1
    )

    #interrogação
    button_image_1 = PhotoImage(
        file=relative_to_assets("inicial_interrogacao.png"))
    button_1 = Button(window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: infos(),
        relief="flat"
    )
    button_1.place(
        x=605.0,
        y=8.0,
        width=53.0,
        height=51.980770111083984
    )

    #iniciar/retomar
    button_image_2 = PhotoImage(
        file=relative_to_assets("inicial_iniciar.png"))
    button_2 = Button(window,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: iniciar(),
        relief="flat"
    )
    button_2.place(
        x=468.0,
        y=83.0,
        width=190.0,
        height=55.0
    )

    #pausar
    button_image_3 = PhotoImage(
        file=relative_to_assets("inicial_pausar.png"))
    button_3 = Button(window,
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: pause(),
        relief="flat"
    )
    button_3.place(
        x=467.0,
        y=161.0,
        width=191.0,
        height=57.0
    )

    #finalizar execução
    button_image_4 = PhotoImage(
        file=relative_to_assets("inicial_finalizar.png"))
    button_4 = Button(window,
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: finalizar(),
        relief="flat"
    )
    button_4.place(
        x=468.0,
        y=233.0,
        width=190.0,
        height=56.0
    )

    #confirmar
    button_image_5 = PhotoImage(
        file=relative_to_assets("inicial_confirmar.png"))
    button_5 = Button(window,
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: adjusts(),
        relief="flat"
    )
    button_5.place(
        x=13.0,
        y=235.0,
        width=192.0,
        height=54.0
    )

    #exercicios
    button_image_6 = PhotoImage(
        file=relative_to_assets("inicial_exercicios.png"))
    button_6 = Button(window,
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: cartilha_completa(),
        relief="flat"
    )
    button_6.place(
        x=374.0,
        y=236.0,
        width=53.01960754394531,
        height=52.0
    )

    #user
    entry_image_1 = PhotoImage(
        file=relative_to_assets("inicial_user.png"))
    entry_bg_1 = canvas.create_image(
        205.5,
        119.5,
        image=entry_image_1
    )
    configs['entry_1'] = Entry(window,
        bd=0,
        bg="#94C9FA",
        fg="#000716",
        highlightthickness=0
    )
    configs['entry_1'].place(
        x=30.0,
        y=108.0,
        width=351.0,
        height=21.0
    )

    #camera
    entry_image_2 = PhotoImage(
        file=relative_to_assets("inicial_camera.png"))
    entry_bg_2 = canvas.create_image(
        322.5,
        195.5,
        image=entry_image_2
    )
    configs['entry_2'] = Entry(window,
        bd=0,
        bg="#94C9FA",
        fg="#000716",
        highlightthickness=0
    )
    configs['entry_2'].place(
        x=264.0,
        y=184.0,
        width=117.0,
        height=21.0
    )

    #tempo de trab
    entry_image_3 = PhotoImage(
        file=relative_to_assets("inicial_tempo.png"))
    entry_bg_3 = canvas.create_image(
        108.0,
        195.5,
        image=entry_image_3
    )
    configs['entry_3'] = Entry(window,
        bd=0,
        bg="#94C9FA",
        fg="#000716",
        highlightthickness=0
    )
    configs['entry_3'].place(
        x=30.0,
        y=184.0,
        width=156.0,
        height=21.0
    )
    window.resizable(False, False)
    window.mainloop()

def exPunho():
    global window
    for i in window.winfo_children():           #fecha os elementos da janela atual
        i.destroy()


    window.geometry("380x878")
    window.configure(bg = "#FFFFFF")
    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 878,
        width = 380,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("ex_punho.png"))
    image_1 = canvas.create_image(
        190.0,
        439.0,
        image=image_image_1
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("ex_voltar.png"))
    button_1 = Button(window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: janela_inicial(),
        relief="flat"
    )
    button_1.place(
        x=12.0,
        y=8.0,
        width=40.0,
        height=40.0
    )
    
    window.resizable(False, False)
    window.mainloop()

def exPescoco():
    global window
    for i in window.winfo_children():           #fecha os elementos da janela atual
        i.destroy()
    
    window.geometry("380x627")
    window.configure(bg = "#FFFFFF")
    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 627,
        width = 380,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("ex_pescoco.png"))
    image_1 = canvas.create_image(
        190.0,
        313.0,
        image=image_image_1
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("ex_voltar.png"))
    button_1 = Button(window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: janela_inicial(),
        relief="flat"
    )
    button_1.place(
        x=11.0,
        y=8.0,
        width=40.0,
        height=40.0
    )
    window.resizable(False, False)
    window.mainloop()

def exSuperiores():
    global window
    for i in window.winfo_children():           #fecha os elementos da janela atual
        i.destroy()
    
    window.geometry("380x802")
    window.configure(bg = "#FFFFFF")
    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 802,
        width = 380,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("ex_sup.png"))
    image_1 = canvas.create_image(
        190.0,
        404.0,
        image=image_image_1
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("ex_voltar.png"))
    button_1 = Button(window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: janela_inicial(),
        relief="flat"
    )
    button_1.place(
        x=11.0,
        y=8.0,
        width=40.0,
        height=40.0
    )
    window.resizable(False, False)
    window.mainloop()

def exColuna():
    global window
    for i in window.winfo_children():           #fecha os elementos da janela atual
        i.destroy()
    
    window.geometry("380x873")
    window.configure(bg = "#FFFFFF")
    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 873,
        width = 380,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("ex_coluna.png"))
    image_1 = canvas.create_image(
        190.0,
        441.0,
        image=image_image_1
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("ex_voltar.png"))
    button_1 = Button(window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: janela_inicial(),
        relief="flat"
    )
    button_1.place(
        x=12.0,
        y=8.0,
        width=40.0,
        height=40.0
    )
    window.resizable(False, False)
    window.mainloop()



window = Tk()                                   #cria janela
janela_inicial()                                #chama função de ajustar janela
