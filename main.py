# main.py
import os # Certifique-se de importar os
from app import app # Importa a instância 'app' do seu pacote 'app'

# Se você estiver chamando o load_dotenv() aqui também, certifique-se de que não haja duplicidade,
# ou que o load_dotenv() em app/__init__.py seja o único lugar.
# Idealmente, load_dotenv() deve ser chamado ANTES da instância Flask ser criada
# e suas configurações serem lidas, para que as variáveis de ambiente já estejam disponíveis.

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug_mode)