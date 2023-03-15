import requests
from datetime import datetime
global headers
import time
import copy
headers = {
    "user-access":"xxxxxxxxxxxxxxxxxx",
    "authorization": "Bearer x54x64x89x49x84x98x1468x4x6c4"
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

urlContribuinetes = "https://tributos.betha.cloud/tributos/v1/api/cadastros/referentes/contribuintes/"
urlLogradouro = "https://tributos.betha.cloud/tributos/v1/api/cadastros/enderecos/logradouros/"
urlBairros = "https://tributos.betha.cloud/tributos/v1/api/cadastros/enderecos/bairros/"

ids = open("id.txt","r").read().split(",")
log = open("DadosAlterados.txt", "a")
log.write("\n"+"_"*45+datetime.now().__str__()+"_"*45+"\n"+"_"*45+"log_reestimulo_municipio"+"_"*45+"\n\n\n")


for value in ids:
    log.write("_"*45+value+"_"*45+"\n")
    print(urlContribuinetes + value)
    retorno = requisicaoTela("GET",                                                                                     # Consultando os contribuientes
                             urlContribuinetes + value,
                             Pheaders=headers).json()
    jsonIntegralContribuiente = copy.deepcopy(retorno)
    print("1 get endereço",jsonIntegralContribuiente)
    log.write("JSON integral contribuiente: "+jsonIntegralContribuiente.__str__()+"\n")                                 # Deletenado a versão para nao gerar erros nas requisições de put
    jsonSemEndereco = copy.deepcopy(retorno)                                                                            # Gerando o JSON sem os endereções para o PUT
    jsonSemEndereco["enderecos"] = []
    retorno = requisicaoTela("PUT",                                                                                     # Insere contribuiente sem endereco
                             urlContribuinetes + value,
                             Pheaders=headers,
                             Pjson=jsonSemEndereco)
    print("1 put endereço ", retorno.json())
    for enderecos in jsonIntegralContribuiente["enderecos"]:                                                            # Inico do bloco do reestimulo dos logradouros e bairros para confirmar que o dado existe na base fly
        jsonIntegralLogradouro = requisicaoTela("GET",                                                                  # Inicio logradouros
                                                urlLogradouro + enderecos["logradouro"]["id"].__str__()
                                                , Pheaders=headers).json()
        print("1 get logradouros", jsonIntegralLogradouro)
        log.write("JSON integral Logradouro: " + jsonIntegralLogradouro.__str__() + "\n")
        del jsonIntegralLogradouro["version"]

        jsonNomeLogradouroAlterado = copy.deepcopy(jsonIntegralLogradouro)                                              # Gerando Json com o nome alterado para gerar alteração no cadastro unico
        jsonNomeLogradouroAlterado["nome"] = jsonNomeLogradouroAlterado["nome"]+"."

        retorno = requisicaoTela("PUT",                                                                                 # Requisição com o nome alterado
                                 urlLogradouro+enderecos["logradouro"]["id"].__str__(),
                                 Pheaders=headers,
                                 Pjson=jsonNomeLogradouroAlterado)
        print("1 put logradouro ", retorno)
        retorno = requisicaoTela("PUT",                                                                                 # Requisição com o nome correto
                                 urlLogradouro+enderecos["logradouro"]["id"].__str__(),
                                 Pheaders=headers,
                                 Pjson=jsonIntegralLogradouro)
        print("2 put logradouro", retorno.json())
        jsonIntegralBairro = requisicaoTela("GET",                                                                      # Inicio bairros
                                            urlBairros+enderecos["bairro"]["id"].__str__(),
                                            Pheaders=headers).json()
        print("1 get bairro", jsonIntegralBairro)
        log.write("JSON integral Bairro: " + jsonIntegralBairro.__str__() + "\n")
        del jsonIntegralBairro["version"]                                                                               # Retira a versão

        jsonBairroNomeAlterado = copy.deepcopy(jsonIntegralBairro)                                                      # Gerando Json com o nome alterado para gerar alteração no cadastro unico
        jsonBairroNomeAlterado["nome"] = jsonBairroNomeAlterado["nome"]+"."

        retorno = requisicaoTela("PUT",
                                 urlBairros+enderecos["bairro"]["id"].__str__(),
                                 Pheaders=headers,
                                 Pjson=jsonBairroNomeAlterado)
        print("1 put bairro ", retorno)
        retorno = requisicaoTela("PUT",
                                 urlBairros+enderecos["bairro"]["id"].__str__(),
                                 Pheaders=headers,
                                 Pjson=jsonIntegralBairro)                                                              # Fim correção dos logradouros e bairros
        print("2 put bairro ", retorno)
                                                                                                                        # Inicio do bloco de Contribuientes
    for endereco in jsonIntegralContribuiente["enderecos"]:                                                             # retirando os ids dos endereço para realizar o put alterando dado
        del endereco["id"]
    print(jsonIntegralContribuiente)
    del jsonIntegralContribuiente["version"]
    retorno = requisicaoTela("PUT",
                             urlContribuinetes + value,
                             Pheaders=headers,
                             Pjson=jsonIntegralContribuiente)                                                           # Insere novamente o endereco
    print("2 put endereço ",retorno.json())
    time.sleep(3)

    