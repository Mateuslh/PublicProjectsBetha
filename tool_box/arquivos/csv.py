import csv

# Escreve lista de dicts em csv
def escrever_csv(lista_de_dicts, nome_arquivo):
    if not lista_de_dicts:
        return

    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo_csv:
        fieldnames = lista_de_dicts[0].keys()
        escritor = csv.DictWriter(arquivo_csv, fieldnames=fieldnames)
        escritor.writeheader()
        for linha in lista_de_dicts:
            escritor.writerow(linha)

# Retorna lista de dicts
def ler_csv(nome_arquivo, delimiter=",", ordem_cabecalhos=None):
    lista_de_dicionarios = []

    with open(nome_arquivo, mode='r', newline='') as arquivo_csv:
        leitor_csv = csv.DictReader(arquivo_csv, delimiter=delimiter, fieldnames=ordem_cabecalhos)
        for linha in leitor_csv:
            lista_de_dicionarios.append(linha)

    return lista_de_dicionarios

# Essa funcao recebe uma lista de dict da funcao ler_csv e retorna os campos escolhidos
def buscar_campos_especificos(lista_de_dicionarios, campos):
    resultados = []

    for dicionario in lista_de_dicionarios:
        resultado = {}
        for campo in campos:
            if campo in dicionario:
                resultado[campo] = dicionario[campo]
            else:
                resultado[campo] = None
        resultados.append(resultado)

    return resultados


# Esta função lê um arquivo CSV e retorna apenas os registros que retornam True para a função parametrizada.
def filtrar_registros_csv(nome_arquivo, criterio):
    registros_filtrados = []
    with open(nome_arquivo, mode='r', newline='') as arquivo_csv:
        leitor_csv = csv.DictReader(arquivo_csv)
        for linha in leitor_csv:
            if criterio(linha):
                registros_filtrados.append(linha)
    return registros_filtrados
