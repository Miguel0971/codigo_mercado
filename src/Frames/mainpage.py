import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkwidgets import CheckboxTreeview
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.Class.Classes import Produtos
from src.Class.Classes import Usuario
from src.Class.Classes import Pages
estado_das_checkboxes = {}

root = tk.Tk()
root.title("Página Principal")
style = ttk.Style("darkly")
root.resizable(False, False)

variavel1 = tk.IntVar()
variavel2 = tk.IntVar()
UNCHECK = '☐' 
CHECKED = '✅'
subframe = ttk.Frame(root, padding=15, bootstyle="secondary", width=300)
subframe.pack(side=LEFT, fill=Y)
mainframe = ttk.Frame(root, padding=20, bootstyle="primary")
mainframe.pack(side=RIGHT, fill=BOTH, expand=TRUE)
frame_busca = ttk.Frame(mainframe, padding=10, style="primary")
frame_busca.pack(fill='x', padx=20, pady=10)


columns = ("Nome", "Código", "Preço", "Quantidade", "Validade", "Fabricação", "Peso")
treeview = CheckboxTreeview(mainframe, columns=columns, show="tree headings")
treeview.pack(fill='both', expand=True, padx=20, pady=20)
entrada_busca = ttk.Entry(frame_busca, font=("Arial", 14))
entrada_busca.pack(side='left', fill='x', expand=True, padx=2)


tabela = Produtos(treeview, estado_das_checkboxes, entrada_busca, root)
paginas = Pages(root, None)
usuario = Usuario(root, subframe)


botao_cadastro = ttk.Button(subframe, text="Cadastrar produto", bootstyle=(SUCCESS, OUTLINE), width=30, command=lambda: paginas.passar_pagina("./src/Frames/cadastrar.py"))
botao_cadastro.grid(column=1, row=1, sticky=(W), pady=(10,0))

botao_alterar = ttk.Button(subframe, text="Alterar produto", bootstyle=(SUCCESS,OUTLINE), width=30, command=tabela.alterar_produto)
botao_alterar.grid(column=1, row=2, sticky=(W), pady=(10,0))

botao_delete = ttk.Button(subframe, text="Deletar", bootstyle=(DANGER,OUTLINE), width=30, command=tabela.deletar)
botao_delete.grid(column=1, row=3, sticky=(W), pady=(10,0))

botao_logout = ttk.Button(subframe, text="Logout", bootstyle=(DANGER,OUTLINE), width=30, command=lambda: paginas.passar_pagina("./src/Frames/programa.py"))
botao_logout.grid(column=1, row=6, sticky=(S), pady=(300,0))


botao_buscar = ttk.Button(frame_busca, text="Buscar", bootstyle=INFO, command=tabela.mostrar_detalhes_do_produto)
botao_buscar.pack(side='left', padx=5)

usuario.administrador()


# Definir as colunas
for colunas in columns:
    treeview.heading(colunas, text=colunas)

treeview.column("Nome", width=100, anchor="center")
treeview.column("Código", width=100, anchor="center")
treeview.column("Preço", width=100, anchor="center")
treeview.column("Quantidade", width=100, anchor="center")
treeview.column("Validade", width=100, anchor="center")
treeview.column("Fabricação", width=100, anchor="center")
treeview.column("Peso", width=100, anchor="center")
tabela.tabela_produtos()
treeview.column("#0", width=80, anchor="center")
treeview.heading("#0", text="Selecionar", anchor="center")


root.mainloop()