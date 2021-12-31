# Projeto - Data App - Previsão do Preço de Convênio Médico

# Imports
import pandas as pd
import numpy as np
import streamlit as st
import pickle
from PIL import Image
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")


# Define a hora e a data
data_hora = datetime.now().strftime('%d/%m/%Y  -  %Hh%Mmin%Ss')

# Define o título do Dashboard
st.title("PREVISÃO DO PREÇO DE SEGUROS")


st.sidebar.title('DADOS DO CONDUTOR')

# Nome do usuário
usuario = st.sidebar.text_input("Digite seu nome")
idade = st.sidebar.slider('Selecione a idade', 18,80,18, key="age")

st.sidebar.title('DADOS DO VEÍCULO')

# Escrevendo o nome do usuário
st.write('ORÇAMENTO')

coluna1, coluna2 = st.columns(2)
with coluna1:
	st.write("CLIENTE:", usuario)
with coluna2:
	st.write('DATA:', data_hora)

# Carregando o dataframe
df = pd.read_csv('dataset_st.csv', sep = ',', encoding = 'utf-8')

# Removendo observação com erro de digitação
df_idx= df[df["Modelo_x"]=='09-MAR'].index
df= df.drop(df_idx)

# Selecionando os dados com indexação
categoria_index = df.drop(columns=[
	'Preco_Seguro_x',
	'Modelo_x',
	'Ano_x',
	'Volume_Motor_x',
	'Quilometragem_x',
	'Cilindros_x',
	'Cor_x',
	'Airbag_x',
	'Preco_Seguro_y',
	'Modelo_y',
	'Ano_y',
	'Volume_Motor_y',
	'Quilometragem_y',
	'Cilindros_y',
	'Cor_y',
	'Airbag_y'
	]).drop_duplicates().sort_values(by=['Categoria_x'])

modelo_index = df.drop(columns=[
	'Preco_Seguro_x',
	'Ano_x',
	'Categoria_x',
	'Volume_Motor_x',
	'Quilometragem_x',
	'Cilindros_x',
	'Cor_x',
	'Airbag_x',
	'Preco_Seguro_y',
	'Ano_y',
	'Categoria_y',
	'Volume_Motor_y',
	'Quilometragem_y',
	'Cilindros_y',
	'Cor_y',
	'Airbag_y'
	]).drop_duplicates().sort_values(by=['Modelo_x'])

cor_index = df.drop(columns=[
	'Preco_Seguro_x',
	'Modelo_x',
	'Ano_x',
	'Categoria_x',
	'Volume_Motor_x',
	'Quilometragem_x',
	'Cilindros_x',
	'Airbag_x',
	'Preco_Seguro_y',
	'Modelo_y',
	'Ano_y',
	'Categoria_y',
	'Volume_Motor_y',
	'Quilometragem_y',
	'Cilindros_y',
	'Airbag_y'
	]).drop_duplicates().sort_values(by=['Cor_x'])


# Variaveis de entrada
unique_categoria = list(sorted(set(categoria_index['Categoria_x'])))
unique_modelo = list(sorted(set(modelo_index['Modelo_x'])))
unique_cor = list(sorted(set(cor_index['Cor_x'])))


Categoria = st.sidebar.selectbox('Selecione a categoria', unique_categoria, key="cat")	
filtro_categoria = df[df['Categoria_x']== Categoria]
filtro_categoria = list(sorted(set(filtro_categoria['Modelo_x'])))
Modelo = st.sidebar.selectbox("Selecione o modelo",filtro_categoria, key="mod")
Ano = st.sidebar.slider('Informe o ano', 1990, 2020, 1990, key="ano")
Volume_Motor = st.sidebar.slider("Selecione o volume do motor", 0, 100, 0, key="vmotor")
Quilometragem = st.sidebar.number_input('Informe a quilometragem',  min_value= 0, key="km")
Cilindros = st.sidebar.slider("Selecione os cilindros", 0, 20, 0, key="cil")
Cor = st.sidebar.selectbox("Selecione a cor", unique_cor, key="cor")
Airbag = st.sidebar.slider ("Selecione a quantidade de airbags", 0, 20, 0, key="airbag")


# Dicionário para receber informações
dados_usuario = {'Categoria': Categoria,

				'Modelo': Modelo,

				'Ano': Ano,

				'Volume do Motor': Volume_Motor,

				'Quilometragem': Quilometragem,

				'Cilindros': Cilindros,

				'Cor': Cor,

				'Airbag': Airbag,

				}

variaveis = pd.DataFrame(dados_usuario, index=['>'])

linha1 = ['Categoria', 'Modelo', 'Ano', 'Volume do Motor', 'Quilometragem']
linha2 = ['Cilindros', 'Cor', 'Airbag']

df_linha1 = variaveis[linha1]
df_linha2 = variaveis[linha2]


st.subheader('Visualização dos Dados')
st.write(df_linha1)
st.write(df_linha2)


# Prepara os dados para as previsões
dados_novo_cliente = variaveis.copy()

for index, value in modelo_index.iterrows():

	if dados_novo_cliente['Modelo'][0] == value['Modelo_x']:
		dados_novo_cliente['Modelo'][0]= value['Modelo_y']
		break

for index, value in categoria_index.iterrows():
   
    	if dados_novo_cliente['Categoria']['>'] == value['Categoria_x']:
        	dados_novo_cliente['Categoria']['>']= value['Categoria_y']

for item in range(0,len(dados_novo_cliente['Ano']),1):
   
    	if dados_novo_cliente['Ano'][item] == df['Ano_x'][item]:
        	dados_novo_cliente['Ano'][item]= df['Ano_y'][item]

for index, value in cor_index.iterrows():
   
    	if dados_novo_cliente['Cor']['>'] ==  value['Cor_x']:
        	dados_novo_cliente['Cor']['>']= value['Cor_y']


Categoria2 = dados_novo_cliente['Categoria']
Modelo2 = dados_novo_cliente['Modelo']
Ano2 = dados_novo_cliente['Ano']
Volume_Motor2 = dados_novo_cliente['Volume do Motor']
Quilometragem2 = dados_novo_cliente['Quilometragem']
Cilindros2 = dados_novo_cliente['Cilindros']
Cor2 = dados_novo_cliente['Cor']
Airbag2 = dados_novo_cliente['Airbag']


# Lista com os valores das variáveis
dados_novo_cliente2 = [Modelo2, Ano2, Categoria2, Volume_Motor2, Quilometragem2, Cilindros2, Cor2, Airbag2]
print('dados_novo_cliente2 #################################################')
print(dados_novo_cliente2)

# Reshape
novo_cliente = np.array(dados_novo_cliente2).reshape(1, -1)


# Faz as previsões (botão)
if st.button('Calcular o Preço'):


# Carrega o modelo
	modelo_final = pickle.load(open('MODELO_FINAL.sav', 'rb')) 
	st.write("Preço previsto para o Seguro: R$ %.2f" % (modelo_final.predict(novo_cliente)))
	
	nova_consulta = st.button("Nova Consulta")


