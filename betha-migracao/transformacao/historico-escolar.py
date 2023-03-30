from re import search, sub, findall
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
                    'hash_chave_dsk': encurtar(sistema, tipo_registro, item['aluno']['id'], item['anoConclusao'],
                                               item['etapa'], item['situacao']),
                    'id_desktop': id_desktop if id_desktop is not None else None,
                    'descricao_tipo_registro': f'Cadastro de {tipo_registro}',
                    'json': dumps(item),
                    'i_chave_dsk1': item['aluno']['id'],
                    'i_chave_dsk2': item['anoConclusao'],
                    'i_chave_dsk3': item['etapa'],
                    'i_chave_dsk4': item['situacao']
                }
                if 'id' in item and item['id'] is not None:
                    dado.update({'id_gerado': item['id']})
                elif 'idGerado' in item and item['idGerado'] is not None:
                    dado.update({'id_gerado': item['idGerado'][[id_registro for id_registro in item['idGerado']][-1]]})
                registros_formatados.append(dado)
    except Exception as e:
        print(f'\n* Erro ao executar função "formatar" {e}')
    finally:
        return registros_formatados


def enviar(registros):
    lista_dado = []
    lista_controle = []
    listaBnc = []
    try:
        total = len(registros)
        contador = 0
        for item in registros:
            contador += 1
            print(f'\r- Gerando JSON: {contador}/{total}', '\n' if contador == total else '', end='')
            dado = {
                'idIntegracao': encurtar(sistema, tipo_registro, item['aluno'], item['anoconclusao'],
                                         item['etapa'], item['situacao']),
                'conteudo': {
                    'aluno': {
                        'id': item['aluno']
                    },
                    'municipio': {
                        'id': item['municipio']
                    },
                    'situacao': item['situacao'],
                    'anoConclusao': item['anoconclusao'],
                    'nivelModalidade': item['nivelmodalidade'],
                    'nivelEscolar': item['nivelescolar']
                }
            }
            if 'nomeestabelecimento' in item and item['nomeestabelecimento'] is not None:
                dado['conteudo'].update({'nomeEstabelecimento': item['nomeestabelecimento']})
            if 'situacaoespecifica' in item and item['situacaoespecifica'] is not None:
                dado['conteudo'].update({'situacaoEspecifica': item['situacaoespecifica']})
            if 'descricaocurso' in item and item['descricaocurso'] is not None:
                dado['conteudo'].update({'descricaoCurso': item['descricaocurso']})
            if 'conclusaoorigem' in item and item['conclusaoorigem'] is not None:
                dado['conteudo'].update({'conclusaoOrigem': item['conclusaoorigem']})
            if 'nomeestabelecimento' in item and item['nomeestabelecimento'] is not None:
                dado['conteudo'].update({'nomeEstabelecimento': item['nomeestabelecimento']})
            else:
                dado['conteudo'].update({'nomeEstabelecimento': 'Estabelecimento não informado!'})
            if 'etapa' in item and item['etapa'] is not None:
                dado['conteudo'].update({'etapa': item['etapa']})
            if 'percentualfrequencia' in item and item['percentualfrequencia'] is not None:
                dado['conteudo'].update({'percentualFrequencia': item['percentualfrequencia']})
            if 'cargahorariatotalemsegundos' in item and item['cargahorariatotalemsegundos'] is not None:
                dado['conteudo'].update({'cargaHorariaTotalEmSegundos': item['cargahorariatotalemsegundos']})
            if 'diasletivos' in item and item['diasletivos'] is not None:
                dado['conteudo'].update({'diasLetivos': item['diasletivos']})
            if 'tipoitemorganizacaocurricular' in item and item['tipoitemorganizacaocurricular'] is not None:
                dado['conteudo'].update({'tipoItemOrganizacaoCurricular': item['tipoitemorganizacaocurricular']})
            obs =''
            if 'componentes' in item and item['componentes'] is not None:
                dado['conteudo'].update({
                    'componentes': []
                })
                conteudo = item['componentes'].split('[OBS]')
                taman = len(conteudo)
                for itens in range(taman):
                    if itens == taman - 1:
                        if conteudo[itens] != '' and conteudo[itens] is not None:
                            if findall('^.*?[?=NotasObs]]', conteudo[itens]):
                                conteudo[itens] = sub('^.*?[?=NotasObs]]', '', conteudo[itens])
                                obs += ' OBS Notas:' + conteudo[itens]
                                continue
                    lista = conteudo[itens].split('\\n')
                    if lista [0] =='':
                        lista.pop(0)
                    tamanho = len(lista)
                    if tamanho > 0:
                        for i in range(tamanho):
                            if lista[i] == '':
                                continue
                            disciplina, dados = lista[i].split('=')
                            nota = dados.split('|')[0]
                            carga = 0
                            nota=nota.replace(',','.')
                            descritiva = None
                            numerica = None
                            try:
                                numerica = float(nota)
                                tipo = 'NUMERICO_DUAS_CASAS_DECIMAIS'
                            except Exception:
                                descritiva = nota
                                tipo = 'DESCRITIVA'
                            var = ''
                            iddisc, bnc = getdisciplina(disciplina)
                            componente = {
                                'tipoAvaliacao': tipo,
                                'notaNumerica': numerica,
                                'notaDescritiva': descritiva,
                                'cargaHorariaTotalEmSegundos': carga,
                                'orientacaoCurricular': bnc
                            }
                            if iddisc is not None:
                                componente.update({
                                    'itemOrganizacaoCurricular': {
                                        'id': iddisc
                                    }
                                })
                            dado['conteudo']['componentes'].append(componente)
            if 'observacao' in item and item['observacao'] is not None:
                obs = item['observacao'] + obs
            if len(obs)>600:
                obs = obs[:600]
            dado['conteudo'].update({'observacao': obs})

            # print(f'@ Dado(s) gerado(s) ({contador}): ', dado)
            lista_dado.append(dado)
            lista_controle.append(formatar([dado['conteudo']], item['id_desktop'])[0])
    except Exception as e:
        print(f'* Erro ao executar função "enviar" {e}')
    finally:
        # return {'lista_controle': [], 'lista_dado': []}
        return {'lista_controle': lista_controle, 'lista_dado': lista_dado}


def getdisciplina(disciplina):
    mapa = {
        '919': [420497, None],
        '1489': [420497, None],
        '256': [420497, None],
        '1':[420557,None],
        '1088':[420549,None],
        '1138':[420477,None],
        '1147':[420571,None],
        '1149':[420502,None],
        '1156':[420501,None],
        '1160':[420556,None],
        '1197':[420567,None],
        '12':[420523,None],
        '1260':[420526,None],
        '1344':[420545,'BASE_NACIONAL_COMUM'],
        '1392':[420519,None],
        '1415':[420513,None],
        '1482':[420530,None],
        '1484':[420529,None],
        '1491':[420485,None],
        '1493':[420482,None],
        '1494':[420486,None],
        '1495':[420487,None],
        '1496':[420507,None],
        '1497':[420508,None],
        '1499':[420509,None],
        '1502':[420495,None],
        '1503':[420494,None],
        '1507':[420543,None],
        '1508':[420544,None],
        '1509':[420528,None],
        '1511':[420531,None],
        '1513':[420570,None],
        '1515':[420496,None],
        '1516':[420506,None],
        '1517':[420559,'BASE_NACIONAL_DIVERSIFICADA'],
        '1518':[420586,'BASE_NACIONAL_COMUM'],
        '1519':[420587,'BASE_NACIONAL_COMUM'],
        '1520':[420588,'BASE_NACIONAL_COMUM'],
        '1521':[420589,'BASE_NACIONAL_COMUM'],
        '1522':[420590,'BASE_NACIONAL_COMUM'],
        '1523':[420591,'BASE_NACIONAL_DIVERSIFICADA'],
        '1524':[420592,None],
        '1525':[420593,None],
        '1526':[420594,'BASE_NACIONAL_DIVERSIFICADA'],
        '1527':[420595,None],
        '1528':[420596,None],
        '1529':[420597,None],
        '1530':[420598,None],
        '1531':[420599,None],
        '1532':[420600,None],
        '1533':[420601,None],
        '1534':[420602,None],
        '1535':[420603,None],
        '1536':[420604,None],
        '1537':[420605,None],
        '1538':[420606,None],
        '1539':[420607,None],
        '1540':[420608,None],
        '1541':[420609,None],
        '1542':[420610,None],
        '1543':[420611,None],
        '1544':[420614,None],
        '1545':[420615,None],
        '1546':[420616,None],
        '1547':[420617,None],
        '1548':[420612,None],
        '1549':[420613,None],
        '155':[420547,None],
        '1550':[420618,None],
        '1551':[420619,None],
        '1552':[420620,None],
        '1553':[420621,None],
        '1554':[420622,None],
        '1555':[420624,None],
        '1556':[420625,None],
        '1557':[420626,None],
        '1558':[420627,None],
        '1559':[420628,None],
        '1560':[420629,None],
        '1561':[420630,None],
        '1562':[420631,None],
        '1563':[420632,None],
        '1564':[420633,'BASE_NACIONAL_COMUM'],
        '1565':[420634,None],
        '1566':[420635,None],
        '1567':[420636,None],
        '1568':[420637,None],
        '1569':[420638,None],
        '1570':[420639,None],
        '1571':[420640,None],
        '1572':[420641,'BASE_NACIONAL_DIVERSIFICADA'],
        '1573':[420642,None],
        '1574':[420643,None],
        '1575':[420644,None],
        '1576':[420645,None],
        '1577':[420646,None],
        '1578':[420647,None],
        '1579':[420648,None],
        '1580':[420649,None],
        '1581':[420650,None],
        '1582':[420651,None],
        '1583':[420652,None],
        '1584':[420653,None],
        '1585':[420654,None],
        '1586':[420655,None],
        '1587':[420623,None],
        '1588':[420656,None],
        '1589':[420657,None],
        '1590':[420658,None],
        '1591':[420659,None],
        '1592':[420660,None],
        '1593':[420661,None],
        '1594':[420662,None],
        '1595':[420663,None],
        '1596':[420664,None],
        '1597':[420665,None],
        '1598':[420666,None],
        '1599':[420667,None],
        '1600':[420668,None],
        '1601':[420669,None],
        '1602':[420670,None],
        '1603':[420671,None],
        '1604':[420672,None],
        '1605':[420673,None],
        '1606':[420674,None],
        '1607':[420675,None],
        '1608':[420676,None],
        '1609':[420677,None],
        '1610':[420678,None],
        '1611':[420679,None],
        '1612':[420680,None],
        '1613':[420681,None],
        '1614':[420682,None],
        '1615':[420683,None],
        '1616':[420684,None],
        '1617':[420685,None],
        '18':[420510,None],
        '195':[420585,None],
        '199':[420563,None],
        '2':[420515,None],
        '201':[420578,None],
        '202':[420564,'BASE_NACIONAL_COMUM'],
        '203':[420511,None],
        '204':[420491,None],
        '205':[420575,None],
        '207':[420574,None],
        '22':[420524,None],
        '23':[420576,None],
        '234':[420493,None],
        '257':[420558,None],
        '261':[420542,None],
        '277':[420555,None],
        '3':[420520,None],
        '301':[420568,'BASE_NACIONAL_COMUM'],
        '302':[420538,'BASE_NACIONAL_COMUM'],
        '303':[420535,None],
        '304':[420540,'BASE_NACIONAL_COMUM'],
        '305':[420573,None],
        '306':[420518,None],
        '307':[420513,'BASE_NACIONAL_COMUM'],
        '309':[420532,None],
        '312':[420475,None],
        '316':[420584,None],
        '318':[420499,None],
        '319':[420561,'BASE_NACIONAL_DIVERSIFICADA'],
        '320':[420560,'BASE_NACIONAL_DIVERSIFICADA'],
        '322':[420562,None],
        '328':[420583,None],
        '378':[420533,None],
        '4':[420551,None],
        '40':[420539,None],
        '42':[420580,None],
        '43':[420488,None],
        '437':[420581,None],
        '469':[420492,None],
        '477':[420577,None],
        '487':[420503,None],
        '5':[420512,None],
        '533':[420522,None],
        '535':[420546,None],
        '536':[420537,None],
        '55':[420548,None],
        '582':[420554,None],
        '586':[420566,None],
        '597':[420484,None],
        '6':[420536,None],
        '602':[420521,None],
        '605':[420579,None],
        '61':[420483,None],
        '611':[420527,'BASE_NACIONAL_COMUM'],
        '612':[420489,'BASE_NACIONAL_COMUM'],
        '617':[420498,None],
        '62':[420476,None],
        '620':[420504,None],
        '628':[420480,'BASE_NACIONAL_COMUM'],
        '631':[420565,None],
        '7':[420517,None],
        '72':[420572,None],
        '734':[420569,None],
        '75':[420497,None],
        '76':[420505,None],
        '78':[420490,None],
        '792':[420553,None],
        '8':[420478,'BASE_NACIONAL_COMUM'],
        '808':[420582,None],
        '81':[420552,None],
        '810':[420481,None],
        '818':[420516,None],
        '829':[420479,None],
        '853':[420534,None],
        '86':[420525,None],
        '9':[420541,None],
        '912':[420550,None],
        '928':[420500,None]
    }
    return mapa[disciplina]