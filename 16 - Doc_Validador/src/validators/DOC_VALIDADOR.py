import pandas as pd

class DocumentoValidator:
    def __init__(self, documento: str):
        """Inicializa a classe com um documento (CPF ou CNPJ)."""
        self.documento = self._clean_documento(documento)
    
    def _clean_documento(self, documento: str) -> str:
        """Remove caracteres não numéricos do documento e valida se a entrada é válida."""
        if not isinstance(documento, str):
            raise ValueError("O documento deve ser uma string.")
        return ''.join(filter(str.isdigit, documento))
    
    def _is_sequence(self) -> bool:
        """Verifica se o documento é uma sequência de números repetidos."""
        return self.documento == self.documento[0] * len(self.documento)
    
    def _calculate_digit(self, base: str, weights: list) -> int:
        """Calcula um dígito verificador com base nos pesos fornecidos."""
        total = sum(int(num) * weight for num, weight in zip(base, weights))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder
    
    def _validate_cpf(self) -> bool:
        """Valida um CPF."""
        if len(self.documento) != 11 or not self.documento.isdigit() or self._is_sequence():
            return False
        
        # Calcula o primeiro dígito verificador
        first_digit = self._calculate_digit(self.documento[:9], list(range(10, 1, -1)))
        if first_digit != int(self.documento[9]):
            return False
        
        # Calcula o segundo dígito verificador
        second_digit = self._calculate_digit(self.documento[:10], list(range(11, 1, -1)))
        return second_digit == int(self.documento[10])
    
    def _validate_cnpj(self) -> bool:
        """Valida um CNPJ."""
        if len(self.documento) != 14 or not self.documento.isdigit() or self._is_sequence():
            return False
        
        # Pesos para os cálculos dos dígitos verificadores
        weights_first = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        weights_second = [6] + weights_first
        
        # Calcula o primeiro dígito verificador
        first_digit = self._calculate_digit(self.documento[:12], weights_first)
        if first_digit != int(self.documento[12]):
            return False
        
        # Calcula o segundo dígito verificador
        second_digit = self._calculate_digit(self.documento[:13], weights_second)
        return second_digit == int(self.documento[13])

    def validate_document(self) -> tuple:
        """Valida o documento e retorna o tipo e status."""
        if len(self.documento) == 11:
            is_valid = self._validate_cpf()
            return "CPF", "Válido" if is_valid else "Inválido"
        elif len(self.documento) == 14:
            is_valid = self._validate_cnpj()
            return "CNPJ", "Válido" if is_valid else "Inválido"
        else:
            return "Desconhecido", "Inválido"

    
    @staticmethod
    def validate_dataframe(df: pd.DataFrame, column_name: str, type_column: str, status_column: str) -> pd.DataFrame:
        """
        Valida uma coluna de documentos (CPFs ou CNPJs) em um DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame contendo os documentos.
            column_name (str): Nome da coluna com os documentos.
            type_column (str): Nome da coluna para o tipo do documento.
            status_column (str): Nome da coluna para o status do documento.
        
        Returns:
            pd.DataFrame: DataFrame atualizado com as novas colunas.
        """
        def validate_doc(doc):
            validator = DocumentoValidator(doc)
            return validator.validate_document()
        
        # Aplica a validação à coluna especificada
        df[[type_column, status_column]] = df[column_name].apply(
            lambda doc: pd.Series(validate_doc(doc))
        )
        return df
