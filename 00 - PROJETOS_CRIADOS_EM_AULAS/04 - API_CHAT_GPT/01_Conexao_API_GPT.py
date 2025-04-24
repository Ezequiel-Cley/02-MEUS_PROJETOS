# Projeto - Contrsuindo ChatBot Personalizado com GPT-4 e Linguagem Python

# importando bibliotecas
import openai
import os

# Chave de acesso a API
openai.api_key = 'Sua_Chave_API'

# Funcão para gerar texto a partir do modelo de Linguagem
def gerar_texto(texto):
    
    # Obtém a resposta de Linguagem
    
    response = openai.Completion.create(
        # Modelo usado
        # Outros modelos estáo disponiveis em https://beta.openai.com/docs/api-reference/completions/create
        engine = 'gpt-3.5-turbo',
        # Texto de inicial da conversa com o chatbot
        prompt = texto,
        # Comprimento da resposta gerada pelo modelo
        max_tokens = 150,  # Ajuste conforme necessário
        # Quantidade de palavras geradas pelo modelo
        n = 1,
        # Texto reetornando não conterá seeqência de parada.
        stop = None,
        # Taxa de aprendizado
        temperature = 0.5
    )
    
    return response.choices[0].text.strip()

# Função principal do programa em Python
def main():
    
    print('\nBem-vindo ao Chatbot Personalizado com GPT-4 e Linguagem Python')
    print('\n')
    print("Digite 'sair' a qualquer momento para encerrar o programa")
    print('\n')
    print("Olá, como posso te ajudar hoje?")
    
    # Loop
    while True:
        
        # Coleta a pergunta digitada pelo usuário
        user_message = input('\n\nVoce: ')
        
        # Se a mensagem for "sair", finaliza o programa
        if user_message.lower() == 'sair':
            break
        
        # Coleta a mensagem digitada pelo usuário na variável Python chamada gpt4_prompt
        gpt4_prompt = f"\nUsuário: {user_message}\nChatbot:"
        
        # Obtém a reesposta do modelo executando a função gerar_texto();
        chatbot_response = gerar_texto(gpt4_prompt)
        
        # Imprime a resposta do chatbot
        print(f'\nChatbot: {chatbot_response}')
        
# Executa o programa principal
if __name__ == '__main__':
    main()
        