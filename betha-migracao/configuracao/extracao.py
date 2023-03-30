from json import loads
from re import search,findall
from configuracao.conexao import executar
from configuracao.funcao import analisar


def iniciar_extracao(diretorio, envio):
    inicio = analisar()
    for arquivo in envio:
        registro = search("(.*)\.[^.]+$", arquivo).group(1)
        with open(diretorio + arquivo, encoding='ISO-8859-1') as conteudo:
            extrair(registro, conteudo.read())
    analisar(inicio)


def extrair(registro, conteudo):
    inicio = analisar()
    print(f"\n# Iniciando leitura: {registro}")
    lista_chave = []
    conteudo = conteudo.split('\n')
    primeira = conteudo[0].split('@@@@@@@@')
    conteudo.pop(0)
    conteudo.pop(-1)
    for coluna in primeira:
        lista_chave.append(coluna)
    drop = """DROP TABLE IF EXISTS public.{} CASCADE""".format(registro)
    create = """CREATE TABLE IF NOT EXISTS public.{} (
                i_sequencial serial NOT NULL,
                {})""".format(registro, ",".join([i + " text NULL" for i in set(lista_chave)]))
    executar(drop)
    executar(create)
    lista_inserir = []
    lista_erros = []
    total = len(conteudo)
    for indice, linha in enumerate(conteudo):
        lista_dados = []
        linha = linha.replace('""', '" "')


        # textoCerto = '1,2,"123",3,"123"'
        # textoErrado = '1,2,"123,"",3,"123"'


        if findall('("[^",]*("[^",]*)+")',linha) is not None:
            for grupo in findall('("[^",]*("[^",]*)+")',linha):
                linha = linha.replace(grupo[0],'"'+grupo[0].replace('"','')+'"')
        if findall('("[^"]*[^"]")',linha) is not None:
            for grupo in findall('("[^"]*[^"]")',linha):
                linha = linha.replace(grupo,grupo.replace(',',';;;'))
        linha = linha.split('@@@@@@@@')
        # print(linha)
        for dado in linha:
            dado = dado.replace('"', '')
            dado = dado.replace(';;;', ',')
            if dado in (' ','','   ','    '):
                dado = None
            lista_dados.append(dado)
        print(f'\r+ Gerando registro: {indice+1}', end='\n' if indice == total - 1 else '')
        if len(lista_chave) == len(lista_dados):
            lista_inserir.append("""INSERT INTO public.{}({}) VALUES({})
                    """.format(registro,
                               ",".join(lista_chave),
                               ",".join(['null' if lista_dados[i] is None else "'"+str.replace(lista_dados[i], "'", "''").strip()+"'" for i in
                                         range(len(lista_dados))])))
        else:
            lista_erros.append(indice)
    if len(lista_erros) >0:
        print(f'\nLinhas que geraram mais colunas {lista_erros}')
    dados = ";".join(lista_inserir)
    executar(dados)
    analisar(inicio)
