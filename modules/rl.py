import gradio as gr
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import scipy.stats as stats
from joblib import dump
import joblib
import os
import locale

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    # Fallback para uma localidade padrão (ex.: 'C' ou 'en_US.UTF-8')
    locale.setlocale(locale.LC_ALL, 'C')

# Função para carregar a planilha de dados
def carregar_planilha(file):
    try:
        # Carregar o arquivo Excel sem forçar o tipo inicialmente
        df = pd.read_excel(file.name)

        # Garantir que todas as colunas sejam convertidas para float, ignorando erros
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Converte para número, valores inválidos viram NaN

        # Substituir NaN por zero ou outro valor padrão, se necessário
        df.fillna(0, inplace=True)

        # Garantir que os cabeçalhos sejam strings
        df.columns = [str(col) for col in df.columns]

        # Adicionar índice baseado na posição
        df.insert(0, "Dado", range(1, len(df) + 1))

        # Arredondar colunas de tipo float para 4 casas decimais
        for col in df.select_dtypes(include=[float]).columns:
            df[col] = df[col].round(4)

        cabecalhos = list(df.columns)
        return cabecalhos, df
    except Exception as e:
        print(f"Erro ao carregar a planilha: {e}")
        return [], pd.DataFrame()
    
# Função para aplicar a transformação selecionada
def aplicar_transformacao(df, coluna, transformacao):
    try:
        if transformacao == "1/x":
            return 1 / df[coluna].replace(0, np.nan).fillna(0)  # Evitar divisão por zero
        elif transformacao == "ln(x)":
            return np.log(df[coluna].replace(0, np.nan).fillna(0))  # Evitar log de zero
        elif transformacao == "x²":
            return df[coluna] ** 2
        elif transformacao == "exp(x)":
            return np.exp(df[coluna])
        else:
            return df[coluna]  # Sem transformação, retorna a coluna original
    except Exception as e:
        return df[coluna]  # Retorna original em caso de erro   
    
# Função para criar gráficos de dispersão para análise exploratória com transformações
def grafico_dispersao(df, y_coluna, transformacao_y, x_coluna, transformacao_x, dados_out):
    if df.empty or x_coluna not in df.columns or y_coluna not in df.columns:
        return None  # Retornar None se o DataFrame estiver vazio ou as colunas não forem válidas

    # Copiar o DataFrame para manipulação
    df_grafico = df.copy()
    # Convertendo a entrada manual em uma lista de inteiros
    dados_out = [int(num.strip()) for num in dados_out.split(",") if num.strip()]
    # Removendo os outliers dos DataFrames
    df_grafico = df_grafico[~df_grafico["Dado"].isin(dados_out)]
    # Aplicar transformações nas colunas x e y
    x = aplicar_transformacao(df_grafico, x_coluna, transformacao_x)
    y = aplicar_transformacao(df_grafico, y_coluna, transformacao_y)
    # Calcular a linha de tendência
    coef = np.polyfit(x, y, 1)  # Coeficientes da linha de tendência (linear)
    linha_tendencia = np.poly1d(coef)
    y_tendencia = linha_tendencia(x)
    # Calcular resíduos (distância dos pontos à linha de tendência)
    residuos = np.abs(y - y_tendencia)
    # Normalizar os resíduos para aplicar o colormap
    residuos_norm = (residuos - residuos.min()) / (residuos.max() - residuos.min())
    # Calcular o valor de correlação
    correlacao = np.corrcoef(x, y)[0, 1]
    # Criar o gráfico de dispersão com Plotly
    fig = go.Figure()
    # Adicionar os pontos ao gráfico com colormap
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=dict(
            size=8,
            color=residuos_norm,  # Colormap com base nos resíduos
            colorscale='Spectral',  # Escolher o esquema de cores (pode ser ajustado)
            showscale=False,  # Desabilitar a barra de cores
        ),
        text=[f"Índice: {idx}<br>{x_coluna}: {x_val:.2f}<br>{y_coluna}: {y_val:.2f}<br>Resíduo: {resid:.2f}"
              for idx, x_val, y_val, resid in zip(df_grafico["Dado"], x, y, residuos)],  # Informações no tooltip
        hoverinfo="text"
    ))

    # Adicionar a linha de tendência ao gráfico
    fig.add_trace(go.Scatter(
        x=x,
        y=y_tendencia,
        mode='lines',
        line=dict(color='darkred', width=2),  # Linha de tendência com vermelho escuro
    ))

    # Atualizar o layout do gráfico
    fig.update_layout(
        title=f"Gráfico de Dispersão: {x_coluna} vs {y_coluna}<br>Correlação: {correlacao:.2f}",
        xaxis_title=f"{x_coluna} ({transformacao_x})",
        yaxis_title=f"{y_coluna} ({transformacao_y})",
        template="plotly_white",
        showlegend=False
    )

    return fig

# Função para criar boxplot para análise exploratória com transformações
def grafico_boxplot(df, y_coluna, transformacao_y, x_coluna, transformacao_x, dados_out):
    if df.empty or y_coluna not in df.columns:
        return None  # Retorna None se o DataFrame estiver vazio ou as colunas não forem válidas

    # Copiar o DataFrame para manipulação
    df_boxplot = df.copy()

    # Convertendo a entrada manual em uma lista de inteiros
    dados_out = [int(num.strip()) for num in dados_out.split(",") if num.strip()]
    # Removendo os outliers dos DataFrames
    df_boxplot = df_boxplot[~df_boxplot["Dado"].isin(dados_out)]

    # Aplicar transformação na coluna Y
    y = aplicar_transformacao(df_boxplot, y_coluna, transformacao_y)

    # Criar lista de textos personalizados para hover
    hover_text = [
        f"Índice: {idx}<br>{y_coluna}: {y_val:.2f}"
        for idx, y_val in zip(df_boxplot["Dado"], y)
    ]

    # Criar o gráfico de boxplot com Plotly
    fig = go.Figure()

    # Adicionar os dados ao gráfico
    fig.add_trace(go.Box(
        y=y,
        name=y_coluna,
        boxpoints='all',  # Mostra todos os pontos, incluindo outliers
        jitter=0.8,  # Espalhamento horizontal dos pontos
        pointpos=-1.8,  # Posição relativa dos pontos em relação ao boxplot
        marker=dict(
            color='orange',
            size=8
        ),
        line=dict(color='gray'),
        hovertemplate="%{text}",  # Personaliza o hover
        text=hover_text  # Insere a lista de textos no hover
    ))

    # Atualizar o layout do gráfico
    fig.update_layout(
        title=f"Boxplot da Coluna: {y_coluna} ({transformacao_y})",
        yaxis_title=f"{y_coluna} ({transformacao_y})",
        template="plotly_white",
        showlegend=False
    )

    return fig

# Função para atualizar os dropdowns    
def atualizar_dropdowns(cabeçalhos):
    if cabeçalhos:
        # Remover 'Índice' das opções, se não for relevante para as análises
        cabecalhos_sem_indice = [col for col in cabeçalhos if col != "Dado"]
        dropdown_update_x = gr.update(choices=cabecalhos_sem_indice, value=cabecalhos_sem_indice)
        dropdown_update = gr.update(choices=cabecalhos_sem_indice, value=[])
        return [dropdown_update_x] + [dropdown_update] * 4 + [dropdown_update]  # Inclui var_dep
    else:
        dropdown_reset = gr.update(choices=[], value=[])
        return [dropdown_reset] * 5 + [dropdown_reset]  # Inclui var_dep

# Função para criar os cabeçalhos e colocar os limites por variável sem os outliers
def criar_dataframe_cabecalhos(cabecalhos, x, ln_x, exp_x, inv_x, quad_x, dados, dados_out, var_dep):
    if dados.empty:
        return pd.DataFrame(), {}

    # Remover os outliers antes de calcular os limites
    if dados_out:
        dados_out = [int(num.strip()) for num in dados_out.split(",") if num.strip()]
        dados = dados[~dados["Dado"].isin(dados_out)]

    # Criar um dicionário com as seleções
    escalas = {
        col: [escala] for col, escala in zip(
            x + ln_x + exp_x + inv_x + quad_x,
            ["(x)"] * len(x) + ["ln(x)"] * len(ln_x) + ["exp(x)"] * len(exp_x)
            + ["1/(x)"] * len(inv_x) + ["(x)²"] * len(quad_x)
        )
    }

    # Criar o DataFrame base
    df = pd.DataFrame.from_dict(escalas, orient='index', columns=['Escala']).transpose()

    # Reorganizar as colunas para garantir que 'var_dep' seja a primeira
    if var_dep in df.columns:
        cols = [var_dep] + [col for col in df.columns if col != var_dep]
        df = df[cols]

    # Calcular as linhas adicionais (máximo, mínimo, média) com duas casas decimais
    limites = {
        "Máximo": dados.max().round(2),
        "Mínimo": dados.min().round(2),
        "Média": dados.mean().round(2)
    }

    # Adicionar as linhas ao DataFrame
    for label, valores in limites.items():
        linha = {col: valores[col] if col in valores else '' for col in df.columns}
        df = pd.concat([df, pd.DataFrame([linha], index=[label])])

    return df, escalas

# Função para criar DataFrames original, escalado, correlação e outliers
def criar_dataframes(dados, x, ln_x, exp_x, inv_x, quad_x, dados_out, var_dep):
    if dados.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), None

    # Selecionar as colunas escolhidas e incluir "Dado" como identificador
    colunas_escolhidas = x + ln_x + exp_x + inv_x + quad_x
    df_original = dados[["Dado"] + colunas_escolhidas]  # Incluindo "Dado"

    # Aplicar escalas e manter "Dado"
    df_escalado = pd.DataFrame()
    df_escalado["Dado"] = dados["Dado"]  # Preservar "Dado" no escalado

    for col in x:
        df_escalado[col] = dados[col]  # (x)
    for col in ln_x:
        df_escalado[col] = np.log(dados[col].replace(0, np.nan)).fillna(0)  # ln(x), evitando log de zero
    for col in exp_x:
        df_escalado[col] = np.exp(dados[col])  # exp(x)
    for col in inv_x:
        df_escalado[col] = 1 / dados[col].replace(0, np.nan).fillna(0)  # 1/(x), evitando divisão por zero
    for col in quad_x:
        df_escalado[col] = dados[col] ** 2  # (x)²

    # Reorganizar colunas para que var_dep fique como a segunda coluna
    if var_dep in df_original.columns:
        colunas_reorganizadas_original = (
            ["Dado", var_dep] + [col for col in df_original.columns if col not in ["Dado", var_dep]]
        )
        df_original = df_original[colunas_reorganizadas_original]

    if var_dep in df_escalado.columns:
        colunas_reorganizadas_escalado = (
            ["Dado", var_dep] + [col for col in df_escalado.columns if col not in ["Dado", var_dep]]
        )
        df_escalado = df_escalado[colunas_reorganizadas_escalado]

    # Criando o novo DataFrame com a coluna 'variáveis' sem índice
    df_variaveis = pd.DataFrame({'variáveis': df_original.columns})
    df_variaveis.reset_index(drop=True, inplace=True)

    # Verificar se dados_out está em branco
    if not dados_out.strip():
        df_outliers = pd.DataFrame()  # DataFrame vazio para outliers
    else:
        # Convertendo a entrada manual em uma lista de inteiros
        dados_out = [int(num.strip()) for num in dados_out.split(",") if num.strip()]
        # Criando o DataFrame de outliers
        df_outliers = df_original[df_original["Dado"].isin(dados_out)]  # Filtrar com base nos valores de dados_out
        # Removendo os outliers dos DataFrames originais e escalados
        df_original = df_original[~df_original["Dado"].isin(dados_out)]
        df_escalado = df_escalado[~df_escalado["Dado"].isin(dados_out)]
    
    # Criar matriz de correlação
    correlation_matrix = df_escalado.drop(columns=["Dado"]).corr().round(2)  # "Dado" não entra na correlação

    return df_original, df_escalado, df_outliers  # , correlation_matrix

# Função para Regressão Linear
def realizar_regressao(var_dep, dados_transformados, df_original, escalas):
    if isinstance(dados_transformados, pd.DataFrame) and not dados_transformados.empty:
        try:
            import statsmodels.api as sm
            import numpy as np

            if var_dep in dados_transformados.columns:
                # Separando X e y
                y = dados_transformados[var_dep]
                X = dados_transformados.drop(columns=[var_dep, "Dado"])

                # Número de variáveis independentes
                num_variaveis = X.shape[1]

                # Adicionando constante
                X = sm.add_constant(X)

                # Ajustando modelo
                modelo = sm.OLS(y, X).fit()
                
                # Inicializar resultados gerais
                resultados_gerais = ""

                # Estatísticas gerais do modelo
                residuos = modelo.resid
                desvio_padrao_residuos = round(np.std(residuos), 8)
                erro_padronizado = np.round(residuos / desvio_padrao_residuos, 8)
                estatistica_F = round(modelo.fvalue, 8)
                nivel_significancia = round(modelo.f_pvalue, 8)
                r_squared = round(modelo.rsquared, 8)
                r_squared_adjusted = round(modelo.rsquared_adj, 8)
                num_observacoes = int(round(modelo.nobs, 0))
                coef_correlacao = round(np.sqrt(r_squared), 8)

                # Comparação com a curva normal de resíduos
                intervalos = [(-1.00, 1.00), (-1.64, 1.64), (-1.96, 1.96)]
                percentuais = []
                for intervalo in intervalos:
                    min_intervalo, max_intervalo = intervalo
                    count = np.sum((erro_padronizado >= min_intervalo) & (erro_padronizado <= max_intervalo))
                    percentual = round(count / len(erro_padronizado) * 100, 0)
                    percentuais.append(f"{percentual:.0f}%")
                perc_resid = ", ".join(percentuais)

                # Teste Kolmogorov-Smirnov (KS)
                ks_test = sm.stats.diagnostic.kstest_normal(residuos)
                ks_test_formatted = tuple(f"{val:.4f}" for val in ks_test)
                
                import statsmodels.api as sm

                # Teste Kolmogorov-Smirnov (KS)
                ks_test = sm.stats.diagnostic.kstest_normal(residuos)
                ks_test_formatted = tuple(f"{val:.4f}" for val in ks_test)
                
                # Interpretando o resultado
                estatistica_ks, p_valor_ks = ks_test  # Desempacotando os valores
                
                if p_valor_ks > 0.05:
                    ks_interpretacao = "Não há evidências estatísticas suficientes para rejeitar a hipótese nula. Os resíduos podem seguir uma distribuição normal."
                else:
                    ks_interpretacao = "Rejeitamos a hipótese nula. Há evidências estatísticas de que os resíduos não seguem uma distribuição normal."


                # Distância de Cook
                influencia = modelo.get_influence()
                distancia_cook = influencia.cooks_distance[0]

                # Criar DataFrame com resultados por variável
                coeficientes = modelo.params
                erros_padrao = modelo.bse
                t_values = modelo.tvalues
                p_values = modelo.pvalues

                # Adicionar a coluna Escala com base no dicionário de escalas
                escalas_coluna = [escalas[var][0] if var in escalas else "Nenhuma" for var in coeficientes.index]

                resultados_vars = pd.DataFrame({
                    "Variável": coeficientes.index,
                    "Escala": escalas_coluna,  # Adicionando a coluna Escala
                    "Coeficiente": coeficientes.values.round(4),
                    "Erro Padrão": erros_padrao.values.round(4),
                    "t-valor": t_values.values.round(4),
                    "P>|t|": p_values.values.round(4)
                })

                # Expressão da equação do modelo com a variável dependente transformada
                if var_dep in escalas:
                    escala_y = escalas[var_dep][0]  # Obter a escala associada
                    if escala_y == "ln(x)":
                        y_label_transformada = f"ln({var_dep})"
                        ajustar_termo = lambda termo: f"exp({termo})"  # Aplicar exponencial
                    elif escala_y == "1/(x)":
                        y_label_transformada = f"1/({var_dep})"
                        ajustar_termo = lambda termo: f"1/({termo})"  # Aplicar inverso
                    elif escala_y == "(x)²":
                        y_label_transformada = f"({var_dep})²"
                        ajustar_termo = lambda termo: f"sqrt({termo})"  # Aplicar raiz quadrada
                    elif escala_y == "exp(x)":
                        y_label_transformada = f"exp({var_dep})"
                        ajustar_termo = lambda termo: f"ln({termo})"  # Aplicar logaritmo natural
                    else:
                        y_label_transformada = var_dep  # Sem transformação
                        ajustar_termo = lambda termo: termo  # Sem ajuste
                else:
                    y_label_transformada = var_dep  # Sem transformação
                    ajustar_termo = lambda termo: termo  # Sem ajuste

                # Construir os termos da equação
                termos = []
                for var, coef in zip(coeficientes.index, coeficientes.values):
                    if var == 'const':
                        interseção = f"{coef:.4f}"
                    else:
                        if var in escalas:
                            escala_var = escalas[var][0]  # Obter a escala associada
                            if escala_var == "ln(x)":
                                var_label = f"ln({var})"
                            elif escala_var == "1/(x)":
                                var_label = f"1/({var})"
                            elif escala_var == "(x)²":
                                var_label = f"({var})²"
                            elif escala_var == "exp(x)":
                                var_label = f"exp({var})"
                            else:
                                var_label = var  # Sem transformação
                        else:
                            var_label = var  # Sem transformação
                        termos.append(f"{coef:.4f} * {var_label}")

                # Montar a equação com a variável dependente transformada
                lado_direito = interseção + " + " + " + ".join(termos)
                equacao_transformada = f"{y_label_transformada} = {lado_direito}"
                # Montar a equação com a variável dependente na escala direta
                equacao_revertida = f"{var_dep} = {ajustar_termo(lado_direito)}"
                # Substituir pontos por vírgulas nas equações
                equacao_transformada = equacao_transformada.replace('.', ',')
                equacao_revertida = equacao_revertida.replace('.', ',')
                # Adicionar as duas formas da equação aos resultados gerais
                #resultados_gerais += f"\nEquação do modelo (variável dependente transformada): {equacao_transformada}"
                resultados_gerais += f"\nEquação do modelo (variável dependente na escala direta): {equacao_revertida}"

                # Classificar variáveis com base nos p-valores
                def classificar(valor):
                    if valor > 0.3:
                        return "Fora dos critérios"
                    elif valor > 0.2:
                        return "Grau I"
                    elif valor > 0.1:
                        return "Grau II"
                    else:
                        return "Grau III"

                resultados_vars['Classificação'] = resultados_vars['P>|t|'].apply(classificar)

                # Determinar grau único considerando todas as variáveis
                def determinar_grau_unico(classificacoes):
                    if "Fora dos critérios" in classificacoes:
                        return "Fora dos critérios"
                    elif "Grau I" in classificacoes:
                        return "Grau I"
                    elif "Grau II" in classificacoes:
                        return "Grau II"
                    else:
                        return "Grau III"

                tab5 = determinar_grau_unico(resultados_vars['Classificação'])

                # Enquadramento na NBR 14.653-2
                # Item 2 da tabela
                if num_observacoes >= 6 * (num_variaveis + 1):
                    tab2 = "Grau III"
                elif num_observacoes >= 4 * (num_variaveis + 1):
                    tab2 = "Grau II"
                elif num_observacoes >= 3 * (num_variaveis + 1):
                    tab2 = "Grau I"
                else:
                    tab2 = "Fora dos critérios"

                # Item 6 da tabela
                if nivel_significancia <= 0.01:
                    tab6 = "Grau III"
                elif nivel_significancia <= 0.02:
                    tab6 = "Grau II"
                elif nivel_significancia <= 0.05:
                    tab6 = "Grau I"
                else:
                    tab6 = "Fora dos critérios"

                # Resultados gerais formatados
                resultados_gerais = f"""
                Desvio Padrão dos Resíduos: {desvio_padrao_residuos}
                Estatística F: {estatistica_F} | Nível de Significância: {nivel_significancia}
                R²: {r_squared} | R² Ajustado: {r_squared_adjusted}
                Correlação: {coef_correlacao}
                Número de Observações: {num_observacoes}
                Número de Variáveis Independentes: {num_variaveis}

                Fundamentação - Quant. min. dados (Item 2 tab 9.2.1 NBR 14.653-2): {tab2}
                Fundamentação - Signif. Regressores (Item 5 tab 9.2.1 NBR 14.653-2): {tab5}
                Fundamentação - Signif. Modelo (Item 6 tab 9.2.1 NBR 14.653-2): {tab6}

                Testes de normalidade:
                1) Comparação (curva normal) - Percentuais atingidos: {perc_resid}
                   Ideal 68% - aceitável de 64% a 75%
                   Ideal 90% - aceitável de 88% a 95%
                   Ideal 95% - aceitável de 95% a 100%

                Teste Kolmogorov-Smirnov: Estatística = {ks_test_formatted[0]}, Valor-p = {ks_test_formatted[1]} - ({ks_interpretacao})

                Distância de Cook (Máxima): {np.max(distancia_cook):.8f}
                
                Equação do modelo: {equacao_revertida}
                """
                
                # Adicionando a coluna de erro padronizado ao df_final
                df_original_res = df_original.copy()
                df_original_res['Erro Padronizado'] = erro_padronizado

                # Criar DataFrame apenas com os dados cujo erro padronizado é maior que 2
                df_grandes_residuos = df_original_res[abs(df_original_res['Erro Padronizado']) > 2].copy()
                df_grandes_residuos['Erro Abs'] = abs(df_grandes_residuos['Erro Padronizado'])        
                           
                # Listagem de pontos com resíduos > 2  
                listagem_grandes_residuos = ", ".join(map(str, df_grandes_residuos.iloc[:, 0].tolist()))
                
                # Listagem dos pontos influenciantes
                limite_cook = 1
                pontos_influentes = []
                for i, cook_dist in enumerate(distancia_cook):
                    if cook_dist > limite_cook:
                        pontos_influentes.append(dados_transformados.iloc[i]["Dado"])  # Usando a primeira coluna como rótulo

                # Transformando a lista em uma string separada por vírgula
                listagem_pontos_influentes = ", ".join(map(str, pontos_influentes))
                              
                # Criação de um dataframe para valores previstos
                valores_previstos = modelo.predict(X)
                valores_previstos_trans = valores_previstos.copy()
                # Reverter a escala da variável dependente, se aplicável
                if var_dep in escalas:
                    escala_var_dep = escalas[var_dep][0]  # Obtém a escala associada

                    if escala_var_dep == "ln(x)":
                        valores_previstos = np.exp(valores_previstos)  # Reverte ln(x) para x
                    elif escala_var_dep == "1/(x)":
                        valores_previstos = 1 / valores_previstos  # Reverte 1/(x) para x
                    elif escala_var_dep == "(x)²":
                        valores_previstos = np.sqrt(valores_previstos)  # Reverte (x)² para x
                    elif escala_var_dep == "exp(x)":
                        valores_previstos = np.log(valores_previstos)  # Reverte exp(x) para x
                    # Caso não seja necessário reverter, mantém os valores ajustados como estão

                # Adicionando os valores ajustados como uma nova coluna ao DataFrame original
                df_calc_obs = df_original.copy()
                df_calc_obs['Valores Ajustados'] = round(valores_previstos, 8)
                # Resíduo
                df_calc_obs['Resíduo'] = (df_calc_obs[var_dep].replace(0, np.nan) - df_calc_obs['Valores Ajustados']).round(4)
                # Erro padronizado
                df_calc_obs['Erro Padronizado'] = erro_padronizado.round(4)
                # Adicionando a coluna de Erro
                # Certifique-se de evitar divisão por zero
                df_calc_obs['Erro'] = df_calc_obs['Valores Ajustados'] / df_calc_obs[var_dep].replace(0, np.nan)
                # Arredondar os valores da coluna 'Erro' para melhorar a apresentação
                df_calc_obs['Erro'] = df_calc_obs['Erro'].round(4)
                # Criando a coluna de erro percentual
                df_calc_obs['Erro Percentual (%)'] = (abs(df_calc_obs['Erro'] - 1) * 100).round(4)
                           
                # Adicionando os valores ajustados como uma nova coluna ao DataFrame original
                df_calc_obs_trans = dados_transformados.copy()
                df_calc_obs_trans['Valores Ajustados'] = round(valores_previstos_trans, 8)           
                            
                return resultados_gerais, resultados_vars, df_grandes_residuos, listagem_grandes_residuos, listagem_pontos_influentes, df_calc_obs, df_calc_obs_trans, erro_padronizado, modelo
            else:
                return "Erro: A variável dependente não está nos dados transformados.", pd.DataFrame(), pd.DataFrame(), "Erro", "Erro", pd.DataFrame(), pd.DataFrame(), [], None
        except Exception as e:
            return f"Erro na regressão: {str(e)}", pd.DataFrame(), pd.DataFrame(), "Erro", "Erro", pd.DataFrame(), pd.DataFrame(), [], None
    else:
        return "Erro: Dados transformados inválidos ou vazios.", pd.DataFrame(), pd.DataFrame(), "Erro", "Erro", pd.DataFrame(), pd.DataFrame(), [], None

# Função para plotar gráficos do modelo
def graficos(escala_dependente, df_calc_obs, df_calc_obs_trans, erro_padronizado, var_dep, num_bins=20):

    # Gráfico 1: Resíduos Padronizados
    # Normalizar os resíduos padronizados para o colormap
    residuos_norm = (np.abs(erro_padronizado) - np.abs(erro_padronizado).min()) / \
                    (np.abs(erro_padronizado).max() - np.abs(erro_padronizado).min())

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df_calc_obs_trans['Valores Ajustados'],
        y=erro_padronizado,
        mode='markers',
        marker=dict(
            size=8,
            color=residuos_norm,  # Aplicar o colorscale
            colorscale='Spectral',  # Escolher a paleta de cores
        ),
        text=df_calc_obs_trans.iloc[:, 0],
        hovertemplate="<b>Índice: %{text}</b><br>Valores Ajustados: %{x:.2f}<br>Resíduos: %{y:.2f}<extra></extra>"
    ))
    fig1.add_hline(y=0, line_dash="dash", line_color="black")
    fig1.add_hline(y=2, line_dash="dot", line_color="red")
    fig1.add_hline(y=-2, line_dash="dot", line_color="red")
    fig1.update_layout(
        title="Gráfico de Resíduos Padronizados",
        xaxis_title="Valores Ajustados",
        yaxis_title="Resíduos Padronizados",
        template="plotly_white"
    )

    # Gráfico 2: Histograma dos Resíduos Padronizados com Curva Normal
    # Calcula média e desvio padrão dos resíduos
    mean_residuos = np.mean(erro_padronizado)
    std_residuos = np.std(erro_padronizado)

    # Dados para a curva normal
    x_vals = np.linspace(mean_residuos - 4 * std_residuos, mean_residuos + 4 * std_residuos, 500)
    y_vals = stats.norm.pdf(x_vals, mean_residuos, std_residuos)  # PDF da curva normal

    # Criar o histograma (frequência normalizada)
    hist_values, bin_edges = np.histogram(erro_padronizado, bins=num_bins, density=True)
    scale_factor = max(hist_values) / max(y_vals)  # Ajustar altura da curva normal
    y_vals_scaled = y_vals * scale_factor

    # Calcular o valor médio dos resíduos absolutos para cada bin
    bin_centers = bin_edges[:-1] + np.diff(bin_edges) / 2
    bin_colors = 1 - (np.abs(bin_centers) - np.abs(bin_centers).min()) / (np.abs(bin_centers).max() - np.abs(bin_centers).min()) 

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=bin_centers,  # Centraliza as barras
        y=hist_values,
        width=np.diff(bin_edges),
        marker=dict(
            color=bin_colors,  # Aplicar o colorscale
            colorscale='Reds',
        ),
        opacity=0.7,
        name='Histograma'
    ))

    # Adicionar a curva normal ajustada
    fig2.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals_scaled,
        mode='lines',
        line=dict(color='red', width=2),
        name='Curva Normal'
    ))

    fig2.update_layout(
        title="Histograma dos Resíduos Padronizados com Curva Normal",
        xaxis_title="Resíduos Padronizados",
        yaxis_title="Frequência Normalizada",
        template="plotly_white",
    )
    
    # Gráfico 3: Valores Ajustados vs Preços Observados
    if escala_dependente == "Direta":
        df_graf_ao = df_calc_obs
    else:
        df_graf_ao = df_calc_obs_trans
    
    # Definir os eixos
    valores_observados = df_graf_ao.iloc[:, 1]  # Segunda coluna do DataFrame
    valores_calculados = df_graf_ao['Valores Ajustados']
    
    # Cálculo dos resíduos normalizados
    residuos = np.abs(valores_observados - valores_calculados)
    residuos_norm = (residuos - residuos.min()) / (residuos.max() - residuos.min())  # Normalizar para o colorscale
    
    # Ajustar a reta de regressão linear com statsmodels
    X = sm.add_constant(valores_observados)  # Adicionar uma constante (intercepto)
    modelo = sm.OLS(valores_calculados, X).fit()  # Ajustar o modelo OLS
    x_reta = np.linspace(valores_observados.min(), valores_observados.max(), 100)  # Valores de X para a reta
    y_reta = modelo.predict(sm.add_constant(x_reta))  # Predizer Y com base no modelo
    
    # Criar o gráfico
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=valores_observados,
        y=valores_calculados,
        mode='markers',
        marker=dict(
            size=8,
            color=residuos_norm,  # Aplicar o colorscale
            colorscale='Spectral',  # Escolher a paleta de cores
            showscale=False
        ),
        text=df_graf_ao.iloc[:, 0],  # Índice ou outra coluna para hover
        hovertemplate="<b>Índice: %{text}</b><br>Observado: %{x:.2f}<br>Ajustado: %{y:.2f}<extra></extra>",
        showlegend=False  # Remover legenda deste trace
    ))
    
    # Adicionar a reta ajustada (linha de regressão)
    fig3.add_trace(go.Scatter(
        x=x_reta,
        y=y_reta,
        mode="lines",
        line=dict(color="green", dash="solid"),
        name="Reta Ajustada"
    ))
    
    # Configuração do layout
    fig3.update_layout(
        title="Valores Ajustados vs Preços Observados",
        xaxis_title="Preços Observados",
        yaxis_title="Valores Ajustados",
        template="plotly_white",
        showlegend=False  # Remover legenda
    )



    # Gráfico 4: Matriz de Correlações
    corr_matrix = df_calc_obs_trans.drop(columns=["Dado", "Valores Ajustados"], errors='ignore').corr()

    # Criar o Heatmap diretamente com texto
    fig4 = go.Figure()

    # Adicionar os valores manualmente como anotação no gráfico
    for i, row in enumerate(corr_matrix.index):
        for j, col in enumerate(corr_matrix.columns):
            # Determinar a cor do texto com base nas condições
            if row == col:
                color = "black"  # Preto para a diagonal (mesma variável)
            elif corr_matrix.loc[row, col] > 0.8:  # Correlação acima de 0.8
                if row == var_dep or col == var_dep:
                    color = "blue"  #tr Azul para correlação com var_dep
                else:
                    color = "red"  # Vermelho para correlação alta entre variáveis independentes
            else:
                color = "black"  # Preto para todas as outras correlações

            # Adicionar o texto no gráfico
            fig4.add_trace(go.Scatter(
                x=[col],
                y=[row],
                text=[f"{corr_matrix.loc[row, col]:.2f}"],
                mode="text",
                textfont=dict(size=12, color=color),  # Aplicar a cor
            ))

    # Atualizar o layout
    fig4.update_layout(
        title="Matriz de Correlações",
        xaxis=dict(title="Variáveis", tickmode='array', tickvals=corr_matrix.columns),
        yaxis=dict(title="Variáveis", tickmode='array', tickvals=corr_matrix.index),
        template="plotly_white",
        showlegend=False
    )

    return fig1, fig2, fig3, fig4

# Função para exportar para o excel
def exportar_para_excel(nome_arquivo, df_planilha, df_infos, df_original, df_escalado, df_outliers, resultados_gerais, resultados_vars, df_calc_obs, df_calc_obs_trans):
    try:
        # Criar um arquivo Excel com múltiplas abas
        with pd.ExcelWriter(nome_arquivo, engine='xlsxwriter') as writer:
            # Adicionar os DataFrames em abas específicas
            df_planilha.to_excel(writer, sheet_name='Dados Originais', index=False)
            df_infos.to_excel(writer, sheet_name='Infos', index=False)
            df_original.to_excel(writer, sheet_name='Dados Modelo', index=False)
            #df_escalado.to_excel(writer, sheet_name='Dados Modelo Transformados', index=False)
            df_outliers.to_excel(writer, sheet_name='Outliers', index=False)
            
            # Converter "Resultados Gerais" para um DataFrame formatado
            resultados_lista = [linha.strip() for linha in resultados_gerais.split("\n") if linha.strip()]
            resultados_df = pd.DataFrame({"Descrição": resultados_lista})
            resultados_df.to_excel(writer, sheet_name='Resultados Gerais', index=False)
            
            # Resultados por variável
            resultados_vars.to_excel(writer, sheet_name='Resultados Variáveis', index=False)
                  
            # Valores calculados x observados
            df_calc_obs.to_excel(writer, sheet_name='Calc x Obs', index=False)
            
            # Valores calculados transformados
            #df_calc_obs_trans.to_excel(writer, sheet_name='Calculados Transformados', index=False)

        return f"Arquivo '{nome_arquivo}' criado com sucesso."
    except Exception as e:
        return f"Erro ao criar o arquivo Excel: {str(e)}"
    
# Função para salvar o modelo
def exportar_modelo_completo_avse(nome_pacote, modelo, resultados_gerais, df_planilha, df_infos, df_original, df_outliers, resultados_vars, df_calc_obs):
    try:
        # Verificar se o nome do pacote está vazio
        if not nome_pacote:
            return "Erro: O nome do arquivo não pode estar vazio."

        # Garantir que o nome do pacote tenha a extensão .avse
        if not nome_pacote.endswith(".avse"):
            nome_pacote += ".avse"

        # Empacotar todos os itens em um dicionário
        pacote = {
            "modelo": modelo,
            "Resultados Gerais": resultados_gerais,
            "df_planilha": df_planilha,
            "df_infos": df_infos,
            "df_original": df_original,
            "df_outliers": df_outliers,
            "resultados_vars": resultados_vars,
            "df_calc_obs": df_calc_obs
        }

        # Salvar o pacote usando joblib
        dump(pacote, nome_pacote)
        return f"Pacote '{nome_pacote}' criado com sucesso."
    except Exception as e:
        return f"Erro ao criar o pacote: {str(e)}"
    
# Função para carregar o modelo
def carregar_modelo(nome_pacote):
    try:
        # Carregar o pacote salvo
        pacote = joblib.load(nome_pacote)

        # Recuperar os objetos do pacote
        modelo = pacote.get("modelo", None)  # Objeto do modelo salvo
        resultados_gerais = pacote.get("Resultados Gerais", "")  # Resultados gerais do modelo
        df_planilha = pacote.get("df_planilha", pd.DataFrame())
        df_infos = pacote.get("df_infos", pd.DataFrame())
        df_original = pacote.get("df_original", pd.DataFrame())
        df_outliers = pacote.get("df_outliers", pd.DataFrame())
        resultados_vars = pacote.get("resultados_vars", pd.DataFrame())
        df_calc_obs = pacote.get("df_calc_obs", pd.DataFrame())

        # Adicionar uma linha em branco no df_infos se ele não estiver vazio
        if not df_infos.empty:
            df_infos.loc[len(df_infos)] = [None] * len(df_infos.columns)
            
        # Transpor o DataFrame
        df_infos_transposed = df_infos.T
        
        # Renomear as colunas
        df_infos_transposed.columns = ['Escalas', 'Máximo', 'Mínimo', 'Médio', 'Avaliando']
        
        # Adicionar a coluna 'Variáveis' com os nomes das colunas originais
        df_infos_transposed.insert(0, 'Variáveis', df_infos.columns)   
        
        # Atribuir o valor padrão "------" à célula da primeira linha da última coluna
        df_infos_transposed.iloc[0, -1] = "Variável dependente"
        
        # Obter apenas o nome do arquivo, sem o caminho
        nome_arquivo = os.path.basename(nome_pacote)
        
        # Criar mensagem de sucesso com o nome do modelo
        mensagem_sucesso = f"Modelo '{nome_arquivo}' carregado com sucesso."
            
        # Retornar todos os componentes necessários
        return (
            mensagem_sucesso,  # Mensagem de sucesso com o nome do modelo
            modelo,  # Modelo carregado para previsões
            resultados_gerais,  # Resultados gerais do modelo
            df_planilha,  # Dados originais
            df_original,  # Dados usados no modelo
            df_outliers,  # Outliers identificados
            resultados_vars,  # Resultados por variável
            df_calc_obs,  # Dados calculados x observados
            df_infos_transposed,  # Informações adicionais do modelo
        )
    except Exception as e:
        # Retornar valores padrão em caso de erro
        return (
            "Carregue o modelo antes de clicar no botão VISUALIZAR MODELO",
            None,  # Modelo não carregado
            "",  # Resultados gerais vazio
            pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),
        )



def realizar_previsoes(modelo, tab_infos_carregada):
    try:
        if modelo is None or tab_infos_carregada.empty:
            return "Erro: Modelo não carregado ou tabela de informações vazia.", pd.DataFrame(), pd.DataFrame(), ""

        # Identificar as escalas das variáveis independentes e dependente
        escalas_independentes = tab_infos_carregada.iloc[1:, 1].to_list()  # a partir da 2ª linha da 2ª coluna
        escala_dependente = tab_infos_carregada.iloc[0, 1]  # 1ª linha da 2ª coluna

        # Valores para previsão estão a partir da 2ª linha da 6ª coluna
        valores_entrada = tab_infos_carregada.iloc[1:, 5].values

        # Converter valores para numéricos, substituindo inválidos por NaN
        valores_entrada = pd.to_numeric(valores_entrada, errors='coerce')

        # Aplicar escalas às variáveis independentes
        valores_transformados = []
        for valor, escala in zip(valores_entrada, escalas_independentes):
            if np.isnan(valor):
                valores_transformados.append(np.nan)  # Manter NaN se o valor for inválido
            elif escala == "ln(x)":
                valores_transformados.append(np.log(valor) if valor > 0 else np.nan)  # Evitar log de zero ou negativo
            elif escala == "1/(x)":
                valores_transformados.append(1 / valor if valor != 0 else np.nan)  # Evitar divisão por zero
            elif escala == "(x)²":
                valores_transformados.append(valor ** 2)
            elif escala == "exp(x)":
                valores_transformados.append(np.exp(valor))
            else:
                valores_transformados.append(valor)

        # Transformar em DataFrame para manter o formato necessário
        df_previsao = pd.DataFrame([valores_transformados], columns=tab_infos_carregada.iloc[1:, 0])

        # Adicionar constante ao modelo para previsão
        X = sm.add_constant(df_previsao, has_constant='add')

        # Garantir que as colunas em X correspondam às usadas no modelo
        colunas_modelo = modelo.model.exog_names
        X = X.reindex(columns=colunas_modelo, fill_value=0)  # Reordenar e preencher colunas faltantes com 0

        # Verificar se existem valores NaN nos dados transformados
        if X.isnull().values.any():
            return "Erro: Existem valores inválidos após a transformação. Verifique os dados de entrada.", df_previsao, pd.DataFrame(), ""

        # Realizar a previsão
        previsao_transformada = modelo.predict(X).iloc[0]

        # Ajustar para a escala direta da variável dependente
        if escala_dependente == "ln(x)":
            previsao_final = np.exp(previsao_transformada)
        elif escala_dependente == "1/(x)":
            previsao_final = 1 / previsao_transformada
        elif escala_dependente == "(x)²":
            previsao_final = np.sqrt(previsao_transformada)
        elif escala_dependente == "exp(x)":
            previsao_final = np.log(previsao_transformada)
        else:
            previsao_final = previsao_transformada

        # Calcular limites do campo de arbítrio
        limite_inferior_arbitrio = previsao_final * 0.85
        limite_superior_arbitrio = previsao_final * 1.15

        # Calcular intervalo de confiança de 80%
        intervalos = modelo.get_prediction(X).conf_int(alpha=0.2)
        limite_inferior_ic = intervalos[0, 0]  # Acessar diretamente o valor do array
        limite_superior_ic = intervalos[0, 1]  # Acessar diretamente o valor do array

        # Ajustar limites de IC para a escala direta, se necessário
        if escala_dependente == "ln(x)":
            limite_inferior_ic = np.exp(limite_inferior_ic)
            limite_superior_ic = np.exp(limite_superior_ic)
        elif escala_dependente == "1/(x)":
            limite_inferior_ic = 1 / limite_inferior_ic
            limite_superior_ic = 1 / limite_superior_ic
        elif escala_dependente == "(x)²":
            limite_inferior_ic = np.sqrt(limite_inferior_ic)
            limite_superior_ic = np.sqrt(limite_superior_ic)
        elif escala_dependente == "exp(x)":
            limite_inferior_ic = np.log(limite_inferior_ic)
            limite_superior_ic = np.log(limite_superior_ic)

        # Cálculo da extrapolação
        extrapolacao_info = ""
        valores_ajustados = valores_entrada.copy()
        contagem_extrapolacoes = 0
        fora_dos_criterios = False
        for i, valor in enumerate(valores_entrada):
            maximo = pd.to_numeric(tab_infos_carregada.iloc[i+1, 2], errors='coerce')  # Coluna 3 (Mínimo)
            minimo = pd.to_numeric(tab_infos_carregada.iloc[i+1, 3], errors='coerce')  # Coluna 4 (Máximo)

            if not np.isnan(valor):
                if valor < minimo:
                    percentual_extrapolacao = ((minimo - valor) / minimo) * -100
                    extrapolacao_info += f"Variável '{tab_infos_carregada.iloc[i+1, 0]}' está {percentual_extrapolacao:.2f}% abaixo do mínimo da amostra.\n"
                    valores_ajustados[i] = minimo  # Ajustar valor para o mínimo
                    contagem_extrapolacoes += 1
                    if percentual_extrapolacao < -50:
                        fora_dos_criterios = True
                elif valor > maximo:
                    percentual_extrapolacao = ((valor - maximo) / maximo) * 100
                    extrapolacao_info += f"Variável '{tab_infos_carregada.iloc[i+1, 0]}' está {percentual_extrapolacao:.2f}% acima do máximo da amostra.\n"
                    valores_ajustados[i] = maximo  # Ajustar valor para o máximo
                    contagem_extrapolacoes += 1
                    if percentual_extrapolacao > 100:
                        fora_dos_criterios = True

        # Criar novos DataFrames para cada variável que extrapolou
        previsoes_extrapoladas = []
        for i, (valor, ajustado) in enumerate(zip(valores_entrada, valores_ajustados)):
            if valor != ajustado:
                valores_transformados_ext = []
                for valor_ext, escala in zip(valores_ajustados, escalas_independentes):
                    if np.isnan(valor_ext):
                        valores_transformados_ext.append(np.nan)
                    elif escala == "ln(x)":
                        valores_transformados_ext.append(np.log(valor_ext) if valor_ext > 0 else np.nan)
                    elif escala == "1/(x)":
                        valores_transformados_ext.append(1 / valor_ext if valor_ext != 0 else np.nan)
                    elif escala == "(x)²":
                        valores_transformados_ext.append(valor_ext ** 2)
                    elif escala == "exp(x)":
                        valores_transformados_ext.append(np.exp(valor_ext))
                    else:
                        valores_transformados_ext.append(valor_ext)

                df_previsao_ext = pd.DataFrame([valores_transformados_ext], columns=tab_infos_carregada.iloc[1:, 0])
                X_ext = sm.add_constant(df_previsao_ext, has_constant='add')
                X_ext = X_ext.reindex(columns=colunas_modelo, fill_value=0)

                if X_ext.isnull().values.any():
                    continue

                previsao_transformada_ext = modelo.predict(X_ext).iloc[0]

                if escala_dependente == "ln(x)":
                    previsao_final_ext = np.exp(previsao_transformada_ext)
                elif escala_dependente == "1/(x)":
                    previsao_final_ext = 1 / previsao_transformada_ext
                elif escala_dependente == "(x)²":
                    previsao_final_ext = np.sqrt(previsao_transformada_ext)
                elif escala_dependente == "exp(x)":
                    previsao_final_ext = np.log(previsao_transformada_ext)
                else:
                    previsao_final_ext = previsao_transformada_ext

                previsoes_extrapoladas.append((df_previsao_ext, previsao_final_ext))

        # Determinar a fundamentação da extrapolação
        if fora_dos_criterios:
            fundamentacao = "Fundamentação - Extrapolação (Item 4 (a) tab 9.2.1 NBR 14.653-2): Fora dos critérios"
        elif contagem_extrapolacoes == 1:
            fundamentacao = "Fundamentação - Extrapolação (Item 4 (a) tab 9.2.1 NBR 14.653-2): Grau II"
        elif contagem_extrapolacoes > 1:
            fundamentacao = "Fundamentação - Extrapolação (Item 4 (a) tab 9.2.1 NBR 14.653-2): Grau I"
        else:
            fundamentacao = ""

        # Retornar as informações
        resultado_texto = (
            f"Valor estimado central: {locale.currency(previsao_final, grouping=True)}\n"
            "------------------------------------\n"
            f"Limite inferior do campo de arbítrio (- 15% do Valor estimado central): {locale.currency(limite_inferior_arbitrio, grouping=True)}\n"
            f"Limite superior do campo de arbítrio (+ 15% do Valor estimado central): {locale.currency(limite_superior_arbitrio, grouping=True)}\n"
            "------------------------------------\n"
            f"Limite inferior do Intervalo de Confiança de 80%: {locale.currency(limite_inferior_ic, grouping=True)}\n"
            f"Limite superior do Intervalo de Confiança de 80%: {locale.currency(limite_superior_ic, grouping=True)}\n"
            "------------------------------------\n"
            f"{extrapolacao_info.strip()}\n"
            f"{fundamentacao}\n"
        )
        
        
        resultado_df = df_previsao
        resultado_df_ext = pd.DataFrame()
        resultado_texto_ext = ""
        
        if previsoes_extrapoladas:
            for df_ext, previsao_ext in previsoes_extrapoladas:
                resultado_df_ext = df_ext
                resultado_texto_ext = (
                    f"Valor estimado central (na fronteira amostral): {locale.currency(previsao_ext, grouping=True)}\n"
                    "------------------------------------\n"
                )
                
                # Cálculo da variação percentual
                variacao_percentual = abs((previsao_final - previsao_ext) / previsao_final) * 100
        
                # Determinar a fundamentação com base na variação percentual
                if variacao_percentual > 20:
                    fundamentacao_ext = "Fundamentação - Extrapolação (Item 4 (b) tab 9.2.1 NBR 14.653-2): Fora dos critérios"
                elif variacao_percentual > 15:
                    fundamentacao_ext = "Fundamentação - Extrapolação (Item 4 (b) tab 9.2.1 NBR 14.653-2): Grau I"
                else:
                    fundamentacao_ext = "Fundamentação - Extrapolação (Item 4 (b) tab 9.2.1 NBR 14.653-2): Grau II"
        
                resultado_texto_ext += f"{fundamentacao_ext}\n"

        return resultado_df, resultado_texto, resultado_df_ext, resultado_texto_ext

    except Exception as e:
        return pd.DataFrame(), "Erro ao realizar a previsão: {str(e)}", pd.DataFrame(), ""


#--------------------------------------------INTERFACE-------------------------------------------#

def rl_tab():
    # Criação da aba
    with gr.Tab("Regressão Linear"):
        planilha_input = gr.File(label="Carregar Planilha", file_types=[".xls", ".xlsx"], elem_classes=["small-file-upload"])

        with gr.Group():

        #---------ESTADOS DE ARMAZENAMENTO-------------#

            # Estado para armazenamentos
            cabeçalhos_state = gr.State([])
            dados_state = gr.State(pd.DataFrame())
            escalas_state = gr.State({})
            erro_padronizado_state = gr.State([])
            # Estados para armazenar os gráficos Plotly gerados
            grafico_residuos_state = gr.State(None)
            grafico_histograma_state = gr.State(None)
            grafico_ajustados_state = gr.State(None)
            matriz_corr_state = gr.State(None)
            # Estado para armazenar o modelo gerado
            modelo_state = gr.State(None)

        #---------PLANILHA DE ENTRADA-------------#

            # Checkbox para controlar a visibilidade da planilha carregada
            mostrar_planilha = gr.Checkbox(label="MOSTRAR PLANILHA CARREGADA e GRÁFICOS PARA ANÁLISE EXPLORATÓRIA   (Os gráficos de dispersão e boxplot são atualizados com a retirada de dados)", value=False)
            tabela_planilha = gr.Dataframe(visible=False, max_height=250, elem_classes=["small span"])  # Oculto por padrão

        #---------GRÁFICOS DE DISPERSÃO-------------#

            # Gráficos de dispersão
            with gr.Row(equal_height=True):
                coluna_y_dispersao = gr.Dropdown(label="Eixo Y (Dispersão)", choices=[], interactive=True, visible=False, scale=3)
                transformacao_y = gr.Dropdown(
                    label="Transformação para Eixo Y",
                    choices=["Nenhuma", "1/x", "ln(x)", "x²", "exp(x)"],
                    value="Nenhuma",
                    interactive=True,
                    visible=False,
                    scale=2
                )
                coluna_x_dispersao = gr.Dropdown(label="Eixo X (Dispersão)", choices=[], interactive=True, visible=False, scale=3)
                transformacao_x = gr.Dropdown(
                    label="Transformação para Eixo X",
                    choices=["Nenhuma", "1/x", "ln(x)", "x²", "exp(x)"],
                    value="Nenhuma",
                    interactive=True,
                    visible=False,
                    scale=2
                )
                # Adicionando os gráficos de dispersão e boxplot lado a lado com o mesmo botão
                botao_dispersao_boxplot = gr.Button("Gerar Gráficos de Dispersão e Boxplot", visible=False)
            with gr.Row():
                grafico_dispersao_saida = gr.Plot(label="Gráfico de Dispersão", visible=False, scale=3)
                grafico_boxplot_saida = gr.Plot(label="Gráfico Boxplot", visible=False, scale=1)

        #---------ESCOLHA DAS VARIÁVEIS-------------#

        # Checkbox para controlar a visibilidade dos dropdowns
        mostrar_dropdowns = gr.Checkbox(label="VARIÁVEIS E ESCALAS   (Variável dependente e variáveis independentes)", value=False, elem_classes="checkbox-yellow")
        # Dropdown multi-select para cabeçalhos
        # Título do conjunto
        with gr.Group():
            var_ind = gr.Markdown("Selecione as variáveis desejadas no dropdown da escala para a transformação", visible=False)  # Adiciona um título ao grupo de dropdowns
            with gr.Row():
                colunas_x = gr.Dropdown(label="(Direta: y ou x)", multiselect=True, choices=[], value=[], interactive=True, visible=False)
                colunas_ln_x = gr.Dropdown(label="Logarítmica: ln(y) ou ln(x)", multiselect=True, choices=[], interactive=True, visible=False)
                colunas_exp_x = gr.Dropdown(label="Exponencial: exp(y) ou exp(x)", multiselect=True, choices=[], interactive=True, visible=False)
                colunas_inv_x = gr.Dropdown(label="Inversa: 1/(y) ou 1/(x)", multiselect=True, choices=[], interactive=True, visible=False)
                colunas_quad_x = gr.Dropdown(label="Quadrática: (x)² ou (y²) ", multiselect=True, choices=[], interactive=True, visible=False)
        # Escolha da variável dependente
        var_dep = gr.Dropdown(label="Variável Dependente", multiselect=False, choices=[], interactive=True, visible=False)

        #---------DATAFRAMES-------------#

        with gr.Row(equal_height=True):
            # Botão para gerar DataFrames
            botao_gerar_df = gr.Button("Gerar Planilhas", scale=1)
            # Checkbox para controlar visibilidade dos DataFrames gerados
            mostrar_dataframes = gr.Checkbox(label="MOSTRAR PLANILHAS   (Escalas e limites, Variáveis transformadas e Outliers)", value=False, scale=3)
        # DataFrames para visualização
        tabela_cabecalhos = gr.Dataframe(label="Planilha com Cabeçalhos, Escalas, Máximo, Mínimo e Média das variáveis utilizadas", max_height=200, visible=False, elem_classes=["small span"])
        tabela_original = gr.Dataframe(label="Planilha original com Variáveis Escolhidas", max_height=250, visible=False, elem_classes=["small span"])
        tabela_escalada = gr.Dataframe(label="Planilha com Variáveis Transformadas", max_height=250, visible=False, interactive=True, headers=None, elem_classes=["small span"])
        #matriz_correl = gr.Dataframe(label="Matriz de correlações", max_height=250, visible=False, interactive=True, headers=None, elem_classes=["small span"])
        df_out = gr.Dataframe(label="Outliers", max_height=150, visible=False, interactive=True, headers=None, elem_classes=["small span"])

        #---------MODELO-------------#

        with gr.Row(equal_height=True):
            # Adicionando botão para executar a regressão
            botao_regressao = gr.Button("Gerar Modelo", scale=1)
            # Checkbox para visualizar os resultados
            mostrar_resultados = gr.Checkbox(label="REGRESSÃO LINEAR   (Resultados gerais e por variável, Resíduos > 2 e Pontos Influenciantes, Valores calculados x valores observados)", value=False, scale=3)
        # Resultados gerais e por variáveis
        with gr.Row():
            resultado_geral = gr.Textbox(label="Resultados Gerais", lines=25, interactive=False, visible=False, scale=1)
            resultado_coef = gr.Dataframe(label="Resultados por Variável", interactive=False, visible=False, scale=1, elem_classes=["small span"])
        # Resíduos (dataframe e listagem)
        residuos = gr.Dataframe(label="Resíduos padronizados > 2", interactive=False, max_height=250, visible=False, scale=1, elem_classes=["small span"])
        with gr.Row():
            # Resíduos > 2
            residuos_list = gr.Textbox(label="Listagem resíduos padronizados > 2", lines=2, interactive=False, visible=False, scale=2)
            # Pontos influenciantes
            pontos_inf = gr.Textbox(label="Listagem dos Pontos Influenciantes", lines=2, interactive=False, visible=False, scale=1)
            # Entrada dinâmica
            entrada_dinamica = gr.Textbox(label="Retirar dados", lines=2, placeholder="Copie e cole os dados da caixa de texto ao lado ou escolha o dado a ser retirado",
                interactive=True, visible=False, scale=2)

        # Adicionando a visualização para df_calc_obs
        calc_obs = gr.Dataframe(label="Calculados x Observados", max_height=250, visible=False, interactive=True, headers=None, elem_classes=["small span"])
        calc_obs_trans = gr.Dataframe(label="Calculados Transformados", max_height=250, visible=False, interactive=True, elem_classes=["small span"])

        #---------GRÁFICOS DO MODELO-------------#

        with gr.Row(equal_height=True):
            # Adicionar botão para gerar gráficos
            botao_graficos = gr.Button("Gerar Gráficos", scale=1)
            # Checkbox para controlar a visibilidade da seção de gráficos do modelo
            mostrar_graficos = gr.Checkbox(label="GRÁFICOS DO MODELO   (Resíduos padronizados, histograma e valores ajustados vs observados, Matriz de Correlações)", value=False, scale=3)
        # Escolha a escala da variável dependente para o gráfico Ajustados x Observado
        escala_graf_ao = gr.Dropdown(label="Escolha a escala da variável dependente para o gráfico Valores Ajustados x Observado", choices=["Transformada", "Direta"])

        # Adicionar rádio para selecionar o gráfico
        grafico_selecao = gr.Radio(
            choices=["Resíduos Padronizados", "Histograma", "Valores Ajustados vs Observados", "Matriz de Correlações"],
            label="Selecione o Gráfico",
            interactive=True,
            visible=False
        )

        # Adicionar saída para o gráfico selecionado
        grafico_saida = gr.Plot(label="Gráfico Selecionado", visible=False)

        #---------EXPORTAR PARA O EXCEL-------------#

        with gr.Row(equal_height=True):
            botao_exportar_excel = gr.Button("Exportar Planilha")
            arquivo_excel = gr.File(label="Baixar Excel", interactive=False, visible=False)

        #---------SALVAR MODELO-------------#

        with gr.Row(equal_height=True):
            # Adicionar campo de entrada para o nome do arquivo
            nome_arquivo_modelo = gr.Textbox(
                label="Nome do Arquivo do Modelo",
                placeholder="Digite o nome do modelo e clique no botão ao lado para salvar",
                interactive=True,
                scale=3
            )
            # Adicionar botão "SALVAR MODELO" e output para indicar o sucesso/erro
            botao_salvar_modelo = gr.Button("Salvar Modelo", scale=1)
        saida_salvar_modelo = gr.Textbox(
            label="Status do Salvamento do Modelo",
            interactive=False,
            visible=False,
            lines=2
        )

        #---------CARREGAR MODELO-------------#

        with gr.Row(equal_height=True):
           # Entrada para carregar o modelo
            modelo_input = gr.File(label="Carregar Modelo", file_types=[".avse"], elem_classes=["small-file-upload"])
            # Botão para carregar o modelo
            botao_carregar_modelo = gr.Button("Visualizar Modelo")
            # Checkbox abaixo do botão "Visualizar Modelo"
            mostrar_modelo_checkbox = gr.Checkbox(
                label="MOSTRAR DETALHES DO MODELO",
                value=False,
                elem_classes=["checkbox-yellow"]
            )
        # Mensagem de status para aparecer logo abaixo do modelo_input
        status_carregamento = gr.Textbox(
            label="Status do Carregamento do Modelo",
            interactive=False,
            visible=False,  # Certifique-se de que está visível
            lines=1,
            elem_classes=["small span"]
        )

        # TextBox para exibir os resultados gerais
        resultado_geral_carregado = gr.Textbox(
            label="Resultados Gerais (Carregados)",
            interactive=False,
            visible=False,
            lines=25,  # Ajuste o número de linhas conforme necessário
            elem_classes=["small span"]
        )

        # DataFrames para exibição
        tabela_planilha_carregada = gr.Dataframe(label="Dados Originais", visible=False, max_height=250, elem_classes=["small span"])
        tabela_original_carregada = gr.Dataframe(label="Dados Modelo", visible=False, max_height=250, elem_classes=["small span"])
        tabela_outliers_carregada = gr.Dataframe(label="Outliers", visible=False, max_height=250, elem_classes=["small span"])
        tabela_resultados_vars_carregada = gr.Dataframe(label="Resultados Variáveis", visible=False, max_height=250, elem_classes=["small span"])
        tabela_calc_obs_carregada = gr.Dataframe(label="Calculados x Observados", visible=False, max_height=250, elem_classes=["small span"])
        tab_infos_carregada = gr.Dataframe(label="Variáveis, escalas, limites e avaliando", interactive=True, visible=False, elem_classes=["small span"])

        #---------AVALIAÇÃO-------------#

        botao_previsao = gr.Button("Realizar Previsão")
        tabela_previsao = gr.Dataframe(label="Valores Transformados para Previsão", visible=True, max_height=250)
        previsao_saida = gr.Textbox(label="Resultado da Previsão", lines=8, interactive=False, visible=True)

        # Adicionar DataFrames para exibir os resultados das previsões ajustadas
        tabela_previsao_ajustada = gr.Dataframe(label="Valores Transformados para Previsão Ajustada", visible=True, max_height=250)
        previsao_ajustada_saida = gr.Textbox(label="Resultado da Previsão Ajustada", lines=8, interactive=False, visible=True)

        # 1. CONTROLE DE VISIBILIDADE

        # 1.1. Mostrar ou ocultar a planilha carregada e os gráficos
        mostrar_planilha.change(
            lambda visible, dados: [gr.update(visible=visible, value=dados)] * 8,
            inputs=[mostrar_planilha, dados_state],
            outputs=[
                tabela_planilha, coluna_y_dispersao, transformacao_y, coluna_x_dispersao,
                transformacao_x, botao_dispersao_boxplot,
                grafico_dispersao_saida, grafico_boxplot_saida
            ]
        )

        # 1.2. Mostrar ou ocultar os dropdowns para escolha de variáveis transformadas
        mostrar_dropdowns.change(
            lambda visible: [gr.update(visible=visible)] * 7,
            inputs=[mostrar_dropdowns],
            outputs=[var_ind, colunas_x, colunas_ln_x, colunas_exp_x, colunas_inv_x, colunas_quad_x, var_dep]
        )

        # 1.3. Mostrar ou ocultar os DataFrames gerados (cabeçalhos, escalas, correlação, etc.)
        mostrar_dataframes.change(
            lambda visible: [gr.update(visible=visible)] * 3,
            inputs=[mostrar_dataframes],
            outputs=[tabela_cabecalhos, tabela_escalada, df_out] #matriz_correl,
        )

        # 1.4. Mostrar ou ocultar os resultados da regressão (resultados gerais, resíduos, etc.)
        mostrar_resultados.change(
            lambda visible: [gr.update(visible=visible)] * 7,
            inputs=[mostrar_resultados],
            outputs=[resultado_geral, resultado_coef, residuos, residuos_list, pontos_inf, entrada_dinamica, calc_obs]
        )

        # 1.5. Mostrar ou ocultar a seção de gráficos e componentes associados
        mostrar_graficos.change(
            lambda visible: [gr.update(visible=visible)] * 2,
            inputs=[mostrar_graficos],
            outputs=[grafico_selecao, grafico_saida]
        )

        # 1.6. Mostrar ou ocultar os detalhes do modelo carregado
        mostrar_modelo_checkbox.change(
            lambda visible: [gr.update(visible=visible)] * 8,
            inputs=[mostrar_modelo_checkbox],
            outputs=[
                resultado_geral_carregado, tabela_planilha_carregada, tabela_original_carregada,
                tabela_outliers_carregada, tabela_resultados_vars_carregada, tabela_calc_obs_carregada,
                tab_infos_carregada, status_carregamento
            ]
        )

        # 2. CARREGAMENTO DE PLANILHA E ATUALIZAÇÃO DE DADOS

        # 2.1. Carregar a planilha e extrair cabeçalhos e dados
        planilha_input.change(
            lambda file: carregar_planilha(file),
            inputs=[planilha_input],
            outputs=[cabeçalhos_state, dados_state]
        )

        # 2.2. Atualizar as opções de dropdown para o gráfico de dispersão ao carregar uma planilha
        cabeçalhos_state.change(
            lambda cabecalhos: [gr.update(choices=cabecalhos, value=None)] * 2,
            inputs=[cabeçalhos_state],
            outputs=[coluna_y_dispersao, coluna_x_dispersao]
        )

        # 2.3. Atualizar os dropdowns para transformações e seleção de variáveis dependentes/independentes
        cabeçalhos_state.change(
            atualizar_dropdowns,
            inputs=[cabeçalhos_state],
            outputs=[colunas_x, colunas_ln_x, colunas_exp_x, colunas_inv_x, colunas_quad_x, var_dep]
        )

        # 2.4. Atualizar o gráfico exibido com base na seleção do usuário
        grafico_selecao.change(
            lambda escala, selecao, fig1, fig2, fig3, fig4: (
                fig1 if selecao == "Resíduos Padronizados" else
                (fig2 if selecao == "Histograma" else
                (fig3 if selecao == "Valores Ajustados vs Observados" else fig4))
            ),
            inputs=[escala_graf_ao, grafico_selecao, grafico_residuos_state, grafico_histograma_state, grafico_ajustados_state, matriz_corr_state],
            outputs=[grafico_saida]
        )

        # 3. BOTÕES
        # 3.1. Botão para conectar à função de Gerar os gráficos de dispersão e boxplot (GERAR DISPERSÃO E BOXPLOT)
        botao_dispersao_boxplot.click(
            lambda df, y_coluna, transformacao_y, x_coluna, transformacao_x, dados_out: (
                grafico_dispersao(df, y_coluna, transformacao_y, x_coluna, transformacao_x, dados_out),
                grafico_boxplot(df, y_coluna, transformacao_y, x_coluna, transformacao_x, dados_out)
            ),
            inputs=[dados_state, coluna_y_dispersao, transformacao_y, coluna_x_dispersao, transformacao_x, entrada_dinamica],
            outputs=[grafico_dispersao_saida, grafico_boxplot_saida]
        )

        # 3.2. Botão para conectar à função de Gerar os dataframes cabeçalhos, escalas e estatísticas básicas (máximo, mínimo, média) e
        # transformados, escalados e correlação (GERAR PLANILHAS)
        botao_gerar_df.click(
            criar_dataframe_cabecalhos,
            inputs=[cabeçalhos_state, colunas_x, colunas_ln_x, colunas_exp_x, colunas_inv_x, colunas_quad_x, dados_state, entrada_dinamica, var_dep],
            outputs=[tabela_cabecalhos, escalas_state]
        )

        botao_gerar_df.click(
            criar_dataframes,
            inputs=[dados_state, colunas_x, colunas_ln_x, colunas_exp_x, colunas_inv_x, colunas_quad_x, entrada_dinamica, var_dep],
            outputs=[tabela_original, tabela_escalada, df_out]  # , matriz_correl
        )

        # 3.3. Botão para conectar à função de realizar regressão linear com base nas variáveis selecionadas (GERAR MODELO)
        botao_regressao.click(
            realizar_regressao,
            inputs=[var_dep, tabela_escalada, tabela_original, escalas_state],
            outputs=[resultado_geral, resultado_coef, residuos, residuos_list, pontos_inf, calc_obs, calc_obs_trans,
                    erro_padronizado_state, modelo_state]
        )

        # 3.4. Botão para conectar à função de Gerar gráficos do modelo (GERAR GRÁFICOS - resíduos, histograma, ajustados vs observados)
        botao_graficos.click(
            graficos,  # Função que gera os gráficos Plotly
            inputs=[escala_graf_ao, calc_obs, calc_obs_trans, erro_padronizado_state, var_dep],
            outputs=[grafico_residuos_state, grafico_histograma_state, grafico_ajustados_state, matriz_corr_state]
        )

        # 3.5. Botão para conectar à função de exportar para o excel (EXPORTAR PLANILHA)
        botao_exportar_excel.click(
            lambda df_planilha, df_infos, df_original, df_escalado, df_out, resultados_gerais, resultados_vars, df_calc_obs, df_calc_obs_trans: (
                "resultado.xlsx",
                exportar_para_excel(
                    "resultado.xlsx", df_planilha, df_infos, df_original, df_escalado, df_out,
                    resultados_gerais, resultados_vars, df_calc_obs, df_calc_obs_trans
                )
            )[0],
            inputs=[
                dados_state, tabela_cabecalhos, tabela_original, tabela_escalada, df_out,
                resultado_geral, resultado_coef, calc_obs, calc_obs_trans
            ],
            outputs=[arquivo_excel]
        )
        # Atualizar visibilidade do status após clique no botão
        botao_exportar_excel.click(
            lambda *args: gr.update(visible=True),
            inputs=[],
            outputs=[arquivo_excel]
        )

        # 3.6. Botão para conectar à função de salvar o modelo (SALVAR MODELO)
        botao_salvar_modelo.click(
            lambda nome_arquivo, modelo, resultados_gerais, df_planilha, df_infos, df_original, df_outliers, resultados_vars, df_calc_obs: (
                exportar_modelo_completo_avse(
                    nome_arquivo, modelo, resultados_gerais, df_planilha, df_infos, df_original,
                    df_outliers, resultados_vars, df_calc_obs
                )
            ),
            inputs=[
                nome_arquivo_modelo, modelo_state, resultado_geral, dados_state, tabela_cabecalhos,
                tabela_original, df_out, resultado_coef, calc_obs
            ],
            outputs=[saida_salvar_modelo]
        )
        # Atualizar visibilidade do status após clique no botão
        botao_salvar_modelo.click(
            lambda: gr.update(visible=True),
            inputs=[],
            outputs=[saida_salvar_modelo]
        )

        # 3.7. Botão para conectar à função de carregamento do modelo (VISUALIZAR MODELO)
        botao_carregar_modelo.click(
            carregar_modelo,
            inputs=[modelo_input],
            outputs=[
                status_carregamento,  # Mensagem de status aparece logo abaixo da caixa de upload
                modelo_state,         # Estado para armazenar o modelo carregado
                resultado_geral_carregado,
                tabela_planilha_carregada, tabela_original_carregada, tabela_outliers_carregada,
                tabela_resultados_vars_carregada, tabela_calc_obs_carregada, tab_infos_carregada
            ]
        )

        # 3.8. Botão para conectar à função de realizar previsões (REALIZAR PREVISÃO)
        botao_previsao.click(
            realizar_previsoes,
            inputs=[modelo_state, tab_infos_carregada],
            outputs=[tabela_previsao, previsao_saida, tabela_previsao_ajustada, previsao_ajustada_saida]
        )

    return locals()


### Pontos de máximo e mínimo
### Colunas com Coordenadas (ter a possibilidade de dizer se há ou não coordenadas para criar uma dispesão espacial)
### Endereços
### Colunas que possuem valor 0, não podem ser utilizados na ln ou inversa (mensagem de erro?)
### Micronumerosidade
### Média, mediana e moda
### Problema no ordenamento dos dataframes
### Implementar avaliação em massa
### Implementar relatório em word
### Conectar a elaboração do modelo com o carregamento
