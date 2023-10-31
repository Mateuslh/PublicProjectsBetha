def formata_filtro_betha(string):
    elementos = string.replace("\n", "").replace(" ", "").split(",")
    map = {}
    for elemento in elementos:
        partes = elemento.split(".")
        chave = partes[0]
        if chave not in map:
            map[chave] = []
        if len(partes) > 1:
            map[chave].append(".".join(partes[1:]))
    estrutura = ""
    for chave, subelementos in map.items():
        estrutura += chave
        if subelementos:
            estrutura += "(" + formata_filtro_betha(",".join(subelementos)) + ")"
        estrutura += ","
    return estrutura.rstrip(",")