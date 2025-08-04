document.addEventListener('DOMContentLoaded', () => {
    const hamburgerIcon = document.getElementById('menu-user');
    const sidebarMenu = document.getElementById('sidebar-menu');

    if (hamburgerIcon && sidebarMenu) {
        hamburgerIcon.addEventListener('click', () => {
            hamburgerIcon.classList.toggle('active'); // Anima o ícone
            sidebarMenu.classList.toggle('active');   // Mostra/esconde o menu lateral
            document.body.classList.toggle('no-scroll'); // Opcional: impede scroll do body
        });
    }

    // Opcional: Fechar o menu ao clicar em um link ou fora dele
    sidebarMenu.addEventListener('click', (event) => {
        if (event.target.tagName === 'A' || event.target === sidebarMenu) {
            hamburgerIcon.classList.remove('active');
            sidebarMenu.classList.remove('active');
            document.body.classList.remove('no-scroll');
        }
    });
});