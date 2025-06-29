import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page config
st.set_page_config(
    page_title="NBA Draft ROI Dashboard",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .section-header {
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load the NBA data with value metrics"""
    try:
        df = pd.read_csv("NBAStats_with_value_metrics.csv")
        return df
    except FileNotFoundError:
        st.error("❌ Could not find 'NBAStats_with_value_metrics.csv'. Please run value_metrics.py first.")
        st.stop()

def main():
    # Header
    st.markdown('<h1 class="main-header">🏀 NBA Draft ROI Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header("🔧 Filters")
    
    # Year range filter
    if 'DRAFT_YEAR' in df.columns:
        draft_years = df['DRAFT_YEAR'].dropna()
        if len(draft_years) > 0:
            year_range = st.sidebar.slider(
                "Draft Year Range",
                min_value=int(draft_years.min()),
                max_value=int(draft_years.max()),
                value=(int(draft_years.min()), int(draft_years.max()))
            )
            df_filtered = df[(df['DRAFT_YEAR'] >= year_range[0]) & (df['DRAFT_YEAR'] <= year_range[1])]
        else:
            df_filtered = df
    else:
        df_filtered = df
    
    # Draft round filter
    if 'DRAFT_ROUND' in df_filtered.columns:
        available_rounds = sorted(df_filtered['DRAFT_ROUND'].dropna().unique())
        if len(available_rounds) > 0:
            selected_rounds = st.sidebar.multiselect(
                "Draft Rounds",
                options=available_rounds,
                default=available_rounds
            )
            if selected_rounds:
                df_filtered = df_filtered[df_filtered['DRAFT_ROUND'].isin(selected_rounds)]
    
    # Filter for drafted players only
    drafted_players = df_filtered[df_filtered['draft_value_ratio'].notna()]
    
    # Main dashboard content
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Players",
            value=f"{len(df_filtered):,}",
            delta=f"All time data"
        )
    
    with col2:
        st.metric(
            label="Drafted Players",
            value=f"{len(drafted_players):,}",
            delta=f"{len(drafted_players)/len(df_filtered)*100:.1f}% of total"
        )
    
    with col3:
        if len(drafted_players) > 0:
            avg_roi = drafted_players['draft_value_ratio'].mean()
            st.metric(
                label="Average ROI",
                value=f"{avg_roi:.1f}",
                delta="Draft value ratio"
            )
    
    with col4:
        if len(df_filtered) > 0:
            avg_career = df_filtered['career_length'].mean()
            st.metric(
                label="Avg Career Length",
                value=f"{avg_career:.1f} years",
                delta="All players"
            )
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Visualizations", "🏆 Top Performers", "📈 Analysis", "📋 Data Explorer"])
    
    with tab1:
        st.markdown('<h2 class="section-header">Interactive Visualizations</h2>', unsafe_allow_html=True)
        
        # Create three columns for the three main plots
        viz_col1, viz_col2 = st.columns(2)
        
        with viz_col1:
            st.subheader("Draft Position vs Value Score")
            if len(drafted_players) > 0:
                fig1 = px.scatter(
                    drafted_players, 
                    x='DRAFT_NUMBER', 
                    y='value_score',
                    hover_data=['PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'DRAFT_YEAR'],
                    title="Draft Number vs Value Score",
                    labels={'DRAFT_NUMBER': 'Draft Position', 'value_score': 'Value Score'}
                )
                fig1.add_scatter(
                    x=drafted_players['DRAFT_NUMBER'], 
                    y=np.poly1d(np.polyfit(drafted_players['DRAFT_NUMBER'], drafted_players['value_score'], 1))(drafted_players['DRAFT_NUMBER']),
                    mode='lines',
                    name='Trend Line',
                    line=dict(color='red', dash='dash')
                )
                st.plotly_chart(fig1, use_container_width=True)
        
        with viz_col2:
            st.subheader("Average ROI by Draft Round")
            if len(drafted_players) > 0:
                roi_by_round = drafted_players.groupby('DRAFT_ROUND')['draft_value_ratio'].mean().reset_index()
                fig2 = px.line(
                    roi_by_round, 
                    x='DRAFT_ROUND', 
                    y='draft_value_ratio',
                    markers=True,
                    title="Average ROI by Draft Round",
                    labels={'DRAFT_ROUND': 'Draft Round', 'draft_value_ratio': 'Average ROI'}
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        # Top 10 ROI Players Bar Chart (full width)
        st.subheader("Top 10 ROI Players")
        if len(drafted_players) > 0:
            top_10_roi = drafted_players.nlargest(10, 'draft_value_ratio')
            top_10_roi['player_name'] = top_10_roi['PLAYER_FIRST_NAME'] + ' ' + top_10_roi['PLAYER_LAST_NAME']
            
            fig3 = px.bar(
                top_10_roi,
                x='player_name',
                y='draft_value_ratio',
                title="Top 10 Players by Draft ROI",
                labels={'player_name': 'Player', 'draft_value_ratio': 'ROI'},
                hover_data=['DRAFT_YEAR', 'DRAFT_NUMBER', 'value_score']
            )
            fig3.update_xaxis(tickangle=45)
            st.plotly_chart(fig3, use_container_width=True)
    
    with tab2:
        st.markdown('<h2 class="section-header">Top Performers</h2>', unsafe_allow_html=True)
        
        perf_col1, perf_col2 = st.columns(2)
        
        with perf_col1:
            st.subheader("🏆 Top 10 ROI Players")
            if len(drafted_players) > 0:
                top_roi = drafted_players.nlargest(10, 'draft_value_ratio')[
                    ['PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'DRAFT_YEAR', 'DRAFT_NUMBER', 
                     'draft_value_ratio', 'value_score', 'career_length']
                ]
                
                for i, (_, player) in enumerate(top_roi.iterrows(), 1):
                    with st.container():
                        st.markdown(f"""
                        **{i}. {player['PLAYER_FIRST_NAME']} {player['PLAYER_LAST_NAME']}**
                        - ROI: {player['draft_value_ratio']:.1f}
                        - Draft: {player['DRAFT_YEAR']:.0f} (#{int(player['DRAFT_NUMBER'])})
                        - Career: {player['career_length']} years
                        - Value Score: {player['value_score']:.1f}
                        """)
                        st.divider()
        
        with perf_col2:
            st.subheader("⭐ Top 10 Value Score Players")
            if len(df_filtered) > 0:
                top_value = df_filtered.nlargest(10, 'value_score')[
                    ['PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'DRAFT_YEAR', 'DRAFT_NUMBER', 
                     'value_score', 'PTS', 'REB', 'AST', 'career_length']
                ]
                
                for i, (_, player) in enumerate(top_value.iterrows(), 1):
                    draft_info = f"#{int(player['DRAFT_NUMBER'])}" if pd.notna(player['DRAFT_NUMBER']) else "Undrafted"
                    with st.container():
                        st.markdown(f"""
                        **{i}. {player['PLAYER_FIRST_NAME']} {player['PLAYER_LAST_NAME']}**
                        - Value Score: {player['value_score']:.1f}
                        - Draft: {player['DRAFT_YEAR']:.0f} ({draft_info})
                        - Stats: {player['PTS']:.1f} PTS, {player['REB']:.1f} REB, {player['AST']:.1f} AST
                        - Career: {player['career_length']} years
                        """)
                        st.divider()
    
    with tab3:
        st.markdown('<h2 class="section-header">Detailed Analysis</h2>', unsafe_allow_html=True)
        
        analysis_col1, analysis_col2 = st.columns(2)
        
        with analysis_col1:
            st.subheader("📊 ROI by Draft Round")
            if len(drafted_players) > 0:
                round_analysis = drafted_players.groupby('DRAFT_ROUND')['draft_value_ratio'].agg([
                    'count', 'mean', 'median', 'std'
                ]).round(2)
                round_analysis.columns = ['Players', 'Avg ROI', 'Median ROI', 'Std Dev']
                round_analysis = round_analysis.sort_values('Avg ROI', ascending=False)
                st.dataframe(round_analysis, use_container_width=True)
        
        with analysis_col2:
            st.subheader("🏀 Best Drafting Teams")
            if len(drafted_players) > 0:
                team_analysis = drafted_players.groupby('TEAM_NAME').agg({
                    'draft_value_ratio': ['count', 'mean', 'sum'],
                    'DRAFT_NUMBER': 'mean'
                }).round(2)
                team_analysis.columns = ['Players', 'Avg ROI', 'Total ROI', 'Avg Draft Pos']
                team_analysis = team_analysis[team_analysis['Players'] >= 5]  # At least 5 players
                team_analysis = team_analysis.sort_values('Avg ROI', ascending=False)
                st.dataframe(team_analysis.head(15), use_container_width=True)
        
        # Value Score Distribution
        st.subheader("📈 Value Score Distribution")
        if len(df_filtered) > 0:
            fig_hist = px.histogram(
                df_filtered, 
                x='value_score', 
                bins=50,
                title="Distribution of Value Scores",
                labels={'value_score': 'Value Score', 'count': 'Frequency'}
            )
            st.plotly_chart(fig_hist, use_container_width=True)
    
    with tab4:
        st.markdown('<h2 class="section-header">Data Explorer</h2>', unsafe_allow_html=True)
        
        # Search functionality
        search_col1, search_col2 = st.columns([2, 1])
        
        with search_col1:
            search_player = st.text_input("🔍 Search for a player:", placeholder="Enter player name...")
        
        with search_col2:
            show_all = st.checkbox("Show all players", value=False)
        
        # Filter data based on search
        if search_player:
            mask = (df_filtered['PLAYER_FIRST_NAME'].str.contains(search_player, case=False, na=False) | 
                   df_filtered['PLAYER_LAST_NAME'].str.contains(search_player, case=False, na=False))
            display_df = df_filtered[mask]
            st.success(f"Found {len(display_df)} player(s) matching '{search_player}'")
        elif show_all:
            display_df = df_filtered
        else:
            display_df = df_filtered.head(100)  # Show first 100 by default
            st.info("Showing first 100 players. Use search or 'Show all players' to see more.")
        
        # Select columns to display
        available_columns = ['PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'DRAFT_YEAR', 'DRAFT_ROUND', 
                           'DRAFT_NUMBER', 'TEAM_NAME', 'PTS', 'REB', 'AST', 'career_length', 
                           'value_score', 'draft_value_ratio']
        
        # Filter to only show columns that exist in the dataframe
        available_columns = [col for col in available_columns if col in df_filtered.columns]
        
        selected_columns = st.multiselect(
            "Select columns to display:",
            options=available_columns,
            default=available_columns[:8]  # Show first 8 columns by default
        )
        
        if selected_columns:
            st.dataframe(
                display_df[selected_columns],
                use_container_width=True,
                hide_index=True
            )
        
        # Download button
        if len(display_df) > 0:
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Download filtered data as CSV",
                data=csv,
                file_name="nba_draft_roi_filtered.csv",
                mime="text/csv"
            )
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; margin-top: 2rem;'>
        <p>🏀 NBA Draft ROI Analysis Dashboard | Built with Streamlit</p>
        <p>Data includes player statistics, draft information, and calculated value metrics</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
