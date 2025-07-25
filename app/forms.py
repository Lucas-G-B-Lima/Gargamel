# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
import re # Para validação de telefone

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

    btnSubmit = SubmitField('Cadastrar')

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

