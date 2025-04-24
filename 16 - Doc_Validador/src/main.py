# src/main.py

from validators.DOC_VALIDADOR import DocumentoValidator  # Importação do módulo de validação

# Agora você pode usar a classe DocumentoValidator
documento = "12345678901"
validator = DocumentoValidator(documento)
print(validator.validate_document())

