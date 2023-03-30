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
                    'hash_chave_dsk': encurtar(sistema, tipo_registro, item['descricao'].upper()),
                    'descricao_tipo_registro': f'Cadastro de {tipo_registro}',
                    'id_desktop': id_desktop if id_desktop is not None else None,
                    'json': dumps(item),
                    'i_chave_dsk1': item['descricao'].upper()
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
            # print(item)
            dado = {
                'idIntegracao': encurtar(sistema, tipo_registro, item['descricao'].upper()),
                'conteudo': {
                    'descricao': item['descricao'],
                    'tipoIdentificacao': item['tipoidentificacao'],
                    'tipoOrganizacao': item['tipoorganizacao'],
                    'diasLetivos': item['diasletivos'],
                    'situacaoCadastral': item['situacao'],
                    'curso': {
                        'id': item['curso']
                    }
                }
            }
            # print(f'@ Dado(s) gerado(s) ({contador}): ', dado)
            lista_dado.append(dado)
            lista_controle.append(formatar([dado['conteudo']],item['id_desktop'])[0])
    except Exception as e:
        print(f'* Erro ao executar função "enviar" {e}')
    finally:
        return {'lista_controle': lista_controle, 'lista_dado': lista_dado}
