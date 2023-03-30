from re import search
from configuracao.funcao import encurtar
from json import dumps

limite = 100
sistema = 1
tipo_registro = search('([^\\\]+(?=\.py$))', __file__).group(1)
endereco = f'https://educacao.betha.cloud/service-layer/v2/api/{tipo_registro}'
lote = f'https://educacao.betha.cloud/service-layer/v2/api/lotes/'


def formatar(registros, id_desktop=None):
    registros_formatados = []
    try:
        if len(registros) > 0:
            for item in registros:
                dado = {
                    'sistema': sistema,
                    'tipo_registro': tipo_registro,
                    'hash_chave_dsk': encurtar(sistema, tipo_registro, item['periodoAvaliativo']['id'],item['turma']['id'], item['estabelecimento']['id'],item['anoLetivo']['id']),
                    'id_desktop': id_desktop if id_desktop is not None else None,
                    'descricao_tipo_registro': f'Cadastro de {tipo_registro}',
                    'json': dumps(item),
                    'i_chave_dsk1': item['periodoAvaliativo']['id'],
                    'i_chave_dsk2': item['turma']['id'],
                    'i_chave_dsk3': item['estabelecimento']['id'],
                    'i_chave_dsk4': item['anoLetivo']['id']
                }
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
                'idIntegracao': encurtar(sistema, tipo_registro, item['periodoavaliativo'],item['turma'], item['estabelecimento'],item['anoletivo']),
                'conteudo': {
                    'anoLetivo': {
                        'id': item['anoletivo']
                    },
                    'estabelecimento': {
                        'id': item['estabelecimento']
                    },
                    'periodoAvaliativo': {
                        'id': item['periodoavaliativo']
                    },
                    'turma': {
                        'id': item['turma']
                    },
                    'tipoPeriodo': item['tipoperiodo'],
                    'status': item['status']
                }
            }
            # print(f'@ Dado(s) gerado(s) ({contador}): ', dado)
            lista_dado.append(dado)
            lista_controle.append(formatar([dado['conteudo']], item['id_desktop'])[0])
    except Exception as e:
        print(f'* Erro ao executar função "enviar" {e}')
    finally:
        return {'lista_controle': lista_controle, 'lista_dado': lista_dado}
