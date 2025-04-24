import requests

def sender_photo(token, chat, caminho, topico=None, caption=None):
    """
    Envia uma foto para um chat no Telegram usando o bot e o token fornecidos.

    Parameters:
        token (str): O token do bot do Telegram.
        chat (str): O ID do chat para o qual a foto será enviada.
        caminho (str): O caminho do arquivo da foto a ser enviada.
        topico (int, opcional): O ID do tópico dentro do chat (caso esteja enviando para um fórum de tópicos em um grupo).
        caption (str, opcional): Uma legenda para a foto.

    Returns:
        None

    Exemplo de uso:
        sender_photo('seu_token', 'id_do_chat', 'caminho_da_foto.jpg', topico=123, caption="Minha foto")
    """
    try:
        # URL da API do Telegram para enviar a foto
        url = f'https://api.telegram.org/bot{token}/sendPhoto'

        # Parâmetros da requisição
        params = {"chat_id": chat}

        # Se um tópico for informado, adiciona ao dicionário
        if topico:
            params["message_thread_id"] = topico

        # Se uma legenda for fornecida, adiciona ao dicionário
        if caption:
            params["caption"] = caption

        # Abrir o arquivo da foto em modo binário
        with open(caminho, 'rb') as foto:
            response = requests.post(url, params=params, files={'photo': foto})

        # Verifica a resposta
        if response.status_code == 200:
            print("📸 Foto enviada com sucesso!")
        else:
            print("❌ Erro ao enviar a foto:", response.text)

    except Exception as e:
        print("🚨 Erro no envio da foto:", e)


# Criando Variáveis para disparar a mensagem
tk = 'TOKEN_DO_SEU_BOT_DO_TELEGRAM'  # Token do bot
gp = 'ID_DO_GRUPO_OU_USUARIO'  # ID do chat/grupo
ft = r'\\C\aminho\completo\da\foto\imagem.png'  # Caminho da foto
tp = None  # ID do tópico (caso aplicável)
caption = "Aqui está minha foto 📷"  # Legenda opcional

# Chama a função para envio da mensagem
sender_photo(tk, gp, ft, tp, caption)
