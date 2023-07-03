import sys
import os
sys.path.append(os.getcwd())
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dash_table, dcc
from datetime import date
from app import app
from callback_apps  import callback_page1
from datetime import datetime
from components import my_components as c1

df = pd.read_csv(r'data\sales_data.csv', index_col = 0)
text_font_size = '18px'
radio_valor = dbc.Col(
                dcc.RadioItems(id='radio-item-value', 
                                        options=[
                                            {'label': 'Z-Score', 'value': 'Score'},
                                            {'label': 'X-Value', 'value': 'X-Value'},
                                            {'label': 'MinMaxScaler', 'value': 'MinMaxScaler'}
                                        ], 
                                        value='MinMaxScaler',
                                        inline=True,
                                        labelStyle={'display': 'inline-block', 'margin-right': '10px', 'margin-top': '5px'},
                                        style = {'font-size': text_font_size}
                                    ),
                                width=9,
                            )



# Montagem do layout
layout = html.Div(
    [   
    dbc.Container(
        [
        dcc.Markdown(
            """
            # Impacto de produtos no Faturamento do Hotmart

            Nessa análise, vão ser investigados como os produtos mais populares e de maior faturamento impactam o desempenho financeiro da Hotmart. 
            
            O objetivo principal é compreender a relação entre esses produtos e o faturamento da empresa, proporcionando insights sobre os principais 
            impulsionadores do sucesso financeiro da Hotmart.

            ## Pré-processamento e desáfios da análise

            Antes de seguir para análise alguns passos anteiores foram necessários para obtenção de resultados, nessa seção o foco é na explicação desses passos.

            #### Dados codificados com Z-Score

            Os dados de preço foram codificiados para impedir o vazamento de informações, utilizando o Z-Score.
            Utilizando Z-Score a média dos valores é definida como zero, os valores abaixo da média são negativos e os acima da média positivos, o que nos leva a alguns problemas:

                1- A soma direta dos valores dos Z-Score vão levar a inconsistências. 
                    Ex: Produtos com valor abaixo da média vão ficar mais negativos com maior tiragem.

                2- Produtos com valores próximos da média, vão ter contribuição zero ao valor total.

                3- O Z-Score pode ser utilizado para avaliar o Ticket médio dos produtos. Mas para contribuição total, uma análise direta não seria tão fácil.
            
            Para lidar com isso eu testei 2 abordagens:

            1- Testei a definição de valores médios e desvio padrão, para ver o comportamento dos valores.

            2- Fiz uma normalização dos dados utilizando MinMaxScale de (0.001-1)

            Fiz uma insepeção visual nos valores de cursos no site da hotmart para ter uma noção de preço dos produtos.
            Acabei encontrando produtos indo de $1 até $10000, mas como os valores são de 2016 acreditei que seria mais seguro ir com os valores de MinMaxScale que assumem que o produto de menor valor é 1000 vezes mais barato que o de maior valor. 

            Abaixo é possível visualizar os valores do Z-Score, X-Value e MinMaxScaler. Para o X-Value em especifico é possível utilizar os inputs para observar diferentes valores de média e desvio padrão.

            #### Indicadores de valores de produto (Z-Score)"""),
    radio_valor,
    dbc.Row(
        [dbc.Col(c1.input_top_label(id='valor-mean-transform-z', label='Valor médio', value = 30), width=2),
         dbc.Col(c1.input_top_label(id='valor-std-transform-z', label='Desvio padrão', value = 50), width=2)]
        ),
    dbc.Row([
            c1.indicator_card(id='indicador-produto-barato', width=4),
            c1.indicator_card(id='indicador-produto-caro', width=4),
            c1.indicator_card(id='indicador-faturamento', width=4),
            ]),
    dcc.Markdown(
        """
        
        Abaixo é possível observar como o faturamento acumulado da Hotmart é afetado pelos produtos de maior faturamento.
        
        No gráfico de barras abaixo é possível observar o percentual de cada um dos grupos 

        Olhando para os observamos que mais de 90% do Faturamento da Hotmart é gerado apenas por 20% dos produtos, algo similar ao observado em outros mercados que seguem o príncipio de pareto (80/20).

        Exmplo de uso do Slider:
        Se o slider está em 90% significa, 10% dos produtos com maior faturamento são considerados "Maiores Produtos", os outros 90% "Outros Produtos".


        *Atenção os valores do gráfico para o **Z-Score** não funcionam corretamente, devido a natureza do **Z-Score**, valores negativos e valores médios em zero.
        Podemos observar por exemplo que temo       
        Para *X-Value* e *MinMaxScaler* essa relação esta em formato de percentual, já para *Z-Score* estão os valores brutos.

        """),
        dbc.Label('Threshold maiores produtores',
                  size="md",
                  style={'font-size': text_font_size}),
        dcc.Slider(min=0, max=100, step=5, value=90, id='threshold-slider')
        ,
        dcc.Markdown("#### Evolução percentual faturamento Total, por percentil de produtos"),
        dbc.Row(
        dbc.Col(
            [
                dcc.Graph(
                    id='line-cumulative-revenue',
                    figure={},
                    style={'width': '100%'}
                ),
            ],
            width= 12 #{'offset': 2},  # Adjust the width and offset as needed
        ),
        justify='center',
    ),
        dcc.Markdown("#### Faturamento Total, por tipo de produtos"),
        dbc.Row(
        dbc.Col(
            [
                dcc.Graph(
                    id='bar-cumulative-revenue',
                    figure={},
                    style={'width': '100%'}
                ),
            ],
            width= 12 #{'offset': 2},  # Adjust the width and offset as needed
        ),
        justify='center',
    ),
    dcc.Markdown(
        """
            ## Aumentando o Faturamento da Hotmart
            A partir da análise anterior conseguimos observar que o valor total vendido na Hotmart é altamente dependente dos maiores produtores.
            Uma das formas de reduzir as dependências com esses produtos, é fazendo com que outros produtos aumentem o seu faturamento.

            Para fazer isso, a forma escolhida vai ser entender quais são os principais Drivers para aumento da venda de produtos.
            Para obter isso foram geradas Features que vão permitir entender melhor como indicar para um Produtor entender como trazer mais atenção a seu produto.

            A partir dessa seção vamos focar em análises para desenvolvimento de Features e resultados obtidos. Todas essas análises estão assumindo normalização via MinMaxScaler.

            *Esse é um modelo inicial, e existem muitos avanços a serem feitos tanto na construção de novas features quanto na melhoria do Pipeline.*

            ### Exploração dos dados

            Primeiro foi observado a varibilidade dos preços dos produtos, abaixo é possível observar a grande diferença entre os Outliers e os valores abaixo do último quartil.
        """),
        dcc.Markdown(
        """
            Com isso o foco que foi dado ao projeto, foi gerar um classificador que identifica em qual quartil um projeto com certas características vai cair.
            Isso possibilita identificar as principais variáveis responsáveis por alto faturamento desses produtos.

            Inicialmente foi observado a correlação entre possíveis Fetures e o total vendido por um produto.
            Esssas Features foram, product_category, product_niche, product_creation_data, e se o produto pode ser obtido múltiplas vezes ou não.
        """),
    dcc.Markdown("""
    ### Uso do modelo

    Abaixo temos um Proxy de uso do modelo para identificar em qual quantil ficaria o produto.
    """),
    dbc.Row(
        [dbc.Col(c1.input_top_label(id='producer-id', label='Producer Id', value = 30), width=2),
         dbc.Col(c1.input_top_label(id='repurchase', label='Repurchase', value = 'True', type="text"), width=2),
         dbc.Col(c1.input_top_label(id='product-category', label='Product Category', value = "Podcast", type="text"), width=2),
         dbc.Col(c1.input_top_label(id='product-niche', label='Product Niche', value = "Child psychology", type="text"), width=2),
         dbc.Col(c1.input_top_label(id='product-creation-data', label='Product Creation Data', value = '2011-03-19', type="text"), width=2)]
        ),
        html.Div(id='previsao-modelo')
        ]
        )]
        )

  #['producer_id', 'repurchase', 'product_category', 'product_niche', 'product_creation_date']