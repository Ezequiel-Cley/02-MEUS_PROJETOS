
import requests

def send_message(token, chat_id, message, topico=None):
    """
    Envia uma mensagem de texto para um chat no Telegram.

    Parameters:
        token (str): O token do bot do Telegram.
        chat_id (str): O ID do chat para o qual a mensagem será enviada.
        message (str): O texto da mensagem a ser enviada.
        topico (int, opcional): O ID do tópico dentro do chat (caso esteja enviando para um fórum de tópicos em um grupo).
        
    Returns:
        None

    Exemplo de uso:
        send_message('seu_token', 'ID_do_chat', 'Esta é uma mensagem de exemplo.')
    """
    try:
        # Define um dicionário 'data' com os parâmetros necessários para enviar a mensagem
        data = {"chat_id": chat_id, "text": message}
        
        if topico:
            data["message_thread_id"] = topico
        
        # Monta a URL da API do Telegram com o token do bot
        url = "https://api.telegram.org/bot{}/sendMessage".format(token)
        
        # Envia a requisição POST para a URL com os dados da mensagem
        requests.post(url, data)
    except Exception as e:
        # Captura e imprime qualquer erro que ocorra durante o envio
        print("Erro no sendMessage:", e)
        
# Criando Variaveis para disparar a mensagem

# Define o token do seu bot do Telegram
tk = 'TOKEN_DO_SEU_BOT_DO_TELEGRAM'

# Define o Grupo que deseja realizar o Envio
gp = 'ID_DO_GRUPO_OU_USUARIO'

# Define o ID do tópico (caso aplicável)
tp = None

# Define Mensagem que deseja enviar Automáticamente
msg = """
    Mensagem será enviada aqui 
    Coloque maior número de detalhes
    Que desejar!!! 

"""

# Chama a função para envio da Mensagem
send_message(tk,gp,msg, tp)