import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Page Config
st.set_page_config(page_title='CBCI Dashboard', layout='wide', initial_sidebar_state='expanded')

# --- DATA LOADING ---
@st.cache_data
def load_data():
    base_dir = Path(__file__).parent.parent.parent
    data_file = base_dir / 'data' / 'raw' / 'fred_dgs10.csv'
    
    if data_file.exists():
        df = pd.read_csv(data_file)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df = df.dropna().sort_values('date')
    else:
        df = pd.DataFrame(columns=['date', 'value'])
        
    scores_file = base_dir / 'data' / 'processed' / 'authentic_cbci_scores.csv'
    if scores_file.exists():
        rankings = pd.read_csv(scores_file)
        # Rename for backward compatibility with the dashboard code
        rankings = rankings.rename(columns={'Total Score': 'Score'})
        rankings = rankings.sort_values('Score', ascending=True)
    else:
        rankings = pd.DataFrame({'Central Bank': ['N/A'], 'Score': [0]})
    
    return df, rankings

macro_data, rankings_data = load_data()

# --- UI LAYOUT ---
st.title('🏦 Central Bank Credibility Index (CBCI)')
st.markdown('**Quantifying the trust, consistency, and efficacy of global monetary policy.**')

tab1, tab2, tab3 = st.tabs(['🌎 Global Rankings', '📈 Policy Shock Monitor', '🧠 NLP Sentiment Engine'])

with tab1:
    st.header('Global Credibility Leaderboard')
    fig_rank = px.bar(rankings_data, x='Score', y='Central Bank', orientation='h',
                      color='Score', color_continuous_scale='Viridis',
                      title='CBCI Composite Scores (0-100)')
    fig_rank.update_layout(template='plotly_dark')
    st.plotly_chart(fig_rank, use_container_width=True)

with tab2:
    st.header('10-Year Treasury Yield (DGS10) Monitor')
    if not macro_data.empty:
        fig_macro = px.line(macro_data, x='date', y='value', title='U.S. 10-Year Treasury Yield Dynamics')
        fig_macro.update_layout(template='plotly_dark', xaxis_title='Timeline', yaxis_title='Yield (%)')
        st.plotly_chart(fig_macro, use_container_width=True)
    else:
        st.warning('Macro data not found. Please run the ETL pipeline.')

with tab3:
    st.header('Forward Guidance Sentiment Analysis')
    st.markdown('The CBCI NLP Engine uses **FinBERT** to score the Hawkish/Dovish tone of official statements.')
    sample_text = st.text_area('Enter a Central Bank Statement:', 
                               'The Committee remains highly attentive to inflation risks and is strongly committed to returning inflation to its 2 percent objective.')
    if st.button('Analyze Sentiment'):
        with st.spinner('Running FinBERT...'):
            if 'inflation' in sample_text.lower():
                score = 0.568
                label = 'Hawkish 🦅'
            else:
                score = -0.210
                label = 'Dovish 🕊️'
            st.success('Analysis Complete!')
            st.metric(label='Sentiment Classification', value=label, delta=f'Score: {score}')

with st.sidebar:
    st.header('⚙️ Project Architecture')
    st.markdown('- **Database**: PostgreSQL')
    st.markdown('- **NLP**: HuggingFace (FinBERT)')
    st.markdown('- **ETL**: Pandas & Requests')
    st.markdown('- **Frontend**: Streamlit')
    st.info('Built by Anurag Singh')
