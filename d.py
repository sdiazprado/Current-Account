import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Current Account", layout="wide", page_icon="🌍")

# 2. Data Loading & Mapping
@st.cache_data
def load_data():
    df = pd.read_excel('global_imbalances_panel_filled.xlsx', sheet_name=0)
    df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
    
    # Diccionario maestro de los 32 países
    g32_map = {
        'ARG': 'Argentina', 'AUS': 'Australia', 'BRA': 'Brazil', 'CAN': 'Canada', 
        'CHE': 'Switzerland', 'CHN': 'China', 'DEU': 'Germany', 'DNK': 'Denmark', 
        'EGY': 'Egypt', 'ESP': 'Spain', 'EUU': 'European Union', 'FIN': 'Finland', 
        'FRA': 'France', 'GBR': 'United Kingdom', 'IDN': 'Indonesia', 'IND': 'India', 
        'IRL': 'Ireland', 'ITA': 'Italy', 'JPN': 'Japan', 'KOR': 'South Korea', 
        'MAR': 'Morocco', 'MEX': 'Mexico', 'NLD': 'Netherlands', 'NOR': 'Norway', 
        'PHL': 'Philippines', 'RUS': 'Russia', 'SAU': 'Saudi Arabia', 'SGP': 'Singapore', 
        'SWE': 'Sweden', 'TUR': 'Turkey', 'USA': 'United States', 'ZAF': 'South Africa'
    }
    
    df = df[df['iso3'].isin(g32_map.keys())].copy()
    df['country_name'] = df['iso3'].map(g32_map)
    
    # Cargar el codebook para los nombres elegantes de las variables
    df_codebook = pd.read_excel('global_imbalances_panel_filled.xlsx', sheet_name=1)
    if 'variable' in df_codebook.columns and 'description' in df_codebook.columns:
        mapping_dict = dict(zip(df_codebook['variable'], df_codebook['description']))
    else:
        mapping_dict = {}
        
    return df, mapping_dict

df, clean_names = load_data()

def format_var(raw_col):
    """Devuelve el nombre limpio del diccionario o capitaliza la variable cruda."""
    clean_name = clean_names.get(raw_col)
    if pd.isna(clean_name): 
        return str(raw_col).replace('_', ' ').title()
    return str(clean_name)

# Identify variables and parameters for the UI
non_graphable = ['iso3', 'country', 'country_name', 'year']
graphable_vars = sorted([col for col in df.columns if col not in non_graphable])
unique_countries = sorted(df['country_name'].dropna().unique())
# Lista de años disponibles ordenada del más reciente al más antiguo
available_years = sorted(df['year'].dropna().unique(), reverse=True)

# 3. App Header
st.title("Current Account Visualization")
st.markdown("Exploratory data tool")
st.divider()

# 4. TABS STRUCTURE
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 1. Time Series", 
    "📊 2. Cross-Sectional", 
    "🔍 3. Scatter", 
    "🧮 4. Correlation Matrix"
])

# --- TAB 1: TIME SERIES ---
with tab1:
    st.subheader("Temporal Evolution")
    
    # 1. Row of controls (Countries, Variable, and Time Range)
    col_c, col_v = st.columns([2, 2]) # Selectors for what to see
    with col_c:
        t1_countries = st.multiselect("Select Countries:", options=unique_countries, default=['United States', 'China', 'Germany', 'Mexico'], key="t1_c")
    with col_v:
        t1_var = st.selectbox("Select Variable:", options=graphable_vars, format_func=format_var, key="t1_v")
    
    # Second row for the years (Compact)
    anios_asc = sorted(available_years)
    col_y1, col_y2, col_spacer = st.columns([1, 1, 2]) # Using a spacer to keep selectors on the left
    with col_y1:
        t1_start = st.selectbox("Start Year:", options=anios_asc, index=0, key="t1_start")
    with col_y2:
        t1_end = st.selectbox("End Year:", options=anios_asc, index=len(anios_asc)-1, key="t1_end")
    
    st.divider() # Subtle visual separation before the chart

    # 2. Rendering Logic
    if t1_start > t1_end:
        st.error("⚠️ The Start Year cannot be greater than the End Year.")
    elif t1_countries:
        # Filter data
        df_t1 = df[df['country_name'].isin(t1_countries)].dropna(subset=[t1_var, 'year'])
        df_t1 = df_t1[(df_t1['year'] >= t1_start) & (df_t1['year'] <= t1_end)]
        
        if not df_t1.empty:
            fig1 = px.line(df_t1, x='year', y=t1_var, color='country_name', markers=True, template="simple_white")
            fig1.update_layout(
                xaxis_title="Year", 
                yaxis_title=format_var(t1_var), 
                legend_title="Country", 
                hovermode="closest"
            )
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.warning("No data available for the selected parameters in this time range.")
# --- TAB 2: CROSS-SECTIONAL (TOP/BOTTOM & HISTOGRAM) ---
with tab2:
    st.subheader("Cross-Sectional Distribution")
    col1, col2 = st.columns(2)
    with col1:
        t2_year = st.selectbox("Select Year:", options=available_years, index=0, key="t2_y")
    with col2:
        t2_var = st.selectbox("Select Variable:", options=graphable_vars, format_func=format_var, key="t2_v")
        
    df_t2 = df[df['year'] == t2_year].dropna(subset=[t2_var])
    
    if not df_t2.empty:
        c1, c2 = st.columns(2)
        
        with c1:
            df_sorted = df_t2.sort_values(by=t2_var, ascending=False)
            top5 = df_sorted.head(5)
            bottom5 = df_sorted.tail(5)
            df_extremes = pd.concat([top5, bottom5]).drop_duplicates()
            
            df_extremes['color'] = df_extremes[t2_var].apply(lambda x: 'Positive' if x >= 0 else 'Negative')
            
            fig2a = px.bar(df_extremes, x=t2_var, y='country_name', orientation='h', 
                           color='color', color_discrete_map={'Positive': '#2ca02c', 'Negative': '#d62728'},
                           title=f"Top 5 & Bottom 5 ({t2_year})", template="simple_white")
            fig2a.update_layout(yaxis={'categoryorder':'total ascending'}, yaxis_title="", xaxis_title=format_var(t2_var), showlegend=False)
            st.plotly_chart(fig2a, use_container_width=True)
            
        with c2:
            fig2b = px.histogram(df_t2, x=t2_var, nbins=15, title=f"Global Distribution ({t2_year})", template="simple_white", opacity=0.7)
            fig2b.update_layout(xaxis_title=format_var(t2_var), yaxis_title="Count of Countries")
            st.plotly_chart(fig2b, use_container_width=True)
    else:
        st.warning(f"No data available for {format_var(t2_var)} in the year {t2_year}.")

# --- TAB 3: BIVARIATE SCATTER PLOT ---
with tab3:
    st.subheader("Relationship & Tendency (OLS)")
    col1, col2, col3 = st.columns(3)
    with col1:
        t3_x = st.selectbox("X-Axis (Independent Var):", options=graphable_vars, index=1 if len(graphable_vars)>1 else 0, format_func=format_var, key="t3_x")
    with col2:
        t3_y = st.selectbox("Y-Axis (Dependent Var):", options=graphable_vars, index=0, format_func=format_var, key="t3_y")
    with col3:
        t3_year = st.selectbox("Select Year for Scatter:", options=available_years, index=0, key="t3_yr")
        
    df_t3 = df[df['year'] == t3_year].dropna(subset=[t3_x, t3_y])
    
    if not df_t3.empty:
        fig3 = px.scatter(df_t3, x=t3_x, y=t3_y, hover_name='country_name', text='iso3',
                          trendline="ols", trendline_color_override="red",
                          title=f"Relationship between {format_var(t3_x)} and {format_var(t3_y)} ({t3_year})",
                          template="simple_white")
        
        fig3.update_traces(textposition='top center', marker=dict(size=10, opacity=0.6, color='#1f77b4'))
        fig3.update_layout(xaxis_title=format_var(t3_x), yaxis_title=format_var(t3_y))
        
        st.plotly_chart(fig3, use_container_width=True)
        
        results = px.get_trendline_results(fig3)
        if not results.empty:
            r_squared = results.iloc[0]["px_fit_results"].rsquared
            st.caption(f"**R-squared (OLS):** {r_squared:.4f}. *(This indicates how much variance in Y is explained by X in this specific year).*")
    else:
        st.warning("Insufficient data to plot the relationship for this year.")

# --- TAB 4: CORRELATION MATRIX ---
with tab4:
    st.subheader("Multicollinearity Check")
    st.markdown("Select variables to view their Pearson correlation coefficients across the entire panel.")
    
    default_vars = graphable_vars[:5] if len(graphable_vars) >= 5 else graphable_vars
    t4_vars = st.multiselect("Select Variables for Correlation:", options=graphable_vars, default=default_vars, format_func=format_var, key="t4_v")
    
    if len(t4_vars) > 1:
        corr_matrix = df[t4_vars].corr()
        elegant_names = [format_var(v) for v in t4_vars]
        corr_matrix.index = elegant_names
        corr_matrix.columns = elegant_names
        
        fig4 = px.imshow(corr_matrix, text_auto=".2f", aspect="auto", 
                         color_continuous_scale='RdBu_r', zmin=-1, zmax=1,
                         title="Pearson Correlation Heatmap")
        fig4.update_layout(xaxis_title="", yaxis_title="")
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("Please select at least two variables to generate the correlation matrix.")

# --- AUTHOR LINK ---
st.sidebar.markdown(
    f"""
    <div style="text-align: center;">
        <a href="https://github.com/sdiazprado" target="_blank" style="text-decoration: none; color: gray; font-size: 14px;">
            📁 Created by: sdiazprado
        </a>
    </div>
    """, 
    unsafe_allow_html=True
)

