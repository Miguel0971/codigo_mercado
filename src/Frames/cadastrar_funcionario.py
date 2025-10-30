import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkwidgets import CheckboxTreeview
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.Class.Classes import Popup
from src.Class.Classes import Produtos
from src.Class.Classes import Usuario
from src.Class.Classes import Pages
paginas = Pages()

root = tk.Tk()
root.title("Cadastro de Funcionário")
style = ttk.Style("darkly")
root.resizable(False, False)

mainframe = ttk.Frame(root, padding=2)
mainframe.grid(row=0, column=0, sticky=(N, E, W, S))

labels_usadas = ["CPF", "Nome de Usuário", "Senha", "Nome Completo"]
entradas = {}
for contador, label in enumerate(labels_usadas):
    label_criada = tk.Label(mainframe, text=f"{label}: ", relief="solid", bd=2, padx=10, pady=5, width=15, font=("Arial",16))
    label_criada.grid(row=contador, column=0, padx=10, pady=5, sticky=W)

    entry_criada = ttk.Entry(mainframe, font=("Arial",16))
    entry_criada.grid(row=contador, column=0, padx=(220,0), pady=5, sticky=E)
    entradas[label] = entry_criada
    
funcionarios = Usuario(root, None, entradas)



botao_voltar = ttk.Button(mainframe, text="Voltar", bootstyle=(DANGER,OUTLINE), padding=(40,20), command=lambda: paginas.passar_pagina("./src/Frames/mainpage.py"))
botao_voltar.grid(row=8, column=0, pady=(30, 10), padx=(10,10), sticky=W)

botao_cadastrar = ttk.Button(mainframe, text="Cadastrar", bootstyle=(SUCCESS,OUTLINE), padding=(40,20), command=funcionarios.cadastrar_func)
botao_cadastrar.grid(row=8, column=0, pady=(30,10), padx=(10,10), sticky=E)

root.mainloop()