import secrets
from app import db
from flask import url_for, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import UserLogin, UserDados, UserBJJ #Tabelas do banco de dados
from datetime import datetime, date, timedelta

# Login via usuario e senha =========================================================
def process_login_senha(request):
    
    # 1. Captura os dados do formulário
    username = request.form['username']  # Usando acesso direto pois o front já validou
    password = request.form['password']
    modo_anonimo = request.form.get('anonima', 'off') == 'on'

    # 2. Validação EXCLUSIVA do back-end: existência do usuário
    user = UserLogin.query.filter_by(login=username).first() #o frist é necesario, eu checkei

    if not user:
        return jsonify({
            'status': 'error',
            'message': 'Usuário não encontrado'
        }), 404
    
    # 3. Verificação de senha (essencial, não pode ser feita no front)
    if not user.check_password(password):
        return jsonify({
            'status': 'error',
            'message': 'Senha incorreta'
        }), 401

    # 4. Configuração da sessão
    session.update({
        'user_id': user.id,
        'logged_in': True,
        'login_method': 'senha',
        'anonima': modo_anonimo
    })

    # 5. Resposta de sucesso
    return redirect(url_for('home_page'))



# Login via rede social =========================================================
def process_login_social(request):

    # 1. Pega o nome da rede social do botão "OSS!"
    social_network = request.form['login_type']
    
    # 2. Configuração básica da sessão
    session.update({
        'logged_in': True,
        'username': f"Convidado ({social_network})",
        'login_method': f"social_{social_network}",
        'last_login': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Formato legível
        'guest_data': {
            'social': social_network,
            'academy': request.form.get('guest_academy', 'Não informada'),
            'belt': request.form.get('guest_belt', 'Não informada')
        }
    })
    
    # 3. Login
    return redirect(url_for('home_page'))


# Login via usuario convidado =========================================================
def process_login_convidado(name, academy, belt, master):
    # A validação de nome agora é feita pelo WTForms, antes desta função ser chamada.

    try:
        # 3. Configura sessão
        session.update({
            'logged_in': True,
            'user_type': 'guest',
            'username': f"{name} (Convidado)", # Usando o nome recebido
            'guest_data': {
                'name': name,
                'academy': academy,
                'belt': belt,
                'is_master': master, # Usando 'master' diretamente do form (True/False)
                'login_time': datetime.now().strftime('%d/%m/%Y %H:%M')
            }
        })
        return redirect(url_for('home_page')) # Redireciona para a homepage <-- Restaurado!

    except Exception as e:
        # Se ocorrer um erro interno (ex: DB), ainda podemos retornar um JSON de erro
        # No entanto, se o fluxo do seu app espera um redirect, você pode precisar de um tratamento diferente aqui
        # Para este caso, vamos manter o retorno de JSON para erros inesperados
        print(f"Erro ao processar login de convidado: {e}")
        return jsonify({'status': 'error', 'message': 'Ocorreu um erro inesperado ao tentar entrar como convidado.'}), 500


# Cadastro de usuario =========================================================
def process_cadastro_logic(username, password, nome, email, telefone, peso, 
                         nascimento, academia, faixa, graus, ultima_graduacao):
    """
    Lógica completa de cadastro com:
    - Validações
    - Salvamento no banco
    - Tratamento de erros
    """
    
    try:
        # 1. Verifica se usuário/email já existem
        if UserLogin.query.filter_by(login=username).first():
            return {'status': 'error', 'message': 'Nome de usuário já em uso'}, 409
            
        if UserDados.query.filter_by(email=email).first():
            return {'status': 'error', 'message': 'E-mail já cadastrado'}, 409
        
        # Função auxiliar para converter datas
        def parse_date(date_input):
            if date_input is None:
                return None
            try:
                if isinstance(date_input, date):  # Corrigido usando date
                    return date_input
                elif isinstance(date_input, str):
                    return datetime.strptime(date_input, '%Y-%m-%d').date()
                return None
            except (ValueError, TypeError) as e:
                print(f"Erro ao converter data: {e}")
                return None
        
        try:
            data_nascimento = parse_date(nascimento)
            data_graduacao = parse_date(ultima_graduacao) if ultima_graduacao else None
        except ValueError as e:
            return {'status': 'error', 'message': f'Formato de data inválido: {str(e)}'}, 400


        # 2. Cria o usuário principal
        novo_usuario = UserLogin(
            login=username,
            data_criacao=datetime.now(),
            senha_hash=generate_password_hash(password))
            
        # 3. Cria dados pessoais
        dados_pessoais = UserDados(
            nome=nome,
            email=email,
            telefone=telefone,
            peso=float(peso) if peso else None,
            nascimento=data_nascimento,
            status='ativo')
            
        # 4. Cria dados de BJJ
        dados_bjj = UserBJJ(
            academia=academia,
            faixa=faixa,
            graus=int(graus.split()[-1]) if graus else 0,
            ultima_graduacao=data_graduacao)
            
        # 5. Associa os relacionamentos
        novo_usuario.dados = dados_pessoais
        novo_usuario.bjj = dados_bjj
        
        # 6. Salva no banco
        db.session.add(novo_usuario)
        db.session.commit()
        
        return {'status': 'success', 'message': 'Usuário cadastrado com sucesso!\nFaça login para continuar.'}, 201
        
    except ValueError as e:
        db.session.rollback()
        return {'status': 'error', 'message': f'Formato de dados inválido: {str(e)}'}, 400
        
    except Exception as e:
        db.session.rollback()
        print(f"Erro durante cadastro: {str(e)}")
        return {'status': 'error', 'message': 'Erro interno no servidor'}, 500

# Recuperar senha de usuario =========================================================
def process_recuperacao_senha(request):
    #Processa a recuperação de senha com validações e segurança básica.
    
    # 1. Validação dos dados de entrada
    identificador = request.form['forgot_password_user'].strip()
    metodo = request.form['forgot_metodo'].lower()

    # 2. Busca o usuário no banco de dados
    try:
        if '@' in identificador: # Verifica se é email ou username
            user = UserDados.query.filter_by(email=identificador).first()
            if user:
                user = user.user_login  # Chega até o login pelo e-mail que está na variavel user
        else:
            user = UserLogin.query.filter_by(login=identificador).first()

        if not user:
            return jsonify({
                'status': 'success',  # Mesmo status para não vazar informações
                'message': f'Se existir, um código foi enviado para seu {metodo}'
            }), 200

        # 3. Gera token seguro e data de expiração
        token = secrets.token_urlsafe(32)  # Token criptograficamente seguro
        expiracao = datetime.now() + timedelta(hours=1)  # Válido por 1 hora

        # 4. Simula o envio (em produção, integrar com serviço real)
        if metodo == 'email':
            print(f"\n--- Simulação de e-mail ---")
            print(f"Para: {user.dados.email}")
            print(f"Assunto: Recuperação de senha")
            print(f"Token: {token}\n")
        else:  # telefone
            print(f"\n--- Simulação de SMS ---")
            print(f"Para: {user.dados.telefone}")
            print(f"Mensagem: Seu código é {token[:6]}\n")

        # 5. Atualiza o usuário com token (na prática, use uma tabela dedicada)
        user.token_recuperacao = token
        user.token_expiracao = expiracao
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': f'Código de recuperação enviado para seu {metodo}.',
            'token': token[:6]  # Só para demonstração (não fazer em produção)
        }), 200


    except Exception as e:
        db.session.rollback()
        print(f"Erro na recuperação: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Falha ao processar solicitação'
        }), 500