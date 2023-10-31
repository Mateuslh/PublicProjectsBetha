def extrair_substrings(string, campos):
    dicionario = {}
    for campo, (inicio, fim) in campos.items():
        if 0 <= inicio < len(string) and 0 <= fim < len(string) and inicio <= fim:
            dicionario[campo] = string[inicio:fim + 1]
    return dicionario


# extrair_substrings(linha,
#                    {
#                        "inscricao": (6, 14),
#                        "parcelas": (779, 947)
#                    })

def dividir_string(string, tamanho):
    if tamanho <= 0:
        raise ValueError("O tamanho deve ser maior que zero.")
    return [string[i:i+tamanho] for i in range(0, len(string), tamanho)]