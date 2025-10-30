import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.Class.Classes import Usuario
from src.Class.Classes import Pages

root = tk.Tk()
root.title('Login de Usuário')
style = ttk.Style("darkly")

mainframe = ttk.Frame(root, padding=100)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.resizable(False, False)
paginas = Pages(root, None)
usuarios = Usuario(root, None, None)

label_de_usuario = ttk.Label(mainframe, font=("Arial",16), text= 'Insira seu nome de usuário:')
label_de_usuario.grid(column=1, row=1, sticky=(W), pady=(0, 10))

entrada_de_usuario = tk.Entry(mainframe, width=80)
entrada_de_usuario.grid(column=1, row=2, sticky=(W, E), pady=(0, 10))

label_de_senha = ttk.Label(mainframe, font=("Arial",16), text= 'Insira sua senha:')
label_de_senha.grid(column=1, row= 3, sticky=(W), pady=(0,10))

entrada_de_senha = ttk.Entry(mainframe, width=80, show="*")
entrada_de_senha.grid(column=1, row=4, sticky=(W, E), pady=(0,10))

botao_gerador_senha = ttk.Button(mainframe, text="Gerar uma nova senha segura", bootstyle=(INFO,OUTLINE), padding=(10,10), command=usuarios.gerar_senha)
botao_gerador_senha.place(relx=1.18, rely=1.5, anchor=SE)

botao_esqueci = ttk.Button(mainframe, text="Esqueci minha senha", bootstyle=(DANGER, OUTLINE), width=30, command=lambda: paginas.passar_pagina("./src/Frames/redefinir_senha.py"))
botao_esqueci.grid(column=1, row=6, sticky=(W), pady=(10,0))

botao_entrar = ttk.Button(mainframe, text="Entrar", bootstyle=(SUCCESS, OUTLINE), width=30, command=lambda: usuarios.verificar_login(entrada_de_usuario, entrada_de_senha))
botao_entrar.grid(column=1, row=6, sticky=(E), pady=(10,0))

root.mainloop()