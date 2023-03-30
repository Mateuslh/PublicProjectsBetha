from configuracao.conexao import AUTORIZACAO, consultar, executar, atualizar_lote, inserir_ocorrencia, \
    inserir_registro, inserir_lote
from datetime import datetime
from math import ceil
from hashlib import md5
from time import sleep
from requests import get, post, delete
from json import dumps
from re import match


def iniciar_configuracao(recriar=False):
    try:
        if recriar:
            executar("""DROP SCHEMA IF EXISTS public CASCADE;CREATE SCHEMA public;""")
        print('\n# Verificando existência de tabelas de controle de migração')
        resultado = consultar("""SELECT 1 
                                 FROM information_schema.tables
                                 WHERE table_schema = 'public' 
                                 AND table_name = 'controle_migracao_registro'""")
        if len(resultado) > 0:
            print('- Tabelas de controle encontradas')
        else:
            print('- Tabelas de controle não encontradas')
            configurar()
    except Exception as e:
        print(f'\n* Erro durante a execução da função "iniciar_configuracao" {e}')


def configurar():
    try:
        print("# Iniciando configuração no banco de dados.")
        resultado = open(f"configuracao/configuracao.sql", "r").read().split("--%/%")
        for comando in resultado:
            if len(comando) > 0:
                executar(comando)
        print("- Configuração efetuada com sucesso.")
    except Exception as e:
        print(f'\n* Erro durante a execução da função "configurar" {e}')


def iniciar_envio(realizar_busca, realizar_atualizacao, realizar_envio, realizar_lote, lista_registro):
    try:
        for tipo_registro in lista_registro:
            iniciar(realizar_busca, realizar_atualizacao, realizar_envio, realizar_lote, tipo_registro)
    except Exception as e:
        print(f'\n* Erro durante a execução da função "iniciar_envio" {e}')


def iniciar_sincronizacao(buscar, lista_registro):
    try:
        for tipo_registro in lista_registro:
            sincronizar(buscar, tipo_registro)
    except Exception as e:
        print(f'\n* Erro durante a execução da função "iniciar_sincronizacao" {e}')


def sincronizar(buscar, tipo_registro):
    inicio = analisar()
    try:
        print(f"# Iniciando sincronização de {tipo_registro}.")
        modulo = __import__(f'sincronizar.{tipo_registro}', globals(), locals(), ['buscar'])
        if buscar:
            lista_registro = modulo.buscar(coletar(tipo_registro))
        else:
            lista_registro = modulo.buscar()
        total = len(lista_registro['lista_controle'])
        print(f'- Encontrado(s) {total} registro(s) no cloud')
        if total > 0:
            inserir_registro(lista_registro['lista_controle'])
        print(f'# Sincronização de {tipo_registro} finalizada!')
    except Exception as e:
        print(f'\n* Erro durante a execução da função "sincronizar" {e}')
    finally:
        analisar(inicio)


def iniciar(realizar_busca, realizar_atualizacao, realizar_envio, realizar_lote, tipo_registro):
    inicio = analisar()
    try:
        modulo = __import__(f'transformacao.{tipo_registro}', globals(), locals(), ['formatar', 'enviar'])
        if realizar_busca:
            print(f'\n# Iniciando busca de dados no cloud do registro {tipo_registro}')
            lista_registro = buscar(modulo.endereco)
            total = len(lista_registro)
            print(f'- Encontrado(s) {total} registro(s) no cloud')
            if total > 0:
                inserir_registro(modulo.formatar(lista_registro))
                # print('+ Tabela de controle atualiza com sucesso')
        if realizar_envio:
            lista_registro = coletar(tipo_registro)
            if len(lista_registro) > 0:
                transformar(lista_registro, modulo)
        if realizar_lote:
            validar_lote(tipo_registro)
        if realizar_atualizacao:
            pass
        print(f'# Migração do registro {tipo_registro} finalizada!')
    except Exception as e:
        print(f'\n* Erro durante a execução da função "iniciar" {e}')
    finally:
        analisar(inicio)


def transformar(lista_registro, modulo):
    print('# Iniciando processo de transformação')
    retorno_enviar = modulo.enviar(lista_registro)
    print(f'- Processo de transformação finalizado')
    if True:
        inserir_registro(retorno_enviar['lista_controle'])
        retorno = preparar(retorno_enviar['lista_dado'], modulo.endereco, modulo.lote,
                           modulo.tipo_registro, modulo.limite, modulo.sistema)
        inserir_lote(retorno)


def coletar(tipo_registro):
    inicio = analisar()
    lista_registro = []
    try:
        print('# Iniciando a extracao dos dados a enviar')
        lista_registro = consultar(open(f'./extracao/{tipo_registro}.sql', "r", encoding='UTF-8').read())
        print(f'- {len(lista_registro)} registro(s) encontrado(s)')
        # print(f'\n- Consulta finalizada')
    except Exception as e:
        print(f'* Erro ao executar função "coletar" {e}')
    finally:
        analisar(inicio)
        return lista_registro


def buscar(endereco, limite=50, usuario=None, autorizacao=AUTORIZACAO):
    inicio = analisar()
    lista_dado = []
    try:
        proximo = True
        distancia = 0
        tipo = 0
        erro = 0
        pagina = 1
        cabecalho = {'authorization': autorizacao}
        if usuario:
            cabecalho.update({'user-access': usuario})
            endereco = endereco #+ 'list'
        while proximo:
            print(f'\r- Realizando busca na página {pagina}', end='')
            # sleep(0.5)
            requisicao = None
            # print("\nTipo de busca", tipo)
            if tipo == 0:
                requisicao = get(url=endereco, params={'offset': distancia, 'limit': limite}, headers=cabecalho)
            elif tipo == 1:
                requisicao = get(url=endereco, params={'iniciaEm': distancia, 'nRegistros': limite}, headers=cabecalho)
            if requisicao.ok:
                retorno = requisicao.json()
                if tipo == 0:
                    proximo = retorno['hasNext'] if 'hasNext' in retorno else False
                elif tipo == 1:
                    proximo = retorno['maisPaginas'] if 'maisPaginas' in retorno else False
                if tipo == 0:
                    if 'content' in retorno:
                        for i in retorno['content']:
                            lista_dado.append(i)
                elif tipo == 1:
                    if 'conteudo' in retorno:
                        for i in retorno['conteudo']:
                            lista_dado.append(i)
                else:
                    for i in retorno:
                        lista_dado.append(i)
                pagina += 1
                distancia += limite
                erro = 0
            else:
                if "iniciaEm" in requisicao.text:
                    print("\r* Iniciando busca com o tipo '1'")
                    tipo = 1
                else:
                    print(requisicao.text)
                erro += 1
            if erro >= 5:
                print('\r* Diversas requisições consecutivas retornaram erro, verificar se o servidor está ativo')
                raise Exception(requisicao.text)
        print('\n- Busca de página(s) finalizada')
    except Exception as e:
        print(f'\n* Erro durante a execução da função "buscar" {e}')
    finally:
        analisar(inicio)
        return lista_dado


def encurtar(*lista_chave):
    texto = ''
    hash_chave = None
    try:
        for chave in lista_chave:
            texto += str(chave)
        hash_chave = md5(texto.encode('utf-8')).hexdigest()
    except Exception as e:
        print(f'\n* Erro durante a execução da função "encurtar" {e}')
    finally:
        return hash_chave


def preparar(lista_dado, endereco, lote, tipo_registro, limite, sistema):
    if len(lista_dado) <= 0:
        return
    retorno_requisicao = []
    try:
        print('- Iniciando montagem e envio de lote(s)')
        lote_envio = []
        enviado = 0
        total = ceil(len(lista_dado) / limite)
        for dado in lista_dado:
            lote_envio.append(dado)
            if len(lote_envio) >= limite:
                retorno_envio = enviar_lote(lote_envio, tipo_registro, endereco, lote, sistema)
                if retorno_envio['id_lote'] is not None:
                    retorno_requisicao.append(retorno_envio)
                enviado += 1
                print(f'\r- Lote(s) enviado(s): {enviado}/{total}', end='')
                lote_envio = []
        if len(lote_envio) > 0:
            retorno_envio = enviar_lote(lote_envio, tipo_registro, endereco, lote, sistema)
            if retorno_envio['id_lote'] is not None:
                retorno_requisicao.append(retorno_envio)
        if limite != total:
            print(f'\r- Lote(s) enviado(s): {total}/{total}', end='\n')
        print(f'- Envio de lote(s) finalizado')
    except Exception as e:
        print(f'\n* Erro ao executar função "preparar" {e}')
    finally:
        return retorno_requisicao


def enviar_lote(lote_envio, tipo_registro, endereco, lote, sistema, retorno_requisicao=None):
    if 'dtoList' in lote_envio[0]:
        lote_envio = lote_envio[0]
    envio = dumps(lote_envio)
    if retorno_requisicao is None:
        retorno_requisicao = {
            'sistema': sistema,
            'tipo_registro': tipo_registro,
            'data_hora_envio': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'usuario': 'betha-migracao',
            'url_consulta': None,
            'status': 1,
            'id_lote': None,
            'conteudo_json': envio
        }
    try:
        # sleep(0.5)
        requisicao = post(endereco,
                          headers={'authorization': f'bearer {AUTORIZACAO}', 'content-type': 'application/json'},
                          data=envio)
        if requisicao.ok:
            retorno = requisicao.json()
            if 'id_lote' in retorno:
                retorno_requisicao['id_lote'] = retorno['idLote']
            elif 'id' in retorno:
                retorno_requisicao['id_lote'] = retorno['id']
            elif 'idLote' in retorno:
                retorno_requisicao['id_lote'] = retorno['idLote']
            elif 'idLot' in retorno:
                retorno_requisicao['id_lote'] = retorno['idLot']
            else:
                print('\n@ JSON: ', retorno)
                retorno_requisicao['id_lote'] = None
            # print('@ Lote enviado:', retorno_requisicao['id_lote'])
            retorno_requisicao['url_consulta'] = lote + str(retorno_requisicao['id_lote'])
        else:
            raise Exception(requisicao.text)
    except Exception as e:
        print(f'\n* Erro ao executar função "enviar_lote" {e}')
        # print(f'\r* Realizando uma nova tentativa de enviar o lote', end='')
        enviar_lote(lote_envio, tipo_registro, endereco, lote, sistema, retorno_requisicao)
    finally:
        return retorno_requisicao


def validar_lote(tipo_registro=None, incosistencia=None):
    if incosistencia is None:
        incosistencia = {'registro': 0, 'lote': 0}
    try:
        print('# Iniciando validação de lote(s) pendente(s)')
        total_validado = 0
        total_lote = 0
        pendencia = True
        while pendencia:
            comando = 'SELECT id_lote, url_consulta FROM public.controle_migracao_lotes WHERE status not in (3, 4, 5)'
            if tipo_registro is not None:
                comando += f" AND tipo_registro = '{tipo_registro}'"
            resultado = consultar(comando)
            total = len(resultado)
            pendencia = False
            if total <= 0:
                print(f'\r- Não há lote(s) pendente(s) para validação', end='\n')
                return
            if total_lote == 0:
                total_lote = total
                print(f'# Verificando {total} lote(s) pendente(s)')
            for lote in resultado:
                print(f'\r- Lotes executados: {total_validado}/{total_lote}', end='')
                endereco = lote['url_consulta']
                # sleep(0.5)
                requisicao = get(endereco, headers={'authorization': AUTORIZACAO, 'content-type': 'application/json'})
                if requisicao.ok:
                    retorno = requisicao.json()
                    if 'id' in retorno:
                        id_lote = retorno['id']
                    elif 'idLote' in retorno:
                        id_lote = retorno['idLote']
                    elif 'idLot' in retorno:
                        id_lote = retorno['idLot']
                    else:
                        id_lote = ''
                    if 'status' in retorno:
                        status = retorno['status']
                    elif 'situacao' in retorno:
                        status = retorno['situacao']
                    elif 'statusLote' in retorno:
                        status = retorno['statusLote']
                    elif 'statusLot' in retorno:
                        status = retorno['statusLot']
                    else:
                        status = ''
                    if status in ['AGUARDANDO_EXECUCAO', 'EXECUTANDO', 'QUEUE', 'PROCESSING']:
                        pendencia = True
                    else:
                        incosistencia = analisar_lote(incosistencia, retorno, id_lote, tipo_registro)
                        total_validado += 1
                        print(f'\r- Lotes executados: {total_validado}/{total_lote}', end='')
                else:
                    raise Exception(requisicao.text)
        if incosistencia["registro"] > 0:
            print(f'\n- {incosistencia["registro"]} registro(s) com inconsistência. ')
        else:
            print('\n- Nenhuma inconsistência encontrada no(s) registro(s)')
        if incosistencia["lote"] > 0:
            print(f'- {incosistencia["lote"]} lote(s) com inconsistência. ')
        else:
            print('- Nenhuma inconsistência encontrada no(s) lote(s)')
        print(f'- Consulta de lotes finalizada')
    except Exception as e:
        print(f'\n* Erro ao executar função "validar_lote" {e}')
        validar_lote(tipo_registro, incosistencia)


def analisar_lote(incosistencia, retorno, id_lote, tipo_registro):
    status_lote = None
    lista_lote = []
    lista_ocorrencia = []
    try:
        if 'status' in retorno:
            status_lote = retorno['status']
        elif 'situacao' in retorno:
            status_lote = retorno['situacao']
        elif 'statusLote' in retorno:
            status_lote = retorno['statusLote']
        elif 'statusLot' in retorno:
            status_lote = retorno['statusLot']
        if status_lote in ['EXECUTADO', 'PROCESSADO', 'PROCESSED', 'EXECUTADO_OK']:
            status_lote = 3
        elif status_lote in ['EXECUTADO_PARCIALMENTE', 'EXECUTADO_PARCIALMENTE_OK']:
            status_lote = 4
        else:
            status_lote = 5
        if status_lote in [4, 5]:
            incosistencia['lote'] += 1
        if 'id' in retorno:
            id_registro = retorno["id"]
        elif 'idLote' in retorno:
            id_registro = retorno["idLote"]
        elif 'idLot' in retorno:
            id_registro = retorno["idLot"]
        else:
            id_registro = ''
        if 'updatedIn' in retorno:
            if match('\d{2}\.\d+$', retorno['updatedIn']):
                data_hora_ret = datetime.strptime(retorno['updatedIn'], '%Y-%m-%dT%H:%M:%S.%f')
            elif match('\d{2}:\d{2}:\d{2}$', retorno['updatedIn']):
                data_hora_ret = datetime.strptime(retorno['updatedIn'], '%Y-%m-%dT%H:%M:%S')
            else:
                data_hora_ret = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            data_hora_ret = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comando = """UPDATE public.controle_migracao_lotes
                     SET status = {}, 
                     data_hora_ret = '{}'
                     WHERE id_lote = '{}'""".format(status_lote, data_hora_ret, id_registro)
        executar(comando)
        if 'retorno' in retorno:
            tipo = 'retorno'
        elif 'messageList' in retorno:
            tipo = 'messageList'
        else:
            raise Exception('* Sem tipo de retorno: ', retorno)
        for registro in retorno[tipo]:
            sistema = '0'
            status = None
            id_gerado = None
            id_integracao = None
            mensagens = None
            id_existente = None
            if 'mensagens' in registro:
                mensagens = registro['mensagens']
            elif 'message' in registro:
                mensagens = registro['message']
            elif 'mensagem' in registro:
                mensagens = registro['mensagem']
            if 'idExistente' in registro and tipo_registro != 'funcionario':
                id_existente = registro['idExistente']
            elif 'idExistente' in registro and tipo_registro == 'funcionario' and registro['idExistente'] is not None:
                inserir_registro([{'sistema': '1',
                                   'tipo_registro': 'pessoa',
                                   'descricao_tipo_registro': 'Cadastro de pessoa',
                                   'hash_chave_dsk': encurtar('1',
                                                              'pessoa',
                                                              registro['idExistente'],
                                                              registro['idIntegracao']),
                                   'id_gerado': registro['idExistente'],
                                   'i_chave_dsk1': registro['idIntegracao']}])
            if 'idIntegracao' in registro:
                id_integracao = registro['idIntegracao']
            elif 'clientId' in registro:
                id_integracao = registro['clientId']
            if 'status' in registro:
                status = registro['status']
            elif 'situacao' in registro:
                status = registro['situacao']
            elif 'mostCritical' in registro:
                status = registro['mostCritical']
            if status in ['SUCESSO', 'SUCESS', 'EXECUTADO', 'WARNING']:
                if 'id' in registro:
                    if 'iGruposMateriais' in registro['id']:
                        id_gerado = registro['id']['iGruposMateriais']
                    # elif 'iUnidadesMedidas' in registro['id']:
                    #     id_gerado = registro['id']['iUnidadesMedidas']
                    else:
                        id_gerado = registro['id'][[id_registro for id_registro in registro['id']][-1]]
                elif 'idGerados' in registro:
                    if 'idAluno' in registro['idGerados']:
                        id_gerado = registro['idGerados']['idAluno']
                    # elif 'idDisciplina' in registro['idGerados']:
                    #     id_gerado = registro['idGerados']['idDisciplina']
                    elif 'idMatricula' in registro['idGerados']:
                        id_gerado = registro['idGerados']['idMatricula']
                        if 'idEnturmacao' in registro['idGerados']:
                            inserir_registro([{'sistema':'1',
                                               'tipo_registro':'enturmacao',
                                               'descricao_tipo_registro':'Cadastro de enturmaca',
                                               'hash_chave_dsk':encurtar('1',
                                                                         'enturmaca',
                                                                         registro['idGerados']['idEnturmacao']),
                                               'id_gerado':registro['idGerados']['idEnturmacao'],
                                               'id_desktop':registro['idGerados']['idMatricula'],
                                               'i_chave_dsk1':registro['idGerados']['idMatricula']}])
                    else:
                        id_gerado = registro['idGerados'][[id_registro for id_registro in registro['idGerados']][-1]]
                elif 'idGerado' in registro:

                    # if 'iPessoas' in registro['idGerado']:
                    #     id_gerado = registro['idGerado']['iPessoas']
                    if isinstance(registro['idGerado'], int):
                        id_gerado = registro['idGerado']
                    # else:
                    #     id_gerado = registro['idGerado']
                    else:
                        id_gerado = registro['idGerado'][[id_registro for id_registro in registro['idGerado']][-1]]
                hash_chave = id_integracao
                if id_gerado is None:
                    print('\n@ id_gerado: ', registro)
                if hash_chave is None:
                    print('\n@ hash_chave: ', registro)
                if id_gerado is not None and hash_chave is not None:
                    lista_lote.append([id_gerado, hash_chave])
            elif status in ['ERRO', 'ERROR']:
                if 'mensagem' in registro and registro['mensagem'] is not None:
                    if registro['mensagem'] == "Essa avaliação já foi registrada":
                        id_existente = 1
                        mensagens = ''
                    if registro['mensagem'] == "Este registro de falta já foi cadastrado":
                        id_existente = 2
                        mensagens = ''
                if id_existente is not None:
                    id_gerado = id_existente
                    hash_chave = id_integracao
                    if id_gerado is not None and hash_chave is not None:
                        lista_lote.append([id_gerado, hash_chave])
                else:
                    # print('\n* Envio invalido: ', mensagens)
                    incosistencia['registro'] += 1
                    registro_status = 1
                    registro_resolvido = 1
                    lista_ocorrencia.append((id_integracao, sistema, tipo_registro, None, 9, registro_status,
                                             registro_resolvido, 1, id_lote, mensagens, '', '', id_existente))
            else:
                print('\n@ JSON: ', registro)
        inserir_ocorrencia(lista_ocorrencia)
        atualizar_lote(lista_lote)
    except Exception as e:
        print(f'\n* Erro ao executar função "analisar_lote" {e}')
    finally:
        return incosistencia


def excluir(lista_registro, endereco, usuario=None, autorizacao=AUTORIZACAO, tipo='CLOUD'):
    total = len(lista_registro)
    if total <= 0:
        return
    inicio = analisar()
    print(f'- Encontrado(s) {total} registro(s) no cloud')
    for indice, registro in enumerate(lista_registro):
        dado = []
        print(f"\r- Excluindo identificador {str(registro['id'])} ({round(((indice + 1) * 100) / total, 2)}%)", end='')
        cabecalho = {"authorization": autorizacao, 'content-type': 'application/json'}
        if usuario is not None:
            cabecalho.update({'user-access': usuario})
        if tipo == 'CLOUD':
            dado.append({
                'idGerado': registro['id'],
                'conteudo': {
                    'id': registro['id']
                }
            })
            dado = dumps(dado)
        elif tipo == 'FLY':
            dado.append({
                'dtoList': [
                    {
                        registro['descricao']: {
                            registro['identificador']: registro['id']
                        }
                    }
                ]
            })
            dado = dumps(dado[0])
        try:
            requisicao = delete(endereco + (str(registro['id']) if usuario is not None else ''),
                                headers=cabecalho, data=dado)
            if requisicao.ok:
                pass
            else:
                raise Exception(requisicao.text)
        except Exception as e:
            print(f'\n* Erro ao executar função "excluir" {e}')
    analisar(inicio)


def analisar(dh_inicio=None):
    if dh_inicio is None:
        return datetime.now()
    else:
        print(f'@ Processo finalizado. ({round((datetime.now() - dh_inicio).total_seconds(), 2)} segundos)')
