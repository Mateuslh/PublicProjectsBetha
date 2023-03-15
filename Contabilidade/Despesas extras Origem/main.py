#---------------------------Orientações---------------------------#
# O dados podem ser pegos por meio do F12,
# offset deve ser alterado exlusivamente quando
# o Bearer token expirar durante a execução do script,
# o valor dele será informado se isso ocorrer.


#---------------------------Parametros----------------------------#

appcontext= "xxxxxxxxxxxxxxxxxxxxxxxx"
authorization= "Bearer xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
useraccess= "xxxxxxxxxx-xxxxxxxxxxx=="
offset=0

#------------------------------------------------------------------#

from requests import get, put
from datetime import datetime

def analisar(dh_inicio=None):
    if dh_inicio is None:
        return datetime.now()
    else:
        print(f' Processo finalizado. ({round((datetime.now() - dh_inicio).total_seconds(), 2)} segundos)')

Headers = {"app-context": appcontext,
           "authorization": authorization,
           "user-access":useraccess}

teste = get("https://contabilidade.cloud.betha.com.br/contabilidade/api/contabil/despesas-extras?filter=&limit=1&offset=0", headers=Headers)
if teste.status_code != 200:
    print("ERRO!\nVerificar os tokens,erro: "+teste.json().__str__())
    exit()

aux = []
depesasExtras = []
verifc = []


print("Buscando as despesas extras...")
tempo = analisar()
while True:
    dadosGet = get("https://contabilidade.cloud.betha.com.br/contabilidade/api/contabil/despesas-extras?filter=&limit=100&offset=" + offset.__str__(), headers=Headers).json()
    offset += 100
    for i in dadosGet['content']:
        depesasExtras.append(i)
    if dadosGet["hasNext"] == False:
        break
analisar(tempo)
print("Consultando o JSON completo das "+len(depesasExtras).__str__()+" despesas e verificando se possuem 'origens'...")
tempo = analisar()

for i in range(0,len(depesasExtras)):
    idDespesaExtra = depesasExtras[i]['id']
    verifc = get("https://contabilidade.cloud.betha.com.br/contabilidade/api/contabil/despesas-extras/" + idDespesaExtra.__str__(), headers=Headers)
    if verifc.status_code == 401:
        print("||ERRO||\n"+depesasExtras[i].__str__()+"\n\n\n")
        Headers["authorization"] = input("insira o token: Ex:Bearer xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx\n\n\n\n")
        verifc = get("https://contabilidade.cloud.betha.com.br/contabilidade/api/contabil/despesas-extras/" + idDespesaExtra.__str__(),
            headers=Headers)
    depesasExtras[i] = verifc.json()
    if depesasExtras[i]['classificacoes'][0]['origens']==[]:
        lista_origens = get("https://contabilidade.cloud.betha.com.br/contabilidade/api/contabil/despesas-extras/"+idDespesaExtra.__str__()+"/classificacoes/" + (depesasExtras[i]['classificacoes'][0]['classificacao']['id']).__str__() + "/sugestoes", headers=Headers).json()
        for origens in lista_origens['origens']:
            if depesasExtras[i]['valor'] == origens["valor"] and depesasExtras[i]['classificacoes'][0]['recursos'][0]['recurso']['numero'] == origens["recursoVinculo"]['recurso']['numero'] and depesasExtras[i]['data'] == origens["recursoVinculo"]["documentoOrigem"]["data"]:
                depesasExtras[i]["classificacoes"][0]["origens"] = (origens)
                aux.append(depesasExtras[i]['numero'])
                retorno = put(
                    "https://contabilidade.cloud.betha.com.br/contabilidade/api/contabil/despesas-extras/"+ idDespesaExtra.__str__(),
                    json=depesasExtras[i], headers=Headers)
analisar(tempo)
print(len(aux).__str__()+" despesas alteradas, as despesas extras alteradas foram:"+aux.__str__())