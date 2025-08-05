# views.py
from app import app #Trabalha no app
from flask import render_template, url_for, request, redirect, session, jsonify
from .noticias_data import get_todas_as_noticias, get_noticia_por_id
from .parceiros_data import get_todos_os_parceiros
from .auth_logic import (
    process_login_senha, 
    process_login_social, 
    process_login_convidado, 
    process_cadastro_logic,
    process_recuperacao_senha
)
from .forms import CadastroForm, ForgotPasswordForm, GuestLoginForm, LoginForm


@app.errorhandler(404)
def page_not_found(e):
    context = {
        'logged_in': 'user_logged_in'
    }
    return render_template('not_found.html',context=context), 404

@app.route('/')
def home_login():
    
    form_login = LoginForm()
    form_cadastro = CadastroForm()
    form_forgot_password = ForgotPasswordForm()
    form_guest_login = GuestLoginForm()

    return render_template('index.html', 
                           form_l=form_login,
                           form_c=form_cadastro, 
                           form_p=form_forgot_password,
                           form_g=form_guest_login) # Passe o formulário para o template

@app.route('/home')
def page_home():

    todas_as_noticias = get_todas_as_noticias()
    todos_os_parceiros = get_todos_os_parceiros()
    
    user_logged_in = session.get('logged_in', False)
    username = session.get('username', 'Convidado')
    login_method = session.get('login_method', 'N/A')

    usuario = 'Lucas Lima'
    faixa = 'Faixa Preta'
    academia = 'Garga BJJ'

    context = {
        'logged_in': user_logged_in,
        'username': username,
        'login_method': login_method,
        
        'usuario': usuario,
        'faixa': faixa,
        'academia': academia
    }
    return render_template('home.html',
                           noticias=todas_as_noticias,
                           parceiros=todos_os_parceiros,
                           context=context)

@app.route('/locais')
def page_locais():

    todos_os_parceiros = get_todos_os_parceiros()
    #    tive que adicionar context pois esta dando erro por eu ter um "arquivo base"
    context = {
        'logged_in': 'user_logged_in'
    }
    #
    return render_template('locais.html',
                           parceiros=todos_os_parceiros,
                           context=context)

@app.route('/eventos')
def page_eventos():
    #    tive que adicionar context pois esta dando erro por eu ter um "arquivo base"
    context = {
        'logged_in': 'user_logged_in'
    }
    #
    return render_template('eventos.html',context=context)

@app.route('/sobre')
def page_sobre():
    #    tive que adicionar context pois esta dando erro por eu ter um "arquivo base"
    context = {
        'logged_in': 'user_logged_in'
    }
    #
    return render_template('sobre.html',context=context)

@app.route('/parceiros')
def page_parceiros():
    #    tive que adicionar context pois esta dando erro por eu ter um "arquivo base"
    context = {
        'logged_in': 'user_logged_in'
    }
    todos_os_parceiros = get_todos_os_parceiros()
    #
    return render_template('parceiros.html',
                           parceiros=todos_os_parceiros,
                           context=context)

@app.route('/layout')
def page_layout():
    context = {
        'logged_in': 'user_logged_in'
    }
    #
    return render_template('layout.html',context=context)



@app.route('/noticias')
def page_noticias():
    #
    #
    #
    return render_template('noticias.html')



############## =========== PROCESSOS =========== ##############

@app.route('/processar_login', methods=['POST']) #OK
def processar_login_unificado():
    login_type = request.form.get('login_type') # Pega o valor do botão 'OSS!' clicado
    
    if login_type == 'senha':
        return process_login_senha(request)
    elif login_type in ['google', 'instagram', 'x-twitter', 'facebook', 'telegram', 'pinterest']:
        return process_login_social(request)
    elif login_type == 'convidado':
        return process_login_convidado(request)
    else:
        print("Tipo de login desconhecido ou botão 'OSS!' não clicado.")
        return jsonify({'status': 'error', 'message': 'Erro: Tipo de login inválido.'}), 400

# CADASTRO ================================================================
@app.route('/processar_cadastro', methods=['POST']) # Removido GET, pois o JS faz o AJAX
def handle_cadastro():
    print("Dados do formulário:", request.form)  # ← Adicione esta linha
    form = CadastroForm() # Instancia o formulário novamente para validação

    # Flask-WTF já verifica se é POST e se o CSRF token é válido
    if form.validate_on_submit(): 
        # Se a validação do WTForms passou, chame sua lógica de negócio
        # Passe os dados limpos do formulário para a função de lógica
        response_data, status_code = process_cadastro_logic(
            # Não é mais necessário passar 'req=request' se a lógica não usar o objeto request diretamente
            username=form.register_username.data,
            password=form.register_password.data, # Senha em texto puro
            nome=form.register_name.data,
            email=form.register_email.data,
            telefone=form.register_telefone.data,
            peso=form.register_peso.data or None,
            nascimento=form.register_nascimento.data,
            academia=form.register_academy.data or None,
            faixa=form.register_belt.data,
            graus=form.register_grau.data,
            ultima_graduacao=form.register_data_graduacao.data or None
        )
        # Retorna a resposta JSON da lógica
        return jsonify(response_data), status_code
    else:
        # Se a validação do WTForms falhou, retorne os erros em JSON
        # form.errors contém um dicionário com os erros de cada campo
        print("Erros de validação do formulário:", form.errors)
        return jsonify({'status': 'error', 'message': 'Erro de validação no formulário.', 'errors': form.errors}), 400


@app.route('/processar_recuperacao_senha', methods=['POST'])
def handle_recuperacao_senha():
    return process_recuperacao_senha(request)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('login_method', None)
    session.pop('anonima', None)
    session.pop('guest_data', None)
    print("Usuário deslogado.")
    return redirect(url_for('home_login'))

@app.route('/processar_login_convidado', methods=['POST'])
def handle_login_convidado():
    form = GuestLoginForm() 
    if form.validate_on_submit():
        return process_login_convidado(
            name=form.guest_name.data,
            academy=form.guest_academy.data,
            belt=form.guest_belt.data,
            master=form.master.data
        )
    else:
        # Se a validação do WTForms falhou, retorne os erros em JSON.
        # Isso ainda será capturado pelo JavaScript.
        print("Erros de validação do formulário de convidado:", form.errors)
        return jsonify({'status': 'error', 'message': 'Erro de validação no formulário de convidado.', 'errors': form.errors}), 400
