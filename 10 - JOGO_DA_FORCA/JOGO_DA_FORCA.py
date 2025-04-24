import random
from os import system, name

# Variaveis com as listas com palavras aleartorias

frutas = ["banana","maça","abacaxi","morango"]
objetos = ["escada","bicicleta","notebook","quadro"]
locais = ["fortaleza","goias","pernanbunco","bahia"]
definir = {"Fruta":0,"Objeto":1,"Local":2}

valores = list(definir.values())  # Obtém uma lista dos valores do dicionário
valor_aleatorio = random.choice(valores)  # Seleciona aleatoriamente um valor da lista
if valor_aleatorio == 0:
    palavras = frutas
elif valor_aleatorio == 1:
    palavras = objetos
elif valor_aleatorio == 2:
    palavras = locais
else:
    print("Palavras não definidas")
    
    
# Função para limpar a tela a cada execuçao
def limpa_tela():
    
    # Windows
    if name == 'nt':
        _ = system('cls')
        
    # Mac ou Linux
    else:
        _ = system('clear')
     

# Função que desenha a forca na tela
def display_hangman(chances):

    # Lista de estágios da forca
    stages = [  # estágio 6 (final)
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """,
                # estágio 5
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                """,
                # estágio 4
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                """,
                # estágio 3
                """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                """,
                # estágio 2
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                """,
                # estágio 1
                """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """,
                # estágio 0
                """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """
    ]
    return stages[chances]
       
# Função 
def game(palavra, opções, dica):

    limpa_tela()
    
    print("\nBem-Vindo(a) ao jogo da forca!")
    print("Adivinhe a Palavra Abaixo: \n")

    #Escolhendo Aleortariamente uma palavra
    palavra = random.choice(palavra).upper()
    
    # Cria o tabuleiro com o caracter "_" multiplicado pelo comprimento da palavra
    tabuleiro = ["_"] * len(palavra)
    
    # List compreshesion
    letras_descobertas = ["_" for letra in palavra]
    
    # Número de Chances
    chances = 6
    
    # Lista para as letras erradas
    letras_erradas = [] 
    
    while chances > 0:
        
        for i,j in opções.items():
            if dica == j:
                print(f"Dica: A palavra é um(a) {i}  \n")
        
        # Print
        print(display_hangman(chances))
        #print("Palavra: ", tabuleiro)
        print("\n")
        
        # Print
        print(" ".join(letras_descobertas))
        print("\n Chances restantes: ", chances)
        print("\n Letras erradas: "," ".join(letras_erradas))
        
        # Tentativa
        tentativa = input("\n Digite uma letra: ").upper()
        
        # Condicional para descoberta de palavras
        if tentativa in palavra:
            index = 0
            print("\nVocê acertou a letra!")
            for letra in palavra:
                if tentativa == letra:
                    letras_descobertas[index] = letra
                index += 1
        else:
            print("\nVocê já tentou essa letra. Escolha outra!")
            chances -= 1
            letras_erradas.append(tentativa)

        limpa_tela()
        
        # Condicional em caso de Vitoria
        if "_" not in letras_descobertas:
            print("\n Voçê venceu, a palavra descoberta é", palavra)
            break
        
    # Condicional em caso de Derrota
    if "_" in letras_descobertas:
        print("\n Você perdeu, a palavra era", palavra)


# bloco main
if __name__ == "__main__":
    game(palavras, definir, valor_aleatorio)
    
