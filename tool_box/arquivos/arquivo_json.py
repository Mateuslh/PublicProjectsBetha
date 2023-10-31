import json

def escrever_em_json(data, nome_arquivo,modo="a"):
    with open(nome_arquivo,modo) as arquivo:
        json.dump(data, arquivo, indent=4)

def ler_de_json(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        data = json.load(arquivo)
    return data
