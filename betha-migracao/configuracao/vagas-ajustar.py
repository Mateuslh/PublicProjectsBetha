# from conexao import consultar
# import requests
# import json
#
# resultados = consultar("""
#  select
# 	id_gerado,id_desktop,anoletivo,estabelecimento,etapamatriz,turno,sum(qtdvagas) as qtdvagas,qtdvagasreservadas
# from (
# 	select
# 	(select id_gerado from public.controle_migracao_registro where hash_chave_dsk = md5(concat('1', 'quadro-vagas', anoLetivo, estabelecimento,etapaMatriz,turno))) as id_gerado,
# 		*
# 		from (
# 			select
# 				null as id_desktop,
# 				(select cmr.id_gerado from controle_migracao_registro cmr where cmr.id_desktop = 2020 and cmr.tipo_registro= 'ano-letivo') as anoLetivo,
# 				(select cmr.id_gerado from controle_migracao_registro cmr where cmr.id_desktop =p.idesc::int and cmr.tipo_registro = 'estabelecimento') as estabelecimento,
# 				(select id_gerado from controle_migracao_registro cmr where id_desktop = concat(turma.idcur,turma.idcurser,turma.idcurgrd)::int and cmr.tipo_registro ='etapa-matriz') as etapaMatriz,
# 				(select upper(x.longdesc) from xtrn x where idtrn = (select idtrn from ptur_hor ph where ph.idturhor = turma.idturhor and ph.idesc = p.idesc)) as turno,
# 				count(idmat) as qtdVagas,
# 				0 as qtdVagasReservadas
# 			from pmat p
# 				inner join ptur turma on (turma.idtur = p.idtur and turma.idesc = p.idesc)
# 				inner join pcur cur on (cur.idcur = turma.idcur)
# 				inner join pltv ltv on (turma.idltv = ltv.idltv and turma.idesc = ltv.idesc)
# 			where
# 				ltv.ano = '2020'
# 			group by p.idesc, turma.idcurgrd, turma.idcur, turma.idcurser, turma.idturhor
# 	) as consulta
# ) as consulta
# --where id_gerado is null
# group by id_gerado,id_desktop,anoletivo,estabelecimento,etapamatriz,turno,qtdvagasreservadas
# """)
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
#             "qtdVagas": int(i['qtdvagas'])
#         }
#     })
#     # print(lista)
#     contador +=1
#     contador2 +=1
#     if (contador % 20) ==0 or contador2 == tamanho:
#         url = "https://educacao.betha.cloud/service-layer/v2/api/quadro-vagas"
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