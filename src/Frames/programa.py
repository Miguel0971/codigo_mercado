import tkinter as tk
from tkinter import *
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import subprocess
import json 


def mostrar_popup(mensagem):
    popup = tk.Toplevel() 
    popup.title("Mensagem")
    popup.geometry("500x150")
    popup.resizable(False, False)
    
    label = ttk.Label(popup, text=mensagem, font=("Arial", 14))
    label.pack(padx=20, pady=20)

    botao_fechar = ttk.Button(popup, text="Fechar", bootstyle=(SUCCESS,OUTLINE), padding=(40,20), command=popup.destroy)
    botao_fechar.pack(pady=10)

    popup.transient(root) 
    popup.grab_set()  

def esqueci_pagina():
    root.destroy()
    subprocess.run(["python", "./src/Frames/redefinir_senha.py"])
S
def mainpage():
    root.destroy()
    subprocess.run(["python", "./src/Frames/mainpage.py"])

def verificar_login():
    nome_de_usuario = entrada_de_usuario.get().strip()
    senha_do_usuario = entrada_de_senha.get().strip()
    usuario_encontrado = False
    
    if not nome_de_usuario or not senha_do_usuario:
        mostrar_popup("Você não inseriu corretamente os dados!")
    else:
        arquivo_funcionarios = open('./src/List/funcionarios.json', 'r', encoding='utf-8')
        funcionarios = json.load(arquivo_funcionarios)
        for cpf, usuarios in funcionarios.items():
            if usuarios["nome"].lower() == nome_de_usuario.lower() and usuarios["senha"].lower() == senha_do_usuario.lower():
                dados_login = { "nome": nome_de_usuario }
                arquivo_login = open('./src/List/usuario_logado.json', 'r', encoding='utf-8')
                login = json.load(arquivo_login)
                arquivo_login.close()
                login.update(dados_login)
                arquivo = open('./src/List/usuario_logado.json', 'w', encoding='utf-8')
                json.dump(login, arquivo, indent=4, ensure_ascii=False)
                arquivo.close()
                usuario_encontrado = True
                root.destroy()  
                subprocess.run(["python", "./src/Frames/mainpage.py"])
                break
        if not usuario_encontrado:
            mostrar_popup("Seu usuário não foi encontrado no sistema.")


def gerar_senha():
    pass 
            

root = tk.Tk()
root.title('Login de Usuário')
style = ttk.Style("darkly")

mainframe = ttk.Frame(root, padding=100)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.resizable(False, False)




label_de_usuario = ttk.Label(mainframe, font=("Arial",16), text= 'Insira seu nome de usuário:')
label_de_usuario.grid(column=1, row=1, sticky=(W), pady=(0, 10))

entrada_de_usuario = tk.Entry(mainframe, width=80)
entrada_de_usuario.grid(column=1, row=2, sticky=(W, E), pady=(0, 10))

label_de_senha = ttk.Label(mainframe, font=("Arial",16), text= 'Insira sua senha:')
label_de_senha.grid(column=1, row= 3, sticky=(W), pady=(0,10))

entrada_de_senha = ttk.Entry(mainframe, width=80, show="*")
entrada_de_senha.grid(column=1, row=4, sticky=(W, E), pady=(0,10))

botao_gerador_senha = ttk.Button(mainframe, text="Gerar uma nova senha segura", bootstyle=(INFO,OUTLINE), padding=(10,10), command=gerar_senha)
botao_gerador_senha.place(relx=1.18, rely=1.5, anchor=SE)

botao_esqueci = ttk.Button(mainframe, text="Esqueci minha senha", bootstyle=(DANGER, OUTLINE), width=30, command=esqueci_pagina)
botao_esqueci.grid(column=1, row=6, sticky=(W), pady=(10,0))

botao_entrar = ttk.Button(mainframe, text="Entrar", bootstyle=(SUCCESS, OUTLINE), width=30, command=verificar_login)
botao_entrar.grid(column=1, row=6, sticky=(E), pady=(10,0))


root.mainloop()


