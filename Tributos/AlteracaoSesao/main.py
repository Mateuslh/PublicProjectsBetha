import requests
from datetime import datetime

idEndereco = []
offset= 0

f = open("DadosAlterados.txt", "a")


Headers = {"authorization":"Bearer x8484x65x4x654x6x4x684x64x6x" ,
           "user-access":"xxxxxxxxxxx"}

while True:
  retornoGet = requests.get("https://tributos.betha.cloud/tributos/v1/api/cadastros/enderecos/secoes?filter=&limit=1000&offset=" + offset.__str__(), headers=Headers)
  if retornoGet.status_code != 200:
    print("ERRO!\nVerificar os tokens,erro: " + retornoGet.json().__str__())
    exit()
  retonoGetJSON = retornoGet.json()
  print("offset: "+offset.__str__())
  print("Status: " + retornoGet.status_code.__str__())
  offset += 1000
  for conteudo in retonoGetJSON ["content"]:
    idEndereco.append(conteudo)
  if retonoGetJSON ["hasNext"] == False:
    break

print("Fim do Get\n\n\nIniciando o delete...")
f.write("\n_______________________________________________"+datetime.now().__str__()+"_______________________________________________\n___________________________________________________log_delete_pm_laguna_________________________________________________\n")
for dadosGet in idEndereco:
  id = dadosGet["id"]
  JSON={"id":id}
  retornoDel = requests.delete("https://tributos.betha.cloud/tributos/v1/api/cadastros/enderecos/secoes/" + id.__str__(), headers=Headers, json=JSON)
  if retornoDel.status_code == 401:
    Headers["authorization"] = input("Token expirado, insira o novo token:")
    retornoDel = requests.delete(
      "https://tributos.betha.cloud/tributos/v1/api/cadastros/enderecos/secoes/" + id.__str__(), headers=Headers,
      json=JSON)
  if retornoDel.status_code == 204:
    f.write(datetime.now().__str__() +"- ID: " + id.__str__() + " status: " + retornoDel.status_code.__str__() + "\n")
  print("\nid:"+id.__str__()+"\nstatus: "+retornoDel.status_code.__str__())

f.close()

