# from conexao import consultar
# import requests
# import json
# from time import sleep
#
# resultados = consultar("""--drop index if exists idx_i_chave_dsk1,idx_i_chave_dsk2,idx_i_chave_dsk3,idx_i_chave_dsk4,idx_i_chave_dsk5,idx_i_chave_dsk6,idx_i_chave_dsk7,idx_id_desktop,idx_id_gerado,idx_tipo_registro,idx_mat_idaln,idx_pdia_avd_iddis,idx_pdia_avd_idesc,idx_pdia_avd_idmat,idx_pdia_avd_idprd,idx_pdia_i_sequencial,idx_pdia_iddis,idx_pdia_idesc,idx_pdia_idmat,idx_pdia_notas,idx_tur_idtur;
# --
# --CREATE INDEX idx_i_chave_dsk1 ON public.controle_migracao_registro USING btree (i_chave_dsk1);
# --CREATE INDEX idx_i_chave_dsk2 ON public.controle_migracao_registro USING btree (i_chave_dsk2);
# --CREATE INDEX idx_i_chave_dsk3 ON public.controle_migracao_registro USING btree (i_chave_dsk3);
# --CREATE INDEX idx_i_chave_dsk4 ON public.controle_migracao_registro USING btree (i_chave_dsk4);
# --CREATE INDEX idx_i_chave_dsk5 ON public.controle_migracao_registro USING btree (i_chave_dsk5);
# --CREATE INDEX idx_i_chave_dsk6 ON public.controle_migracao_registro USING btree (i_chave_dsk6);
# --CREATE INDEX idx_i_chave_dsk7 ON public.controle_migracao_registro USING btree (i_chave_dsk7);
# --CREATE INDEX idx_id_desktop ON public.controle_migracao_registro USING btree (id_desktop);
# --CREATE INDEX idx_id_gerado ON public.controle_migracao_registro USING btree (id_gerado);
# --CREATE INDEX idx_tipo_registro ON public.controle_migracao_registro USING btree (tipo_registro);
# --CREATE INDEX idx_mat_idaln ON public.pmat USING btree (idaln);
# --CREATE INDEX idx_pdia_avd_iddis ON public.pdia_avd USING btree (iddis);
# --CREATE INDEX idx_pdia_avd_idesc ON public.pdia_avd USING btree (idesc);
# --CREATE INDEX idx_pdia_avd_idmat ON public.pdia_avd USING btree (idmat);
# --CREATE INDEX idx_pdia_avd_idprd ON public.pdia_avd USING btree (idprd);
# --CREATE INDEX idx_pdia_i_sequencial ON public.pdia USING btree (i_sequencial);
# --CREATE INDEX idx_pdia_iddis ON public.pdia USING btree (iddis);
# --CREATE INDEX idx_pdia_idesc ON public.pdia USING btree (idesc);
# --CREATE INDEX idx_pdia_idmat ON public.pdia USING btree (idmat);
# --CREATE INDEX idx_pdia_notas ON public.pdia USING btree (notas);
# --CREATE INDEX idx_tur_idtur ON public.ptur USING btree (idtur);
# select turma from(
# select
# 	*
# 	from(
# 	select
# 		*,
# 		(select pa.observacoes from pdia_avd pa where pa.idmat = consulta.idmat and pa.idesc = consulta.idesc and pa.iddis = consulta.iddis and pa.idprd = consulta.periodo) as parecer,
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
# 					ltv.ano in ('2019')--,'2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005','2004','2003','2002','2001','2000','1999','1998')
# --					limit 2
# 		) as consulta
# 	) as consulta
# where id_gerado is null
# ) as consulta
# where notanumerica is not null or parecer is not null
# )as a group by turma""")
# lista = []
# tamanho = len(resultados)
# contador = 0
# contador2 = 0
# contador3=0
# for i in resultados:
#     # print(i['id_gerado'],i['quantidademaximaalunos'])
#     import requests
#
#     url = f"https://api.educacao.betha.cloud/educacao/api/matricula/turma/{i['turma']}"
#
#     payload = {}
#     headers = {
#         'Authorization': 'Bearer 024bab57-cf7a-4f7b-a8cc-1b336f688632',
#         'user-access': 'KvXZC4VEMEE=',
#         'app-context': 'eyJhbm9sZXRpdm8iOnsidmFsdWUiOiI4MzQ0IiwiaW5zdWxhdGlvbiI6ZmFsc2V9fQ=='
#     }
#
#     response = requests.request("GET", url, headers=headers, data=payload)
#
#     response = response.json()
#     url = f"https://api.educacao.betha.cloud/educacao/api/matricula/turma/{i['turma']}"
#
#     payload = json.dumps(response)
#     headers = {
#         'Authorization': 'Bearer 024bab57-cf7a-4f7b-a8cc-1b336f688632',
#         'user-access': 'KvXZC4VEMEE=',
#         'app-context': 'eyJhbm9sZXRpdm8iOnsidmFsdWUiOiI4MzQ0IiwiaW5zdWxhdGlvbiI6ZmFsc2V9fQ==',
#         'Content-Type': 'application/json'
#     }
#
#     response = requests.request("PUT", url, headers=headers, data=payload)
#     contador += 1
#     print(i['turma'],contador,response.status_code)
#     sleep(2)
#
