# main.py
import os
from app import app #Pega de init.py

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000)) #No render ele espera que eu passe uma "porta" como variavel de ambiente
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() == "true" #Deixa assim, o gemini até gritou cmg rsrs
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
    # Forcing rebuild