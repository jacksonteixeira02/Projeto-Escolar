import sqlite3
import csv

con = sqlite3.connect("escola.db")
cursor = con.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS alunos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, nota REAL NOT NULL)
""")


def cadastrarAlunoNota():
    nome = str(input("Digite o nome do aluno: ")).title()
    try:
        nota = float(input("Digite a nota do aluno: "))
        if nota < 0 or nota > 10:
            print("Nota invalida")
        else:
            cursor.execute("INSERT INTO alunos (nome, nota) VALUES (?, ?)", (nome, nota))
            con.commit()
    except ValueError:
        print("Nota Invalida")


def listarAlunos():
    dados = cursor.execute("SELECT * FROM alunos")
    for aluno in dados:
        print(f"ID: {aluno[0]} | Nome: {aluno[1]} | Nota: {aluno[2]}")

def excluirAluno():
    try:
        identidadeAluno = int(input("Informe o id do aluno: "))
    except ValueError:
            print("ID inválido, digite um número")
            return
    dados = cursor.execute("SELECT * FROM alunos")
    for aluno in dados:
        if identidadeAluno == aluno[0]:
            cursor.execute("DELETE FROM alunos WHERE ID = ?", (identidadeAluno,))
            con.commit()

def exportarAlunosCSV():
    with open("alunos.csv", "w", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["ID", "Nome", "Nota"])
        dados = cursor.execute("SELECT * FROM alunos")
        for aluno in dados:
            escritor.writerow(aluno)

def editarDados():
    try:
        editar = int(input("Informe o id do aluno: "))
    except ValueError:
            print("ID inválido, digite um número")
            return
    novoNome = input("Digite o novo nome: ").title()
    novaNota = int(input("Digite a nota editada: "))
    dados = cursor.execute("SELECT * FROM alunos")
    for aluno in dados:
        if editar == aluno[0]:
            cursor.execute("UPDATE alunos SET nome = ?, nota, ID = ? WHERE id = ?", (novoNome, novaNota, editar,))
            con.commit()


while True:
    print("===== MENU =====")
    print("1 - Cadastrar aluno")
    print("2 - Listar alunos")
    print("3 - Exportar alunos para CSV")
    print("4 - Excluir aluno")
    print("5 - Editar aluno")
    print("6 - Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrarAlunoNota()
    elif opcao == "2":
        listarAlunos()
    elif opcao == "3":
        exportarAlunosCSV()
        print("Dados exportados para alunos.csv\n")
    elif opcao == "4":
        print("Excluir aluno")
        excluirAluno()
    elif opcao == "5":
        print("Editar aluno")
        editarDados()
    elif opcao == "6":
        print("Programa fechado!")
        con.close()
        break
    else:
        print("Opção inválida! Tente novamente.\n")
