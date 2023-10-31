from configuracao.funcao import iniciar_configuracao, iniciar_envio
from configuracao.exclusao import iniciar_exclusao
from configuracao.extracao import iniciar_extracao
from configuracao.funcao import iniciar_sincronizacao


# Exclusão do(s) registro(s)
def exclusao():
    iniciar_exclusao([
        # {'endereco': "https://educacao.betha.cloud/service-layer/v2/api/historico-escolar/", 'tela': False},
        # {'endereco': "https://api.educacao.betha.cloud/educacao/api/pessoas/aluno/", 'tela': True},
        # {'endereco': "https://api.educacao.betha.cloud/educacao/api/pessoa/responsavel/", 'tela': True},
        # {'endereco': "https://api.educacao.betha.cloud/educacao/api/pessoa/filiacao/", 'tela': True},
        # {'endereco': "https://api.educacao.betha.cloud/educacao/api/pessoa/pessoas/", 'tela': True},
        # {'endereco': "https://api.educacao.betha.cloud/educacao/api/matriz/disciplinas/", 'tela': True},
        # {'endereco': "https://educacao.betha.cloud/service-layer/v2/api/estabelecimento/", 'tela': False},
        # {'endereco': "https://educacao.betha.cloud/service-layer/v2/api/matriz-curricular/", 'tela': False},
        # {'endereco': "https://educacao.betha.cloud/service-layer/v2/api/calendario-secretaria/", 'tela': False},
        # {'endereco': "https://educacao.betha.cloud/service-layer/v2/api/calendario-estabelecimento/", 'tela': False},
        # {'endereco': "https://educacao.betha.cloud/service-layer/v2/api/calendario-matriz-curricular/", 'tela': False},
        # {'endereco': "https://api.educacao.betha.cloud/educacao/api/matricula/turma/", 'tela': True},
        # {'endereco': "https://api.educacao.betha.cloud/educacao/api/matricula/matriculas/", 'tela': True},
        # {'endereco': "https://educacao.betha.cloud/service-layer/v2/api/quadro-vagas/", 'tela': False}
        # {'endereco': "https://educacao.betha.cloud/service-layer/v2/api/registro-avaliacao/", 'tela': False}
        # {'endereco': "https://educacao.betha.cloud/service-layer/v2/api/curso-aperfeicoamento/", 'tela': False}
    ])


# Configuração das tabelas de controle do(s) registro(s)
def configuracao():
    iniciar_configuracao(False)


# Extração dos dados
def extracao():
    iniciar_extracao('C:/Users/mateus.hemkemeier/Desktop/', [
         'testes.csv',
    ])


# Buscar, Atualizar, Enviar, Validar Lote
def transformacao():
    iniciar_envio(False, True, True, True, [
           'auditoria-imoveis'
    ])


# Consultar no banco
def sincronizar():
    iniciar_sincronizacao(False, [
        # 'item-avaliavel',
        # 'itens-educacionais',
        # 'periodo-avaliativo',
        # 'municipios'
        # 'cartorio'
    ])


if __name__ == '__main__':
    # exclusao()
    # configuracao()
    # extracao()
    # sincronizar()
    transformacao()
    pass
