import os
import time

# Função para extração de Dados do Log
def read_log(path):

    """
    Lê um arquivo de log e filtra as linhas que começam com "Finished" e "Error" e extrai as informações da data de modificação do arquivo.

    Parameters:
        path (str): O caminho do arquivo de log.

    Returns:
        tuple: Uma tupla contendo duas strings:
            - A primeira string contém as linhas que começam com "Error", ou 'None' se não houver.
            - A segunda string contém as linhas que começam com "Finished".
            - A Terceira String contém a data de modificação do arquivo 'dt_m'
    """

    
# Abra o arquivo de log em modo de leitura
    try:
        with open(path, 'r', encoding='utf-8') as arquivo_log:
            linhas = arquivo_log.readlines()
    except UnicodeDecodeError:
        print("Não foi possível ler usando UTF-8. Tentando outras codificações.")

        # Tente ler o arquivo usando Latin-1
        with open(path, 'r', encoding='latin-1') as arquivo_log:
            linhas = arquivo_log.readlines()

    # Use uma função lambda para filtrar as linhas que começam com "Finished"
    finished_lines = str(list(filter(lambda linha: linha.startswith('Finished'), linhas)))

    # Imprima as linhas que começam com "Error"
    error_lines = str(list(filter(lambda linha: linha.startswith('Error'), linhas)))
    if error_lines == '[]':

        error_lines = None
        
    else:
        error_lines = error_lines.replace('[','').replace(']','')

    finished_lines = finished_lines.replace('[','').replace(']','')
    
    # Extraido data de modificação do arquivo
    dt_m = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(time.ctime(os.path.getmtime(f'{path}') ) ) ) 
    
    return error_lines, finished_lines, dt_m