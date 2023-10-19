from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify

class Fornecedor:
    def __init__(self, nome, documento):
        self.nome = nome
        self.documento = documento

    def to_dict(self):
        return {
            "nome": self.nome,
            "documento": self.documento
        }

fornecedor1 = Fornecedor('EmpresaA', '123456')
fornecedor2 = Fornecedor('EmpresaB', '786543')
fornecedor3 = Fornecedor('EmpresaC', '234567')
fornecedor4 = Fornecedor('EmpresaD', '342190')
fornecedor5 = Fornecedor('EmpresaE', '789412')
fornecedor6 = Fornecedor('EmpresaF', '987548')
listaFornecedores = [fornecedor1, fornecedor2, fornecedor3, fornecedor4, fornecedor5, fornecedor6]

app = Flask(__name__)
app.secret_key='modalgr'

@app.route('/')
def index():
    return render_template('lista.html', titulo='Fornecedores: ', fornecedores=listaFornecedores)

@app.route('/fornecedores')
def getFornecedores():
    queryString = request.args.get('query')
    fornecedorEncontrado = []
    for fornecedor in listaFornecedores:
        if fornecedor.documento == queryString:
            fornecedorEncontrado.append(fornecedor.to_dict())

    if queryString and fornecedorEncontrado:
        return jsonify({
                "message": "Fornecedor encontrado",
                "data": fornecedorEncontrado
            })

    if queryString and not fornecedorEncontrado:
        return jsonify({
            "message": "Nenhum fornecedor encontrado com esse documento",
            "data": fornecedorEncontrado
        })

    fornecedores = [fornecedor.to_dict() for fornecedor in listaFornecedores]
    if fornecedores:
        return jsonify({
                "message": "Fornecedores encontrados",
                "data": fornecedores
            })
    else:
        return jsonify({
            "message": "Nenhum fornecedor encontrado",
            "data": fornecedores
        })

@app.route('/novo')
def novoFornecedor():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        #return redirect('/login?proxima=novo') #ANTES
        return redirect(url_for('login', proxima='novo')) # DEPOIS
    return render_template('adicionaFornecedor.html', titulo='Cadastrar fornecedor: ')

@app.route('/criar', methods=['POST',])
def criarFornecedor():
    nome = request.form['nome']
    documento = request.form['documento']
    fornecedor = Fornecedor(nome, documento)
    listaFornecedores.append(fornecedor)
    session['novo_fornecedor'] = request.form['nome']
    flash(session['novo_fornecedor'] + ' adicionado com sucesso!')
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    if not proxima:
        return render_template('login.html')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['senha'] == '123456':
        session['usuario_logado'] = request.form['usuario']
        flash(session['usuario_logado'] + ' logado com sucesso!')
        proximaPagina = request.form['proxima']
        if not proximaPagina:
            return redirect(url_for('index'))
        return redirect (proximaPagina)
    else:
        flash('Usuário ou senha incorreta')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuário deslogado!')
    return redirect(url_for('index'))

app.run(debug=True)