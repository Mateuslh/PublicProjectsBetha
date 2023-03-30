# from conexao import consultar, executar
# import requests
# import json
#
#
# consulta = consultar("""select * from public.controle_migracao_registro where tipo_registro = 'alunos' and i_chave_dsk7 is null and id_gerado is not null""")
# contador = 0
# executares= ''
# for i in consulta:
#     # print(i)
#     url = f"https://api.educacao.betha.cloud/educacao/api/pessoas/aluno/{i['id_gerado']}"
#     # print(url)
#     payload = {}
#     headers = {
#         'user-access': 'KvXZC4VEMEE=',
#         'authorization': 'Bearer  2512e9c1-130f-4e24-b7ab-2490817d7630'
#     }
#
#     response = requests.request("GET", url, headers=headers, data=payload)
#     response = response.json()
#     # print(response)
#     executar(f"""update public.controle_migracao_registro set i_chave_dsk7 = '{response['pessoa']['id']}' where id_gerado = {i['id_gerado']} and tipo_registro='alunos';""")
#     contador +=1
#     print(f'\r executado {contador}/{len(consulta)}', end='')
#     # exit()
#
#
#
#
