import gradio as gr
from modules.dados import dados_tab
from modules.planilha import planilha_tab  # Importe apenas planilha_tab, save_new_df é usado internamente no módulo
from modules.otimiza import otimiza_tab
from modules.rl import rl_tab
from modules.ml import ml_tab
from modules.evo import evo_tab

# Cria o app principal
theme = gr.themes.Citrus(
    primary_hue="gray",
)

# .css para estilizar a interface + JavaScript para ajustar o scroll
with gr.Blocks(theme=theme, css="""
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;700&display=swap');

    .small-file-upload { 
        height: 65px; 
        text-align: center;
        color: black; /* Cor das letras */
        border: 2px solid black !important; /* Borda sólida e larga, !important para sobrepor estilos conflitantes */
        box-sizing: border-box; /* Garante que a borda não afete o tamanho total */
    }
    .small-file-upload span { 
        display: none;  /* Oculta o texto interno */
    }
    .small-file-upload input[type="file"] {
        color: black; /* Garante que o texto interno fique preto */
    }
    .small-file-upload label {
        color: black; /* Garante que o texto do rótulo fique preto */
    }
    .small span {
        font-size: 1.2em; /* Reduz o tamanho da fonte nos DataFrames */
        white-space: nowrap; /* Impede quebra de linha no cabeçalho */
        width: auto; /* Permite que a largura da coluna cresça conforme o conteúdo */
        display: inline-block; /* Garante que o ajuste de largura funcione corretamente */
    }
    .small span dados {
        font-size: 0.8em; /* Reduz o tamanho da fonte nos DataFrames */
        white-space: nowrap; /* Impede quebra de linha no cabeçalho */
        width: auto; /* Permite que a largura da coluna cresça conforme o conteúdo */
        display: inline-block; /* Garante que o ajuste de largura funcione corretamente */
    }
    
    /* Estilo para o título com fonte Quicksand */
    h1 {
        text-align: center;
        font-family: 'Quicksand', sans-serif; /* Aplica a fonte Quicksand */
        font-weight: 700; /* Peso da fonte */
        margin: 20px 0; /* Espaçamento ao redor do título */
        color: black; /* Cor do texto */
    }
    /* Estilo customizado para ajustar a altura do mapa */
    .map-container {
        height: 600px !important;
        margin: 0;
        padding: 0;
        <style>
    }
""") as app:
    # Adiciona JavaScript para rolar para o topo após ordenar tabelas
    gr.HTML("""
    <script>
        // Função para resetar o scroll ao topo da tabela
        function resetScrollToTop() {
            let tableContainer = document.querySelector(".dataframe-container");
            if (tableContainer) {
                tableContainer.scrollTop = 0; // Voltar ao topo
            }
        }

        // Monitorar cliques nos cabeçalhos da tabela
        document.addEventListener("click", function(e) {
            if (e.target.closest(".dataframe-container th")) {
                resetScrollToTop();
            }
        });
    </script>
    """)

    with gr.Tabs():     
        # Adiciona abas importadas
        dados_ui, filtered_df_output = dados_tab()  ##### MODIFICAÇÃO #####
        planilha_ui, new_df_output = planilha_tab(filtered_df_output)  ##### MODIFICAÇÃO ##### # Passa filtered_df_output para a aba Carregar Planilha
        otimiza_ui = otimiza_tab(new_df_output)     # Passa new_df_output para a aba Otimizar Modelo
        rl_ui = rl_tab()
        ml_ui = ml_tab(new_df_output)              # Passa new_df_output para a aba Machine Learning
        evo_ui = evo_tab()

# Executa o app
if __name__ == "__main__":
    app.launch('localhost', 0000, aplicativo)


