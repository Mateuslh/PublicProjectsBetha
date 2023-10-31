import os

def existe_pasta(path):
    return os.path.exists(path)

def cria_pasta(path):
    if not existe_pasta(path):
        os.mkdir(path)
