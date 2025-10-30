import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
import subprocess
from PIL import Image, ImageTk
from ttkwidgets import CheckboxTreeview
import sys, os

class MainClass:
    def __init__(self):
        pass

class Popup:
    # Método construtor: define o que há
    def __init__(self, popup, root):
        self.popup = popup
        self.root = root

    # Método: o que faz
    def mostrar_popup(self, mensagem):
        self.popup = tk.Toplevel(self.root)
        self.popup.title("Mensagem")
        self.popup.geometry("500x150")
        self.popup.resizable(False, False)

        label = ttk.Label(self.popup, text=mensagem, font=("Arial", 14))
        label.pack(padx=20, pady=20)

        botao_fechar = ttk.Button(self.popup, text="Fechar", bootstyle=(SUCCESS,OUTLINE), padding=(40,20), command=self.popup.destroy)
        botao_fechar.pack(pady=10)

        self.popup.transient(self.root)
        self.popup.grab_set()
        
        
class Produtos:
    def __init__(self, treeview, estado_das_checkboxes, entrada_busca, root):
        self.treeview = treeview
        self.estado = estado_das_checkboxes
        self.entrada_busca = entrada_busca
        self.root = root
        
        
    def carregar_produtos(self):
        arquivo_produtos = open('./src/List/produtos.json', 'r', encoding='utf-8')
        produtos = json.load(arquivo_produtos)
        arquivo_produtos.close()
        return produtos
    
    def codigo(self):
        codigo = None
        if len(sys.argv) > 1:
            codigo = sys.argv[1].zfill(5)
            print("Código recebido:", codigo)
        
    
    def carregar_dados(self, entradas):
        popups = Popup()
        try:
            with open('./src/List/produtos.json', 'r', encoding='utf-8') as f:
                produtos = json.load(f)
            if self.codigo in produtos:
                produto = produtos[self.codigo]
            # preencher entradas
                entradas["Nome"].insert(0, produto.get("nome", ""))
                entradas["Preço"].insert(0, produto.get("preco", ""))
                entradas["Quant"].insert(0, produto.get("quantidade", ""))
                entradas["VAL"].insert(0, produto.get("val", ""))
                entradas["FAB"].insert(0, produto.get("fab", ""))
                entradas["Peso"].insert(0, produto.get("peso", ""))
            else:
                popups.mostrar_popup("Código do produto não encontrado!")
        except Exception as e:
            popups.mostrar_popup(f"Erro ao carregar dados: {str(e)}")
    
    def alterar(self, entradas):
        popups = Popup()
        nome = entradas["Nome"].get()
        preco = entradas["Preço"].get()
        quantidade = entradas["Quant"].get()
        val = entradas["VAL"].get()
        fab = entradas["FAB"].get()
        peso = entradas["Peso"].get()

        try:
            with open('./src/List/produtos.json', 'r', encoding='utf-8') as f:
                produtos = json.load(f)

            if self.codigo in produtos:
                produtos[self.codigo] = {
                    "nome": nome,
                    "preco": preco,
                    "quantidade": quantidade,
                    "val": val,
                    "fab": fab,
                    "peso": peso
                }

                with open('./src/List/produtos.json', 'w', encoding='utf-8') as f:
                    json.dump(produtos, f, indent=4, ensure_ascii=False)

                popups.mostrar_popup("Produto alterado com sucesso!")
            else:
                popups.mostrar_popup("Produto não encontrado para alterar!")
        except Exception as e:
            popups.mostrar_popup(f"Erro ao alterar produto: {str(e)}")
    
    def tabela_produtos(self):
        busca = self.entrada_busca.get().lower()
        produtos = self.carregar_produtos()
        for contador in self.treeview.get_children():
            self.treeview.delete(contador)  # Limpa a tabela antes de adicionar outros itens, evitando bug
        for id, produto in produtos.items():
            if busca in produto['nome'].lower():
                item_id = self.treeview.insert(
                    '', 'end', 
                values=(produto['nome'], id, produto['preco'], produto['quantidade'], produto['val'], produto['fab'], produto['peso'])
                )
            self.estado[item_id] = False
    
    def alterar_produto(self):
        selecionados = self.treeview.get_checked() # Procura o item marcado na checkbox
    
        if len(selecionados) == 0:
            popup_n_selecionado = Popup(None, self.root)
            popup_n_selecionado.mostrar_popup("Nenhum produto selecionado!")
            return
    
        if len(selecionados) > 1:
            popup_selecione = Popup(None, self.root)
            popup_selecione.mostrar_popup("Selecione apenas um produto para alterar!")
            return
    
        item_selecionado = selecionados[0]
        codigo_produto = self.treeview.item(item_selecionado)['values'][1]  # índice 1 é o código
    
        subprocess.run(["python", "./src/Frames/alterar.py", str(codigo_produto)])
        self.tabela_produtos()
    
    def deletar(self):
        selecionados = self.treeview.get_checked() # Procura o item marcado na checkbox
    
        if len(selecionados) == 0:
            popup_n_selecionado = Popup(None, self.root)
            popup_n_selecionado.mostrar_popup("Nenhum produto selecionado!")
            return
    
        if len(selecionados) > 1:
            popup_selecione = Popup(None, self.root)
            popup_selecione.mostrar_popup("Selecione apenas um produto para deletar!")
            return
            # Vai abrir um popup certinho com os detalhes do produto, resolvi fazer esse com popup porque não exige funções nem nada, não há necessidade de criar tela só para ele
        self.popup = tk.Toplevel(self.root)
        self.popup.title("Confirmação")
        self.popup.geometry("550x200")
        self.popup.resizable(False, False)
        self.popup.configure(bg="#3399FF")  
        label = tk.Label(
            self.popup, text="Você tem certeza de que deseja deletar este produto?", font=("Arial", 14), bg="#3399FF", fg="white", padx=10, pady=10
        )
        label.grid(row=0, column=0, columnspan=2, pady=20, padx=20)
    
        botao_voltar = ttk.Button(self.popup, text="Voltar", bootstyle=DANGER, command=self.popup.destroy, padding=(20, 10))
        botao_voltar.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    
        botao_confirmar = ttk.Button(self.popup, text="Confirmar", bootstyle=SUCCESS, command=self.confirmar_delete, padding=(20, 10))
        botao_confirmar.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
    def confirmar_delete(self):
    # Recuperar o item selecionado
        selecionados = self.treeview.get_checked()
        item_selecionado = selecionados[0]
        codigo_produto = self.treeview.item(item_selecionado)['values'][1]  
    
        produtos = Produtos()
        produtos.carregar_produtos()


        codigo_str = str(codigo_produto)
        produtos_corrigidos = {} 

        for primeiro_correcao, segundo_correcao in produtos.items():
            chave_convertida = str(primeiro_correcao)
            produtos_corrigidos[chave_convertida] = segundo_correcao


        if codigo_str in produtos_corrigidos:
            del produtos_corrigidos[codigo_str]
            with open('./src/List/produtos.json', 'w', encoding='utf-8') as arquivo_produtos:
                json.dump(produtos_corrigidos, arquivo_produtos, ensure_ascii=False, indent=4)
            tabela = Produtos()
            tabela.tabela_produtos()
            popup_delete = Popup(None, self.root)
            popup_delete.mostrar_popup("Produto deletado com sucesso!")
        else:
            popup_n_encontrado = Popup(None, self.root)
            popup_n_encontrado.mostrar_popup(f"Produto não encontrado! (Código: {codigo_produto})")
            
    def mostrar_detalhes_do_produto(self):
        busca = self.entrada_busca.get().lower()
        produtos = Produtos()
        produtos.carregar_produtos()
    
        for id, produto in produtos.items():
            if busca in produto['nome'].lower():
            # Vai abrir um popup certinho com os detalhes do produto, resolvi fazer esse com popup porque não exige funções nem nada, não há necessidade de criar tela só para ele
                popup = tk.Toplevel(self.root)
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
        popup_nenhum = Popup(None, self.root)
        popup_nenhum.mostrar_popup("Nenhum produto foi encontrado!")
        
    def cadastrar(self, entradas):
            popups = Popup()
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
                popups.mostrar_popup("Todos os campos são obrigatórios!")
            else:
                arquivo_produtos = open('./src/List/produtos.json', 'r', encoding='utf-8')
                produtos = json.load(arquivo_produtos)
                arquivo_produtos.close()
                produtos.update(dados_produto)
                arquivo = open('./src/List/produtos.json', 'w', encoding='utf-8')
                json.dump(produtos, arquivo, indent=4, ensure_ascii=False)
                arquivo.close()
                popups.mostrar_popup("Produto cadastrado com sucesso!")
        
            
class Pages:
    def __init__(self, root, nome):
        self.nome = nome
        self.root = root
        
        
    def passar_pagina(self, nome):
        self.root.destroy()
        subprocess.run(["python", f"{nome}"])
        
        
class Usuario(Pages):
    def __init__(self, root, subframe, entradas):
        self.root = root
        self.subframe = subframe
        self.entradas = entradas
        
    def cadastrar(self):
        popups = Popup(None, self.root)
        cpf = self.entradas["CPF"].get()
        username = self.entradas["Nome de Usuário"].get()
        senha = self.entradas["Senha"].get()
        nome_completo = self.entradas["Nome Completo"].get()
        dados_funcionario = { self.entradas["CPF"].get(): {
            "nome": self.entradas["Nome de Usuário"].get(),
            "senha": self.entradas["Senha"].get(),
            "nome_completo": self.entradas["Nome Completo"].get()
        }
        }
        if not cpf or not username or not senha or not nome_completo or not dados_funcionario:
            popups.mostrar_popup("Todos os campos são obrigatórios!")
        else:
            arquivo_funcionarios = open('./src/List/funcionarios.json', 'r', encoding='utf-8')
            funcionarios = json.load(arquivo_funcionarios)
            arquivo_funcionarios.close()
            funcionarios.update(dados_funcionario)
            arquivo = open('./src/List/funcionarios.json', 'w', encoding='utf-8')
            json.dump(funcionarios, arquivo, indent=4, ensure_ascii=False)
            arquivo.close()
            popups.mostrar_popup("Funcionário cadastrado com sucesso!")
            
    def verificar_usuario(self):
        arquivo_login = open('./src/List/usuario_logado.json', 'r', encoding='utf-8')
        login = json.load(arquivo_login)
        arquivo_login.close()
        usuario_logado = login["nome"]
        print("Usuário logado:", usuario_logado)
        return usuario_logado
    
    def administrador(self):
        if self.verificar_usuario() == "Administrador":
            botao_adm = ttk.Button(self.subframe, text="Cadastrar Funcionário", bootstyle=(DANGER,OUTLINE), width=30, command=lambda: Pages(self.subframe, None).passar_pagina("./src/Frames/cadastrar_funcionario.py"))
            botao_adm.grid(column=1, row=4, sticky=(S), pady=(10,0))
            
    def verificar_login(self, entrada_de_usuario, entrada_de_senha):
        popups = Popup(None, self.root)
        nome_de_usuario = entrada_de_usuario.get().strip()
        senha_do_usuario = entrada_de_senha.get().strip()
        usuario_encontrado = False
    
        if not nome_de_usuario or not senha_do_usuario:
            popups.mostrar_popup("Você não inseriu corretamente os dados!")
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
                    self.root.destroy()  
                    subprocess.run(["python", "./src/Frames/mainpage.py"])
                    break
            if not usuario_encontrado:
                popups.mostrar_popup("Seu usuário não foi encontrado no sistema.")
                
    def gerar_senha():
            pass 