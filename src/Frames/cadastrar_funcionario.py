import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
import subprocess

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


def cadastrar():
   cpf = entradas["CPF"].get()
   username = entradas["Nome de Usuário"].get()
   senha = entradas["Senha"].get()
   nome_completo = entradas["Nome Completo"].get()
   dados_funcionario = { entradas["CPF"].get(): {
        "nome": entradas["Nome de Usuário"].get(),
        "senha": entradas["Senha"].get(),
        "nome_completo": entradas["Nome Completo"].get()
   }
    }
   if not cpf or not username or not senha or not nome_completo or not dados_funcionario:
       mostrar_popup("Todos os campos são obrigatórios!")
   else:
       arquivo_funcionarios = open('./src/List/funcionarios.json', 'r', encoding='utf-8')
       funcionarios = json.load(arquivo_funcionarios)
       arquivo_funcionarios.close()
       funcionarios.update(dados_funcionario)
       arquivo = open('./src/List/funcionarios.json', 'w', encoding='utf-8')
       json.dump(funcionarios, arquivo, indent=4, ensure_ascii=False)
       arquivo.close()
       mostrar_popup("Funcionário cadastrado com sucesso!")
       

       


def voltar():
    root.destroy()
    subprocess.run(["python", "./src/Frames/mainpage.py"])




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

botao_voltar = ttk.Button(mainframe, text="Voltar", bootstyle=(DANGER,OUTLINE), padding=(40,20), command=voltar)
botao_voltar.grid(row=8, column=0, pady=(30, 10), padx=(10,10), sticky=W)

botao_cadastrar = ttk.Button(mainframe, text="Cadastrar", bootstyle=(SUCCESS,OUTLINE), padding=(40,20), command=cadastrar)
botao_cadastrar.grid(row=8, column=0, pady=(30,10), padx=(10,10), sticky=E)

root.mainloop()