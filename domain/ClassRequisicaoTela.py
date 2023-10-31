import requests
from domain.ClassHeaders import Headers
from numpy import array

class RequisicaoTela:
    header = Headers()

    def __init__(self, Method=None, Purl=None, Pdata=None, Pheaders=None, Pfiles=None, Pjson=None, Pparam=None):
        """
        :type Pdata: Any
        :type Method: str
        :type Pheaders: class headers
        :type Purl: str
        :type Pfiles: files
        :type Pparam: dict
        :type Pjson: str(json)
        """
        self.method = Method
        self.url = Purl
        self.data = Pdata
        self.files = Pfiles
        self.json = Pjson
        self.params = Pparam
        RequisicaoTela.header = Pheaders if isinstance(Pheaders, Headers) else RequisicaoTela.header

    def rodar(self, Method=False, Purl=False, Pdata=False, Pheaders=False, Pfiles=False, Pjson=False, Pparam=False):
        requisicao = requests.request(method=Method if Method != False else self.method,
                                      url=Purl if Purl != False else self.url,
                                      headers=Pheaders if Pheaders != False else RequisicaoTela.header.dictHeadersAtivo(),
                                      data=Pdata if Pdata != False else self.data,
                                      files=Pfiles if Pfiles != False else self.files,
                                      json=Pjson if Pjson != False else self.json,
                                      params=Pparam if Pparam != False else self.params)
        if not self.verificaRetorno(requisicao):
            requisicao = self.rodar(Method=Method, Purl=Purl, Pdata=Pdata, Pheaders=Pheaders, Pfiles=Pfiles,
                                    Pjson=Pjson, Pparam=Pparam)
        return requisicao

    @staticmethod
    def getHeader():
        return RequisicaoTela.header.dictHeadersAtivo()

    def rodarRegistrosMultiplos(self, Method=False, Purl=False, Pdata=False, Pheaders=False , Pfiles=False, Pjson=False,
                                Pparam={}, Plimit=20, PoffSet=0, retornarJson=False):
        offSet = PoffSet
        params = Pparam
        hasNext = True
        retornosRequisicao = []
        while hasNext:
            newParams = {
                "offset": str(offSet),
                "limit": str(Plimit)
            }
            params.update(newParams)
            retornoRequisicao = self.rodar(Method=Method, Purl=Purl, Pdata=Pdata, Pheaders=Pheaders, Pfiles=Pfiles,
                                           Pjson=Pjson, Pparam=params)
            hasNext = self.existeMais(retornoRequisicao)
            offSet += Plimit
            if retornarJson:
                try:
                    conteudos = retornoRequisicao.json()['content']
                except Exception as erro:
                    conteudos = retornoRequisicao.json()
                retornosRequisicao.append(conteudos)
            else:
                retornosRequisicao.append(retornoRequisicao)
        listaRetornoAchatada = array(retornosRequisicao).flatten()
        return listaRetornoAchatada

    @staticmethod
    def existeMais(retorno):
        return retorno.json()["hasNext"]

    @staticmethod
    def verificaRetorno(retorno):
        # verifica se a requisição foi bem sucedida
        if retorno.status_code != 200:
            print("A requisição foi mal sucedida, verificando motivo:")
            if retorno.status_code == 401:
                print(
                    "Possivel erro de autenticação\n ERRO:" + retorno.json().__str__() + "\n\niniciando obtencao de novo token...")
                novoToken = input("Insira o novo Token:")
                RequisicaoTela.header.definirAuthorization(novoToken)
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
                if continuar == "n":
                    exit()
                if continuar == "s":
                    return True
        else:
            return retorno
