import pandas as pd
import sys
import os
sys.path.append(os.getcwd())
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from app import app
from dash import html, dcc
from sklearn.preprocessing import MinMaxScaler
from src.models.predict_model import single_prediction
import plotly.express as px
def transform_z_values(values, mean, std):
    return values*std + mean


df = pd.read_csv(r'data\sales_data.csv', index_col = 0)
scaler = MinMaxScaler(feature_range=(10**-4, 1))
df['purchase_value_min_max'] = scaler.fit_transform(df[['purchase_value']])
y = df.groupby('product_id').agg(value_product = ('purchase_value_min_max', 'sum'))
y['target_q'] = pd.qcut(y['value_product'], q=4, labels=['Quartil 1', 'Quartil 2', 'Quartil 3', 'Quartil 4'])
df = df.merge(y.reset_index()[['product_id', 'target_q']], on=['product_id'], how='left')


def create_indicator(value, title):
    color = '#e6e1df'
    indicator = go.Figure(go.Indicator(
        mode="number",
        value=value,
        title={
            'text': title,
            'font': {'color': color}
        },
        number={
            'font': {'color': color}
        }
    ))
    indicator.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",  # Set the plot background color to transparent
        paper_bgcolor="rgba(0,0,0,0)"  # Set the paper (plot area) background color to transparent
        )
    return indicator

def plot_cumulative_revenue(df, purchase, threshold):
    # Your data processing code
    product_revenue = df.groupby(['product_id']).agg(revenue_product=(purchase, 'sum')).sort_values(by='revenue_product')
    product_revenue['cumulative_revenue'] = product_revenue['revenue_product'].cumsum()
    product_revenue['percentile'] = pd.qcut(product_revenue['revenue_product'], q=101, labels=False, duplicates='drop')
    df_percentile = product_revenue.groupby('percentile')['cumulative_revenue'].max().reset_index()
    df_percentile['percentage_revenue'] = df_percentile['cumulative_revenue'] / product_revenue['cumulative_revenue'].max()
    if purchase!='purchase_value':
        df_percentile['percentage_revenue'] = df_percentile['percentage_revenue']*100
    # Create the plot
    fig = go.Figure()
    blue_line = df_percentile[df_percentile['percentile'] <= threshold]
    fig.add_trace(go.Scatter(
        x=blue_line['percentile'],
        y=blue_line['percentage_revenue'],
        mode='lines',
        line=dict(color='lightgray', width=4),
        name='Outros produtos'
    ))
    hotmart_line = df_percentile[df_percentile['percentile'] >= threshold]
    fig.add_trace(go.Scatter(
        x=hotmart_line['percentile'],
        y=hotmart_line['percentage_revenue'],
        mode='lines',
        line=dict(color='#ff4e1a', width=4),
        name='Maiores produtos'
    ))

    fig.update_layout(
        xaxis_title='Percentil produtos por faturamento',
        yaxis_title='Percentual faturamento total',
        plot_bgcolor='rgba(0,0,0,0)',  # Remove background color
        font=dict(size=18),  # Increase font size
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False,)
    return fig

def plot_revenue_bar(df, percentile_threshold, purchase):
    # Calculate the cumulative revenue and percentile
    product_revenue = df.groupby('product_id')[purchase].sum().sort_values()
    product_revenue = product_revenue.reset_index()
    product_revenue['percentile'] = pd.qcut(product_revenue[purchase], q=100, labels=False, duplicates='drop')
    
    # Determine high-sellers and low-sellers based on percentile threshold
    high_sellers = product_revenue[product_revenue['percentile'] >= percentile_threshold]
    low_sellers = product_revenue[product_revenue['percentile'] < percentile_threshold]
    
    # Calculate percentage contribution of each group
    total_revenue = product_revenue[purchase].sum()
    high_sellers_percentage = (high_sellers[purchase].sum() / total_revenue)*100
    low_sellers_percentage = (low_sellers[purchase].sum() / total_revenue)*100
    bar_width = 0.6
    # Create the bar plots for high-sellers and low-sellers
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=['Maiores Produtos'],
        y=[high_sellers_percentage],
        name='Maiores Produtos',
        marker=dict(color='#ff4e1a'),
        width=bar_width,  # Reduce bar width
        text=[f'{high_sellers_percentage:.2f}%'],  # Add percentage value to text
        textposition='inside',  # Position the text inside the bar
    ))
    fig.add_trace(go.Bar(
        x=['Outros Produtos'],
        y=[low_sellers_percentage],
        name='Outros Produtos',
        marker=dict(color='lightgray'),
        width=bar_width,  # Reduce bar width
        text=[f'{low_sellers_percentage:.2f}%'],  # Add percentage value to text
        textposition='inside',  # Position the text inside the bar
    ))
    
    # Set the layout
    fig.update_layout(
        showlegend=False,  # Remove legend
        plot_bgcolor='rgba(0,0,0,0)',  # Remove background color
        yaxis_title='Percentual faturamento total',
        font=dict(size=18),
        xaxis=dict(
            showgrid=False,  # Remove x-axis gridlines
            tickfont=dict(size=18),  # Increase x-axis tick font size
        ),
        yaxis=dict(
            range=[0, 100], # Set y-axis range from 0 to 1
            showgrid=False,  # Remove y-axis gridlines
            tickfont=dict(size=18),  # Increase y-axis tick font size
           
        ),
    )
    
    # Show the figure
    return fig
    
def get_transformed_z_indicators(scale='Z-score',mean=30, std=50, high_sellers_threshold=90):
    indicators = []

    value = 'purchase_value'
    if scale == 'X-Value':
        if mean is None:
            mean = 30
        if std is None:
            std = 50
        df['purchase_value_x'] = df['purchase_value'].apply(transform_z_values, mean=mean, std=std)
        value = 'purchase_value_x'
    elif scale == 'MinMaxScaler':
        value = 'purchase_value_min_max'

    line_cumulative = plot_cumulative_revenue(df, value, high_sellers_threshold)
    #if value == 'purchase_value':
    #    scaler = MinMaxScaler(feature_range=(10**-3, 1))
    #    df['purchase_value_min_max'] = scaler.fit_transform(df[['purchase_value']])
    #    bar_cumulative = plot_revenue_bar(df, high_sellers_threshold, purchase='purchase_value_min_max')
    #else:
    bar_cumulative = plot_revenue_bar(df, high_sellers_threshold, purchase=value)

    cheapest_product = df[value].min()
    most_expensive_product = df[value].max()
    total_revenue = df[value].sum()

    # Indicador 0
    indicators.append(create_indicator(cheapest_product, 'Produto mais barato'))
    # Indicador 1
    indicators.append(create_indicator(most_expensive_product, 'Produto mais caro'))
    # Indicador 2
    indicators.append(create_indicator(total_revenue, 'Faturamento da Hotmart'))
    # Line Plot
    indicators.append(line_cumulative)
    # Box plot
    indicators.append(bar_cumulative)
    return indicators

@app.callback(
    Output('indicador-produto-barato', 'figure'),
    Output('indicador-produto-caro', 'figure'),
    Output('indicador-faturamento', 'figure'),
    Output('line-cumulative-revenue', 'figure'),
    Output('bar-cumulative-revenue', 'figure'),
    [Input('radio-item-value', 'value'),
     Input('valor-mean-transform-z', 'value'),
     Input('valor-std-transform-z', 'value'),
     Input('threshold-slider', 'value')])
def update_z_indicators(scale, mean, std, high_sellers_threshold):
    indicators = get_transformed_z_indicators(scale=scale, mean=mean, std=std, high_sellers_threshold=high_sellers_threshold)
    # Perform data filtering and plot updates based on the selected dates
        
    return  indicators[0] if len(indicators) > 0 else {}, \
            indicators[1] if len(indicators) > 1 else {}, \
            indicators[2] if len(indicators) > 2 else {}, \
            indicators[3] if len(indicators) > 3 else {}, \
            indicators[4] if len(indicators) > 4 else {}

def plot_box_faturamento():
    # Create the box plot
    fig = px.box(y.round(3), x='value_product', color='target_q', labels={'target_q': 'Quartil Faturamento'})
    # Set the x-axis type to 'log'
    fig.update_xaxes(type='log',
                     showgrid=False)
    fig.update_layout(
        xaxis_title='Faturamento de Produtos',
        plot_bgcolor='rgba(0,0,0,0)',  # Remove background color
        font=dict(size=18),  # Increase font size
    )
    fig.update_yaxes(showgrid=False,)
    # Show the figure
    return fig

def plot_quntile_proportion():
    # Create the box plot
    fig = px.bar(df, x='product_category', y='target_q' labels={'target_q': 'Quartil Faturamento'})
    # Set the x-axis type to 'log'
    fig.update_xaxes(showgrid=False)
    fig.update_layout(
        xaxis_title='Faturamento de Produtos',
        plot_bgcolor='rgba(0,0,0,0)',  # Remove background color
        font=dict(size=18),  # Increase font size
    )
    fig.update_yaxes(showgrid=False,)
    # Show the figure
    return fig


def feature_exploration():
    inputs = []
    inputs.append(plot_box_faturamento())
    return inputs
@app.callback(    
    Output('box-faturamento', 'figure'),
    [Input('column-analise', 'value')]
    )
def update_feature_exploration(column=None):
    inputs = feature_exploration()
    return  inputs[0] if len(inputs) > 0 else {}
    


@app.callback(
    Output('previsao-modelo', 'children'),
    [Input('producer-id', 'value'),
    Input('repurchase', 'value'),
    Input('product-category', 'value'), 
    Input('product-niche', 'value'),
    Input('product-creation-data', 'value')])
def prediction(producer_id, repurchase, product_category, product_niche, product_creation_date):
    prediction = single_prediction(product_id=-1, producer_id=producer_id, repurchase=bool(repurchase), 
                                    product_category=product_category, product_niche=product_niche, 
                                    product_creation_date=product_creation_date)
    return f"Valor esperado do produto: MinMaxScale {prediction}"
