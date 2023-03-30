# from conexao import consultar, executar
# import requests
# import json
#
# resultados = consultar("""
# select
# 	turma
# 	from(
# select
# 	*
# 	from(
# 	select
# 		*,
# 		(select left(pa.observacoes,15977) from pdia_avd pa where pa.idmat = consulta.idmat and pa.idesc = consulta.idesc and pa.iddis = consulta.iddis and pa.idprd = consulta.periodo) as parecer,
# 		(select cmr.id_gerado::varchar from controle_migracao_registro cmr where cmr.i_chave_dsk1 = consulta.anoLetivo::varchar and cmr.i_chave_dsk3 = disciplina::varchar and cmr.i_chave_dsk6 = consulta.turma::varchar and regexp_replace(cmr.i_chave_dsk5 ,'\D','','g') = consulta.periodo and cmr.i_chave_dsk4 = 'MEDIA_PERIODO' and cmr.tipo_registro ='item-avaliavel') as itemavaliavel,
# 		(select cmr.i_chave_dsk7 from controle_migracao_registro cmr where cmr.i_chave_dsk1 = consulta.anoLetivo::varchar and cmr.i_chave_dsk3 = disciplina::varchar and cmr.i_chave_dsk6 = consulta.turma::varchar and regexp_replace(cmr.i_chave_dsk5 ,'\D','','g') = consulta.periodo and cmr.i_chave_dsk4 = 'MEDIA_PERIODO' and cmr.tipo_registro ='item-avaliavel') as tipoNota
# 	from (
# 		select
# 			(select id_gerado from public.controle_migracao_registro where hash_chave_dsk = md5(concat('1', 'registro-avaliacao',consulta.id_desktop))) as id_gerado,
# 			row_number() over (partition by idmat,idesc,iddis,coalesce(RPAD(notas,16,'0'),'0000000000000000') order by ordem)::varchar as periodo,
# 			(select id_gerado from controle_migracao_registro cmr where cmr.hash_chave_dsk = md5(concat('1', 'turmas',consulta.idtur,estabelecimento)) and cmr.tipo_registro = 'turmas') as turma,
# 			(select id_gerado from controle_migracao_registro cmr where cmr.id_desktop = matricula and cmr.tipo_registro='enturmacao') as enturmacao,
# 			*
# 			from (
# 				select
# 					concat(p.i_sequencial,generate_series(1, length(coalesce(RPAD(p.notas,16,'0'),'0000000000000000')),4)) as id_desktop,
# 					(select cmr.id_gerado from controle_migracao_registro cmr where cmr.id_desktop = ltv.ano::int and cmr.tipo_registro= 'ano-letivo') as anoLetivo,
# 					(select cmr.id_gerado from controle_migracao_registro cmr where cmr.id_desktop = mat.idesc::int and cmr.tipo_registro = 'estabelecimento') as estabelecimento,
# 					(select cmr.id_gerado from controle_migracao_registro cmr where id_desktop = p.iddis::int and tipo_registro ='disciplinas') as disciplina,
# 					(select cmr.id_gerado from controle_migracao_registro cmr where cmr.i_chave_dsk1 = p.idmat and cmr.i_chave_dsk2 = p.idesc and cmr.tipo_registro = 'matricula-movimentacao') as matricula,
# 					(select cmr.i_chave_dsk2 from controle_migracao_registro cmr where cmr.id_desktop = 1 and cmr.tipo_registro = 'configuracao-avaliacao')::int as notaConceito,
# 					p.idmat,
# 					p.idesc,
# 					p.iddis,
# 					coalesce(RPAD(p.notas,16,'0'),'0000000000000000') as notas,
# 					mat.idaln,
# 					tur.idtur,
# 					generate_series(1, length(coalesce(RPAD(p.notas,16,'0'),'0000000000000000')),4) as ordem,
# 	 				nullif((substring(coalesce(RPAD(p.notas,16,'0'),'0000000000000000') from generate_series(1, length(coalesce(RPAD(p.notas,16,'0'),'0000000000000000')), 4) for 4)::double precision/100),0) as notaNumerica
# 				from pdia p
# 					inner join pmat mat on (mat.idmat = p.idmat and mat.idesc = p.idesc)
# 					inner join ptur tur on (tur.idtur = mat.idtur and tur.idesc = p.idesc)
# 					inner join pltv ltv on (tur.idltv = ltv.idltv and p.idesc = ltv.idesc)
# 				where
# 					ltv.ano in ('2020')
# --					and tur.idtur not in ((select sub.idtur from ptur_sub as sub inner join ptur tur on (tur.idesc = sub.idesc and tur.idtur = sub.idtur) inner join pltv p on (p.idesc = tur.idesc and p.idltv = tur.idltv) where	p.ano  in ('2020') group by sub.idtur,sub.idesc))
# --					and tur.idesc not in ((select sub.idesc from ptur_sub as sub inner join ptur tur on (tur.idesc = sub.idesc and tur.idtur = sub.idtur) inner join pltv p on (p.idesc = tur.idesc and p.idltv = tur.idltv) where	p.ano  in ('2020') group by sub.idtur,sub.idesc))
# 		) as consulta
# 	) as consulta
# where
# enturmacao is not null
# ) as consulta
# where notanumerica is not null or parecer is not null) as consulta group by turma
# """)
#
#
# lista = []
# tamanho = len(resultados)
# contador = 0
# contador2 = 0
# contador3 = 0
# lotes = []
# total = 0
# for i in resultados:
#     url = f"https://api.educacao.betha.cloud/educacao/api/commons/turma/{i['turma']}/avaliacoes/completos?limit=999"
#
#     payload = {}
#     headers = {
#         'Authorization': 'Bearer 507cb27d-3648-4f40-82b8-1f1c2e9a0912',
#         'app-context': 'eyJhbm9sZXRpdm8iOnsidmFsdWUiOiI4MzM4IiwiaW5zdWxhdGlvbiI6ZmFsc2V9fQ==',
#         'user-access': 'KvXZC4VEMEE='
#     }
#
#     response = requests.request("GET", url, headers=headers, data=payload)
#     response = response.json()
#     total += response['total']
#     print(response['total'])
# print('total',total)
# # 35617, 34416, 1201
#
# # resultados = consultar("""
# # select
# # 	*
# # 	from(
# # 	select
# # 		*,
# # 		(select left(pa.observacoes,15977) from pdia_avd pa where pa.idmat = consulta.idmat and pa.idesc = consulta.idesc and pa.iddis = consulta.iddis and pa.idprd = consulta.periodo) as parecer,
# # 		(select cmr.id_gerado::varchar from controle_migracao_registro cmr where cmr.i_chave_dsk1 = consulta.anoLetivo::varchar and cmr.i_chave_dsk3 = disciplina::varchar and cmr.i_chave_dsk6 = consulta.turma::varchar and regexp_replace(cmr.i_chave_dsk5 ,'\D','','g') = consulta.periodo and cmr.i_chave_dsk4 = 'MEDIA_PERIODO' and cmr.tipo_registro ='item-avaliavel') as itemavaliavel,
# # 		(select cmr.i_chave_dsk7 from controle_migracao_registro cmr where cmr.i_chave_dsk1 = consulta.anoLetivo::varchar and cmr.i_chave_dsk3 = disciplina::varchar and cmr.i_chave_dsk6 = consulta.turma::varchar and regexp_replace(cmr.i_chave_dsk5 ,'\D','','g') = consulta.periodo and cmr.i_chave_dsk4 = 'MEDIA_PERIODO' and cmr.tipo_registro ='item-avaliavel') as tipoNota
# # 	from (
# # 		select
# # 			(select id_gerado from public.controle_migracao_registro where hash_chave_dsk = md5(concat('1', 'registro-avaliacao',consulta.id_desktop))) as id_gerado,
# # 			row_number() over (partition by idmat,idesc,iddis,coalesce(RPAD(notas,16,'0'),'0000000000000000') order by ordem)::varchar as periodo,
# # 			(select id_gerado from controle_migracao_registro cmr where cmr.hash_chave_dsk = md5(concat('1', 'turmas',consulta.idtur,estabelecimento)) and cmr.tipo_registro = 'turmas') as turma,
# # 			(select id_gerado from controle_migracao_registro cmr where cmr.id_desktop = matricula and cmr.tipo_registro='enturmacao') as enturmacao,
# # 			*
# # 			from (
# # 				select
# # 					concat(p.i_sequencial,generate_series(1, length(coalesce(RPAD(p.notas,16,'0'),'0000000000000000')),4)) as id_desktop,
# # 					(select cmr.id_gerado from controle_migracao_registro cmr where cmr.id_desktop = ltv.ano::int and cmr.tipo_registro= 'ano-letivo') as anoLetivo,
# # 					(select cmr.id_gerado from controle_migracao_registro cmr where cmr.id_desktop = mat.idesc::int and cmr.tipo_registro = 'estabelecimento') as estabelecimento,
# # 					(select cmr.id_gerado from controle_migracao_registro cmr where id_desktop = p.iddis::int and tipo_registro ='disciplinas') as disciplina,
# # 					(select cmr.id_gerado from controle_migracao_registro cmr where cmr.i_chave_dsk1 = p.idmat and cmr.i_chave_dsk2 = p.idesc and cmr.tipo_registro = 'matricula-movimentacao') as matricula,
# # 					(select cmr.i_chave_dsk2 from controle_migracao_registro cmr where cmr.id_desktop = 1 and cmr.tipo_registro = 'configuracao-avaliacao')::int as notaConceito,
# # 					p.idmat,
# # 					p.idesc,
# # 					p.iddis,
# # 					coalesce(RPAD(p.notas,16,'0'),'0000000000000000') as notas,
# # 					mat.idaln,
# # 					tur.idtur,
# # 					generate_series(1, length(coalesce(RPAD(p.notas,16,'0'),'0000000000000000')),4) as ordem,
# # 	 				nullif((substring(coalesce(RPAD(p.notas,16,'0'),'0000000000000000') from generate_series(1, length(coalesce(RPAD(p.notas,16,'0'),'0000000000000000')), 4) for 4)::double precision/100),0) as notaNumerica
# # 				from pdia p
# # 					inner join pmat mat on (mat.idmat = p.idmat and mat.idesc = p.idesc)
# # 					inner join ptur tur on (tur.idtur = mat.idtur and tur.idesc = p.idesc)
# # 					inner join pltv ltv on (tur.idltv = ltv.idltv and p.idesc = ltv.idesc)
# # 				where
# # 					ltv.ano in ('2020')
# # 					and tur.idtur not in ((select sub.idtur from ptur_sub as sub inner join ptur tur on (tur.idesc = sub.idesc and tur.idtur = sub.idtur) inner join pltv p on (p.idesc = tur.idesc and p.idltv = tur.idltv) where	p.ano  in ('2020') group by sub.idtur,sub.idesc))
# # 					and tur.idesc not in ((select sub.idesc from ptur_sub as sub inner join ptur tur on (tur.idesc = sub.idesc and tur.idtur = sub.idtur) inner join pltv p on (p.idesc = tur.idesc and p.idltv = tur.idltv) where	p.ano  in ('2020') group by sub.idtur,sub.idesc))
# # 		) as consulta
# # 	) as consulta
# # where
# # id_gerado is not null and
# # enturmacao is not null
# # ) as consulta
# # where notanumerica is not null or parecer is not null""")
# #
# # lista = []
# # tamanho = len(resultados)
# # contador = 0
# # contador2 = 0
# # contador3 = 0
# # lotes = []
# # total = 0
# # for i in resultados:
# #
# #
# #     lista.append({
# #         "idGerado": f"{i['id_gerado']}",
# #         "conteudo": {
# #           "id": i['id_gerado']
# #         }
# #       })
# #
# #     contador += 1
# #     contador2 +=1
# #     if (contador % 100) ==0 or contador2 == tamanho:
# #         url = "https://educacao.betha.cloud/service-layer/v2/api/registro-avaliacao/"
# #         payload = json.dumps(lista)
# #         headers = {
# #             'Authorization': 'Bearer 5f9b5b63-d635-466a-9b42-79fa89083243',
# #             'Content-Type': 'application/json'
# #         }
# #         response = requests.request("DELETE", url, headers=headers, data=payload)
# #         response = response.json()
# #         lotes.append(response['id'])
# #         lista = []
# #         contador = 0
# #         contador3+=1
# #         print("enviado",contador3)
# #
# # apagar =[]
# # for j in lotes:
# #     import requests
# #
# #     url = f"https://educacao.betha.cloud/service-layer/v2/api/lotes/{j}"
# #     print(url)
# #     payload = {}
# #     headers = {
# #         'Authorization': 'Bearer 6f8535ff-dc7e-4455-84e2-b05ed6141c26'
# #     }
# #
# #     response = requests.request("GET", url, headers=headers, data=payload)
# #
# #     response = response.json()
# #
# #     for k in response['retorno']:
# #         if k['situacao'] =='EXECUTADO':
# #             apagar.append(k['idGerado'])
# # # print(f"""delete from controle_migracao_registro where id_gerado in ({','.join(apagar)})""")
# # print(apagar)
# # executar(f"""delete from controle_migracao_registro where id_gerado in ({','.join(apagar)}) and tipo_registro = 'registro-avaliacao'""")
