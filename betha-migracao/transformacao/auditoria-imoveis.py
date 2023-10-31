from re import search
from configuracao.funcao import encurtar
from json import dumps

limite = 100
sistema = 335
tipo_registro = search('([^\\\]+(?=\.py$))', __file__).group(1)
endereco = 'https://tributos.betha.cloud/service-layer-tributos/api/registrosTabaux/'
lote = 'https://tributos.betha.cloud/service-layer-tributos/api/registrosTabaux/'


def formatar(registros, id_desktop=None):
    registros_formatados = []
    try:
        if len(registros) > 0:
            for item in registros:
                dado = {
                    'sistema': sistema,
                    'tipo_registro': tipo_registro,
                    'hash_chave_dsk': encurtar(sistema, tipo_registro, id_desktop,item["campo2"]),
                    'descricao_tipo_registro': f'Cadastro de {tipo_registro}',
                    'id_desktop': id_desktop if id_desktop is not None else None,
                    'json': dumps(item),
                    'i_chave_dsk1': id_desktop,
                    'i_chave_dsk2': item["campo2"]
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
                'idIntegracao': encurtar(sistema, tipo_registro, item['id_desktop'],item["dt_alteracoes"]),
                'registrosTabaux': {
                    "campo1": item["i_imoveis"],
                    "campo2": item["dt_alteracoes"],
                    "campo3": item["i_usuarios"],
                    "campo4": item["contrib"],
                    "campo5": item["valor_antigo"],
                    "campo6": item["valor_novo"],
                    "campo7": item["processo"],
                    "campo8": item["desc_campo"],
                    "campo9": item["insc_imo"],
                    "campo10": item["i_pessoas"],
                    "iTabelaAuxiliar": 20
                }
            }
            # print(f'@ Dado(s) gerado(s) ({contador}): ', dado)
            lista_dado.append(dado)
            lista_controle.append(formatar([dado['registrosTabaux']],item['id_desktop'])[0])
    except Exception as e:
        print(f'* Erro ao executar função "enviar" {e}')
    finally:
        return {'lista_controle': lista_controle, 'lista_dado': lista_dado}
