# 📤 Envio de Mensagens com Anexos para Google Chat + Upload no Google Drive

Esta função em Python permite o envio de mensagens para espaços do **Google Chat**, com ou sem anexos. Quando um arquivo é especificado, ele é carregado em um **Drive Compartilhado** do Google Drive e compartilhado com o domínio da empresa, com um link acessível via Chat.

---
## Requisitos
Instalação das bibliotecas abaixo:
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client


## 🚀 Funcionalidade

- Envia mensagens de texto para um espaço específico no Google Chat.
- Se um arquivo for fornecido:
  - Faz upload do arquivo para um Drive Compartilhado.
  - Gera um link direto para o arquivo.
  - Compartilha o arquivo com permissão de leitura para o domínio `Seu_Dominio.com.br`.
  - Inclui o link do arquivo na mensagem enviada ao Chat.

---

## 🧾 Parâmetros da Função

```python
send_to_google_chat(caption: str, space_id: str, Id_Pasta: str, Dominio: str, file_path: Optional[str] = None)
