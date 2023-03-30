from psycopg2 import connect, DatabaseError
from os import getenv
from dotenv import load_dotenv
from os.path import join, dirname


load_dotenv(join(dirname(__file__), '../.env'))
AUTORIZACAO = getenv("TOKEN")
if not (AUTORIZACAO.lower().startswith('bearer')):
    AUTORIZACAO = f'bearer {AUTORIZACAO}'
TOKENUSER = getenv("TOKENUSER")
if not (TOKENUSER.lower().startswith('bearer')):
    TOKENUSER = f'bearer {TOKENUSER}'
ACCESSUSER = getenv("ACCESSUSER")
APPCONTEXT = getenv("APPCONTEXT")

def conectar():
    conexao = None
    try:
        conexao = connect(host=getenv("HOST"), port=getenv("PORT"), database=getenv("DATABASE"), user=getenv("USER"),
                          password=getenv("PASSWORD"))
    except (Exception, DatabaseError) as e:
        print(f'\n* Erro ao executar função "conectar". {e}')
    finally:
        return {'cursor': conexao.cursor(), 'conexao': conexao}


def executar(comando, registro=None, unico=True):
    conexao = conectar()
    try:
        if unico:
            if registro:
                conexao['cursor'].execute(comando, registro)
            else:
                conexao['cursor'].execute(comando)
        else:
            conexao['cursor'].executemany(comando, registro)
        conexao['conexao'].commit()
    except (Exception, DatabaseError) as e:
        print(f'\n* Erro ao executar função "executar". {e}')
    finally:
        conexao['cursor'].close()


def consultar(comando):
    conexao = conectar()
    lista_dado = []
    try:
        conexao['cursor'].execute(comando)
        resultado = conexao['cursor'].fetchall()
        for i, descricao in enumerate(resultado):
            lista_dado.append({})
            for j, valor in enumerate([d[0] for d in conexao['cursor'].description]):
                lista_dado[i][valor] = descricao[j]
    except (Exception, DatabaseError) as e:
        print(f'\n* Erro ao executar função "consultar". {e}')
    finally:
        conexao['cursor'].close()
        return lista_dado


def inserir_registro(lista_registro, limite=200):
    if len(lista_registro) <= 0:
        return
    try:
        lista_dado = []
        comando = """INSERT INTO public.controle_migracao_registro 
                     (sistema, tipo_registro, hash_chave_dsk, descricao_tipo_registro, id_desktop, id_gerado, i_chave_dsk1, 
                     i_chave_dsk2, i_chave_dsk3, i_chave_dsk4, i_chave_dsk5, i_chave_dsk6, i_chave_dsk7, 
                     i_chave_dsk8,i_chave_dsk9, i_chave_dsk10, i_chave_dsk11, i_chave_dsk12, json_enviado) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                     ON CONFLICT (hash_chave_dsk) DO UPDATE SET
                     json_enviado = EXCLUDED.json_enviado,id_gerado = %s"""
        for registro in lista_registro:
            dado = (
                registro.get('sistema'),
                registro.get('tipo_registro'),
                registro.get('hash_chave_dsk'),
                registro.get('descricao_tipo_registro'),
                registro.get('id_desktop'),
                registro.get('id_gerado'),
                registro.get('i_chave_dsk1'),
                None if 'i_chave_dsk2' not in registro else registro.get('i_chave_dsk2'),
                None if 'i_chave_dsk3' not in registro else registro.get('i_chave_dsk3'),
                None if 'i_chave_dsk4' not in registro else registro.get('i_chave_dsk4'),
                None if 'i_chave_dsk5' not in registro else registro.get('i_chave_dsk5'),
                None if 'i_chave_dsk6' not in registro else registro.get('i_chave_dsk6'),
                None if 'i_chave_dsk7' not in registro else registro.get('i_chave_dsk7'),
                None if 'i_chave_dsk8' not in registro else registro.get('i_chave_dsk8'),
                None if 'i_chave_dsk9' not in registro else registro.get('i_chave_dsk9'),
                None if 'i_chave_dsk10' not in registro else registro.get('i_chave_dsk10'),
                None if 'i_chave_dsk11' not in registro else registro.get('i_chave_dsk11'),
                None if 'i_chave_dsk12' not in registro else registro.get('i_chave_dsk12'),
                None if 'json' not in registro else registro.get('json'),
                None if 'id_gerado' not in registro else registro.get('id_gerado')
            )
            lista_dado.append(dado)
        lista_cortada = ([lista_dado[i:i + limite] for i in range(0, len(lista_dado), limite)])
        for registro in lista_cortada:
            executar(comando, registro, False)
    except Exception as e:
        print(f'\n* Erro ao executar função "inserir_registro". {e}')


def inserir_lote(lista_registro, limite=200):
    if len(lista_registro) <= 0:
        return
    # print(f'+ Inserindo dados na tabela de controle de lotes.')
    try:
        comando = """INSERT INTO public.controle_migracao_lotes 
                     (sistema, tipo_registro, data_hora_env, usuario, url_consulta, status,
                     id_lote, conteudo_json) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        lista_dado = []
        for registro in lista_registro:
            lista_dado.append((registro['sistema'], registro['tipo_registro'],
                               registro['data_hora_envio'], registro['usuario'],
                               registro['url_consulta'], registro['status'],
                               registro['id_lote'], registro['conteudo_json']))
        lista_cortada = ([lista_dado[i:i + limite] for i in range(0, len(lista_dado), limite)])
        for registro in lista_cortada:
            executar(comando, registro, False)
    except Exception as e:
        print(f'\n* Erro ao executar função "inserir_lote". {e}')


def atualizar_lote(lista_registro, limite=500):
    if len(lista_registro) <= 0:
        return
    try:
        comando = "UPDATE public.controle_migracao_registro SET id_gerado = %s WHERE hash_chave_dsk = %s"
        lista_dado = []
        for registro in lista_registro:
            lista_dado.append((registro[0], registro[1]))
        lista_cortada = ([lista_dado[i:i + limite] for i in range(0, len(lista_dado), limite)])
        for registro in lista_cortada:
            executar(comando, registro, False)
    except Exception as e:
        print(f'\n* Erro ao executar função "atualizar_lote". {e}')


def inserir_ocorrencia(lista_registro):
    if len(lista_registro) <= 0:
        return
    try:
        # print('+ Inserindo dados na tabela de controle de ocorrências.')
        comando = """INSERT INTO public.controle_migracao_registro_ocor
                     (hash_chave_dsk, sistema, tipo_registro, id_gerado, origem, situacao, resolvido,
                     i_sequencial_lote, id_integracao, mensagem_erro, mensagem_ajuda, json_enviado, id_existente)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        for registro in lista_registro:
            executar(comando, registro)
    except Exception as e:
        print(f'\n* Erro ao executar função "inserir_ocorrencia". {e}')
