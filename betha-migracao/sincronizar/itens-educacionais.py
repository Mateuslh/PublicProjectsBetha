from re import search
from configuracao.funcao import encurtar
from json import dumps
from configuracao.conexao import TOKENUSER, ACCESSUSER, APPCONTEXT, consultar, executar
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
                                                item['turma'],
                                                item['disciplina'],
                                                item['estabelecimento'],
                                                item['estabelecimento_desk'],
                                                item['tipoFrequencia']),
                    'descricao_tipo_registro': f'Cadastro de {tipo_registro}',
                    'json': dumps(item),
                    'i_chave_dsk1': item['turma'],
                    'i_chave_dsk2': item['disciplina'],
                    'i_chave_dsk3': item['estabelecimento'],
                    'i_chave_dsk4': item['estabelecimento_desk'],
                    'i_chave_dsk5': item['tipoFrequencia']
                }
                if 'id' in item and item['id'] is not None:
                    dado.update({'id_gerado': item['id']})
                registros_formatados.append(dado)
    except Exception as e:
        print(f'* Erro ao executar função "formatar" {e}')
    finally:
        return registros_formatados


def buscar(lista_registro):
    lista_dados = []
    lista_controle = []
    try:
        total = len(lista_registro)
        contador = 0
        for id in lista_registro:
            contador += 1

            endereco = f"https://api.educacao.betha.cloud/educacao/api/matricula/turma/{id['id_gerado']}/frequencias/registros-faltas"

            payload = {}
            headers = {
                'authorization': TOKENUSER,
                'user-access': ACCESSUSER,
                'app-context': APPCONTEXT
            }

            response = requests.request("GET", endereco, headers=headers, data=payload)
            response = response.json()

            if 'code' in response and response['code'] != 200:
                print('Erro, verificar requisição de tela!')
                return []

            print(f'\r- Gerando JSON: {contador}/{total}', '\n' if contador == total else '', end='')
            # print(response,id['id_gerado'])
            for itemEducacional in response['itensEducacionais']:
                dado = {
                    'idIntegracao': encurtar(sistema, tipo_registro, id['id_gerado'],
                                               itemEducacional['descricao'],
                                               id['estabelecimento'],
                                               id['idesc'],
                                               response['configuracao']['tipoRegistroFrequencia']
                                            ),
                    'itemEducacional': {
                        'id': itemEducacional['id'],
                        'turma': id['id_gerado'],
                        'disciplina': itemEducacional['descricao'],
                        'estabelecimento':id['estabelecimento'],
                        'estabelecimento_desk':id['idesc'],
                        'tipoFrequencia': response['configuracao']['tipoRegistroFrequencia']
                    }
                }
                lista_dados.append(dado)
                lista_controle.append(formatar([dado['itemEducacional']])[0])
    except Exception as e:
        print(f'* Erro ao executar função "buscar" {e}')
        exit()
    finally:
        return {'lista_controle': lista_controle, 'lista_dado': lista_dados}

