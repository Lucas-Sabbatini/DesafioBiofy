CONTRACT_EXTRACTION_PROMPT = """
    Analise o seguinte texto de contrato e extraia as seguintes informações no formato JSON.
    Se uma informação não for encontrada ou não se aplicar, retorne um array vazio ([]) para listas, um objeto vazio ({{}}) para dicionários, ou `null` para strings e outros valores únicos.

    Estrutura do JSON esperada:
    {{
        "parties": [], // Lista de strings com os nomes das partes envolvidas
        "monetary_values": [], // Lista de strings com valores monetários encontrados (ex: "R$ 10.000,00", "mil dólares")
        "main_obligations": [], // Lista de strings com as obrigações principais de cada parte
        "additional_data": {{}}, // Dicionário com dados adicionais importantes (ex: "objeto": "locação de imóvel", "vigencia": "5 anos")
        "termination_clause": null // String com o texto da cláusula de rescisão, se existir, ou null
    }}

    Texto do Contrato:
    ---
    {contract_text}
    ---
    """