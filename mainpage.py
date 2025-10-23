import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
import subprocess
from PIL import Image, ImageTk

estado_das_checkboxes = {}
# Carregar imagens de checkbox



def carregar_produtos():
    arquivo_produtos = open('produtos.json', 'r', encoding='utf-8')
    produtos = json.load(arquivo_produtos)
    arquivo_produtos.close()
    return produtos

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



def cad_produto():
    root.destroy()
    subprocess.run(["python", "cadastrar.py"])

def voltar():
    root.destroy()
    subprocess.run(["python", "programa.py"])

def tabela_produtos():
    busca = entrada_busca.get().lower()
    produtos = carregar_produtos()
    for contador in treeview.get_children():
        treeview.delete(contador)  # Limpa a tabela antes de adicionar outros itens, evitando bug
    for id, produto in produtos.items():
      if busca in produto['nome'].lower():
        item_id = treeview.insert(
            '', 'end', 
            values=(produto['nome'], id, produto['preco'], produto['quantidade'], produto['val'], produto['fab'], produto['peso']), # As colunas da treeview para o programa
            image=imagem_unchecado  # Imagenzinha bonitinha para meu checkbox kkkkkkkk
        )
        treeview.item(item_id, image=imagem_unchecado)
        estado_das_checkboxes[item_id] = False


def alternar_checkbox(event):
    region = treeview.identify_region(event.x, event.y)
    column = treeview.identify_column(event.x)
    
    if region == "tree" or column == "#1":  # "#1" é a coluna 'Selecionar'
        item_id = treeview.identify_row(event.y)
        if item_id:
            estado_atual = estado_das_checkboxes.get(item_id, False)
            novo_estado = not estado_atual
            estado_das_checkboxes[item_id] = novo_estado
            imagem = imagem_checado if novo_estado else imagem_unchecado
            treeview.item(item_id, image=imagem)


def mostrar_detalhes_do_produto():
    busca = entrada_busca.get().lower()
    produtos = carregar_produtos()
    
    for id, produto in produtos.items():
        if busca in produto['nome'].lower():
            # Vai abrir um popup certinho com os detalhes do produto, resolvi fazer esse com popup porque não exige funções nem nada, não há necessidade de criar tela só para ele
            popup = tk.Toplevel(root)
            popup.title("Tela de Pesquisa")
            popup.geometry("420x400")
            popup.resizable(False, False)
            popup.configure(bg="#3399FF")  
            valores = [
                produto["nome"],
                id,
                produto["preco"],
                produto["quantidade"],
                produto["val"],
                produto["fab"],
                produto["peso"]
            ]
            
            labels_usadas = ["Nome", "Código", "Preço", "Quant", "VAL", "FAB", "Peso"]
            entradas = {}
            for i, (label, valor) in enumerate(zip(labels_usadas, valores)):
                label_criada = tk.Label(
                    popup, text=f"{label}:", relief="solid", bd=2, padx=10, pady=5,
                    width=6, font=("Arial", 14), bg="#3399FF", anchor="w"
                )
                label_criada.grid(row=i, column=0, padx=10, pady=5, sticky="w")

                entry_criada = ttk.Entry(popup, font=("Arial", 14), width=25)
                entry_criada.insert(0, valor)
                entry_criada.config(state="readonly")
                entry_criada.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            botao_voltar = ttk.Button(popup, text="Voltar", bootstyle=DANGER, command=popup.destroy, padding=(30,15))
            botao_voltar.grid(row=len(labels_usadas), column=0, columnspan=2, pady=15)
            return  # Dar uma parada no for para ele não meter o louco e procurar mais de um resultado

            

    
    # Se nenhum produto for encontrado
    mostrar_popup()

def itens_selecionados():
    selecionados = []
    for item_id, checado in estado_das_checkboxes.items():
        if checado:
            selecionados.append(item_id)
    return selecionados

def alterar_produto():
    selecionados = [item_id for item_id, marcado in estado_das_checkboxes.items() if marcado] # Procura o item marcado na checkbox
    
    if len(selecionados) == 0:
        mostrar_popup("Nenhum produto selecionado!")
        return
    
    if len(selecionados) > 1:
        mostrar_popup("Selecione apenas um produto para alterar!")
        return
    
    item_selecionado = selecionados[0]
    codigo_produto = treeview.item(item_selecionado)['values'][1]  # índice 1 é o código
    
    subprocess.run(["python", "alterar.py", str(codigo_produto)])
    tabela_produtos()
    
def confirmar_delete():
    # Recuperar o item selecionado
    selecionados = [item_id for item_id, marcado in estado_das_checkboxes.items() if marcado]
    
    if len(selecionados) == 0:
        mostrar_popup("Nenhum produto selecionado!")
        return
    
    if len(selecionados) > 1:
        mostrar_popup("Selecione apenas um produto para deletar!")
        return
    
    item_selecionado = selecionados[0]
    codigo_produto = treeview.item(item_selecionado)['values'][1]  
    
    produtos = carregar_produtos()


    codigo_str = str(codigo_produto)
    produtos_corrigidos = {} 

    for primeiro_correcao, segundo_correcao in produtos.items():
        chave_convertida = str(primeiro_correcao)
        produtos_corrigidos[chave_convertida] = segundo_correcao


    if codigo_str in produtos_corrigidos:
      del produtos_corrigidos[codigo_str]
      with open('produtos.json', 'w', encoding='utf-8') as arquivo_produtos:
        json.dump(produtos_corrigidos, arquivo_produtos, ensure_ascii=False, indent=4)
      tabela_produtos()
      mostrar_popup("Produto deletado com sucesso!")
    else:
      mostrar_popup(f"Produto não encontrado! (Código: {codigo_produto})")



def deletar():
    selecionados = [item_id for item_id, marcado in estado_das_checkboxes.items() if marcado] # Procura o item marcado na checkbox
    
    if len(selecionados) == 0:
        mostrar_popup("Nenhum produto selecionado!")
        return
    
    if len(selecionados) > 1:
        mostrar_popup("Selecione apenas um produto para alterar!")
        return
    
    item_selecionado = selecionados[0]
    codigo_produto = treeview.item(item_selecionado)['values'][1]  # índice 1 é o código
            # Vai abrir um popup certinho com os detalhes do produto, resolvi fazer esse com popup porque não exige funções nem nada, não há necessidade de criar tela só para ele
    popup = tk.Toplevel(root)
    popup.title("Confirmação")
    popup.geometry("550x200")
    popup.resizable(False, False)
    popup.configure(bg="#3399FF")  
    label = tk.Label(
        popup, text="Você tem certeza de que deseja deletar este produto?", font=("Arial", 14), bg="#3399FF", fg="white", padx=10, pady=10
    )
    label.grid(row=0, column=0, columnspan=2, pady=20, padx=20)
    
    botao_voltar = ttk.Button(popup, text="Voltar", bootstyle=DANGER, command=popup.destroy, padding=(20, 10))
    botao_voltar.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    
    botao_confirmar = ttk.Button(popup, text="Confirmar", bootstyle=SUCCESS, command=confirmar_delete, padding=(20, 10))
    botao_confirmar.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Daqui para baixo é básico, a parte visível da coisa.
# O que eu usei:
# root.resizable: Tornar não alterável o tamanho da página, para evitar cagada no meu código
# padding = alterar o tamanho
# pady/padx = Alterar o espaçamento em Y ou X
# Side = Nome diz né cacete, altera o lado que está
# Expand = Sério? Kkkkkkkk
# Fill = Função para dar uma encorpada a mais 
# Width = Aumentar o tamanho
# Column = Coluna da minha página
# Row = Linha da página
# Sticky = Forçar um lado, praticamente a mesma bosta do side

root = tk.Tk()
root.title("Página Principal")
style = ttk.Style("darkly")
root.resizable(False, False)

imagem_checado = ImageTk.PhotoImage(Image.open("checado.png").resize((20, 20)))
imagem_unchecado = ImageTk.PhotoImage(Image.open("unchecked.png").resize((20, 20)))


subframe = ttk.Frame(root, padding=15, bootstyle="secondary", width=300)
subframe.pack(side=LEFT, fill=Y)

mainframe = ttk.Frame(root, padding=20, bootstyle="primary")
mainframe.pack(side=RIGHT, fill=BOTH, expand=TRUE)

frame_busca = ttk.Frame(mainframe, padding=10, style="primary")
frame_busca.pack(fill='x', padx=20, pady=10)


botao_cadastro = ttk.Button(subframe, text="Cadastrar produto", bootstyle=(SUCCESS, OUTLINE), width=30, command=cad_produto)
botao_cadastro.grid(column=1, row=1, sticky=(W), pady=(10,0))

botao_alterar = ttk.Button(subframe, text="Alterar produto", bootstyle=(SUCCESS,OUTLINE), width=30, command=alterar_produto)
botao_alterar.grid(column=1, row=2, sticky=(W), pady=(10,0))

botao_logout = ttk.Button(subframe, text="Deletar", bootstyle=(DANGER,OUTLINE), width=30, command=deletar)
botao_logout.grid(column=1, row=3, sticky=(W), pady=(10,0))

botao_logout = ttk.Button(subframe, text="Logout", bootstyle=(DANGER,OUTLINE), width=30, command=voltar)
botao_logout.grid(column=1, row=4, sticky=(S), pady=(300,0))


entrada_busca = ttk.Entry(frame_busca, font=("Arial", 14))
entrada_busca.pack(side='left', fill='x', expand=True, padx=2)

botao_buscar = ttk.Button(frame_busca, text="Buscar", bootstyle=INFO, command=mostrar_detalhes_do_produto)
botao_buscar.pack(side='left', padx=5)


columns = ("Nome", "Código", "Preço", "Quantidade", "Validade", "Fabricação", "Peso")
treeview = ttk.Treeview(mainframe, columns=columns, show="tree headings", style="secondary")
treeview.pack(fill='both', expand=True, padx=20, pady=20)

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
treeview.bind("<Button-1>", alternar_checkbox)
tabela_produtos()
treeview.column("#0", width=75, anchor="center")
treeview.heading("#0", text="Selecionar")

root.mainloop()