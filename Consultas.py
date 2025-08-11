import psycopg2
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog

# ==============================
# Conexão com o banco
# ==============================
def conectar_bd():
    try:
        conn = psycopg2.connect(
            dbname="TP-BD1",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao banco:\n{e}")
        return None

# ==============================
# Funções utilitárias
# ==============================
def consultar(sql, params=None):
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute(sql, params if params else ())
        resultados = cur.fetchall()
        cur.close()
        return resultados
    except Exception as e:
        messagebox.showerror("Erro", f"Erro na consulta:\n{e}")
        return []

def executar(sql, params=None):
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute(sql, params if params else ())
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        messagebox.showerror("Erro", f"Erro na operação:\n{e}")
        return False

def mostrar_resultados(resultados):
    texto_area.delete(1.0, tk.END)
    if not resultados:
        texto_area.insert(tk.END, "Nenhum resultado encontrado.")
    else:
        for linha in resultados:
            texto_area.insert(tk.END, str(linha) + "\n")

# ==============================
# Consultas
# ==============================
def listar_projetos_professores():
    sql = """
        SELECT p.CodProjeto, p.NomeProjeto, pr.NomeProfessor
        FROM Projeto p
        JOIN Professor pr ON p.CodProf = pr.CodProf;
    """
    resultados = consultar(sql)
    mostrar_resultados(resultados)

def listar_oportunidades():
    sql = "SELECT IdOportunidade, CodProjeto, QtVagas FROM Oportunidade;"
    resultados = consultar(sql)
    mostrar_resultados(resultados)

def listar_alunos_por_oportunidade():
    id_op = simpledialog.askinteger("Consulta", "Digite o IdOportunidade:")
    cod_proj = simpledialog.askinteger("Consulta", "Digite o CodProjeto:")
    if id_op is None or cod_proj is None:
        return
    sql = """
        SELECT a.Matricula, a.NomeAluno
        FROM Inscreve i
        JOIN Aluno a ON i.Matricula = a.Matricula
        WHERE i.IdOportunidade = %s AND i.CodProjeto = %s;
    """
    resultados = consultar(sql, (id_op, cod_proj))
    mostrar_resultados(resultados)

def listar_contribuicoes_por_financiador():
    cod_fin = simpledialog.askinteger("Consulta", "Digite o CodFinanciador:")
    if cod_fin is None:
        return
    sql = """
        SELECT DescricaoContrib, ValorContrib
        FROM Contribuicao
        WHERE CodFinanciador = %s;
    """
    resultados = consultar(sql, (cod_fin,))
    mostrar_resultados(resultados)

# ==============================
# Atualização / Exclusão
# ==============================
def atualizar_qtd_vagas():
    id_op = simpledialog.askinteger("Atualizar Vagas", "Digite o IdOportunidade:")
    cod_proj = simpledialog.askinteger("Atualizar Vagas", "Digite o CodProjeto:")
    novo_valor = simpledialog.askinteger("Atualizar Vagas", "Digite a nova quantidade de vagas:")
    if id_op is None or cod_proj is None or novo_valor is None:
        return
    sql = """
        UPDATE Oportunidade
        SET QtVagas = %s
        WHERE IdOportunidade = %s AND CodProjeto = %s;
    """
    if executar(sql, (novo_valor, id_op, cod_proj)):
        messagebox.showinfo("Sucesso", f"Quantidade de vagas atualizada para {novo_valor}.")
        listar_oportunidades()

def excluir_inscricao():
    matricula = simpledialog.askinteger("Excluir Inscrição", "Digite a Matrícula do aluno:")
    id_op = simpledialog.askinteger("Excluir Inscrição", "Digite o IdOportunidade:")
    cod_proj = simpledialog.askinteger("Excluir Inscrição", "Digite o CodProjeto:")
    if matricula is None or id_op is None or cod_proj is None:
        return
    sql = """
        DELETE FROM Inscreve
        WHERE Matricula = %s AND IdOportunidade = %s AND CodProjeto = %s;
    """
    if executar(sql, (matricula, id_op, cod_proj)):
        messagebox.showinfo("Sucesso", "Inscrição excluída.")
        listar_alunos_por_oportunidade()

# ==============================
# Menus
# ==============================
def limpar_tela():
    for widget in root.winfo_children():
        widget.destroy()

def mostrar_menu_principal():
    limpar_tela()
    tk.Label(root, text="Menu Principal", font=("Arial", 14, "bold")).pack(pady=10)
    
    tk.Button(root, text="Consultas", width=30, command=mostrar_menu_consultas).pack(pady=5)
    tk.Button(root, text="Atualização / Exclusão", width=30, command=mostrar_menu_atualizacoes).pack(pady=5)
    tk.Button(root, text="Sair", width=30, command=sair).pack(pady=10)

def mostrar_menu_consultas():
    limpar_tela()
    tk.Label(root, text="Menu de Consultas", font=("Arial", 14, "bold")).pack(pady=10)
    
    tk.Button(root, text="Projetos e Professores", width=30, command=listar_projetos_professores).pack(pady=5)
    tk.Button(root, text="Oportunidades", width=30, command=listar_oportunidades).pack(pady=5)
    tk.Button(root, text="Alunos por Oportunidade", width=30, command=listar_alunos_por_oportunidade).pack(pady=5)
    tk.Button(root, text="Contribuições por Financiador", width=30, command=listar_contribuicoes_por_financiador).pack(pady=5)
    
    tk.Button(root, text="Voltar", width=30, command=mostrar_menu_principal).pack(pady=10)
    adicionar_area_texto()

def mostrar_menu_atualizacoes():
    limpar_tela()
    tk.Label(root, text="Menu de Atualização/Exclusão", font=("Arial", 14, "bold")).pack(pady=10)
    
    tk.Button(root, text="Atualizar QtVagas", width=30, command=atualizar_qtd_vagas).pack(pady=5)
    tk.Button(root, text="Excluir Inscrição", width=30, command=excluir_inscricao).pack(pady=5)
    
    tk.Button(root, text="Voltar", width=30, command=mostrar_menu_principal).pack(pady=10)
    adicionar_area_texto()

# ==============================
# Área de texto
# ==============================
def adicionar_area_texto():
    global texto_area
    texto_area = scrolledtext.ScrolledText(root, width=60, height=15)
    texto_area.pack(pady=10)

# ==============================
# Sair
# ==============================
def sair():
    if conn:
        conn.close()
    root.destroy()

# ==============================
# Programa principal
# ==============================
conn = conectar_bd()

root = tk.Tk()
root.title("Sistema Acadêmico - Consultas e Atualizações")

mostrar_menu_principal()

root.mainloop()
