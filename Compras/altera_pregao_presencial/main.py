import funcoesGerais

headers = {
    "Authorization":"Bearer 123abc45-d678-9e01-2345-67fg8h9i01j2"
}

ids = open("id.txt","r").read().split("|")
log = open("DadosAlterados.txt", "a")
backup = open("Backup.JSON", "a")


funcoesGerais.altera_pregao_presencial(arquivoLog=log,ids=ids,headers=headers)
funcoesGerais.alimentaBackup(ids=ids,arquivoBackup=backup,headers=headers)

