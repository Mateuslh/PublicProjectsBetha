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
                'idIntegracao': encurtar(sistema, tipo_registro, item['nome'].upper(), item['datanascimento'],
                                         item['sexo']),
                'aluno': {
                    'pessoa': {
                        'nome': item['nome'],
                        'dataNascimento': item['datanascimento'],
                        'sexo': item['sexo'],
                        'complemento': {}
                    }
                }
            }
            if 'id_gerado' in item and item['id_gerado'] is not None:
                dado['aluno'].update({'id': item['id_gerado']})
            if 'id_pessoa' in item and item['id_pessoa'] is not None:
                dado['aluno']['pessoa'].update({'id':item['id_pessoa']})
            if 'nomefantasia' in item and item['nomefantasia'] is not None:
                dado['aluno']['pessoa'].update({'nomeFantasia': item['nomefantasia']})
            if 'logradouro' in item and 'numero' in item and 'bairro' in item and 'municipio' in item and item['logradouro'] is not None and item['numero'] is not None and item['bairro'] is not None and item['municipio'] is not None:
                dado['aluno'].update({'enderecos':[]})
                enderecoAluno = {
                    'logradouro': item['logradouro'],
                    'bairro': item['bairro'],
                    'municipio': {
                        'id': item['municipio']
                    },
                    'numero': item['numero'],
                    'localizacaoZona': item['zona']
                }

                if 'cep' in item and item['cep'] is not None:
                    enderecoAluno.update({'cep': item['cep']})
                if 'complemento' in item and item['complemento'] is not None:
                    enderecoAluno.update({'complemento': item['complemento']})
                dado['aluno']['enderecos'].append(enderecoAluno)
            if 'telefones' in item and item['telefones'] is not None:
                dado['aluno']['pessoa'].update({
                    'telefones': []
                })
                lista = item['telefones'].split('%||%')
                if len(lista) > 0:
                    for listacampo in lista:
                        campo = listacampo.split('%|%')
                        dado['aluno']['pessoa']['telefones'].append({
                            'descricao': campo[0],
                            'tipoNumero': campo[1],
                            'tipo': campo[2],
                            'telefone': campo[3],
                            'observacao': campo[4]
                        })
            if 'permiteenviosms' in item and item['permiteenviosms'] is not None:
                dado['aluno'].update({'permiteEnvioSms': item['permiteenviosms']})
            if 'emails' in item and item['emails'] is not None:
                dado['aluno']['pessoa'].update({
                    'emails': []
                })
                lista = item['emails'].split('%||%')
                if len(lista) > 0:
                    for listacampo in lista:
                        campo = listacampo.split('%|%')
                        dado['aluno']['pessoa']['emails'].append({
                            'descricao': campo[0],
                            'email': campo[1],
                            'tipo': campo[2]
                        })
            if 'permiteenvioemail' in item and item['permiteenvioemail'] is not None:
                dado['aluno'].update({'permiteEnvioEmail': item['permiteenvioemail']})
            if 'responsaveis' in item and item['responsaveis'] is not None:
                dado['aluno'].update({
                    'responsaveis': []
                })
                lista = item['responsaveis'].split('%||%')
                if len(lista) > 0:
                    for listacampo in lista:
                        campo = listacampo.split('%|%')
                        dado['aluno']['responsaveis'].append({
                            'responsavel': {
                                'id': int(campo[0])
                            },
                            "permiteRetirarAluno": False,
                            "diaSemana": [],
                            "parentesco": campo[1],
                            "outroParentesco": campo[2]
                        })
            if 'filiacoes' in item and item['filiacoes'] is not None:
                dado['aluno'].update({
                    'filiacoes': []
                })
                lista = item['filiacoes'].split('%||%')
                if len(lista) > 0:
                    for listacampo in lista:
                        campo = listacampo.split('%|%')
                        dado['aluno']['filiacoes'].append({
                            'filiacao': {
                                'id': int(campo[0])
                            },
                            "permiteRetirarAluno": False,
                            "diaSemana": [],
                            "ehResponsavel": True,
                            "tipo": campo[1],
                            "natureza": campo[2]
                        })
            if 'estadocivil' in item and item['estadocivil'] is not None:
                dado['aluno']['pessoa'].update({'estadoCivil': item['estadocivil']})
            if 'religiao' in item and item['religiao'] is not None:
                dado['aluno'].update({'religiao': {'id':item['religiao']}})
            if 'grauinstrucao' in item and item['grauinstrucao'] is not None:
                dado['aluno']['pessoa'].update({'grauInstrucao': item['grauinstrucao']})
            if 'dataobito' in item and item['dataobito'] is not None:
                dado['aluno']['pessoa'].update({
                    'obito': {
                        'dataObito': item['dataobito']
                    }
                })
            if 'municipionascimento' in item and item['municipionascimento'] is not None:
                dado['aluno']['pessoa'].update({
                    'municipioNascimento': {
                        'id': item['municipionascimento']
                    }
                })
            if 'paisorigem' in item and item['paisorigem'] is not None:
                dado['aluno'].update({'paisOrigem': {'id':item['paisorigem']}})
            if 'rg' in item and item['rg'] is not None:
                dado['aluno']['pessoa'].update({'rg': item['rg']})
            if 'certidaocivil' in item and item['certidaocivil'] is not None:
                dado['aluno'].update({'certidaoCivil': item['certidaocivil']})
            if 'modelocertidao' in item and item['modelocertidao'] is not None:
                dado['aluno'].update({'modeloCertidao': item['modelocertidao']})
            if 'numerotermo' in item and item['numerotermo'] is not None:
                dado['aluno'].update({'numeroTermo': item['numerotermo']})
            if 'numerocertidao' in item and item['numerocertidao'] is not None:
                dado['aluno'].update({'numeroCertidao': item['numerocertidao']})
            if 'folhacertidao' in item and item['folhacertidao'] is not None:
                dado['aluno'].update({'folhaCertidao': item['folhacertidao']})
            if 'livrocertidao' in item and item['livrocertidao'] is not None:
                dado['aluno'].update({'livroCertidao': item['livrocertidao']})
            if 'emissaocertidao' in item and item['emissaocertidao'] is not None:
                dado['aluno'].update({'emissaoCertidao': item['emissaocertidao']})
            if 'municipiocertidao' in item and item['municipiocertidao'] is not None:
                dado['aluno'].update({'municipioCertidao': {'id': item['municipiocertidao']}})
            if 'cartoriocertidao' in item and item['cartoriocertidao'] is not None:
                dado['aluno'].update({'cartorioCertidao': { 'id':item['cartoriocertidao']}})
            if 'numeroreservista' in item and item['numeroreservista'] is not None:
                dado['aluno']['pessoa']['complemento'].update({'numeroReservista': item['numeroreservista']})
            if 'pis' in item and item['pis'] is not None:
                dado['aluno']['pessoa'].update({'pis': item['pis']})
            if 'cpf' in item and item['cpf'] is not None:
                dado['aluno']['pessoa'].update({'cpf': item['cpf']})
            if 'raca' in item and item['raca'] is not None:
                dado['aluno']['pessoa']['complemento'].update({'raca': item['raca']})
            if 'deficiencia' in item and item['deficiencia'] is not None:
                dado['aluno'].update({'alunoDeficiencias':[]})
                deficiencias = item['deficiencia'].split(',')
                for deficiencia in deficiencias:
                    defici = deficiencia.split('|')
                    dado['aluno']['alunoDeficiencias'].append({
                        'deficiencia': {
                            'id':int(defici[0]),
                            'nome':defici[1]
                        }
                    })
            if 'possuisuperdotacao' in item and item['possuisuperdotacao'] is not None:
                dado['aluno'].update({'possuiSuperdotacao': item['possuisuperdotacao']})
            # print(f'@ Dado(s) gerado(s) ({contador}): ', dado)
            lista_dado.append(dado)
            lista_controle.append(formatar([dado['aluno']], item['id_desktop'])[0])
    except Exception as e:
        print(f'* Erro ao executar função "enviar" {e}')
    finally:
        return {'lista_controle': lista_controle, 'lista_dado': lista_dado}
