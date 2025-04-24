# Bibliotecas

# Biblioteca de Conexão com Bando de Dados
import pyodbc

# Biblioteca de Mondelagem e Criações de Dados 
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table

# Bibliotecas para envio de fotos no telegram
# Instalar o pacote (python-telegram-bot)
import asyncio
from telegram import Bot
from telegram import InputFile

# Parâmetros de conexão
server = 'Inserir o IP para conexão com Banco'
database = 'Nome_do_Banco_que_Deseja_Se_Conectar'
username = 'Nome_de_Usuario_Para_Conexão'

# String de conexão com autenticação do Windows
connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};Trusted_Connection=yes;'

# Conectando ao banco de dados
conn = pyodbc.connect(connection_string)

# Sua consulta SQL
query = """SELECT 
            CONVERT(DATE, TDA.DATA_INCLUSAO) AS DATA,
            TDA.DEVEDOR_ID, TC.FANTASIA AS CONTRATANTE,
            TDA.USUARIO_INCLUSAO AS OPERADOR,
            TD.DESCRICAO,
            case when TD.SE_DISCADOR = 's' then 1 else 0 end as 'TRABALHADO',
            case when TD.SE_PRODUTIVO = 's' then 1 else 0 end as 'PRODUTIVO',
            case when TD.SE_PRODUTIVO = 's' then 0 else 1 end as 'IMPRODUTIVO',
            case when TD.SE_PROMESSA = 's' then 1 else 0 end as 'PROMESSA',]
            COLUNA_VALOR.VALOR_TOTAL 
        FROM tbdevedor_acionamento TDA WITH(NOLOCK) 
        INNER JOIN tbacao_cobranca TD WITH(NOLOCK) ON TD.ACAO_ID = TDA.ACAO_ID 
        INNER JOIN tbcontratante TC WITH(NOLOCK) ON TC.CONTRATANTE_ID = TDA.CONT_ID 
        INNER JOIN ( SELECT T
                        2.DEVEDOR_ID, 
                        SUM(T2.VALOR) VALOR_TOTAL 
                        FROM tbtitulo T2 WITH(NOLOCK) 
                        WHERE T2.CONT_ID IN ('192','93','200') 
                        GROUP BY T2.DEVEDOR_ID) COLUNA_VALOR ON COLUNA_VALOR.DEVEDOR_ID = TDA.DEVEDOR_ID 
        WHERE TDA.CONT_ID IN ('192','93','200') 
        AND CAST(TDA.DATA_INCLUSAO AS DATE) = GETDATE()
        AND DATEPART(HOUR, TDA.DATA_INCLUSAO) <=  DATEPART(HOUR, GETDATE())
        """

# Executando a consulta e criando um DataFrame diretamente
dados = pd.read_sql(query, conn)
print('Conexão com Banco de Dados foi realizada com Sucesso')

# Criando uma nova coluna 'VALOR_PRODUTIVO' com base na condição 'PRODUTIVO' == 1
dados['VALOR_PRODUTIVO'] = dados.apply(lambda row: dados.loc[row.name, 'VALOR_TOTAL'] if row['PRODUTIVO'] == 1 else 0, axis=1)

# Criando uma nova coluna 'VALOR_PROMESSA' com base na condição 'PROMESSA' == 1
dados['VALOR_PROMESSA'] = dados.apply(lambda row: dados.loc[row.name, 'VALOR_TOTAL'] if row['PROMESSA'] == 1 else 0, axis=1)

# Criando uma nova coluna 'VALOR_IMPRODUTIVO' com base na condição 'IMPRODUTIVO' == 1
dados['VALOR_IMPRODUTIVO'] = dados.apply(lambda row: dados.loc[row.name, 'VALOR_TOTAL'] if row['IMPRODUTIVO'] == 1 else 0, axis=1)


# Realizado o Agrupamento da Minha Base para criação da minha Base
Base_01 = dados.groupby(['CONTRATANTE','OPERADOR']).agg(
    #Soma Trabalhado
    TRABALHADO = ('TRABALHADO','sum'),
    #Soma Produtivo
    PRODUTIVO = ('PRODUTIVO','sum'),
    #Soma Promessa
    PROMESSA = ('PROMESSA','sum'),
    #Soma Valor_Produtivo
    VALOR_PRODUTIVO = ('VALOR_PRODUTIVO', 'sum'),
    # Soma Valor_Promessa
    VALOR_PROMESSA = ('VALOR_PROMESSA', 'sum'),
    #Soma Improdutivo
    IMPRODUTIVO = ('IMPRODUTIVO','sum'),
    # Soma Valor_Promessa
    VALOR_IMPRODUTIVO = ('VALOR_IMPRODUTIVO', 'sum')
).reset_index()

# Calculando o Porcentual Produtivo
Base_01['PERCT_PRODUTIVO'] = round(Base_01['PRODUTIVO'] / Base_01['TRABALHADO']*100,2)
Base_01['PERCT_PROMESSA'] = round(Base_01['PROMESSA'] / Base_01['TRABALHADO']*100,2)

# Alterando o Formato das Colunas Valores, para REAL
Base_01['VALOR_PRODUTIVO'] = Base_01['VALOR_PRODUTIVO'].apply(lambda valor: f'R$ {valor:,.2f}')
Base_01['VALOR_PROMESSA'] = Base_01['VALOR_PROMESSA'].apply(lambda valor: f'R$ {valor:,.2f}')
Base_01['VALOR_IMPRODUTIVO'] = Base_01['VALOR_IMPRODUTIVO'].apply(lambda valor: f'R$ {valor:,.2f}')

# Alterando o Formato das Colunas PORCENTUAIS
Base_01['PERCT_PRODUTIVO'] = Base_01['PERCT_PRODUTIVO'].apply(lambda valor: f'{valor:,.2f}%')
Base_01['PERCT_PROMESSA'] = Base_01['PERCT_PROMESSA'].apply(lambda valor: f'{valor:,.2f}%')

# Alterando os Nomes das Colunas para Adpatação em Foto
Base_01 = Base_01.rename(columns={'VALOR_PRODUTIVO': 'R$_PRODUTIVO'})
Base_01 = Base_01.rename(columns={'VALOR_PROMESSA': 'R$_PROMESSA'})
Base_01 = Base_01.rename(columns={'VALOR_IMPRODUTIVO': 'R$_IMPRODUTIVO'})
Base_01 = Base_01.rename(columns={'PERCT_PRODUTIVO': '%PRODUTIVO'})
Base_01 = Base_01.rename(columns={'PERCT_PROMESSA': '%PROMESSA'})

# Realiza a troca do cravamento (Envio de 2° Via) para (Contato sem Agendamento)
dados['DESCRICAO'] = dados['DESCRICAO'].replace('ENVIO DE 2° VIA', 'CONTATO SEM AGENDAMENTO')

# Criando Base de Dados das Tabulações Produtivas
dados_p = dados.loc[dados['PRODUTIVO'] == 1]

# Criando Base de Dados das Tabulações Improdutivas
dados_i = dados.loc[dados['IMPRODUTIVO'] == 1]

# Realizado a Agrupamento para criação da 2 Base
Base_02 = dados_p.groupby(['CONTRATANTE','DESCRICAO']).agg(
    QTDE = ('TRABALHADO','count'),
    VALOR = ('VALOR_TOTAL', 'sum')
).reset_index()

# Mudado para 3 casas decimais
Base_02['VALOR'] = Base_02['VALOR'].apply(lambda valor: f'R$ {valor:,.2f}')

# Realizado a Agrupamento para criação da 3 Base
Base_03 = dados_i.groupby(['CONTRATANTE','DESCRICAO']).agg(
    QTDE = ('TRABALHADO','count'),
    VALOR = ('VALOR_TOTAL', 'sum')
).reset_index()

# Mudado para 3 casas decimais
Base_03['VALOR'] = Base_03['VALOR'].apply(lambda valor: f'R$ {valor:,.2f}')


# Criando Imagem da Primeira Tabela

# Criando uma figura e eixo vazios
fig, ax = plt.subplots(figsize=(10, 6))
# Tamanhos personalizados das colunas (em proporção)
col_widths = [0.15, 0.15, 0.1, 0.1, 0.1, 0.15, 0.15, 0.1, 0.15, 0.1, 0.1]
# Removendo eixos
ax.axis('off')
# Adicionando um título à tabela
titulo = "Acompanhamento por Operador"
ax.set_title(titulo, fontsize=32, fontweight='bold', loc='center', pad=20)
# Criando uma tabela com os dados do DataFrame
tab = table(ax, Base_01, loc='center', cellLoc='center', colWidths=col_widths)
# Personalizando o estilo da tabela
tab.auto_set_font_size(False)
tab.set_fontsize(12)
tab.scale(2.2, 2.2) # Ajuste o tamanho da tabela conforme necessário
# Personalizando células específicas
for i in range(len(Base_01.columns)):
    tab.get_celld()[0, i].set_facecolor("#33BC14") # Fundo amarelo para a primeira linha (cabeçalho)
    tab.get_celld()[0, i].set_fontsize(14) # Tamanho de fonte maior para o cabeçalho
    tab.get_celld()[0, i].set_text_props(weight='bold') # Texto em negrito para o cabeçalho
    # ... Continue personalizando outras células, como bordas, cores de fundo, cores de texto, etc.
# Salvando a figura como uma imagem
plt.savefig(r'\\DISCO\LOCAL\ONDE\DESEJA\SALVAR\IMAGEM\tabela_imagem_1.png', bbox_inches='tight', pad_inches=0.5)
#plt.show()


# Criando uma figura com dois subplots, uma coluna e duas linhas

fig, axes = plt.subplots(2, 1, figsize=(12, 8))
# Tamanhos personalizados das colunas (em proporção)
col_widths = [0.15, 0.30, 0.1, 0.1, 15]
# Dados das tabelas (substitua Base_02 e Base_03 pelos seus DataFrames)
bases = [Base_02, Base_03]
pads = [100,0]
# Títulos das tabelas
titulos = ["Acionamentos Produtivos", "Acionamentos Improdutivos"]
# Loop para criar as duas tabelas
for i, ax in enumerate(axes):
    # Removendo eixos
    ax.axis('off')
    # Adicionando um título à tabela
    ax.set_title(titulos[i], fontsize=14, fontweight='bold', pad=pads[i])
    # Criando uma tabela com os dados do DataFrame
    tab = table(ax, bases[i], loc='center', cellLoc='center', colWidths=col_widths)
    # Personalizando o estilo da tabela (se necessário)
    tab.auto_set_font_size(False)
    tab.set_fontsize(12)
    tab.scale(2.2, 2.2) # Ajuste o tamanho da tabela conforme necessário
    # Personalizando células específicas (se necessário)
    for j in range(len(bases[i].columns)):
        tab.get_celld()[0, j].set_facecolor("#33BC14") # Fundo Verde para a primeira linha (cabeçalho)
        tab.get_celld()[0, j].set_fontsize(14) # Tamanho de fonte maior para o cabeçalho
        tab.get_celld()[0, j].set_text_props(weight='bold') # Texto em negrito para o cabeçalho
        # ... Continue personalizando outras células, como bordas, cores de fundo, cores de texto, etc.
# Ajustando o espaço entre os subplots
plt.subplots_adjust(hspace=0.7)
# Salvando a figura como uma imagem (opcional)
plt.savefig(r'\\DISCO\LOCAL\ONDE\DESEJA\SALVAR\IMAGEM\tabela_imagem_2.png', bbox_inches='tight', pad_inches=0.5)
#plt.show()



# Etapa de Envio via Telegram Automatico

# define o token do seu bot do Telegram
TOKEN = 'TOKEN_DO_SEU_BOT_DO_TELEGRAM'

# inicializa o objeto bot
bot = Bot(token=TOKEN)

# Incluir código do grupo
GRUPO = 'CÓDIGO_DO_GRUPO_PARA_ENVIAR_OU_USUARIO'

caminho_imagem_1 = r'\\DISCO\LOCAL\ONDE\DESEJA\SALVAR\IMAGEM\tabela_imagem_1.png'
caminho_imagem_2 = r'\\DISCO\LOCAL\ONDE\DESEJA\SALVAR\IMAGEM\tabela_imagem_2.png'

# define uma função assíncrona para enviar a foto 1
async def enviar_foto():
    with open(caminho_imagem_1, 'rb') as imagem:
        await bot.send_photo(chat_id=GRUPO, photo=InputFile(imagem))

# define uma função assíncrona para enviar a foto 2 
async def enviar_foto2():
    with open(caminho_imagem_2, 'rb') as imagem:
        await bot.send_photo(chat_id=GRUPO, photo=InputFile(imagem))

# chama a função assíncrona usando asyncio 1
loop = asyncio.get_event_loop()
loop.run_until_complete(enviar_foto())

# chama a função assíncrona usando asyncio 2 
loop = asyncio.get_event_loop()
loop.run_until_complete(enviar_foto2())
