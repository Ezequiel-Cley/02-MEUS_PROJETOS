# Programa de Calculadora Simples

# Cria um Dicionario para determinar cada operação Matemática da Calculadora
oper = {1:'Soma',2:'Substrção',3:'Multiplicação',4:'Divisão'}

# Escreve para ter um visual da Calculadora
print('----------------------------------------')
print('Calculadora Simples - Selecione Operação')
print('1 - Soma')
print('2 - Subtração')
print('3 - Multiplicação')
print('4 - Divisão')
print('----------------------------------------')

# Da opção do usuário determina a operação desejada
operacao = int(input('Escolha a opção de 1 á 4: '))
print('----------------------------------------')

# Realizar validação se a opção desejada é Valida
while (operacao < 1) or (operacao > 4):
    print('Você Selecionou uma opção invalida favor selecionar uma opção correta')
    print('----------------------------------------')
    operacao = int(input('Escolha a opção de 1 á 4: '))
    print('----------------------------------------')

# Imprimir para o usuário a opção selecionada e qual calculo ela representa
for i,j in oper.items():
    if i == operacao:
        print(f'Opção informada foi {operacao} que representa a operação de {j}')

print('----------------------------------------')
print('Selecione com quantos números desejada Realizar a operação')
print('----------------------------------------')

# Define com quantos números deseja realizar a operação Matematica desejada
tam = tam = int(input('Selecione a opção de 2 até 10 números: '))
print('----------------------------------------')

# Lógica para impedir que o usuário escolha um opção invalida
while (tam < 2) or (tam > 10):
    print('Você Selecionou um número invalido deve escolher um número entre 2 e 10 !')
    print('----------------------------------------')
    tam = int(input('Selecione a opção de 2 até 10 números: '))
print('----------------------------------------')

# Cria uma lista vazia para acresentar os números digitados pelo usuário
lista_de_numeros = []

# Loop para receber os números que devem ser calculados;
for i in range(0, tam):
    num = float(input(f'Selecione o número de posição {i+1} para realizar o calculo: '))
    print('----------------------------------------')
    lista_de_numeros.append(num)

# Cria uma função para que realize o calculo de acordo com opção desejada
def calcular(op, numeros):
    resultado = numeros[0]  # Começa com o primeiro número da lista

    # Define condição para Calculo da Soma
    if op == 1:
        for num in numeros[1:]:
            resultado += num
            
    # Define condição para Calculo da Subtração
    elif op == 2:
        for num in numeros[1:]:
            resultado -= num
            
    # Define condição para Calculo de Multiplicação
    elif op == 3:
        for num in numeros[1:]:
            if num == 0:
                print("Erro: multiplicação por zero.")
                return None
            resultado *= num
    
    # Define condição para Calculo de Divisão
    elif op == 4:
        for num in numeros[1:]:
            if num == 0:
                print("Erro: divisão por zero.")
                return None
            resultado /= num
    else:
        print("Erro: operação não suportada.")
        return None

    return resultado

# Chamado a função passado os parametros criado anteriormente
rst =  calcular(operacao, lista_de_numeros)
print('----------------------------------------')

# Define texto para apresentar o resultado para o usuário
print(f'O resultado do seu calculo é de {round(float(rst),6)}')

print('----------------------------------------')