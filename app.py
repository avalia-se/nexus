import streamlit as st
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from geopy.distance import geodesic
import googlemaps
from geopy.exc import GeocoderTimedOut
from streamlit_folium import st_folium
import folium
from branca.colormap import LinearColormap
import base64
from io import BytesIO
import sys
import pydeck as pdk
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components

# Print the Python version
print("Python version")
print(sys.version)
print("Version info.")
print(sys.version_info)

image1 = 'avalia-removebg-preview.png'

# Function to add heatmap layer to folium map
def add_heatmap_layer(map_obj, data, column_name, colormap_name, radius=15):
    heat_data = data[['latitude', 'longitude', column_name]].dropna()
    heat_layer = folium.FeatureGroup(name=f'Variável - {column_name}')

    cmap = LinearColormap(colors=['blue', 'white', 'red'], vmin=heat_data[column_name].min(), vmax=heat_data[column_name].max())

    for index, row in heat_data.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=radius,
            fill=True,
            fill_color=cmap(row[column_name]),
            fill_opacity=0.5,
            weight=0,
            popup=f"{column_name}: {row[column_name]:.2f}"  # Fix here
        ).add_to(heat_layer)

    heat_layer.add_to(map_obj)
    
# Function to calculate distance in meters between two coordinates
def calculate_distance(lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return geodesic(coords_1, coords_2).meters

def knn_predict(df, target_column, features_columns, k=5):
    # Separate features and target variable
    X = df[features_columns]
    y = df[target_column]

    # Check if there is enough data for prediction
    if len(X) < k:
        return np.zeros(len(X))  # Return an array of zeros if there isn't enough data

    # Create KNN regressor
    knn = KNeighborsRegressor(n_neighbors=k)

    # Fit the model
    knn.fit(X, y)

    # Use the model to predict target_column for the filtered_data
    predictions = knn.predict(df[features_columns])

    return predictions

# Set wide mode
st.set_page_config(layout="wide")

# Create a DataFrame with sample data
data = pd.read_excel('data_nexus.xlsx')

# Initialize variables to avoid NameError
radius_visible = True
custom_address_initial = 'Centro, Lajeado - RS, Brazil'  # Initial custom address
#custom_lat = data['latitude'].median()
custom_lat = -29.45880114339262
#custom_lon = data['longitude'].median()
custom_lon = -51.97011580843118
radius_in_meters = 150000
filtered_data = data  # Initialize with the entire dataset

# Calculate a zoom level based on the maximum distance
zoom_level = 13

font_url = "https://fonts.googleapis.com/css2?family=Quicksand:wght@300..700&display=swap"

title_html = f"""
<style>
    @import url('{font_url}');
    h1 {{
        font-family: 'Quicksand', sans-serif;
    }}
</style>
<span style='color: #566f71; font-size: 50px;'>aval</span>
<span style='color: #edb600; font-size: 50px;'>ia</span>
<span style='color: #566f71; font-size: 50px;'>.se</span>
"""

# Create a sidebar for controls
with st.sidebar:
    st.image(image1, width=200)
    #st.markdown(title_html, unsafe_allow_html=True)

    # Add a dropdown for filtering "Fonte"
    selected_fonte = st.selectbox('Finalidade', data['Fonte'].unique(), index=data['Fonte'].unique().tolist().index('Venda'))
    data = data[data['Fonte'] == selected_fonte]

    # Add a dropdown for filtering "Tipo"
    selected_tipo = st.selectbox('Tipo de imóvel', data['Tipo'].unique(), index=data['Tipo'].unique().tolist().index('Apartamento'))
    data_tipo = data[data['Tipo'] == selected_tipo]
    
    custom_address = st.text_input('Informe o endereço', custom_address_initial)
    radius_visible = True  # Show radius slider for custom coordinates

    gmaps = googlemaps.Client(key='AIzaSyDoJ6C7NE2CHqFcaHTnhreOfgJeTk4uSH0')  # Replace with your API key

    try:
        # Ensure custom_address ends with " - RS, Brazil"
        custom_address = custom_address.strip()  # Remove leading/trailing whitespaces
        if not custom_address.endswith(" - RS, Brazil"):
            custom_address += " - RS, Brazil"

        location = gmaps.geocode(custom_address)[0]['geometry']['location']
        custom_lat, custom_lon = location['lat'], location['lng']
    except (IndexError, GeocoderTimedOut):
        st.error("Erro: Não foi possível geocodificar o endereço fornecido. Por favor, verifique e tente novamente.")

    # Conditionally render the radius slider
    if radius_visible:
        radius_in_meters = st.number_input('Selecione raio (em metros)', min_value=0, max_value=100000, value=2000)

    # Add sliders to filter data based
    #atotal_range = st.slider('Área Total', float(data_tipo['Atotal'].min()), float(data_tipo['Atotal'].max()), (float(data_tipo['Atotal'].min()), float(data_tipo['Atotal'].max())), step=.1 if data_tipo['Atotal'].min() != data_tipo['Atotal'].max() else 0.1)
    #apriv_range = st.slider('Área Privativa', float(data_tipo['Apriv'].min()), float(data_tipo['Apriv'].max()), (float(data_tipo['Apriv'].min()), float(data_tipo['Apriv'].max())), step=.1 if data_tipo['Apriv'].min() != data_tipo['Apriv'].max() else 0.1)

    # Create two columns for Área Total inputs
    col1, col2 = st.columns(2)
    with col1:
        atotal_min = st.number_input('Área Total mínima', 
                                     min_value=float(data_tipo['Atotal'].min()), 
                                     max_value=float(data_tipo['Atotal'].max()), 
                                     value=float(data_tipo['Atotal'].min()),
                                     step=0.1)
    with col2:
        atotal_max = st.number_input('Área Total máxima', 
                                     min_value=float(data_tipo['Atotal'].min()), 
                                     max_value=float(data_tipo['Atotal'].max()), 
                                     value=float(data_tipo['Atotal'].max()),
                                     step=0.1)

    # Create two columns for Área Privativa inputs
    col3, col4 = st.columns(2)
    with col3:
        apriv_min = st.number_input('Área Privativa mínima', 
                                    min_value=float(data_tipo['Apriv'].min()), 
                                    max_value=float(data_tipo['Apriv'].max()), 
                                    value=float(data_tipo['Apriv'].min()),
                                    step=0.1)
    with col4:
        apriv_max = st.number_input('Área Privativa máxima', 
                                    min_value=float(data_tipo['Apriv'].min()), 
                                    max_value=float(data_tipo['Apriv'].max()), 
                                    value=float(data_tipo['Apriv'].max()),
                                    step=0.1)

    
    #data_tipo = data_tipo[(data_tipo['Atotal'].between(atotal_range[0], atotal_range[1])) &
            #(data_tipo['Apriv'].between(apriv_range[0], apriv_range[1]))]
        
    data_tipo = data_tipo[(data_tipo['Atotal'].between(atotal_min, atotal_max)) &
            (data_tipo['Apriv'].between(apriv_min, apriv_max))]
    
# Links to other apps at the bottom of the sidebar
#st.sidebar.markdown(factor_html, unsafe_allow_html=True)
#st.sidebar.markdown(evo_html, unsafe_allow_html=True)

filtered_data = data_tipo[data_tipo.apply(lambda x: calculate_distance(x['latitude'], x['longitude'], custom_lat, custom_lon), axis=1) <= radius_in_meters]
filtered_data = filtered_data.dropna()  # Drop rows with NaN values

# Add a custom CSS class to the map container
st.markdown(f"""<style>
.map {{
  width: 100%;
  height: 100vh;
}}
</style>""", unsafe_allow_html=True)

# Determine which area feature to use for prediction
filtered_data['area_feature'] = np.where(filtered_data['Apriv'] != 0, filtered_data['Apriv'], filtered_data['Atotal'])

# Define the target column based on conditions
filtered_data['target_column'] = np.where(filtered_data['Vunit_priv'] != 0, filtered_data['Vunit_priv'], filtered_data['Vunit_total'])

# Apply KNN and get predicted target values
predicted_target = knn_predict(filtered_data, 'target_column', ['latitude', 'longitude', 'area_feature'])  # Update with your features

# Add predicted target values to filtered_data
filtered_data['Predicted_target'] = predicted_target


# Set custom width for columns
tab1, tab2, tab3= st.tabs(["Mapa", "Planilha", "Análise dos Dados"])

with tab1:
    # Define a PyDeck view state for the initial map view
    view_state = pdk.ViewState(latitude=filtered_data['latitude'].mean(), longitude=filtered_data['longitude'].mean(), zoom=zoom_level)

    # Define a PyDeck layer for plotting
    layer = pdk.Layer(
        "ScatterplotLayer",
        filtered_data,
        get_position=["longitude", "latitude"],
        get_color="[237, 181, 0, 160]",  # RGBA color for light orange, adjust opacity with the last number
        get_radius=100,  # Adjust dot size as needed
    )

    # Create a PyDeck map using the defined layer and view state
    deck_map = pdk.Deck(layers=[layer], initial_view_state=view_state, map_style="mapbox://styles/mapbox/light-v9")

    # Display the map in Streamlit
    st.pydeck_chart(deck_map)
    #st.map(filtered_data, zoom=zoom_level, use_container_width=True)

with tab2:
    st.write("Dados:", filtered_data)  # Debug: Print filtered_data

    if st.button('Baixar planilha'):
        st.write("Preparando...")
        # Set up the file to be downloaded
        output_df = filtered_data

        # Create a BytesIO buffer to hold the Excel file
        excel_buffer = BytesIO()

        # Convert DataFrame to Excel and save to the buffer
        with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
            output_df.to_excel(writer, index=False, sheet_name="Sheet1")

        # Reset the buffer position to the beginning
        excel_buffer.seek(0)

        # Create a download link
        b64 = base64.b64encode(excel_buffer.read()).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="sample_data.xlsx">Clique aqui para baixar a planilha</a>'
        #st.markdown(href, unsafe_allow_html=True)

        # Use st.empty() to create a placeholder and update it with the link
        download_placeholder = st.empty()
        download_placeholder.markdown(href, unsafe_allow_html=True)

with tab3:
    k_threshold = 5

    # Function to perform bootstrap on the predicted target values
    def bootstrap_stats(bound_data, num_samples=1000):
        # Reshape the predicted_target array
        bound_data = np.array(bound_data).reshape(-1, 1)

        # Bootstrap resampling
        bootstrapped_means = []
        for _ in range(num_samples):
            bootstrap_sample = np.random.choice(bound_data.flatten(), len(bound_data), replace=True)
            bootstrapped_means.append(np.mean(bootstrap_sample))

        # Calculate lower and higher bounds
        lower_bound = np.percentile(bootstrapped_means, 16.)
        higher_bound = np.percentile(bootstrapped_means, 84.)

        return lower_bound, higher_bound

    # Apply KNN and get predicted Predicted_target values
    predicted_target = knn_predict(filtered_data, 'Predicted_target', ['latitude', 'longitude', 'area_feature'])

    # Check if there are predictions to display
    if 'Predicted_target' in filtered_data.columns and not np.all(predicted_target == 0):

        # Apply bootstrap - bounds
        lower_bound, higher_bound = bootstrap_stats(filtered_data['target_column'])

        mean_value = np.mean(filtered_data['Predicted_target'])

        # Display the results with custom styling
        st.markdown("## **Algoritmo KNN (K-nearest neighbors)**")
        st.write(f"Valor médio (Reais/m²) para as características selecionadas: ${mean_value:.2f}$ Reais")
        st.write(f"Os valores podem variar entre ${lower_bound:.2f}$ e ${higher_bound:.2f}$ Reais, dependendo das características dos imóveis.")
    else:
        st.warning(f"**Dados insuficientes para inferência do valor. Mínimo necessário:** {k_threshold}")

    import streamlit as st

    # Generate the profile report
    with st.spinner('Carregando análise...'):
        profile = ProfileReport(filtered_data, title="Análise Exploratória dos Dados", explorative=True)
        profile_html = profile.to_html()

    # Replace English text with Portuguese
    profile_html = profile_html.replace("Overview", "Visão geral")
    profile_html = profile_html.replace("Alerts", "Alertas")
    profile_html = profile_html.replace("Reproduction", "Reprodução")
    profile_html = profile_html.replace("Dataset statistics", "Estatísticas do conjunto de dados")
    profile_html = profile_html.replace("Variable types", "Tipos de variáveis")
    profile_html = profile_html.replace("Variables", "Variáveis")
    profile_html = profile_html.replace("Interactions", "Interações")
    profile_html = profile_html.replace("Correlations", "Correlações")
    profile_html = profile_html.replace("Missing values", "Valores faltantes")
    profile_html = profile_html.replace("Sample", "Amostra")
    profile_html = profile_html.replace("Number of variables", "Número de variáveis")
    profile_html = profile_html.replace("Number of observations", "Número de observações")
    profile_html = profile_html.replace("Missing cells", "Células faltantes")
    profile_html = profile_html.replace("Missing cells (%)", "Células faltantes (%)")
    profile_html = profile_html.replace("Duplicate rows", "Linhas duplicadas")
    profile_html = profile_html.replace("Duplicate rows (%)", "Linhas duplicadas (%)")
    profile_html = profile_html.replace("Total size in memory", "Tamanho total na memória")
    profile_html = profile_html.replace("Average record size in memory", "Tamanho médio do registro na memória")
    profile_html = profile_html.replace("Text", "Texto")
    profile_html = profile_html.replace("Numeric", "Numérico")
    profile_html = profile_html.replace("Categorical", "Categórico")
    profile_html = profile_html.replace("Distinct", "Distinto")
    profile_html = profile_html.replace("Distinct (%)", "Distinto (%)")
    profile_html = profile_html.replace("Missing", "Faltando")
    profile_html = profile_html.replace("Missing (%)", "Faltando (%)")
    profile_html = profile_html.replace("Memory size", "Tamanho da memória")
    profile_html = profile_html.replace("Real number", "Número real")
    profile_html = profile_html.replace("Infinite", "Infinito")
    profile_html = profile_html.replace("Infinite (%)", "Infinito (%)")
    profile_html = profile_html.replace("Mean", "Média")
    profile_html = profile_html.replace("Minimum", "Mínimo")
    profile_html = profile_html.replace("Maximum", "Máximo")
    profile_html = profile_html.replace("Zeros", "Zeros")
    profile_html = profile_html.replace("Zeros (%)", "Zeros (%)")
    profile_html = profile_html.replace("Negative", "Negativo")
    profile_html = profile_html.replace("Negative (%)", "Negativo (%)")
    profile_html = profile_html.replace("Other values (2)", "Outros valores (2)")
    profile_html = profile_html.replace("Link", "Link")
    profile_html = profile_html.replace("UNIQUE", "ÚNICO")
    profile_html = profile_html.replace("CONSTANT", "CONSTANTE")
    profile_html = profile_html.replace("Average", "Média")
    profile_html = profile_html.replace("Number of rows", "Número de linhas")
    profile_html = profile_html.replace("Distinct values", "Valores distintos")
    profile_html = profile_html.replace("Histogram", "Histograma")
    profile_html = profile_html.replace("Top", "Top")
    profile_html = profile_html.replace("Bottom", "Inferior")
    profile_html = profile_html.replace("Frequency", "Frequência")
    profile_html = profile_html.replace("has constant value", "tem valores constantes")
    profile_html = profile_html.replace("has unique value", "tem valores únicos")
    profile_html = profile_html.replace("Analysis started", "Início da análise")
    profile_html = profile_html.replace("Analysis finished", "Término da análise")
    profile_html = profile_html.replace("Duration", "Duração")
    profile_html = profile_html.replace("Software version", "Versão do software")
    profile_html = profile_html.replace("Download configuration", "Configuração para download")
    profile_html = profile_html.replace("Select Columns", "Selecione coluna")
    profile_html = profile_html.replace("Length", "Comprimento")
    profile_html = profile_html.replace("Max length", "Comprimento máximo")
    profile_html = profile_html.replace("Median length", "Comprimento mediano")
    profile_html = profile_html.replace("Mean length", "Comprimento médio")
    profile_html = profile_html.replace("Min length", "Comprimento mínimo")
    profile_html = profile_html.replace("Characters and Unicode", "Caracteres e Unicode")
    profile_html = profile_html.replace("Total characters", "Total de caracteres")
    profile_html = profile_html.replace("Distinct characters", "Caracteres distintos")
    profile_html = profile_html.replace("Distinct categories", "Categorias distintas")
    profile_html = profile_html.replace("Distinct scripts", "Scripts distintos")
    profile_html = profile_html.replace("Distinct blocks", "Blocos distintos")
    profile_html = profile_html.replace("The Unicode Standard assigns character properties to each code point, which can be used to analyse textual variables.", "O Padrão Unicode atribui propriedades de caracteres a cada ponto de código, que podem ser usados para analisar variáveis textuais.")
    profile_html = profile_html.replace("Unique", "Único")
    profile_html = profile_html.replace("Unique (%)", "Único (%)")
    profile_html = profile_html.replace("Words", "Palavras")
    profile_html = profile_html.replace("Characters", "Caracteres")
    profile_html = profile_html.replace("Most occurring characters", "Caracteres mais frequentes")
    profile_html = profile_html.replace("Categories", "Categorias")
    profile_html = profile_html.replace("Most occurring categories", "Categorias mais frequentes")
    profile_html = profile_html.replace("(unknown)", "(desconhecido)")
    profile_html = profile_html.replace("Most frequent character per category", "Caractere mais frequente por categoria")
    profile_html = profile_html.replace("Scripts", "Scripts")
    profile_html = profile_html.replace("Most occurring scripts", "Scripts mais frequentes")
    profile_html = profile_html.replace("Most frequent character per script", "Caractere mais frequente por script")
    profile_html = profile_html.replace("Blocks", "Blocos")
    profile_html = profile_html.replace("Most occurring blocks", "Blocos mais frequentes")
    profile_html = profile_html.replace("Frequency (%)", "Frequência (%)")
    profile_html = profile_html.replace("Most frequent character per block", "Caractere mais frequente por bloco")
    profile_html = profile_html.replace("Matrix", "Matriz")
    profile_html = profile_html.replace("First rows", "Primeiras linhas")
    profile_html = profile_html.replace("Last rows", "Últimas linhas")
    profile_html = profile_html.replace("More details", "Maior detalhamento")
    profile_html = profile_html.replace("Statistics", "Estatísticas")
    profile_html = profile_html.replace("Quantile statistics", "Estatísticas de quantis")
    profile_html = profile_html.replace("Common values", "Valores comuns")
    profile_html = profile_html.replace("Extreme values", "Valores extremos")
    profile_html = profile_html.replace("5-th percentile", "5º percentil")
    profile_html = profile_html.replace("median", "mediana")
    profile_html = profile_html.replace("95-th percentile", "95º percentil")
    profile_html = profile_html.replace("Range", "Intervalo")
    profile_html = profile_html.replace("Interquartile range (IQR)", "Intervalo Interquartil")
    profile_html = profile_html.replace("Descriptive statistics", "Estatísticas descritivas")
    profile_html = profile_html.replace("Standard deviation", "Desvio padrão")
    profile_html = profile_html.replace("Coefficient of variation (CV)", "Coeficiente de variação (CV)")
    profile_html = profile_html.replace("Kurtosis", "Curtose")
    profile_html = profile_html.replace("Median Absolute Deviation (MAD)", "Desvio Absoluto Mediano (MAD)")
    profile_html = profile_html.replace("Skewness", "Assimetria")
    profile_html = profile_html.replace("Sum", "Soma")
    profile_html = profile_html.replace("Variance", "Variância")
    profile_html = profile_html.replace("Monotonicity", "Monotonicidade")
    profile_html = profile_html.replace("Not monotonic", "Não monotônica")
    profile_html = profile_html.replace("Histogram with fixed size bins (bins=16)", "Histograma com intervalos de tamanho fixo (intervalos=16)")
    profile_html = profile_html.replace("Minimum 10 values", "Mínimo 10 valores")
    profile_html = profile_html.replace("Maximum 10 values", "Máximo 10 valores")
    profile_html = profile_html.replace("1st row", "1ª linha")
    profile_html = profile_html.replace("2nd row", "2ª linha")
    profile_html = profile_html.replace("3rd row", "3ª linha")
    profile_html = profile_html.replace("4th row", "4ª linha")
    profile_html = profile_html.replace("5th row", "5ª linha")

    # Display the modified HTML in Streamlit
    components.html(profile_html, height=600, scrolling=True)
