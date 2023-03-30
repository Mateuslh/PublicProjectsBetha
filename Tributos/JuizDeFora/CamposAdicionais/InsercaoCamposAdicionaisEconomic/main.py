import requests


urlCamposAdicionais = "https://tributos.betha.cloud/tributos/v1/api/cadastros/cadastros-auxiliares/campos-adicionais?filter=(+cadastro+%3D+%27ECONOMICOS%27+and+tipo+not+in(%27ITEM_SELECAO%27))&limit=1&offset=0&sort="
urlGetCampo = "https://tributos.betha.cloud/tributos/v1/api/cadastros/cadastros-auxiliares/campos-adicionais/"
headers = {
        'user-access': "bhEXHhRrmulpElC9LB63iw==",
        'authorization': "Bearer 7889ef1f-ca62-427d-8cbf-f10bb0001731"
    }

def criaHeaders():
    global headers
    user = input("insira o user access:")
    authorization = input("insira o Bearer, sem a palavra 'Bearer' no começo:")
    headers = {
        'user-access': user,
        'authorization': 'Bearer ' + authorization
    }


def requisicaoTela(Pmetodo, Purl, Pheaders, Pdata={}, Pfiles=[], Pjson={}):
    requisicao = requests.request(Pmetodo,
                                  Purl,
                                  headers=Pheaders,
                                  data=Pdata,
                                  files=Pfiles,
                                  json=Pjson
                                  )

    if not verificaRetorno(requisicao):
        global headers
        requisicaoTela(Pmetodo,Purl,Pheaders=headers,Pdata=Pdata,Pfiles=Pfiles,Pjson=Pjson)
    return requisicao


def verificaRetorno(retorno):
    # verifica se a requisição foi bem sucedida
    if retorno.status_code != 200:
        print("A requisição foi mal sucedida, verificando motivo:")
        if retorno.status_code == 401:
            print("Possivel erro de autenticação\n ERRO:" + retorno.json()[
                "message"] + "\n\niniciando processo do novo token")
            criaHeaders()
            return False
        if retorno.status_code == 415:
            print("erro no corpo da requisição, verifica-la\n ERRO:" + retorno.json().__str__())
            exit()
        else:
            print(retorno.status_code)
            print(retorno.json())
            continuar = input(
                "Não foi possivel indentificar o erro, Digite 's' caso queira continuar as demais requisições e 'n',"
                " caso não queira.")
            if (continuar == "n"):
                exit()
            if continuar == "s":
                return True
    else:
        return retorno

def percorrerJSON(obj):
    for propriedade in obj:
        #Caso a propriedade seja um objeto, chame a função recursivamente
        if isinstance(obj[propriedade], dict):
            percorrerJSON(obj[propriedade])
        if isinstance(obj[propriedade],list):
            for posicaoLista in obj[propriedade]:
                percorrerJSON(posicaoLista)
        else:
            print(propriedade + ": " + str(obj[propriedade]))

requisicao = requisicaoTela(Pmetodo="GET",Purl=urlCamposAdicionais,Pheaders=headers)

for conteudo in requisicao.json()["content"]:
    jsonCampoEconomico = requisicaoTela(Pmetodo="GET",Purl=urlGetCampo+conteudo["id"].__str__(),Pheaders=headers).json()
    deletes = []
    print(jsonCampoEconomico)
    for item in jsonCampoEconomico:
        if jsonCampoEconomico[item] is None or jsonCampoEconomico[item]==[]:
            deletes.append(item)
    for propriedades in deletes:
        del jsonCampoEconomico[propriedades]
    percorrerJSON(jsonCampoEconomico)