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

# Dynamické zobrazení uložených obrázků (cesta zachována podle vašeho projektu)
if latka.startswith("Ibuprofen"):
    try:
        st.image("Leky/ibuprofen.png", caption="Ibuprofenové přípravky", width=200)
    except:
        st.info("ℹ️ Zde se zobrazí obrázek ibuprofen.png")
else:
    try:
        st.image("Leky/paracetamol.png", caption="Paracetamolové přípravky", width=200)
    except:
        st.info("ℹ️ Zde se zobrazí obrázek paracetamol.png")

st.markdown("---")

# 3. KROK: Výběr formy léku a nastavení výchozích hodnot
st.header("3. Forma léku a síla")
forma = st.radio("V jaké formě je lék?", ["Sirup (tekutý)", "Čípek nebo Tableta (pevný)"])

# Nastavení parametrů a defaultních hodnot sirupů podle zvolené látky
if latka.startswith("Ibuprofen"):
    davka_mg_na_kg = 10
    odstup = "6 až 8 hodin (max 3-4x denně)"
    # Výchozí hodnoty pro Nurofen (20mg v 1ml -> 100mg / 5ml)
    default_mg = 20
    default_ml = 1
else:
    davka_mg_na_kg = 15
    odstup = "6 hodin (v případě potřeby po 4h, max 4x denně)"
    # Výchozí hodnoty pro Paracetamol sirup (24mg v 1ml -> 120mg / 5ml)
    default_mg = 24
    default_ml = 1

potrebne_mg = vaha * davka_mg_na_kg

if forma == "Sirup (tekutý)":
    st.write("Zadejte údaje z krabičky (přednastaveno podle obvyklého sirupu):")
    c1, c2 = st.columns(2)
    with c1:
        mg_v_baleni = st.number_input("Miligramy (mg):", min_value=1, value=default_mg)
    with c2:
        ml_v_baleni = st.number_input("Mililitry (ml):", min_value=1, value=default_ml)
    
    sila_leku = mg_v_baleni / ml_v_baleni
    vysledek_presny = potrebne_mg / sila_leku
    
    # ZAOKROUHLENÍ DOLŮ na nejbližších 0.5 ml
    vysledek_zaokrouhleny = (vysledek_presny * 2) // 1 / 2
    if vysledek_zaokrouhleny == 0:
        vysledek_zaokrouhleny = 0.5

    st.markdown("---")
    st.header("📋 Doporučené dávkování")
    st.success(f"### 👉 Podat na stříkačce: **{vysledek_zaokrouhleny:.1f} ml**")
    st.caption(f"💡 Přesný matematický výpočet: {vysledek_presny:.2f} ml. Zaokrouhleno dolů na nejbližší rysku (0,5 ml).")

else:
    st.write("Zadejte sílu jednoho čípku nebo jedné tablety (např. 125 mg):")
    sila_leku = st.number_input("Miligramy v 1 kuse (mg/ks):", min_value=1, value=125)
    
    vysledek_presny_ks = potrebne_mg / sila_leku
    
    # ZAOKROUHLENÍ DOLŮ na nejbližších 0.5 kusu (půlky)
    vysledek_zaokrouhleny_ks = (vysledek_presny_ks * 2) // 1 / 2
    if vysledek_zaokrouhleny_ks == 0:
        vysledek_zaokrouhleny_ks = 0.5

    st.markdown("---")
    st.header("📋 Doporučené dávkování")
    
    if vysledek_zaokrouhleny_ks == 0.5:
        text_ks = "půlku (0.5) čípku/tablety"
    elif vysledek_zaokrouhleny_ks == 1.0:
        text_ks = "1 celý čípek/tabletu"
    elif vysledek_zaokrouhleny_ks == 1.5:
        text_ks = "1 a půl (1.5) čípku/tablety"
    else:
        text_ks = f"{vysledek_zaokrouhleny_ks:.1f} kusu"

    st.success(f"### 👉 Podat v jedné dávce: **{text_ks}**")
    st.caption(f"💡 Přesný matematický výpočet: {vysledek_presny_ks:.2f} ks. Zaokrouhleno dolů na poloviny.")

st.info(f"Dítě o váze {vaha} kg potřebuje v jedné dávce **{potrebne_mg:.0f} mg** účinné látky.")

# Rady pro čípky a tablety
if forma != "Sirup (tekutý)":
    st.write("💡 **Tip pro pevné formy:**")
    if latka.startswith("Paracetamol"):
        st.warning("⚠️ **Pozor u čípků:** Čípky by se správně neměly půlit (účinná látka v nich nemusí být rovnoměrně rozptýlená). Pokud vypočítaná dávka nesedí na celý čípek, konzultujte s lékařem sirup nebo jinou sílu čípku.")
    else:
        st.write("- Tablety lze obvykle bezpečně dělit (půlit/čtvrtit).")

st.write(f"⏱️ **Odstup mezi dávkami:** {odstup}")