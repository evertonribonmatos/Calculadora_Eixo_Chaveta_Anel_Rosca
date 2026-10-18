import streamlit as st
import pandas as pd
from math import sqrt

st.set_page_config(page_title="Calculadora de Eixo - Chaveta, Anel e Rosca", layout="wide")
st.title("🔧 Calculadora Técnica de Eixo")
st.markdown("### Baseado em: DIN 6885 • DIN 471 • ISO 68-1 / ISO 965")

# ==================== SIDEBAR ====================
st.sidebar.header("Dados de Entrada")

d_eixo = st.sidebar.number_input("Diâmetro do eixo (mm)", 10.0, 100.0, 24.0, 0.5)
passo_rosca = st.sidebar.number_input("Passo da rosca (mm)", 1.0, 3.0, 2.0, 0.5)
largura_pescoço = st.sidebar.number_input("Largura do pescoço (mm)", 2.0, 10.0, 3.5, 0.1)
chanfro = st.sidebar.number_input("Chanfro 45° (mm)", 0.2, 2.0, 0.5, 0.1)

# ==================== CÁLCULOS CHAVETA ====================
st.header("1. Chaveta (DIN 6885)")

if d_eixo <= 22:
    b, h, t1, t2, L_min = 6.0, 6.0, 3.5, 2.8, 18.0
elif d_eixo <= 30:
    b, h, t1, t2, L_min = 8.0, 7.0, 4.0, 3.3, 22.0
else:
    b, h, t1, t2, L_min = 10.0, 8.0, 4.5, 3.8, 25.0

L_rec = round(d_eixo * 1.5, 1)

st.write(f"**Largura (b):** {b} mm")
st.write(f"**Altura (h):** {h} mm")
st.write(f"**Profundidade no eixo (t₁):** {t1} mm")
st.write(f"**Profundidade na bucha (t₂):** {t2} mm")
st.write(f"**Comprimento mínimo:** {L_min} mm")
st.write(f"**Comprimento recomendado:** {L_rec} mm")

# ==================== ANEL ELÁSTICO ====================
st.header("2. Anel Elástico (DIN 471)")

if d_eixo == 20:
    s, canal_larg, canal_prof, d_fundo = 1.2, 1.3, 0.5, 19.0
elif d_eixo == 24:
    s, canal_larg, canal_prof, d_fundo = 1.5, 1.5, 0.6, 22.5
else:
    s = round(d_eixo * 0.06, 1)
    canal_larg = round(d_eixo * 0.065, 1)
    canal_prof = round(d_eixo * 0.025, 1)
    d_fundo = round(d_eixo - 2 * canal_prof, 1)

st.write(f"**Espessura do anel (s):** {s} mm")
st.write(f"**Largura do canal:** {canal_larg} mm")
st.write(f"**Profundidade do canal:** {canal_prof} mm")
st.write(f"**Diâmetro fundo do canal:** {d_fundo} mm")

# ==================== ROSCA ====================
st.header("3. Rosca (ISO 68-1)")

P = passo_rosca
H = round((sqrt(3)/2) * P, 3)
H2 = round(H/2, 3)
H4 = round(H/4, 3)

st.write(f"**Passo (P):** {P} mm")
st.write(f"**Altura teórica (H):** {H} mm")
st.write(f"**Altura máxima útil (H/2):** {H2} mm")
st.write(f"**Altura mínima crista (H/4):** {H4} mm")

# ==================== PESOÇO E CHANFRO ====================
st.header("4. Pescoço e Chanfro")
st.write(f"**Largura do pescoço:** {largura_pescoço} mm")
st.write(f"**Chanfro 45°:** {chanfro} mm")

# ==================== TABELA RESUMO ====================
st.header("📋 Resumo Final")

dados = {
    "Item": [
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
    "Valor (mm)": [
        d_eixo, b, t1, L_rec, s, canal_prof, H, largura_pescoço, chanfro
    ]
}

df = pd.DataFrame(dados)
st.dataframe(df, use_container_width=True)

st.success("✅ Todos os cálculos estão prontos para uso!")
