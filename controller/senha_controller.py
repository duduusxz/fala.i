from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from model import usuario_model
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

senha_bp = Blueprint('senha', __name__)

# Rota de nova senha
@senha_bp.route('/nova_senha', methods=['GET', 'POST'])
def nova_senha():
    email = request.args.get('email') or request.form.get('email')
    if request.method == 'POST':
        nova_senha = request.form['nova_senha']
        senha_hash = generate_password_hash(nova_senha)
        usuario_model.atualizar_senha(email, senha_hash)
        flash("Senha atualizada com sucesso!")
        return redirect(url_for('login.login'))
    return render_template('PaginaNovaSenha/PaginaNovaSenha.html', email=email)


# Rota esqueci senha
@senha_bp.route('/esqueci_senha', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'POST':
        email = request.form['email']
        rm = request.form['rm']
        usuario = usuario_model.buscar_usuario_por_rm_e_email(rm, email)

        if not usuario:
            flash("Usuário não encontrado. Verifique seu RM e email.")
            return redirect(url_for('senha.esqueci_senha'))

        # Configura envio de e-mail
        host = "smtp.gmail.com"
        port = 587
        login = "fala.i.contact@gmail.com"
        password = "veitocpyuezkjcbe"

        server = smtplib.SMTP(host, port)
        server.starttls()
        server.login(login, password)

        link = f"https://chatbot-tcc.onrender.com/nova_senha?email={email}"
        corpo_html = f"""
        <html>
        <body>
        <h2>Redefinição de Senha</h2>
        <p>Para redefinir sua senha, clique no link abaixo:</p>
        <a href="{link}">Redefinir Senha</a>
        </body>
        </html>
        """

        email_msg = MIMEMultipart()
        email_msg['From'] = login
        email_msg['To'] = email
        email_msg['Subject'] = "Redefinição de Senha Fala.i"
        email_msg.attach(MIMEText(corpo_html, 'html'))

        server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
        server.quit()

        flash("Email enviado com sucesso! Verifique sua caixa de entrada.")
        return redirect(url_for('login.login'))

    return render_template('PaginaEsqueciSenha/PaginaEsqueciSenha.html')
