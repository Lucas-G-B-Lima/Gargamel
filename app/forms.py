# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
import re # Para validação de telefone

    
# FORM PARA LOGIN ===============================================
class LoginForm(FlaskForm):
    username = StringField("Usuário", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=6, max=100)])
    anonimo = BooleanField('aaaa?', default=False) # Checkbox para categoria Master


# FORM PARA CADASTRO DE USUARIO ===============================================
class CadastroForm(FlaskForm):
    # Informações de usuário
    register_username = StringField('Usuário:', validators=[
        DataRequired('O nome de usuário é obrigatório.'),
        Length(min=4, max=25, message='O usuário deve ter entre 4 e 25 caracteres.')
    ])
    register_email = StringField('E-mail:', validators=[
        DataRequired('O e-mail é obrigatório.'),
        Email('Formato de e-mail inválido.')
    ])
    register_telefone = StringField('Telefone:', validators=[
        DataRequired('O telefone é obrigatório.'),
        Length(min=10, max=15, message='O telefone deve ter entre 10 e 15 dígitos.')
    ])
    register_password = PasswordField('Senha:', validators=[
        DataRequired('A senha é obrigatória.'),
        Length(min=6, message='A senha deve ter no mínimo 6 caracteres.')
    ])
    register_confirm_password = PasswordField('Confirmar Senha:', validators=[
        DataRequired('A confirmação de senha é obrigatória.'),
        EqualTo('register_password', message='As senhas devem ser iguais.')
    ])

    # Informações do atleta
    register_name = StringField('Nome:', validators=[DataRequired('O nome é obrigatório.')])
    register_academy = StringField('Academia:', validators=[Optional()])
    
    register_belt = SelectField('Selecione sua faixa:', choices=[
        ('Não graduado', 'Não graduado'),
        ('Faixa Branca', 'Faixa Branca'),
        ('Faixa Azul', 'Faixa Azul'),
        ('Faixa Roxa', 'Faixa Roxa'),
        ('Faixa Marrom', 'Faixa Marrom'),
        ('Faixa Preta', 'Faixa Preta'),
        ('Faixa Coral', 'Faixa Coral'),
        ('Faixa Vermelha', 'Faixa Vermelha'),
        ('Faixa Branca Grau V', 'Faixa Branca Grau V')
    ], validators=[DataRequired('A faixa é obrigatória.')])
    
    # Opções de grau expandidas até o Grau 10
    register_grau = SelectField('Selecione um grau:', choices=[
        ('Grau 0', 'Sem grau'),
        ('Grau 1', 'Grau I'),
        ('Grau 2', 'Grau II'),
        ('Grau 3', 'Grau III'),
        ('Grau 4', 'Grau IV'),
        ('Grau 5', 'Grau V'),
        ('Grau 6', 'Grau VI'),
        ('Grau 7', 'Grau VII'),
        ('Grau 8', 'Grau VIII'),
        ('Grau 9', 'Grau IX'),
        ('Grau 10', 'Grau X')
    ], validators=[DataRequired('O grau é obrigatório.')])
    
    register_nascimento = DateField('Data de Nascimento:', format='%Y-%m-%d', validators=[
        DataRequired('A data de nascimento é obrigatória.')
    ])
    
    register_peso = StringField('Peso (kg):', validators=[Optional()])
    register_data_graduacao = DateField('Última Graduação:', format='%Y-%m-%d', validators=[Optional()]) # REMOVIDO: DataRequired


    # Validador customizado para a lógica de graus da Faixa Preta
    def validate_register_grau(self, field):
        # Converte o valor do grau para inteiro para comparação
        try:
            grau_int = int(field.data.replace('Grau ', ''))
        except ValueError:
            # Se não conseguir converter (ex: 'Sem grau'), trate como 0 para validação
            grau_int = 0 if field.data == 'Grau 0' else -1 # -1 para indicar erro se não for 0

        # Se a faixa NÃO for "Faixa Preta" e o grau for maior que 4
        if self.register_belt.data != 'Faixa Preta' and grau_int > 4:
            raise ValidationError('Apenas Faixas Pretas podem ter graus acima de IV.')
        
        # Se a faixa for "Faixa Preta" e o grau for maior que 10
        if self.register_belt.data == 'Faixa Preta' and grau_int > 10:
             raise ValidationError('Faixas Pretas podem ter no máximo Grau X.')
        
        # Se o grau for inválido (não conseguiu converter e não é 'Grau 0')
        if grau_int < 0:
            raise ValidationError('Grau selecionado inválido.')


# FORM PARA RECUPERACAO DE SENHA ===============================================
class ForgotPasswordForm(FlaskForm):
    forgot_password_user = StringField('E-mail ou Usuário:', validators=[
        DataRequired('Informe seu e-mail ou usuário.')
    ])
    forgot_metodo = SelectField('Selecione um método de recuperação:', choices=[
        ('-', 'Selecione'), # Manter a opção "Selecione"
        ('email', 'E-mail'),
        ('telefone', 'Telefone')
    ], validators=[
        DataRequired('Selecione um método de recuperação válido.'),
    ])

    def validate_forgot_metodo(self, field):
        if field.data == '-':
            raise ValidationError('Por favor, selecione um método de recuperação.')
        
    def validate_forgot_password_user(self, field):
        metodo = self.forgot_metodo.data
        user_input = field.data

        # Se o método escolhido for e-mail, valide o formato do e-mail usando o validador Email do WTForms
        if metodo == 'email':
            # Instancia o validador Email com sua mensagem personalizada
            email_validator = Email('Por favor, insira um formato de e-mail válido.')
            try:
                # Chama o validador Email manualmente.
                # Ele espera (form, field) como argumentos.
                email_validator(self, field) 
            except ValidationError as e:
                # Se o validador Email levantar uma exceção, nós a re-lançamos
                # Isso garante que a mensagem personalizada do Email() seja usada
                raise e
        # Não há validação de formato de entrada para o caso de 'telefone',
        # pois essa informação será verificada apenas no banco de dados.


# FORM PARA LOGIN COMO CONVIDADO ===============================================
class GuestLoginForm(FlaskForm):
    guest_name = StringField('Nome:', validators=[
        DataRequired('Por favor, insira seu nome.')
    ])
    guest_academy = StringField('Academia:', validators=[
        DataRequired('Por favor, insira o nome da sua academia.')
    ])
    guest_belt = SelectField('Selecione sua faixa:', choices=[
        ('Não graduado', 'Não graduado'),
        ('Faixa Branca', 'Faixa Branca'),
        ('Faixa Azul', 'Faixa Azul'),
        ('Faixa Roxa', 'Faixa Roxa'),
        ('Faixa Marrom', 'Faixa Marrom'),
        ('Faixa Preta', 'Faixa Preta'),
        ('Faixa Coral', 'Faixa Coral'),
        ('Faixa Vermelha', 'Faixa Vermelha'),
    ], validators=[
        DataRequired('Por favor, selecione sua faixa.')
    ])
    master = BooleanField('Categoria Master?', default=False) # Checkbox para categoria Master