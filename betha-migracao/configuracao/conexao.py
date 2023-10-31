from pyodbc import connect, DatabaseError
from os import getenv
from dotenv import load_dotenv
from os.path import join, dirname
from json import dumps

load_dotenv(join(dirname(__file__), '../.env'))
AUTORIZACAO = getenv("TOKEN")
if not (AUTORIZACAO.lower().startswith('bearer')):
    AUTORIZACAO = f'bearer {AUTORIZACAO}'
TOKENUSER = getenv("TOKENUSER")
if not (TOKENUSER.lower().startswith('bearer')):
    TOKENUSER = f'bearer {TOKENUSER}'
ACCESSUSER = getenv("ACCESSUSER")
APPCONTEXT = getenv("APPCONTEXT")
ODBC = getenv("ODBC")


def conectar():
    conexao = None
    try:
        conexao = connect(f'DSN={ODBC}', ConnectionIdleTimeout=0)
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
            print(comando, registro)
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
        for registro in lista_registro:
            dado = """IF EXISTS (
    SELECT hash_chave_dsk FROM bethadba.controle_migracao_registro WHERE hash_chave_dsk = '{}'
) BEGIN
    UPDATE bethadba.controle_migracao_registro SET
        id_gerado = '{}'
    WHERE hash_chave_dsk = '{}'
END ELSE BEGIN
    INSERT INTO bethadba.controle_migracao_registro (
        sistema, tipo_registro, hash_chave_dsk, id_gerado, i_chave_dsk1, 
        i_chave_dsk2, i_chave_dsk3, i_chave_dsk4, i_chave_dsk5, i_chave_dsk6, i_chave_dsk7, 
        i_chave_dsk8, i_chave_dsk9, i_chave_dsk10, i_chave_dsk11, i_chave_dsk12
    ) VALUES (
        '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'
    )
END
                  """.format(
                registro.get('hash_chave_dsk'),
                registro.get('id_gerado'),
                registro.get('hash_chave_dsk'),
                registro.get('sistema'),
                registro.get('tipo_registro'),
                registro.get('hash_chave_dsk'),
                registro.get('id_gerado'),
                registro.get('i_chave_dsk1'),
                '' if 'i_chave_dsk2' not in registro else registro.get('i_chave_dsk2'),
                '' if 'i_chave_dsk3' not in registro else registro.get('i_chave_dsk3'),
                '' if 'i_chave_dsk4' not in registro else registro.get('i_chave_dsk4'),
                '' if 'i_chave_dsk5' not in registro else registro.get('i_chave_dsk5'),
                '' if 'i_chave_dsk6' not in registro else registro.get('i_chave_dsk6'),
                '' if 'i_chave_dsk7' not in registro else registro.get('i_chave_dsk7'),
                '' if 'i_chave_dsk8' not in registro else registro.get('i_chave_dsk8'),
                '' if 'i_chave_dsk9' not in registro else registro.get('i_chave_dsk9'),
                '' if 'i_chave_dsk10' not in registro else registro.get('i_chave_dsk10'),
                '' if 'i_chave_dsk11' not in registro else registro.get('i_chave_dsk11'),
                '' if 'i_chave_dsk12' not in registro else registro.get('i_chave_dsk12'),
                '' if 'id_gerado' not in registro else registro.get('id_gerado')
            )
            lista_dado.append(dado)
        lista_cortada = ([lista_dado[i:i + limite] for i in range(0, len(lista_dado), limite)])
        for registro in lista_dado:
            executar(registro)

    except Exception as e:
        print(f'\n* Erro ao executar função "inserir_registro". {e}')


def inserir_lote(lista_registro, limite=200):
    if len(lista_registro) <= 0:
        return
    # print(f'+ Inserindo dados na tabela de controle de lotes.')
    try:

        lista_dado = []
        for registro in lista_registro:
            dado = """INSERT INTO bethadba.controle_migracao_lotes 
                                 (sistema, tipo_registro, data_hora_env, usuario, url_consulta, status,
                                 id_lote) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(
                                registro['sistema'], registro['tipo_registro'],
                               registro['data_hora_envio'], registro['usuario'],
                               registro['url_consulta'], registro['status'],
                               registro['id_lote'])
            lista_dado.append(dado)
        lista_cortada = ([lista_dado[i:i + limite] for i in range(0, len(lista_dado), limite)])
        for registro in lista_dado:
            executar(registro)
    except Exception as e:
        print(f'\n* Erro ao executar função "inserir_lote". {e}')


def atualizar_lote(lista_registro, limite=500):
    if len(lista_registro) <= 0:
        return
    try:

        lista_dado = []
        for registro in lista_registro:
            lista_dado.append("UPDATE bethadba.controle_migracao_registro SET id_gerado = '{}' WHERE hash_chave_dsk = '{}'".format(registro[0], registro[1]))
        lista_cortada = ([lista_dado[i:i + limite] for i in range(0, len(lista_dado), limite)])
        for registro in lista_dado:
            executar(registro)
    except Exception as e:
        print(f'\n* Erro ao executar função "atualizar_lote". {e}')


def inserir_ocorrencia(lista_registro):
    if len(lista_registro) <= 0:
        return
    try:
        # print('+ Inserindo dados na tabela de controle de ocorrências.')
        for registro in lista_registro:
            print(registro)
            registro = dumps(registro)
            print(registro)
            dado = """INSERT INTO bethadba.controle_migracao_registro_ocor
                                 (hash_chave_dsk, sistema, tipo_registro, id_gerado, origem, situacao, resolvido,
                                 i_sequencial_lote, id_integracao, mensagem_erro, mensagem_ajuda, id_existente)
                                 VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(
                registro[1], registro[2], registro[2],
                registro[3], registro[4], registro[4], registro[5],
                registro[6], registro[7], registro[8], registro[9],
             registro[10]
            )
            executar(dado)
    except Exception as e:
        print(f'\n* Erro ao executar função "inserir_ocorrencia". {e}')
