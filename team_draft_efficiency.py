import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set up pr NBA styling
plt.style.use('default')
COLORS = {
    'primary': '#C8102E',      # NBA red
    'secondary': '#1D428A',    # Royal blue  
    'accent': '#FDB927',       # Lakers gold
    'success': '#00788C',      # Teal
    'chart_colors': ['#C8102E', '#1D428A', '#FDB927', '#00788C', '#FF6900', '#CE1141']
}

def calculate_per_season_roi(df):
    """
    Calculate ROI per season played, giving more weight to efficiency
    """
    print("Calculating Per-Season ROI Metrics...")
    
    # Create enhanced metrics
    df_enhanced = df.copy()
    
    # 1. ROI per season (value per year, adjusted by draft position)
    df_enhanced['roi_per_season'] = np.where(
        (df_enhanced['career_length'] > 0) & (df_enhanced['DRAFT_NUMBER'].notna()),
        df_enhanced['value_score'] / (df_enhanced['career_length'] * df_enhanced['DRAFT_NUMBER']),
        np.nan
    )
    
    # 2. Efficiency score (performance relative to expectations)
    df_enhanced['expected_value'] = np.where(
        df_enhanced['DRAFT_NUMBER'].notna(),
        100 - df_enhanced['DRAFT_NUMBER'],  # Higher picks have higher expectations
        0
    )
    
    df_enhanced['efficiency_score'] = np.where(
        df_enhanced['expected_value'] > 0,
        df_enhanced['value_score'] / df_enhanced['expected_value'],
        np.nan
    )
    
    # 3. Draft value category
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
    
    # 4. Quality tiers based on performance
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
    
    print(f"✅ Enhanced metrics calculated for {len(df_enhanced)} players")
    return df_enhanced

def analyze_team_draft_efficiency(df_enhanced):
    """
    Comprehensive team draft efficiency analysis
    """
    print("🏆 Analyzing Team Draft Efficiency...")
    
    # Filter to drafted players only
    drafted = df_enhanced[df_enhanced['DRAFT_NUMBER'].notna()].copy()
    
    if len(drafted) == 0:
        print("❌ No drafted players found")
        return None
    
    # Team-level aggregations
    team_stats = drafted.groupby('TEAM_NAME').agg({
        'PLAYER_FIRST_NAME': 'count',  # Total picks
        'value_score': ['mean', 'sum', 'std'],
        'roi_per_season': ['mean', 'median'],
        'efficiency_score': ['mean', 'median'],
        'career_length': 'mean',
        'DRAFT_NUMBER': 'mean',
        'DRAFT_YEAR': ['min', 'max']
    }).round(3)
    
    # Flatten column names
    team_stats.columns = [
        'total_picks', 'avg_value', 'total_value', 'value_std',
        'avg_roi_per_season', 'median_roi_per_season',
        'avg_efficiency', 'median_efficiency',
        'avg_career_length', 'avg_draft_position',
        'first_draft_year', 'last_draft_year'
    ]
    
    # Calculate draft span
    team_stats['draft_span_years'] = team_stats['last_draft_year'] - team_stats['first_draft_year'] + 1
    
    # Quality picks analysis
    quality_picks = drafted[drafted['value_score'] >= 50].groupby('TEAM_NAME').size()
    elite_picks = drafted[drafted['value_score'] >= 200].groupby('TEAM_NAME').size()
    
    team_stats['quality_picks'] = team_stats.index.map(quality_picks).fillna(0)
    team_stats['elite_picks'] = team_stats.index.map(elite_picks).fillna(0)
    
    # Calculate efficiency rates
    team_stats['quality_pick_rate'] = (team_stats['quality_picks'] / team_stats['total_picks'] * 100).round(1)
    team_stats['elite_pick_rate'] = (team_stats['elite_picks'] / team_stats['total_picks'] * 100).round(1)
    
    # Draft position efficiency (finding gems in later rounds)
    late_round_gems = drafted[(drafted['DRAFT_NUMBER'] > 15) & (drafted['value_score'] >= 100)]
    late_gems_by_team = late_round_gems.groupby('TEAM_NAME').size()
    team_stats['late_round_gems'] = team_stats.index.map(late_gems_by_team).fillna(0)
    
    # Filter teams with meaningful sample size (minimum 10 picks)
    qualified_teams = team_stats[team_stats['total_picks'] >= 10].copy()
    
    print(f"Analysis complete for {len(qualified_teams)} qualified teams")
    return qualified_teams, drafted

def create_team_efficiency_dashboard(team_stats, drafted_players):
    """
    Create comprehensive visualizations for team draft efficiency
    """
    print("Creating Team Draft Efficiency Dashboard...")
    
    # 1. Top Performing Teams by ROI per Season
    fig1 = px.bar(
        team_stats.nlargest(15, 'avg_roi_per_season').reset_index(),
        x='TEAM_NAME',
        y='avg_roi_per_season',
        title='Top 15 Teams: Average ROI per Season',
        labels={'avg_roi_per_season': 'Average ROI per Season', 'TEAM_NAME': 'Team'},
        color='avg_roi_per_season',
        color_continuous_scale='Reds'
    )
    fig1.update_layout(
        xaxis_tickangle=45,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500
    )
    fig1.show()
    
    # 2. Draft Efficiency Matrix (Quality vs Quantity)
    fig2 = px.scatter(
        team_stats.reset_index(),
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
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500
    )
    fig2.show()
    
    # 3. Late Round Success Stories
    fig3 = px.bar(
        team_stats.nlargest(10, 'late_round_gems').reset_index(),
        x='TEAM_NAME',
        y='late_round_gems',
        title='Best at Finding Late Round Gems (Picks 16+, Value 100+)',
        labels={'late_round_gems': 'Late Round Gems Found', 'TEAM_NAME': 'Team'},
        color='late_round_gems',
        color_continuous_scale='Blues'
    )
    fig3.update_layout(
        xaxis_tickangle=45,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    fig3.show()
    
    # 4. Team Consistency Analysis
    consistency_data = team_stats[['avg_efficiency', 'value_std']].copy()
    consistency_data['consistency_score'] = consistency_data['avg_efficiency'] / (consistency_data['value_std'] + 1)
    
    fig4 = px.scatter(
        consistency_data.reset_index(),
        x='value_std',
        y='avg_efficiency',
        size='consistency_score',
        hover_name='TEAM_NAME',
        title='Draft Consistency: Efficiency vs Variability',
        labels={
            'value_std': 'Value Standard Deviation (Lower = More Consistent)',
            'avg_efficiency': 'Average Efficiency Score',
            'consistency_score': 'Consistency Score'
        },
        color_discrete_sequence=[COLORS['secondary']]
    )
    fig4.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500
    )
    fig4.show()
    
    print("✅ Dashboard visualizations created successfully!")

def generate_draft_efficiency_report(team_stats, drafted_players):
    """
    Generate comprehensive text report
    """
    print("📋 Generating Draft Efficiency Report...")
    print("=" * 80)
    print("🏀 NBA TEAM DRAFT EFFICIENCY REPORT")
    print("=" * 80)
    
    # Top performers in each category
    print("\n🏆 TOP PERFORMERS BY CATEGORY")
    print("-" * 50)
    
    print(f"\n📈 Best ROI per Season:")
    top_roi = team_stats.nlargest(5, 'avg_roi_per_season')
    for i, (team, data) in enumerate(top_roi.iterrows(), 1):
        print(f"{i:2d}. {team:<20} {data['avg_roi_per_season']:.3f} ROI/season")
    
    print(f"\n🎯 Highest Quality Pick Rate:")
    top_quality = team_stats.nlargest(5, 'quality_pick_rate')
    for i, (team, data) in enumerate(top_quality.iterrows(), 1):
        print(f"{i:2d}. {team:<20} {data['quality_pick_rate']:.1f}% quality picks")
    
    print(f"\n💎 Best at Finding Late Round Gems:")
    top_gems = team_stats.nlargest(5, 'late_round_gems')
    for i, (team, data) in enumerate(top_gems.iterrows(), 1):
        print(f"{i:2d}. {team:<20} {int(data['late_round_gems'])} late round gems")
    
    # Draft position analysis
    print(f"\n📊 DRAFT EFFICIENCY BY POSITION")
    print("-" * 50)
    
    position_analysis = drafted_players.groupby('draft_category').agg({
        'roi_per_season': 'mean',
        'efficiency_score': 'mean',
        'value_score': 'mean',
        'PLAYER_FIRST_NAME': 'count'
    }).round(3)
    
    for category, data in position_analysis.iterrows():
        print(f"{category:<20} | ROI/Season: {data['roi_per_season']:.3f} | "
              f"Efficiency: {data['efficiency_score']:.3f} | "
              f"Players: {int(data['PLAYER_FIRST_NAME'])}")
    
    # Success stories
    print(f"\n⭐ NOTABLE SUCCESS STORIES")
    print("-" * 50)
    
    # Best late round picks
    late_successes = drafted_players[
        (drafted_players['DRAFT_NUMBER'] > 30) & 
        (drafted_players['value_score'] >= 150)
    ].nlargest(5, 'value_score')
    
    print("\nBest Second Round Picks (31+):")
    for _, player in late_successes.iterrows():
        print(f"• {player['PLAYER_FIRST_NAME']} {player['PLAYER_LAST_NAME']} "
              f"(#{int(player['DRAFT_NUMBER'])}, {player['TEAM_NAME']}) - "
              f"Value: {player['value_score']:.1f}")
    
    # Team insights
    print(f"\n🔍 KEY INSIGHTS")
    print("-" * 50)
    
    best_overall = team_stats.nlargest(1, 'avg_roi_per_season').index[0]
    most_consistent = team_stats.nsmallest(1, 'value_std').index[0]
    best_late_round = team_stats.nlargest(1, 'late_round_gems').index[0]
    
    print(f"• Best Overall Draft Efficiency: {best_overall}")
    print(f"• Most Consistent Drafting: {most_consistent}")
    print(f"• Best at Late Round Picks: {best_late_round}")
    
    avg_quality_rate = team_stats['quality_pick_rate'].mean()
    print(f"• League Average Quality Pick Rate: {avg_quality_rate:.1f}%")
    
    print("\n" + "=" * 80)

def main():
    """
    Main execution function
    """
    try:
        print("🏀 NBA TEAM DRAFT EFFICIENCY ANALYSIS")
        print("=" * 50)
        
        # Load data
        print("📁 Loading NBA data with value metrics...")
        df = pd.read_csv("NBAStats_with_value_metrics.csv")
        print(f"✅ Loaded {len(df)} players")
        
        # Calculate enhanced metrics
        df_enhanced = calculate_per_season_roi(df)
        
        # Analyze team efficiency
        team_stats, drafted_players = analyze_team_draft_efficiency(df_enhanced)
        
        if team_stats is not None:
            # Create visualizations
            create_team_efficiency_dashboard(team_stats, drafted_players)
            
            # Generate report
            generate_draft_efficiency_report(team_stats, drafted_players)
            
            # Save results
            team_stats.to_csv("team_draft_efficiency_report.csv")
            print(f"\n💾 Results saved to 'team_draft_efficiency_report.csv'")
            
        print("\n🎉 Analysis complete!")
        
    except FileNotFoundError:
        print("❌ Could not find 'NBAStats_with_value_metrics.csv'")
        print("Please run value_metrics.py first to generate the enhanced dataset.")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
