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
   nome = entradas["Nome"].get()
   codigo = entradas["Código"].get()
   preco = entradas["Preço"].get()
   quantidade = entradas["Quant"].get()
   val = entradas["VAL"].get()
   fab = entradas["FAB"].get()
   peso = entradas["Peso"].get()
   dados_produto = { entradas["Código"].get(): {
        "nome": entradas["Nome"].get(),
        "preco": entradas["Preço"].get(),
        "quantidade": entradas["Quant"].get(),
        "val": entradas["VAL"].get(),
        "fab": entradas["FAB"].get(),
        "peso": entradas["Peso"].get()
   }
    }
   if not nome or not codigo or not preco or not quantidade or not val or not fab or not peso or not dados_produto:
       mostrar_popup("Todos os campos são obrigatórios!")
   else:
       arquivo_produtos = open('produtos.json', 'r', encoding='utf-8')
       produtos = json.load(arquivo_produtos)
       arquivo_produtos.close()
       produtos.update(dados_produto)
       arquivo = open('produtos.json', 'w', encoding='utf-8')
       json.dump(produtos, arquivo, indent=4, ensure_ascii=False)
       arquivo.close()
       mostrar_popup("Produto cadastrado com sucesso!")
       

       


def voltar():
    root.destroy()
    subprocess.run(["python", "mainpage.py"])




root = tk.Tk()
root.title("Cadastro de Produto")
style = ttk.Style("darkly")
root.resizable(False, False)

mainframe = ttk.Frame(root, padding=2)
mainframe.grid(row=0, column=0, sticky=(N, E, W, S))

labels_usadas = ["Nome", "Código", "Preço", "Quant", "VAL", "FAB", "Peso"]
entradas = {}




for contador, label in enumerate(labels_usadas):
    label_criada = tk.Label(mainframe, text=f"{label}: ", relief="solid", bd=2, padx=10, pady=5, width=6, font=("Arial",22))
    label_criada.grid(row=contador, column=0, padx=10, pady=5, sticky=W)

    entry_criada = ttk.Entry(mainframe, font=("Arial",22))
    entry_criada.grid(row=contador, column=0, padx=(136,0), pady=5, sticky=E)
    entradas[label] = entry_criada

botao_voltar = ttk.Button(mainframe, text="Voltar", bootstyle=(DANGER,OUTLINE), padding=(40,20), command=voltar)
botao_voltar.grid(row=8, column=0, pady=(30, 10), padx=(10,10), sticky=W)

botao_cadastrar = ttk.Button(mainframe, text="Cadastrar", bootstyle=(SUCCESS,OUTLINE), padding=(40,20), command=cadastrar)
botao_cadastrar.grid(row=8, column=0, pady=(30,10), padx=(10,10), sticky=E)

root.mainloop()