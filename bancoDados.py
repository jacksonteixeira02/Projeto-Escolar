import sqlite3
class BancoDados:
    def __init__(self):
        pass

    @staticmethod
    def conectar():
        return sqlite3.connect("bancoDados/escola.db")

    @staticmethod
    def conectarAlunos():
        return sqlite3.connect("bancoDados/alunos.db")

    @staticmethod
    def conectarUsuarios():
        return sqlite3.connect("bancoDados/usuarios.db")

    @staticmethod
    def conectarProfessor():
        return sqlite3.connect("bancoDados/professor.db")
