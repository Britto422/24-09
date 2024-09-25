import tkinter as tk
from tkinter import ttk
import sqlite3

# Funções para manipulação do banco de dados
def conectar_bd():
    conn = sqlite3.connect('cidades.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS cidades (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        populacao INTEGER NOT NULL)''')
    conn.commit()
    return conn

def inserir_cidade(nome, populacao):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO cidades (nome, populacao) VALUES (?, ?)', (nome, populacao))
    conn.commit()
    conn.close()
    atualizar_treeview()

def atualizar_treeview():
    for row in tree.get_children():
        tree.delete(row)
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cidades')
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)
    conn.close()

def preencher_formulario(event):
    item_selecionado = tree.selection()[0]
    valores = tree.item(item_selecionado, 'values')
    entry_nome.delete(0, tk.END)
    entry_nome.insert(0, valores[1])
    entry_populacao.delete(0, tk.END)
    entry_populacao.insert(0, valores[2])

# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Cadastro de Cidades")

# Campos de formulário
tk.Label(root, text="Nome da Cidade").grid(row=0, column=0)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1)

tk.Label(root, text="População").grid(row=1, column=0)
entry_populacao = tk.Entry(root)
entry_populacao.grid(row=1, column=1)

# TreeView para exibir as cidades
tree = ttk.Treeview(root, columns=('ID', 'Nome', 'População'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Nome', text='Nome')
tree.heading('População', text='População')
tree.grid(row=3, column=0, columnspan=2)

tree.bind("<ButtonRelease-1>", preencher_formulario)

# Botões
tk.Button(root, text="Incluir", command=lambda: inserir_cidade(entry_nome.get(), entry_populacao.get())).grid(row=4, column=0)
tk.Button(root, text="Alterar").grid(row=4, column=1)
tk.Button(root, text="Excluir").grid(row=4, column=2)

atualizar_treeview()

root.mainloop()