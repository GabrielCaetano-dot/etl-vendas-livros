import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

#configuração do banco de dados
load_dotenv()

usuario = os.getenv('DB_USER')
senha = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
porta = os.getenv('DB_PORT')
banco = os.getenv('DB_NAME')

engine = create_engine(f'postgresql+psycopg2://{usuario}:{senha}@{host}:{porta}/{banco}')

#importando tabela
df = pd.read_csv('vendas_livrarias.csv')

#arrumando valores nulos
df['filial'] = df['filial'].fillna(value = 'Não Informado')
df['categoria'] = df['categoria'].fillna(value = 'Não Informado')
df = df.dropna(subset = 'quantidade_vendida')
df = df.dropna(subset = 'preco_unitario')
df = df.dropna(subset = 'custo_unitario')
df = df.dropna(subset = 'data_venda')

#padronizando os valores
remocao = str.maketrans(',', '.', 'R$')
df['preco_unitario'] = df['preco_unitario'].str.translate(remocao)
df['custo_unitario'] = df['custo_unitario'].str.translate(remocao)
df['preco_unitario'] = df['preco_unitario'].astype(float)
df['custo_unitario'] = df['custo_unitario'].astype(float)
df['data_venda'] = pd.to_datetime(df['data_venda'], dayfirst = True)
df = df.drop_duplicates(subset = ['livro','filial', 'data_venda'], keep = 'first')

#enriquecendo os dados
df['receita_total'] = (df['quantidade_vendida'] * df['preco_unitario']).round(2)
df['margem_lucro'] = ((df['preco_unitario'] - df['custo_unitario']) * df['quantidade_vendida']).round(2)
df['alerta_prejuizo'] = np.where(df['margem_lucro'] < 0, True, False) 

#exportando tabela com filtro
df[df['quantidade_vendida']>5].to_sql(name='vendas', con = engine, if_exists = 'replace', index = False)
