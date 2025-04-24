import paramiko
import time
import os

def baixar_arquivo_sftp(local_path, remote_path, hostname, username, private_key, retries=5, chunk_size=1024 * 1024):
    """
    Envia um arquivo grande em partes menores, recomeçando caso a conexão falhe.

    Parâmetros:
    - local_path: Caminho do arquivo local.
    - remote_path: Caminho do arquivo no servidor.
    - hostname: Endereço do servidor SFTP.
    - username: Nome de usuário para autenticação.
    - private_key: Chave privada para autenticação ou senha.
    - retries: Número de tentativas em caso de falha.
    - chunk_size: Tamanho do bloco de escrita (1MB por padrão).
    
    """
    for attempt in range(retries):
        transport = None
        sftp = None
        file_size = 0
        bytes_baixados = 0

        try:
            # Conectar ao servidor
            print(f"Tentativa {attempt + 1} de {retries} para baixar {remote_path}...")

            transport = paramiko.Transport((hostname, 22))
            transport.set_keepalive(10)  # Mantém a conexão ativa
            transport.connect(username=username, password=private_key)
            sftp = paramiko.SFTPClient.from_transport(transport)

            # Obter tamanho total do arquivo
            file_size = sftp.stat(remote_path).st_size
            print(f"Tamanho do arquivo: {file_size / (1024 * 1024):.2f} MB")

            # Verifica se o arquivo já foi baixado parcialmente
            if os.path.exists(local_path):
                bytes_baixados = os.path.getsize(local_path)
                print(f"Arquivo já baixado parcialmente: {bytes_baixados / (1024 * 1024):.2f} MB")
            else:
                bytes_baixados = 0

            # Abrir arquivo local no modo append para continuar o download
            with sftp.file(remote_path, "rb") as remote_file, open(local_path, "ab") as local_file:
                remote_file.seek(bytes_baixados)  # Pula para a posição onde parou

                while bytes_baixados < file_size:
                    data = remote_file.read(chunk_size)  # Lê um pedaço do arquivo
                    if not data:
                        break  # Download completo

                    local_file.write(data)  # Escreve no arquivo local
                    bytes_baixados += len(data)

                    # Exibe progresso
                    print(f"\rProgresso: {bytes_baixados / file_size:.2%} ({bytes_baixados / (1024 * 1024):.2f} MB baixados)", end="")

            print(f"\nArquivo '{os.path.basename(remote_path)}' baixado com sucesso!")
            return True

        except Exception as e:
            print(f"\nErro ao baixar '{remote_path}' (tentativa {attempt + 1}): {e}")

        finally:
            if sftp:
                sftp.close()
            if transport:
                transport.close()

        time.sleep(2)  # Espera antes da próxima tentativa

    print(f"\nFalha ao baixar '{remote_path}' após {retries} tentativas.")
    return False