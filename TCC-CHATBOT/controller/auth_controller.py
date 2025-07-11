# Controller para autenticação de usuários
# controller/auth_controller.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from model.usuario_model import cadastrar, buscar_usuario_por_rm_e_email, listar_todos_usuarios
from model.usuario_model import buscar_usuario_por_email  # ou outras funções
from model.usuario_model import obter_ranking  
from model.usuario_model import buscar_podio
from model.usuario_model import get_db_connection

from model import usuario_model  # Usado para chamar criar_tabela(), se necessário
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



#importações  para realizar o sistema de autenticação


auth_bp = Blueprint('auth', __name__) # começa a definir o blueprint para autenticação

# define uma chave secreta para a aplicação, que é usada para proteger as sessões do usuário



# chama a função criar_tabela do model.usuario_model, que vai criar a tabela de usuários no banco de dados se ela não existir


@auth_bp.route('/cadastro', methods=['GET', 'POST'])  # define nessa linha a rota de cadastro, que vai pegar as informações do usuário e postar no form
def cadastro():
    if request.method == "POST":
        email = request.form["email"]
        rm = request.form["rm"]
        senha = request.form["senha"]  # pega os dados do formulário de cadastro para verificar
        confirmarSenha = request.form["confirmarSenha"]  # pega a confirmação de senha do formulário
        
        if confirmarSenha != senha:  # verifica se a confirmação de senha é igual à senha
            flash("Erro, coloque a senha igual ")  # se não for igual, retorna erro

        
        if len (email ) < 10 or len (email) > 40:
            return jsonify({"erro": "Email deve ter entre 10 e 40 caracteres."})  # verifica se o email, rm e senha estão dentro dos limites de caracteres
        
            
        if len (rm) < 5 or len (rm) > 5:
            return jsonify({"erro": "RM deve ter exatamente 5 caracteres."})
        
        if len (senha) < 8 or len (senha) > 50:
            return jsonify({"erro": "Senha deve ter entre 8 e 50 caracteres."})
        
        # verifica se a senha e a confirmação de senha são iguais

        if usuario_model.buscar_usuario_por_email( email):
            print("Usuário já cadastrado com esse RM ou e-mail.")
            return redirect(url_for("auth.cadastro"))  # se o usuário já estiver cadastrado, redireciona para a página de login
        
        senha_hash = generate_password_hash(senha)
        usuario_model.cadastrar(rm, email, senha_hash) # chama a função cadastrar do model.usuario_model, que vai inserir os dados no banco de dados
        
        print("Usuário cadastrado com sucesso!") # se o usuário for cadastrado com sucesso, retorna essa mensagem
        return redirect(url_for("auth.login"))  # redireciona para a página de login após o cadastro
        
        
    return render_template("PaginaCadastro/PaginaCadastro.html") # aqui rennderiza a página de cadastro, que é a PaginaLogin.html ( Ambas estão juntas no template)

 
   


#Inicio na pagina de login rota e configuração

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        rm = request.form["rm"]
        senha = request.form["senha"]

        usuario = usuario_model.buscar_usuario_por_rm_e_email(rm, email)

        if usuario:
            senha_hash = usuario['senha']
            if isinstance(senha_hash, bytes):
                senha_hash = senha_hash.decode('utf-8')

            if check_password_hash(senha_hash, senha):
                session['usuario_id'] = usuario['id']
                session['usuario_email'] = usuario['email']
                session['usuario_rm'] = usuario['rm']
                flash("Login realizado com sucesso!")
                return redirect(url_for('auth.inicio'))

        # Se chegou aqui, login falhou

    return render_template("PaginaLogin/PaginaLogin.html")
    
# Fim da pagina de login rota e configuração

#inicio para função de logout

@auth_bp.route('/logout')
def logout():
    session.clear()  # Limpa a sessão do usuário
    flash("Você foi desconectado com sucesso.")
    
    return redirect(url_for('auth.login'))  # Redireciona para a página de login após o logout

# Ffim da pagina de inicio e configuração

#inicio para ver os users


#fim para ver os users

#inicio rota de nova senha

@auth_bp.route('/nova_senha', methods=['GET', 'POST'])  # rota definida para a página de nova senha
def nova_senha():
    email = request.args.get('email') or request.form.get('email')

    
    if request.method == 'POST':
        nova_senha = request.form['nova_senha']
        senha_hash = generate_password_hash(nova_senha)  # Gera o hash da nova senha
        usuario_model.atualizar_senha(email, senha_hash)
        # Atualiza a senha no banco de dados
        flash("Senha atualizada com sucesso!")
        return redirect(url_for('auth.login'))
    
    return render_template('PaginaNovaSenha/PaginaNovaSenha.html', email=email)  # Renderiza a página de nova senha, passando o email do usuário



# inicio rota esqueci a senha
@auth_bp.route('/esqueci_senha', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'POST':
        email = request.form['email']
        rm = request.form['rm']
        
        usuario = usuario_model.buscar_usuario_por_rm_e_email(rm, email)
        
        if not usuario: # se nao tiver user da o flash q n pode redefinir senha
            flash("Usuário não encontrado. Verifique seu RM e email.")
            return redirect(url_for('auth.esqueci_senha'))  # redireciona para a página de esqueci senha
        
        
    
        #conecta no servidor SMPTP e configura o envio de email
        
        host = "smtp.gmail.com"  # servidor SMTP do Gmail
        port = 587  # porta para envio de email
        login = "fala.i.contact@gmail.com"
        password = "veitocpyuezkjcbe"
        
        #conecta a porta e configura o server
        
        server = smtplib.SMTP(host, port)
        server.ehlo() # inicia a conexão com o servidor SMTP
        server.starttls() # inicia a conexão TLS para segurança
        server.login(login, password)  # faz o login no servidor SMTP com o email e senha
        
        #cria o link e envia o email

        banner_url = "https://i.postimg.cc/QNmfFJKx/banner.png"


        link   = f"http://localhost:5000/nova_senha?email={email}" # cria o link para a página de nova senha, passando o email do usuário
        linkSuporte = f"http://localhost:5000/inicio?email={email}"

        corpo_html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f3f0fa; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 10px; padding: 25px; box-shadow: 0px 4px 8px rgba(0,0,0,0.1);">

              <img src="{banner_url}" alt="Banner" style="width: 100%; max-height: 200px; object-fit: cover; border-radius: 8px 8px 0 0;">

              <h2 style="color: #5e35b1;">🔐 Redefinição de Senha</h2>

              <p>Olá,</p>

              <p>Recebemos uma solicitação para redefinir a sua senha em nossa plataforma. Isso pode acontecer quando você esquece a senha ou deseja reforçar a segurança da sua conta.</p>

              <p>Se foi você quem solicitou essa alteração, clique no botão abaixo para continuar com a redefinição de forma segura:</p>

              <p style="text-align: center; margin: 30px 0;">
                <a href="{link}" style="background-color: #7e57c2; color: white; padding: 14px 28px; border-radius: 6px; text-decoration: none; font-size: 16px; font-weight: bold;">
                   Redefinir Senha
                </a>
              </p>

              <p>Se você <strong>não reconhece esta solicitação</strong>, por favor entre em contato com nosso suporte imediatamente para garantir a segurança da sua conta.</p>

              <p style="text-align: center; margin: 25px 0;">
                <a href="{linkSuporte}" style="background-color: #7e57c2; color: white; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-size: 15px; font-weight: bold;">
                   Falar com o Suporte
                </a>
              </p>

              <p style="font-size: 14px; color: #666;">💡 Dica de segurança: Nunca compartilhe sua senha com ninguém e altere-a regularmente para manter sua conta protegida.</p>

              <p style="margin-top: 30px;">Atenciosamente,<br>
              <strong>Equipe de Suporte</strong><br>
              Fala.i</p>
            </div>
          </body>
        </html>
        """

        email_msg = MIMEMultipart() # cria a mensagem de email
        email_msg['From'] = login  # define o remetente do email
        email_msg['To'] = email  # define o destinatário do email
        email_msg['Subject'] = "Redefinição de Senha Fala.i" #assunto email  
        email_msg.attach(MIMEText(corpo_html, 'html'))  # anexa o corpo do email
        
        sucesso = server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string()) 
        # envia o email
        
        server.quit()
        
        if not sucesso:
            flash("Email enviado com sucesso! Verifique sua caixa de entrada.")
        else:
            flash("Erro ao enviar o email. Tente novamente mais tarde.")
    
        return redirect(url_for('auth.login'))  # redireciona para a página de esqueci senha após enviar o email
    
    return render_template('PaginaEsqueciSenha/PaginaEsqueciSenha.html')


#fim da rota esqueci senha


#inicio da pagina de inicio e configuração
@auth_bp.route('/inicio') # rota definida para a página inicial 
def inicio():
    
    if 'usuario_id' not in session:
        flash("Você precisa fazer login primeiro.")
        return redirect(url_for('auth.login'))
    
    return render_template('PaginaInicial/PaginaInicial.html', usuario_email=session ['usuario_email'], usuario_rm=session['usuario_rm'])  # renderiza a página inicial, que é a PaginaInicial.html, passando o email e o RM do usuário logado na sessão

#fim da pagina de inicio e configuração


#Começo sistema agenda

@auth_bp.route('/agenda')  # rota definida para a página de agenda
def agenda():

    return render_template('PaginaAgenda/PaginaAgenda.html')

@auth_bp.route('/tarefas', methods=['GET'])
def listar_tarefas():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM tb_tarefas ORDER BY data_tarefa, horario_tarefa')
            tarefas = cursor.fetchall()
        return jsonify(tarefas), 200
    except Exception as e:
        print("Erro ao buscar tarefas:", e)
        return jsonify({'erro': 'Erro ao buscar tarefas'}), 500
    finally:
        conn.close()

# ---------------------------
# FUNÇÃO DE ADICIONAR TAREFA
# ---------------------------
@auth_bp.route('/tarefas', methods=['POST'])
def adicionar_tarefa():
    dados = request.get_json()

    titulo = dados.get('titulo')
    descricao = dados.get('descricao')
    data_tarefa = dados.get('data_tarefa')
    horario_tarefa = dados.get('horario_tarefa')

    # Verifica se os campos obrigatórios foram enviados
    if not all([titulo, data_tarefa, horario_tarefa]):
        return jsonify({'erro': 'Campos obrigatórios faltando'}), 400

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO tb_tarefas (titulo, descricao, data_tarefa, horario_tarefa)
                VALUES (%s, %s, %s, %s)
            ''', (titulo, descricao, data_tarefa, horario_tarefa))
            conn.commit()
        return jsonify({'mensagem': 'Tarefa salva com sucesso'}), 201

    except Exception as e:
        print('Erro ao salvar tarefa:', e)
        return jsonify({'erro': 'Erro no servidor'}), 500

    finally:
        conn.close()
#fim sistema agenda


#inicio termos de uso

@auth_bp.route('/termos')  # rota definida para a página de termos de uso
def termos():
    return render_template('PaginaRanking/PaginaRanking.html')

#fim dos termos

#inicio ranking

@auth_bp.route('/ranking')
def ranking():
    ranking = obter_ranking()  # lista simples
    top3 = buscar_podio()
    restantes = ranking[3:]
    return render_template("PaginaRanking/PaginaRanking.html", ranking=ranking, top3=top3, restantes=restantes)






#fim do ranking


#inicio da minha conta

@auth_bp.route('/minha_conta')
def conta():
    return render_template('PaginaConta/PaginaConta.html')

# fim minha conta

# rota aviso

@auth_bp.route('/aviso')
def aviso():
    return render_template('aviso.html')


# aqui se inicia uma outra funçao que vai fazer a verificação e order by no ranking

def verificar():
    return None



# inicio rota nova senha

