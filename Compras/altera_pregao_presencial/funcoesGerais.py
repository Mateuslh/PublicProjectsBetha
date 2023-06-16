from datetime import datetime
import requests
import json
def alimentaBackup(ids,arquivoBackup,headers):
    listaJSON = []
    for listIdAno in ids:
        processoAdminstrativoId,processoAdminstrativoAno = listIdAno.split(",")[0],listIdAno.split(",")[1]
        url = "https://compras.betha.cloud/compras-services/api/exercicios/" + processoAdminstrativoAno + '/processos-administrativo/' + processoAdminstrativoId + '/forma-contratacao'
        listaJSON.append(requests.get(url=url,headers=headers).json())
    arquivoBackup.write(str(json.dumps(listaJSON)))
def altera_pregao_presencial(ids,arquivoLog,headers):
    arquivoLog.write("\n" + "_" * 45 + datetime.now().__str__() + "_" * 45 + "\n" + "_" * 45 + "log_altera_pregao_presencial" + "_" * 45 + "\n\n\n")
    for listIdAno in ids:
        processoAdminstrativoId,processoAdminstrativoAno = listIdAno.split(",")[0],listIdAno.split(",")[1]
        url = "https://compras.betha.cloud/compras-services/api/exercicios/" + processoAdminstrativoAno + '/processos-administrativo/' + processoAdminstrativoId + '/forma-contratacao'
        jsonRetornoGet = requests.get(url=url, headers=headers).json()
        arquivoLog.write("\nid: "+str(processoAdminstrativoId)+"\n"+str(jsonRetornoGet))
        jsonRetornoGet["fundamentacaoLegal"]["id"] = 281
        jsonRetornoPost = requests.post(url=url, headers=headers,json=jsonRetornoGet).json()
        arquivoLog.write(str(jsonRetornoPost))