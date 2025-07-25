import sqlite3
from bancoDados import BancoDados
import random
from aluno import Aluno

class Usuarios:
    def __init__(self, id=None, email=None, senha=None):
        self.id = id
        self.email = email
        self.senha = senha
        pass

    def logar(self, email, senha):
        con = BancoDados.conectarUsuarios()
        cur = con.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        usuario = cur.fetchone()
        con.close()
        return usuario

    def cadastrarProfessor(self, email, senha, materia):
        con = BancoDados.conectarUsuarios()
        cur = con.cursor()

        cur.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
        usuario = cur.fetchone()

        if usuario:
            usuarioId = usuario[0]
        else:
            cur.execute("INSERT INTO usuarios (email, senha) VALUES (?, ?)", (email, senha))
            usuarioId = cur.lastrowid
            con.commit()

        con.close()

        con = BancoDados.conectarProfessor()
        cur = con.cursor()

        cur.execute("SELECT id FROM professores WHERE usuario_id = ?", (usuarioId,))
        professor = cur.fetchone()

        if professor:
            con.close()
            raise ValueError("Este usuário já está vinculado a um professor.")
        else:
            cur.execute("INSERT INTO professores (nome, materia, usuario_id) VALUES (?, ?, ?)", (email, materia, usuarioId))

        con.commit()
        con.close()

    def cadastrarAluno(self, email, senha, nome):
        con = BancoDados.conectarUsuarios()
        cur = con.cursor()


        cur.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
        usuario = cur.fetchone()

        if usuario:
            usuarioId = usuario[0]
        else:
            cur.execute("INSERT INTO usuarios (email, senha) VALUES (?, ?)", (email, senha))
            usuarioId = cur.lastrowid
            con.commit()

        con.close()

        con = BancoDados.conectarAlunos()
        cur = con.cursor()

        cur.execute("SELECT id FROM alunos WHERE usuario_id = ?", (usuarioId,))
        aluno = cur.fetchone()

        if aluno:
            con.close()
            raise ValueError("Este usuário já está vinculado a um aluno.")
        else:
            matricula = Aluno.gerarMatricula()
            cur.execute("INSERT INTO alunos (nome, matricula, usuario_id) VALUES (?, ?, ?)",
                        (nome, matricula, usuarioId))

        con.commit()
        con.close()

