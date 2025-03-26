import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import gradio as gr
from math import radians, sin, cos, sqrt, atan2
import googlemaps
import locale
from .shared_state import state  # Importa o estado compartilhado

# Inicializando o cliente Google Maps com a chave da API
gmaps = googlemaps.Client(key='AIzaSyDoJ6C7NE2CHqFcaHTnhreOfgJeTk4uSH0')

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    # Fallback para uma localidade padrão (ex.: 'C' ou 'en_US.UTF-8')
    locale.setlocale(locale.LC_ALL, 'C')

# Load the data
data_path = 'dados/data_2.xlsx'
df = pd.read_excel(data_path, sheet_name='Planilha1')
# Garantir que a coluna "Data" seja do tipo datetime
df['Data'] = pd.to_datetime(df['Data'], errors='coerce')

# Função para calcular a distância haversine
def haversine(lat1, lon1, lat2, lon2):
    raio_terra = 6371000  # Raio da Terra em metros
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return raio_terra * c

# Função unificada para gerar mapa, estatísticas, DataFrame filtrado e arquivo de download
def unified_action(selected_types, selected_bairros, selected_fonte, min_atotal, max_atotal, min_apriv, max_apriv, min_ater, max_ater, min_date, max_date, address=None, radius=None):
    filtered_df = df.copy()

    # Filtrando os dados com base nos tipos
    if "Todos" not in selected_types:
        filtered_df = filtered_df[filtered_df['Tipo'].isin(selected_types)]

    # Filtrando os dados com base nos bairros
    if "Todos" not in selected_bairros:
        filtered_df = filtered_df[filtered_df['Bairro'].isin(selected_bairros)]

    # Filtrando os dados com base na fonte
    if "Todos" not in selected_fonte:
        filtered_df = filtered_df[filtered_df['Fonte'].isin(selected_fonte)]

    # Filtrando por área total
    if min_atotal is not None:
        filtered_df = filtered_df[filtered_df['Atotal'] >= min_atotal]
    if max_atotal is not None:
        filtered_df = filtered_df[filtered_df['Atotal'] <= max_atotal]

    # Filtrando por área privativa
    if min_apriv is not None:
        filtered_df = filtered_df[filtered_df['Apriv'] >= min_apriv]
    if max_apriv is not None:
        filtered_df = filtered_df[filtered_df['Apriv'] <= max_apriv]

    # Filtrando por área de terreno
    if min_ater is not None:
        filtered_df = filtered_df[filtered_df['Ater'] >= min_ater]
    if max_ater is not None:
        filtered_df = filtered_df[filtered_df['Ater'] <= max_ater]
        
    # Filtrando por data, se especificada
    if min_date is not None:
        filtered_df = filtered_df[filtered_df['Data'] >= pd.to_datetime(min_date)]
    
    if max_date is not None:
        filtered_df = filtered_df[filtered_df['Data'] <= pd.to_datetime(max_date)]

    # Filtrando por endereço e raio, se fornecidos
    if address:
        try:
            result = gmaps.geocode(address)
            if result:
                coordinates = result[0]['geometry']['location']
                center_lat = coordinates['lat']
                center_lon = coordinates['lng']
    
                if radius:  # Se o raio for especificado
                    # Calculando distâncias e filtrando
                    filtered_df['Distance'] = filtered_df.apply(
                        lambda row: haversine(center_lat, center_lon, row['Latitude'], row['Longitude']),
                        axis=1
                    )
                    filtered_df = filtered_df[filtered_df['Distance'] <= radius]
                else:  # Se nenhum raio for especificado
                    # Filtrar pelo nome da rua ou bairro
                    address_components = result[0]['address_components']
                    street = None
                    neighborhood = None
    
                    for component in address_components:
                        if 'route' in component['types']:  # Rua
                            street = component['long_name']
                        if 'sublocality' in component['types'] or 'locality' in component['types']:  # Bairro
                            neighborhood = component['long_name']
    
                    if street:
                        filtered_df = filtered_df[filtered_df['Localização'].str.contains(street, na=False)]
                    elif neighborhood:
                        filtered_df = filtered_df[filtered_df['Bairro'].str.contains(neighborhood, na=False)]
        except Exception as e:
            print(f"Erro ao filtrar pelo endereço: {e}")


    # Criando o mapa
    fig = px.scatter_mapbox(
        filtered_df,
        lat="Latitude",
        lon="Longitude",
        hover_name="Localização",
        hover_data={
            "Valor": True,
            "Vunit_priv": True,
            "Tipo": True,
            "url": True,
        },
        color="Tipo",
        size="Valor",
        size_max=30,
        zoom=10
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        autosize=True,
        height=600,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )

    # Adicionando círculo ao mapa se endereço e raio forem fornecidos
    if address and radius:
        try:
            raio_terra = 6371000
            pontos_lat = []
            pontos_lon = []
            for angulo in range(360):
                ang_rad = radians(angulo)
                d_lat = (radius / raio_terra) * cos(ang_rad)
                d_lon = (radius / (raio_terra * cos(radians(center_lat)))) * sin(ang_rad)
                pontos_lat.append(center_lat + d_lat * (180 / 3.141592653589793))
                pontos_lon.append(center_lon + d_lon * (180 / 3.141592653589793))

            fig.add_trace(go.Scattermapbox(
                lat=pontos_lat,
                lon=pontos_lon,
                mode='lines',
                fill='toself',
                fillcolor='rgba(0, 0, 255, 0.2)',
                line=dict(color='blue', width=2),
                name='Raio'
            ))

            fig.add_trace(go.Scattermapbox(
                lat=[center_lat],
                lon=[center_lon],
                mode='markers',
                marker=dict(size=10, color='red'),
                name='Centro'
            ))
        except Exception as e:
            print(f"Erro ao adicionar o círculo no mapa: {e}")

    # Gerando estatísticas
    if filtered_df.empty:
        stats_text = "Nenhum dado disponível."
    else:
        stats_text = (f"Quantidade de Dados: {len(filtered_df):n}\n"
                      f"Média do Valor: {locale.format_string('%.2f', filtered_df['Valor'].mean(), grouping=True)}\n"
                      f"Máximo do Valor: {locale.format_string('%.2f', filtered_df['Valor'].max(), grouping=True)}\n"
                      f"Mínimo do Valor: {locale.format_string('%.2f', filtered_df['Valor'].min(), grouping=True)}")

    # Salvando DataFrame filtrado em arquivo CSV
    file_path = "dados/dados_filtrados.xlsx"
    filtered_df.to_excel(file_path)

    return fig, stats_text, filtered_df, file_path

# List of unique property types, bairros, and fonte, with "Todos" as default
property_types = ["Todos"] + sorted(df['Tipo'].dropna().unique().tolist())
bairro_list = ["Todos"] + sorted(df['Bairro'].dropna().unique().tolist())
fonte_list = ["Todos"] + sorted(df['Fonte'].dropna().unique().tolist())


def dados_tab():
    with gr.Tab("Pesquisar Dados"):
        toggle_filters = gr.Checkbox(label="Exibir Campos de Pesquisa", value=True)

        with gr.Row(visible=True) as filters:
            tipo_filter = gr.Dropdown(label="Selecione os Tipos de Imóvel", choices=property_types, value=["Todos"], multiselect=True)
            bairro_filter = gr.Dropdown(label="Selecione os Bairros", choices=bairro_list, value=["Todos"], multiselect=True)
            fonte_filter = gr.Dropdown(label="Selecione a Fonte", choices=fonte_list, value=["Todos"], multiselect=True)

        with gr.Row(visible=True) as area_filters:
            min_atotal = gr.Number(label="Área Total Mínima", value=None)
            max_atotal = gr.Number(label="Área Total Máxima", value=None)
            min_apriv = gr.Number(label="Área Privativa Mínima", value=None)
            max_apriv = gr.Number(label="Área Privativa Máxima", value=None)
            min_ater = gr.Number(label="Área Terreno Mínima", value=None)
            max_ater = gr.Number(label="Área Terreno Máxima", value=None)
            
        with gr.Row(visible=True) as date_filters:
            min_date = gr.Textbox(label="Data Inicial (AAAA-MM-DD)", value="")
            max_date = gr.Textbox(label="Data Final (AAAA-MM-DD)", value="")

        with gr.Row(visible=True) as address_filters:
            address_input = gr.Textbox(label="Endereço (Opcional)")
            radius_input = gr.Number(label="Raio em metros (Opcional)")

        with gr.Row():
            search_button = gr.Button("Pesquisar")
            clear_button = gr.Button("Limpar")

        map_output = gr.Plot()
        stats_output = gr.Textbox(lines=4, label="Estatísticas")
        filtered_df_output = gr.DataFrame(label="Dados Filtrados")
        download_output = gr.File(label="Baixar Dados Filtrados")

        def clear_action():
            return (["Todos"], ["Todos"], ["Todos"], None, None, None, None, None, None, "", "", "", None, None, "", pd.DataFrame(), None)

        toggle_filters.change(
            lambda show: (
                gr.update(visible=show), 
                gr.update(visible=show), 
                gr.update(visible=show),
                gr.update(visible=show)  # Adiciona o filtro de data na visibilidade
            ), 
            inputs=[toggle_filters], 
            outputs=[filters, area_filters, address_filters, date_filters]
        )


        search_button.click(
            unified_action,
            inputs=[tipo_filter, bairro_filter, fonte_filter, min_atotal, max_atotal, min_apriv, max_apriv, 
                    min_ater, max_ater, min_date, max_date, address_input, radius_input],
            outputs=[map_output, stats_output, filtered_df_output, download_output]
        )

        clear_button.click(
            clear_action, 
            outputs=[tipo_filter, bairro_filter, fonte_filter, min_atotal, max_atotal, min_apriv, max_apriv, 
                     min_ater, max_ater, min_date, max_date, address_input, radius_input, 
                     map_output, stats_output, filtered_df_output, download_output]
        )

    return locals(), filtered_df_output


### implementar o KNN
### Arrumar a questão de que somente clicando no botão "Limpar" é possível acionar os filtros
### Filtro por data
### Zoon oelo filtro de raio
### Gráfico de linhas
