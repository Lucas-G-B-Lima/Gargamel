# noticias_data.py

def get_todas_as_noticias():
    """
    Retorna uma lista de dicionários, onde cada dicionário representa uma notícia.
    Cada notícia terá:
    - 'id': um identificador único para a notícia.
    - 'titulo': O título da notícia.
    - 'imagem': O caminho para a imagem da notícia.
    - 'link': O link para a página completa da notícia (o "portal de notícias").
    """
    noticias = [
        {
            'id': 1,
            'titulo': "NOTICIA TESTE: Gargamel é campeão no Mundial de BJJ!",
            'imagem': 'Midia/Noticias_img/Img_teste_noticia.jpg',
            'link': '/noticia/1' # Link para a página detalhada da notícia
        },
        {
            'id': 2,
            'titulo': "Lima finaliza faixa preta em seminário de jiu-jitsu!",
            'imagem': 'Midia/Noticias_img/Img_teste_noticia.jpg',
            'link': '/noticia/2'
        },
        {
            'id': 3,
            'titulo': "Nova filial da Garga-BJJ é inaugurada nos EUA!",
            'imagem': 'Midia/Noticias_img/Img_teste_noticia.jpg',
            'link': '/noticia/3'
        },
        {
            'id': 4,
            'titulo': "Conheça os benefícios do jiu-jitsu para a saúde mental.",
            'imagem': 'Midia/Noticias_img/Img_teste_noticia.jpg',
            'link': '/noticia/4'
        }
    ]
    return noticias

def get_noticia_por_id(noticia_id):
    """
    Retorna uma única notícia baseada no seu ID.
    """
    todas_noticias = get_todas_as_noticias()
    for noticia in todas_noticias:
        if noticia['id'] == noticia_id:
            return noticia
    return None # Retorna None se a notícia não for encontrada