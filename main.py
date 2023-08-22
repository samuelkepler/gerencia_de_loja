from flask import Flask, request, render_template, redirect
import sqlite3
from models.produto import Produto

app = Flask(__name__)

conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        quilos REAL,
        quantidade INTEGER,
        preco REAL
    )
''')
conn.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    with sqlite3.connect('estoque.db') as conn:
        cursor = conn.cursor()

        if request.method == 'POST':
            nome = request.form['nome']
            quilos = float(request.form['quilos'])
            quantidade = int(request.form['quantidade'])
            preco = float(request.form['preco'])

            novo_produto = Produto(nome, quilos, quantidade, preco)

            cursor.execute('INSERT INTO produtos (nome, quilos, quantidade, preco) VALUES (?, ?, ?, ?)',
                           (novo_produto.nome, novo_produto.quilos, novo_produto.quantidade, novo_produto.preco))
            conn.commit()

        cursor.execute('SELECT * FROM produtos')
        produtos = cursor.fetchall()

    return render_template('formulario.html', produtos=produtos)

@app.route('/editar/<int:produto_id>', methods=['GET', 'POST'])
def editar_produto(produto_id):
    with sqlite3.connect('estoque.db') as conn:
        cursor = conn.cursor()

        if request.method == 'POST':
            # Processar a atualização do produto
            novo_nome = request.form['novo_nome']
            novo_quilos = float(request.form['novo_quilos'])
            nova_quantidade = int(request.form['nova_quantidade'])
            novo_preco = float(request.form['novo_preco'])

            cursor.execute('UPDATE produtos SET nome=?, quilos=?, quantidade=?, preco=? WHERE id=?',
                           (novo_nome, novo_quilos, nova_quantidade, novo_preco, produto_id))
            conn.commit()

            return redirect('/')

        cursor.execute('SELECT * FROM produtos WHERE id=?', (produto_id,))
        produto = cursor.fetchone()

    return render_template('editar.html', produto=produto)

@app.route('/excluir/<int:produto_id>')
def excluir_produto(produto_id):
    with sqlite3.connect('estoque.db') as conn:
        cursor = conn.cursor()

        cursor.execute('DELETE FROM produtos WHERE id=?', (produto_id,))
        conn.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
