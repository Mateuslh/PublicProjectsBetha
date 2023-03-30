from re import search
from configuracao.funcao import encurtar
from json import dumps

limite = 10
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
                    'hash_chave_dsk': encurtar(sistema, tipo_registro,id_desktop,item['anoLetivo']['id']),
                    'descricao_tipo_registro': f'Cadastro de {tipo_registro}',
                    'id_desktop': id_desktop if id_desktop is not None else None,
                    'json': dumps(item),
                    'i_chave_dsk1': id_desktop,
                    'i_chave_dsk2': item['anoLetivo']['id']
                }
                if 'id' in item and item['id'] is not None:
                    dado.update({'id_gerado': item['id']})
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
                'idIntegracao': encurtar(sistema, tipo_registro,item['id_desktop'],item['anoletivo']),
                'conteudo': {
                    'descricao': item['descricao'],
                    'descricaoPeriodoAvaliativo': item['descricaoperiodoavaliativo'],
                    'tipoPeriodoAvaliativo': item['tipoperiodoavaliativo'],
                    'calendario': {
                        'dataInicial': item['datainicial'],
                        'dataFinal': item['datafinal'],
                        'observacao': item['observacao'],
                        'diasLetivosSemana': item['diasletivossemana'].split(',')
                    },
                    'calendarioEstabelecimento': {
                        'id': item['calendarioestabelecimento']
                    },
                    'estabelecimento':{
                        'id': item['estabelecimento']
                    },
                    'matrizCurricular': {
                        'id': item['matrizcurricular']
                    },
                    'anoLetivo': {
                        'id': item['anoletivo']
                    }
                }
            }

            if 'periodosavaliativos' in item and item['periodosavaliativos'] is not None:
                dado['conteudo'].update({
                    'periodosAvaliativos': []
                })
                lista = item['periodosavaliativos'].split('||')
                lista.sort()
                if len(lista) > 0:
                    for i in lista:
                        periodos = i.split(',')
                        dado['conteudo']['periodosAvaliativos'].append({
                            'descricao': periodos[0],
                            'dataFinal': periodos[1],
                            'dataInicial': periodos[2]
                        })
            # print(f'@ Dado(s) gerado(s) ({contador}): ', dado)
            lista_dado.append(dado)
            lista_controle.append(formatar([dado['conteudo']],item['id_desktop'])[0])
    except Exception as e:
        print(f'* Erro ao executar função "enviar" {e}')
    finally:
        return {'lista_controle': lista_controle, 'lista_dado': lista_dado}
