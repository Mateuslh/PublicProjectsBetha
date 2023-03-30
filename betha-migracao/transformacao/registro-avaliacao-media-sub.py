from re import search
from configuracao.funcao import encurtar
from json import dumps

limite = 100
sistema = 1
tipo_registro = search('([^\\\]+(?=\.py$))', __file__).group(1)
endereco = f'https://educacao.betha.cloud/service-layer/v2/api/registro-avaliacao'
lote = f'https://educacao.betha.cloud/service-layer/v2/api/lotes/'


def formatar(registros, id_desktop=None):
    registros_formatados = []
    try:
        if len(registros) > 0:
            for item in registros:
                dado = {
                    'sistema': sistema,
                    'tipo_registro': tipo_registro,
                    'hash_chave_dsk': encurtar(sistema, tipo_registro, id_desktop),
                    'id_desktop': id_desktop if id_desktop is not None else None,
                    'descricao_tipo_registro': f'Cadastro de {tipo_registro}',
                    'json': dumps(item),
                    'i_chave_dsk1': id_desktop
                }
                if 'id' in item and item['id'] is not None:
                    dado.update({'id_gerado': item['id']})
                elif 'idGerados' in item and item['idGerados'] is not None:
                    dado.update({'id_gerado': item['idGerados']['idMatricula']})
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
                'idIntegracao': encurtar(sistema, tipo_registro, item['id_desktop']),
                'conteudo': {
                    'anoLetivo': {
                        'id': item['anoletivo']
                    },
                    'estabelecimento': {
                        'id': item['estabelecimento']
                    },
                    'itemAvaliavel': {
                        'id': item['itemavaliavel']
                    },
                    'enturmacao': {
                        'id': item['enturmacao']
                    }
                }
            }
            if 'id_gerado' in item and item['id_gerado'] is not None:
                dado['conteudo'].update({'id': item['id_gerado']})
            if item['tiponota'] == 'DESCRITIVO':
                if item['parecer'] is None:
                    descritiva=''
                else:
                    descritiva = item['parecer']
                if item['mediafinal'] is not None:
                    descritiva += ' Nota numérica: '+str(item['mediafinal'])
                dado['conteudo'].update({
                    'modoAvaliacao': 'DESCRITIVO',
                    'notaDescritiva': descritiva
                })
            else:
                # if item['notanumerica'] is None:
                #     dado['conteudo'].update({
                #         'modoAvaliacao': 'CONCEITO',
                #         'notaConceito': {
                #             'id': item['notaconceito']
                #         }
                #     })
                # else:
                nota = 0.0
                if item['mediafinal'] is not None:
                    if item['mediafinal'] > 10:
                        nota = 10
                    else:
                        nota = item['mediafinal']
                dado['conteudo'].update({
                    'notaNumerica': nota,
                    'modoAvaliacao': 'NUMERICO',
                    'parecer': item['parecer']
                })

            # print(f'@ Dado(s) gerado(s) ({contador}): ', dado)
            lista_dado.append(dado)
            lista_controle.append(formatar([dado['conteudo']], item['id_desktop'])[0])
    except Exception as e:
        print(f'* Erro ao executar função "enviar" {e}')
    finally:
        return {'lista_controle': lista_controle, 'lista_dado': lista_dado}
