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
    <!-- Adicionando o favicon -->
    <link rel="icon" href="{{ url_for('static', filename='ia_y.png') }}" sizes="128x128" type="image/png">
    <title>avalia.se - o valor do seu bem</title>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <style>
    html, body {
        height: 100%; /* Garante que o corpo da página ocupe 100% da altura da janela */
        margin: 0;
        padding: 0px;
        font-family: 'Quicksand', sans-serif; /* Define a fonte Quicksand para toda a página */
    }

    body {
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
      
      h2 {scroll-margin-top: 50px; /* Define a margem superior para evitar o corte dos títulos */ }

      .container {padding-top: 70px; /* Adiciona um padding para compensar a barra de navegação */ }
      
      h1, h2, h5, strong {
        color: #000000;
        font-weight: 500;
        text-align: left; /* Alinhando os títulos à esquerda */
      }


      .caixa-preta {
          background-color: gray;
          color: white;
          padding: 15px;
          border-radius: 10px;
          width: 300px;
          text-align: center;
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
        flex-shrink: 0;
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
      
      .navbar-toggler-icon {
        background-image: url("data:image/svg+xml;charset=utf8,%3Csvg viewBox='0 0 30 30' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath stroke='rgba%28255, 255, 255, 1%29' stroke-width='2' stroke-linecap='round' stroke-miterlimit='10' d='M4 7h22M4 15h22M4 23h22'/%3E%3C/svg%3E");
      }

      .navbar-toggler {border-color: rgba(255, 255, 255, 0.1); }
      
      .servicos-columns {
        display: flex;
        justify-content: space-between;
      }

      .servico-item {
        flex: 1;
        margin: 0 10px;
        padding: 20px;
        background-color: #f5f5f5;
        border-radius: 8px;
      }

      .servico-item p {
        margin-top: 10px;
      }
      
      .main-content {
        padding-top: 0;
        margin-top: 0;
      }

      .full-width-section {
        padding-top: 0px;
        margin-top: 0px;
      }

      /* Media query para esconder o logotipo em telas pequenas */
      @media (max-width: 480px) {
        .logo-container img {
          display: none;
        }
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
          <li class="nav-item"><a class="nav-link" href="#cenario">Cenário</a></li>
          <li class="nav-item"><a class="nav-link" href="#servicos">Serviços</a></li>
          <li class="nav-item"><a class="nav-link" href="#aplicativos">Aplicativos</a></li>
          <li class="nav-item"><a class="nav-link" href="#cases">Cases</a></li>
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
                  <h5 style="color: #FFC000; font-size: 36px">A avalia.se é uma empresa de tecnologia e serviços para avaliação de bens</h5>
                </div>
              </div>
            </div>

            <div class="carousel-item">
              <img src="{{ url_for('static', filename='resized_banner2.jpg') }}" class="d-block w-100 banner-img" alt="Banner 2">
              <div class="carousel-caption d-none d-md-block" style="top: 60%; transform: translateY(-50%);">
                <div style="background-color: rgba(0, 0, 0, 0.8); border-radius: 20px; padding: 15px; display: inline-block;">
                  <h5 style="color: #FFC000; font-size: 36px">Buscamos entender o mercado imobiliário para tornar responsivos os municípios na avaliação de imóveis</h5>
                </div>
              </div>
            </div>

            <div class="carousel-item">
              <img src="{{ url_for('static', filename='resized_banner3.jpg') }}" class="d-block w-100 banner-img" alt="Banner 3">
              <div class="carousel-caption d-none d-md-block" style="top: 60%; transform: translateY(-50%);">
                <div style="background-color: rgba(0, 0, 0, 0.8); border-radius: 20px; padding: 15px; display: inline-block;">
                  <h5 style="color: #FFC000; font-size: 36px">Agilizamos os processos de avaliação por meio da tecnologia</h5>
                </div>
              </div>
            </div>

            <div class="carousel-item">
              <img src="{{ url_for('static', filename='resized_banner4.jpg') }}" class="d-block w-100 banner-img" alt="Banner 4">
              <div class="carousel-caption d-none d-md-block" style="top: 60%; transform: translateY(-50%);">
                <h5 style="color: #554E39; font-size: 45px;">
                  O mais importante para nós da avalia.se é 
                  <strong style="color: #b38b00;">o valor do seu bem</strong>
                </h5>

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
        object-fit: cover;
      }
    </style>

<!-- Conteúdo principal -->
<div class="main-content">
<!-- Apenas o div "cenario" terá o fundo cinza claro e ocupará toda a largura da página -->
<div id="cenario" class="container-fluid contexto-content full-width-section">
  <div class="container">
    <h2 style="color: black; font-weight: bold;">Cenário</h2>
    <div class="servicos-columns" style="display: flex; justify-content: space-between; gap: 20px;">
      <!-- Desafio -->
      <div class="servico-item" style="background-color: #d3d3d3; padding: 20px; border-radius: 0; flex: 1;">
        <strong style="font-size: 1.3em;">Condicionantes</strong>
        <p style="font-size: 1.2em;">A avaliação de imóveis, fundamental para os municípios, é uma atividade complexa e regulamentada, que está presente em vários processos, como plantas de valores, desapropriações, aquisições, locações, entre outros.</p>

      </div>

      <!-- Impacto -->
      <div class="servico-item" style="background-color: #d3d3d3; padding: 20px; border-radius: 0; flex: 1;">
        <strong style="font-size: 1.3em;">Impactos</strong>
        <p style="font-size: 1.2em;">Valores imprecisos podem gerar prejuízos financeiros, desencadear processos judiciais, comprometer a arrecadação municipal e impactar negativamente a imagem da administração pública perante a sociedade.</p>
      </div>

      <!-- Desafios Municipais -->
      <div class="servico-item" style="background-color: #d3d3d3; padding: 20px; border-radius: 0; flex: 1;">
        <strong style="font-size: 1.3em;">Realidades do Municípios</strong>
        <p style="font-size: 1.2em;">A alta demanda, a falta de profissionais especializados e de sistemas adequados, além da dificuldade em manter um banco de dados atualizado, são alguns dos desafios para a gestão municipal.</p>
      </div>
    </div>

    <!-- Processo Avaliatório (Agora dentro do Cenario) -->
    <div class="row" style="margin-top: 40px;">
      <!-- Coluna Esquerda - Texto -->
      <div class="col-md-6">
        <h2 style="color: black; font-weight: bold;">Processo Avaliatório</h2>
        <p style="font-size: 1.2em;">O processo avaliatório, de forma sucinta, é um conjunto de etapas baseadas na NBR 14.653, necessárias para produzir um Laudo de Avaliação ou um Parecer Técnico.</p>
        <p style="font-size: 1.2em;">Para cumprir estas etapas são necessárias diversas ações e alguns sistemas como planilhas eletrônicas, sistemas de geo, softwares de avaliação e editores de texto.</p>
      </div>

      <!-- Coluna Direita - Carrossel -->
      <div class="col-md-6">
        <div id="carouselProcesso" class="carousel slide" data-ride="carousel" data-interval="5000">
          <div class="carousel-inner">
            <div class="carousel-item active">
              <div class="bloco">
                <h4 class="carrossel-titulo">Identificação do objeto</h4>
                <ul class="carrossel-explicacao">
                    <li>Vistoria</li>
                    <li>Fotos</li>
                    <li>Entorno</li>
                    <li>Diagnóstico de mercado</li>
                </ul>
              </div>
            </div>
            <div class="carousel-item">
              <div class="bloco">
                <h4 class="carrossel-titulo">Levantamento de dados</h4>
                <ul class="carrossel-explicacao">
                    <li>Ofertas</li>
                    <li>Transações</li>
                    <li>Consolidação do banco de dados</li>
                </ul>
              </div>
            </div>
            <div class="carousel-item">
              <div class="bloco">
                <h4 class="carrossel-titulo">Estipular as premissas para as variáveis do modelo</h4>
                <ul class="carrossel-explicacao">
                    <li>Variável dependente - explicada</li>
                    <li>Variáveis independente - explicativas</li>
                </ul>
              </div>
            </div>
            <div class="carousel-item">
              <div class="bloco">
                <h4 class="carrossel-titulo">Tratamento dos dados</h4>
                <ul class="carrossel-explicacao">
                    <li>Análise exploratória</li>
                    <li>Regressão Linear</li>
                    <li>Tratamento por Fatores</li>
                </ul>
              </div>
            </div>
            <div class="carousel-item">
              <div class="bloco">
                <h4 class="carrossel-titulo">Elaboração do documento técnico</h4>
                <ul class="carrossel-explicacao">
                    <li>Laudo de Avaliação</li>
                    <li>Parecer Técnico</li>
                </ul>
              </div>
            </div>
            <!-- Add remaining carousel items as needed -->
          </div>
          <!-- Carousel Controls -->
          <a class="carousel-control-prev" href="#carouselProcesso" role="button" data-slide="prev">
            <span class="carousel-control-prev-icon" style="filter: invert(100%);" aria-hidden="true"></span>
            <span class="sr-only">Anterior</span>
          </a>
          <a class="carousel-control-next" href="#carouselProcesso" role="button" data-slide="next">
            <span class="carousel-control-next-icon" style="filter: invert(100%);" aria-hidden="true"></span>
            <span class="sr-only">Próximo</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .bloco {
      background-color: white; /* Fundo branco */
      color: black;
      padding: 20px;
      text-align: center;
      border: 4px solid #b38b00; /* Borda amarelo ouro */
      border-radius: 0; /* Cantos retos */
      display: flex;
      flex-direction: column;
      justify-content: center;
      height: 100%;
  }
  .carrossel-titulo {
      font-weight: bold;
      color: #b38b00; /* Título em amarelo ouro */
      font-size: 2em;
  }
  .carrossel-explicacao {
      font-weight: bold;
      list-style-type: none;
      padding: 0;
      color: black;
      font-size: 1.6em; /* Explicações em preto */
  }
  
  /* Carrossel do processo avaliatório */
  #carouselProcesso .carousel-inner {
      height: 400px; /* Define uma altura fixa apenas para o carrossel do processo */
  }
  #carouselProcesso .carousel-item {
      height: 100%;
  }
  .carousel-control-prev-icon, .carousel-control-next-icon {
      background-color: transparent;
  }
  .bloco {
      display: flex;
      flex-direction: column;
      justify-content: center;
      height: 100%;
  }
</style>


<div id="servicos" class="full-width-section" style="background-color: #FFC000; padding: 20px 0;">
  <div class="container" style="display: flex; justify-content: space-between; gap: 20px;">
    
    <!-- Carrossel à esquerda -->
    <div class="col-md-4">
      <div id="carouselServicos" class="carousel slide h-100" data-ride="carousel" data-interval="10000">
        <div class="carousel-inner h-100" style="position: relative;">
          <!-- Imagem de fundo fixa -->
          <img src="{{ url_for('static', filename='data.png') }}" alt="Fundo" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0;">
          
          <!-- Primeira frase -->
          <div class="carousel-item active h-100 d-flex align-items-center justify-content-center" style="visibility: visible;">
            <div class="carousel-caption d-flex flex-column justify-content-center text-center" style="background-color: rgba(0, 0, 0, 0.7); padding: 20px; border-radius: 10px; width: 80%; z-index: 1;">
              <h5 style="color: #ffffff; font-weight: bold; font-size: 2em;">Aplicativos de avaliação conforme a NRB 14.643</h5>
            </div>
          </div>

          <!-- Segunda frase -->
          <div class="carousel-item h-100 d-flex align-items-center justify-content-center" style="visibility: hidden;">
            <div class="carousel-caption d-flex flex-column justify-content-center text-center" style="background-color: rgba(0, 0, 0, 0.7); padding: 20px; border-radius: 10px; width: 80%; z-index: 1;">
              <h5 style="color: #ffffff; font-weight: bold; font-size: 2em;">Técnicas avançadas de Machine Learning</h5>
            </div>
          </div>

          <!-- Terceira frase -->
          <div class="carousel-item h-100 d-flex align-items-center justify-content-center" style="visibility: hidden;">
            <div class="carousel-caption d-flex flex-column justify-content-center text-center" style="background-color: rgba(0, 0, 0, 0.7); padding: 20px; border-radius: 10px; width: 80%; z-index: 1;">
              <h5 style="color: #ffffff; font-weight: bold; font-size: 2em;">Oportunidade de capacitação para avaliadores</h5>
            </div>
          </div>
        </div>

        <!-- Controles do Carrossel -->
        <a class="carousel-control-prev" href="#carouselServicos" role="button" data-slide="prev">
          <span class="carousel-control-prev-icon" style="filter: invert(100%);" aria-hidden="true"></span>
          <span class="sr-only">Anterior</span>
        </a>
        <a class="carousel-control-next" href="#carouselServicos" role="button" data-slide="next">
          <span class="carousel-control-next-icon" style="filter: invert(100%);" aria-hidden="true"></span>
          <span class="sr-only">Próximo</span>
        </a>
      </div>
    </div>

    <!-- Texto à direita -->
    <div class="col-md-8">
      <h2 style="color: black; font-weight: bold;">Serviços</h2>
      <p style="font-size: 1.2em;">Conhecemos profundamente a área da Engenharia de Avaliações e nos diferenciamos porque somos avaliadores criando soluções para avaliadores. Utilizamos a inteligência artificial, para agilizar os processos, acurar os resultados e manter sempre atualizadas as soluções e as bases de dados.</p>
      <strong style="font-size: 1.6em; color: white;">Soluções para avaliações</strong>
      <p style="font-size: 1.2em;">A avalia.se oferece um sistema amplo de soluções para avaliadores, que inclui desde aplicativos que contemplam todas as etapas do processo de avaliação — da coleta de dados à geração do laudo técnico — até modelos avançados para avaliação em massa, utilizando as técnicas mais modernas da ciência de dados.</p>
      <strong style="font-size: 1.6em; color: white;">Treinamento e capacitação</strong>
      <p style="font-size: 1.2em;">Oportunizamos capacitação técnica contínua para as equipes municipais, garantindo que estejam sempre atualizadas com as melhores práticas e ferramentas disponíveis no mercado de avaliações imobiliárias.</p>
    </div>
  </div>
</div>

<div id="aplicativos" class="container">
    <h2 style="color: black; font-weight: bold;">Aplicativos</h2>

    <div class="app-buttons" style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: space-between;">
        <!-- Dashboard Geoespacial -->
        <div class="caixa-preta" style="flex: 1 1 calc(25% - 20px); display: flex; flex-direction: column; justify-content: space-between; align-items: center; padding: 20px; background-color: white; color: black; border: 2px solid #b38b00;">
            <a href="https://fschwartzer-geo-dash-tabs.hf.space" target="_blank" class="app-button" style="text-decoration: none; color: black; font-weight: bold; display: flex; flex-direction: column; align-items: center; width: 100%;">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#b38b00" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="app-icon" style="width: 50px; height: 50px; margin-bottom: 10px;">
                    <circle cx="12" cy="12" r="10"></circle>
                    <path d="M2 12h20M12 2a15.3 15.3 0 0 1 0 20M12 2a15.3 15.3 15.3 0 0 0 0 20"></path>
                </svg>
                <span style="flex-grow: 1; text-align: center;">Dashboard Geoespacial</span>
                <p style="text-align: center; margin-top: 10px; font-size: 0.9em; color: black; font-weight: normal;">Dados de mercado, variáveis e análise exploratória.</p>
            </a>
        </div>

        <!-- Regressão Linear -->
        <div class="caixa-preta" style="flex: 1 1 calc(25% - 20px); display: flex; flex-direction: column; justify-content: space-between; align-items: center; padding: 20px; background-color: white; color: black; border: 2px solid #b38b00;">
            <a href="https://davidsb-avalia-se-rl-tabs.hf.space" target="_blank" class="app-button" style="text-decoration: none; color: black; font-weight: bold; display: flex; flex-direction: column; align-items: center; width: 100%;">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#b38b00" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="app-icon" style="width: 50px; height: 50px; margin-bottom: 10px;">
                    <line x1="3" y1="21" x2="21" y2="21"></line>
                    <line x1="3" y1="21" x2="3" y2="3"></line>
                    <circle cx="7" cy="17" r="1"></circle>
                    <circle cx="13" cy="10" r="1"></circle>
                    <circle cx="19" cy="6" r="1"></circle>
                    <line x1="3" y1="19" x2="19" y2="6"></line>
                </svg>
                <span style="flex-grow: 1; text-align: center;">Regressão Linear</span>
                <p style="text-align: center; margin-top: 10px; font-size: 0.9em; color: black; font-weight: normal;">Método Comparativo Direto de Dados de Mercado (NBR 14653-2:2011), com tratamento dos dados pelo método científico.</p>
            </a>
        </div>

        <!-- Método Evolutivo -->
        <div class="caixa-preta" style="flex: 1 1 calc(25% - 20px); display: flex; flex-direction: column; justify-content: space-between; align-items: center; padding: 20px; background-color: white; color: black; border: 2px solid #b38b00;">
            <a href="#" target="_blank" class="app-button" style="text-decoration: none; color: black; font-weight: bold; display: flex; flex-direction: column; align-items: center; width: 100%;">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#b38b00" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="app-icon" style="width: 50px; height: 50px; margin-bottom: 10px;">
                    <polyline points="6,22 6,8 18,8 18,22"></polyline>
                    <line x1="4" y1="22" x2="20" y2="22"></line>
                    <line x1="9" y1="10" x2="9" y2="10"></line>
                    <line x1="9" y1="14" x2="9" y2="14"></line>
                    <line x1="9" y1="18" x2="9" y2="18"></line>
                    <line x1="15" y1="10" x2="15" y2="10"></line>
                    <line x1="15" y1="14" x2="15" y2="14"></line>
                    <line x1="15" y1="18" x2="15" y2="18"></line>
                </svg>
                <span style="flex-grow: 1; text-align: center;">Método Evolutivo</span>
                <p style="text-align: center; margin-top: 10px; font-size: 0.9em; color: black; font-weight: normal;">Método com a avaliação separada do terreno e da construção, conforme a NBR 14653-2:2011.</p>
            </a>
        </div>

        <!-- Bens Móveis -->
        <div class="caixa-preta" style="flex: 1 1 calc(25% - 20px); display: flex; flex-direction: column; justify-content: space-between; align-items: center; padding: 20px; background-color: white; color: black; border: 2px solid #b38b00;">
            <a href="#" target="_blank" class="app-button" style="text-decoration: none; color: black; font-weight: bold; display: flex; flex-direction: column; align-items: center; width: 100%;">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#b38b00" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="app-icon" style="width: 50px; height: 50px; margin-bottom: 10px;">
                    <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                    <line x1="8" y1="21" x2="16" y2="21"></line>
                    <line x1="12" y1="17" x2="12" y2="21"></line>
                </svg>
                <span style="flex-grow: 1; text-align: center;">Bens Móveis</span>
                <p style="text-align: center; margin-top: 10px; font-size: 0.9em; color: black; font-weight: normal;">Avaliação patrimonial de Órgãos Públicos e Empresas.</p>
             </a>
        </div>
    </div>
    <div style="margin-top: 30px;">
        <strong style="font-size: 1.3em;">Todos os aplicativos da avalia.se seguem a lógica da "Agilidade" nos processos, "Acurácia" nos resultados e "Atualização" permanente nos sistemas e bases de dados.</strong>
    </div>
</div>

<!-- Cases com fundo cinza claro e largura total -->
<div id="cases" class="full-width-section" style="background-color: #f0f0f0; padding: 0 0 40px 0;"> <!-- Removido o padding superior -->
    <div class="container">
        <h2 style="color: black; font-weight: bold; margin-top: 0;">Cases</h2> <!-- Removido o margin-top -->
        <img src="{{ url_for('static', filename='lajeado.png') }}" alt="lajeado" style="display: block; margin: 20px auto; width: 200px; height: auto;">
        <p style="font-size: 1.2em;">Em 2023, a avalia.se firmou uma parceria acadêmica com o Município de Lajeado com a intenção de conhecer melhor a realidade do município no que se refere a avaliação de imóveis e a partir daí propor soluções.</p>
        <p style="font-size: 1.2em;">Lajeado, município do Vale do Taquari, possui uma área 91.231 km² e uma população de aproximadamente 90 mil habitantes. Em relação ao Produto Interno Bruto (PIB), Lajeado tem uma projeção de crescimento de 11% para 2024, o que é maior do que a média nacional de 2%.</p>
        
        <div class="servicos-columns" style="display: flex; justify-content: space-between; gap: 20px;">
            <!-- Diagnóstico -->
            <div class="servico-item" style="background-color: #d3d3d3; padding: 20px; border-radius: 0; flex: 1;">
                <strong style="font-size: 1.3em;">Diagnóstico</strong>
                <p style="font-size: 1.2em;">Poucos técnicos capacitados</p>
                <p style="font-size: 1.2em;">Dificuldade em manter os bancos de dados atualizados</p>
                <p style="font-size: 1.2em;">Dificuldades na produzir modelos estatísticos</p>
                <p style="font-size: 1.2em;">Tempo excessivo para elaboração de um laudo</p>
            </div>

            <!-- Soluções -->
            <div class="servico-item" style="background-color: #d3d3d3; padding: 20px; border-radius: 0; flex: 1;">
                <strong style="font-size: 1.3em;">Soluções</strong>
                <p style="font-size: 1.2em;">Fornecimento de dados de mercado atualizados e geolocalizados</p>
                <p style="font-size: 1.2em;">Criação de variáveis explicativas (superfície de renda IBGE pelo processo de krigagem)</p>
                <!-- Adicione a imagem da krigagem aqui -->           
                <p style="font-size: 1.2em;">Disponibilização de aplicativos de cálculo (Evolutivo, Regressão Linear e Fatores)</p>
            </div>

            <!-- Resultados -->
            <div class="servico-item" style="background-color: #d3d3d3; padding: 20px; border-radius: 0; flex: 1;">
                <strong style="font-size: 1.3em;">Resultados</strong>
                <p style="font-size: 1.2em;">Redução de 45% no tempo de elaboração das avaliações</p>
                <p style="font-size: 1.2em;">Estudo demonstrando uma redução de custo mensal na ordem de 60% com comissões de servidores para avaliações para fins patrimoniais</p>
            </div>
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
