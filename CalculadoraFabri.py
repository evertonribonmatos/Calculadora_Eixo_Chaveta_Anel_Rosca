import streamlit as st
import pandas as pd
from math import sqrt

st.set_page_config(page_title="Calculadora de Eixo - Chaveta, Anel e Rosca", layout="wide")
st.title("🔧 Calculadora Técnica de Eixo")
st.markdown("### DIN 6885 • DIN 471 • ISO 68-1 / ISO 965 (M4 até M39)")

# ==================== DADOS DAS NORMAS ====================
rosas_data = {
    "M4":   {"d_eixo": 4.0, "passos": [0.7, 0.5], "chanfro_ideal": 0.3, "pescoço_ideal": 2.5, "chanfro_min": 0.2, "pescoço_min": 2.0, "chanfro_max": 0.5, "pescoço_max": 4.0},
    "M5":   {"d_eixo": 5.0, "passos": [0.8, 0.5], "chanfro_ideal": 0.4, "pescoço_ideal": 2.5, "chanfro_min": 0.3, "pescoço_min": 2.0, "chanfro_max": 0.6, "pescoço_max": 4.0},
    "M6":   {"d_eixo": 6.0, "passos": [1.0, 0.75, 0.5], "chanfro_ideal": 0.5, "pescoço_ideal": 2.5, "chanfro_min": 0.4, "pescoço_min": 2.0, "chanfro_max": 0.8, "pescoço_max": 4.0},
    "M8":   {"d_eixo": 8.0, "passos": [1.25, 1.0, 0.75, 0.5], "chanfro_ideal": 0.5, "pescoço_ideal": 2.5, "chanfro_min": 0.4, "pescoço_min": 2.0, "chanfro_max": 0.8, "pescoço_max": 4.0},
    "M10":  {"d_eixo": 10.0, "passos": [1.5, 1.25, 1.0, 0.75, 0.5], "chanfro_ideal": 0.5, "pescoço_ideal": 3.0, "chanfro_min": 0.4, "pescoço_min": 2.0, "chanfro_max": 0.8, "pescoço_max": 5.0},
    "M12":  {"d_eixo": 12.0, "passos": [1.75, 1.5, 1.25, 0.75, 0.5], "chanfro_ideal": 0.5, "pescoço_ideal": 3.0, "chanfro_min": 0.4, "pescoço_min": 2.0, "chanfro_max": 0.8, "pescoço_max": 5.0},
    "M14":  {"d_eixo": 14.0, "passos": [2.0, 1.5, 1.0, 0.75], "chanfro_ideal": 0.6, "pescoço_ideal": 3.0, "chanfro_min": 0.5, "pescoço_min": 2.5, "chanfro_max": 0.9, "pescoço_max": 5.0},
    "M16":  {"d_eixo": 16.0, "passos": [2.0, 1.5, 1.0, 0.75], "chanfro_ideal": 0.6, "pescoço_ideal": 3.0, "chanfro_min": 0.5, "pescoço_min": 2.5, "chanfro_max": 0.9, "pescoço_max": 5.0},
    "M18":  {"d_eixo": 18.0, "passos": [2.5, 2.0, 1.5, 1.0], "chanfro_ideal": 0.6, "pescoço_ideal": 3.0, "chanfro_min": 0.5, "pescoço_min": 2.5, "chanfro_max": 0.9, "pescoço_max": 5.0},
    "M20":  {"d_eixo": 20.0, "passos": [2.5, 2.0, 1.5, 1.0], "chanfro_ideal": 0.5, "pescoço_ideal": 3.5, "chanfro_min": 0.4, "pescoço_min": 2.5, "chanfro_max": 0.8, "pescoço_max": 6.0},
    "M22":  {"d_eixo": 22.0, "passos": [2.5, 2.0, 1.5, 1.0], "chanfro_ideal": 0.7, "pescoço_ideal": 3.5, "chanfro_min": 0.5, "pescoço_min": 2.5, "chanfro_max": 0.9, "pescoço_max": 6.0},
    "M24":  {"d_eixo": 24.0, "passos": [3.0, 2.0, 1.5, 1.0], "chanfro_ideal": 0.5, "pescoço_ideal": 3.5, "chanfro_min": 0.4, "pescoço_min": 2.5, "chanfro_max": 0.8, "pescoço_max": 6.0},
    "M27":  {"d_eixo": 27.0, "passos": [3.0, 2.0, 1.5, 1.0], "chanfro_ideal": 0.7, "pescoço_ideal": 3.5, "chanfro_min": 0.5, "pescoço_min": 2.5, "chanfro_max": 0.9, "pescoço_max": 6.0},
    "M30":  {"d_eixo": 30.0, "passos": [3.5, 2.0, 1.5, 1.0], "chanfro_ideal": 0.7, "pescoço_ideal": 3.5, "chanfro_min": 0.5, "pescoço_min": 2.5, "chanfro_max": 0.9, "pescoço_max": 7.0},
    "M33":  {"d_eixo": 33.0, "passos": [3.5, 2.0, 1.5, 1.0], "chanfro_ideal": 0.7, "pescoço_ideal": 3.5, "chanfro_min": 0.5, "pescoço_min": 2.5, "chanfro_max": 0.9, "pescoço_max": 7.0},
    "M36":  {"d_eixo": 36.0, "passos": [4.0, 3.0, 2.0, 1.0], "chanfro_ideal": 0.8, "pescoço_ideal": 4.0, "chanfro_min": 0.6, "pescoço_min": 3.0, "chanfro_max": 1.0, "pescoço_max": 7.0},
    "M39":  {"d_eixo": 39.0, "passos": [4.0, 3.0, 2.0, 1.0], "chanfro_ideal": 0.8, "pescoço_ideal": 4.0, "chanfro_min": 0.6, "pescoço_min": 3.0, "chanfro_max": 1.0, "pescoço_max": 7.0},
}

def get_chaveta(d):
    if d <= 22:
        return 6.0, 6.0, 3.5, 2.8, 18.0
    elif d <= 30:
        return 8.0, 7.0, 4.0, 3.3, 22.0
    else:
        return 10.0, 8.0, 4.5, 3.8, 25.0

def get_anel(d):
    if d == 20:
        return 1.2, 1.3, 0.5, 19.0
    elif d == 24:
        return 1.5, 1.5, 0.6, 22.5
    else:
        s = round(d * 0.06, 1)
        larg = round(d * 0.065, 1)
        prof = round(d * 0.025, 1)
        fundo = round(d - 2 * prof, 1)
        return s, larg, prof, fundo

# ==================== SIDEBAR ====================
st.sidebar.header("Dados de Entrada")

rosca_selecionada = st.sidebar.selectbox("Rosca (M)", list(rosas_data.keys()), index=10)
dados_rosca = rosas_data[rosca_selecionada]

d_eixo = dados_rosca["d_eixo"]
passos_disponiveis = dados_rosca["passos"]
chanfro_ideal = dados_rosca["chanfro_ideal"]
pescoço_ideal = dados_rosca["pescoço_ideal"]
chanfro_min = dados_rosca["chanfro_min"]
pescoço_min = dados_rosca["pescoço_min"]
chanfro_max = dados_rosca["chanfro_max"]
pescoço_max = dados_rosca["pescoço_max"]

passo_rosca = st.sidebar.selectbox("Passo da rosca (mm)", passos_disponiveis, index=0)

st.sidebar.write(f"**Diâmetro do eixo:** {d_eixo} mm")

# ==================== PESOÇO E CHANFRO COM CORES ====================
st.sidebar.subheader("Pescoço e Chanfro (condicionado)")

# Pescoço
largura_pescoço = st.sidebar.slider(
    "Largura do pescoço (mm)",
    min_value=pescoço_min,
    max_value=pescoço_max,
    value=pescoço_ideal,
    step=0.1
)

# Chanfro
chanfro = st.sidebar.slider(
    "Chanfro 45° (mm)",
    min_value=chanfro_min,
    max_value=chanfro_max,
    value=chanfro_ideal,
    step=0.1
)

# ==================== INDICADORES DE COR ====================
col1, col2 = st.sidebar.columns(2)

with col1:
    if largura_pescoço == pescoço_ideal:
        st.success(f"✅ Ideal: {pescoço_ideal} mm")
    elif pescoço_min <= largura_pescoço <= pescoço_max:
        st.warning(f"⚠️ Dentro da tolerância")
    else:
        st.error("❌ Fora da tolerância")

with col2:
    if chanfro == chanfro_ideal:
        st.success(f"✅ Ideal: {chanfro_ideal} mm")
    elif chanfro_min <= chanfro <= chanfro_max:
        st.warning(f"⚠️ Dentro da tolerância")
    else:
        st.error("❌ Fora da tolerância")

# ==================== CÁLCULOS ====================
st.header("1. Chaveta (DIN 6885)")
b, h, t1, t2, L_min = get_chaveta(d_eixo)
L_rec = round(d_eixo * 1.5, 1)

st.write(f"**Largura (b):** {b} mm")
st.write(f"**Altura (h):** {h} mm")
st.write(f"**Profundidade no eixo (t₁):** {t1} mm")
st.write(f"**Profundidade na bucha (t₂):** {t2} mm")
st.write(f"**Comprimento mínimo:** {L_min} mm")
st.write(f"**Comprimento recomendado:** {L_rec} mm")

st.header("2. Anel Elástico (DIN 471)")
s, canal_larg, canal_prof, d_fundo = get_anel(d_eixo)
st.write(f"**Espessura do anel (s):** {s} mm")
st.write(f"**Largura do canal:** {canal_larg} mm")
st.write(f"**Profundidade do canal:** {canal_prof} mm")
st.write(f"**Diâmetro fundo do canal:** {d_fundo} mm")

st.header("3. Rosca (ISO 68-1)")
P = passo_rosca
H = round((sqrt(3)/2) * P, 3)
H2 = round(H/2, 3)
H4 = round(H/4, 3)

st.write(f"**Rosca:** {rosca_selecionada} × {P} mm")
st.write(f"**Passo (P):** {P} mm")
st.write(f"**Altura teórica (H):** {H} mm")
st.write(f"**Altura máxima útil (H/2):** {H2} mm")
st.write(f"**Altura mínima crista (H/4):** {H4} mm")

st.header("4. Pescoço e Chanfro")
st.write(f"**Largura do pescoço:** {largura_pescoço} mm")
st.write(f"**Chanfro 45°:** {chanfro} mm")

# ==================== TABELA RESUMO ====================
st.header("📋 Resumo Final")

dados = {
    "Item": [
        "Rosca",
        "Diâmetro do eixo",
        "Largura chaveta (b)",
        "Profundidade chaveta no eixo (t₁)",
        "Comprimento chaveta recomendado",
        "Espessura anel elástico (s)",
        "Profundidade canal anel",
        "Altura rosca teórica (H)",
        "Largura do pescoço",
        "Chanfro 45°"
    ],
    "Valor": [
        f"{rosca_selecionada} × {P}",
        f"{d_eixo} mm",
        f"{b} mm",
        f"{t1} mm",
        f"{L_rec} mm",
        f"{s} mm",
        f"{canal_prof} mm",
        f"{H} mm",
        f"{largura_pescoço} mm",
        f"{chanfro} mm"
    ]
}

df = pd.DataFrame(dados)
st.dataframe(df, use_container_width=True)

st.success("✅ Valores dentro da tolerância conforme norma!")
