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
                    'hash_chave_dsk': encurtar(sistema, tipo_registro, item['descricao']),
                    'descricao_tipo_registro': f'Cadastro de {tipo_registro}',
                    'json': dumps(item),
                    'id_desktop': None,
                    'i_chave_dsk1': item['descricao']
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
                'idIntegracao': encurtar(sistema, tipo_registro, item['descricao']),
                'conteudo': {
                    'descricao': item['descricao'],
                    'tipoCursoAperfeicoamento': item['tipocursoaperfeicoamento'],
                    'tipoCursoOutro': item['tipocursooutro'],
                    'formacaoContinuada': item['formacaocontinuada']
                }
            }
            if 'areaformacaocontinuada' in item and item['areaformacaocontinuada'] is not None:
                dado['conteudo'].update({
                    'areaFormacaoContinuada': item['areaformacaocontinuada']
                })
            if 'areaformacaocontinuadaoutro' in item and item['areaformacaocontinuadaoutro'] is not None:
                dado['conteudo'].update({
                    'areaFormacaoContinuadaOutro': item['areaformacaocontinuadaoutro']
                })
            if 'estabelecimento' in item and item['estabelecimento'] is not None:
                dado['conteudo'].update({
                    'estabelecimento': item['estabelecimento']
                })
            if 'cargahorariaemsegundos' in item and item['cargahorariaemsegundos'] is not None:
                dado['conteudo'].update({
                    'cargaHorariaEmSegundos': item['cargahorariaemsegundos']
                })
            # print(f'@ Dado(s) gerado(s) ({contador}): ', dado)
            lista_dado.append(dado)
            lista_controle.append(formatar([dado['conteudo']])[0])
    except Exception as e:
        print(f'* Erro ao executar função "enviar" {e}')
    finally:
        return {'lista_controle': lista_controle, 'lista_dado': lista_dado}
