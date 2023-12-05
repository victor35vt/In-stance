
from pathlib import Path
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


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
        command=lambda: print("button_2 clicked"),
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
        command=lambda: print("button_3 clicked"),
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
        command=lambda: print("button_4 clicked"),
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
        command=lambda: print("button_5 clicked"),
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

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        205.5,
        119.5,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#94C9FA",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=30.0,
        y=108.0,
        width=351.0,
        height=21.0
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        322.5,
        195.5,
        image=entry_image_2
    )
    entry_2 = Entry(
        bd=0,
        bg="#94C9FA",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.place(
        x=264.0,
        y=184.0,
        width=117.0,
        height=21.0
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        108.0,
        195.5,
        image=entry_image_3
    )
    entry_3 = Entry(
        bd=0,
        bg="#94C9FA",
        fg="#000716",
        highlightthickness=0
    )
    entry_3.place(
        x=30.0,
        y=184.0,
        width=156.0,
        height=21.0
    )
    window.resizable(False, False)
    window.mainloop()

janela_inicial()