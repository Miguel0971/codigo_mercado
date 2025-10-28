import tkinter as tk
import ttkbootstrap as ttk
import subprocess
from ttkbootstrap.constants import *
from tkinter import *

root = tk.Tk()
root.title("Redefinir Senha")
style = ttk.Style("darkly")
root.resizable(False, False)

def mostrar_popup(mensagem):
    popup = tk.Toplevel() 
    popup.title("Mensagem")
    popup.geometry("500x150")
    popup.resizable(False, False)
    
    label = ttk.Label(popup, text=mensagem, font=("Arial", 14))
    label.pack(padx=20, pady=20)

    botao_fechar = ttk.Button(popup, text="Fechar", bootstyle=(SUCCESS,OUTLINE), padding=(40,20), command=popup.destroy)
    botao_fechar.pack(pady=10)

    # Não deixar usar a tela de cadastro enquanto tá com o popup ligado
    popup.transient(root)  # Faz o pupop ficar em cima da tela de cadastro
    popup.grab_set()  # Faz com que o foco permaneça na janela do popup

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
  subprocess.run(["python", "./src/Frames/programa.py"])

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