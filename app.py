from flask import Flask, render_template, request, redirect, url_for, flash
import urllib.request, json
from flask_sqlalchemy import SQLAlchemy

#nome do aplicativo
#chamada do modulo do flask passando um parametro para ele 
 
app = Flask(__name__)

app.secret_key = "\x15\x13\xe1\xf1'\x96\x93\x8f\xd0\x1cC?\xfcS\x82\xbf" 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lol.sqlite3'

db = SQLAlchemy()

db.init_app(app)

nome = []
registros = []

class personagem(db.Model):
	nome = db.Column(db.String(15), primary_key=True)
	descricao = db.Column(db.String(100))
	tipo = db.Column(db.String(10))
	valor = db.Column(db.Integer)

	def __init__(self, nome, descricao, tipo, valor):    
            self.nome = nome
            self.descricao = descricao
            self.valor = valor
            self.tipo = tipo

#criação da rota que será seguida
#sendo a principal coloca-se apenas o /
@app.route('/', methods= ["Get" , "Post"])
#cria-se a função principal que será processada na rota criada 
def principal():
    #return ("Hello World !")
    if request.method == "POST":
        if request.form.get("personagem") and request.form.get("lane"):
            registros.append({"personagem": request.form.get("personagem"), "lane": request.form.get("lane")})
    return render_template("index.html", registros=registros)
#para a execução é necessário a criação de uma variavel ambiente ex: set FLASK_APP = nome do arquivo que deseja rodar
#ao final 'flask run
#se o ambiente for de 'produção' deverá 'set FLAK_ENV=development'
#deve-se colocar a variavel fora da função para que assim ela não seja atualizada localmente 

#criando a rota '/sobre'
@app.route('/sobre', methods = ["GET", "POST"])
def sobre():
    #nome = {"Fernando Augusto":"Lider", "Bruninho":"Braço",
    #        "Markley":"Pensador", "Gay-OSO":"Inovador",
    #        "Relampago Carlinhos":"Cabeça","Matheus":"Coração"}
    #nome = ["Fernando Augusto" ,"Bruninho", "Markley", "Gay-OSO", "Relampago Carlinhos" ]
    #forma de receber os dados que serão inseridos pelos usuarios 
    if request.method == "POST":
        if request.form.get("nome"):
           nome.append(request.form.get("nome"))
    return render_template("sobre.html",nome=nome)

@app.route('/filmes/<propriedade>')
def filmes(propriedade):

    if propriedade == 'populares':
        url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=8a4f5803f0e6eb7fc498fbc059904d3f"
    elif propriedade == 'kids':
        url = "https://api.themoviedb.org/3/discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&api_key=8a4f5803f0e6eb7fc498fbc059904d3f"
    elif propriedade == '2010':
        url = "https://api.themoviedb.org/3/discover/movie?primary_release_year=2010&sort_by=vote_average.desc&api_key=8a4f5803f0e6eb7fc498fbc059904d3f"
    elif propriedade == 'drama':
        url =  "https://api.themoviedb.org/3/discover/movie?with_genres=18&sort_by=vote_average.desc&vote_count.gte=10&api_key=8a4f5803f0e6eb7fc498fbc059904d3f"
    elif propriedade == 'tom_cruise':        
        url = "https://api.themoviedb.org/3/discover/movie?with_genres=878&with_cast=500&sort_by=vote_average.desc&api_key=8a4f5803f0e6eb7fc498fbc059904d3f"
    resposta = urllib.request.urlopen(url)

    dados = resposta.read()

    jsondata = json.loads(dados)

    return render_template("filmes.html", filmes=jsondata['results'])

@app.route('/personagens')
def personagens():
    return render_template("personagens.html", personagens=personagem.query.all())

@app.route('/cria_personagem', methods=["GET" , "POST"])
def cria_personagem():
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    tipo = request.form.get('tipo')
    valor = request.form.get('valor')

    if request.method == 'POST':
        if not nome or not descricao or not tipo or not valor:
            flash("Preencha todos os campos do Formulario","erro")
        else:
            personagens = personagem(nome, descricao, tipo, valor)
            db.session.add(personagens)
            db.session.commit()
            return redirect(url_for('personagens'))
    return render_template("novo_personagem.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)