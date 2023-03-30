# import requests
# import json
# from conexao import consultar, executar
# from configuracao.conexao import inserir_registro
# from funcao import encurtar
# #
# consuta = consultar("""select
# *
# from(
# 	select
# 		*,
# 		(select id_gerado from controle_migracao_registro cmr where cmr.hash_chave_dsk = md5(concat('1', 'turmas',idtur,estabelecimento)) and cmr.tipo_registro = 'turmas' and i_chave_dsk7 is null)  as turma,
# 		(select cmr.id_gerado from controle_migracao_registro cmr where cmr.id_desktop = split_part(ano,',',1)::int and cmr.tipo_registro= 'ano-letivo') as anoLetivo
# 	from(
# 		select
# 			sub.idtur,
# 			(select cmr.id_gerado from controle_migracao_registro cmr where cmr.id_desktop = sub.idesc::int and cmr.tipo_registro = 'estabelecimento') as estabelecimento,
# 			string_agg(sub.idtursub,','),
# 			string_agg(p.ano,',') as ano
# 		from
# 			ptur_sub as sub
# 			inner join ptur tur on (tur.idesc = sub.idesc and tur.idtur = sub.idtur)
# 			inner join pltv p on (p.idesc = tur.idesc and p.idltv = tur.idltv)
# 		where
# 			p.ano in ('2021') and tur.idtur not in ('73117')
# 		group by
# 			sub.idtur,sub.idesc
# 	) as consulta
# ) as consulta
# where turma is not null
# """)
# # consuta =[8593626, 8746380, 8593612, 8746323]
# total = 0
# cont = 0
# contador = 0
# contador2 = 0
# tamanho = len(consuta)
# lista = []
# listaPaga=[]
# for i in consuta:
#     url = "https://educacao.betha.cloud/educacao/conversao/api/turmas/remover"
#
#     payload = json.dumps([
#         {
#             "turma": {
#                 "id": i['turma'],
#                 "anoLetivo": {
#                     "id": i['anoletivo']
#                 },
#                 "estabelecimento":{
#                     "id": i['estabelecimento']
#                 },
#                 "tipo":"TURMA"
#             }
#         }
#     ])
#     headers = {
#         'Authorization': 'Bearer 5f9b5b63-d635-466a-9b42-79fa89083243',
#         'Content-Type': 'application/json'
#     }
#
#     response = requests.request("PUT", url, headers=headers, data=payload)
#     response = response.json()
#     lista.append(response['idLote'])
# for i in lista:
#   statusLote = 'QUEUE'
#   while statusLote == 'QUEUE':
#
#     url = f"https://educacao.betha.cloud/educacao/conversao/api/lotes/{i}"
#
#     payload = {}
#     headers = {
#       'Authorization': 'Bearer 353ab402-2ec3-4e12-b679-1ea14a136a6d'
#     }
#
#     response = requests.request("GET", url, headers=headers, data=payload)
#     response = response.json()
#     statusLote = response['statusLote']
#   # print(response)
#   for j in response['retorno']:
#     if j['status'] == "SUCESSO":
#         print('feito')
#     else:
#         print('erro',j)
# #
# #     url = f"https://educacao.betha.cloud/service-layer/v2/api/calendario-matriz-curricular/{i['id_gerado']}"
# #
# #     payload = {}
# #     headers = {
# #         'Authorization': 'Bearer 5f9b5b63-d635-466a-9b42-79fa89083243'
# #     }
# #
# #     response = requests.request("GET", url, headers=headers, data=payload)
# #     response = response.json()
# #     executar(f"""update controle_migracao_registro set i_chave_dsk2 ='{response['anoLetivo']['id']}' where id_gerado ={i['id_gerado']} and tipo_registro = 'calendario-matriz-curricular'""")
# #   listaPaga.append(
# #       {
# #           "item": {
# #               "idGerados": {
# #                   "idMatricula": i
# #               }
# #           }
# #       }
# #   )
# #   contador += 1
# #   contador2 += 1
# #   if contador % 10 ==0 or contador2 == tamanho:
# #     contador = 0
# #     payload = json.dumps(listaPaga)
# #     url = "https://educacao.betha.cloud/educacao/conversao/api/matricula-movimentacao/remover/"
# #     headers = {
# #       'Authorization': 'Bearer 5f9b5b63-d635-466a-9b42-79fa89083243',
# #       'Content-Type': 'application/json'
# #     }
# #     contador = 0
# #     listaPaga = []
# #     response = requests.request("PUT", url, headers=headers, data=payload)
# #     # print(response)
# #     response = response.json()
# #     # print(response)
# #     lista.append(response['idLote'])
# # print(lista)
# # # # lista = [32656082, 32656083, 32656084, 32656085, 32656086, 32656087, 32656088, 32656089, 32656090, 32656091, 32656092, 32656093, 32656094, 32656095, 32656096, 32656097, 32656098, 32656099, 32656100, 32656101, 32656102]
# # for i in lista:
# #   statusLote = 'QUEUE'
# #   while statusLote == 'QUEUE':
# #
# #     url = f"https://educacao.betha.cloud/educacao/conversao/api/lotes/{i}"
# #
# #     payload = {}
# #     headers = {
# #       'Authorization': 'Bearer 353ab402-2ec3-4e12-b679-1ea14a136a6d'
# #     }
# #
# #     response = requests.request("GET", url, headers=headers, data=payload)
# #     response = response.json()
# #     statusLote = response['statusLote']
# #   # print(response)
# #   for j in response['retorno']:
# #     if j['status'] == "SUCESSO":
# #         print('feito')
# #
# #       executar(f"""update controle_migracao_registro set i_chave_dsk7 ='1' where id_gerado ={j['idGerados']['idTurma']}""")
# #       total +=1
# #   print(total)
# # print(total-cont)
# # hasNext = True
# # limit = 99
# # offset = 0
# # contador = 0
# # while hasNext:
# #
# #     url = f"https://educacao.betha.cloud/service-layer/v2/api/quadro-vagas?limit={limit}&offset={offset}"
# #
# #     payload={}
# #     headers = {
# #       'Authorization': 'Bearer 5f9b5b63-d635-466a-9b42-79fa89083243'
# #     }
# #
# #     response = requests.request("GET", url, headers=headers, data=payload)
# #     response = response.json()
# #     hasNext = response['hasNext']
# #     contador +=1
# #     offset = limit * contador
# #     for i in response['content']:
# #         inserir_registro([{'sistema': '1',
# #                            'tipo_registro':'quadro-vagas',
# #                            'descricao_tipo_registro':'Cadastro de quadro-vagas',
# #                            'hash_chave_dsk':encurtar('1',
# #                                                      'quadro-vagas',
# #                                                      i['anoLetivo']['id'],
# #                                                      i['estabelecimento']['id'],
# #                                                      i['etapaMatriz']['id'],
# #                                                      i['turno']),
# #                            'id_gerado':i['id'],
# #                            'i_chave_dsk1':i['anoLetivo']['id'],
# #                            'i_chave_dsk2':i['estabelecimento']['id'],
# #                            'i_chave_dsk3':i['etapaMatriz']['id'],
# #                            'i_chave_dsk4':i['turno']}])
# #     print(contador, offset)
