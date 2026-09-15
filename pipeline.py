import pandas as pd
import numpy as np
df = pd.read_csv('vendas_livrarias.csv')

#variavel utilizada para checar duplicatas
#tp = pd.concat((df['livro'].duplicated().rename('duplicata'), df['livro']), axis=1)

#arrumando valores nulos
df[]=


#padronizando os valores
remocao = str.maketrans(',', '.', 'R$')
df['preco_unitario'] = df['preco_unitario'].str.translate(remocao)
df['custo_unitario'] = df['custo_unitario'].str.translate(remocao)
df['preco_unitario'] = df['preco_unitario'].astype(float)
df['custo_unitario'] = df['custo_unitario'].astype(float)
df['data_venda'] = pd.to_datetime(df['data_venda'])
df = df.drop_duplicates(subset = ['livro'], keep = 'first')

#enriquecendo os dados
df['receita_total'] = df['quantidade_vendida'] * df['preco_unitario']
df['margem_lucro'] = (df['custo_unitario'] - df['preco_unitario']) * df['quantidade_vendida']
df['alerta_prejuizo'] = np.where(df['margem_lucro'] > 0, True, False) 


#df[df['quantidade_vendas']>5]

print(df)