import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Link Publico para acesso a planilha com os dados do Forms
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQo-SmZSvyZj6UR7I0MofPqI5aG_GxWpH2PJV-UvSPI2tFOeT0SU-bVEFVFbgwt3bDKqf_2D2heBcnb/pub?output=csv'

# Carregar respostas do formulário
df = pd.read_csv(url)

# Configurar o conteúdo do e-mail
email_remetente = "seu_email@gmail.com"
email_destinatario = "destinatario_email@gmail.com"
senha = "sua_senha"
 
assunto = "Respostas do Forms - Atualização Diária"
corpo = df.to_html()  # Converte os dados para tabela HTML

# Configurar o e-mail
msg = MIMEMultipart()
msg['From'] = email_remetente
msg['To'] = email_destinatario
msg['Subject'] = assunto

msg.attach(MIMEText(corpo, 'html'))

# Enviar o e-mail
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(email_remetente, senha)
    server.sendmail(email_remetente, email_destinatario, msg.as_string())

print("E-mail enviado com sucesso!")
