import paramiko
import os
import time

def enviar_arquivo_sftp(local_path, remote_path, hostname, username, private_key, retries=5, chunk_size=1024 * 1024):
    """
    Envia um arquivo grande em partes menores, recomeçando caso a conexão falhe.

    Parâmetros:
    - local_path: Caminho do arquivo local.
    - remote_path: Caminho do arquivo no servidor.
    - hostname: Endereço do servidor SFTP.
    - username: Nome de usuário para autenticação.
    - private_key: Chave privada para autenticação.
    - retries: Número de tentativas em caso de falha.
    - chunk_size: Tamanho do bloco de escrita (1MB por padrão).
    """
    
    file_size = os.path.getsize(local_path)
    print(f"Iniciando envio de '{local_path}' ({file_size / (1024 * 1024):.2f} MB) para '{remote_path}'...")

    for attempt in range(retries):
        transport = None
        sftp = None
        bytes_enviados = 0

        try:
            print(f"Tentativa {attempt + 1} de {retries} para enviar {local_path}...")
            
            transport = paramiko.Transport((hostname, 22))
            transport.set_keepalive(10)
            transport.connect(username=username, pkey=private_key)
            sftp = paramiko.SFTPClient.from_transport(transport)
            
            # Verifica se o arquivo já foi enviado parcialmente
            try:
                bytes_enviados = sftp.stat(remote_path).st_size
                print(f"Arquivo já enviado parcialmente: {bytes_enviados / (1024 * 1024):.2f} MB")
            except FileNotFoundError:
                bytes_enviados = 0

            # Abre o arquivo local e continua de onde parou
            with open(local_path, "rb") as local_file, sftp.file(remote_path, "ab") as remote_file:
                local_file.seek(bytes_enviados)  # Pula para a posição onde parou
                
                while bytes_enviados < file_size:
                    data = local_file.read(chunk_size)
                    if not data:
                        break
                    
                    remote_file.write(data)
                    bytes_enviados += len(data)

                    print(f"\rProgresso: {bytes_enviados / file_size:.2%} ({bytes_enviados / (1024 * 1024):.2f} MB enviados)", end="")

            print(f"\nArquivo '{os.path.basename(local_path)}' enviado com sucesso!")
            return True

        except Exception as e:
            print(f"\nErro ao enviar '{local_path}' (tentativa {attempt + 1}): {e}")
        
        finally:
            if sftp:
                sftp.close()
            if transport:
                transport.close()
        
        time.sleep(2)  # Espera antes da próxima tentativa

    print(f"\nFalha ao enviar '{local_path}' após {retries} tentativas.")
    return False
