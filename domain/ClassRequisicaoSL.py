import json
import os
from typing import Union

from requests import request
from tool_box.arquivos.arquivo_json import escrever_em_json,ler_de_json
from tool_box.arquivos.pastas import cria_pasta
from tool_box.listas import collate, groupBy
from datetime import datetime

class RequisicaoServiceLayer:
    def __init__(self, Method: str, Purl: str = None, Pdata: Union[dict, str] = None, Pheaders: object = None, Pfiles: object = None, Pjson: object = None, Pparam: object = None,
                 Pverify: object = True) -> object:
        """
        :param Method: String
        :param Purl: String
        :param Pheaders: Dicionario
        :param Pparam: Dicionario
        """
        self.method = Method
        self.url = Purl
        self.params = Pparam
        self.headers = Pheaders
        self.data = Pdata
        self.files = Pfiles
        self.json = Pjson
        self.verify = Pverify
        self.__erros = []
        self.__retorno = []
        self.__lotes = {}

    @property
    def lotes(self):
        return list(self.__lotes.values())

    def cria_lotes(self, list_registros, tamanho_lote):
        """
        :param list_registros: Lista de registros para requisição.
        :param tamanho_lote: Tamanho do lote a ser enviado.
        :return: None
        """
        try:
            lista_segregada = collate(tamanho_sublista=tamanho_lote, lista=list_registros)
            for lista in lista_segregada:
                hashJson = hash(str(lista)+str(datetime.now()))
                self.__lotes[str(hashJson)] = lista
        except Exception as erro:
            print(f'Erro ao criar lotes:{str(erro)}')

    def envia_lotes(self):
        """
        :return: class:`Lote <Lote>` object
        """
        for uuid, lote in self.__lotes.items():
            try:
                resposta = request(method=self.method, url=self.url, json=lote, headers=self.headers)
                retorno = {
                    "hash": uuid,
                    "retorno": resposta.text
                }
                if resposta.status_code == 200:
                    self.__retorno.append(retorno)
                else:
                    self.__erros.append(retorno)
                    print(f"Falha ao enviar lote: {resposta.status_code} - {resposta.text}")
            except Exception as erro:
                print(f"Erro ao enviar lote '{uuid}':{str(erro)}")
        return self

    def cria_log_erro(self, pasta):
        cria_pasta(pasta)
        if self.__erros:
            nome_pasta = pasta + "/erros"
            cria_pasta(nome_pasta)
            erro_por_hash = groupBy(self.__erros, "hash")
            for chave, valores in erro_por_hash.items():
                nome_arquivo_erro = nome_pasta + "/" + str(chave)
                escrever_em_json(nome_arquivo=nome_arquivo_erro, data=valores)

    def cria_log_resultado(self, pasta):
        cria_pasta(pasta)
        if self.__retorno:
            nome_pasta = pasta + "/retornos"
            cria_pasta(nome_pasta)
            retorno_por_hash = groupBy(self.__retorno, "hash")
            for chave, valores in retorno_por_hash.items():
                nome_arquivo_resultado = nome_pasta + "/" + str(chave)
                escrever_em_json(nome_arquivo=nome_arquivo_resultado, data=valores)

    def cria_log_registros_lotes(self, pasta):
        cria_pasta(pasta)
        nome_arquivo = pasta + "/lote.json"
        valores = [self.__lotes]
        if os.path.exists(nome_arquivo):
            valores += (ler_de_json(nome_arquivo))
        if self.__lotes:
            escrever_em_json(nome_arquivo=nome_arquivo, data=valores,modo="w")

    def cria_logs(self, pasta):
        cria_pasta(pasta)
        self.cria_log_erro(pasta=pasta)
        self.cria_log_resultado(pasta=pasta)
        self.cria_log_registros_lotes(pasta=pasta)
        return self

    def rodar(self, Method=False, Purl=False, Pdata=False, Pheaders=False, Pfiles=False, Pjson=False, Pparam=False):
        try:
            requisicao = {
                "method": (Method if Method is not False else self.method),
                "url": (Purl if Purl is not False else self.url),
                "headers": (Pheaders if Pheaders is not False else self.headers),
                "data": (Pdata if Pdata is not False else self.data),
                "files": (Pfiles if Pfiles is not False else self.files),
                "json": (Pjson if Pjson is not False else self.json),
                "params": (Pparam if Pparam is not False else self.params),
                "verify": self.verify
            }

            resposta = request(
                method=requisicao["method"],
                url=requisicao["url"],
                headers=requisicao["headers"],
                data=requisicao["data"],
                files=requisicao["files"],
                json=requisicao["json"],
                params=requisicao["params"],
                verify=requisicao["verify"]
            )

            retorno = {
                "hash": f'get {Purl}',
                "body": requisicao,
                "retorno": resposta.text
            }
            if resposta.status_code == 200:
                self.__retorno.append(retorno)
            else:
                self.__erros.append(retorno)
                print(f"Falha ao enviar requisicao: {resposta.status_code} - {resposta.text}")
        except Exception as erro:
            jsonFormatado = json.dumps(requisicao, indent=4)
            print(f"Erro ao enviar requisicao:\n Erro:{str(erro)}\n Requisicao:{jsonFormatado}")
        return requisicao
