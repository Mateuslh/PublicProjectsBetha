import json

class Headers:
    def __init__(self, autorization="", otherfields={}):
        self.Authorization = autorization
        self.otherfields = otherfields

    def alterarOtherfields(self):
        if self.otherfields == {}:
            print("Sem campos para alterar")
        print("Alterando campos, caso haja necessidade da alteração, insera o novo valor, caso contrario aperte Enter")
        for campo in self.otherfields:
            novoValor = input(campo.__str__() + ":")
            if novoValor != "":
                self.otherfields[campo] = novoValor

    def definirAuthorization(self, bearer):
        self.Authorization = bearer

    def JsonHeadersAtivo(self):
        dictHeader = self.dictHeadersAtivo()
        jsonHeadersAtivo = json.dumps(dictHeader)
        return jsonHeadersAtivo

    def dictHeadersAtivo(self):
        dictHeadersAtivo = {}
        for campo in self.otherfields:
            dictHeadersAtivo[campo] = self.otherfields[campo]
        if self.Authorization != "":
            dictHeadersAtivo["Authorization"] = self.Authorization
        return dictHeadersAtivo