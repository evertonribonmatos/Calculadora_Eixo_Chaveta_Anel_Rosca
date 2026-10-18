import streamlit as st
import pandas as pd
from math import sqrt

st.set_page_config(page_title="Calculadora Técnica de Eixo", layout="wide")
st.title("🔧 Calculadora Técnica de Eixo")
st.markdown("### Todas as roscas • DIN • ISO • ASME • ABNT")

# ==================== DADOS DAS NORMAS ====================
# Rosca Métrica ISO (M4 a M39)
rosas_metricas = {
    "M4":   {"d": 4.0, "passos": [0.7, 0.5], "chanfro_ideal": 0.3, "pescoço_ideal": 2.5, "chanfro_min": 0.2, "pescoço_min": 2.0, "chanfro_max": 0.5, "pescoço_max": 4.0},
    "M5":   {"d": 5.0, "passos": [0.8, 0.5], "chanfro_ideal": 0.4, "pescoço_ideal": 2.5, "chanfro_min": 0.3, "pescoço_min": 2.0, "chanfro_max": 0.6, "pescoço_max": 4.0},
    "M6":   {"d": 6.0, "passos": [1.0, 0.75, 0.5], "chanfro_ideal": 0.5, "pescoço_ideal": 2.5, "chanfro_min": 0.4, "pescoço_min": 2.0, "chanfro_max": 0.8, "pescoço_max": 4.0},
    "M8":   {"d": 8.0, "passos": [1.25, 1.0, 0.75, 0.5], "chanfro_ideal": 0.5, "pescoço_ideal": 2.5, "chanfro_min": 0.4, "pescoço_min": 2.0, "chanfro_max": 0.8, "pescoço_max": 4.0},
    "M10":  {"d": 10.0, "passos": [1.5, 1.25, 1.0, 0.75, 0.5], "chanfro_ideal": 0.5, "pescoço_ideal": 3.0, "chanfro_min": 0.4, "pescoço_min": 2.0, "chanfro_max": 0.8, "pescoço_max": 5.0},
    "M12":  {"d": 12.0, "passos": [1.75, 1.5, 1.25, 0.75, 0.5], "chanfro_ideal": 0.5, "pescoço_ideal": 3.0, "chanfro_min": 0.4, "pescoço_min": 2.0, "chanfro_max": 0.8, "pescoço_max": 5.0},
    "M14":  {"d": 14.0, "passos": [2.0, 1.5, 1.0, 0.75], "chanfro_ideal": 0.6, "pescoço_ideal": 3.0, "chanfro_min": 0.5, "pescoço_min": 2.5, "chanfro_max": 0.9, "pescoço_max": 5.0},
    "M16":  {"d": 16.0, "passos": [2.0, 1.5, 1.0, 0.75], "chanfro_ideal": 0.6, "pescoço_ideal": 3.0, "chanfro_min": 0.5, "pescoço_min": 2.5, "chanfro_max": 0.9, "pescoço_max": 5.0},
    "M18":  {"d": 18.0, "passos": [2.5, 2.0, 1.5, 1.0], "chanfro_ideal": 0.6, "pescoço_ideal": 3.0, "chanfro_min": 0.5, "pescoço_min": 2.5, "chanfro_max": 0.9, "pescoço_max": 5.0},
    "M20":  {"d": 20.0, "passos": [2.5, 2.0, 1.5, 1.0], "chanfro_ideal": 0.5, "pescoço_ideal": 3.5, "chanfro_min": 0.4, "pescoço_min": 2.5, "chanfro_max": 0.8, "pescoço_max": 6.0},
    "M22":  {"d": 22.0, "passos": [2.5, 2.0, 1.5, 1.0], "chanfro_ideal": 0.7, "pescoço_ideal": 3.5, "chanfro_min": 0.5, "pescoço_min": 2.5, "chanfro_max": 0.9, "pescoço_max": 6.0},
    "M24":  {"d": 24.0, "passos": [3.0, 2.0, 1.5, 1.0], "chanfro_ideal": 0.5, "pescoço_ideal": 3.5, "chanfro_min": 0.4, "pescoço_min": 2.5, "chanfro_max": 0.8, "pescoço_max": 6.0},
    "M27":  {"d": 27.0, "passos": [3.0, 2.0, 1.5, 1.0], "chanfro_ideal": 0.7, "pescoço_ideal": 3.5, "chanfro_min": 0.5, "pescoço_min": 2.5, "chanfro_max": 0.9, "pescoço_max": 6.0},
    "M30":  {"d": 30.0, "passos": [3.5, 2.0, 1.5, 1.0], "chanfro_ideal": 0.7, "pescoço_ideal": 3.5, "chanfro_min": 0.5, "pescoço_min": 2.5, "chanfro_max": 0.9, "pescoço_max": 7.0},
    "M33":  {"d": 33.0, "passos": [3.5, 2.0, 1.5, 1.0], "chanfro_ideal": 0.7, "pescoço_ideal": 3.5, "chanfro_min": 0.5, "pescoço_min": 2.5, "chanfro_max": 0.9, "pescoço_max": 7.0},
    "M36":  {"d": 36.0, "passos": [4.0, 3.0, 2.0, 1.0], "chanfro_ideal": 0.8, "pescoço_ideal": 4.0, "chanfro_min": 0.6, "pescoço_min": 3.0, "chanfro_max": 1.0, "pescoço_max": 7.0},
    "M39":  {"d": 39.0, "passos": [4.0, 3.0, 2.0, 1.0], "chanfro_ideal": 0.8, "pescoço_ideal": 4.0, "chanfro_min": 0.6, "pescoço_min": 3.0, "chanfro_max": 1.0, "pescoço_max": 7.0},
}

# Rosca Whitworth (polegada)
rosas_whitworth = {
    "1/4\"": {"d": 6.35, "passos": [19, 26], "chanfro_ideal": 0.4, "pescoço_ideal": 2.5},
    "5/16\"": {"d": 7.94, "passos": [18, 26], "chanfro_ideal": 0.5, "pescoço_ideal": 2.5},
    "3/8\"": {"d": 9.53, "passos": [16, 26], "chanfro_ideal": 0.5, "pescoço_ideal": 3.0},
    "1/2\"": {"d": 12.70, "passos": [12, 26], "chanfro_ideal": 0.6, "pescoço_ideal": 3.5},
    "5/8\"": {"d": 15.88, "passos": [11, 26], "chanfro_ideal": 0.6, "pescoço_ideal": 3.5},
    "3/4\"": {"d": 19.05, "passos": [10, 26], "chanfro_ideal": 0.7, "pescoço_ideal": 4.0},
    "1\"":   {"d": 25.40, "passos": [8, 26], "chanfro_ideal": 0.8, "pescoço_ideal": 4.0},
}

# Rosca UNC / UNF (polegada)
rosas_unc_unf = {
    "1/4\"-20 UNC": {"d": 6.35, "passos": [20], "chanfro_ideal": 0.4, "pescoço_ideal": 2.5},
    "1/4\"-28 UNF": {"d": 6.35, "passos": [28], "chanfro_ideal": 0.4, "pescoço_ideal": 2.5},
    "5/16\"-18 UNC": {"d": 7.94, "passos": [18], "chanfro_ideal": 0.5, "pescoço_ideal": 2.5},
    "5/16\"-24 UNF": {"d": 7.94, "passos": [24], "chanfro_ideal": 0.5, "pescoço_ideal": 2.5},
    "3/8\"-16 UNC": {"d": 9.53, "passos": [16], "chanfro_ideal": 0.5, "pescoço_ideal": 3.0},
    "3/8\"-24 UNF": {"d": 9.53, "passos": [24], "chanfro_ideal": 0.5, "pescoço_ideal": 3.0},
    "1/2\"-13 UNC": {"d": 12.70, "passos": [13], "chanfro_ideal": 0.6, "pescoço_ideal": 3.5},
    "1/2\"-20 UNF": {"d": 12.70, "passos": [20], "chanfro_ideal": 0.6, "pescoço_ideal": 3.5},
}

# Rosca Trapezoidal (Tr)
rosas_trapezoidal = {
    "Tr 8x1.5": {"d": 8.0, "passos": [1.5], "chanfro_ideal": 0.5, "pescoço_ideal": 3.0},
    "Tr 10x2":  {"d": 10.0, "passos": [2.0], "chanfro_ideal": 0.5, "pescoço_ideal": 3.0},
    "Tr 12x2":  {"d": 12.0, "passos": [2.0], "chanfro_ideal": 0.6, "pescoço_ideal": 3.0},
    "Tr 16x2":  {"d": 16.0, "passos": [2.0], "chanfro_ideal": 0.6, "pescoço_ideal": 3.0},
    "Tr 20x3":  {"d": 20.0, "passos": [3.0], "chanfro_ideal": 0.7, "pescoço_ideal": 4.0},
    "Tr 24x3":  {"d": 24.0, "passos": [3.0], "chanfro_ideal": 0.7, "pescoço_ideal": 4.0},
    "Tr 30x4":  {"d": 30.0, "passos": [4.0], "chanfro_ideal": 0.8, "pescoço_ideal": 5.0},
}

# Rosca Redonda (Rd)
rosas_redonda = {
    "Rd 8x1/6": {"d": 8.0, "passos": [1.5], "chanfro_ideal": 0.5, "pescoço_ideal": 3.0},
    "Rd 10x1/6": {"d": 10.0, "passos": [1.5], "chanfro_ideal": 0.5, "pescoço_ideal": 3.0},
    "Rd 12x1/6": {"d": 12.0, "passos": [1.5], "chanfro_ideal": 0.6, "pescoço_ideal": 3.0},
    "Rd 16x1/6": {"d": 16.0, "passos": [1.5], "chanfro_ideal": 0.6, "pescoço_ideal": 3.0},
    "Rd 20x1/6": {"d": 20.0, "passos": [1.5], "chanfro_ideal": 0.7, "pescoço_ideal": 4.0},
    "Rd 24x1/6": {"d": 24.0, "passos": [1.5], "chanfro_ideal": 0.7, "pescoço_ideal": 4.0},
}

# Rosca ACME
rosas_acme = {
    "1/2\"-10 ACME": {"d": 12.7, "passos": [10], "chanfro_ideal": 0.6, "pescoço_ideal": 3.5},
    "5/8\"-8 ACME": {"d": 15.88, "passos": [8], "chanfro_ideal": 0.6, "pescoço_ideal": 3.5},
    "3/4\"-6 ACME": {"d": 19.05, "passos": [6], "chanfro_ideal": 0.7, "pescoço_ideal": 4.0},
    "1\"-5 ACME": {"d": 25.4, "passos": [5], "chanfro_ideal": 0.8, "pescoço_ideal": 5.0},
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
st.sidebar.header("Tipo de Rosca")

tipo_rosca = st.sidebar.selectbox(
    "Selecione o tipo de rosca",
    ["Métrica ISO (M)", "Whitworth (polegada)", "UNC / UNF (polegada)", "Trapezoidal (Tr)", "Redonda (Rd)", "ACME"],
    index=0
)

# ==================== SELEÇÃO DE ROSCA CONFORME TIPO ====================
if tipo_rosca == "Métrica ISO (M)":
    rosca_selecionada = st.sidebar.selectbox("Rosca (M)", list(rosas_metricas.keys()), index=10)
    dados = rosas_metricas[rosca_selecionada]
    d_eixo = dados["d"]
    passos = dados["passos"]
    chanfro_ideal = dados["chanfro_ideal"]
    pescoço_ideal = dados["pescoço_ideal"]
    chanfro_min = dados["chanfro_min"]
    pescoço_min = dados["pescoço_min"]
    chanfro_max = dados["chanfro_max"]
    pescoço_max = dados["pescoço_max"]

elif tipo_rosca == "Whitworth (polegada)":
    rosca_selecionada = st.sidebar.selectbox("Rosca Whitworth", list(rosas_whitworth.keys()), index=3)
    dados = rosas_whitworth[rosca_selecionada]
    d_eixo = dados["d"]
    passos = dados["passos"]
    chanfro_ideal = dados["chanfro_ideal"]
    pescoço_ideal = dados["pescoço_ideal"]
    chanfro_min = chanfro_ideal - 0.1
    pescoço_min = pescoço_ideal - 0.5
    chanfro_max = chanfro_ideal + 0.2
    pescoço_max = pescoço_ideal + 1.0

elif tipo_rosca == "UNC / UNF (polegada)":
    rosca_selecionada = st.sidebar.selectbox("Rosca UNC / UNF", list(rosas_unc_unf.keys()), index=2)
    dados = rosas_unc_unf[rosca_selecionada]
    d_eixo = dados["d"]
    passos = dados["passos"]
    chanfro_ideal = dados["chanfro_ideal"]
    pescoço_ideal = dados["pescoço_ideal"]
    chanfro_min = chanfro_ideal - 0.1
    pescoço_min = pescoço_ideal - 0.5
    chanfro_max = chanfro_ideal + 0.2
    pescoço_max = pescoço_ideal + 1.0

elif tipo_rosca == "Trapezoidal (Tr)":
    rosca_selecionada = st.sidebar.selectbox("Rosca Trapezoidal", list(rosas_trapezoidal.keys()), index=4)
    dados = rosas_trapezoidal[rosca_selecionada]
    d_eixo = dados["d"]
    passos = dados["passos"]
    chanfro_ideal = dados["chanfro_ideal"]
    pescoço_ideal = dados["pescoço_ideal"]
    chanfro_min = chanfro_ideal - 0.1
    pescoço_min = pescoço_ideal - 0.5
    chanfro_max = chanfro_ideal + 0.2
    pescoço_max = pescoço_ideal + 1.0

elif tipo_rosca == "Redonda (Rd)":
    rosca_selecionada = st.sidebar.selectbox("Rosca Redonda", list(rosas_redonda.keys()), index=4)
    dados = rosas_redonda[rosca_selecionada]
    d_eixo = dados["d"]
    passos = dados["passos"]
    chanfro_ideal = dados["chanfro_ideal"]
    pescoço_ideal = dados["pescoço_ideal"]
    chanfro_min = chanfro_ideal - 0.1
    pescoço_min = pescoço_ideal - 0.5
    chanfro_max = chanfro_ideal + 0.2
    pescoço_max = pescoço_ideal + 1.0

elif tipo_rosca == "ACME":
    rosca_selecionada = st.sidebar.selectbox("Rosca ACME", list(rosas_acme.keys()), index=2)
    dados = rosas_acme[rosca_selecionada]
    d_eixo = dados["d"]
    passos = dados["passos"]
    chanfro_ideal = dados["chanfro_ideal"]
    pescoço_ideal = dados["pescoço_ideal"]
    chanfro_min = chanfro_ideal - 0.1
    pescoço_min = pescoço_ideal - 0.5
    chanfro_max = chanfro_ideal + 0.2
    pescoço_max = pescoço_ideal + 1.0

# Passo
passo_rosca = st.sidebar.selectbox("Passo da rosca", passos, index=0)

st.sidebar.write(f"**Diâmetro do eixo:** {d_eixo} mm")

# ==================== PESOÇO E CHANFRO COM CORES ====================
st.sidebar.subheader("Pescoço e Chanfro")

largura_pescoço = st.sidebar.slider(
    "Largura do pescoço (mm)",
    min_value=pescoço_min,
    max_value=pescoço_max,
    value=pescoço_ideal,
    step=0.1
)

chanfro = st.sidebar.slider(
    "Chanfro 45° (mm)",
    min_value=chanfro_min,
    max_value=chanfro_max,
    value=chanfro_ideal,
    step=0.1
)

# Indicadores de cor
if largura_pescoço == pescoço_ideal:
    st.sidebar.success(f"✅ Ideal: {pescoço_ideal} mm")
elif pescoço_min <= largura_pescoço <= pescoço_max:
    st.sidebar.warning(f"⚠️ Dentro da tolerância")
else:
    st.sidebar.error("❌ Fora da tolerância")

if chanfro == chanfro_ideal:
    st.sidebar.success(f"✅ Ideal: {chanfro_ideal} mm")
elif chanfro_min <= chanfro <= chanfro_max:
    st.sidebar.warning(f"⚠️ Dentro da tolerância")
else:
    st.sidebar.error("❌ Fora da tolerância")

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

st.header("3. Rosca")
st.write(f"**Tipo:** {tipo_rosca}")
st.write(f"**Rosca:** {rosca_selecionada}")
st.write(f"**Passo:** {passo_rosca}")

if tipo_rosca == "Métrica ISO (M)":
    P = passo_rosca
    H = round((sqrt(3)/2) * P, 3)
    H2 = round(H/2, 3)
    H4 = round(H/4, 3)
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
        "Tipo de rosca",
        "Rosca selecionada",
        "Diâmetro do eixo",
        "Largura chaveta (b)",
        "Profundidade chaveta no eixo (t₁)",
        "Comprimento chaveta recomendado",
        "Espessura anel elástico (s)",
        "Profundidade canal anel",
        "Largura do pescoço",
        "Chanfro 45°"
    ],
    "Valor": [
        tipo_rosca,
        rosca_selecionada,
        f"{d_eixo} mm",
        f"{b} mm",
        f"{t1} mm",
        f"{L_rec} mm",
        f"{s} mm",
        f"{canal_prof} mm",
        f"{largura_pescoço} mm",
        f"{chanfro} mm"
    ]
}

df = pd.DataFrame(dados)
st.dataframe(df, use_container_width=True)

st.success("✅ App atualizado com todas as roscas e normas!")
