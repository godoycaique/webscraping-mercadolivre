import pandas as pd
from datetime import datetime
import sqlite3

#Ler arquivo CSV
mercadolivre_df = pd.read_json('..\data\data.jsonl', lines=True)

#Setar pandas para ler todas as colunas
pd.options.display.max_columns = None

#Adicionar data e hora da coleta
mercadolivre_df['_data_coleta'] = datetime.now()

#Adicionar coluna com posição do item na pagina
mercadolivre_df['_rk_position'] = pd.RangeIndex(start=1, stop=len(mercadolivre_df) + 1)

#Converter colunas de valores para float
mercadolivre_df['old_price'] = mercadolivre_df['old_price'].fillna(0).astype(float)
mercadolivre_df['old_cents'] = mercadolivre_df['old_cents'].fillna(0).astype(float)
mercadolivre_df['new_price'] = mercadolivre_df['new_price'].fillna(0).astype(float)
mercadolivre_df['new_cents'] = mercadolivre_df['new_cents'].fillna(0).astype(float)
mercadolivre_df['rating'] = mercadolivre_df['rating'].fillna(0).astype(float)

#Tratar colunas de reais e centavos
mercadolivre_df['old_price'] = mercadolivre_df['old_price'] + mercadolivre_df['old_cents'] / 100
mercadolivre_df['new_price'] = mercadolivre_df['new_price'] + mercadolivre_df['new_cents'] / 100

#Tratar coluna com dados da busca
mercadolivre_df['_search'] = mercadolivre_df['search'].str.split('/').str[3]

#Dropar colunas não utilizadas
mercadolivre_df = mercadolivre_df.drop(columns=['old_cents', 'new_cents', 'search'])

#Conectar ao banco de dados SQLite
conn = sqlite3.connect('../data/quotes.db')

#Salvar o DataFrame no banco de dados SQLite
mercadolivre_df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

#Fechar a conexão com o banco de dados
conn.close()