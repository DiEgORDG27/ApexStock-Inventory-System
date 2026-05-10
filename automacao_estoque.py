import mysql.connector
import pandas as pd
import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk, simpledialog, Tk
# from PIL import Image, ImageTk  # Para ícones e imagens (instalar Pillow se necessário)

ADMIN_PASSWORD = "12345"

def criar_banco_se_nao_existe():
    # Cria banco e tabela se não existirem
    conexao = None
    try:
        # Conectar sem especificar banco
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
        )
        cursor = conexao.cursor()
        
        # Criar banco
        cursor.execute("CREATE DATABASE IF NOT EXISTS empresa_db")
        
        # Usar banco
        cursor.execute("USE empresa_db")
        
        # Criar tabela
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Produto VARCHAR(255) NOT NULL,
                Quantidade INT NOT NULL,
                Valor DECIMAL(10, 2) NOT NULL,
                DataEntrada DATE NOT NULL,
                DataSaida DATE,
                Fornecedor VARCHAR(255) NOT NULL
            )
        """)
        # Ajusta coluna antiga com acento caso o banco tenha sido criado por versão anterior
        cursor.execute("SHOW COLUMNS FROM inventario LIKE 'DataSaída'")
        if cursor.fetchone():
            cursor.execute("ALTER TABLE inventario CHANGE COLUMN `DataSaída` DataSaida DATE")
        
        conexao.commit()
        print("Banco de dados e tabela criados com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao criar banco: {err}")
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()

def conectar_mysql():
    # Estabelece conexão com a base local
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='empresa_db'
    )

def enviar_dados_mysql(dados_csv, dados_excel):
    # Insere dados transformados no inventário
    conexao = None
    try:
        conexao = conectar_mysql()
        cursor = conexao.cursor()
        
        sql_query = '''
            INSERT INTO inventario (Produto, Quantidade, Valor, DataEntrada, DataSaida, Fornecedor)
            VALUES (%s, %s, %s, %s, %s, %s)
        '''

        def executar_insercao(df):
            for _, row in df.iterrows():
                valores = (
                    row['Produto'], 
                    row['Quantidade'], 
                    row['Valor'], 
                    row['Data de Entrada'], 
                    row['Data de Saída'], 
                    row['Fornecedor']
                )
                cursor.execute(sql_query, valores)

        executar_insercao(dados_csv)
        executar_insercao(dados_excel)

        conexao.commit()
        messagebox.showinfo("Sucesso", "Dados integrados ao MySQL com sucesso!")

    except mysql.connector.Error as err:
        messagebox.showerror("Erro de Banco", f"Falha na conexão ou inserção: {err}")
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()

def consultar_produtos(filtro_coluna=None, filtro_valor=None):
    # Busca produtos no banco
    conexao = None
    try:
        conexao = conectar_mysql()
        cursor = conexao.cursor()
        query = "SELECT id, Produto, Quantidade, Valor, DataEntrada, DataSaida, Fornecedor FROM inventario"
        params = []
        if filtro_coluna and filtro_valor:
            query += f" WHERE {filtro_coluna} LIKE %s"
            params.append(f"%{filtro_valor}%")
        cursor.execute(query, params)
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=['ID', 'Produto', 'Quantidade', 'Valor', 'DataEntrada', 'DataSaida', 'Fornecedor'])
        return df
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Falha na consulta: {err}")
        return pd.DataFrame()
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()

def consultar_baixo_estoque():
    # Retorna itens com estoque baixo
    conexao = None
    try:
        conexao = conectar_mysql()
        cursor = conexao.cursor()
        cursor.execute("SELECT id, Produto, Quantidade, Valor, DataEntrada, DataSaida, Fornecedor FROM inventario WHERE Quantidade < 20")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=['ID', 'Produto', 'Quantidade', 'Valor', 'DataEntrada', 'DataSaida', 'Fornecedor'])
        return df
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Falha na consulta: {err}")
        return pd.DataFrame()
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()

def consultar_fornecedores():
    # Lista fornecedores distintos
    conexao = None
    try:
        conexao = conectar_mysql()
        cursor = conexao.cursor()
        cursor.execute("SELECT DISTINCT Fornecedor FROM inventario")
        rows = cursor.fetchall()
        fornecedores = [row[0] for row in rows]
        return fornecedores
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Falha na consulta: {err}")
        return []
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()

def consultar_produtos_fornecedor(fornecedor):
    # Busca produtos do fornecedor selecionado
    return consultar_produtos('Fornecedor', fornecedor)

def editar_produto(id_produto, coluna, novo_valor):
    # Atualiza campo de um produto
    conexao = None
    try:
        conexao = conectar_mysql()
        cursor = conexao.cursor()
        query = f"UPDATE inventario SET {coluna} = %s WHERE id = %s"
        cursor.execute(query, (novo_valor, id_produto))
        conexao.commit()
        messagebox.showinfo("Sucesso", "Produto editado com sucesso!")
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Falha na edição: {err}")
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()

def exportar_csv(df, caminho):
    # Exporta para CSV
    try:
        df.to_csv(caminho, index=False)
        messagebox.showinfo("Sucesso", f"Dados exportados para {caminho}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na exportação: {e}")

def exportar_excel(df, caminho):
    # Exporta para Excel
    try:
        df.to_excel(caminho, index=False)
        messagebox.showinfo("Sucesso", f"Dados exportados para {caminho}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha na exportação: {e}")

def adicionar_produto_manual(produto, quantidade, valor, data_entrada, data_saida, fornecedor):
    # Insere produto manualmente
    conexao = None
    try:
        conexao = conectar_mysql()
        cursor = conexao.cursor()
        query = """
            INSERT INTO inventario (Produto, Quantidade, Valor, DataEntrada, DataSaida, Fornecedor)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (produto, quantidade, valor, data_entrada, data_saida, fornecedor))
        conexao.commit()
        messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Falha ao adicionar produto: {err}")
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()

def adicionar_fornecedor_manual(nome, telefone, endereco, cnpj, email):
    # Registra fornecedor em memória de teste
    # Como não temos tabela separada, podemos armazenar em inventario ou criar uma nota
    messagebox.showinfo("Info", f"Fornecedor '{nome}' cadastrado (Telefone: {telefone}, Endereço: {endereco}, CNPJ: {cnpj}, Email: {email})")
    # Futuramente, criar tabela fornecedores

def processar_dados(entry_csv, entry_excel):
    # Processa arquivos CSV e Excel
    caminho_csv = entry_csv.get()
    caminho_excel = entry_excel.get()

    if not caminho_csv or not caminho_excel:
        messagebox.showwarning("Atenção", "Por favor, selecione ambos os arquivos antes de processar.")
        return

    try:
        df_csv = pd.read_csv(caminho_csv)
        df_excel = pd.read_excel(caminho_excel)

        df_csv = df_csv.drop_duplicates()
        df_excel = df_excel.drop_duplicates()

        for df in [df_csv, df_excel]:
            df['Data de Entrada'] = pd.to_datetime(df['Data de Entrada']).dt.date
            df['Data de Saída'] = pd.to_datetime(df['Data de Saída']).dt.date

        colunas_necessarias = ['Produto', 'Quantidade', 'Valor', 'Data de Entrada', 'Data de Saída', 'Fornecedor']
        
        dados_csv = df_csv[colunas_necessarias]
        dados_excel = df_excel[colunas_necessarias]

        enviar_dados_mysql(dados_csv, dados_excel)

    except Exception as e:
        messagebox.showerror("Erro de Processamento", f"Falha ao ler ou transformar dados: {e}")

def selecionar_arquivo_csv(entry):
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
    if caminho:
        entry.delete(0, ctk.END)
        entry.insert(0, caminho)

def selecionar_arquivo_excel(entry):
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])
    if caminho:
        entry.delete(0, ctk.END)
        entry.insert(0, caminho)

def selecionar_caminho_exportar(extensao):
    return filedialog.asksaveasfilename(defaultextension=extensao, filetypes=[(f"Arquivos {extensao.upper()}", f"*.{extensao}")])

def criar_janela_popup(titulo, largura, altura):
    # Cria janela filha centralizada
    janela = ctk.CTkToplevel(app)
    janela.title(titulo)
    janela.resizable(False, False)
    app.update_idletasks()
    x = app.winfo_x() + (app.winfo_width() // 2) - (largura // 2)
    y = app.winfo_y() + (app.winfo_height() // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")
    janela.transient(app)
    return janela

def atualizar_tabela(tree, df, mostrar_status=False):
    # Atualiza tabela de itens
    for item in tree.get_children():
        tree.delete(item)
    if not df.empty:
        if mostrar_status:
            columns = ['Status'] + list(df.columns)
        else:
            columns = list(df.columns)
        tree["columns"] = columns
        tree["show"] = "headings"
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100 if col != 'Status' else 50)
        for _, row in df.iterrows():
            values = list(row)
            if mostrar_status and 'Quantidade' in df.columns:
                quantidade = row['Quantidade']
                if quantidade == 0:
                    values = ['🚨'] + values
                elif quantidade < 20:
                    values = ['⚠️'] + values
                else:
                    values = ['✅'] + values
            tree.insert("", "end", values=values)

def pesquisar_produtos(entry_pesquisa, combo_filtro, tree):
    filtro_valor = entry_pesquisa.get()
    filtro_coluna = combo_filtro.get()
    if filtro_coluna == "Nenhum":
        df = consultar_produtos()
    else:
        df = consultar_produtos(filtro_coluna, filtro_valor)
    atualizar_tabela(tree, df)

def abrir_janela_importar_exportar():
    # Abre painel de importação/exportação
    janela = criar_janela_popup("Importar/Exportar", 400, 300)
    
    ctk.CTkLabel(janela, text="📥 Importar Dados", font=("Arial", 14, "bold")).pack(pady=10)
    
    # Campos para importar
    entry_csv = ctk.CTkEntry(janela, width=300, placeholder_text="Arquivo CSV...")
    entry_csv.pack(pady=5)
    ctk.CTkButton(janela, text="Buscar CSV", command=lambda: selecionar_arquivo_csv(entry_csv)).pack(pady=5)
    
    entry_excel = ctk.CTkEntry(janela, width=300, placeholder_text="Arquivo Excel...")
    entry_excel.pack(pady=5)
    ctk.CTkButton(janela, text="Buscar Excel", command=lambda: selecionar_arquivo_excel(entry_excel)).pack(pady=5)
    
    ctk.CTkButton(janela, text="Processar e Enviar", command=lambda: processar_dados(entry_csv, entry_excel)).pack(pady=10)
    
    ctk.CTkLabel(janela, text="📤 Exportar Dados", font=("Arial", 14, "bold")).pack(pady=10)
    ctk.CTkButton(janela, text="Exportar para CSV", command=lambda: exportar_csv(consultar_produtos(), selecionar_caminho_exportar("csv"))).pack(pady=5)
    ctk.CTkButton(janela, text="Exportar para Excel", command=lambda: exportar_excel(consultar_produtos(), selecionar_caminho_exportar("xlsx"))).pack(pady=5)

def abrir_adicionar_produto():
    # Abre formulário de novo produto
    janela = criar_janela_popup("Adicionar Produto", 400, 600)
    
    ctk.CTkLabel(janela, text="Produto:").pack(pady=5)
    entry_produto = ctk.CTkEntry(janela)
    entry_produto.pack(pady=5)
    
    ctk.CTkLabel(janela, text="Quantidade:").pack(pady=5)
    entry_quantidade = ctk.CTkEntry(janela)
    entry_quantidade.pack(pady=5)
    
    ctk.CTkLabel(janela, text="Valor:").pack(pady=5)
    entry_valor = ctk.CTkEntry(janela)
    entry_valor.pack(pady=5)
    
    ctk.CTkLabel(janela, text="Data Entrada (YYYY-MM-DD):").pack(pady=5)
    entry_data_entrada = ctk.CTkEntry(janela)
    entry_data_entrada.pack(pady=5)
    
    ctk.CTkLabel(janela, text="Data Saída (opcional):").pack(pady=5)
    entry_data_saida = ctk.CTkEntry(janela)
    entry_data_saida.pack(pady=5)
    
    ctk.CTkLabel(janela, text="Fornecedor:").pack(pady=5)
    entry_fornecedor = ctk.CTkEntry(janela)
    entry_fornecedor.pack(pady=5)
    
    def salvar():
        try:
            produto = entry_produto.get()
            quantidade = int(entry_quantidade.get())
            valor = float(entry_valor.get())
            data_entrada = entry_data_entrada.get()
            data_saida = entry_data_saida.get() or None
            fornecedor = entry_fornecedor.get()
            adicionar_produto_manual(produto, quantidade, valor, data_entrada, data_saida, fornecedor)
            janela.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Dados inválidos! Verifique os campos.")
    
    ctk.CTkButton(janela, text="Salvar", command=salvar).pack(pady=20)

def abrir_edicao_fornecedor(fornecedor):
    senha = simpledialog.askstring("Senha Admin", "Digite a senha de admin:", show='*')
    if not senha:
        return
    if senha != ADMIN_PASSWORD:
        messagebox.showerror("Erro", "Senha incorreta!")
        return
    
    df = consultar_produtos_fornecedor(fornecedor)
    if df.empty:
        messagebox.showinfo("Info", "Nenhum produto encontrado para este fornecedor.")
        return
    
    # Criar nova janela para edição
    edit_window = criar_janela_popup(f"Editar Produtos - {fornecedor}", 900, 600)
    
    # Dados do fornecedor (simulados)
    fornecedor_data = {
        "Nome": fornecedor,
        "Telefone": "(11) 99999-9999",  # Simulado
        "Endereço": "Rua Exemplo, 123 - São Paulo, SP",  # Simulado
        "CNPJ": "12.345.678/0001-99",  # Simulado
        "Email": "contato@exemplo.com"  # Simulado
    }
    
    # Frame para dados do fornecedor
    fornecedor_frame = ctk.CTkFrame(edit_window)
    fornecedor_frame.pack(fill="x", padx=10, pady=10)
    
    ctk.CTkLabel(fornecedor_frame, text=f"Dados do Fornecedor: {fornecedor}", font=("Arial", 14, "bold")).pack(pady=5)
    for key, value in fornecedor_data.items():
        ctk.CTkLabel(fornecedor_frame, text=f"{key}: {value}").pack(anchor="w", padx=10)
    
    # Tabela de produtos
    tree = ttk.Treeview(edit_window)
    tree.pack(fill="both", expand=True, padx=10, pady=10)
    atualizar_tabela(tree, df)
    
    def on_double_click(event):
        item = tree.selection()[0]
        col = tree.identify_column(event.x)
        col_index = int(col.replace('#', '')) - 1
        coluna = df.columns[col_index]
        id_produto = tree.item(item, "values")[0]
        novo_valor = simpledialog.askstring("Editar", f"Novo valor para {coluna}:", initialvalue=tree.item(item, "values")[col_index])
        if novo_valor:
            editar_produto(id_produto, coluna, novo_valor)
            df.at[int(id_produto)-1, coluna] = novo_valor  # Ajustar índice
            atualizar_tabela(tree, df)
    
    tree.bind("<Double-1>", on_double_click)

def abrir_adicionar_fornecedor():
    # Abre formulário de fornecedor
    janela = criar_janela_popup("Adicionar Fornecedor", 400, 450)
    
    ctk.CTkLabel(janela, text="Nome:").pack(pady=5)
    entry_nome = ctk.CTkEntry(janela)
    entry_nome.pack(pady=5)
    
    ctk.CTkLabel(janela, text="Telefone:").pack(pady=5)
    entry_telefone = ctk.CTkEntry(janela)
    entry_telefone.pack(pady=5)
    
    ctk.CTkLabel(janela, text="Endereço:").pack(pady=5)
    entry_endereco = ctk.CTkEntry(janela)
    entry_endereco.pack(pady=5)
    
    ctk.CTkLabel(janela, text="CNPJ:").pack(pady=5)
    entry_cnpj = ctk.CTkEntry(janela)
    entry_cnpj.pack(pady=5)
    
    ctk.CTkLabel(janela, text="Email:").pack(pady=5)
    entry_email = ctk.CTkEntry(janela)
    entry_email.pack(pady=5)
    
    def salvar():
        nome = entry_nome.get()
        telefone = entry_telefone.get()
        endereco = entry_endereco.get()
        cnpj = entry_cnpj.get()
        email = entry_email.get()
        adicionar_fornecedor_manual(nome, telefone, endereco, cnpj, email)
        janela.destroy()
    
    ctk.CTkButton(janela, text="Salvar", command=salvar).pack(pady=20)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("ApexStock - Sistema de Inventário Avançado")
app.geometry("1000x700")

# Estilo para tabelas
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", 
                background="#2b2b2b",
                foreground="white", 
                rowheight=25,
                fieldbackground="#2b2b2b",
                borderwidth=1,
                relief="solid")
style.map('Treeview', background=[('selected', '#3478c5')])
style.configure("Treeview.Heading", 
                background="#1f1f1f",
                foreground="white",
                relief="flat",
                borderwidth=1)
style.map("Treeview.Heading", background=[('active', '#1f1f1f')])
style.configure("Treeview.Item", borderwidth=1, relief="solid")

# Ícone do app (criar um ícone simples ou usar padrão)
# app.iconbitmap('icone.ico')  # Futuramente adicionar ícone
# Para ícone na taskbar, usar app.iconphoto(False, tk.PhotoImage(file='icone.png'))

# Header com logo e ícone importar/exportar
header_frame = ctk.CTkFrame(app, height=60)
header_frame.pack(fill="x", padx=20, pady=(20,10))

logo_label = ctk.CTkLabel(header_frame, text="🛒 ApexStock", font=("Arial", 24, "bold"))
logo_label.pack(side="left", padx=10)

# Botões no header
btn_frame = ctk.CTkFrame(header_frame)
btn_frame.pack(side="right", padx=10)

import_export_btn = ctk.CTkButton(btn_frame, text="📥📤", width=60, height=40, command=abrir_janela_importar_exportar)
import_export_btn.pack(side="left", padx=5)

add_produto_btn = ctk.CTkButton(btn_frame, text="➕ Produto", height=40, command=abrir_adicionar_produto)
add_produto_btn.pack(side="left", padx=5)

tabview = ctk.CTkTabview(app, width=950, height=600)
tabview.pack(pady=10, padx=20, fill="both", expand=True)

# Aba Visualizar
tab_visualizar = tabview.add("🔍 Visualizar Inventário")
ctk.CTkLabel(tab_visualizar, text="Visualizar e Pesquisar Produtos", font=("Arial", 16, "bold")).pack(pady=10)

frame_pesquisa = ctk.CTkFrame(tab_visualizar)
frame_pesquisa.pack(pady=10, padx=10, fill="x")

ctk.CTkLabel(frame_pesquisa, text="Filtrar por:").grid(row=0, column=0, padx=5)
combo_filtro = ctk.CTkComboBox(frame_pesquisa, values=["Nenhum", "Produto", "Fornecedor", "DataEntrada"])
combo_filtro.grid(row=0, column=1, padx=5)
entry_pesquisa = ctk.CTkEntry(frame_pesquisa, width=300, placeholder_text="Digite o termo de pesquisa...")
entry_pesquisa.grid(row=0, column=2, padx=5)
ctk.CTkButton(frame_pesquisa, text="Pesquisar", command=lambda: pesquisar_produtos(entry_pesquisa, combo_filtro, tree_visualizar)).grid(row=0, column=3, padx=5)

tree_visualizar = ttk.Treeview(tab_visualizar)
tree_visualizar.pack(fill="both", expand=True, padx=10, pady=10)
df_inicial = consultar_produtos()
atualizar_tabela(tree_visualizar, df_inicial)

# Aba Baixo Estoque
tab_baixo = tabview.add("⚠️ Baixo Estoque")
ctk.CTkLabel(tab_baixo, text="Produtos com Estoque Baixo", font=("Arial", 16, "bold")).pack(pady=10)
tree_baixo = ttk.Treeview(tab_baixo)
tree_baixo.pack(fill="both", expand=True, padx=10, pady=10)
df_baixo = consultar_baixo_estoque()
atualizar_tabela(tree_baixo, df_baixo, mostrar_status=True)

# Aba Fornecedores
tab_fornecedores = tabview.add("🏢 Fornecedores")
ctk.CTkLabel(tab_fornecedores, text="Cadastro e Gestão de Fornecedores", font=("Arial", 16, "bold")).pack(pady=10)

# Lista de fornecedores
fornecedor_frame = ctk.CTkScrollableFrame(tab_fornecedores)
fornecedor_frame.pack(fill="both", expand=True, padx=10, pady=10)

fornecedores = consultar_fornecedores()
for fornecedor in fornecedores:
    btn = ctk.CTkButton(fornecedor_frame, text=fornecedor, command=lambda f=fornecedor: abrir_edicao_fornecedor(f))
    btn.pack(pady=2, fill="x")

# Botão para adicionar fornecedor
ctk.CTkButton(tab_fornecedores, text="➕ Adicionar Fornecedor", command=abrir_adicionar_fornecedor).pack(pady=10)

# Loop principal
if __name__ == "__main__":
    criar_banco_se_nao_existe()
    app.mainloop()