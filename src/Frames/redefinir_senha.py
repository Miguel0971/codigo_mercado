import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.Class.Classes import Popup
from src.Class.Classes import Usuario
from src.Class.Classes import Pages

root = tk.Tk()
root.title("Redefinir Senha")
style = ttk.Style("darkly")
root.resizable(False, False)
popups = Popup(root, None)

mainframe = ttk.Frame(root, padding=100)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

paginas = Pages(root, None)



labels_usadas = ["Insira seu CPF", "Insira seu nome completo", "Insira sua nova senha"]
entradas = {}

for contador, label in enumerate(labels_usadas):
    label_criada = tk.Label(mainframe, text=f"{label}:", relief="solid", bd=2, padx=10, pady=5, width=26, font=("Arial", 16))
    label_criada.grid(row=contador*2, column=0, pady=(0,10), sticky=W)

    entry_criada = ttk.Entry(mainframe, font=("Arial", 22))
    entry_criada.grid(row=contador*2+1, column=0, pady=5, sticky=E)
    entradas[label] = entry_criada

funcionarios = Usuario(root, None, entradas, None)

botao_voltar = ttk.Button(mainframe, text="Voltar", bootstyle=DANGER, padding=(40,20), command=lambda:paginas.passar_pagina("./src/Frames/programa.py"))
botao_voltar.grid(row=6, column=0, pady=(5, 0), sticky=W)

botao_enviar = ttk.Button(mainframe, text="Enviar", bootstyle=SUCCESS, padding=(40,20), command=lambda:funcionarios.redefinir_senha(entradas))
botao_enviar.grid(row=6, column=0, pady=(5, 0), sticky=E)

botao_gerador_senha = ttk.Button(mainframe, text="Gerar uma nova senha segura", bootstyle=(INFO,OUTLINE), padding=(10,10), command=funcionarios.gerar_senha)
botao_gerador_senha.place(relx=1.25, rely=1.25, anchor=SE)



root.mainloop()