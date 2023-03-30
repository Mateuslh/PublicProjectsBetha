from re import search

from configuracao.conexao import consultar
from configuracao.funcao import encurtar
from json import dumps

limite = 50
sistema = 1
tipo_registro = search('([^\\\]+(?=\.py$))', __file__).group(1)
endereco = f'https://educacao.betha.cloud/educacao/conversao/api/{tipo_registro}/'
lote = f'https://educacao.betha.cloud/educacao/conversao/api/lotes/'


def formatar(registros, id_desktop=None):
    registros_formatados = []
    try:
        if len(registros) > 0:
            for item in registros:
                # if id_desktop is None:
                #     id_desktop = consultar("select id as id_desktop FROM modules.componente_curricular where trim(left(upper(replace(nome,'  ',' ')),60)) = {} limit 1".format(item['descriaco'].upper()))[0]['id_desktop']
                dado = {
                    'sistema': sistema,
                    'tipo_registro': tipo_registro,
                    'hash_chave_dsk': encurtar(sistema, tipo_registro, item['descricao'].upper()),
                    'id_desktop': id_desktop if id_desktop is not None else None,
                    'descricao_tipo_registro': f'Cadastro de {tipo_registro}',
                    'json': dumps(item),
                    'i_chave_dsk1': item['descricao'].upper()
                }
                if 'id' in item and item['id'] is not None:
                    dado.update({'id_gerado': item['id']})
                elif 'idGerado' in item and item['idGerado'] is not None:
                    dado.update({'id_gerado': item['idGerado'][[id_registro for id_registro in item['idGerado']][-1]]})
                registros_formatados.append(dado)
    except Exception as e:
        print(f'* Erro ao executar função "formatar" {e}')
    finally:
        return registros_formatados


def enviar(registros):
    lista_dado = []
    lista_controle = []
    try:
        total = len(registros)
        contador = 0
        for item in registros:
            contador += 1
            print(f'\r- Gerando JSON: {contador}/{total}', '\n' if contador == total else '', end='')
            dado = {
                'idIntegracao': encurtar(sistema, tipo_registro, item['descricao'].upper()),
                'disciplina': {
                    'inep': {
                        'id': item['inep']
                    },
                    'descricao': item['descricao'],
                    'sigla': item['sigla']
                }
            }
            # print(f'@ Dado(s) gerado(s) ({contador}): ', dado)
            lista_dado.append(dado)
            lista_controle.append(formatar([dado['disciplina']], item['id_desktop'])[0])
    except Exception as e:
        print(f'* Erro ao executar função "enviar" {e}')
    finally:
        return {'lista_controle': lista_controle, 'lista_dado': lista_dado}
