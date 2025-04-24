import pandas as pd
# Modulos do Plotly
import plotly.express as px

url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ14LQ4pSpjviMuQYs10wdo_i9M0SEL53MTLjEamFtc-SP82URGNHUbExhlmQCTHhCMwSTmsQGhsOKK/pubhtml'
df = pd.read_html(url, header =0, index_col=0, skiprows=1)[0].reset_index()

df = df.iloc[:, :15]

df = df.dropna(subset=['CLIENTE'])

DASH01 = df.groupby(by=['OPERADOR']).agg(    VENDAS = ('CLIENTE','count')).sort_values(by='VENDAS', ascending=True).reset_index()

def MAISCULA(d):
    if isinstance(d, str):
        return d.upper()
    else:
        return d

df['UF'] = df['UF'].apply(MAISCULA)

DASH02 = df.groupby(by=['UF']).agg(  VENDAS = ('CLIENTE','count')).reset_index()

DASH02['%VENDAS'] = DASH02['VENDAS']/DASH02['VENDAS'].sum() * 100

df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y')
df['DIA'] =  df['DATA'].dt.day

DASH03 = df.groupby(by=['DIA']).agg( VENDAS = ('CLIENTE','count')).reset_index()

# Gráfico de Linhas
Figura_Linhas = px.line(
    DASH03, x='DIA', y='VENDAS', title='Vendas Por Dia', text='VENDAS',
    markers=True, height=500,  width=1000, labels={'DIA': 'DIAS', 'VENDAS': 'Vendas'})

# Definindo o formato dos valores ao pairar o mouse sobre os pontos do gráfico
Figura_Linhas.update_traces(
    textposition='top center',
    fill='tozeroy',
    fillcolor='rgba(198, 213, 245, 0.5)',
    textfont=dict(size=13, color='blue', family='Arial')
)

# Ajustando a cor de fundo do gráfico
Figura_Linhas.update_layout(
    plot_bgcolor='#f2f5fa',
    #xaxis_range=[6.8, 12.2],
    yaxis_range=[0, DASH03.VENDAS.max() + ( DASH03.VENDAS.max() * 0.25 ) ],
    xaxis_showgrid=False,
)
Figura_Linhas.show()

TOTAL = DASH02['VENDAS'].sum()
Figura_Pizza = px.pie(
    DASH02,
    names='UF', values='VENDAS',
    title='% Vendas Por Estado',
    hole=0.6,
    #color_discrete_sequence=px.colors.sequential.Cividis
)

Figura_Pizza.update_traces(
    hoverinfo='label+percent', textinfo='percent+label', textfont_size=12,
    textposition='inside',
    marker=dict( line=dict(color='#ffffff', width=2) ) )

Figura_Pizza.add_annotation(
    x=0.5, y=0.5,
    showarrow=False,
    text=f'{ round(TOTAL)}',
    font=dict(
      #family='Courier New, monospace',
      size=30,
      color='#000000'
    ),
)

Figura_Pizza.update( layout_showlegend=True )

Figura_Pizza

# Gráfico de Barras
Figura_Barras = px.bar( DASH01, x='VENDAS', y='OPERADOR', title='Total de Barras', text='VENDAS')

# Definindo o formato dos valores ao pairar o mouse sobre os pontos do gráfico
Figura_Barras.update_traces(
    textfont=dict(size=16, color='white', family='Arial')
)

# Ajustando a cor de fundo do gráfico
Figura_Barras.update_layout(
    plot_bgcolor='#f2f5fa',
    xaxis_showgrid=False
)

Figura_Barras.show()
