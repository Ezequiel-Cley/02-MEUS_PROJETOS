# === IMPORTANDO BIBLIOTECAS ===
import os
import mimetypes
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def send_to_google_chat(caption, space_id, Id_Pasta, Dominio="Seu_Dominio", file_path=None):
    """
    Envia uma mensagem (com ou sem arquivo) para um espaço do Google Chat e,
    caso especificado, faz upload do arquivo para um Drive Compartilhado.

    Parâmetros:
    ----------
    caption : str
        Texto da mensagem a ser enviada para o Google Chat.
    space_id : str
        ID do espaço no Google Chat (ex: 'spaces/AAA...').
    file_path : str, opcional
        Caminho completo do arquivo a ser enviado e publicado no Drive. Se None, apenas o texto é enviado.
    Id_Pasta: str
        ID da pasta onde o uploud do arquivo deve acontecer 
    Dominio: str
        Dominio para quais usuários devem visualizar os arquivos que você realizar uploud
    
    Requisitos:
    ----------
    - A conta Google usada deve ter acesso ao espaço do Chat e ao Drive Compartilhado.
    - É necessário que o arquivo de credenciais (`client_secret`) e o `token.json` estejam acessíveis.

    Observações:
    -----------
    - O arquivo é salvo em um Drive Compartilhado com ID fixo.
    - Após o upload, o arquivo é compartilhado com permissões de leitura para o domínio 'meirelesefreitas.com.br'.
    """
    
    # === SCOPES NECESSÁRIOS PARA GOOGLE CHAT E GOOGLE DRIVE ===
    SCOPES = [
        'https://www.googleapis.com/auth/chat.messages',
        'https://www.googleapis.com/auth/drive.file'
    ]

    #ID_DA_PASTA_PARA_ALOCAR_ARQUIVOS
    id_pasta_publicacao = Id_Pasta

    # === CAMINHOS DOS ARQUIVOS DE CREDENCIAIS ===
    CLIENT_SECRET_FILE = r"\\caminho\do\arquivo\Credencial\client_secret_123456789.apps.googleusercontent.com.json"
    TOKEN_FILE = r'\\caminho\do\arquivo\Token\token.json'

    try:
        creds = None

        # === CARREGA TOKEN EXISTENTE ===
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

        # === ATUALIZA OU GERA NOVO TOKEN ===
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())

        # === MENSAGEM SEM ARQUIVO ANEXADO ===
        if not file_path:
            message = {"text": f"{caption}"}

        # === MENSAGEM COM UPLOAD DE ARQUIVO PARA DRIVE COMPARTILHADO ===
        else:
            # Inicializa serviço do Google Drive
            drive_service = build('drive', 'v3', credentials=creds)

            # ID do Drive Compartilhado (substitua conforme necessário)
            shared_drive_id = id_pasta_publicacao

            # Metadados do arquivo
            file_metadata = {
                'name': os.path.basename(file_path),
                'parents': [shared_drive_id]
            }

            # Upload do arquivo
            media = MediaFileUpload(file_path, mimetype=mimetypes.guess_type(file_path)[0], resumable=True)
            file = drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id',
                supportsAllDrives=True
            ).execute()

            file_id = file.get('id')
            file_link = f"https://drive.google.com/uc?id={file_id}"

            # Torna o arquivo acessível para leitura no domínio
            drive_service.permissions().create(
                fileId=file_id,
                body={'type': 'domain', 'role': 'reader', 'domain': Dominio},
                supportsAllDrives=True
            ).execute()

            # Mensagem com link para o arquivo
            message = {
                "text": f"{caption}\n📎 Arquivo: [{os.path.basename(file_path)}]({file_link})"
            }

        # === ENVIO PARA GOOGLE CHAT ===
        chat_service = build('chat', 'v1', credentials=creds)
        chat_service.spaces().messages().create(
            parent=space_id,
            body=message
        ).execute()

        print("✅ Arquivo enviado com sucesso para o Google Chat!")

    except Exception as e:
        print("❌ Erro no envio via Google Chat:", e)