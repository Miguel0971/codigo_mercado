import tkinter as tk
import ttkbootstrap as ttk
import subprocess
from ttkbootstrap.constants import *
from tkinter import *

root = tk.Tk()
root.title("Redefinir Senha")
style = ttk.Style("darkly")
root.resizable(False, False)

def botao_enviar():
  # if entrada_cpf.get() == "" or entrada_nome.get() == "" or entrada_senha.get() == "":
  #   print("Preencha todos os campos!")
  # elif entrada_cpf.get() and entrada_nome.get() and entrada_senha.get():
  #   print("Senha redefinida com sucesso!")
  #   root.destroy()
  #   subprocess.run(["python", "main.py"])
  pass
  

def botao_voltar():
  root.destroy()
  subprocess.run(["python", "programa.py"])

mainframe = ttk.Frame(root, padding=250)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))


label_cpf = ttk.Label(mainframe, text="Insira seu CPF:", font=("Arial",16))
label_cpf.grid(row=0, column=1, sticky=W)
entrada_cpf = ttk.Entry(mainframe, width=60)
entrada_cpf.grid(row=1, column=1, pady=(0,10), sticky=(W,E))

label_nome = ttk.Label(mainframe, text="Insira seu nome completo:", font=("Arial",16))
label_nome.grid(row=2, column=1, pady=(0,10), sticky=W)
entrada_nome = ttk.Entry(mainframe, width=60)
entrada_nome.grid(row=3, column=1, sticky=(W,E))

label_senha = ttk.Label(mainframe, text="Insira sua senha:", font=("Arial",16))
label_senha.grid(row=4, column=1, pady=(0,10), sticky= W)
entrada_senha = ttk.Entry(mainframe, width=60)
entrada_senha.grid(row=5, column=1, pady=(0,10), sticky=(W,E))

botao_voltar = ttk.Button(mainframe, text="Voltar", bootstyle=DANGER, padding=(40,20), command=botao_voltar)
botao_voltar.grid(row=6, column=1, pady=(5, 0), sticky=W)

botao_enviar = ttk.Button(mainframe, text="Enviar", bootstyle=SUCCESS, padding=(40,20), command=botao_enviar)
botao_enviar.grid(row=6, column=1, pady=(5, 0), sticky=E)



root.mainloop()