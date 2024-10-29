from flask import Flask, render_template_string

# Criação da aplicação Flask
app = Flask(__name__)

# HTML Template como string
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>avalia.se - o valor do seu bem</title>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="icon" href="/static/icon.png" type="image/png">
    <style>
        /* RESET BÁSICO */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Quicksand', sans-serif;
            line-height: 1.6;
            scroll-behavior: smooth;
        }

        /* ESTILO MENU DE TOPO */
        .top-nav {
            background-color: #000;
            color: #fff;
            padding: 8px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.4); /* Sombra leve */
        }

        .top-nav .logo h1 {
            font-size: 30px;
            color: #fff;
            cursor: pointer;
        }

        .top-nav .logo h1 .highlight {
            color: #FFC000; /* Amarelo aplicado ao "ia" */
        }

        .top-nav .menu {
            list-style-type: none;
            display: flex;
        }

        .top-nav .menu li {
            margin-left: 20px;
        }

        .top-nav .menu li a {
            color: #fff;
            text-decoration: none;
            font-size: 14px;
            transition: color 0.3s ease;
        }

        .top-nav .menu li a:hover {
            color: #ddd;
        }

        /* ESTILO MENU HAMBRUGUER (escondido em telas grandes) */
        .hamburger {
            display: none;
            font-size: 30px;
            cursor: pointer;
            color: #fff;
        }

        /* Responsividade: ajuste do menu para telas menores */
        @media (max-width: 768px) {
            .top-nav .menu {
                display: none;
                flex-direction: column;
                width: 100%;
                background-color: #000;
                position: absolute;
                top: 60px;
                left: 0;
            }

            .top-nav .menu.active {
                display: flex;
            }

            .hamburger {
                display: block; /* O ícone hamburguer aparece em telas pequenas */
                position: absolute;
                right: 20px; /* Alinha à direita */
                top: 15px; /* Alinha verticalmente */
            }

            .top-nav .menu li {
                margin: 10px 0;
                text-align: center;
            }
        }

        /* Ajuste para o estilo genérico dos containers */
        .container {
            padding: 100px 20px; /* Mantém o padding */
            text-align: center;
            display: flex;
            flex-direction: column; /* Empilha os elementos verticalmente */
        }
        
        
        /* ESTILO PARA A SEÇÃO AVALIA.SE */
        #avalia-se {
            position: relative;
            height: 100vh; /* A seção ocupará a altura total da janela */
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #FFFFFF; /* Cor de fundo branco */
            color: #000; /* Definindo o texto como preto */
        }

        #avalia-se .typewriter-text {
            font-size: 48px;
            font-weight: bold;
            color: #000; /* Alterando a cor do texto para preto */
            white-space: normal;
            text-align: center;
            margin-left: 10vw;
            margin-right: 10vw;
            line-height: 1.2;
            border-right: 6px solid #FFC000;
            animation: blinkCursor 0.7s steps(40) infinite normal;
            position: relative; /* Garante que o texto esteja acima do fundo */
        }


        /* ESTILO PARA O CONTAINER INÍCIO */
        /* ESTILO PARA A IMAGEM */
        #inicio {
            display: flex;
            flex-direction: column;
            width: 100%;
            height: 100vh; /* O contêiner ocupa toda a altura da janela */
            position: relative; /* Adiciona posição relativa para conter o texto sobre a imagem */
        }

        #inicio .image-section {
            background: url('/static/poa.jpg') no-repeat center center;
            background-size: cover;
            width: 100%;
            height: 75vh; /* Agora ocupa 80% da altura da tela */
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        #inicio .image-section .overlay-text {
            color: #fff;
            font-size: 2vw; /* Ajusta o tamanho da fonte com base na largura da tela */
            font-weight: bold;
            text-align: center; /* Centraliza o texto */
            white-space: normal; /* Permite quebras de linha */
            position: absolute;
            padding: 20px; /* Adiciona um padding para evitar que o texto encoste nas bordas */
            max-width: 80%; /* Limita a largura máxima do texto para evitar que se estenda demais */
            line-height: 1.3; /* Ajusta o espaçamento entre linhas */
        }

        #inicio .image-section .overlay-text p {
            margin: 0;
            line-height: 1.2; /* Mantém uma altura de linha menor */
        }
        
        @media (max-width: 768px) {
            #inicio .image-section .overlay-text {
                font-size: 5vw; /* Aumenta o tamanho da fonte em dispositivos menores */
                padding: 10px; /* Reduz o padding em dispositivos menores */
                max-width: 90%; /* Aumenta a largura máxima do texto para ocupar mais da tela */
            }
        }

        /* ESTILO PARA A BLACK SECTION */
        #inicio .black-section {
            background-color: #000;
            color: #fff;
            width: 100%;
            height: 25vh; /* Agora ocupa 20% da altura da tela */
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 50px; /* Espaçamento lateral */
        }

        #inicio .black-section .text-item {
            color: #FFC000; /* Amarelo ouro */
            font-size: 1.8rem; /* Menor tamanho de fonte */
            font-weight: bold;
            text-align: center;
            margin-top: 15px; /* Aumenta o espaço antes de cada bloco de título */
            margin-bottom: 15px; /* Aumenta o espaço depois de cada bloco de título */
        }

        .black-section .sub-text {
            color: #fff;
            font-size: 1.0rem; /* Menor tamanho de fonte */
            font-weight: normal;
            text-align: center;
            margin-top: 5px; /* Ajuste o espaçamento entre o título e o subtítulo */
            margin-bottom: 0; /* Remove espaço extra abaixo da frase */
        }

        @media (min-width: 769px) and (max-width: 1024px) {
            #inicio .black-section {
                height: auto; /* Ajusta automaticamente a altura com base no conteúdo */
                padding: 20px 0; /* Adiciona um pouco de padding */
                flex-direction: column; /* Itens empilhados em coluna */
                justify-content: center;
            }

            #inicio .black-section .text-item {
                margin: 30px 0; /* Aumenta o espaço entre os blocos de texto */
                text-align: center;
            }
        }

        @media (max-width: 768px) {
            #inicio .black-section {
                height: auto;
                padding: 10px 0;
                flex-direction: column;
                justify-content: center;
            }

            #inicio .black-section .text-item {
                width: 100%; /* Garante que os itens ocupem toda a linha */
                margin: 20px 0; /* Ajuste o espaçamento entre os blocos de texto */
                text-align: center;
                position: relative;
            }

            #inicio .black-section .text-item::after {
                content: ""; /* Adiciona um espaço fictício (linha invisível) */
                display: block;
                height: 2px; /* Altura da linha invisível */
                margin: 20px 0; /* Espaçamento entre o fim de um bloco e o próximo título */
                width: 50%; /* Largura da linha fictícia */
                background-color: transparent; /* A linha é invisível */
            }

            .black-section .sub-text {
                margin-top: 5px; /* Espaçamento entre o título e a frase */
                margin-bottom: 0;
            }
        }


        /* ESTILO PARA O CONTAINER CENÁRIO */
        /* Container com imagem de fundo e overlay */
        #cenario {
            position: relative;
            padding: 20px 20px;
            text-align: center;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 30vh;
            margin: 20px 10px;
            overflow: hidden;
        }

        /* Overlay para clarear a imagem de fundo */
        #cenario::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('/static/city.png') no-repeat center center;
            background-size: cover;
            z-index: -1;
            opacity: 0.1; /* Controle de opacidade */
            filter: brightness(1.5); /* Opcional: pode ajustar o brilho da imagem */
        }

        /* Para a frase span Cenário */
        .cenario-label {
            display: block; /* Exibe a palavra como um bloco separado */
            color: #C49A00; /* Amarelo ouro mais escuro */
            font-size: 20px; /* Ajuste o tamanho conforme necessário */
            font-weight: bold; /* Deixa o texto em negrito */
            margin-bottom: 10px; /* Espaço entre o "cenário" e a frase abaixo */
            text-align: center; /* Centraliza o texto */
        }


        /* Para a frase span Censo */
        .censo-label {
            display: block; /* Exibe a palavra como um bloco separado */
            color: #C49A00; /* Amarelo ouro mais escuro */
            font-size: 20px; /* Ajuste o tamanho conforme necessário */
            font-weight: bold; /* Deixa o texto em negrito */
            margin-bottom: 10px; /* Espaço entre o "cenário" e a frase abaixo */
            text-align: center;
        }


        /* Estilo do carrossel */
        #cenario .carousel {
            width: 50%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
            background-color: #fff;
        }

        #cenario .carousel .frase {
            padding: 20px; /* Reduz o padding */
            color: #000;
            font-size: 1.2rem; /* Diminui o tamanho da fonte */
            font-weight: bold;
            line-height: 1.2; /* Reduz o espaçamento entre linhas */
            text-align: center;
            opacity: 0;
            transition: opacity 0.5s ease-in-out;
            position: absolute;
        }

        #cenario .carousel .active {
            opacity: 1;
        }

        /* Exibir as setas de navegação */
        #cenario .carousel .prev,
        #cenario .carousel .next {
            cursor: pointer;
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background-color: transparent;
            color: #000;
            padding: 10px;
            font-size: 20px; /* Reduz o tamanho das setas */
        }

        #cenario .carousel .prev {
            left: -40px;
        }

        #cenario .carousel .next {
            right: -40px;
        }

         /* Ajustes para telas grandes */
        @media (min-width: 1025px) {
            #cenario {
                height: 50vh; /* Altura ajustada para telas grandes */
            }

            #cenario .carousel .frase {
                font-size: 1.8rem; /* Tamanho da fonte em telas grandes */
            }
        }

        /* Ajustes para notebooks */
        @media (min-width: 769px) and (max-width: 1024px) {
            #cenario {
                height: 45vh; /* Altura ajustada para notebooks */
            }

            #cenario .carousel .frase {
                font-size: 1.6rem; /* Tamanho da fonte ajustado para notebooks */
            }
        }

        /* Ajustes para smartphones */
        @media (max-width: 768px) {
            #cenario {
                height: auto; /* Altura automática para evitar espaços grandes */
                min-height: 30vh; /* Definir uma altura mínima menor em celulares */
            }

            #cenario .carousel .frase {
                font-size: 1.4rem; /* Aumentar o tamanho da fonte para melhor legibilidade */
            }

            #cenario .carousel .prev,
            #cenario .carousel .next {
                font-size: 18px; /* Tamanho das setas ajustado para telas menores */
            }
        }


        /* ESTILO PARA O CONTAINER SERVIÇOS */
        #servicos {
            background-color: #FFC000;
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            gap: 10px;
            height: auto; /* Deixe a altura ser ajustada automaticamente */
            padding-top: 100px; /* Adicione espaçamento para compensar o menu fixo */
        }

        #servicos .servicos-content p {
            font-size: 16px !important; /* Mais específico para os parágrafos */
            line-height: 1.4 !important;
            text-align: justify; /* Justifica o texto */
            color: #000; /* Cor do texto */
        }

        #servicos .servicos-content h3 {
            font-size: 20px; /* Ajuste o tamanho conforme necessário */
            line-height: 1.5; /* Ajusta a altura da linha */
            color: #000; /* Cor do texto */
            font-weight: bold; /* Negrito */
            margin-top: 20px; /* Adiciona espaçamento superior */
            margin-bottom: 10px; /* Espaçamento inferior ajustado */
        }

        /* Estilo atualizado para o texto da seção Serviços (aplicável apenas em telas grandes) */
        #servicos .servicos-content {
            flex: 1;
            text-align: left;
            background-color: #FFC000;
            padding: 20px;
            box-sizing: border-box; /* Inclui o padding dentro da largura total */
        }
        
                /* Estilo do botão de cadastro com fundo preto no container Serviços */
        .register-button-black {
            display: inline-block;
            padding: 10px 20px;
            background-color: #000; /* Fundo preto */
            color: #fff; /* Texto branco */
            text-decoration: none;
            font-weight: bold;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }

        /* Alteração de cor ao passar o mouse */
        .register-button-black:hover {
            background-color: #333; /* Fundo levemente mais claro ao passar o mouse */
        }

        #servicos-carousel {
            flex: 1;
            position: relative;
            overflow: hidden;
            background-color: #FFFFFF;
            padding: 20px; /* Adicione algum padding para evitar que o conteúdo encoste nas bordas */
            box-sizing: border-box; /* Certifique-se de que o padding está dentro das dimensões do contêiner */
            border: 5px solid #FFC000; /* Aqui você define a borda, ajuste a espessura e a cor */
            border-radius: 0px; /* Mantém os cantos retos */
        }

        #servicos-carousel img {
            width: 100%;
            height: auto;
            object-fit: cover;
            object-position: center;
        }

        #servicos-carousel .prev,
        #servicos-carousel .next {
            cursor: pointer;
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background-color: rgba(0, 0, 0, 0.5);
            color: #fff;
            padding: 10px;
            font-size: 20px;
        }

        #servicos-carousel .prev {
            left: 10px;
        }

        #servicos-carousel .next {
            right: 10px;
        }

        /* Ajustes específicos para telas maiores que notebooks */
        @media (min-width: 1440px) {
            #servicos {
                flex-direction: row; /* Divide em colunas em telas grandes */
                justify-content: space-between;
            }

            #servicos .servicos-content {
                width: 40%; /* O texto ocupa 40% da largura */
            }

            #servicos-carousel {
                width: 60%; /* O carrossel ocupa 60% da largura */
            }
        }

        /* Ajustes para telas intermediárias e notebooks */
        @media (min-width: 769px) and (max-width: 1440px) {
            #servicos {
                flex-direction: column; /* Empilha os elementos em coluna */
                align-items: center; /* Centraliza os itens no eixo vertical */
                gap: 20px; /* Espaçamento entre os elementos */
                padding: 40px 20px; /* Ajuste de padding */
            }

            .servicos-content {
                width: 90%; /* O texto agora ocupa 90% da largura */
                text-align: left; /* Mantém o alinhamento à esquerda */
                margin-bottom: 20px; /* Espaçamento inferior */
            }

            #servicos-carousel {
                width: 90%; /* O carrossel ocupa 90% da largura */
                height: auto; /* Ajuste automático da altura do carrossel */
            }
        }

        /* Ajustes de responsividade para celulares */
        @media (max-width: 768px) {
            #servicos {
                flex-direction: column;
                gap: 20px;
                height: auto;
                align-items: center; /* Centraliza o conteúdo */
                padding: 20px 10px; /* Ajuste o padding para evitar espaços laterais */
                padding-top: 120px; /* Espaço extra para evitar corte do título em smartphones */
            }

            .servicos-content {
                width: 100%; /* O texto ocupa 100% da largura disponível */
                padding: 20px 15px; /* Padding lateral reduzido */
                max-width: none; /* Remove o limite de largura para ocupar todo o espaço */
                text-align: justify; /* Justifica o texto para manter uma boa legibilidade */
            }

            #servicos-carousel {
                width: 100%; /* O carrossel ocupa toda a largura */
                padding: 10px 15px; /* Ajuste o padding para evitar espaços laterais */
            }
        }


        /* ESTILO PARA O CONTAINER PLANOS */
        #planos {
            background-color: #FFFFFF;
            color: #000;
            padding: 40px 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            width: 100%;
            margin: 0 auto;
            box-sizing: border-box;
            margin-bottom: 40px; /* Espaço inferior */
            max-height: 80vh; /* Limita a altura para evitar invasão do container Contato */
            overflow-y: auto; /* Adiciona rolagem vertical quando o conteúdo ultrapassa a altura */
        }

        /* Layout Flexível para as Caixas de Plano */
        .planos-container {
            display: flex;
            flex-direction: row;
            gap: 20px;
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            align-items: stretch;
        }

        /* Caixa de cada Plano */
        .plano-box {
            background-color: #b0b0b0;
            padding: 20px;
            border-radius: 8px;
            flex: 1;
            text-align: center;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-sizing: border-box;
            transition: background-color 0.3s ease;
        }

        /* Efeito Amarelo ao Passar o Mouse nos Boxes de Plano */
        .plano-box:hover {
            background-color: #FFC000;
        }

        /* Lista de Benefícios de cada Plano */
        .plano-box ul {
            text-align: left;
            padding-left: 20px;
            list-style-position: inside;
            margin-bottom: 20px;
        }

        /* Preço de cada Plano */
        .plano-preco {
            background-color: rgba(0, 0, 0, 0.7);
            color: #fff;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
            margin-top: auto;
        }

        /* Responsividade para dispositivos móveis */
        @media (max-width: 768px) {
            .planos-container {
                flex-direction: column; /* Empilha as caixas verticalmente */
                align-items: center; /* Centraliza as caixas dentro do container */
            }

            .plano-box {
                width: 90%; /* Define a largura das caixas para ocupar 90% da tela */
                max-width: 400px; /* Define um limite de largura */
                margin: 10px auto; /* Centraliza as caixas horizontalmente */
            }
        }


        /* ESTILO PARA O CONTAINER CONTATOS */
        #contato {
            background-color: #000;
            color: #fff;
            font-size: 16px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 25vh;
        } /* Ajustes para o contêiner de Contato */

        .social-icons {
            display: flex;
            justify-content: center;
            margin-top: 10px;
        }

        .social-icons a {
                margin: 0 10px;
                text-decoration: none;
            }

            .social-icons svg {
                width: 32px;
                height: 32px;
                fill: #fff; /* Cor inicial de preenchimento */
                stroke: #fff; /* Cor inicial da borda */
                transition: fill 0.3s ease, stroke 0.3s ease; /* Transição suave para mudança de cor */
            }

            .social-icons a:hover svg {
                fill: #FFC000; /* Preenchimento amarelo ao passar o mouse */
                stroke: #FFC000; /* Borda amarela ao passar o mouse */
        }
    
        .container h2 {
            font-size: 36px;
            margin-bottom: 20px;
        }

        /* Responsividade */
        @media (max-width: 768px) {
            .top-nav {
                flex-direction: column;
            }

            .top-nav .menu {
                flex-direction: column;
                margin-top: 10px;
            }

            .top-nav .menu li {
                margin: 10px 0;
            }

            /* Responsividade para o contêiner Início */
            #inicio .image-section {
                height: 40vh;
                /* Ajusta a altura para telas menores */
            }

            #inicio .black-section {
                height: 60vh;
                flex-direction: column;
            }

            #inicio .black-section .text-item {
                margin: 10px 0;
            }
        }

         /* ESTILO PARA O AS FRASES DINÂMICAS */
        .typewriter-text {
            font-size: 48px;
            font-weight: bold;
            color: #333;
            white-space: normal;
            /* Permite a quebra de linha */
            word-wrap: break-word;
            overflow: hidden;
            border-right: 6px solid #FFC000;
            /* Cursor amarelo */
            animation: blinkCursor 0.7s steps(40) infinite normal;
            margin-left: 10vw;
            margin-right: 10vw;
            display: inline-block;
            /* Permite que o cursor se mova para a nova linha */
            line-height: 1.2;
            /* Mantém a distância adequada entre as linhas */
        }

        /* Animação para o cursor */
        @keyframes blinkCursor {
            from {
                border-right-color: #000;
            }

            to {
                border-right-color: transparent;
            }
        }
    </style>

    <!-- MENU DE NAVEGAÇÃO FIXO -->
    <nav class="top-nav">
        <div class="logo">
            <h1 id="avalia-link">aval<span class="highlight">ia</span>.se</h1>
        </div>
        <div class="hamburger" onclick="toggleMenu()">☰</div> <!-- Ícone de menu -->

        <ul class="menu" id="menu">
            <li><a href="#inicio">Início</a></li>
            <li><a href="#cenario">Cenário</a></li>
            <li><a href="#servicos">Serviços</a></li>
            <li><a href="#planos">Planos</a></li> <!-- Novo link para Planos -->
            <li><a href="#contato">Contato</a></li>
            <li><a href="#login">Login</a></li>
        </ul>
    </nav>

    <!-- CONTAINERS PARA CADA SEÇÃO -->
    
    <!-- AVALIA.SE -->
    <section id="avalia-se" class="container">
        <p class="typewriter-text" id="dynamic-text"></p>
    </section>

    <section id="inicio">
        <div class="image-section">
            <div class="overlay-text">
                <p>Para uma cidade ser responsiva na avaliação de imóveis,</p>
                <p>é preciso entender as necessidades de todos os envolvidos</p>
            </div>
        </div>
        <div class="black-section">
            <div class="text-item">
                Servidores
                <p class="sub-text">Precisam de atenção às normas e de precisão nos resultados.</p>
            </div>
            <div class="text-item">
                Gestores
                <p class="sub-text">Buscam agilidade nos processos e a aprovação dos cidadãos.</p>
            </div>
            <div class="text-item">
                Cidadãos
                <p class="sub-text">Demandam respostas rápidas e justas às suas necessidades.</p>
            </div>
        </div>
    </section>
    
    <!-- CONTAINER CENÁRIO COM O CARROSSEL -->
    <section id="cenario">
        <div class="carousel">
            <div class="frase active">
                <span class="cenario-label">CENÁRIO</span>
                <p>AVALIAÇÃO DE IMÓVEIS NOS MUNICÍPIOS BRASILEIROS.</p>
            </div>
            
            <div class="frase">
                <p>No Brasil, existem aproximadamente 5.200 municípios considerados pequenos ou médios, ou seja, 94% do total. Estes municípios possuem diversas demandas relacionadas à avaliação de imóveis.</p>
                <span class="censo-label">CENSO 2022</span>
            </div>

            <div class="frase">
                <p>A avaliação de imóveis é uma atividade complexa e regulamentada, presente em vários processos, como plantas de valores, desapropriações, aquisições, locações, entre outros.</p>
            </div>

            <div class="frase">
                <p>A alta demanda, a falta de profissionais especializados e de sistemas adequados, além da dificuldade em manter um banco de dados atualizado, são alguns dos desafios para a gestão municipal.</p>
            </div>

            <div class="frase">
                <p>Valores imprecisos geram prejuízos financeiros, processos judiciais, comprometem a arrecadação municipal e impactam negativamente a imagem da administração pública diante da sociedade.</p>
            </div>

            <div class="frase">
                <p>MAS NÓS PODEMOS AJUDAR...</p>
            </div>

            <span class="prev" onclick="showPrev()">&#10094;</span>
            <span class="next" onclick="showNext()">&#10095;</span>
        </div>
    </section>

    <!-- JavaScript para controle do carrossel -->
    <script>
        let currentIndex = 0;
        const frases = document.querySelectorAll('.carousel .frase');

        function showFrase(index) {
            frases.forEach((frase, i) => {
                frase.classList.remove('active');
                if (i === index) {
                    frase.classList.add('active');
                }
            });
        }

        function showNext() {
            currentIndex = (currentIndex + 1) % frases.length;
            showFrase(currentIndex);
        }

        function showPrev() {
            currentIndex = (currentIndex - 1 + frases.length) % frases.length;
            showFrase(currentIndex);
        }
    </script>

    <!-- SERVIÇOS -->
    <section id="servicos" class="container">
        <div class="servicos-content">
            <h2>Nossos serviços</h2>
            <p>
                Desenvolvemos soluções inovadoras para profissionais do setor. Utilizamos a inteligência artificial para agilizar os processos, acurar os resultados e garantir que nossas soluções e bases de dados estejam sempre atualizadas e alinhadas às necessidades do mercado.
            </p>
            <h3>Soluções para avaliações</h3>
            <p>
                Aplicativos que contemplam todas as etapas do processo avaliatório — da coleta de dados à geração do laudo técnico.
            </p>
            
            <h3>Soluções para avaliações em massa</h3>
            <p>
                Elaboração de modelos avançados, utilizando as técnicas mais modernas da ciência de dados.
            </p>
            
            <h3>Treinamento e capacitação</h3>
            <p>
                Oferecemos capacitação para as equipes municipais, garantindo que estejam sempre atualizadas com as melhores práticas e ferramentas disponíveis no mercado de avaliações imobiliárias.
            </p>
            <!-- Botão de Cadastro com caixinha preta -->
            <div style="text-align: center; margin-top: 20px;">
                <a href="#login" class="register-button-black">
                    Clique aqui e cadastre-se
                </a>
            </div>
        </div>
        
        <!-- Carrossel de imagens -->
        <div id="servicos-carousel">
            <img src="/static/1.png" alt="Imagem 1" class="carousel-img">
            <img src="/static/2.png" alt="Imagem 2" class="carousel-img">
            <img src="/static/3.png" alt="Imagem 3" class="carousel-img">
            <img src="/static/4.jpg" alt="Imagem 4" class="carousel-img">
            <img src="/static/5.jpg" alt="Imagem 5" class="carousel-img">
            <span class="prev" onclick="showPrevImage()">&#10094;</span>
            <span class="next" onclick="showNextImage()">&#10095;</span>
        </div>
    </section>

    <!-- JavaScript para o carrossel de imagens com transição manual -->
    <script>
        const images = document.querySelectorAll('#servicos-carousel img');
        let currentImageIndex = 0;

        function showImage(index) {
            images.forEach((img, i) => {
                img.style.display = (i === index) ? 'block' : 'none';
            });
        }

        function showNextImage() {
            currentImageIndex = (currentImageIndex + 1) % images.length;
            showImage(currentImageIndex);
        }

        function showPrevImage() {
            currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
            showImage(currentImageIndex);
        }

        // Mostrar a primeira imagem ao carregar a página
        showImage(currentImageIndex);

        // Remova ou comente esta linha para desativar a transição automática
        // setInterval(showNextImage, intervalTime);  // Muda de imagem a cada intervalo definido
    </script>


    <!-- CONTAINER PLANOS -->
    <section id="planos" class="container plano">
        <h2 style="text-align: center; font-size: 36px; margin-bottom: 20px;">Escolha seu plano</h2><!-- Título centralizado -->
        <div class="planos-container">
            <div class="plano-box">
                <h2>Plano Personal</h2>
                <ul>
                    <li>Acesso para 1 usuário</li>
                    <li>100% on-line</li>
                    <li>Acesso à plataforma</li>
                    <li>Acesso aos aplicativos</li>
                    <li>Acesso aos dados de mercado disponíveis na plataforma</li>
                    <li>Chat</li>
                </ul>
                <!-- Valores dos planos -->
                <div class="plano-preco">
                    <p>Mensal: R$ 19,90</p>
                    <p>Anual: R$ 199,90</p>
                </div>
            </div>
            <div class="plano-box">
                <h2>Plano Corporativo</h2>
                <ul>
                    <li>Usuários ilimitados</li>
                    <li>100% on-line</li>
                    <li>Acesso à plataforma</li>
                    <li>Acesso aos aplicativos</li>
                    <li>Dados periodicamente coletados na região solicitada pelo contratante</li>
                    <li>Acesso aos demais dados disponíveis na plataforma</li>
                    <li>Chat</li>
                </ul>
                <!-- Valores dos planos -->
                <div class="plano-preco">
                    <p>Mensal: a partir de R$ 249,90 *</p>
                    <p>Anual: a partir de R$ 2.499,90 *</p>
                    <p>_____________________________</p>
                    <p>* Depende do porte do município (nº de habitantes) e da necessidade de dados</p>
                </div>
            </div>
            <div class="plano-box">
                <h2>On Demand</h2>
                <ul>
                    <li>Coletas específicas de dados</li>
                    <li>Modelos para avaliação em massa</li>
                    <li>Estudos especiais de mercado</li>
                    <li>Consultoria em avaliações</li>
                    <li>Treinamento e capacitação</li>
                </ul>
                <!-- Valores dos planos -->
                <div class="plano-preco">
                    <p>Sob consulta</p>
                    <p>_____________________________</p>
                    <p>Serviços que dependem de uma análise das necessidades do cliente</p>
                </div>
            </div>
        </div>
        <!-- Botão de Cadastro -->
        <div style="text-align: center; margin-top: 20px;">
            <a href="#login" class="register-button" style="padding: 10px 20px; background-color: #FFC000; color: #000; text-decoration: none; font-weight: bold; border-radius: 5px;">
                Clique aqui e cadastre-se (Ganhe o 1º mês grátis)
            </a>
        </div>
    </section>


    <!-- CONTATOS -->
    <section id="contato" class="container">
        <h3>aval<span class="highlight">ia</span>.se</h3>
        <p>e-mail: ai.avalia.se@gmail.com</p>
        <p>Porto Alegre/RS</p>
        <p>Brasil</p>
        
<style>
    .social-icons a {
        margin: 0 10px;
        text-decoration: none;
        transition: fill 0.3s ease; /* Transição suave para a mudança de cor */
    }

    .social-icons svg {
        width: 32px;
        height: 32px;
        fill: #fff; /* Cor inicial dos ícones */
        transition: fill 0.3s ease; /* Transição suave para a mudança de cor */
    }

    .social-icons a:hover svg {
        fill: #FFC000; /* Cor amarela ao passar o mouse */
    }
</style>

        <div class="social-icons">
        <!-- Instagram -->
        <a href="https://instagram.com" target="_blank" title="Instagram">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="#fff" stroke="#fff" stroke-width="2">
                <!-- Borda arredondada externa -->
                <rect width="20" height="20" x="2" y="2" rx="5" ry="5" fill="none"/>
                <!-- Círculo central -->
                <circle cx="12" cy="12" r="3.687" fill="#fff"/>
                <!-- Ponto pequeno no canto superior -->
                <circle cx="17.5" cy="6.5" r="1.5" fill="#fff"/>
            </svg>
        </a>

        <!-- Facebook -->
        <a href="https://facebook.com" target="_blank" title="Facebook">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="32" height="32" fill="#fff">
                <path d="M22.676 0H1.324C.593 0 0 .593 0 1.324v21.352C0 23.407.593 24 1.324 24H12.82v-9.282H9.692V11.08h3.128V8.398c0-3.1 1.891-4.792 4.656-4.792 1.325 0 2.462.099 2.795.143v3.24l-1.918.001c-1.503 0-1.793.715-1.793 1.763v2.31h3.586l-.467 3.638h-3.119V24h6.11C23.407 24 24 23.407 24 22.676V1.324C24 .593 23.407 0 22.676 0z"/>
            </svg>
        </a>

        <!-- LinkedIn -->
        <a href="https://linkedin.com" target="_blank" title="LinkedIn">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="32" height="32" fill="#fff">
                <path d="M22.23 0H1.77C.792 0 0 .774 0 1.73v20.541C0 23.226.792 24 1.77 24h20.46c.978 0 1.77-.774 1.77-1.73V1.73C24 .774 23.208 0 22.23 0zM7.117 20.452H3.577V9h3.54v11.452zM5.347 7.528c-1.133 0-1.927-.793-1.927-1.786 0-.998.8-1.786 1.95-1.786 1.146 0 1.928.788 1.94 1.786 0 .993-.795 1.786-1.94 1.786h-.023zm15.105 12.924h-3.54V14.96c0-1.317-.471-2.216-1.651-2.216-.9 0-1.435.611-1.67 1.2-.086.213-.108.511-.108.807v5.701H9.947S9.99 10.943 9.947 9h3.54v1.563c.47-.73 1.31-1.777 3.187-1.777 2.328 0 4.078 1.518 4.078 4.779v6.888z"/>
            </svg>
        </a>
    </div>


    </section>

    <!-- JavaScript para o efeito de escrita dinâmica -->
    <script>
        const text1 = "A avalia.se é uma empresa de tecnologia e serviços para avaliação de bens.";
        const text2 = "Conhecemos o mercado imobiliário e tornamos responsivos os municípios na avaliação de imóveis.";
        const text3 = "Agilizamos os processos de avaliação por meio da tecnologia.";
        const text4 = "avalia.se - o valor do seu bem";
        let texts = [text1, text2, text3, text4];  // Array de textos
        let index = 0;
        let charIndex = 0;
        let currentText = texts[index];
        let forward = true;

        function typeWriterEffect() {
            const element = document.getElementById('dynamic-text');

            if (forward) {
                element.innerHTML = currentText.slice(0, ++charIndex); // Escreve o texto
                if (charIndex === currentText.length) {
                    forward = false; // Quando o texto completo for escrito, inverte a direção
                    setTimeout(typeWriterEffect, 3000); // Pausa de 3 segundos
                    return;
                }
            } else {
                element.innerHTML = currentText.slice(0, --charIndex); // Apaga o texto
                if (charIndex === 0) {
                    forward = true; // Quando o texto for completamente apagado, volta a escrever
                    index = (index + 1) % texts.length;  // Muda para a próxima frase
                    currentText = texts[index];
                }
            }http://localhost:8888/notebooks/Documents/frontpage_avaliase/avalia.page-responsiva-v2.ipynb#
            setTimeout(typeWriterEffect, 30); // Controla a velocidade de escrita/apagamento
        }

        window.onload = function() {
            typeWriterEffect(); // Inicia o efeito quando a página carregar
        };

        // Função para rolar até a seção "avalia-se"
        document.getElementById('avalia-link').onclick = function() {
            document.getElementById('avalia-se').scrollIntoView({ behavior: 'smooth' });
        };
    </script>
    
    <!-- JavaScript para alternar o menu e rolar para as seções -->
    <script>
        function toggleMenu() {
            const menu = document.getElementById('menu');
            menu.classList.toggle('active');
        }

        // Função para rolar até a seção considerando a altura do menu fixo
        function scrollToSection(sectionId) {
            const element = document.getElementById(sectionId);
            const offset = 60; // altura do menu fixo, ajuste conforme necessário
            const elementPosition = element.getBoundingClientRect().top + window.pageYOffset;

            window.scrollTo({
                top: elementPosition - offset,
                behavior: 'smooth'
            });
        }

        // Configuração dos links de menu para rolar corretamente
        document.querySelectorAll('.menu li a').forEach(link => {
            link.onclick = function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('href').substring(1); // Remove o # do ID
                scrollToSection(targetId);
            };
        });
    </script>


</body>
</html>
'''

# Rota principal que renderiza o HTML
@app.route('/')
def index():
    return render_template_string(html_template)

# Executando o servidor Flask no Jupyter
if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple(app)
