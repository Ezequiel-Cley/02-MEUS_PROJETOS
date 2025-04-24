import logging
import time
import traceback

# Configurar o logger
logging.basicConfig(filename='log_execucao.log', 
                    level=logging.INFO,  # Nível de log, você pode mudar para DEBUG para mais detalhes
                    format='%(asctime)s - %(levelname)s - %(message)s')

def funcao_principal():
    try:
        # Registro do início do processo
        logging.info("Iniciando o processo X")
        start_time = time.time()  # Capturar o tempo inicial

        # Passo 1 - Exemplo de ação
        logging.info("Executando o passo 1")
        time.sleep(1)  # Simulação de uma operação demorada

        # Passo 2 - Exemplo de ação
        logging.info("Executando o passo 2")
        time.sleep(2)  # Simulação de outra operação demorada

        # Passo 3 - Simulação de erro
        logging.info("Executando o passo 3")
        raise ValueError("Erro simulado no passo 3")  # Simulação de erro

    except Exception as e:
        # Registro do erro com detalhes
        logging.error(f"Erro ocorrido: {str(e)}")
        logging.error(traceback.format_exc())

    finally:
        # Registro do tempo total de execução
        end_time = time.time()
        duration = end_time - start_time
        logging.info(f"Processo finalizado em {duration:.2f} segundos.")

# Executar a função principal
funcao_principal()
