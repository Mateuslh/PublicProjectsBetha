# from conexao import consultar
# import requests
# import json
#
# resultados = consultar("""select
# 	*
# from (
# 	select
# 		(select id_gerado from public.controle_migracao_registro where hash_chave_dsk = md5(concat('1', 'turmas',consulta.id_desktop,estabelecimento))) as id_gerado,
# 		*
# 		from (
# 			select
# 				p.idtur as id_desktop,
# 				(select cmr.id_gerado from controle_migracao_registro cmr where cmr.id_desktop = 2021 and cmr.tipo_registro= 'ano-letivo') as anoLetivo,
# 				(select cmr.id_gerado from controle_migracao_registro cmr where cmr.id_desktop =p.idesc::int and cmr.tipo_registro = 'estabelecimento') as estabelecimento,
# 				coalesce((select count(idaln) from pmat p2 where p2.idesc = p.idesc and p2.idtur = p.idtur group by p2.idesc, p2.idtur),1) as quantidadeMaximaAlunos
# 			from ptur p
# 				inner join pcur_grd curgrd on (p.idcurgrd = curgrd.idcurgrd)
# 				inner join pltv ltv on (p.idltv = ltv.idltv and p.idesc = ltv.idesc)
# 				left join public.pcur_ser ps on (ps.idcurser = p.idcurser and ps.idcur = curgrd.idcur)
# 			where
# 				ltv.ano = '2021'
# 	) as consulta
# ) as consulta""")
# lista = []
# tamanho = len(resultados)
# contador = 0
# contador2 = 0
# contador3=0
# for i in resultados:
#     # print(i['id_gerado'],i['quantidademaximaalunos'])
#     lista.append({
#         "idIntegracao": str(i['id_gerado']),
#         "conteudo": {
#             "id": i['id_gerado'],
#             "quantidadeMaximaAlunos": i['quantidademaximaalunos']
#         }
#     })
#     contador +=1
#     contador2 +=1
#     if (contador % 20) ==0 or contador2 == tamanho:
#         url = "https://educacao.betha.cloud/service-layer/v2/api/turma"
#         payload = json.dumps(lista)
#         headers = {
#             'Authorization': 'Bearer 5f9b5b63-d635-466a-9b42-79fa89083243',
#             'Content-Type': 'application/json'
#         }
#         response = requests.request("PUT", url, headers=headers, data=payload)
#
#         print(response.text)
#
#         lista = []
#         contador = 0
#         contador3+=1
#         print("envia",contador3)