import marimo

__generated_with = "0.19.1"
app = marimo.App(width="full", app_title="1000 tráficos", css_file="")


@app.cell
def _(mo):
    mo.md(r"""
    # 1000 tráficos - Piracicaba (jan. 2026)
    ### Uma visão a partir das Sentenças de 1º Grau, por José Eduardo S. Pimentel
    - Construído exclusivamente com informações públicas.
    - Análise e georreferenciamento automatizados: **os dados podem conter erros**.
    - Feito para computador (no celular use o modo paisagem).
    """)
    return


@app.cell
def _():
    import marimo as mo
    import folium
    import pandas as pd
    from folium.plugins import MarkerCluster
    from folium.plugins import HeatMap
    return HeatMap, MarkerCluster, folium, mo, pd


@app.cell
def _(pd):
    # Lê o arquivo CSV
    df = pd.read_csv('https://raw.githubusercontent.com/jespimentel/1000_traficos/refs/heads/main/dados.csv')
    return (df,)


@app.cell
def _(df, mo):
    # Cria o dropdown
    resultado = mo.ui.dropdown(
        options=sorted(list(df['resultado_processo'].unique()) + ['Todas']), 
        label="Tipo de sentença: ", 
        value = 'Todas' # Valor padrão
    )

    # Exibe o dropdown
    resultado
    return (resultado,)


@app.cell
def _(mo):
    # Cria o dropdown
    responsavel_prisao = mo.ui.dropdown(
       options=["policial militar", "policial civil", "policial penal", "guarda municipal", "outros", "Todos"],
       label="Tipo de agente:",
       value="Todos"
    )

    # Exibe o dropdown
    responsavel_prisao
    return (responsavel_prisao,)


@app.cell
def _(mo):
    # Cria o dropdown
    tipo_mapa = mo.ui.dropdown(
       options=["Clusters", "Calor"],
       label="Visualização:",
       value="Clusters"
    )

    # Exibe o dropdown
    tipo_mapa
    return (tipo_mapa,)


@app.cell
def _(df, responsavel_prisao, resultado):
    # Filtragens sucessivas
    df_filtrado = df

    if resultado.value != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['resultado_processo'] == resultado.value]

    if responsavel_prisao.value != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['responsavel_prisao'] == responsavel_prisao.value]
    return (df_filtrado,)


@app.cell
def _(HeatMap, folium):
    def gera_mapa_calor(dados):
        if dados.empty:
            return None

        lat_media = dados['latitude'].mean()
        lon_media = dados['longitude'].mean()

        mapa_obj = folium.Map(location=[lat_media, lon_media], zoom_start=12)

        # Prepara a lista de coordenadas [[lat, lon], [lat, lon], ...]
        coordenadas = dados[['latitude', 'longitude']].values.tolist()

        # Adiciona a camada de calor ao mapa
        HeatMap(coordenadas).add_to(mapa_obj)

        return mapa_obj
    return (gera_mapa_calor,)


@app.cell
def gera_mapa_clusterizado(MarkerCluster, folium):
    def gera_mapa_clusterizado(dados):
        if dados.empty:
            return None

        lat_media = dados['latitude'].mean()
        lon_media = dados['longitude'].mean()

        mapa_obj = folium.Map(location=[lat_media, lon_media], zoom_start=12)
        marker_cluster = MarkerCluster().add_to(mapa_obj)

        for _, row in dados.iterrows():
            html_content = f"""
            <style>
                .popup-table {{ 
                    width: 100%; 
                    border-collapse: collapse; 
                    font-family: sans-serif; 
                    font-size: 10px;
                }}
                .popup-table tr:nth-child(even) {{ background-color: #f8f9fa; }}
                .popup-table td {{ padding: 4px; vertical-align: top; }}
                .popup-table td.label {{ font-weight: bold; width: 80px; }}
            </style>

            <div style="min-width: 250px; max-width: 350px;">
                <h4 style="margin-bottom: 8px; color: #2c3e50; border-bottom: 1px solid #ccc; font-size: 13px;">
                    Processo: {row['numero_do_processo']}
                </h4>
                <table class="popup-table">
                    <tr><td class="label">Data:</td><td>{row['data_fato']}</td></tr>
                    <tr><td class="label">Modus operandi:</td><td style="text-align: justify;">{row['modus_operandi_reu']}</td></tr>
                    <tr><td class="label">Alegação defensiva:</td><td>{row.get('alegacao_reu', 'N/A')}</td></tr>
                    <tr><td class="label">Sentença:</td><td>{row.get('resumo_sentenca', 'N/A')}</td></tr>
                </table>
            </div>
            """

            # Aumente um pouco o height se o texto for muito longo para evitar scroll
            iframe = folium.IFrame(html_content, width=370, height=280)
            popup_obj = folium.Popup(iframe, max_width=400)

            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=popup_obj,
                tooltip=f"Processo: {row['numero_do_processo']}",
                icon=folium.Icon(icon='info-sign', color='blue')
            ).add_to(marker_cluster)

        return mapa_obj
    return (gera_mapa_clusterizado,)


@app.cell
def _(df_filtrado, gera_mapa_calor, gera_mapa_clusterizado, tipo_mapa):
    if tipo_mapa.value == 'Calor':
        mapa_final = gera_mapa_calor(df_filtrado)
    else:
        mapa_final = gera_mapa_clusterizado(df_filtrado)   
    return (mapa_final,)


@app.cell
def _(mapa_final, mo):
    if mapa_final is not None:
        saida = mo.Html(mapa_final._repr_html_())
    else:
        saida = mo.md("Selecione outra opção.")

    saida
    return


@app.cell
def _(df_filtrado):
    df_filtrado
    return


if __name__ == "__main__":
    app.run()
