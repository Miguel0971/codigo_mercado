import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
import sys

codigo = None
if len(sys.argv) > 1:
    codigo = sys.argv[1].zfill(5)
    print("Código recebido:", codigo)



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


def carregar_dados():
    # Carrega dados do produto para preencher as entradas
    try:
        with open('produtos.json', 'r', encoding='utf-8') as f:
            produtos = json.load(f)
        if codigo in produtos:
            produto = produtos[codigo]
            # preencher entradas
            entradas["Nome"].insert(0, produto.get("nome", ""))
            entradas["Preço"].insert(0, produto.get("preco", ""))
            entradas["Quant"].insert(0, produto.get("quantidade", ""))
            entradas["VAL"].insert(0, produto.get("val", ""))
            entradas["FAB"].insert(0, produto.get("fab", ""))
            entradas["Peso"].insert(0, produto.get("peso", ""))
        else:
            mostrar_popup("Código do produto não encontrado!")
    except Exception as e:
        mostrar_popup(f"Erro ao carregar dados: {str(e)}")


def alterar():
    nome = entradas["Nome"].get()
    preco = entradas["Preço"].get()
    quantidade = entradas["Quant"].get()
    val = entradas["VAL"].get()
    fab = entradas["FAB"].get()
    peso = entradas["Peso"].get()

    try:
        with open('produtos.json', 'r', encoding='utf-8') as f:
            produtos = json.load(f)

        if codigo in produtos:
            produtos[codigo] = {
                "nome": nome,
                "preco": preco,
                "quantidade": quantidade,
                "val": val,
                "fab": fab,
                "peso": peso
            }

            with open('produtos.json', 'w', encoding='utf-8') as f:
                json.dump(produtos, f, indent=4, ensure_ascii=False)

            mostrar_popup("Produto alterado com sucesso!")
        else:
            mostrar_popup("Produto não encontrado para alterar!")
    except Exception as e:
        mostrar_popup(f"Erro ao alterar produto: {str(e)}")


def voltar():
    root.destroy()  # Só fecha a janela, sem abrir subprocess


root = tk.Tk()
root.title("Alterar Produto")
style = ttk.Style("darkly")
root.resizable(False, False)

mainframe = ttk.Frame(root, padding=20)
mainframe.grid(row=0, column=0, sticky=(N, E, W, S))

labels_usadas = ["Nome", "Preço", "Quant", "VAL", "FAB", "Peso"]
entradas = {}

for contador, label in enumerate(labels_usadas):
    label_criada = tk.Label(mainframe, text=f"{label}:", relief="solid", bd=2, padx=10, pady=5, width=6, font=("Arial", 22))
    label_criada.grid(row=contador, column=0, padx=10, pady=5, sticky=W)

    entry_criada = ttk.Entry(mainframe, font=("Arial", 22))
    entry_criada.grid(row=contador, column=1, padx=(10, 20), pady=5, sticky=E)
    entradas[label] = entry_criada

botao_voltar = ttk.Button(mainframe, text="Voltar", bootstyle=(DANGER, OUTLINE), padding=(40, 20), command=voltar)
botao_voltar.grid(row=8, column=0, pady=(30, 10), padx=(10, 10), sticky=W)

botao_alterar = ttk.Button(mainframe, text="Alterar", bootstyle=(SUCCESS, OUTLINE), padding=(40, 20), command=alterar)
botao_alterar.grid(row=8, column=1, pady=(30, 10), padx=(10, 10), sticky=E)

carregar_dados()  # preenche as entradas com os dados atuais

root.mainloop()
