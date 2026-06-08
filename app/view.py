from app import app
from flask import render_template, request, jsonify
import os
import sqlite3
import bcrypt

# Database path same as created in app.__init__
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
db_path = os.path.join(project_root, 'base', 'barbearia.db')


@app.route("/", methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route("/create")
def create():
    return "create"

@app.route("/update")
def update():
    return "update"

@app.route("/delete")
def delete():
    return "delete"


@app.route('/usuarios', methods=['POST'])
def create_usuario():
    """Cria um usuário. Aceita JSON ou form-data com campos: nome, email, senha."""
    data = request.get_json(silent=True) or request.form
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    if not all([nome, email, senha]):
        return jsonify({'error': 'nome, email e senha são obrigatórios'}), 400

    # Hash da senha usando bcrypt
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha_hash))
        conn.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    return jsonify({'status': 'ok', 'nome': nome, 'email': email}), 201


@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    """Lista todos os usuários sem exibir senhas."""
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT nome, email FROM usuarios')
        rows = c.fetchall()
        usuarios = [{'nome': row[0], 'email': row[1]} for row in rows]
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    return jsonify(usuarios), 200


@app.route('/login', methods=['POST'])
def login():
    """Autentica um usuário. Aceita JSON ou form-data com campos: email, senha."""
    data = request.get_json(force=True, silent=False) if request.is_json else request.form
    email = data.get('email')
    senha = data.get('senha')

    if not all([email, senha]):
        return jsonify({'error': 'email e senha são obrigatórios'}), 400

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT nome, senha FROM usuarios WHERE email = ?', (email,))
        row = c.fetchone()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    if not row:
        return jsonify({'error': 'email ou senha inválidos'}), 401

    nome, senha_hash = row
    try:
        if bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8')):
            return jsonify({'status': 'ok', 'nome': nome, 'email': email}), 200
        else:
            return jsonify({'error': 'email ou senha inválidos'}), 401
    except ValueError:
        return jsonify({'error': 'email ou senha inválidos'}), 401

