
from pathlib import Path
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

#------------------------------------------------------------------------------------------
#Importando arquivos
from back import *
#importando thread
from threading import Thread

#Notificação (curta, longa)(sonora, visual)
#botão confirmar aplicar
camera = 0
tempoTrab = 50 #50 min pausa 10
User = "Gabriel"
#Botão confirmar
setup(User, tempoTrab*60, camera)

#botão realizar pausa       (Adianta momento da pausa)
def pause():
    pausar()
    x = 1
    #Troca para a tela da cartilha com botão despausar
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




OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\T-Gamer\Desktop\py\SCCP\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def janela_inicial():
    window = Tk()

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
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        335.0,
        165.0,
        image=image_image_1
    )

    #interrogação
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
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
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
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
        file=relative_to_assets("button_3.png"))
    button_3 = Button(
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
        file=relative_to_assets("button_4.png"))
    button_4 = Button(
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
        file=relative_to_assets("button_5.png"))
    button_5 = Button(
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
        file=relative_to_assets("button_6.png"))
    button_6 = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_6 clicked"),
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
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        205.5,
        119.5,
        image=entry_image_1
    )
    configs['entry_1'] = Entry(
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
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        322.5,
        195.5,
        image=entry_image_2
    )
    configs['entry_2'] = Entry(
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
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        108.0,
        195.5,
        image=entry_image_3
    )
    configs['entry_3'] = Entry(
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

janela_inicial()