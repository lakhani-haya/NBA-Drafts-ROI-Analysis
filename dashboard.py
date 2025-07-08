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
    page_title="NBA Draft ROI Analysis Dashboard",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"  # Start with sidebar collapsed to prevent layout shifts
)

# Custom CSS for light NBA-inspired theme
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles with light NBA-inspired colors */
    .stApp {
        background: linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%);
        font-family: 'Inter', sans-serif;
        overflow-x: hidden;
        min-height: 100vh;
    }
    
    /* Main content area */
    .main .block-container {
        background: #FFFFFF;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem auto;
        max-width: 1200px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid #E9ECEF;
    }
    
    /* Header styling with NBA colors */
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #C8102E 0%, #1D428A 50%, #FDB927 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .sub-header {
        font-size: 2rem;
        color: #1A1D29;
        margin-bottom: 1.5rem;
        font-weight: 600;
        border-bottom: 3px solid transparent;
        border-image: linear-gradient(90deg, #C8102E, #1D428A, #FDB927) 1;
        padding-bottom: 0.5rem;
    }
    
    /* Metrics styling */
    .stMetric {
        background: #F8F9FA;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #E9ECEF;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-color: #C8102E;
    }
    
    /* Section headers with NBA colors */
    .section-header {
        color: #1A1D29;
        border-bottom: 2px solid transparent;
        border-image: linear-gradient(90deg, #C8102E, #1D428A, #FDB927) 1;
        padding-bottom: 0.5rem;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        font-weight: 600;
        font-size: 1.5rem;
    }
    
    /* Player cards */
    .player-card {
        background: #FFFFFF;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        border-left: 4px solid #FDB927;
        margin: 0.8rem 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        color: #495057;
    }
    
    .player-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left-color: #C8102E;
    }
    
    /* Insight boxes */
    .insight-box {
        background: #F8F9FA;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #C8102E;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        color: #495057;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #FFFFFF;
        border-right: 2px solid #E9ECEF;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background: #F8F9FA;
        border-radius: 8px;
        padding: 0.5rem;
        gap: 0.5rem;
        border: 1px solid #E9ECEF;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 6px;
        color: #6C757D;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #C8102E 0%, #1D428A 100%) !important;
        color: white !important;
        box-shadow: 0 2px 4px rgba(200, 16, 46, 0.2);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border: 1px solid #E9ECEF;
    }
    
    /* Button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #C8102E 0%, #1D428A 100%);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(200, 16, 46, 0.3);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 6px;
        border: 1px solid #DEE2E6;
        background: #FFFFFF;
        color: #495057;
        transition: border-color 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #C8102E;
        box-shadow: 0 0 0 2px rgba(200, 16, 46, 0.1);
    }
    
    .stSelectbox > div > div {
        border-radius: 6px;
        border: 1px solid #DEE2E6;
        background: #FFFFFF;
    }
    
    .stMultiSelect > div > div {
        border-radius: 6px;
        border: 1px solid #DEE2E6;
        background: #FFFFFF;
    }
    
    /* Plotly charts */
    .js-plotly-plot {
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border: 1px solid #E9ECEF;
    }
    
    /* Text colors */
    .stMarkdown, .stText {
        color: #495057;
    }
    
    .main p {
        color: #6C757D !important;
    }
    
    /* Success/Info/Warning messages */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
        background: #FFFFFF;
    }
    
    .stSuccess {
        border-left-color: #28A745;
        background: #F8FFF9;
        color: #155724;
    }
    
    .stInfo {
        border-left-color: #17A2B8;
        background: #F0F9FF;
        color: #0C5460;
    }
    
    .stWarning {
        border-left-color: #FFC107;
        background: #FFFEF0;
        color: #856404;
    }
    
    /* ONLY prevent sidebar-induced layout shifts */
    [data-testid="stSidebar"] {
        position: relative !important;
    }
    
    .css-1d391kg ~ .css-1lcbmhc {
        margin-left: 0 !important;
    }
    
    /* Ensure stable main content positioning */
    .main {
        transition: margin-left 0s !important;
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

@st.cache_data
def load_team_efficiency_data():
    """Load the team draft efficiency report"""
    try:
        team_df = pd.read_csv("team_draft_efficiency_report.csv")
        return team_df
    except FileNotFoundError:
        st.warning("⚠️ Team efficiency report not found. Run team_draft_efficiency.py to generate it.")
        return None

def calculate_enhanced_metrics(df):
    """Calculate enhanced per-season ROI metrics for dashboard"""
    df_enhanced = df.copy()
    
    # ROI per season
    df_enhanced['roi_per_season'] = np.where(
        (df_enhanced['career_length'] > 0) & (df_enhanced['DRAFT_NUMBER'].notna()),
        df_enhanced['value_score'] / (df_enhanced['career_length'] * df_enhanced['DRAFT_NUMBER']),
        np.nan
    )
    
    # Draft category
    def categorize_pick(draft_num):
        if pd.isna(draft_num):
            return 'Undrafted'
        elif draft_num <= 5:
            return 'Lottery (1-5)'
        elif draft_num <= 14:
            return 'Lottery (6-14)'
        elif draft_num <= 30:
            return 'First Round (15-30)'
        else:
            return 'Second Round (31+)'
    
    df_enhanced['draft_category'] = df_enhanced['DRAFT_NUMBER'].apply(categorize_pick)
    
    # Quality tier
    def quality_tier(value_score):
        if value_score >= 200:
            return 'Elite (200+)'
        elif value_score >= 100:
            return 'High Quality (100-199)'
        elif value_score >= 50:
            return 'Solid Contributor (50-99)'
        elif value_score >= 20:
            return 'Role Player (20-49)'
        else:
            return 'Limited Impact (0-19)'
    
    df_enhanced['quality_tier'] = df_enhanced['value_score'].apply(quality_tier)
    
    return df_enhanced

def main():
    # Header
    st.markdown('<h1 class="main-header">NBA Draft ROI Analysis Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #6C757D; margin-bottom: 3rem;">Comprehensive Analysis of Draft Performance and Return on Investment</p>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    team_efficiency_df = load_team_efficiency_data()
    df_enhanced = calculate_enhanced_metrics(df)
    
    # Sidebar filters
    st.sidebar.markdown("## Analysis Filters")
    st.sidebar.markdown("---")
    
    # Year range filter
    if 'DRAFT_YEAR' in df.columns:
        draft_years = df['DRAFT_YEAR'].dropna()
        if len(draft_years) > 0:
            year_range = st.sidebar.slider(
                "Draft Year Range",
                min_value=int(draft_years.min()),
                max_value=int(draft_years.max()),
                value=(int(draft_years.min()), int(draft_years.max())),
                help="Select the range of draft years to analyze"
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
                default=available_rounds,
                help="Select specific draft rounds to include in analysis"
            )
            if selected_rounds:
                df_filtered = df_filtered[df_filtered['DRAFT_ROUND'].isin(selected_rounds)]
    
    # Filter for drafted players only
    drafted_players = df_filtered[df_filtered['draft_value_ratio'].notna()]
    
    # Executive Summary Section
    st.markdown('<h2 class="sub-header">Executive Summary</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Players Analyzed",
            value=f"{len(df_filtered):,}",
            delta=f"Covering {len(df_filtered['DRAFT_YEAR'].dropna().unique()) if 'DRAFT_YEAR' in df_filtered.columns else 'All'} draft years"
        )
    
    with col2:
        st.metric(
            label="Drafted Players",
            value=f"{len(drafted_players):,}",
            delta=f"{len(drafted_players)/len(df_filtered)*100:.1f}% of dataset"
        )
    
    with col3:
        if len(drafted_players) > 0:
            avg_roi = drafted_players['draft_value_ratio'].mean()
            st.metric(
                label="Average ROI",
                value=f"{avg_roi:.2f}",
                delta="Value per draft position"
            )
    
    with col4:
        if len(df_filtered) > 0:
            avg_career = df_filtered['career_length'].mean()
            st.metric(
                label="Average Career Length",
                value=f"{avg_career:.1f} years",
                delta="All players in dataset"
            )
    
    # Main Analysis Sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Performance Visualization", "Top Performers Analysis", "Team Draft Efficiency", "Statistical Analysis", "Data Explorer"])
    
    with tab1:
        st.markdown('<h2 class="section-header">Performance Visualization</h2>', unsafe_allow_html=True)
        
        # Create three columns for the three main plots
        viz_col1, viz_col2 = st.columns(2)
        
        with viz_col1:
            st.subheader("Draft Position vs Player Value")
            st.markdown("*Analysis of the relationship between draft position and career value*")
            if len(drafted_players) > 0:
                fig1 = px.scatter(
                    drafted_players, 
                    x='DRAFT_NUMBER', 
                    y='value_score',
                    hover_data=['PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'DRAFT_YEAR'],
                    title="Draft Number vs Value Score",
                    labels={'DRAFT_NUMBER': 'Draft Position', 'value_score': 'Career Value Score'},
                    color_discrete_sequence=['#C8102E']
                )
                fig1.add_scatter(
                    x=drafted_players['DRAFT_NUMBER'], 
                    y=np.poly1d(np.polyfit(drafted_players['DRAFT_NUMBER'], drafted_players['value_score'], 1))(drafted_players['DRAFT_NUMBER']),
                    mode='lines',
                    name='Trend Line',
                    line=dict(color='#ef4444', dash='dash', width=3)
                )
                fig1.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12)
                )
                st.plotly_chart(fig1, use_container_width=True)
        
        with viz_col2:
            st.subheader("ROI Efficiency by Draft Round")
            st.markdown("*Average return on investment across different draft rounds*")
            if len(drafted_players) > 0:
                roi_by_round = drafted_players.groupby('DRAFT_ROUND')['draft_value_ratio'].mean().reset_index()
                fig2 = px.line(
                    roi_by_round, 
                    x='DRAFT_ROUND', 
                    y='draft_value_ratio',
                    markers=True,
                    title="Average ROI by Draft Round",
                    labels={'DRAFT_ROUND': 'Draft Round', 'draft_value_ratio': 'Average ROI'},
                    color_discrete_sequence=['#FDB927']
                )
                fig2.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12)
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        # Top 10 ROI Players Bar Chart (full width)
        st.subheader("Highest ROI Draft Selections")
        st.markdown("*Players who significantly exceeded expectations relative to their draft position*")
        if len(drafted_players) > 0:
            top_10_roi = drafted_players.nlargest(10, 'draft_value_ratio')
            top_10_roi['player_name'] = top_10_roi['PLAYER_FIRST_NAME'] + ' ' + top_10_roi['PLAYER_LAST_NAME']
            
            fig3 = px.bar(
                top_10_roi,
                x='player_name',
                y='draft_value_ratio',
                title="Top 10 Players by Draft ROI",
                labels={'player_name': 'Player', 'draft_value_ratio': 'Return on Investment'},
                hover_data=['DRAFT_YEAR', 'DRAFT_NUMBER', 'value_score'],
                color='draft_value_ratio',
                color_continuous_scale='Reds'
            )
            fig3.update_layout(
                xaxis_tickangle=45,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12)
            )
            st.plotly_chart(fig3, use_container_width=True)
    
    with tab2:
        st.markdown('<h2 class="section-header">Top Performers Analysis</h2>', unsafe_allow_html=True)
        
        perf_col1, perf_col2 = st.columns(2)
        
        with perf_col1:
            st.subheader("Highest ROI Players")
            st.markdown("*Players with the best value relative to draft position*")
            if len(drafted_players) > 0:
                top_roi = drafted_players.nlargest(10, 'draft_value_ratio')[
                    ['PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'DRAFT_YEAR', 'DRAFT_NUMBER', 
                     'draft_value_ratio', 'value_score', 'career_length']
                ]
                
                for i, (_, player) in enumerate(top_roi.iterrows(), 1):
                    st.markdown(f"""
                    <div class="player-card">
                        <strong>{i}. {player['PLAYER_FIRST_NAME']} {player['PLAYER_LAST_NAME']}</strong><br>
                        <strong>ROI:</strong> {player['draft_value_ratio']:.2f} | 
                        <strong>Draft:</strong> {player['DRAFT_YEAR']:.0f} (#{int(player['DRAFT_NUMBER'])})<br>
                        <strong>Career:</strong> {player['career_length']} years | 
                        <strong>Value Score:</strong> {player['value_score']:.1f}
                    </div>
                    """, unsafe_allow_html=True)
        
        with perf_col2:
            st.subheader("Highest Value Score Players")
            st.markdown("*Players with the highest overall career value*")
            if len(df_filtered) > 0:
                top_value = df_filtered.nlargest(10, 'value_score')[
                    ['PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'DRAFT_YEAR', 'DRAFT_NUMBER', 
                     'value_score', 'PTS', 'REB', 'AST', 'career_length']
                ]
                
                for i, (_, player) in enumerate(top_value.iterrows(), 1):
                    draft_info = f"#{int(player['DRAFT_NUMBER'])}" if pd.notna(player['DRAFT_NUMBER']) else "Undrafted"
                    st.markdown(f"""
                    <div class="player-card">
                        <strong>{i}. {player['PLAYER_FIRST_NAME']} {player['PLAYER_LAST_NAME']}</strong><br>
                        <strong>Value Score:</strong> {player['value_score']:.1f} | 
                        <strong>Draft:</strong> {player['DRAFT_YEAR']:.0f} ({draft_info})<br>
                        <strong>Stats:</strong> {player['PTS']:.1f} PTS, {player['REB']:.1f} REB, {player['AST']:.1f} AST<br>
                        <strong>Career:</strong> {player['career_length']} years
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h2 class="section-header">Team Draft Efficiency</h2>', unsafe_allow_html=True)
        
        if team_efficiency_df is not None:
            # Team efficiency overview
            st.subheader("📊 Team Draft Efficiency Overview")
            st.markdown("*Comprehensive analysis of which NBA franchises consistently find draft value*")
            
            # Top level metrics
            eff_col1, eff_col2, eff_col3, eff_col4 = st.columns(4)
            
            with eff_col1:
                st.metric(
                    label="Teams Analyzed",
                    value=f"{len(team_efficiency_df)}",
                    delta="Minimum 10 draft picks"
                )
            
            with eff_col2:
                best_roi_team = team_efficiency_df.nlargest(1, 'avg_roi_per_season').iloc[0]
                st.metric(
                    label="Best ROI/Season",
                    value=f"{best_roi_team['avg_roi_per_season']:.3f}",
                    delta=f"{best_roi_team.name}"
                )
            
            with eff_col3:
                best_quality_team = team_efficiency_df.nlargest(1, 'quality_pick_rate').iloc[0]
                st.metric(
                    label="Best Quality Rate",
                    value=f"{best_quality_team['quality_pick_rate']:.1f}%",
                    delta=f"{best_quality_team.name}"
                )
            
            with eff_col4:
                best_gems_team = team_efficiency_df.nlargest(1, 'late_round_gems').iloc[0]
                st.metric(
                    label="Most Late Round Gems",
                    value=f"{int(best_gems_team['late_round_gems'])}",
                    delta=f"{best_gems_team.name}"
                )
            
            # Visualizations
            viz_tab1, viz_tab2, viz_tab3 = st.tabs(["Team Rankings", "Efficiency Matrix", "Draft Success Analysis"])
            
            with viz_tab1:
                st.subheader("🏆 Top Performing Teams by ROI per Season")
                top_15_teams = team_efficiency_df.nlargest(15, 'avg_roi_per_season').reset_index()
                
                fig_top_teams = px.bar(
                    top_15_teams,
                    x='TEAM_NAME',
                    y='avg_roi_per_season',
                    title='Top 15 Teams: Average ROI per Season',
                    labels={'avg_roi_per_season': 'Average ROI per Season', 'TEAM_NAME': 'Team'},
                    color='avg_roi_per_season',
                    color_continuous_scale='Reds',
                    hover_data=['total_picks', 'quality_pick_rate', 'late_round_gems']
                )
                fig_top_teams.update_layout(
                    xaxis_tickangle=45,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=500
                )
                st.plotly_chart(fig_top_teams, use_container_width=True)
                
                # Data table
                st.subheader("📋 Team Performance Summary")
                display_columns = ['total_picks', 'avg_roi_per_season', 'quality_pick_rate', 
                                 'late_round_gems', 'avg_value', 'avg_career_length']
                
                # Reset index to show team names as a column
                team_display_df = team_efficiency_df[display_columns].round(3).reset_index()
                
                st.dataframe(
                    team_display_df,
                    use_container_width=True,
                    column_config={
                        "TEAM_NAME": st.column_config.TextColumn("Team Name"),
                        "total_picks": st.column_config.NumberColumn("Total Picks", format="%d"),
                        "avg_roi_per_season": st.column_config.NumberColumn("Avg ROI/Season", format="%.3f"),
                        "quality_pick_rate": st.column_config.NumberColumn("Quality Pick %", format="%.1f%%"),
                        "late_round_gems": st.column_config.NumberColumn("Late Round Gems", format="%d"),
                        "avg_value": st.column_config.NumberColumn("Avg Player Value", format="%.1f"),
                        "avg_career_length": st.column_config.NumberColumn("Avg Career Length", format="%.1f")
                    }
                )
            
            with viz_tab2:
                st.subheader("📈 Draft Efficiency Matrix")
                st.markdown("*Comparing volume of picks vs quality of results*")
                
                fig_matrix = px.scatter(
                    team_efficiency_df.reset_index(),
                    x='total_picks',
                    y='quality_pick_rate',
                    size='avg_value',
                    color='avg_roi_per_season',
                    hover_name='TEAM_NAME',
                    title='Draft Efficiency Matrix: Quality vs Volume',
                    labels={
                        'total_picks': 'Total Draft Picks',
                        'quality_pick_rate': 'Quality Pick Rate (%)',
                        'avg_value': 'Average Player Value',
                        'avg_roi_per_season': 'Avg ROI/Season'
                    },
                    color_continuous_scale='RdYlBu_r'
                )
                fig_matrix.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=500
                )
                st.plotly_chart(fig_matrix, use_container_width=True)
                
                # Insights
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                avg_quality_rate = team_efficiency_df['quality_pick_rate'].mean()
                high_volume_teams = team_efficiency_df[team_efficiency_df['total_picks'] > team_efficiency_df['total_picks'].median()]
                best_high_volume = high_volume_teams.nlargest(1, 'quality_pick_rate').index[0]
                
                st.markdown(f"**📊 Matrix Insights:**")
                st.markdown(f"• League average quality pick rate: **{avg_quality_rate:.1f}%**")
                st.markdown(f"• Best high-volume team (quality): **{best_high_volume}**")
                st.markdown(f"• Teams in top-right quadrant excel at both volume and quality")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with viz_tab3:
                st.subheader("💎 Late Round Success Stories")
                
                # Late round gems chart
                top_gems = team_efficiency_df.nlargest(12, 'late_round_gems').reset_index()
                
                fig_gems = px.bar(
                    top_gems,
                    x='TEAM_NAME',
                    y='late_round_gems',
                    title='Best at Finding Late Round Gems (Picks 16+, Value 100+)',
                    labels={'late_round_gems': 'Late Round Gems Found', 'TEAM_NAME': 'Team'},
                    color='late_round_gems',
                    color_continuous_scale='Blues',
                    hover_data=['quality_pick_rate', 'avg_draft_position']
                )
                fig_gems.update_layout(
                    xaxis_tickangle=45,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=400
                )
                st.plotly_chart(fig_gems, use_container_width=True)
                
                # Draft position efficiency
                st.subheader("🎯 Draft Position Analysis")
                drafted_enhanced = df_enhanced[df_enhanced['DRAFT_NUMBER'].notna()]
                
                position_analysis = drafted_enhanced.groupby('draft_category').agg({
                    'roi_per_season': 'mean',
                    'value_score': 'mean',
                    'PLAYER_FIRST_NAME': 'count'
                }).round(3)
                position_analysis.columns = ['Avg ROI/Season', 'Avg Value Score', 'Total Players']
                
                st.dataframe(
                    position_analysis,
                    use_container_width=True,
                    column_config={
                        "Avg ROI/Season": st.column_config.NumberColumn("Avg ROI/Season", format="%.3f"),
                        "Avg Value Score": st.column_config.NumberColumn("Avg Value Score", format="%.1f"),
                        "Total Players": st.column_config.NumberColumn("Total Players", format="%d")
                    }
                )
            
            # Key Insights Section
            st.markdown('<h3 class="section-header">🔍 Key Draft Efficiency Insights</h3>', unsafe_allow_html=True)
            
            insight_col1, insight_col2 = st.columns(2)
            
            with insight_col1:
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                st.markdown("**🏆 Top Performers:**")
                top_roi = team_efficiency_df.nlargest(3, 'avg_roi_per_season')
                for i, (team, data) in enumerate(top_roi.iterrows(), 1):
                    st.markdown(f"**{i}.** {team} - {data['avg_roi_per_season']:.3f} ROI/season")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                st.markdown("**💎 Late Round Specialists:**")
                top_gems = team_efficiency_df.nlargest(3, 'late_round_gems')
                for i, (team, data) in enumerate(top_gems.iterrows(), 1):
                    st.markdown(f"**{i}.** {team} - {int(data['late_round_gems'])} gems found")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with insight_col2:
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                st.markdown("**🎯 Quality Pick Leaders:**")
                top_quality = team_efficiency_df.nlargest(3, 'quality_pick_rate')
                for i, (team, data) in enumerate(top_quality.iterrows(), 1):
                    st.markdown(f"**{i}.** {team} - {data['quality_pick_rate']:.1f}% quality rate")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                st.markdown("**📊 League Averages:**")
                st.markdown(f"• Quality Pick Rate: **{team_efficiency_df['quality_pick_rate'].mean():.1f}%**")
                st.markdown(f"• ROI per Season: **{team_efficiency_df['avg_roi_per_season'].mean():.3f}**")
                st.markdown(f"• Late Round Gems: **{team_efficiency_df['late_round_gems'].mean():.1f}**")
                st.markdown('</div>', unsafe_allow_html=True)
                
        else:
            st.warning("⚠️ Team efficiency data not available. Please run `team_draft_efficiency.py` to generate the report.")
            st.code("python team_draft_efficiency.py", language="bash")
    
    with tab4:
        st.markdown('<h2 class="section-header">Statistical Analysis</h2>', unsafe_allow_html=True)
        
        analysis_col1, analysis_col2 = st.columns(2)
        
        with analysis_col1:
            st.subheader("ROI Performance by Draft Round")
            st.markdown("*Statistical breakdown of return on investment across draft rounds*")
            if len(drafted_players) > 0:
                round_analysis = drafted_players.groupby('DRAFT_ROUND')['draft_value_ratio'].agg([
                    'count', 'mean', 'median', 'std'
                ]).round(3)
                round_analysis.columns = ['Players', 'Mean ROI', 'Median ROI', 'Std Deviation']
                round_analysis = round_analysis.sort_values('Mean ROI', ascending=False)
                
                st.dataframe(
                    round_analysis, 
                    use_container_width=True,
                    column_config={
                        "Players": st.column_config.NumberColumn("Players", format="%d"),
                        "Mean ROI": st.column_config.NumberColumn("Mean ROI", format="%.3f"),
                        "Median ROI": st.column_config.NumberColumn("Median ROI", format="%.3f"),
                        "Std Deviation": st.column_config.NumberColumn("Std Deviation", format="%.3f")
                    }
                )
                
                # Key insights
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                best_round = round_analysis.index[0]
                best_roi = round_analysis.iloc[0]['Mean ROI']
                st.markdown(f"**Key Insight:** Round {int(best_round)} provides the highest average ROI at {best_roi:.3f}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with analysis_col2:
            st.subheader("Team Drafting Performance")
            st.markdown("*Historical drafting success by NBA franchises*")
            if len(drafted_players) > 0:
                team_analysis = drafted_players.groupby('TEAM_NAME').agg({
                    'draft_value_ratio': ['count', 'mean', 'sum'],
                    'DRAFT_NUMBER': 'mean'
                }).round(3)
                team_analysis.columns = ['Players', 'Avg ROI', 'Total ROI', 'Avg Draft Position']
                team_analysis = team_analysis[team_analysis['Players'] >= 5]  # At least 5 players
                team_analysis = team_analysis.sort_values('Avg ROI', ascending=False)
                
                st.dataframe(
                    team_analysis.head(15), 
                    use_container_width=True,
                    column_config={
                        "Players": st.column_config.NumberColumn("Players", format="%d"),
                        "Avg ROI": st.column_config.NumberColumn("Avg ROI", format="%.3f"),
                        "Total ROI": st.column_config.NumberColumn("Total ROI", format="%.3f"),
                        "Avg Draft Position": st.column_config.NumberColumn("Avg Draft Position", format="%.1f")
                    }
                )
                
                # Key insights
                st.markdown('<div class="insight-box">', unsafe_allow_html=True)
                best_team = team_analysis.index[0]
                best_team_roi = team_analysis.iloc[0]['Avg ROI']
                st.markdown(f"**Key Insight:** {best_team} leads in drafting efficiency with {best_team_roi:.3f} average ROI")
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Value Score Distribution
        st.subheader("Career Value Distribution Analysis")
        st.markdown("*Distribution of player value scores across the dataset*")
        if len(df_filtered) > 0:
            fig_hist = px.histogram(
                df_filtered, 
                x='value_score', 
                nbins=50,
                title="Distribution of Career Value Scores",
                labels={'value_score': 'Career Value Score', 'count': 'Number of Players'},
                color_discrete_sequence=['#1D428A']
            )
            fig_hist.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12)
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            
            # Statistical summary
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Mean Value Score", f"{df_filtered['value_score'].mean():.1f}")
            with col2:
                st.metric("Median Value Score", f"{df_filtered['value_score'].median():.1f}")
            with col3:
                st.metric("Standard Deviation", f"{df_filtered['value_score'].std():.1f}")
            with col4:
                st.metric("Maximum Value Score", f"{df_filtered['value_score'].max():.1f}")
    
    with tab5:
        st.markdown('<h2 class="section-header">Data Explorer</h2>', unsafe_allow_html=True)
        
        # Search functionality
        search_col1, search_col2 = st.columns([2, 1])
        
        with search_col1:
            search_player = st.text_input(
                "Search for a player:", 
                placeholder="Enter player first or last name...",
                help="Search functionality is case-insensitive"
            )
        
        with search_col2:
            show_all = st.checkbox("Show all players", value=False)
        
        # Filter data based on search
        if search_player:
            mask = (df_filtered['PLAYER_FIRST_NAME'].str.contains(search_player, case=False, na=False) | 
                   df_filtered['PLAYER_LAST_NAME'].str.contains(search_player, case=False, na=False))
            display_df = df_filtered[mask]
            if len(display_df) > 0:
                st.success(f"Found {len(display_df)} player(s) matching '{search_player}'")
            else:
                st.warning(f"No players found matching '{search_player}'")
        elif show_all:
            display_df = df_filtered
            st.info(f"Displaying all {len(display_df)} players in the filtered dataset")
        else:
            display_df = df_filtered.head(100)  # Show first 100 by default
            st.info("Displaying first 100 players. Use search or 'Show all players' to see more.")
        
        # Select columns to display
        available_columns = ['PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'DRAFT_YEAR', 'DRAFT_ROUND', 
                           'DRAFT_NUMBER', 'TEAM_NAME', 'PTS', 'REB', 'AST', 'career_length', 
                           'value_score', 'draft_value_ratio']
        
        # Filter to only show columns that exist in the dataframe
        available_columns = [col for col in available_columns if col in df_filtered.columns]
        
        selected_columns = st.multiselect(
            "Select columns to display:",
            options=available_columns,
            default=available_columns[:8],  # Show first 8 columns by default
            help="Choose which data columns to display in the table below"
        )
        
        if selected_columns and len(display_df) > 0:
            st.dataframe(
                display_df[selected_columns],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "PLAYER_FIRST_NAME": "First Name",
                    "PLAYER_LAST_NAME": "Last Name",
                    "DRAFT_YEAR": st.column_config.NumberColumn("Draft Year", format="%d"),
                    "DRAFT_ROUND": st.column_config.NumberColumn("Round", format="%d"),
                    "DRAFT_NUMBER": st.column_config.NumberColumn("Pick #", format="%d"),
                    "PTS": st.column_config.NumberColumn("PPG", format="%.1f"),
                    "REB": st.column_config.NumberColumn("RPG", format="%.1f"),
                    "AST": st.column_config.NumberColumn("APG", format="%.1f"),
                    "career_length": st.column_config.NumberColumn("Career Length", format="%d"),
                    "value_score": st.column_config.NumberColumn("Value Score", format="%.1f"),
                    "draft_value_ratio": st.column_config.NumberColumn("ROI", format="%.3f")
                }
            )
        
        # Download button
        if len(display_df) > 0:
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="Download filtered data as CSV",
                data=csv,
                file_name="nba_draft_roi_analysis.csv",
                mime="text/csv",
                help="Download the currently filtered data as a CSV file"
            )
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #6C757D; margin-top: 3rem; padding: 2rem; background-color: #F8F9FA; border-radius: 12px; border: 1px solid #E9ECEF;'>
        <h4 style='color: #1A1D29; margin-bottom: 1rem; font-weight: 600;'>NBA Draft ROI Analysis Dashboard</h4>
        <p style='margin-bottom: 0.5rem; color: #495057;'><strong>Professional Analytics Platform</strong></p>
        <p style='margin-bottom: 0.5rem; color: #6C757D;'>Comprehensive analysis of NBA draft performance and return on investment</p>
        <p style='margin-bottom: 0; color: #ADB5BD; font-style: italic;'>Built with advanced data science methodologies and interactive visualization</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
