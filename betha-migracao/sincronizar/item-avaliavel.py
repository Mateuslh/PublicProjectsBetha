from re import search
from configuracao.funcao import encurtar
from json import dumps
from time import sleep
from configuracao.conexao import TOKENUSER, ACCESSUSER, consultar, executar
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
                    'hash_chave_dsk': encurtar(sistema, tipo_registro, item['ano'],
                                               item['estabelecimento_gerado'],
                                               item['disciplina_gerado'],
                                               item['tipo'],
                                               item['periodo'],
                                               item['turma'],
                                               item['modoAvaliacao']),
                    'descricao_tipo_registro': f'Cadastro de {tipo_registro}',
                    'json': dumps(item),
                    'i_chave_dsk1': item['ano'],
                    'i_chave_dsk2': item['estabelecimento_gerado'],
                    'i_chave_dsk3': item['disciplina_gerado'],
                    'i_chave_dsk4': item['tipo'],
                    'i_chave_dsk5': item['periodo'],
                    'i_chave_dsk6': item['turma'],
                    'i_chave_dsk7': item['modoAvaliacao']
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
            endereco = f"https://api.educacao.betha.cloud/educacao/api/matricula/turma/{id['id_gerado']}/filhos"

            payload = {}
            headers = {
                'authorization': TOKENUSER,
                'user-access': ACCESSUSER
            }

            response = requests.request("GET", endereco, headers=headers, data=payload)
            response = response.json()

            if 'code' in response and response['code'] != 200:
                print('Erro, verificar requisição de tela!')
                return {'lista_controle': lista_controle, 'lista_dado': lista_dados}
            if 'message' in response and response['message'] is not None:
                print("Erro: ",response['message'])
                continue
            print(f'\r- Gerando JSON: {contador}/{total}', '\n' if contador == total else '', end='')
            for item in response:
                for itemAvaliavel in item['itensAvaliaveis']:
                    dado = {
                        'idIntegracao': encurtar(sistema, tipo_registro, item['anoLetivo']['id'],
                                               item['estabelecimento']['id'],
                                               item['etapaMatrizDisciplina']['disciplina']['id'],
                                               itemAvaliavel['tipoPeriodo'],
                                               itemAvaliavel['descricao'],
                                               item['pai']['id'],
                                               itemAvaliavel['modoAvaliacao']),
                        'itemAvaliavel': {
                            'ano': item['anoLetivo']['id'],
                            'estabelecimento_gerado': item['estabelecimento']['id'],
                            'disciplina_gerado': item['etapaMatrizDisciplina']['disciplina']['id'],
                            'tipo': itemAvaliavel['tipoPeriodo'],
                            'id': itemAvaliavel['id'],
                            'periodo': itemAvaliavel['descricao'],
                            'turma': item['pai']['id'],
                            'modoAvaliacao': itemAvaliavel['modoAvaliacao']
                        }
                    }

                    lista_dados.append(dado)

                    lista_controle.append(formatar([dado['itemAvaliavel']])[0])
    except Exception as e:
        print(f'* Erro ao executar função "buscar" {e}')
        exit()
    finally:
        return {'lista_controle': lista_controle, 'lista_dado': lista_dados}

