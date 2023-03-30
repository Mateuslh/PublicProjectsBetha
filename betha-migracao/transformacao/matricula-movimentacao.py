from re import search
from configuracao.funcao import encurtar
from json import dumps

limite = 10
sistema = 1
tipo_registro = search('([^\\\]+(?=\.py$))', __file__).group(1)
endereco = f'https://educacao.betha.cloud/educacao/conversao/api/{tipo_registro}/'
lote = f'https://educacao.betha.cloud/educacao/conversao/api/lotes/'


def formatar(registros, id_desktop=None,id_desktopesc=None):
    registros_formatados = []
    try:
        if len(registros) > 0:
            for item in registros:
                dado = {
                    'sistema': sistema,
                    'tipo_registro': tipo_registro,
                    'hash_chave_dsk': encurtar(sistema, tipo_registro, id_desktop, id_desktopesc),
                    'id_desktop': id_desktop if id_desktop is not None else None,
                    'descricao_tipo_registro': f'Cadastro de {tipo_registro}',
                    'json': dumps(item),
                    'i_chave_dsk1': id_desktop,
                    'i_chave_dsk2': id_desktopesc
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
                'idIntegracao': encurtar(sistema, tipo_registro, item['id_desktop'], item['id_desktopesc']),
                'item': {
                    'matricula': {
                        'estabelecimento': {
                            'id': item['estabelecimento']
                        },
                        'anoLetivo':{
                            'id': item['anoletivo']
                        },
                        'vaga':{
                            'id': item['vaga']
                        },
                        'aluno':{
                            'id': item['aluno']
                        },
                        'type': item['type'],
                        'turno': item['turno'],
                        'tipo': item['tipo'],
                        'situacao': item['situacao'],
                        'data': item['data'],
                        'utilizarTransporteEscolar': item['utilizartransporteescolar'],
                        'responsavelTransporteEscolar': item['responsaveltransporteescolar']
                    },
                    'turma':{
                        'id': item['turma']
                    }
                }
            }
            if 'movimentos' in item and item['movimentos'] is not None:
                data, tipo = item['movimentos'].split(',')
                dado['item'].update({
                    'movimentacao': {
                        'tipo': tipo,
                        'data': data,
                    }
                })
                motivo = None
                if tipo == "TRANSFERENCIA":
                    motivo = 16
                elif tipo == "CANCELAMENTO":
                    motivo = 17
                elif tipo == "DEIXOU_DE_FREQUENTAR":
                    motivo = 10
                if motivo is not None:
                    dado['item']['movimentacao'].update({
                        'motivo': {
                            'id': motivo
                        }
                    })
            # print(f'@ Dado(s) gerado(s) ({contador}): ', dado)
            lista_dado.append(dado)
            lista_controle.append(formatar([dado['item']], item['id_desktop'],item['id_desktopesc'])[0])
    except Exception as e:
        print(f'* Erro ao executar função "enviar" {e}')
    finally:
        return {'lista_controle': lista_controle, 'lista_dado': lista_dado}
