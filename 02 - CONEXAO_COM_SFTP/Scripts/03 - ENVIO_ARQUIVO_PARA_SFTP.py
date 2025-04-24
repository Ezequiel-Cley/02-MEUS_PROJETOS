# Importando Bibliotecas para Envio dos Arquivos
import paramiko
import os
from datetime import date
from time import sleep

# Definindo sua conexão com API para realizar conexão:
ip = 'Inserir_Seu_IP' # Exemplo "00.00.00.000"
Usuario = 'Inserir_Usuario_do_SFTP'
Senha =  'Inserir_Senha_do_SFTP'

# Cria uma variável de data para identificar os arquivos do Dia Atual!!!
formatted_date = date.today().strftime('%d/%m/%Y').replace("/", "")

# Cria variáveis para o caminho dos arquivos
# Definindo Varivael com o Caminho completo do local onde deve enviar o arquivo:
file_path_s = fr'\Caminho\do\SFTP\para\Colocar\Arquivo\Nome_do_Arquivo{str(formatted_date)}.TXT'
# Definindo o Local onde se encontra o arquivo que deve ser encaminhado:
file_path_r = fr'Disco\Local\Onde\Esta\Arquivo\Para\Enviar\Nome_do_Arquivo.{str(formatted_date)}.TXT'

# Verifica se o arquivo existe para realizar o envio para o SFTP:
if not os.path.exists(file_path_r):
    raise FileNotFoundError("O arquivo não foi encontrado")

# Conectando-se ao SFTP
# Armazendo IP para Conexão com SFTP
transport = paramiko.Transport((ip, 22))
# Armazenando Usuario e Senha para Conexão com SFTP
transport.connect(username= Usuario, password= Senha)
# Realizado Tentativa de Conexão com SFTP
sftp = transport.open_sftp_client()
print("Conexão estabelecida... ")

# Aguardando um Pouco antes de fazer Envio para evitar erro de conexão ao enviar o arquivo
sleep(3)

# Realiza uma tentativa de conexão para envio do Arquivo
try:
    # Realiza o envio do arquivo via SFTP
    sftp.put(file_path_r, file_path_s)
    print("Upload realizado com sucesso")

except Exception as e:
    print("Erro ao realizar o upload:", e)

finally:
    # Fecha a conexão
    sftp.close()
    transport.close()
