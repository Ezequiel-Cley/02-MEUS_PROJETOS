# DocumentoValidator

O **DocumentoValidator** é uma biblioteca Python para validação de documentos como CPF e CNPJ. Ele verifica se os documentos estão no formato correto e se os dígitos verificadores são válidos, ajudando a garantir a integridade e autenticidade desses documentos.

## Funcionalidades

- Validação de CPF e CNPJ.
- Identificação de documentos válidos ou inválidos.
- Validação de um DataFrame de pandas contendo documentos, retornando o tipo de documento e o status de validade.

## Instalação

### Pré-requisitos

- Python 3.12.0
- Pandas==1.5.3

### Como instalar

1. Clone o repositório:

    ```bash
    git clone https://github.com/seu-usuario/documento-validator.git
    ```

2. Instale as dependências:

    Se você estiver utilizando um ambiente virtual (recomendado):

    ```bash
    cd documento-validator
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3. Instale as bibliotecas necessárias com o `pip`:

    ```bash
    pip install -r requirements.txt
    ```

## Uso

### Validação de um único documento (CPF ou CNPJ)

Exemplo de como validar um documento individual:

```python
from src.validators.documento_validator import DocumentoValidator

# Exemplo de CPF válido
documento = "123.456.789-09"
validator = DocumentoValidator(documento)
tipo, status = validator.validate_document()
print(f"Tipo: {tipo}, Status: {status}")
