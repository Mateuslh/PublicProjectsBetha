from re import search
from configuracao.funcao import encurtar
from json import dumps

limite = 10
sistema = 1
tipo_registro = search('([^\\\]+(?=\.py$))', __file__).group(1)
endereco = f'https://educacao.betha.cloud/educacao/conversao/api/{tipo_registro}/'
lote = f'https://educacao.betha.cloud/educacao/conversao/api/lotes/'


def formatar(registros, id_desktop=None):
    registros_formatados = []
    try:
        if len(registros) > 0:
            for item in registros:
                dado = {
                    'sistema': sistema,
                    'tipo_registro': tipo_registro,
                    'hash_chave_dsk': encurtar(sistema, tipo_registro, item['pessoa']['nome'].upper(),
                                               item['pessoa']['dataNascimento'],
                                               item['pessoa']['sexo']),
                    'id_desktop': id_desktop if id_desktop is not None else None,
                    'descricao_tipo_registro': f'Cadastro de {tipo_registro}',
                    'json': dumps(item),
                    'i_chave_dsk1': item['pessoa']['nome'].upper(),
                    'i_chave_dsk2': item['pessoa']['dataNascimento'],
                    'i_chave_dsk3': item['pessoa']['sexo']
                }
                if 'id' in item and item['id'] is not None:
                    dado.update({'id_gerado': item['id']})
                elif 'idGerado' in item and item['idGerado'] is not None:
                    dado.update({'id_gerado': item['idGerado'][[id_registro for id_registro in item['idGerado']][-1]]})
                registros_formatados.append(dado)
    except Exception as error:
        print(f'* Erro ao executar função "formatar" {error}')
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
                'idIntegracao': encurtar(sistema, tipo_registro, item['nome'].upper(), item['datanascimento'],
                                         item['sexo']),
                'filiacao': {
                    'pessoa': {
                        'nome': item['nome'],
                        'dataNascimento': item['datanascimento'],
                        'sexo': item['sexo']
                    }
                }
            }
            if 'cpf' in item and item['cpf'] is not None:
                dado['filiacao']['pessoa'].update({'cpf': item['cpf']})
            if 'pis' in item and item['pis'] is not None:
                dado['filiacao']['pessoa'].update({'pis': item['pis']})
            if 'rg' in item and item['rg'] is not None:
                dado['filiacao']['pessoa'].update({'rg': item['rg']})
            if 'numerotermo' in item and item['numerotermo'] is not None:
                dado['filiacao']['pessoa'].update({'numeroTermo': item['numerotermo']})
            if 'telefones' in item and item['telefones'] is not None:
                dado['filiacao']['pessoa'].update({
                    'telefones': []
                })
                lista = item['telefones'].split('%||%')
                if len(lista) > 0:
                    for listacampo in lista:
                        campo = listacampo.split('%|%')
                        dado['filiacao']['pessoa']['telefones'].append({
                            'descricao': campo[0],
                            'tipoNumero': campo[1],
                            'tipo': campo[2],
                            'telefone': campo[3],
                            'observacao': campo[4]
                        })
            if 'emails' in item and item['emails'] is not None:
                dado['filiacao']['pessoa'].update({
                    'emails': []
                })
                lista = item['emails'].split('%||%')
                if len(lista) > 0:
                    for listacampo in lista:
                        campo = listacampo.split('%|%')
                        dado['filiacao']['pessoa']['emails'].append({
                            'descricao': campo[0],
                            'email': campo[1],
                            'tipo': campo[2]
                        })
            # print(f'@ Dado(s) gerado(s) ({contador}): ', dado)
            lista_dado.append(dado)
            lista_controle.append(formatar([dado['filiacao']], item['id_desktop'])[0])
    except Exception as e:
        print(f'* Erro ao executar função "enviar" {e}')
    finally:
        return {'lista_controle': lista_controle, 'lista_dado': lista_dado}
