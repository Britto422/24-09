import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Criação da tabela de usuários, se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
''')
conn.commit()


# Função para atualizar o Treeview com os dados do banco
def atualizar_treeview():
    # Limpa o Treeview antes de atualizá-lo
    for item in tree.get_children():
        tree.delete(item)

    # Consulta os usuários no banco de dados
    cursor.execute("SELECT * FROM usuarios")
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)


# Função para inserir um novo usuário
def inserir_usuario():
    nome = entry_nome.get()
    email = entry_email.get()

    if nome and email:
        try:
            cursor.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
            conn.commit()
            atualizar_treeview()
            limpar_campos()
            messagebox.showinfo("Sucesso", "Usuário inserido com sucesso!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "O e-mail já está cadastrado.")
    else:
        messagebox.showwarning("Atenção", "Preencha todos os campos.")


# Função para preencher os campos com os dados do registro selecionado
def selecionar_usuario(event):
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        record = item['values']
        entry_id.config(state='normal')
        entry_id.delete(0, tk.END)
        entry_id.insert(0, record[0])
        entry_id.config(state='readonly')
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, record[1])
        entry_email.delete(0, tk.END)
        entry_email.insert(0, record[2])


# Função para alterar um usuário existente
def alterar_usuario():
    id_usuario = entry_id.get()
    nome = entry_nome.get()
    email = entry_email.get()

    if id_usuario and nome and email:
        cursor.execute("UPDATE usuarios SET nome = ?, email = ? WHERE id = ?", (nome, email, id_usuario))
        conn.commit()
        atualizar_treeview()
        limpar_campos()
        messagebox.showinfo("Sucesso", "Usuário alterado com sucesso!")
    else:
        messagebox.showwarning("Atenção", "Selecione um usuário para alterar.")


# Função para excluir um usuário
def excluir_usuario():
    id_usuario = entry_id.get()

    if id_usuario:
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
        conn.commit()
        atualizar_treeview()
        limpar_campos()
        messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
    else:
        messagebox.showwarning("Atenção", "Selecione um usuário para excluir.")


# Função para limpar os campos do formulário
def limpar_campos():
    entry_id.config(state='normal')
    entry_id.delete(0, tk.END)
    entry_id.config(state='readonly')
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)


# Interface gráfica
root = tk.Tk()
root.title("Cadastro de Usuários")

# Labels e campos de entrada
label_id = tk.Label(root, text="ID:")
label_id.grid(row=0, column=0)
entry_id = tk.Entry(root, state='readonly')
entry_id.grid(row=0, column=1)

label_nome = tk.Label(root, text="Nome:")
label_nome.grid(row=1, column=0)
entry_nome = tk.Entry(root)
entry_nome.grid(row=1, column=1)

label_email = tk.Label(root, text="Email:")
label_email.grid(row=2, column=0)
entry_email = tk.Entry(root)
entry_email.grid(row=2, column=1)

# Botões
btn_inserir = tk.Button(root, text="Inserir", command=inserir_usuario)
btn_inserir.grid(row=3, column=0)

btn_alterar = tk.Button(root, text="Alterar", command=alterar_usuario)
btn_alterar.grid(row=3, column=1)

btn_excluir = tk.Button(root, text="Excluir", command=excluir_usuario)
btn_excluir.grid(row=3, column=2)

btn_limpar = tk.Button(root, text="Limpar", command=limpar_campos)
btn_limpar.grid(row=3, column=3)

# Treeview para exibir os dados dos usuários
tree = ttk.Treeview(root, columns=('ID', 'Nome', 'Email'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Nome', text='Nome')
tree.heading('Email', text='Email')
tree.grid(row=4, column=0, columnspan=4)

# Evento de seleção no Treeview
tree.bind('<<TreeviewSelect>>', selecionar_usuario)

# Carregar os dados iniciais
atualizar_treeview()

# Inicializa a interface gráfica
root.mainloop()

# Fechar a conexão com o banco de dados ao encerrar o programa
conn.close()