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
                                                item['nome'],
                                                item['uf']),
                    'descricao_tipo_registro': f'Cadastro de {tipo_registro}',
                    'json': dumps(item),
                    'i_chave_dsk1': item['nome'],
                    'i_chave_dsk2': item['uf']
                }
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
        total = 5626
        contador = 0
        maisPagina= True
        nRegistros = 100
        iniciaEm = 0
        while maisPagina:


            endereco = f"https://e-gov.betha.com.br/glb/service-layer/v2/api/municipios?iniciaEm={iniciaEm}&nRegistros={nRegistros}"

            payload = {}
            headers = {
                'authorization': AUTORIZACAO
            }

            response = requests.request("GET", endereco, headers=headers, data=payload)
            response = response.json()
            # print(response)
            iniciaEm += nRegistros
            maisPagina = response['maisPaginas']

            if 'code' in response and response['code'] != 200:
                print('Erro, verificar GLB!')
                return []



            for municipio in response['conteudo']:
                contador += 1
                print(f'\r- Gerando JSON: {contador}/{total}', '\n' if contador == total else '', end='')
                dado = {
                    'idIntegracao': encurtar(sistema, tipo_registro,
                                               municipio['nome'],
                                               municipio['uf']
                                            ),
                    'municipio': {
                        'id': municipio['idGerado']['iMunicipios'],
                        'nome': municipio['nome'],
                        'uf': municipio['uf']
                    }
                }
                lista_dados.append(dado)
                lista_controle.append(formatar([dado['municipio']])[0])
    except Exception as e:
        print(f'* Erro ao executar função "buscar" {e}')
        exit()
    finally:
        return {'lista_controle': lista_controle, 'lista_dado': lista_dados}

