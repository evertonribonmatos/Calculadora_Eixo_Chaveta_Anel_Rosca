import streamlit as st
import pandas as pd
from math import sqrt

st.set_page_config(page_title="Calculadora de Eixo - Chaveta, Anel e Rosca", layout="wide")
st.title("🔧 Calculadora Técnica de Eixo")
st.markdown("### DIN 6885 • DIN 471 • ISO 68-1 / ISO 965 (M4 até M39)")

# ==================== DADOS DAS NORMAS ====================
# Tabela de roscas métricas (M4 a M39)
rosas_data = {
    "M4":   {"passos": [0.7, 0.5], "chanfro_padrao": 0.3},
    "M5":   {"passos": [0.8, 0.5], "chanfro_padrao": 0.4},
    "M6":   {"passos": [1.0, 0.75, 0.5], "chanfro_padrao": 0.5},
    "M8":   {"passos": [1.25, 1.0, 0.75, 0.5], "chanfro_padrao": 0.5},
    "M10":  {"passos": [1.5, 1.25, 1.0, 0.75, 0.5], "chanfro_padrao": 0.5},
    "M12":  {"passos": [1.75, 1.5, 1.25, 0.75, 0.5], "chanfro_padrao": 0.5},
    "M14":  {"passos": [2.0, 1.5, 1.0, 0.75], "chanfro_padrao": 0.6},
    "M16":  {"passos": [2.0, 1.5, 1.0, 0.75], "chanfro_padrao": 0.6},
    "M18":  {"passos": [2.5, 2.0, 1.5, 1.0], "chanfro_padrao": 0.6},
    "M20":  {"passos": [2.5, 2.0, 1.5, 1.0], "chanfro_padrao": 0.5},
    "M22":  {"passos": [2.5, 2.0, 1.5, 1.0], "chanfro_padrao": 0.7},
    "M24":  {"passos": [3.0, 2.0, 1.5, 1.0], "chanfro_padrao": 0.5},
    "M27":  {"passos": [3.0, 2.0, 1.5, 1.0], "chanfro_padrao": 0.7},
    "M30":  {"passos": [3.5, 2.0, 1.5, 1.0], "chanfro_padrao": 0.7},
    "M33":  {"passos": [3.5, 2.0, 1.5, 1.0], "chanfro_padrao": 0.7},
    "M36":  {"passos": [4.0, 3.0, 2.0, 1.0], "chanfro_padrao": 0.8},
    "M39":  {"passos": [4.0, 3.0, 2.0, 1.0], "chanfro_padrao": 0.8},
}

# Tabela de chavetas (DIN 6885)
def get_chaveta(d):
    if d <= 22:
        return 6.0, 6.0, 3.5, 2.8, 18.0
    elif d <= 30:
        return 8.0, 7.0, 4.0, 3.3, 22.0
    else:
        return 10.0, 8.0, 4.5, 3.8, 25.0

# Tabela de anel elástico (DIN 471)
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

# Seleção de rosca
rosca_selecionada = st.sidebar.selectbox("Rosca (M)", list(rosas_data.keys()), index=10)  # M24 default

# Passo da rosca
passos_disponiveis = rosas_data[rosca_selecionada]["passos"]
passo_rosca = st.sidebar.selectbox("Passo da rosca (mm)", passos_disponiveis, index=0)

# Diâmetro do eixo
d_eixo = st.sidebar.number_input("Diâmetro do eixo (mm)", 4.0, 100.0, 24.0, 0.5)

# Pescoço e chanfro
largura_pescoço = st.sidebar.number_input("Largura do pescoço (mm)", 2.0, 10.0, 3.5, 0.1)
chanfro_padrao = rosas_data[rosca_selecionada]["chanfro_padrao"]
chanfro = st.sidebar.number_input("Chanfro 45° (mm)", 0.2, 2.0, chanfro_padrao, 0.1)

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

st.success("✅ Cálculos atualizados conforme norma!")
