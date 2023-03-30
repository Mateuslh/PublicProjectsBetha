from configuracao.funcao import excluir, buscar
from os import getenv
from dotenv import load_dotenv
from os.path import join, dirname
from re import search

load_dotenv(join(dirname(__file__), '../.env'))


def iniciar_exclusao(lista_registro, tipo='CLOUD'):
    for registro in lista_registro:
        print(f"\n# Operação exclusão {search(r'([a-z0-9-_]+)(/)$', registro['endereco']).group(1)}")
        autorizacao = getenv("TOKENUSER") if registro['tela'] else getenv("TOKEN")
        if not (autorizacao.lower().startswith('bearer')):
            autorizacao = f'bearer {autorizacao}'
        usuario = getenv("ACCESSUSER") if registro['tela'] else None
        if tipo == 'CLOUD':
            excluir(buscar(registro['endereco'], 20, usuario, autorizacao), registro['endereco'], usuario, autorizacao)
        elif tipo == 'FLY':
            lista_dado = []
            for i in range(registro['quantidade']):
                lista_dado.append({
                    'id': i,
                    'descricao': registro['descricao'],
                    'identificador': registro['identificador'],
                })
            excluir(lista_dado, registro['endereco'], usuario, autorizacao, tipo)
        else:
            print('* Tipo invalido para exclusão')
