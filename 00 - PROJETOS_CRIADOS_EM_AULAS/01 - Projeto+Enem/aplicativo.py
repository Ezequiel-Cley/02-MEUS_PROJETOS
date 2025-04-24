import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, ClientsideFunction, State

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import json
from urllib.request import urlopen


# Lendo os dados
Base_Dados = pd.read_csv(r'C:\Users\ezequ\Scripts\01 - APRENDIZADOS\02 - PROJETOS_CRIADOS_EM_AULAS\01 - Projeto+Enem\assets\Dados_tratados_Enem.csv')

### ### ### ###
  ### Mapa ###
### ### ### ###

# Importando os códigos das cidades
with urlopen('https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-35-mun.json') as response:
    geo_json_sp = json.load( response )

# Gráfico
Figura = px.choropleth_mapbox(
  Base_Dados,
  geojson = geo_json_sp,
  locations='codigo_ibge',
  featureidkey = 'properties.id',
  color = 'Media_Nota_Geral',
  hover_data = ['NO_MUNICIPIO_PROVA'],
  color_continuous_scale='Viridis',
  mapbox_style = 'carto-positron',
  center = {'lat':-23.663889, 'lon': -46.537778},
  zoom = 6,
  opacity = 0.65, 
)
# Ajuste do Geo
Figura.update_geos(
    fitbounds='locations', 
    visible=False,
)
# Ajuste Layout
Figura.update_layout(
    autosize=True,
    margin=go.layout.Margin(l=0, r=0, t=0, b=0),
    showlegend=False,
    coloraxis_showscale=False
)


# Criando o aplicativo
Aplicativo = dash.Dash( __name__, external_stylesheets=[ 

    # Estilo
    dbc.themes.JOURNAL, 

    # APIs
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css',
    'https://fonts.googleapis.com/css2?family=Joan&family=Roboto:ital,wght@0,100;1,300&family=Source+Sans+Pro:ital,wght@0,400;1,300&display=swap'
    ], 
    title='Data Viking' 
)


# Rodando o aplicativo no Heroku    
server = Aplicativo.server

# https://dash.plotly.com/deployment

# Criando o Site
Aplicativo.layout = dbc.Container(

    # Pagina
    children=[

        dbc.Row([
            dbc.Navbar(
                dbc.Container(
                    [
                        html.A(
                            
                            dbc.Row(
                                [
                                    dbc.Col(html.Img(src=Aplicativo.get_asset_url('Logo_MBGDados_2.png'), height="30px")),
                                    dbc.Col(dbc.NavbarBrand('Bootcamp Business Intelligence', className="ms-1")),
                                ],
                                align="center", className="g-0",
                            ),
                            href="#",
                            style={"textDecoration": "none"},
                        ),
                    ]
                ),
            ),
        ]),

        # Linha Superior
        dbc.Row([
            
            # Contair
            dbc.Col([

                html.Div([

                    # Titulo
                    html.H5( children=' ' ),
                    # Buttom
                    dbc.Button('Analytics - ENEM 2021', color='danger', id='location-button', size='lg')

                    ], style={'margin-top': '15px' } 
                ),
            
                # Filtro
                html.P( 'Selecione o estado:', style={'margin-top':'10px'} ),

                # Caixa de Seleção
                html.Div(
                    
                    # Caixa de Seleção
                    dcc.Dropdown(
                        id='Estado_Selecao',
                        placeholder='SÃO PAULO',
                        options=[
                            {'label': 'SÃO PAULO', 'value':1 }
                        ],
                        value='',
                        style={'margin-top':'10px'}
                    )
                ),

                # Filtro
                html.P( 'Selecione a cidade:', style={'margin-top':'10px'} ),

                # Caixa de Seleção
                html.Div(
                    
                    # Caixa de Seleção
                    dcc.Dropdown(
                        id='Cidade_Selecao',
                        placeholder='Cidade...',
                        options=[
                            {'label': Loop, 'value': Loop } for Loop in Base_Dados['NO_MUNICIPIO_PROVA']
                        ],
                        value='ANDRADINA',
                        style={'margin-top':'10px'}
                    )
                ),

                # Botaão
                html.Div([

                    #Botao
                    html.Button(
                        id='Processar', 
                        children='Processar',
                        className='btn btn-outline-danger', 
                        n_clicks=0)
                ], style={'margin-top':'15px'} ),

                # -- Conteudo
                dbc.Row([

                    #Coluna 1
                    dbc.Col([

                        #Card
                        dbc.Card([

                            # Info CArd
                            dbc.CardBody([
                                html.Span('Inscritos para a prova', className='card-text'),
                                html.H3('000.000',style={'color':'orange'}, id='Quantidade_Inscritos' ),
                                html.Span('% Estado', className='card-text'),
                                html.H6('0', id='Quantidade_Inscritos_Representacao')
                            ]),
                        ], color='light', outline=True, style={'margin-top':'10px', 'box-shadoow':'0 2px 4px 0 rgba(0,0,0,015), 0 4px 10px 0 rgba(0, 0, 0, 0.19)', 'color':'black' }),
                    ], md=4 ),

                    #Coluna 2
                    dbc.Col([

                        #Card
                        dbc.Card([

                            # Info CArd
                            dbc.CardBody([
                                html.Span('% Realizado a prova', className='card-text'),
                                html.H3('00.00',style={'color':'orange'}, id='Realizado_Prova' ),
                                html.Span('% Estado', className='card-text'),
                                html.H6('0', id='Realizado_Prova_Representacao')
                            ]),
                        ], color='light', outline=True, style={'margin-top':'10px', 'box-shadoow':'0 2px 4px 0 rgba(0,0,0,015), 0 4px 10px 0 rgba(0, 0, 0, 0.19)', 'color':'black' }),
                    ], md=4 ),

                    #Coluna 3
                    dbc.Col([

                        #Card
                        dbc.Card([

                            # Info CArd
                            dbc.CardBody([
                                html.Span('Média de todas notas', className='card-text'),
                                html.H3('00.00',style={'color':'orange'}, id='Media_Prova' ),
                                html.Span('Media Estado', className='card-text'),
                                html.H6('0', id='Media_Prova_Representacao')
                            ]),
                        ], color='light', outline=True, style={'margin-top':'10px', 'box-shadoow':'0 2px 4px 0 rgba(0,0,0,015), 0 4px 10px 0 rgba(0, 0, 0, 0.19)', 'color':'black' }),
                    ], md=4 ),

                    # Gráfico
                    html.Div([

                        # Gráfico
                        dcc.Graph(
                            id='linegraph',
                            style={'background-color':'#f5f5f5', 'margin-top':'10px'}
                        )
                    ]),
                ]),
            ], md=6),

            # Coluna 2
            dbc.Col([

                # Gráfico
                dcc.Loading(
                    id='loading-1',
                    type='default',
                    children=[
                        dcc.Graph(
                            id='Grafico_Mapa',
                            figure=Figura,
                            style={'height':'133vh', 'margin-rigth':'0px'}
                        )
                    ]
                ),
            ]),
        ]),
    
        dbc.Row([
            html.Footer([
                html.Span(['Desenvolvido por by:Data Viking'])
            ])
        ]),
    ]
)

# Funcão para todar o modelo
@Aplicativo.callback( 
    Output('Quantidade_Inscritos', 'children'),
    Output('Quantidade_Inscritos_Representacao', 'children'),
    Output('Realizado_Prova', 'children'),
    Output('Realizado_Prova_Representacao', 'children'),
    Output('Media_Prova', 'children'),
    Output('Media_Prova_Representacao', 'children'),
    [Input('Processar', 'n_clicks')],
    [State('Cidade_Selecao', 'value')] )
def Atualizar_Painel(n_clicks, Cidade_Selecao):

    # Lista
    Retorno = []

    # Query
    Analise = Base_Dados.loc[ Base_Dados['NO_MUNICIPIO_PROVA'] == Cidade_Selecao ]

    # Dados para o painel
    Qtd_Inscritos = Analise['Inscritos']
    Qtd_Inscritos_Rep = Analise['Inscritos_Representacao']
    Rel_Prova = round( Analise['%_Média_Presença'], 2)
    Rel_Prova_Rep = round( Base_Dados['%_Média_Presença'].mean(), 1)
    Med_Prova = round( Analise['Media_Nota_Geral'], 2)
    Med_Prova_Rep = round( Base_Dados['Media_Nota_Geral'].mean(), 2)

    return (
        Qtd_Inscritos,
        Qtd_Inscritos_Rep,
        Rel_Prova,
        Rel_Prova_Rep,
        Med_Prova,
        Med_Prova_Rep,
    )
    
# Funcão para todar o modelo
@Aplicativo.callback( 
    Output('linegraph', 'figure'), 
    [Input('Processar', 'n_clicks')],
    [State('Cidade_Selecao', 'value')] )
def Gerar_Gráfico(n_clicks, Cidade_Selecao):

    # Lista
    #Retorno = []

    # Query
    Analise = Base_Dados.loc[ Base_Dados['NO_MUNICIPIO_PROVA'] == Cidade_Selecao ]

    # Plot do Gráfico
    Analise = Analise[['NU_NOTA_CN', 'NU_NOTA_MT', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_REDACAO']]
    Analise.columns = ['CN', 'MT', 'CH', 'LC', 'REDAÇÃO']
    Analise = Analise.transpose().reset_index()
    Analise.columns=['Nota', 'Valor']
    Retorno = px.bar( Analise, x='Nota', y='Valor', color='Nota', title='Média das notas' )
    Retorno.update_layout( {'plot_bgcolor': '#ffffff', 'paper_bgcolor': '#ffffff' })
    Retorno.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(
            family="Courier",
            size=12,
            color="black"
        ),

    ))



    # Retorno
    return (
        Retorno
    )

if __name__ == '__main__':
    Aplicativo.run_server( debug=True )