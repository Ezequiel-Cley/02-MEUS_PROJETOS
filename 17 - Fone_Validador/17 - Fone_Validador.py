import pandas as pd
import re

# Exemplo de dados em um DataFrame
data = {
    'telefone': [
        '+55 11 98765-4321',
        '+55 21 3456-7890',
        '987654321',
        '+55 31 91234-5678',
        '(11) 2222-3333',
        '+55 55 99999-1234',
        '12345',
        '912345678',         # Celular sem DDD
        '34567890',          # Fixo sem DDD
        '(00) 99999-1234',   # DDD inválido
        '+55 85 98532-0992', # Número internacional completo
        '+5585999999999',    # Número internacional com dígitos repetidos
    ]
}

df = pd.DataFrame(data)

# Lista de DDDs válidos no Brasil
ddds_validos = {
    '11', '12', '13', '14', '15', '16', '17', '18', '19',  # SP
    '21', '22', '24',                                      # RJ
    '27', '28',                                            # ES
    '31', '32', '33', '34', '35', '37', '38',              # MG
    '41', '42', '43', '44', '45', '46',                    # PR
    '47', '48', '49',                                      # SC
    '51', '53', '54', '55',                                # RS
    '61',                                                  # DF
    '62', '64',                                            # GO
    '63',                                                  # TO
    '65', '66',                                            # MT
    '67',                                                  # MS
    '68',                                                  # AC
    '69',                                                  # RO
    '71', '73', '74', '75', '77',                          # BA
    '79',                                                  # SE
    '81', '87',                                            # PE
    '82',                                                  # AL
    '83',                                                  # PB
    '84',                                                  # RN
    '85', '88',                                            # CE
    '86', '89',                                            # PI
    '91', '93', '94',                                      # PA
    '92', '97',                                            # AM
    '95',                                                  # RR
    '96',                                                  # AP
    '98', '99'                                             # MA
}

# Função para validar o telefone e identificar se é fixo ou celular
def validar_telefone(numero):
    # Remove todos os caracteres não numéricos, exceto o sinal de "+"
    numero_limpo = re.sub(r'[^\d+]', '', numero)
    
    # Verifica se o número tem muitos dígitos repetidos (ex: 1111111111, 99999999999)
    if re.fullmatch(r'(\d)\1{7,}', re.sub(r'\D', '', numero_limpo)):
        return 'Inválido'
    
    # Verifica números com código internacional +55 (Brasil)
    if numero_limpo.startswith('+55'):
        numero_sem_codigo = numero_limpo[3:]
        if len(numero_sem_codigo) == 11:
            ddd = numero_sem_codigo[:2]
            if ddd not in ddds_validos:
                return 'Inválido'
            return 'Celular' if numero_sem_codigo[2] == '9' else 'Fixo'
    
    # Verifica números com DDD (11 dígitos)
    if len(numero_limpo) == 11:
        ddd = numero_limpo[:2]
        if ddd not in ddds_validos:
            return 'Inválido'
        return 'Celular' if numero_limpo[2] == '9' else 'Fixo'
    
    # Verifica números sem DDD (8 ou 9 dígitos)
    if len(numero_limpo) == 9 and numero_limpo[0] == '9':
        return 'Celular'
    if len(numero_limpo) == 8:
        return 'Fixo'
    
    return 'Inválido'

# Aplica a função ao DataFrame
df['status'] = df['telefone'].apply(validar_telefone)

# Exibe o resultado
print(df)
