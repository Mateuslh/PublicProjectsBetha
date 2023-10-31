def ler_arquivo(path,encoding='utf-8'):
    linhas = []
    try:
        with open(path, 'r', encoding=encoding) as arquivo:
            for linha in arquivo:
                linhas.append(linha.strip())
    except FileNotFoundError:
        print(f"O arquivo '{path}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {str(e)}")

    return linhas
def escrever_arquivo(nome_arquivo, linhas):
    try:
        with open(nome_arquivo, 'w') as arquivo:
            for linha in linhas:
                arquivo.write(str(linha) + '\n')

        print(f'O arquivo "{nome_arquivo}" foi criado e o conteúdo foi escrito com sucesso.')
    except Exception as e:
        print(f"Ocorreu um erro ao escrever no arquivo: {str(e)}")