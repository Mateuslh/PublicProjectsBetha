# Betha Migração

Ferramenta com objetivo de migração, utilizando o clico de análise de dados ETL (Extrair, Transformar e Carregar), permitindo ser o mais flexível e útil.

## Instalar dependência:
- Executar o comando `pip install -r requirements.txt`

## Configurar ambiente:
- Adicionar arquivo `.env`
- Preencher conforme `.env-example`

## Funcionamento:
Executar o arquivo `migracao.py`, ao qual contem os metódos:
- `iniciar_exclusao` onde exclui registros preenchidos conforme parâmetro.
- `iniciar_configuracao` encarregado de verificar se existe ou executar a criação das tabelas de controle da migração.
- `iniciar_extracao` executa conforme sua migração a importação dos dados.
- `iniciar_envio` responsável por iniciar processo de transfomrmação e envio dos dados conforme construídos na [transformacao](transformacao).