import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Configuração Visual
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# 2. Carregamento dos Dados (Ajustado para os nomes dos seus arquivos)
print("Carregando arquivos...")
df_pedidos = pd.read_csv('olist_orders_dataset.csv')
df_itens = pd.read_csv('olist_order_items_dataset.csv')
df_clientes = pd.read_csv('olist_customers_dataset.csv')

# 3. Limpeza e Transformação de Datas
df_pedidos['order_purchase_timestamp'] = pd.to_datetime(df_pedidos['order_purchase_timestamp'])
df_pedidos['order_delivered_customer_date'] = pd.to_datetime(df_pedidos['order_delivered_customer_date'])

# Filtrar apenas pedidos entregues
df_entregues = df_pedidos[df_pedidos['order_status'] == 'delivered'].copy()

# 4. Cruzamento de Tabelas (Merge)
# Unindo Pedidos + Itens (para ter o Preço)
df_final = pd.merge(df_entregues, df_itens, on='order_id', how='inner')

# Unindo com Clientes (para ter a Localização)
df_completo = pd.merge(df_final, df_clientes, on='customer_id', how='inner')

# 5. ANÁLISE 1: Faturamento Mensal
df_completo['mes_ano'] = df_completo['order_purchase_timestamp'].dt.to_period('M').astype(str)
vendas_mensais = df_completo.groupby('mes_ano')['price'].sum().reset_index()

plt.figure()
sns.lineplot(data=vendas_mensais, x='mes_ano', y='price', marker='o', color='teal')
plt.title('Evolução do Faturamento Mensal', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.ylabel('Faturamento (R$)')
plt.show()

# 6. ANÁLISE 2: Top 5 Estados por Faturamento
top_estados = df_completo.groupby('customer_state')['price'].sum().sort_values(ascending=False).head(5).reset_index()

plt.figure()
sns.barplot(data=top_estados, x='customer_state', y='price', palette='viridis')
plt.title('Top 5 Estados em Faturamento', fontsize=14, fontweight='bold')
plt.ylabel('Total (R$)')
plt.show()

# 7. ANÁLISE 3: Logística (Prazo Médio de Entrega)
df_completo['prazo_entrega'] = (df_completo['order_delivered_customer_date'] - df_completo['order_purchase_timestamp']).dt.days
media_entrega = df_completo[df_completo['prazo_entrega'] >= 0].groupby('customer_state')['prazo_entrega'].mean().sort_values(ascending=False).reset_index()

plt.figure()
sns.barplot(data=media_entrega, x='customer_state', y='prazo_entrega', palette='Reds_r')
plt.title('Média de Dias para Entrega por Estado', fontsize=14, fontweight='bold')
plt.axhline(df_completo['prazo_entrega'].mean(), color='black', linestyle='--', label='Média Nacional')
plt.legend()
plt.show()

print("Análise concluída com sucesso!")
