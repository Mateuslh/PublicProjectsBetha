# from conexao import consultar
# import requests
# import json
#
# resultados = consultar("""select id_gerado from controle_migracao_registro cmr where tipo_registro = 'calendario-matriz-curricular' and  id_gerado >=131196""")
# lista = []
# tamanho = len(resultados)
# contador = 0
# contador2 = 0
# contador3=0
# for i in resultados:
#     # print(i['id_gerado'],i['quantidademaximaalunos'])
#     lista.append({
#         "idGerado": str(i['id_gerado']),
#         "conteudo": {
#             "id": i['id_gerado']
#         }
#     })
#     contador +=1
#     contador2 +=1
#     if (contador % 20) ==0 or contador2 == tamanho:
#         url = "https://educacao.betha.cloud/service-layer/v2/api/calendario-matriz-curricular/"
#         payload = json.dumps(lista)
#         headers = {
#             'Authorization': 'Bearer 5f9b5b63-d635-466a-9b42-79fa89083243',
#             'Content-Type': 'application/json'
#         }
#         response = requests.request("DELETE", url, headers=headers, data=payload)
#
#         print(response.text)
#
#         lista = []
#         contador = 0
#         contador3+=1
#         print("envia",contador3)