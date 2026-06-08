import streamlit as st

# Nastavení stránky
st.set_page_config(
    page_title="Kalkulačka dávkování léků", 
    page_icon="💊", 
    layout="centered"
)

# Hlavní nadpis
st.title("💊 Kalkulačka dávkování: Sirupy, Čípky i Tablety")
st.write("Výpočet přesné dávky podle váhy dítěte a síly léku.")

# Bezpečnostní upozornění
st.warning(
    "⚠️ **Upozornění:** Tento nástroj je pouze orientační pomůcka. "
    "Vždy zkontrolujte dávkování v příbalovém letáku nebo se poraďte s lékařem."
)

st.markdown("---")

# 1. KROK: Váha dítěte
st.header("1. Údaje o dítěti")
vaha = st.number_input("Zadejte váhu dítěte v kg:", min_value=2.0, max_value=70.0, value=12.0, step=0.5)

st.markdown("---")

# 2. KROK: Výběr účinné látky a zobrazení obrázku
st.header("2. Výběr účinné látky")
latka = st.selectbox(
    "Jakou účinnou látku lék obsahuje?",
    ["Ibuprofen (např. Nurofen, Ibalgin, Brufen)", "Paracetamol (např. Paralen, Panadol)"]
)

# Dynamické zobrazení uložených obrázků na základě výběru
if latka.startswith("Ibuprofen"):
    try:
        # PŘIDÁNO "Leky/" před název
        st.image("Leky/ibuprofen.png", caption="Ibuprofenové přípravky", width=200)
    except:
        st.info("ℹ️ Zde se zobrazí obrázek ibuprofen.png")
else:
    try:
        # PŘIDÁNO "Leky/" před název
        st.image("Leky/paracetamol.png", caption="Paracetamolové přípravky", width=200)
    except:
        st.info("ℹ️ Zde se zobrazí obrázek paracetamol.png")

st.markdown("---")

# 3. KROK: Výběr formy léku
st.header("3. Forma léku a síla")
forma = st.radio("V jaké formě je lék?", ["Sirup (tekutý)", "Čípek nebo Tableta (pevný)"])

if forma == "Sirup (tekutý)":
    st.write("Zadejte údaje z krabičky (např. 100 mg / 5 ml):")
    c1, c2 = st.columns(2)
    with c1:
        mg_v_baleni = st.number_input("Miligramy (mg):", min_value=1, value=100)
    with c2:
        ml_v_baleni = st.number_input("Mililitry (ml):", min_value=1, value=5)
    
    sila_leku = mg_v_baleni / ml_v_baleni # Kolik mg je v 1 ml
    jednotka_vysledku = "ml"
    typ_podani = "na stříkačce"

else:
    st.write("Zadejte sílu jednoho čípku nebo jedné tablety (např. 125 mg):")
    sila_leku = st.number_input("Miligramy v 1 kuse (mg/ks):", min_value=1, value=125)
    jednotka_vysledku = "ks (kusů)"
    typ_podani = "v jedné dávce"

st.markdown("---")

# --- VÝPOČET ---
# Ibuprofen: 10 mg/kg | Paracetamol: 15 mg/kg (standardní bezpečné dávky)
if latka.startswith("Ibuprofen"):
    davka_mg_na_kg = 10
    odstup = "8 hodin (max 3x denně)"
else:
    davka_mg_na_kg = 15
    odstup = "6 hodin (v případě potřeby po 4h, max 4x denně)"

potrebne_mg = vaha * davka_mg_na_kg
vysledek = potrebne_mg / sila_leku

# Zobrazení výsledku
st.header("📋 Doporučené dávkování")

st.success(f"### 👉 Podat {typ_podani}: **{vysledek:.1f} {jednotka_vysledku}**")

st.info(f"Dítě o váze {vaha} kg potřebuje v jedné dávce **{potrebne_mg:.0f} mg** účinné látky.")

# Rady pro čípky a tablety
if forma != "Sirup (tekutý)":
    st.write("💡 **Tip pro pevné formy:**")
    st.write("- Tablety lze obvykle dělit (půlit/čtvrtit).")
    st.write("- Čípky se pro přesnější dávku doporučuje neřezat (látka v nich nemusí být rovnoměrně), ale v praxi se to u dětí někdy po poradě s lékařem dělá (podélně).")

st.write(f"⏱️ **Odstup mezi dávkami:** {odstup}")

