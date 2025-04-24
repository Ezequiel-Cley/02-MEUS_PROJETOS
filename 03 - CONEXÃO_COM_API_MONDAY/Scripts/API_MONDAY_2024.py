# Importando Biblioteca para Extração de API
import requests
# Importando Pandas para tratamento e leitura dos dados
import pandas as pd
import datetime

# Acessar componentes do SISTEAMA OPERCIONAL
import os

import asyncio
# Instalar o pacote (python-telegram-bot)
from telegram import Bot

# Configurado Report para Envio de Informações em caso de erro por Telegram!!!
# define o token do seu bot do Telegram
TOKEN = 'INSERIR_TOKEN_DO_SEU_BOT_TELEGRAM'
# inicializa o objeto bot
bot = Bot(token=TOKEN)
# Incluir código do grupo
GRUPO = 'INSERIR_CÓDIGO_DO_GRUPO_QUE_DESEJA_ENVIAR_O_ALERTA'

# Key de acesso a API
apiKey = "Inseri_API_DO_SEU_ADM_MONDAY"

# URL de Acesso a API > Monday
apiUrl = "https://api.monday.com/v2"

# Variavel para Parametro do Requeset Liberar acesso
headers = {"Authorization" : apiKey}

# Query de linguagem GRAPHQL para acesso de API
query2 = '{  boards(page:1) {    id    name    items_page{      items{        id        name        column_values{          column{           title           }          id          text        }      }    }  }}'
data = {'query' : query2}

print('Realizado a solicitação de conexão com a API')

# Realizado conexão com API
r = requests.post(url=apiUrl, json=data, headers=headers) # make request

# Criando Variavel para armazenar o status de conexão com a API
status = r.status_code

# Cria um Loop para realizar diversas tentativas de conexão até conseguir uma conexão com sucesso na API
while status != 200:
    # Realizado conexão com API
    r = requests.post(url=apiUrl, json=data, headers=headers) # make request
    # Armazena novo Status de conexão com A API 
    status = r.status_code
    # Cria logica para armazenar quantidade de tentativas de conexão para acompanhamento em caso de necessidade!!!
    T = 0
    T = T + 1
    print(f'A foram realizadas {T} de conexão com a API')

#Condição de validação se conexão com API foi um Sucesso
if r.status_code == 200:
    # Usando o json_normalize para transformar os dados em um DataFrame
    df = pd.json_normalize(r.json(), record_path=['data', 'boards', 'items_page', 'items','column_values'], meta=[['data', 'boards', 'items_page', 'items','name'],['data', 'boards', 'name'],['data', 'boards', 'items_page', 'items', 'id'] ])
else:
    print(f"Falha na Atualização de Relatório, Erro: Status de conexão com a API {r.status_code}")
    # Mensagem que você deseja enviar
    mensagem = f"Falha na Atualização de Relatório, Erro: Status de conexão com a API {r.status_code}"
    # Enviar a mensagem desejada
    # Cria uma função assicronica para Enviar_mensagem():
    async def enviar_foto():
        await bot.send_message(chat_id=GRUPO, text=mensagem)
    # chama a função assíncrona usando asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(enviar_foto()) 
    exit()

print("Conexão com API Monday realizada com Sucesso ")    

# Organiza as colunas para realizar a alteração de linhas para colunas!!!
df = df[['data.boards.items_page.items.id','data.boards.name','data.boards.items_page.items.name', 'column.title', 'text']]

# Realiza a troca dos nomes das colunas para melhor entedimento da Base
df.rename(columns={'data.boards.items_page.items.id': 'ID',
                   'data.boards.name': 'Quadro',
                   'data.boards.items_page.items.name': 'Elemento',
                   'column.title':'title'},
          inplace = True)

# Use a função pivot para transformar os dados de linhas para colunas mantendo as colunas (ID,Quadro e Elemento)
df_pivot = df.pivot(index=['ID', 'Quadro', 'Elemento'], columns='title', values='text').reset_index()

# Use o método fillna para preencher os valores nulos em 'Rotina' com os valores de 'ROTINA'
#df_pivot['Rotina'].fillna(df_pivot['ROTINA'], inplace=True)

df_pivot = df_pivot[['ID','Quadro','Elemento', 'Responsável', 'Empresa','Rotina','Área','Prioridade','Status','Data','Tempo Estimado','Texto','Subitems']]

# Armazena informação da data atual para acrescenter ao nome do arquivo Historico 
data_atual = str(datetime.date.today())
# Caminho para salvar o arquivo Historico do dia
Caminho = (f'//Caminho/do/HISTORICO//HISTORICO_{data_atual}.parquet')

# Salva o arquivo historico para Incluisão de novos dados e dados antigos:
df_pivot.to_parquet(Caminho, index=False)

# Buscar todos os arquivos de uma diretorio
pasta = ('//Caminho/do/HISTORICO/')
# lê arquivos na pasta
arquivos = os.listdir(pasta)
# Cria um dataframe vazio para realizar o salvamento de varios arquivos em unico Dataframe no Loop 
df_Historica = pd.DataFrame()

# Criando Loop para acessar todos os arquivos do diretorio e unifica-los
for i in arquivos:
    path = f'{pasta}/{i}'
    df_path = pd.read_parquet(f'{path}')
    df_Historica = pd.concat([df_Historica, df_path])
    
    
# Unificando as bases de dados Historicas com a extraida atual pela API
df = pd.concat([df_Historica,df_pivot])

# Remover as duplicadas entre o arquivo historico e Datframe novo extraido pela API
if pd.notna(df['ID']).unique() == True:
    df.drop_duplicates(subset=['ID'], ignore_index=True, inplace= True)
else:
    # Mensagem que você deseja enviar
    mensagem = f"Falha na Atualização de Relatório, Erro: Coluna ID, contém dados nulos!!!"
    # Enviado a mensagem no Grupo
    # Cria uma função assicronica para Enviar_mensagem():
    async def enviar_foto():
        await bot.send_message(chat_id=GRUPO, text=mensagem)
    # chama a função assíncrona usando asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(enviar_foto()) 
    exit()
    
# Realizado a alteração do Tipo da Coluna Data
df['Tempo Estimado'] = pd.to_numeric(df['Tempo Estimado'])

# Criando uma função para criar uma nova coluna com tempo em segundo
def tempo_segundo(Col):
    Col = (Col * 60)
    Col = (Col * 60)
    return Col
# Aplicando a função para a nova coluna para obter os dados em Segundos
df['Tempo_Estimado_Seg'] = df['Tempo Estimado'].apply(tempo_segundo)

# Criando Coluna com a data Atual
def data_hora_atual(Col):
    Col = str(datetime.datetime.today())
    return Col

df['Data_Atual'] = ''
df['Data_Atual'] = df['Data_Atual'].apply(data_hora_atual)

print("Tratamento realizado com Sucesso")    

#Salvando o arquivo Completo em Unico Arquivo CSV
df.to_csv('//Caminho/completo/que/deseja/salvar/Dados_Monday_Consolidado.csv', sep = '|', index=False)

print("Relatório de Acompanhamento de Rotinas DP Atualizado com Sucesso")

# Mensagem que você deseja enviar
mensagem = f"Relatório de Acompanhamento de Rotinas, Atualizado com Sucesso"
#Enviar_mensagem():
# Cria uma função assicronica para Enviar_mensagem():
async def enviar_foto():
    await bot.send_message(chat_id=GRUPO, text=mensagem)
# chama a função assíncrona usando asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(enviar_foto()) 