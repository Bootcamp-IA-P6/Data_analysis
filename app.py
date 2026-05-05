import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.decomposition import PCA

# ── Template global Plotly — tema oscuro ─────────────────────────────────────
_TEXT  = "#e8eaf0"
_BG    = "#1e2130"
_CARD  = "#252a3a"
_GRID  = "#353c55"

pio.templates["dark_airbnb"] = go.layout.Template(
    layout=go.Layout(
        font=dict(color=_TEXT, family="Inter, sans-serif", size=12),
        title=dict(font=dict(color=_TEXT, size=15), x=0.02),
        paper_bgcolor=_BG,
        plot_bgcolor=_BG,
        xaxis=dict(
            tickfont=dict(color=_TEXT, size=11),
            title_font=dict(color=_TEXT, size=12),
            gridcolor=_GRID, linecolor=_GRID, zerolinecolor=_GRID,
        ),
        yaxis=dict(
            tickfont=dict(color=_TEXT, size=11),
            title_font=dict(color=_TEXT, size=12),
            gridcolor=_GRID, linecolor=_GRID, zerolinecolor=_GRID,
        ),
        legend=dict(
            font=dict(color=_TEXT),
            title_font=dict(color=_TEXT),
            bgcolor="rgba(37,42,58,0.9)",
            bordercolor=_GRID, borderwidth=1,
        ),
        coloraxis=dict(colorbar=dict(
            tickfont=dict(color=_TEXT),
            title_font=dict(color=_TEXT),
        )),
    )
)
pio.templates.default = "dark_airbnb"

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Airbnb: Madrid vs Milán",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS — tema oscuro ──────────────────────────────────────────────────
st.markdown("""
<style>
/* ── FONDO GENERAL ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMain"] > div,
[data-testid="block-container"] {
    background-color: #1e2130 !important;
    color: #e8eaf0 !important;
}

/* ── Todo el texto del área principal ── */
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] span,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] div,
[data-testid="stAppViewContainer"] li,
[data-testid="stAppViewContainer"] td,
[data-testid="stAppViewContainer"] th {
    color: #e8eaf0 !important;
}

/* ── Títulos ── */
h1, h2, h3, h4 {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background-color: #141727 !important;
}
[data-testid="stSidebar"] * {
    color: #c8cfe8 !important;
    background-color: transparent !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background-color: #252a3a !important;
    color: #e8eaf0 !important;
    border: 1px solid #3d4560 !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] small {
    color: #7a82a8 !important;
}
[data-testid="stSidebar"] hr {
    border-color: #2e3450 !important;
}

/* ── DROPDOWNS (popover/listbox) — aplica a sidebar Y main ── */
[data-baseweb="popover"],
[data-baseweb="popover"] *,
[data-baseweb="menu"],
[data-baseweb="menu"] *,
[data-baseweb="select"] ul,
[data-baseweb="select"] li,
ul[role="listbox"],
ul[role="listbox"] li,
li[role="option"] {
    background-color: #252a3a !important;
    color: #e8eaf0 !important;
}
li[role="option"]:hover,
ul[role="listbox"] li:hover {
    background-color: #353c55 !important;
    color: #ffffff !important;
}
li[role="option"][aria-selected="true"],
ul[role="listbox"] li[aria-selected="true"] {
    background-color: #e63946 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* ── WIDGETS ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background-color: #252a3a !important;
    color: #e8eaf0 !important;
    border: 1px solid #3d4560 !important;
    border-radius: 8px !important;
}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background-color: #e63946 !important;
    color: #ffffff !important;
}
/* Slider */
[data-testid="stSlider"] [data-testid="stMarkdownContainer"] p {
    color: #e8eaf0 !important;
}
/* Radio buttons */
[data-testid="stRadio"] label,
[data-testid="stRadio"] p {
    color: #e8eaf0 !important;
}

/* ── MÉTRICAS ── */
[data-testid="metric-container"] {
    background-color: #252a3a !important;
    border: 1px solid #3d4560;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
[data-testid="stMetricValue"] {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}
[data-testid="stMetricLabel"] {
    color: #9aa0bf !important;
    font-size: 0.85rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── TARJETAS INFO ── */
.info-card {
    background: #252a3a;
    border-radius: 12px;
    padding: 20px 24px;
    border-left: 5px solid #e63946;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    margin-bottom: 16px;
    font-size: 0.95rem;
    color: #e8eaf0 !important;
    line-height: 1.6;
}
.info-card strong { color: #ffffff !important; }
.info-card.blue   { border-left-color: #5b9fc9; }
.info-card.green  { border-left-color: #2a9d8f; }
.info-card.purple { border-left-color: #8b83ff; }

/* ── ALERTAS ── */
[data-testid="stAlert"] {
    background-color: #252a3a !important;
    border-radius: 8px !important;
}
[data-testid="stAlert"] p,
[data-testid="stAlert"] div,
[data-testid="stAlert"] span {
    color: #e8eaf0 !important;
}

/* ── DIVISOR ── */
hr { border-color: #2e3450 !important; }

/* ── BOTÓN PRIMARIO ── */
.stButton > button[kind="primary"] {
    background-color: #e63946 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    border: none !important;
    padding: 0.5rem 2rem !important;
}
.stButton > button[kind="primary"]:hover {
    background-color: #c1121f !important;
    color: #ffffff !important;
}
.stButton > button {
    background-color: #252a3a !important;
    color: #e8eaf0 !important;
    border: 1px solid #3d4560 !important;
    border-radius: 8px !important;
}

/* ── DATAFRAMES ── */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)

sns.set_theme(style="dark", palette="muted")
plt.rcParams.update({
    "figure.facecolor": "#1e2130",
    "axes.facecolor":   "#1e2130",
    "axes.edgecolor":   "#3d4560",
    "axes.labelcolor":  "#e8eaf0",
    "xtick.color":      "#e8eaf0",
    "ytick.color":      "#e8eaf0",
    "text.color":       "#e8eaf0",
    "grid.color":       "#353c55",
})

# ── Cargar datos ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/airbnb_clean.csv")

df = load_data()

ALL_NUM_COLS = [
    "price", "minimum_nights", "number_of_reviews",
    "reviews_per_month", "calculated_host_listings_count", "availability_365"
]

LABELS_ES = {
    "price": "Precio",
    "minimum_nights": "Noches mínimas",
    "number_of_reviews": "Nº de reseñas",
    "reviews_per_month": "Reseñas/mes",
    "calculated_host_listings_count": "Anuncios del anfitrión",
    "availability_365": "Disponibilidad (días/año)"
}

CITY_COLORS = {"Madrid": "#e63946", "Milán": "#457b9d"}

# ── Navegación lateral ────────────────────────────────────────────────────────
st.sidebar.markdown("## Panel de navegación")
section = st.sidebar.selectbox(
    "Ir a",
    [
        "Resumen general",
        "Análisis de variables",
        "Visualizaciones avanzadas",
        "Clustering (KMeans)",
        "Resultados del clustering",
    ]
)

st.sidebar.divider()
st.sidebar.markdown("### Filtro global")
cities = ["Todas"] + sorted(df["ciudad"].unique().tolist())
selected_city = st.sidebar.selectbox("Ciudad", cities)

df_filtered = df.copy() if selected_city == "Todas" else df[df["ciudad"] == selected_city].copy()

st.sidebar.markdown(f"**{len(df_filtered):,}** anuncios seleccionados")
st.sidebar.divider()
st.sidebar.caption("Fuente: Inside Airbnb | 2026")

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 1 — RESUMEN GENERAL
# ─────────────────────────────────────────────────────────────────────────────
if section == "Resumen general":

    st.title("Airbnb: Madrid vs Milán")
    st.markdown("""
    <div class="info-card blue">
    Dashboard interactivo para comparar el mercado de alquiler a corto plazo en <strong>Madrid</strong> y <strong>Milán</strong>.
    Utiliza el panel lateral para navegar entre secciones y filtrar por ciudad.
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.subheader("Indicadores clave")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total anuncios", f"{len(df_filtered):,}")
    c2.metric("Precio mediano", f"€{df_filtered['price'].median():.0f}/noche")
    c3.metric("Disponibilidad media", f"{df_filtered['availability_365'].mean():.0f} días/año")
    c4.metric("Reseñas medias", f"{df_filtered['number_of_reviews'].mean():.0f}")

    st.divider()

    col_prev, col_null = st.columns([2, 1])
    with col_prev:
        st.subheader("Vista previa del dataset")
        st.dataframe(df_filtered.head(8), use_container_width=True)

    with col_null:
        st.subheader("Calidad de datos")
        total_nulls = df_filtered.isnull().sum().sum()
        if total_nulls == 0:
            st.success("Sin valores nulos en el dataset.")
        else:
            st.warning(f"Valores nulos: {total_nulls:,}")
            nd = df_filtered.isnull().sum()
            nd = nd[nd > 0].reset_index()
            nd.columns = ["Columna", "Nulos"]
            st.dataframe(nd, use_container_width=True)

        st.subheader("Distribución por ciudad")
        city_counts = df_filtered["ciudad"].value_counts().reset_index()
        city_counts.columns = ["Ciudad", "Anuncios"]
        st.dataframe(city_counts, use_container_width=True)

    st.divider()
    st.subheader("Vista rápida")

    col_h, col_b = st.columns(2)
    p99 = df_filtered["price"].quantile(0.99)
    df_p = df_filtered[df_filtered["price"] <= p99]

    with col_h:
        fig = px.histogram(
            df_p, x="price", color="ciudad",
            barmode="overlay", nbins=60, opacity=0.75,
            color_discrete_map=CITY_COLORS,
            labels={"price": "Precio (€/noche)", "ciudad": "Ciudad"},
            title="Distribución del precio por ciudad"
        )
        fig.update_layout(
            plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
            legend_title="Ciudad",
            font=dict(family="Inter, sans-serif", color="#e8eaf0")
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        room_counts = (
            df_filtered.groupby(["ciudad", "room_type"], observed=True)
            .size().reset_index(name="count")
        )
        fig2 = px.bar(
            room_counts, x="room_type", y="count", color="ciudad",
            barmode="group", color_discrete_map=CITY_COLORS,
            labels={"room_type": "Tipo de alojamiento", "count": "Anuncios", "ciudad": "Ciudad"},
            title="Tipos de alojamiento por ciudad"
        )
        fig2.update_layout(
            plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
            legend_title="Ciudad",
            font=dict(family="Inter, sans-serif", color="#e8eaf0")
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    <div class="info-card green">
    La mayoría de los anuncios son <strong>pisos/casas completas</strong>. Los precios presentan una distribución
    muy asimétrica — la <strong>mediana</strong> es un indicador más fiable que la media.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 2 — ANÁLISIS DE VARIABLES
# ─────────────────────────────────────────────────────────────────────────────
elif section == "Análisis de variables":

    st.title("Análisis de variables")
    st.markdown("""
    <div class="info-card">
    Identifica qué variables son más relevantes y cómo se relacionan con el <strong>precio</strong>.
    Usa los controles para explorar distribuciones y comparativas entre ciudades.
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # --- Correlación con precio ---
    st.subheader("Correlación con el precio")

    corr_vals = (
        df_filtered[ALL_NUM_COLS].corr()["price"]
        .drop("price")
        .sort_values(key=abs, ascending=False)
        .reset_index()
    )
    corr_vals.columns = ["Variable", "Correlación con precio"]
    corr_vals["Variable ES"] = corr_vals["Variable"].map(LABELS_ES)

    col_tbl, col_bar = st.columns([2, 3])
    with col_tbl:
        st.dataframe(
            corr_vals[["Variable ES", "Correlación con precio"]]
            .style.format({"Correlación con precio": "{:.3f}"})
            .set_properties(**{"background-color": "#252a3a", "color": "#e8eaf0", "font-weight": "600"})
            .bar(subset=["Correlación con precio"], color=["#457b9d", "#e63946"],
                 vmin=corr_vals["Correlación con precio"].min(),
                 vmax=corr_vals["Correlación con precio"].max()),
            use_container_width=True
        )
    with col_bar:
        corr_min = corr_vals["Correlación con precio"].min()
        corr_max = corr_vals["Correlación con precio"].max()
        fig = px.bar(
            corr_vals, x="Correlación con precio", y="Variable ES",
            orientation="h",
            color="Correlación con precio",
            color_continuous_scale="RdBu",
            range_color=[corr_min, corr_max],
            title="Correlación de Pearson con el precio"
        )
        fig.update_layout(
            coloraxis_showscale=False,
            yaxis={"categoryorder": "total ascending"},
            xaxis={"range": [corr_min * 1.15, corr_max * 1.15 if corr_max != 0 else 0.01]},
            plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
            font=dict(color="#e8eaf0")
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="info-card green">
    <strong>Insight:</strong> La disponibilidad y el nº de anuncios del anfitrión muestran la mayor correlación
    con el precio. Los anuncios con muchas reseñas tienden a ser más económicos.
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # --- Explorador de distribuciones ---
    st.subheader("Explorador de distribuciones")
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        feat_x = st.selectbox("Variable", ALL_NUM_COLS, index=0,
                              format_func=lambda x: LABELS_ES.get(x, x))
    with col_sel2:
        plot_type = st.radio("Tipo de gráfico", ["Histograma", "Boxplot", "Violín"], horizontal=True)

    p99 = df_filtered[feat_x].quantile(0.99)
    df_feat = df_filtered[df_filtered[feat_x] <= p99]

    if plot_type == "Histograma":
        fig = px.histogram(
            df_feat, x=feat_x, color="ciudad", barmode="overlay",
            nbins=50, opacity=0.75, color_discrete_map=CITY_COLORS,
            labels={feat_x: LABELS_ES.get(feat_x, feat_x), "ciudad": "Ciudad"}
        )
    elif plot_type == "Boxplot":
        fig = px.box(
            df_feat, x="ciudad", y=feat_x, color="ciudad",
            color_discrete_map=CITY_COLORS,
            labels={feat_x: LABELS_ES.get(feat_x, feat_x), "ciudad": "Ciudad"}
        )
    else:
        fig = px.violin(
            df_feat, x="ciudad", y=feat_x, color="ciudad",
            box=True, color_discrete_map=CITY_COLORS,
            labels={feat_x: LABELS_ES.get(feat_x, feat_x), "ciudad": "Ciudad"}
        )
    fig.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130", showlegend=True, font=dict(color="#e8eaf0"))
    st.plotly_chart(fig, use_container_width=True)
    st.divider()

    # --- Scatter interactivo ---
    st.subheader("Comparativa entre dos variables")
    col_xa, col_ya = st.columns(2)
    with col_xa:
        sc_x = st.selectbox("Eje X", ALL_NUM_COLS, index=2, key="sc_x",
                            format_func=lambda x: LABELS_ES.get(x, x))
    with col_ya:
        sc_y = st.selectbox("Eje Y", ALL_NUM_COLS, index=0, key="sc_y",
                            format_func=lambda x: LABELS_ES.get(x, x))

    p95x = df_filtered[sc_x].quantile(0.95)
    p95y = df_filtered[sc_y].quantile(0.95)
    df_sc = df_filtered[(df_filtered[sc_x] <= p95x) & (df_filtered[sc_y] <= p95y)]

    fig_sc = px.scatter(
        df_sc, x=sc_x, y=sc_y, color="ciudad",
        color_discrete_map=CITY_COLORS, opacity=0.4,
        hover_data=["neighbourhood", "room_type"],
        trendline="ols",
        labels={sc_x: LABELS_ES.get(sc_x, sc_x), sc_y: LABELS_ES.get(sc_y, sc_y), "ciudad": "Ciudad"},
        title=f"{LABELS_ES.get(sc_x, sc_x)} vs {LABELS_ES.get(sc_y, sc_y)}"
    )
    fig_sc.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130", font=dict(color="#e8eaf0"))
    st.plotly_chart(fig_sc, use_container_width=True)
    st.divider()

    # --- Top barrios ---
    st.subheader("Barrios más caros")
    top_n = st.slider("Número de barrios a mostrar", 5, 20, 10)

    if selected_city == "Todas":
        col_m, col_mi = st.columns(2)
        city_containers = [("Madrid", col_m), ("Milán", col_mi)]
    else:
        city_containers = [(selected_city, st)]

    for city_name, container in city_containers:
        top = (
            df[df["ciudad"] == city_name]
            .groupby("neighbourhood")["price"].mean()
            .sort_values(ascending=False).head(top_n).reset_index()
        )
        top.columns = ["Barrio", "Precio medio (€)"]
        fig_nb = px.bar(
            top, y="Barrio", x="Precio medio (€)", orientation="h",
            color_discrete_sequence=[CITY_COLORS[city_name]],
            title=f"Top {top_n} barrios — {city_name}"
        )
        fig_nb.update_layout(
            yaxis={"categoryorder": "total ascending"},
            plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
            font=dict(color="#e8eaf0")
        )
        container.plotly_chart(fig_nb, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 3 — VISUALIZACIONES AVANZADAS
# ─────────────────────────────────────────────────────────────────────────────
elif section == "Visualizaciones avanzadas":

    st.title("Visualizaciones avanzadas")
    st.markdown("""
    <div class="info-card purple">
    Heatmaps, pairplots y visualizaciones 3D para detectar patrones y relaciones entre variables
    que no son visibles en gráficos simples.
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # --- Heatmap correlación ---
    st.subheader("Mapa de calor — Correlaciones")

    if selected_city == "Todas":
        col_hm, col_hm2 = st.columns(2)
        hm_pairs = [("Madrid", col_hm), ("Milán", col_hm2)]
    else:
        hm_pairs = [(selected_city, st)]

    for city_name, container in hm_pairs:
        subset = df[df["ciudad"] == city_name][ALL_NUM_COLS].dropna()
        corr = subset.corr().round(2)
        labels_renamed = [LABELS_ES.get(c, c) for c in corr.columns]
        fig_hm, ax = plt.subplots(figsize=(7, 5))
        sns.heatmap(
            corr, annot=True, fmt=".2f", cmap="coolwarm",
            vmin=-1, vmax=1, linewidths=0.6, ax=ax,
            xticklabels=labels_renamed, yticklabels=labels_renamed,
            annot_kws={"size": 9}
        )
        ax.set_title(f"Correlaciones — {city_name}", fontsize=13, fontweight="bold", pad=12)
        plt.xticks(rotation=30, ha="right", fontsize=8)
        plt.yticks(rotation=0, fontsize=8)
        plt.tight_layout()
        container.pyplot(fig_hm, use_container_width=True)
        plt.close()

    st.markdown("""
    <div class="info-card green">
    Las correlaciones son generalmente débiles. <strong>Reseñas/mes</strong> y <strong>Nº de reseñas</strong>
    están muy correlacionadas entre sí — en modelado, basta con incluir una de las dos.
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # --- Pairplot ---
    st.subheader("Pairplot — Relaciones entre variables")
    st.markdown("Selecciona hasta 4 variables para explorar sus distribuciones y relaciones cruzadas.")

    pair_vars = st.multiselect(
        "Variables",
        ALL_NUM_COLS,
        default=["price", "number_of_reviews", "availability_365"],
        format_func=lambda x: LABELS_ES.get(x, x)
    )

    if len(pair_vars) < 2:
        st.warning("Selecciona al menos 2 variables.")
    else:
        p99_mask = pd.Series([True] * len(df_filtered), index=df_filtered.index)
        for v in pair_vars:
            p99_mask &= df_filtered[v] <= df_filtered[v].quantile(0.99)
        df_pair = df_filtered[p99_mask][pair_vars + ["ciudad"]].dropna()
        df_pair = df_pair.rename(columns=LABELS_ES)

        if len(df_pair) > 5000:
            df_pair = df_pair.sample(5000, random_state=42)

        pair_labels = [LABELS_ES.get(v, v) for v in pair_vars]
        g = sns.pairplot(
            df_pair, hue="ciudad",
            vars=pair_labels,
            palette=CITY_COLORS,
            plot_kws={"alpha": 0.35, "s": 12},
            diag_kind="kde"
        )
        g.fig.suptitle("Pairplot de variables seleccionadas", y=1.01, fontsize=13, fontweight="bold")
        for ax in g.axes.flatten():
            ax.set_xlabel(ax.get_xlabel(), fontsize=8)
            ax.set_ylabel(ax.get_ylabel(), fontsize=8)
        st.pyplot(g.fig, use_container_width=True)
        plt.close("all")

    st.markdown("""
    <div class="info-card">
    La diagonal muestra la distribución de cada variable por ciudad.
    Los scatterplots fuera de la diagonal revelan la relación entre pares de variables.
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # --- Scatter 3D ---
    st.subheader("Scatter 3D interactivo")
    st.markdown("Explora tres variables a la vez, coloreadas por ciudad. Rota el gráfico para distintas perspectivas.")

    col_3a, col_3b, col_3c = st.columns(3)
    with col_3a:
        ax3 = st.selectbox("Eje X", ALL_NUM_COLS, index=0, key="3dx",
                           format_func=lambda x: LABELS_ES.get(x, x))
    with col_3b:
        ay3 = st.selectbox("Eje Y", ALL_NUM_COLS, index=2, key="3dy",
                           format_func=lambda x: LABELS_ES.get(x, x))
    with col_3c:
        az3 = st.selectbox("Eje Z", ALL_NUM_COLS, index=5, key="3dz",
                           format_func=lambda x: LABELS_ES.get(x, x))

    df_3d = df_filtered[
        (df_filtered[ax3] <= df_filtered[ax3].quantile(0.95)) &
        (df_filtered[ay3] <= df_filtered[ay3].quantile(0.95)) &
        (df_filtered[az3] <= df_filtered[az3].quantile(0.95))
    ].dropna(subset=[ax3, ay3, az3])

    if len(df_3d) > 6000:
        df_3d = df_3d.sample(6000, random_state=42)

    fig_3d = px.scatter_3d(
        df_3d, x=ax3, y=ay3, z=az3,
        color="ciudad", opacity=0.55,
        color_discrete_map=CITY_COLORS,
        labels={
            ax3: LABELS_ES.get(ax3, ax3),
            ay3: LABELS_ES.get(ay3, ay3),
            az3: LABELS_ES.get(az3, az3),
            "ciudad": "Ciudad"
        },
        title=f"3D: {LABELS_ES.get(ax3,ax3)} / {LABELS_ES.get(ay3,ay3)} / {LABELS_ES.get(az3,az3)}"
    )
    fig_3d.update_traces(marker=dict(size=3))
    fig_3d.update_layout(legend_title="Ciudad")
    st.plotly_chart(fig_3d, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 4 — CLUSTERING
# ─────────────────────────────────────────────────────────────────────────────
elif section == "Clustering (KMeans)":

    st.title("Clustering — KMeans")
    st.markdown("""
    <div class="info-card purple">
    Agrupa los anuncios en segmentos según sus características numéricas.
    Selecciona las variables, analiza el número óptimo de grupos y ejecuta el modelo.
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # --- Selección de variables ---
    st.subheader("1. Selección de variables")
    st.markdown("""
    <div class="info-card">
    Usa variables con significado de negocio y baja redundancia.
    <strong>Reseñas/mes</strong> y <strong>Nº de reseñas</strong> están muy correlacionadas — elige solo una.
    </div>
    """, unsafe_allow_html=True)

    selected_feats = st.multiselect(
        "Variables para clustering",
        ALL_NUM_COLS,
        default=["price", "availability_365", "number_of_reviews", "minimum_nights"],
        format_func=lambda x: LABELS_ES.get(x, x)
    )

    if len(selected_feats) < 2:
        st.warning("Selecciona al menos 2 variables para ejecutar el clustering.")
        st.stop()

    st.divider()

    # --- Método del codo ---
    st.subheader("2. Número óptimo de clusters (Método del codo)")

    @st.cache_data
    def compute_elbow(data_hash, feats, max_k=10):
        inertias, sil_scores = [], []
        X = df_filtered[feats].dropna()
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        for k in range(2, max_k + 1):
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = km.fit_predict(X_scaled)
            inertias.append(km.inertia_)
            sil_scores.append(silhouette_score(X_scaled, labels, sample_size=min(5000, len(X_scaled))))
        return list(range(2, max_k + 1)), inertias, sil_scores

    ks, inertias, sil_scores = compute_elbow(
        hash(tuple(sorted(selected_feats)) + (selected_city,)),
        selected_feats
    )

    col_elbow, col_sil = st.columns(2)
    with col_elbow:
        fig_elbow = go.Figure()
        fig_elbow.add_trace(go.Scatter(
            x=ks, y=inertias, mode="lines+markers",
            marker=dict(color="#e63946", size=9, line=dict(color="white", width=2)),
            line=dict(color="#e63946", width=2.5),
            name="Inercia"
        ))
        fig_elbow.update_layout(
            title="Curva del codo", xaxis_title="Número de clusters (k)",
            yaxis_title="Inercia (suma de cuadrados intracluster)",
            plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
            font=dict(color="#e8eaf0")
        )
        st.plotly_chart(fig_elbow, use_container_width=True)

    with col_sil:
        fig_sil = go.Figure()
        fig_sil.add_trace(go.Scatter(
            x=ks, y=sil_scores, mode="lines+markers",
            marker=dict(color="#457b9d", size=9, line=dict(color="white", width=2)),
            line=dict(color="#457b9d", width=2.5),
            name="Silhouette"
        ))
        fig_sil.update_layout(
            title="Coeficiente Silhouette", xaxis_title="Número de clusters (k)",
            yaxis_title="Silhouette (mayor = mejor)",
            plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
            font=dict(color="#e8eaf0")
        )
        st.plotly_chart(fig_sil, use_container_width=True)

    st.markdown("""
    <div class="info-card green">
    Elige <strong>k</strong> donde la curva del codo se dobla y el Silhouette es alto.
    Un Silhouette superior a <strong>0.3</strong> indica una separación razonable entre clusters.
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # --- Ejecutar clustering ---
    st.subheader("3. Ejecutar el modelo")
    n_clusters = st.slider("Número de clusters (k)", min_value=2, max_value=10, value=4)

    if st.button("Ejecutar KMeans", type="primary"):
        X_raw = df_filtered[selected_feats].dropna()
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_raw)

        km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)

        sil = silhouette_score(X_scaled, labels, sample_size=min(5000, len(X_scaled)))
        db = davies_bouldin_score(X_scaled, labels)

        df_cluster = X_raw.copy()
        df_cluster["Cluster"] = labels.astype(str)
        df_cluster["ciudad"] = df_filtered.loc[X_raw.index, "ciudad"].values
        df_cluster["neighbourhood"] = df_filtered.loc[X_raw.index, "neighbourhood"].values

        st.session_state["cluster_df"] = df_cluster
        st.session_state["cluster_feats"] = selected_feats
        st.session_state["cluster_metrics"] = {"silhouette": sil, "davies_bouldin": db, "k": n_clusters}

        st.success(f"Clustering completado — Silhouette: {sil:.3f} | Davies-Bouldin: {db:.3f}")
        st.info("Ve a **Resultados del clustering** en el panel lateral para explorar los resultados.")

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN 5 — RESULTADOS DEL CLUSTERING
# ─────────────────────────────────────────────────────────────────────────────
elif section == "Resultados del clustering":

    st.title("Resultados del clustering")

    if "cluster_df" not in st.session_state:
        st.warning("Aún no se ha ejecutado ningún clustering. Ve a **Clustering (KMeans)** y ejecuta el modelo.")
        st.stop()

    df_cluster = st.session_state["cluster_df"]
    feats = st.session_state["cluster_feats"]
    metrics = st.session_state["cluster_metrics"]

    st.divider()

    # --- Métricas ---
    st.subheader("Métricas del modelo")
    m1, m2, m3 = st.columns(3)
    m1.metric("Clusters (k)", metrics["k"])
    m2.metric("Silhouette", f"{metrics['silhouette']:.3f}",
              help="Rango [-1, 1]. Mayor = clusters mejor separados.")
    m3.metric("Davies-Bouldin", f"{metrics['davies_bouldin']:.3f}",
              help="Menor = mejor. Mide compacidad vs separación.")

    st.markdown(f"""
    <div class="info-card blue">
    Con <strong>k={metrics['k']}</strong>, el modelo obtiene un Silhouette de <strong>{metrics['silhouette']:.3f}</strong>.
    Valores por encima de 0.3 indican estructura significativa en los datos.
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # --- Perfil de clusters ---
    st.subheader("Perfil de cada cluster (valores medios)")
    profile = df_cluster.groupby("Cluster")[feats].mean().round(2)
    profile.columns = [LABELS_ES.get(c, c) for c in profile.columns]
    st.dataframe(
        profile.style
        .format("{:.2f}")
        .set_properties(**{"background-color": "#252a3a", "color": "#e8eaf0", "font-weight": "600"}),
        use_container_width=True
    )
    st.markdown("""
    <div class="info-card green">
    Cada fila representa las características medias de los anuncios en ese cluster.
    Busca clusters con <strong>precio alto + pocas reseñas</strong> (premium) vs <strong>precio bajo + muchas reseñas</strong> (populares).
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # --- PCA 2D y 3D ---
    st.subheader("Visualización de clusters (PCA)")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_cluster[feats])
    pca = PCA(n_components=2, random_state=42)
    components = pca.fit_transform(X_scaled)
    df_pca = pd.DataFrame(components, columns=["PC1", "PC2"])
    df_pca["Cluster"] = df_cluster["Cluster"].values
    df_pca["ciudad"] = df_cluster["ciudad"].values

    col_pca, col_3d = st.columns(2)
    with col_pca:
        fig_pca = px.scatter(
            df_pca.sample(min(8000, len(df_pca)), random_state=42),
            x="PC1", y="PC2", color="Cluster", opacity=0.6,
            title="Clusters en espacio PCA (2D)",
            labels={
                "PC1": f"PC1 ({pca.explained_variance_ratio_[0]:.1%} varianza)",
                "PC2": f"PC2 ({pca.explained_variance_ratio_[1]:.1%} varianza)"
            }
        )
        fig_pca.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130", font=dict(color="#e8eaf0"))
        st.plotly_chart(fig_pca, use_container_width=True)

    with col_3d:
        if len(feats) >= 3:
            pca3 = PCA(n_components=3, random_state=42)
            comp3 = pca3.fit_transform(X_scaled)
            df_pca3 = pd.DataFrame(comp3, columns=["PC1", "PC2", "PC3"])
            df_pca3["Cluster"] = df_cluster["Cluster"].values
            df_pca3_s = df_pca3.sample(min(6000, len(df_pca3)), random_state=42)
            fig_3d = px.scatter_3d(
                df_pca3_s, x="PC1", y="PC2", z="PC3",
                color="Cluster", opacity=0.5,
                title="Clusters en espacio PCA (3D)"
            )
            fig_3d.update_traces(marker=dict(size=3))
            st.plotly_chart(fig_3d, use_container_width=True)
        else:
            st.info("Selecciona 3 o más variables para activar la vista 3D.")

    st.divider()

    # --- Distribución por ciudad ---
    st.subheader("Distribución de clusters por ciudad")
    dist = df_cluster.groupby(["ciudad", "Cluster"]).size().reset_index(name="Anuncios")
    fig_dist = px.bar(
        dist, x="Cluster", y="Anuncios", color="ciudad",
        barmode="group", color_discrete_map=CITY_COLORS,
        labels={"ciudad": "Ciudad"},
        title="Anuncios por cluster y ciudad"
    )
    fig_dist.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130", font=dict(color="#e8eaf0"))
    st.plotly_chart(fig_dist, use_container_width=True)
    st.divider()

    # --- Boxplots por cluster ---
    st.subheader("Distribución de variables por cluster")
    feat_box = st.selectbox(
        "Variable", feats, index=0,
        format_func=lambda x: LABELS_ES.get(x, x)
    )
    fig_box = px.box(
        df_cluster, x="Cluster", y=feat_box, color="Cluster",
        title=f"{LABELS_ES.get(feat_box, feat_box)} por cluster",
        labels={feat_box: LABELS_ES.get(feat_box, feat_box)}
    )
    fig_box.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130", font=dict(color="#e8eaf0"))
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("""
    <div class="info-card">
    Una separación clara en los boxplots confirma que los clusters capturan tipos de anuncios distintos.
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # --- Heatmap centroides ---
    st.subheader("Mapa de calor de centroides")
    profile_raw = df_cluster.groupby("Cluster")[feats].mean().round(2)
    profile_norm = (profile_raw - profile_raw.min()) / (profile_raw.max() - profile_raw.min() + 1e-9)
    profile_norm.columns = [LABELS_ES.get(c, c) for c in profile_norm.columns]

    fig_cent, ax = plt.subplots(figsize=(max(7, len(feats) * 1.4), max(3, metrics["k"] * 0.8)))
    sns.heatmap(
        profile_norm, annot=profile_raw.values, fmt=".1f",
        cmap="YlOrRd", linewidths=0.6, ax=ax,
        annot_kws={"size": 10, "weight": "bold"}
    )
    ax.set_title("Centroides normalizados (valores reales anotados)", fontsize=13,
                 fontweight="bold", pad=12)
    plt.xticks(fontsize=9)
    plt.yticks(fontsize=9, rotation=0)
    plt.tight_layout()
    st.pyplot(fig_cent, use_container_width=True)
    plt.close()

    st.markdown("""
    <div class="info-card purple">
    Las celdas más oscuras indican valores más altos relativos a otros clusters.
    Úsalo para etiquetar los grupos: por ejemplo, precio alto + alta disponibilidad = <strong>anuncios premium</strong>.
    </div>
    """, unsafe_allow_html=True)
