# from conexao import consultar
# import requests
# import json
#
# resultados = consultar("""
# select distinct on (etapaMatriz,etapaMatriznome,disciplina,disciplinanome,orientacaoCurricular)
# 	etapaMatriz,etapaMatriznome,disciplina,disciplinanome,orientacaoCurricular
# 	from(
# 	select
# 		*,
# 		(select pa.observacoes from pdia_avd pa where pa.idmat = consulta.idmat and pa.idesc = consulta.idesc and pa.iddis = consulta.iddis and pa.idprd = consulta.periodo) as parecer,
# 		(select cmr.id_gerado from controle_migracao_registro cmr where cmr.i_chave_dsk1 = consulta.anoLetivo::varchar and cmr.i_chave_dsk3 = disciplina::varchar and cmr.i_chave_dsk6 = consulta.tur::varchar and cmr.i_chave_dsk4 = 'MEDIA_PERIODO' and cmr.tipo_registro ='item-avaliavel') as itemavaliavel,
# 		(select cmr.i_chave_dsk7 from controle_migracao_registro cmr where cmr.i_chave_dsk1 = consulta.anoLetivo::varchar and cmr.i_chave_dsk3 = disciplina::varchar and cmr.i_chave_dsk6 = consulta.tur::varchar and cmr.i_chave_dsk4 = 'MEDIA_PERIODO' and cmr.tipo_registro ='item-avaliavel') as tipoNota
# 	from (
# 		select
# 			(select id_gerado from public.controle_migracao_registro where hash_chave_dsk = md5(concat('1', 'registro-avaliacao',consulta.id_desktop))) as id_gerado,
# 			row_number() over (partition by idmat,idesc,iddis,coalesce(RPAD(notas,16,'0'),'0000000000000000') order by ordem)::varchar as periodo,
# 			(select id_gerado from controle_migracao_registro cmr where cmr.hash_chave_dsk = md5(concat('1', 'turs',consulta.idtur,estabelecimento)) and cmr.tipo_registro = 'turs') as tur,
# 			(select id_gerado from controle_migracao_registro cmr where cmr.id_desktop = matricula and cmr.tipo_registro='enturcao') as enturcao,
# 			*
# 			from (
# 				select
# 					concat(p.i_sequencial,generate_series(1, length(coalesce(RPAD(p.notas,16,'0'),'0000000000000000')),4)) as id_desktop,
# 					(select cmr.id_gerado from controle_migracao_registro cmr where cmr.id_desktop = ltv.ano::int and cmr.tipo_registro= 'ano-letivo') as anoLetivo,
# 					(select cmr.id_gerado from controle_migracao_registro cmr where cmr.id_desktop = mat.idesc::int and cmr.tipo_registro = 'estabelecimento') as estabelecimento,
# 					(select id_gerado from controle_migracao_registro cmr where id_desktop = concat(tur.idcur,tur.idcurser,tur.idcurgrd)::int and cmr.tipo_registro ='etapa-matriz') as etapaMatriz,
# 					(select i_chave_dsk1 from controle_migracao_registro cmr where id_desktop = concat(tur.idcur,tur.idcurser,tur.idcurgrd)::int and cmr.tipo_registro ='etapa-matriz') as etapaMatriznome,
# 					(select cmr.id_gerado from controle_migracao_registro cmr where id_desktop = p.iddis::int and tipo_registro ='disciplinas') as disciplina,
# 					(select cmr.i_chave_dsk1 from controle_migracao_registro cmr where id_desktop = p.iddis::int and tipo_registro ='disciplinas') as disciplinanome,
# 					(select cmr.id_gerado from controle_migracao_registro cmr where cmr.i_chave_dsk1 = p.idmat and cmr.i_chave_dsk2 = p.idesc and cmr.tipo_registro = 'matricula-movimentacao') as matricula,
# 					(select cmr.i_chave_dsk2 from controle_migracao_registro cmr where cmr.id_desktop = 1 and cmr.tipo_registro = 'configuracao-avaliacao')::int as notaConceito,
# 					'BASE_NACIONAL_DIVERSIFICADA' as orientacaoCurricular,
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
# 					inner join pcur_grd_dis pgd on (pgd.idcurgrd = tur.idcurgrd)
# 				where
# 					ltv.ano in ('2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005','2004','2003','2002','2001','2000','1999','1998')
# 		) as consulta
# 	) as consulta
# where id_gerado is null
# ) as consulta
# where notanumerica is not null or parecer is not null
# """)
# lista = []
# tamanho = len(resultados)
# contador = 0
# contador2 = 0
# contador3=0
# for i in resultados:
#     lista.append({
#         'idIntegracao': str(i['etapamatriz']+i['disciplina']),
#         'conteudo': {
#             'cargaHorariaHoras': 1,
#             'cargaHorariaMinutos': 0,
#             'orientacaoCurricular': 'BASE_NACIONAL_DIVERSIFICADA',
#             'quantidadeModulos': 0,
#             'etapa': {
#                 'id': i['etapamatriz']
#             },
#             'disciplina': {
#                 'id': i['disciplina']
#             }
#         }
#     })
#     contador +=1
#     contador2 +=1
#     if (contador % 100) ==0 or contador2 == tamanho:
#         url = "https://educacao.betha.cloud/service-layer/v2/api/etapa-matriz-disciplina"
#         payload = json.dumps(lista)
#         headers = {
#             'Authorization': 'Bearer 5f9b5b63-d635-466a-9b42-79fa89083243',
#             'Content-Type': 'application/json'
#         }
#         response = requests.request("POST", url, headers=headers, data=payload)
#
#         print(response.text)
#
#         lista = []
#         contador = 0
#         contador3+=1
#         print("envia",contador3)