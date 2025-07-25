// script_login.js
document.addEventListener('DOMContentLoaded', () => {
    const welcomeFace = document.querySelector('.welcome-face');
    const backFaces = document.querySelectorAll('.back-face');
    let botaoEnviado = null;

    const cards = {
        login: document.getElementById('login-back'),
        social: document.getElementById('social-back'),
        guest: document.getElementById('guest-back'),
        register: document.getElementById('register-back'),
        forgot: document.getElementById('forgot-password')
    };

    // --- Mostra card específico ---
    function rotateTo(card) {
        welcomeFace.style.transform = 'rotateY(180deg)';
        welcomeFace.inert = true; // Adicionei esta linha

        backFaces.forEach(face => {
            face.style.transform = 'rotateY(180deg)';
            face.inert = true; // Substitui aria-hidden
        });
        card.style.transform = 'rotateY(360deg)';
        card.inert = false; // Substitui aria-hidden
    }

    // --- Voltar para tela inicial ---
    function backToWelcome() {
        welcomeFace.style.transform = 'rotateY(0deg)';
        welcomeFace.inert = false; // Corrigi esta linha (estava dentro do loop)
        backFaces.forEach(face => {
            face.style.transform = 'rotateY(180deg)';
        });
    }

    // --- Botões principais ---
    document.getElementById('login')?.addEventListener('click', () => rotateTo(cards.login));
    document.getElementById('social')?.addEventListener('click', () => rotateTo(cards.social));
    document.getElementById('guest')?.addEventListener('click', () => rotateTo(cards.guest));

    document.getElementById('btn_cadastrar')?.addEventListener('click', () => {
        cards.login.style.transform = 'rotateY(540deg)';
        cards.login.inert = true; // Substitui setAttribute
        cards.register.style.transform = 'rotateY(360deg)';
        cards.register.inert = false; // Substitui setAttribute
    });

    document.getElementById('btn_esqueceu_senha')?.addEventListener('click', () => {
        cards.login.style.transform = 'rotateY(540deg)';
        cards.login.inert = true;
        cards.forgot.style.transform = 'rotateY(360deg)';
        cards.forgot.inert = false;
    });

    document.querySelector('.back-btn-register')?.addEventListener('click', e => {
        e.preventDefault();
        cards.register.style.transform = 'rotateY(180deg)';
        cards.register.inert = true;
        cards.login.style.transform = 'rotateY(360deg)';
        cards.login.inert = false;
    });

    document.querySelector('.back-btn-forgot')?.addEventListener('click', e => {
        e.preventDefault();
        cards.forgot.style.transform = 'rotateY(180deg)';
        cards.forgot.inert = true;
        cards.login.style.transform = 'rotateY(360deg)';
        cards.login.inert = false;
    });

    document.querySelectorAll('.back-btn').forEach(btn => {
        btn.addEventListener('click', e => {
            e.preventDefault();
            backToWelcome();
        });
    });

    // --- Rede Social ---
    const socialButtons = document.querySelectorAll('.social_btn');
    const socialLabel = document.getElementById('rede_social_selecionada');
    const btnLoginSocial = document.getElementById('btn_login_social');

    socialButtons.forEach(button => {
        button.addEventListener('click', () => {
            const isSelected = button.classList.contains('selected');
            socialButtons.forEach(btn => btn.classList.remove('selected'));

            if (!isSelected) {
                button.classList.add('selected');
                btnLoginSocial.value = button.value; 
                socialLabel.textContent = `Você está prestes a fazer login com o: ${button.textContent.trim()}`;
                socialLabel.classList.add('visible');
            } else {
                btnLoginSocial.value = '';
                socialLabel.textContent = '';
                socialLabel.classList.remove('visible');
            }
        });
    });

    // --- Caixa de Mensagem Flutuante ---
    const messageBox = document.getElementById('message-box');
    const messageText = document.getElementById('message-text');
    const closeMessageBtn = document.getElementById('close-message');

    // Função unificada para controle de mensagens (mantida a versão mais completa)
    function showMessage(text, type = 'success') {
        if (!messageBox || !messageText) return;
        
        messageBox.className = `message-box ${type}`;
        messageText.textContent = text;
        
        // Mostrar com animação
        messageBox.style.display = 'flex';
        setTimeout(() => {
            messageBox.classList.add('show');
        }, 10);
        
        // Auto-fechar
        setTimeout(() => {
            messageBox.classList.remove('show');
            setTimeout(() => {
                messageBox.style.display = 'none';
            }, 300);
        }, 6000);
    }

    window.hideMessage = () => {
        if (messageBox) {
            messageBox.style.display = 'none';
        }
    };

    // Event listeners
    closeMessageBtn?.addEventListener('click', hideMessage);

    // --- Envio AJAX dos formulários ---
    const forms = document.querySelectorAll('#form_login, #form_social, #form_guest, #form_register, #form_forgot_password');

    // --- Validação Específica para Formulário Social ---
    const formSocial = document.getElementById('form_social');
    if (formSocial) {
        const btnSubmitSocial = formSocial.querySelector('button[type="submit"]');
        
        btnSubmitSocial.addEventListener('click', function(e) {
            const hasSelectedNetwork = document.querySelector('.social_btn.selected');
            
            if (!hasSelectedNetwork) {
                e.preventDefault();
                showMessage("Por favor, selecione uma rede social antes de continuar", "warning");
                
                // Feedback visual opcional (pode remover se não quiser)
                socialButtons.forEach(btn => {
                    btn.style.boxShadow = '0 0 0 1px #963232';
                    setTimeout(() => btn.style.boxShadow = '', 1000);
                });
            }
        });
    }

    // --- Validação do Formulário de Recuperação ---
    const formForgot = document.getElementById('form_forgot_password');
    if (formForgot) {
        const btnSubmitForgot = formForgot.querySelector('button[type="submit"]');
        
        btnSubmitForgot.addEventListener('click', function(e) {
            const userInput = document.getElementById('forgot_password_user');
            const metodoSelect = document.getElementById('forgot_metodo');
            let isValid = true;

            // Validação 1: Campo de usuário/e-mail preenchido
            if (!userInput.value.trim()) {
                showMessage("Usuário ou e-mail é obrigatório", "warning");
                userInput.style.border = '1px solid #963232';
                setTimeout(() => userInput.style.border = '', 1500);
                isValid = false;
            }

            // Validação 2: Método selecionado
            if (metodoSelect.value === '-' || !['email', 'telefone'].includes(metodoSelect.value)) {
                showMessage("Selecione um método de recuperação válido", "warning");
                metodoSelect.style.border = '1px solid #963232';
                setTimeout(() => metodoSelect.style.border = '', 1500);
                isValid = false;
            }

            if (!isValid) {
                e.preventDefault();
            }
        });
    }

    document.querySelectorAll('form button[type="submit"]').forEach(botao => {
        botao.addEventListener('click', e => {
            botaoEnviado = e.target;
        });
    });

    forms.forEach(form => {
        form.addEventListener('submit', async e => {
            e.preventDefault();
            hideMessage();

            if (botaoEnviado) {
                const nome = botaoEnviado.getAttribute('name');
                const valor = botaoEnviado.getAttribute('value');
                if (nome && valor) {
                    const inputOculto = document.createElement('input');
                    inputOculto.type = 'hidden';
                    inputOculto.name = nome;
                    inputOculto.value = valor;
                    form.appendChild(inputOculto);
                }
            }

            const formData = new FormData(form);
            for (let [key, value] of formData.entries()) {
                console.log(`${key}: ${value}`);
            }
            const action = form.getAttribute('action') || '#';

            try {
                const response = await fetch(action, {
                    method: 'POST',
                    body: formData
                });
                
                if (response.redirected) {
                        window.location.href = response.url;
                        return; // evita tentar fazer .json() com HTML
                    }

                    const data = await response.json();
                    console.log('Dados JSON:', data);

                    if (response.ok) {
                        showMessage(data.message || 'Sucesso!', 'success');
                        form.reset();
                    } else {
                        showMessage(data.message || 'Erro no formulário.', 'error');
                    }

            } catch (error) {
                console.error('Erro de rede/fetch:', error);
                showMessage('Falha de conexão. Tente novamente.', 'error');
            }
        });
    });

    //Mensagem do perfil social indisponicel
    document.querySelectorAll('.social-link.disabled').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Obtém o título do ícone (YouTube, Instagram, etc) de 3 formas diferentes:
            const network = this.dataset.network || // 1. Tenta pegar do data-attribute
                        this.parentElement.title || // 2. Tenta pegar do title do <li>
                        this.querySelector('img').alt.replace('Ícone ', ''); // 3. Pega do alt da imagem
            
            showMessage(`Nosso perfil no ${network} estará disponível em breve!`, 'warning');
        });
    });
    // Botão de contato (usando showMessage existente)
    document.getElementById('btn_contato')?.addEventListener('click', () => {
        showMessage("Caso precise de ajuda, envie um e-mail para gargabjj@contato.com.br", "info");
    });
});
