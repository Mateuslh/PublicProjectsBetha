import requests, json
url = "https://tributos.betha.cloud/service-layer-tributos/api/registrosTabaux"
headers = {
"Authorization":"Bearer 76bfad59-8be6-4397-adc4-826f4b377162"
}
def post_em_lote(registro, tamanhoLote, bearer, api, operacao, analisaLote):
    from math import ceil
    x = 0
    totalLotes = ceil(len(registro) / tamanhoLote)
    for j in range(1, ceil(len(registro) / tamanhoLote) + 1):
        print(f"----Enviando lote {j} de {totalLotes}")
        payload = registro[x:x + tamanhoLote]
        payload = json.dumps(payload)
        # print(payload)
        envia_verifica_lote(bearer=bearer, api=api, payload=payload, operacao=operacao, analisaLote=analisaLote)
        x += tamanhoLote