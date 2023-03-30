from re import search
from configuracao.funcao import encurtar
from json import dumps
from configuracao.conexao import AUTORIZACAO, TOKENUSER, ACCESSUSER, APPCONTEXT, consultar, executar
import requests

sistema = 1
tipo_registro = search('([^\\\]+(?=\.py$))', __file__).group(1)


def formatar(registros):
    registros_formatados = []
    try:
        if len(registros) > 0:
            for item in registros:
                dado = {
                    'sistema': sistema,
                    'tipo_registro': tipo_registro,
                    'hash_chave_dsk': encurtar(sistema, tipo_registro,
                                                item['nome']),
                    'descricao_tipo_registro': f'Cadastro de {tipo_registro}',
                    'json': dumps(item),
                    'i_chave_dsk1': item['nome']
                }
                if 'cidade' in item and item['cidade'] is not None:
                    dado.update({'i_chave_dsk2': item['cidade']})
                if 'id' in item and item['id'] is not None:
                    dado.update({'id_gerado': item['id']})
                registros_formatados.append(dado)
    except Exception as e:
        print(f'* Erro ao executar função "formatar" {e}')
    finally:
        return registros_formatados


def buscar():
    lista_dados = []
    lista_controle = []
    try:
        total = 0
        contador = 0
        maisPagina= True
        nRegistros = 99
        iniciaEm = 0
        while maisPagina:
            endereco = f"https://educacao.betha.cloud/service-layer/v2/api/{tipo_registro}?offset={iniciaEm}&limit={nRegistros}"

            payload = {}
            headers = {
                'authorization': AUTORIZACAO
            }

            response = requests.request("GET", endereco, headers=headers, data=payload)
            response = response.json()
            # print(response)
            iniciaEm += nRegistros

            if 'code' in response and response['code'] != 200:
                print('Erro, verificar GLB!')
                return []

            maisPagina = response['hasNext']
            total = response['total']

            for cartorio in response['content']:
                contador += 1
                print(f'\r- Gerando JSON: {contador}/{total}', '\n' if contador == total else '', end='')
                dado = {
                    'idIntegracao': encurtar(sistema, tipo_registro,
                                               cartorio['nome']
                                            ),
                    'cartorio': {
                        'id': cartorio['id'],
                        'nome': cartorio['nome']
                    }
                }
                if 'municipio' in cartorio and cartorio['municipio'] is not None:
                    dado['cartorio'].update({
                        'cidade': cartorio['municipio']['nome']
                    })
                lista_dados.append(dado)
                lista_controle.append(formatar([dado['cartorio']])[0])
    except Exception as e:
        print(f'* Erro ao executar função "buscar" {e}')
        exit()
    finally:
        return {'lista_controle': lista_controle, 'lista_dado': lista_dados}