from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

class UserLogin(db.Model):
    __tablename__ = 'user_login'
    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime, default=datetime.now())
    login = db.Column(db.String(80), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(128), nullable=False)

    dados = db.relationship('UserDados', backref='user_login', uselist=False)
    bjj = db.relationship('UserBJJ', backref='user_login', uselist=False)

    def set_password(self, password):
        self.senha_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha_hash, password)

    def __repr__(self):
        return f'<UserLogin {self.login}>'


class UserDados(db.Model): # Renomeado para seguir convenção PEP 8 (CamelCase)
    __tablename__ = 'user_dados'
    __table_args__ = (
        db.CheckConstraint('peso > 0', name='check_peso_positivo'),  # ← Adicione
        db.CheckConstraint('nascimento < CURRENT_DATE', name='check_nascimento_valido')
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_login.id'), unique=True, nullable=False)
    # Usar datetime.utcnow para timestamps consistentes
    # e onupdate para atualizar automaticamente na modificação
    data_atualizacao = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    telefone = db.Column(db.String(20), index=True)
    peso = db.Column(db.Numeric(5, 2)) # Ex: 90.50
    nascimento = db.Column(db.Date)
    status = db.Column(db.String(20), default='ativo')

    def __repr__(self):
        return f'<UserDados {self.nome}>'

    @property # Decorador que permite acessar o método como um atributo (ex: usuario.dados.idade)
    def idade(self):
        if self.nascimento:
            today = date.today()
            # Calcula a idade corretamente considerando o mês e dia
            return today.year - self.nascimento.year - ((today.month, today.day) < (self.nascimento.month, self.nascimento.day))
        return None

    @property
    def eh_master(self):
        if self.idade is not None:
            return self.idade >= 30
        return False

    @property
    def categoria_peso(self):
        # Lógica para definir a categoria de peso baseada em peso (o nome da coluna)
        if self.peso is None: # Alterado de self.peso_kg para self.peso
            return "Não Informado"
        # Converte para float para comparações, pois db.Numeric retorna Decimal
        peso_float = float(self.peso)
        if peso_float <= 64:
            return "Pluma"
        elif peso_float <= 70:
            return "Pena"
        elif peso_float <= 76:
            return "Leve"
        elif peso_float <= 82.3:
            return "Médio"
        elif peso_float <= 88.3:
            return "Meio-Pesado"
        elif peso_float <= 94.3:
            return "Pesado"
        elif peso_float <= 100.5:
            return "Super Pesado"
        else: # Se o peso for maior que 100.5
            return "Pesadíssimo"

    @property
    def categoria_idade(self):
        if self.idade is None:
            return "Não Informado"
        # Usando if/elif/else para as categorias de idade
        elif self.idade < 18:
            return "Juvenil"
        elif self.idade < 30:
            return "Adulto"
        elif self.idade < 36:
            return "Master 1"
        elif self.idade < 41:
            return "Master 2"
        elif self.idade < 46:
            return "Master 3"
        elif self.idade < 51:
            return "Master 4"
        elif self.idade < 56:
            return "Master 5"
        else: # Se a idade for 56 ou mais
            return "Master 6"


class UserBJJ(db.Model): # Renomeado para seguir convenção PEP 8 (CamelCase)
    __tablename__ = 'user_bjj'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_login.id'), unique=True, nullable=False)
    # Usar datetime.utcnow para timestamps consistentes
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    academia = db.Column(db.String(200))
    faixa = db.Column(db.String(50))
    graus = db.Column(db.Integer)
    ultima_graduacao = db.Column(db.Date)

    def __repr__(self):
        return f'<UserBJJ para user_id {self.user_id}>'
