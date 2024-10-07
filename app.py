from flask import Flask, render_template_string, url_for
import threading

# Criação do aplicativo Flask
app = Flask(__name__)

# Template HTML da landing page com o menu fixo e carrossel de banners
html_template = """
<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>avalia.se - o valor do seu bem</title>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <style>
    html, body {
        height: 100%; /* Garante que o corpo da página ocupe 100% da altura da janela */
        margin: 0;
        padding: 0px;
    }

    body {
        font-family: 'Quicksand', sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f8f9fa;
        scroll-behavior: smooth;
        position: relative;
        color: #000000;
        display: flex;
        flex-direction: column;
    }

    .topnav {
        overflow: hidden;
        background-color: #000000;
        display: flex;
        align-items: center;
        justify-content: center;
        position: fixed;
        top: 0;
        width: 100%;
        height: 50px;
        z-index: 1000;
      }

      .topnav img {
        position: absolute;
        left: 10px;
        top: 50%;
        transform: translateY(-50%);
        width: 150px;
        height: auto;
      }

      .topnav a {
        float: none;
        display: block;
        color: white;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
        font-size: 18px;
      }

      .topnav a:hover {
        background-color: #495057;
      }
      
      .main-content {
        padding: 100px;
        margin-top: 100px;
        flex: 1 0 auto; /* O conteúdo principal pode crescer conforme necessário */
      }
      
      h2 {scroll-margin-top: 50px; /* Define a margem superior para evitar o corte dos títulos */}

      .container {padding-top: 70px; /* Adiciona um padding para compensar a barra de navegação */}
      

      h1 {
        color: #000000;
        font-weight: 500;
        text-align: center;
      }

      /* Adicione o CSS para os ícones SVG aqui */
      .app-button svg {
          width: 24px;
          height: 24px;
          margin-right: 10px;
          stroke: #000; /* Define a cor do ícone */
      }
      
      .caixa-preta {
          background-color: gray;
          color: white;
          padding: 15px;
          border-radius: 10px; /* Define os cantos arredondados */
          width: 300px; /* Define a largura da caixa */
          text-align: center; /* Centraliza o texto */
      }

      /* Estilo da barra preta no rodapé */
      .footer {
        background-color: #000000;
        color: #ffffff;
        padding: 5px 5px;
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 0px;
        flex-shrink: 0; /* O rodapé não encolhe, mantendo-se fixo no final */
      }

      .footer img {
        width: 150px;
        height: auto;
      }

      .footer .right {
        text-align: right;
      }

      /* Estilo para o fundo cinza claro nas seções */
      .full-width-section {
        background-color: #f2f2f2;
        padding: 20px 0;
        width: 100vw;
        margin-left: calc(-50vw + 50%);
      }
      
      .bg-black {background-color: #000000 !important;}
      
      .navbar-toggler-icon {background-image: url("data:image/svg+xml;charset=utf8,%3Csvg viewBox='0 0 30 30' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath stroke='rgba%28255, 255, 255, 1%29' stroke-width='2' stroke-linecap='round' stroke-miterlimit='10' d='M4 7h22M4 15h22M4 23h22'/%3E%3C/svg%3E");}

      .navbar-toggler {border-color: rgba(255, 255, 255, 0.1); /* Bordas claras ao redor do botão */}
      
      .servicos-columns {
        display: flex;
        justify-content: space-between;
      }

      .servico-item {
        flex: 1;
        margin: 0 10px;
        padding: 20px;
        background-color: #f5f5f5; /* cor de fundo para diferenciar cada coluna */
        border-radius: 8px;
      }

      .servico-item p {
        margin-top: 10px;
      }
      
     /* Remover o padding e a margem que causam o espaço extra entre as seções */
      .main-content {
        padding-top: 0;
        margin-top: 0;
      }

      .full-width-section {
        padding-top: 0px;
        margin-top: 0px;
      }
    </style>
  </head>
  <body>

    <!-- Menu de topo -->
    <nav class="navbar navbar-expand-md navbar-dark bg-black fixed-top">
      <a class="navbar-brand" href="#">
        <img src="{{ url_for('static', filename='avalia_b.png') }}" alt="Logo Avalia" width="150" height="auto">
      </a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item"><a class="nav-link" href="#contexto">Contexto</a></li>
          <li class="nav-item"><a class="nav-link" href="#processo">Processo Avaliatório</a></li>
          <li class="nav-item"><a class="nav-link" href="#solucao">Solução</a></li>
          <li class="nav-item"><a class="nav-link" href="#aplicativos">Aplicativos</a></li>
          <li class="nav-item"><a class="nav-link" href="#municipios">Municípios</a></li>
          <li class="nav-item"><a class="nav-link" href="#servicos">Serviços</a></li>
        </ul>
      </div>
    </nav>

    <!-- Carrossel de banners -->
    <div id="carouselExampleIndicators" class="carousel slide" data-ride="carousel" data-interval="10000">
      <ol class="carousel-indicators">
        <li data-target="#carouselExampleIndicators" data-slide-to="0" class="active"></li>
        <li data-target="#carouselExampleIndicators" data-slide-to="1"></li>
        <li data-target="#carouselExampleIndicators" data-slide-to="2"></li>
        <li data-target="#carouselExampleIndicators" data-slide-to="3"></li>
      </ol>
        <div class="carousel-inner">
            <div class="carousel-item active">
              <img src="{{ url_for('static', filename='resized_banner1_cut.jpg') }}" class="d-block w-100 banner-img" alt="Banner 1">
              <div class="carousel-caption d-none d-md-block" style="top: 60%; transform: translateY(-50%);">
                <div style="background-color: rgba(0, 0, 0, 0.8); border-radius: 20px; padding: 15px; display: inline-block;">
                  <h5 style="font-family: 'Quicksand', sans-serif; color: #FFC000; font-size: 36px">A avalia.se é uma empresa de tecnologia e serviços para avaliação de bens</h5>
                </div>
              </div>
            </div>

            <div class="carousel-item">
              <img src="{{ url_for('static', filename='resized_banner2.jpg') }}" class="d-block w-100 banner-img" alt="Banner 2">
              <div class="carousel-caption d-none d-md-block" style="top: 60%; transform: translateY(-50%);">
                <div style="background-color: rgba(0, 0, 0, 0.8); border-radius: 20px; padding: 15px; display: inline-block;">
                  <h5 style="font-family: 'Quicksand', sans-serif; color: #FFC000; font-size: 36px">Queremos entender o mercado imobiliário e tornar os municípios responsivos na avaliação de imóveis</h5>
                </div>
              </div>
            </div>

            <div class="carousel-item">
              <img src="{{ url_for('static', filename='resized_banner3.jpg') }}" class="d-block w-100 banner-img" alt="Banner 3">
              <div class="carousel-caption d-none d-md-block" style="top: 55%; transform: translateY(-50%);">
                <div style="background-color: rgba(0, 0, 0, 0.8); border-radius: 20px; padding: 15px; display: inline-block;">
                  <h5 style="font-family: 'Quicksand', sans-serif; color: #FFC000; font-size: 36px">Buscamos agilizar as avaliações de imóveis nos municípios por meio da expertise técnica e da tecnologia</h5>
                </div>
              </div>
            </div>

            <div class="carousel-item">
              <img src="{{ url_for('static', filename='resized_banner4.jpg') }}" class="d-block w-100 banner-img" alt="Banner 4">
              <div class="carousel-caption d-none d-md-block" style="top: 60%; transform: translateY(-50%);">
                <h5 style="font-family: 'Quicksand', sans-serif; color: #554E39; font-size: 36px">O mais importante para o avalia.se é <br><strong>o valor do seu bem</strong></h5>
                </div>
              </div>
            </div>
        </div>
        
      <a class="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="sr-only">Previous</span>
      </a>
      <a class="carousel-control-next" href="#carouselExampleIndicators" role="button" data-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="sr-only">Next</span>
      </a>
    </div>

    <style>
      /* Define a altura máxima das imagens no carrossel */
      .banner-img {
        max-height: 620px;
        object-fit: cover; /* Garante que a imagem mantenha suas proporções */
      }
    </style>

<!-- Conteúdo principal -->
<div class="main-content">
    <!-- Apenas o div "contexto" terá o fundo cinza claro e ocupará toda a largura da página -->
    <div id="contexto" class="container-fluid contexto-content full-width-section">
      <div class="container">
        <h2>Contexto</h2>
        <ul>
        <li>A avaliação de imóveis, essencial para os municípios, é um processo complexo e normatizado que exige soluções tecnológicas eficientes e capacitação contínua para lidar com o grande volume de informações envolvido.</li>
        </ul>
        <h2>Desafios que muitos municípios enfrentam</h2>
        <ul>
        <li>A alta demanda, a falta de profissionais especializados e de sistemas adequados, além da dificuldade em manter dados atualizados e integrar diferentes ferramentas, são grandes desafios para a gestão de avaliações imobiliárias.</li>
        </ul>     
        <h2>Possíveis consequências</h2>
        <ul>
        <li>A desatualização de plantas de valores, indenizações inadequadas e a falta de precisão nas aquisições e cobranças geram prejuízos financeiros, processos judiciais e comprometem a transparência pública.</li>
        </ul>
      </div>
    </div>
      
    <!-- Processo -->
     <div id="processo" class="container processo-content">
       <h2>Processo Avaliatório - O que é?</h2>
       <img src="{{ url_for('static', filename='processo.png') }}" class="img-fluid mx-auto d-block" alt="processo" style="display: block; margin: 20px auto; width: 900px; height: auto;">
       <p>O fluxo do processo avaliatório necessita uma série de sistemas que normalmente não são integrados.</p>
       <img src="{{ url_for('static', filename='sistemas.png') }}" class="img-fluid mx-auto d-block" alt="sistemas" style="display: block; margin: 20px auto; width: 900px; height: auto;">
     </div>
 
    <!-- Solução com fundo cinza claro e ocupando toda a largura da página -->
    <div id="solucao" class="full-width-section">
        <div class="container">
          <h2>Solução</h2>
          <p><strong>Todas as etapas do processo de avaliação, da coleta de dados à elaboração do laudo técnico, em um único lugar.</strong></p>
          <p><strong>IA</strong></p>
          <p>Nossa plataforma conta com recursos de inteligência artificial, com o intuito de agilizar os processos, acurar os resultados e manter sempre atualizadas as bases de dados e as soluções.</p>
        </div>
      </div>

    <div id="aplicativos" class="container">
      <h2>Aplicativos</h2>
      <ul>
        <li>Dashboard Geospacial: dados de mercado, variáveis e análise exploratória.</li>
        <li>Regressão Linear: Método Comparativo Direto de Dados de Mercado (NBR 14653-2:2011), com tratamento dos dados pelo método científico (Inferência estatística por meio de Regressão Linear).</li>
        <li>Método Evolutivo: Método com a avaliação separada do terreno e da construção, conforme a NBR 14653-2:2011.</li>
        <li>Bens Móveis: Avaliação patrimonial de Órgãos Públicos e Empresas.</li>
      </ul>

      <div class="app-buttons" style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: space-between;">

        <!-- Dashboard Geoespacial -->
        <div class="caixa-preta" style="flex: 1 1 calc(25% - 20px); display: flex; justify-content: space-between; align-items: center; padding: 20px;">
          <a href="https://fschwartzer-geo-dash-tabs.hf.space" target="_blank" class="app-button" style="text-decoration: none; color: white; font-weight: bold; display: flex; align-items: center; width: 100%;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="app-icon" style="width: 50px; height: 50px; margin-right: 10px;">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M2 12h20M12 2a15.3 15.3 0 0 1 0 20M12 2a15.3 15.3 15.3 0 0 0 0 20"></path>
            </svg>
            <span style="flex-grow: 1; text-align: right;">Dashboard Geoespacial</span>
          </a>
        </div>

        <!-- Regressão Linear -->
        <div class="caixa-preta" style="flex: 1 1 calc(25% - 20px); display: flex; justify-content: space-between; align-items: center; padding: 20px;">
          <a href="https://davidsb-avalia-se-rl-tabs.hf.space" target="_blank" class="app-button" style="text-decoration: none; color: white; font-weight: bold; display: flex; align-items: center; width: 100%;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="app-icon" style="width: 50px; height: 50px; margin-right: 10px;">
              <line x1="3" y1="21" x2="21" y2="21"></line>
              <line x1="3" y1="21" x2="3" y2="3"></line>
              <circle cx="7" cy="17" r="1"></circle>
              <circle cx="13" cy="10" r="1"></circle>
              <circle cx="19" cy="6" r="1"></circle>
              <line x1="3" y1="19" x2="19" y2="6"></line>
            </svg>
            <span style="flex-grow: 1; text-align: right;">Regressão Linear</span>
          </a>
        </div>

        <!-- Método Evolutivo -->
        <div class="caixa-preta" style="flex: 1 1 calc(25% - 20px); display: flex; justify-content: space-between; align-items: center; padding: 20px;">
          <a href="https://davidsb-avalia-evo.hf.space" target="_blank" class="app-button" style="text-decoration: none; color: white; font-weight: bold; display: flex; align-items: center; width: 100%;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="app-icon" style="width: 50px; height: 50px; margin-right: 10px;">
              <polyline points="6,22 6,8 18,8 18,22"></polyline>
              <line x1="4" y1="22" x2="20" y2="22"></line>
              <line x1="9" y1="10" x2="9" y2="10"></line>
              <line x1="9" y1="14" x2="9" y2="14"></line>
              <line x1="9" y1="18" x2="9" y2="18"></line>
              <line x1="15" y1="10" x2="15" y2="10"></line>
              <line x1="15" y1="14" x2="15" y2="14"></line>
              <line x1="15" y1="18" x2="15" y2="18"></line>
            </svg>
            <span style="flex-grow: 1; text-align: right;">Método Evolutivo</span>
          </a>
        </div>

        <!-- Bens Móveis -->
        <div class="caixa-preta" style="flex: 1 1 calc(25% - 20px); display: flex; justify-content: space-between; align-items: center; padding: 20px;">
          <a href="https://fschwartzer-bens-moveis-vision.hf.space" target="_blank" class="app-button" style="text-decoration: none; color: white; font-weight: bold; display: flex; align-items: center; width: 100%;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="app-icon" style="width: 50px; height: 50px; margin-right: 10px;">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
              <line x1="8" y1="21" x2="16" y2="21"></line>
              <line x1="12" y1="17" x2="12" y2="21"></line>
            </svg>
            <span style="flex-grow: 1; text-align: right;">Bens Móveis</span>
          </a>
        </div>
        <ul>
        </ul>

      </div>
    </div>
     
    <!-- Municípios com fundo cinza claro e largura total -->
    <div id="municipios" class="full-width-section">
        <div class="container">
          <h2>Municípios</h2>
          <p><strong>Prefeitura Municipal de Lajeado</strong></p>
          <img src="{{ url_for('static', filename='lajeado.png') }}" alt="lajeado" style="display: block; margin: 20px auto; width: 200px; height: auto;">
          <p>Em 2023, o avalia.se firmou uma parceria acadêmica com o Município de Lajeado com a intenção de conhecer melhor a realidade do município no que se refere a avaliação de imóveis e propor soluções.</p>
          <p>Inicialmente, foi feita uma entrevista aberta com o Eng. Franki Bersh, responsável pelas avaliações do município.</p>
          <p>A partir do diagnóstico, foram disponibilizados os seguintes recursos ao município:</p>
          <ul>
            <li>Dados de mercado atualizados e geolocalizados.</li>
            <li>Variável renda IBGE por meio de uma superfície (processo de krigagem).</li>
            <li>Aplicativos de cálculo.</li>
          </ul>
          <p>Resultados:</p>
          <ul>
            <li><strong><em>Comparando o tempo total empregado na elaboração de algumas avaliações, utilizando os aplicativos de avaliações, scrapping de dados de mercado e variável de localização elaborada com interpolação da Renda Bairro fornecida pelo IBGE, com avaliações similares feitas anteriormente sem estas ferramentas, estimo que o tempo médio por laudo reduziu aproximadamente 45%.</em></strong></li>
          </ul>
          <p style="text-align: right;"><strong><em>Eng. Franki Bersh (Responsável pelas avaliações no Município de Lajeado/RS).</em></strong></p> 
        </div>
      </div>
      
     <!-- Serviços -->
     <!-- Serviços -->
     <div id="servicos" class="container servicos-content">      
       <h2>Consultoria</h2>
       <p style="margin-bottom: 20px;"><strong>Oferecemos uma consultoria especializada para ajudar os municípios a otimizar seus processos de avaliação de imóveis. Além dos aplicativos, disponibilizamos os serviços abaixo com o objetivo de proporcionar uma gestão completa das avaliações.</strong></p>

       <div class="servicos-columns">
         <div class="servico-item">
           <strong>Gestão das Avaliações</strong>
           <p>Organização sistemática de todo o processo de avaliação, desde o cadastro até a geração de laudos técnicos. Organização, padronização e espacialização de modelos e laudos.</p>
         </div>
         <div class="servico-item">
           <strong>Modelos de Machine Learning</strong>
           <p>Elaboração de modelos preditivos utilizando técnicas avançadas de Machine Learning, com o objetivo de automatizar e aprimorar a precisão das avaliações de imóveis.</p>
         </div>
         <div class="servico-item">
           <strong>Capacitação e Treinamento</strong>
           <p>Capacitação técnica contínua para as equipes municipais, garantindo que estejam sempre atualizadas com as melhores práticas e ferramentas disponíveis no mercado de avaliações imobiliárias.</p>
         </div>
       </div>
     </div>
     
    <!-- Barra preta no rodapé, visível no final da rolagem -->
    <div class="footer full-width-section" style="background-color: #000000; padding: 0px;">
      <div class="container" style="display: flex; justify-content: space-between; align-items: center;">
        <div class="left logo-container">
          <img src="{{ url_for('static', filename='avalia_b.png') }}" alt="Logo Avalia" style="height: 42px;">
        </div>

        <div class="right" style="text-align: right;">
          <p>Email: <a href="mailto:ai.avalia.se@gmail.com" style="color: #FFC000; text-decoration: none;">ai.avalia.se@gmail.com</a></p>
          <p>Porto Alegre/RS</p>
          <p>Brasil</p>
        </div>
      </div>
    </div>

    <style>
      /* Media query para esconder o logotipo em telas pequenas */
      @media (max-width: 480px) {
        .logo-container img {
          display: none;
        }
      }
    </style>

    </div>

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
  </body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

def run_app():
    app.run()

# Rodar o Flask no Jupyter
flask_thread = threading.Thread(target=run_app)
flask_thread.start()
