import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import re
import logging
from datetime import datetime

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def validate_file(file_path):
    return os.path.isfile(file_path)

def create_message(sender_email, receiver_email, cc_email, subject, body, file_path, imagem):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = ", ".join(receiver_email)
    message['Cc'] = ", ".join(cc_email) if cc_email else None
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    attach_file(message, file_path)
    attach_file(message, imagem)
    return message

def attach_file(message, file_path):
    attachment = open(file_path, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(file_path)}')
    attachment.close()
    message.attach(part)

def send_email(sender_email, sender_app_password, receiver_email, cc_email, subject, body, file_path, imagem):
    """
    Envia um e-mail com anexos.

    :param sender_email: E-mail do remetente.
    :param sender_app_password: Senha de aplicativo do e-mail do remetente.
    :param receiver_email: Lista de e-mails dos destinatários principais.
    :param cc_email: Lista de e-mails dos destinatários em cópia carbono.
    :param subject: Assunto do e-mail.
    :param body: Corpo do e-mail.
    :param file_path: Caminho do arquivo a ser anexado.
    :param imagem: Caminho da imagem a ser anexada.
    :raises ValueError: Se algum e-mail for inválido.
    :raises FileNotFoundError: Se o arquivo ou imagem não for encontrado.
    :raises smtplib.SMTPException: Se ocorrer um erro ao enviar o e-mail.
    """
    if not all(validate_email(email) for email in receiver_email + cc_email):
        raise ValueError("Um ou mais e-mails são inválidos.")

    if not validate_file(file_path):
        raise FileNotFoundError(f"Arquivo {file_path} não encontrado.")

    if not validate_file(imagem):
        raise FileNotFoundError(f"Imagem {imagem} não encontrada.")

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    message = create_message(sender_email, receiver_email, cc_email, subject, body, file_path, imagem)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_app_password)
            recipients = receiver_email + cc_email if cc_email else receiver_email
            server.sendmail(sender_email, recipients, message.as_string())
        logger.info('Enviado com Sucesso')
    except smtplib.SMTPException as e:
        logger.error(f"Erro ao enviar e-mail: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")

if __name__ == "__main__":
    sender_email = 'Email_Atual@Email.com.br'
    sender_app_password = 'SENHA_EMAIL'

    receiver_email = ['Email@01.com', 'Email@02.com']
    cc_email = ['Email@03.com', 'Email@04.com']

    subject_date = datetime.now().strftime("%d/%m/%Y")
    subject = f"Assunto do E-mail | {subject_date}"
    body = 'Bom dia !\n\n   Segue os Dados solicitados com Imagem demostrativa para acompanhamento.\n\nAtenciosamente\nFulano de Tal'

    file_path = r"Caminho\completo\do\arquivo\nome_do_Arquivo.txt"
    imagem = r'Caminho\completo\da\imagem\nome_da_Imagem.png'

    send_email(sender_email, sender_app_password, receiver_email, cc_email, subject, body, file_path, imagem)
    
    