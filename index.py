import os, psycopg2
from flask import Flask, render_template, redirect, request, session, flash, url_for
from asseclas import usuario, objeto
from dao import ComentarioDao, UsuarioDao

app = Flask(__name__)
app.secret_key = 'afnj98ejfiu'

lista = []

db = psycopg2.connect(os.environ["DATABASE_URL"])
comentario_dao = ComentarioDao(db)
usuario_dao = UsuarioDao(db)
cursor = db.cursor()
cursor.execute('USE comentarios')
#cursor.execute('DROP TABLE objeto')
#cursor.execute('DROP TABLE usuario')
#cursor.execute('''CREATE TABLE usuario (
#      id SERIAL NOT NULL,
#      nome varchar(20) NOT NULL,
#      coduser varchar(12) NOT NULL PRIMARY KEY,
#      senha varchar(12) NOT NULL);''')
#cursor.execute('''CREATE TABLE objeto (
#    id SERIAL NOT NULL PRIMARY KEY,
#    coduser varchar(12) NOT NULL,
#    comentario varchar(40) NOT NULL,
#    foreign key (coduser) references usuario(coduser));''')
#cursor.execute('''INSERT INTO usuario (id, nome, coduser, senha) VALUES (3, 'Demetrio', 'demetrio', 'teste123');''')
#db.commit()


@app.route('/')
def index():
    lista = comentario_dao.listar()
    return render_template('index.html', objetos=lista)

@app.route('/comentario')
def comentario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('comentar')))
    usuario = usuario_dao.buscar_por_coduser(session['usuario_logado'])
    return render_template('comentario.html', titulo='Comentário', usuarionome=(usuario.nome))

@app.route('/comentar', methods=['POST',])
def comentar():
    usuario = usuario_dao.buscar_por_coduser(session['usuario_logado'])
    comentario = request.form['comentario']
    conjunto = objeto(coduser=usuario.coduser, comentario=comentario)
    comentario_dao.salvar(conjunto)
    return redirect(url_for('index'))

@app.route('/login')
def login():
     return render_template ('login.html')
 
@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = usuario_dao.buscar_por_coduser(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.coduser
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else :
        flash('Não logado, tente de novo!')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

app.run(debug=True, host='192.168.163.126')