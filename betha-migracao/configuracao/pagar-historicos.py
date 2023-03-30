from conexao import consultar, executar
import requests
import json

consulta = consultar("""select
	*
from (
	select
		(select id_gerado from public.controle_migracao_registro where hash_chave_dsk = md5(concat('1','historico-escolar',aluno,anoConclusao,etapa,situacao)) limit 1) as id_gerado,
		*
	from (
		select
			(select id_gerado from public.controle_migracao_registro where hash_chave_dsk = md5(concat('1', 'matricula-movimentacao',hst.idmat,hst.idesc)) and i_chave_dsk7 is null) as matricula,
            (select id_gerado from controle_migracao_registro cmr where cmr.tipo_registro = 'alunos' and cmr.i_chave_dsk1 = trim(upper(replace(pessoa.nome,'  ',' '))) and cmr.i_chave_dsk3 = (case pessoa.sexo when 'M' then 'MASCULINO' when 'F' then 'FEMININO' end) and cmr.i_chave_dsk2 = (case when pessoa.datanasc::date < '1200-01-01'::date then '2000-01-01' else pessoa.datanasc::varchar end)) as aluno,
			hst.idano::int as anoConclusao,
			(case hst.idsitmat
					when '20' 	then 'APROVADO'
					when '23' 	then 'APROVADO'
					when '30' 	then 'REPROVADO'
					when '33' 	then 'REPROVADO'
					when '41' 	then 'OUTRA'
					else hst.idsitmat
				end) as situacao,
			regexp_replace(hst.descserie,'(Educação Infantil)','Edu. Inf.') as etapa
		FROM
			phst hst
			inner join public.gpes pessoa on (pessoa.idpes = hst.idpes)
			and hst.idmat is not null
			
	) as consulta
) as consulta
where aluno is not null and matricula is not null and id_gerado is not null
limit 10000""")
print(len(consulta))
payload={}
headers = {
  'Authorization': 'Bearer 5f9b5b63-d635-466a-9b42-79fa89083243',
  'content-type': 'application/json'
}
url = "https://educacao.betha.cloud/service-layer/v2/api/historico-escolar/"
lista = []
lotes = []
contador = 0

for index, i in enumerate(consulta):
    lista.append(
        {
            "idGerado": f"{i['id_gerado']}",
            "conteudo": {
                "id": i['id_gerado']
            }
        }
    )
    contador += 1
    if contador % 100 == 0 or contador == len(consulta):
        payload = json.dumps(lista)
        lista = []
        response = requests.request("DELETE", url, headers=headers, data=payload)
        response = response.json()
        lotes.append(response['id'])
    print("\r Historico {}/{}".format(index,len(consulta)), end='')
print("\n")

apagar = []
payload = {}

for posicao, j in enumerate(lotes):
    url = f"https://educacao.betha.cloud/service-layer/v2/api/lotes/{j}"
    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()
    for k in response['retorno']:
        if (k['situacao'] =='EXECUTADO') or (k['situacao'] =='ERRO' and k['mensagem'] == f"Entidade HistoricoEscolar com o ID: {k['idGerado']} não encontrada"):
            apagar.append(k['idGerado'])
    print("\r Lote {}/{}".format(posicao, len(lotes)), end='')

print("\n")
print(f"""delete from controle_migracao_registro where id_gerado in ({','.join(apagar)})""")
print("\n")
print(apagar)
print(len(apagar))

executar(f"""delete from controle_migracao_registro where id_gerado in ({','.join(apagar)}) and tipo_registro = 'historico-escolar'""")
