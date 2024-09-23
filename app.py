from flask import Flask, render_template_string, url_for
import threading

# Criação do aplicativo Flask
app = Flask(__name__)

# Template HTML da landing page com o menu fixo e scroll para seções
html_template = """
<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Landing Page com Menu de Topo</title>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
    body {
        font-family: 'Quicksand', sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f8f9fa;
        scroll-behavior: smooth;
        position: relative; /* Necessário para o overlay */
        color: #000000; /* Define o texto geral como preto */
    }
    body::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url('{{ url_for('static', filename='cidade.png') }}'); /* Imagem de fundo */
        background-size: cover; /* Ajusta o tamanho da imagem para cobrir toda a área */
        background-position: center; /* Centraliza a imagem */
        background-attachment: fixed; /* Mantém a imagem fixa */
        opacity: 0.15; /* Transparência de 85% */
        z-index: -1; /* Coloca a imagem atrás do conteúdo */
      }
      .topnav {
        overflow: hidden;
        background-color: #000000;
        display: flex;
        align-items: center;
        justify-content: center;
        position: fixed; /* Torna o menu fixo */
        top: 0;
        width: 100%; /* Ocupa toda a largura da tela */
        height: 80px;
        z-index: 1000; /* Mantém o menu acima do restante do conteúdo */
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
        color: white; /* Cor das fontes do menu */
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
        font-size: 18px;
      }
      .topnav a:hover {
        background-color: #495057;
      }
      .main-content {
        padding: 20px;
        margin-top: 100px; /* Garante que o conteúdo não fique escondido atrás do menu */
      }
      h1 {
        color: #000000; /* Define os títulos como pretos */
        font-weight: 500;
        text-align: center;
      }
      p, label {
        color: #000000; /* Define os parágrafos e labels como pretos */
        font-weight: 500;
        text-align: justify;
        margin-bottom: 15px;
      }
      .container {
        max-width: 800px;
        margin: auto;
        padding: 100px 0; /* Adiciona espaço ao redor de cada seção */
      }
    .watermark {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: auto;
        opacity: 0.05;
        z-index: -1;
        background-attachment: fixed; /* Torna a imagem de fundo fixa */
      }
      .app-buttons {
        display: flex;
        justify-content: space-around;
        margin-top: 40px;
      }
    .app-button {
      text-align: center;
      padding: 20px;
      border-radius: 10px;
      background-color: #000000; /* Preto para o fundo do botão */
      color: white;
      text-decoration: none;
      width: 200px;
      transition: background-color 0.3s;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }

    .app-button:hover {
      background-color: #333333; /* Cinza escuro ao passar o mouse */
    }

    .app-icon {
      width: 50px;
      height: 50px;
      margin-bottom: 10px;
      stroke: #FFD700; /* Cor amarelo ouro para o ícone */
    }
      }
      .home-content {
        font-size: 18px; /* Reduz o tamanho da fonte para a seção Home */
      }
      .sobre-content {
        font-size: 20px; /* Aumenta o tamanho da fonte para 20px */
      }
       /* Alterar a cor dos links para amarelo ouro */
    a {
        color: #CC9900; /* Amarelo ouro */
        text-decoration: none; /* Remove o sublinhado dos links */
    }
    
    a:hover {
        color: #FFD700; /* Mantém a cor amarelo ouro ao passar o mouse */
        text-decoration: underline; /* Opcional, adicionar sublinhado ao passar o mouse */
    }
    </style>
  </head>
  <body>

    <!-- Menu de topo -->
    <div class="topnav">
      <img src="{{ url_for('static', filename='avalia_b.png') }}" alt="Logo" class="logo">
      <a href="#inicio">Início</a>
      <a href="#contexto">Contexto</a>
      <a href="#processo">Processo avaliatório</a>
      <a href="#solucao">Solução</a>
      <a href="#aplicativos">Aplicativos</a>
      <a href="#municipios">Municípios</a>
      <a href="#servicos">Serviços</a>
      <a href="#contato">Contato</a>
    </div>

<!-- Conteúdo principal -->
<div class="main-content">
    <div id="inicio" class="container início-content">
        <img src="{{ url_for('static', filename='avalia.png') }}" alt="Logo Avalia" style="display: block; margin: 0 auto 10px auto; width: 400px; height: auto;"> <!-- Ajuste na margem inferior -->
        <h2>Sobre o avalia.se</h2>
        <p>O avalia.se é uma empresa de tecnologia e serviços para avaliação de bens.</p>
        <p>Somos obcecados por entender o mercado imobiliário e existimos para tornar os municípios responsivos na avaliação de imóveis.</p>
        <p>Buscamos agilizar as avaliações de imóveis nos municípios, por meio da expertise técnica e da tecnologia, visando beneficiar tanto às prefeituras quanto aos contribuintes.</p>
        <p>Para isso, contamos com profissionais com vasto conhecimento de avaliações e de serviço público, que valorizam acima de tudo o rigor técnico, o conhecimento do mercado e a imparcialidade.</p>
        <p>O mais importante para o avalia.se é o “valor do seu bem”.<p>
    <h2>Sobre a Engenharia de Avaliações</h2>
        <p>"A Engenharia de Avaliações é uma área interdisciplinar que combina conhecimentos de engenharia, arquitetura e ciências sociais, exatas e naturais para determinar o valor de bens imóveis, direitos associados e custos de reprodução. Essencial para o mercado imobiliário, essa especialidade serve a uma ampla gama de agentes, incluindo imobiliárias, bancos, compradores, vendedores, seguradoras, o judiciário, fundos de pensão, incorporadoras, construtoras, investidores e governos locais. (Dantas, 2012)."</p>
        
    </div>
    <div id="contexto" class="container contexto-content">
      <h2>Contexto</h2>
      <ul>
      <li>Todos os municípios precisam avaliar imóveis para os mais diversos fins.</li>
      <li>O processo de avaliação de um bem é complexo e normatizado (NBR 14.653 – partes I e II).</li>
      <li>A tecnologia traz soluções, mas também desafios, tais como a abundância de informações que precisam ser organizadas e a necessidade de capacitação tecnológica permanente.</li>
      </ul>
      <h2>Problemas que muitos municípios enfrentam</h2>
      <ul>
      <li>Muita demanda.</li>
      <li>Poucos profissionais com capacitação específica na área.</li>
      <li>Poucos recursos (sistemas).</li>
      <li>Dificuldade de manter um banco de dados atualizado.</li>
      <li>Necessidade de utilizar diversos sistemas não integrados.</li>
      </ul>
      
      <h2>Algumas consequências</h2>
      <ul>
      <li>Plantas de valores desatualizadas geram renúncia de receita.</li>
      <li>Pagamento de indenizações com valores injustos geram obras paradas e processos judiciais.</li>
      <li>Aquisições ou aluguéis de imóveis com valores superestimados geram desperdício do dinheiro público.</li>
      <li>Desapropriar ofertando pouco, cobrar impostos (Itbi ou Iptu) cobrando muito, afeta a percepção de transparência.</li>
      </ul>
      
    <!-- Processo -->
     <div id="processo" class="container processo-content">
       <h2>Processo Avaliatório - O que é?</h2>
       <p>De forma simplificada, são as etapas pelas quais o avaliador deve passar para produzir uma avaliação, conforme a Norma.</p>
       <ul>
         <li><strong>ABNT NBR 14653-1:2001</strong> – Avaliação de bens – Parte 1: Procedimentos gerais - Estabelece os princípios e procedimentos gerais para a avaliação de bens, sendo aplicável a todos os tipos de bens e finalidades.</li>
         <li><strong>ABNT NBR 14653-2:2011</strong> – Avaliação de bens – Parte 2: Imóveis urbanos - Foca nos critérios e métodos específicos para avaliação de imóveis urbanos.</li>
         <li><strong>ABNT NBR 14653-3:2004</strong> – Avaliação de bens – Parte 3: Imóveis rurais - Define os procedimentos para avaliação de imóveis rurais, abordando aspectos como a terra, benfeitorias e componentes relacionados à atividade rural.</li>
       </ul>
       <img src="{{ url_for('static', filename='processo.png') }}" alt="processo" style="display: block; margin: 20px auto; width: 900px; height: auto;">
       <p>O fluxo do processo avaliatório necessita uma série de sistemas que normalmente não são integrados.</p>
       <img src="{{ url_for('static', filename='sistemas.png') }}" alt="sistemas" style="display: block; margin: 20px auto; width: 900px; height: auto;">
     </div>
 
    <!-- Solução -->
    <div id="solucao" class="container solucao-content">
      <h2>Solução</h2>
      <p>Queremos proporcionar aos municípios uma solução que facilite a tomada de decisões e o cumprimento de normas legais, maximizando a transparência no processo de avaliação imobiliária.</p>
      <p>Nossas qualidades são a “agilidade” no processo, a “acurácia” nos resultados e a “atualização” permanente das soluções. Assim, nossa proposta é minimizar a subjetividade, a imprecisão e a morosidade nos processos de avaliações de imóveis.</p>
      <p>Como diferencial, a plataforma conta com recursos de inteligência artificial e tem como objetivo contemplar as etapas do processo avaliatório, desde a coleta de dados até a elaboração do laudo técnico, tornando-o ágil e assertivo.</p>

    </div>
      <div id="aplicativos" class="container">
        <h2>Aplicativos</h2>
        <li>Dashboard Geospacial: dados de mercado, variáveis e análise explorastória.</li>
        <li>Regressão Linear: Aplicativo elaborado a partir do Método Comparativo Direto de Dados de Mercado (NBR 14653-2:2011), cujo tratamento dos dados é feito pelo método científico (Inferência estatística por meio de Regressão Linear).</li>
        <li>Poucos recursos (sistemas).</li>
        <li>Dificuldade de manter um banco de dados atualizado.</li>
        <div class="app-buttons" style="display: flex; flex-wrap: wrap; gap: 10px;">
          <a href="#dashboard" class="app-button" style="flex: 1 1 calc(20% - 10px);">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="app-icon">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M2 12h20M12 2a15.3 15.3 0 0 1 0 20M12 2a15.3 15.3 15.3 0 0 0 0 20"></path>
            </svg>
            Dashboard Geoespacial
          </a>

          <a href="#regressao" class="app-button" style="flex: 1 1 calc(20% - 10px);">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="app-icon">
              <line x1="3" y1="21" x2="21" y2="21"></line>
              <line x1="3" y1="21" x2="3" y2="3"></line>
              <circle cx="7" cy="17" r="1"></circle>
              <circle cx="13" cy="10" r="1"></circle>
              <circle cx="19" cy="6" r="1"></circle>
              <line x1="3" y1="19" x2="19" y2="6"></line>
            </svg>
            Regressão Linear
          </a>
         <a href="#evolutivo" class="app-button" style="flex: 1 1 calc(20% - 10px);">
           <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="app-icon">
            <!-- Desenho simplificado do edifício com teto reto -->
            <polyline points="6,22 6,8 18,8 18,22"></polyline>
            <!-- Linha do chão -->
            <line x1="4" y1="22" x2="20" y2="22"></line>
            <!-- Janelas do edifício -->
            <line x1="9" y1="10" x2="9" y2="10"></line>
            <line x1="9" y1="14" x2="9" y2="14"></line>
            <line x1="9" y1="18" x2="9" y2="18"></line>
            <line x1="15" y1="10" x2="15" y2="10"></line>
            <line x1="15" y1="14" x2="15" y2="14"></line>
            <line x1="15" y1="18" x2="15" y2="18"></line>
           </svg>
           Método Evolutivo
         </a>
          <a href="#bensmoveis" class="app-button" style="flex: 1 1 calc(20% - 10px);">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="app-icon">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
              <line x1="8" y1="21" x2="16" y2="21"></line>
              <line x1="12" y1="17" x2="12" y2="21"></line>
            </svg>
            Bens Móveis
          </a>
        </div>
      </div>
     <!-- Municípios -->
      <div id="municipios" class="container municipios-content">
        <h2>Municípios</h2>
        <p><strong><strong>Prefeitura Municipal de Lajeado<strong></p>
        <img src="{{ url_for('static', filename='lajeado.png') }}" alt="lajeado" style="display: block; margin: 20px auto; width: 200px; height: auto;">
        <p>Em 2023, o avalia.se firmou uma parceria academica com o Município de Lajeado com a intenção de conhecer melhor a realidade do município no que se refere a avaliação de imóveis e propor soluções.</p>
        <p>Inicialmente, foi feita uma entrevista aberta com o Eng. Franki Bersh, responsável pela avaliações do município.<p>
        <p>A partir do diagnóstico, foram disponibilizados os seguintes recursos ao município:<p>
        <li>Dados de mercado atualizados e geolocalizados.</li>
        <li>Variável renda IBGE por meio de uma superfície (processo de krigagem).</li>
        <li>Aplicativos de cálculo.</li>
        
        <p>Resultados:</p>
         <ul>
          <li><strong><em>Comparando o tempo total empregado na elaboração de algumas avaliações, utilizando os aplicativos de avaliações, scrapping de dados de mercado e variável de localização elaborada com interpolação da Renda Bairro fornecida pelo IBGE, com avaliações similares feitas anteriormente sem estas ferramentas, estimo que o tempo médio por laudo reduziu aproximadamente 45% (quarenta e cinco por cento).</em></strong></li>
         </ul>
          <p style="text-align: right;"><strong><em>Eng. Franki Bersh (Responsável pelas avaliações no Município de Lajeado/RS).</em></strong></p> 
      </div> 
      
     <!-- Serviços -->
     <div id="servicos" class="container servicos-content">      
       <h2>Consultoria</h2>
       <p style="margin-bottom: 20px;">Oferecemos uma consultoria especializada para ajudar os municípios a otimizar seus processos de avaliação de imóveis. Além dos aplicativos, disponibilizamos os serviços abaixo com o objetivo de proporcionar uma gestão completa das avaliações, garantindo eficiência, precisão e transparência em todas as etapas do processo.</p>
       <ul>
         <li style="margin-bottom: 20px;"><strong>Gestão das Avaliações:</strong> Organização sistemática de todo o processo de avaliação, desde o cadastro até a geração de laudos técnicos. Garantimos que cada etapa seja devidamente documentada e arquivada.</li>
         <li style="margin-bottom: 20px;"><strong>Organização de Nomes de Modelos e Laudos:</strong> Implementamos um sistema de padronização para facilitar a identificação de modelos e laudos, permitindo uma busca mais ágil e eficiente, além de reduzir erros na gestão dos documentos.</li>
         <li style="margin-bottom: 20px;"><strong>Catálogo de Modelos por Região:</strong> Desenvolvemos um catálogo com os modelos de avaliação segmentados por região geográfica, otimizando a aplicação das metodologias mais adequadas às especificidades locais.</li>
         <li style="margin-bottom: 20px;"><strong>Criação de Modelos de Machine Learning:</strong> Nossa equipe de especialistas elabora modelos preditivos utilizando técnicas avançadas de Machine Learning, com o objetivo de automatizar e aprimorar a precisão das avaliações de imóveis.</li>
         <li style="margin-bottom: 20px;"><strong>Integração com o Cadastro de Imóveis:</strong> Facilitamos a integração dos nossos modelos e soluções com o sistema de cadastro de imóveis do município, permitindo um fluxo contínuo e eficiente de informações, reduzindo a necessidade de atualizações manuais.</li>
         <li style="margin-bottom: 20px;"><strong>Capacitação e Treinamento:</strong> Oferecemos capacitação técnica contínua para as equipes municipais, garantindo que estejam sempre atualizadas com as melhores práticas e ferramentas disponíveis no mercado de avaliações imobiliárias.</li>
       </ul>
     </div>
     
     <!-- Contato -->
     <div id="contato" class="container">
      <h2>Entre em contato conosco</h2>
        <p><strong>Email:</strong> <a href="mailto:ai.avalia.se@gmail.com">ai.avalia.se@gmail.com</a></p>
        <p><strong>Celular:</strong> <a href="tel:+5551981776636">+55 (51) 98177-6636</a></p>
        
        <h2>Envie-nos uma mensagem</h2>
        <form action="mailto:ai.avalia.se@gmail.com" method="post" enctype="text/plain">
            <label for="nome">Nome:</label>
            <input type="text" id="nome" name="nome" required style="width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px; border: 1px solid #ccc;">
            
            <label for="email">Seu Email:</label>
            <input type="email" id="email" name="email" required style="width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px; border: 1px solid #ccc;">
            
            <label for="mensagem">Mensagem:</label>
            <textarea id="mensagem" name="mensagem" rows="5" required style="width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px; border: 1px solid #ccc;"></textarea>
            
            <button type="submit" style="padding: 10px 20px; background-color: #6c757d; color: white; border: none; border-radius: 5px; cursor: pointer;">Enviar</button>
        </form>
      </div>
    </div>
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
