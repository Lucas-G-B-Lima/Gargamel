# parceiros_data.py

def get_todos_os_parceiros():
    """
    Retorna uma lista de dicionários, onde cada dicionário representa um parceiro/patrocinador.
    Cada parceiro terá:
    - 'nome': O nome do parceiro/patrocinador.
    - 'logo': O caminho para a imagem da logo do parceiro (opcional, mas bom para o futuro).
    - 'link': O link para o site ou rede social do parceiro.
    """
    parceiros = [
        {
            'nome': "Lima",
            'logo': '../static/Midia/Noticias_img/Img_teste_parceiro.jpg',
            'link': 'https://pt.wikipedia.org/wiki/Jiu-j%C3%ADtsu'
        },
        {
            'nome': "VS BJJ",
            'logo': '../static/Midia/Noticias_img/Img_teste_parceiro.jpg',
            'link': 'https://pt.wikipedia.org/wiki/Jiu-j%C3%ADtsu'
        },
        {
            'nome': "Gladson",
            'logo': '../static/Midia/Noticias_img/Img_teste_parceiro.jpg',
            'link': 'https://pt.wikipedia.org/wiki/Jiu-j%C3%ADtsu'
        },
        {
            'nome': "Academia Top Jitsu",
            'logo': '../static/Midia/Noticias_img/Img_teste_parceiro.jpg',
            'link': 'https://pt.wikipedia.org/wiki/Jiu-j%C3%ADtsu'
        }
    ]
    return parceiros