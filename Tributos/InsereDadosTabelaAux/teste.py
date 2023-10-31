import pandas as pd

imoveis_df = pd.read_csv('audit_imoveis.csv', encoding='latin1', sep=';')

print(imoveis_df)