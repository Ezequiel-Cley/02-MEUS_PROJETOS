import requests

def send_document(token, chat_id, file_path, caption=None, topico=None):
    """
    Envia um documento (arquivo) para um chat no Telegram.

    Parameters:
        token (str): O token do bot do Telegram.
        chat_id (str): O ID do chat para o qual o arquivo será enviado.
        file_path (str): O caminho para o arquivo que você deseja enviar.
        caption (str, opcional): Uma legenda para o arquivo.
        topico (int, opcional): O ID do tópico dentro do chat (caso esteja enviando para um fórum de tópicos em um grupo).

    Returns:
        None

    Exemplo de uso:
        send_document('seu_token', 'ID_do_chat', 'caminho_para_seu_arquivo.csv', 'Legenda opcional', topico=123)
    """
    try:
        # Cria um dicionário com os parâmetros necessários
        data = {"chat_id": chat_id}
        
        # Se um tópico for informado, adiciona ao dicionário
        if topico:
            data["message_thread_id"] = topico

        # Abre o arquivo em modo de leitura binária
        with open(file_path, 'rb') as file:
            # Adiciona o arquivo aos dados da requisição
            files = {"document": (file_path, file)}

            # Se uma legenda for fornecida, adiciona-a aos dados da requisição
            if caption:
                data["caption"] = caption

            # Monta a URL da API do Telegram com o token do bot
            url = f"https://api.telegram.org/bot{token}/sendDocument"

            # Envia a requisição POST para a URL com os dados e o arquivo
            response = requests.post(url, data=data, files=files)

            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 200:
                print("Arquivo enviado com sucesso!")
            else:
                print("Erro ao enviar o arquivo:", response.status_code, response.text)
    except Exception as e:
        # Captura e imprime qualquer erro que ocorra durante o envio
        print("Erro no send_document:", e)


# Criando Variáveis para disparar a mensagem
tk = 'TOKEN_DO_SEU_BOT_DO_TELEGRAM'  # Define o token do seu bot
gp = 'ID_DO_GRUPO_OU_USUARIO'  # Define o grupo ou usuário que receberá o arquivo
arq = r'\\C\aminho\completo\do\arquivo\arquivo.txt'  # Caminho do arquivo
cp = "Documento de Assunto X"  # Legenda opcional
tp = None  # ID do tópico dentro do grupo (se aplicável, ex: 123)

# Chama a função para envio da mensagem
send_document(tk, gp, arq, cp, tp)
