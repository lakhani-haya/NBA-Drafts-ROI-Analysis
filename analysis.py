import pandas as pd
import numpy as np

def analyze_top_roi_players(df):
    """
    Analyze and display the top 10 ROI players
    
    Args:
        df (pd.DataFrame): DataFrame with value metrics
    """
    
    print("=" * 50)
    print("TOP 10 ROI PLAYERS")
    print("=" * 50)
    
    # Filter ondrafted players with valid ROI
    drafted_players = df[df['draft_value_ratio'].notna()]
    
    if len(drafted_players) == 0:
        print("No drafted players with valid ROI found.")
        return
    
    # Get top 10 by ROI
    top_roi_players = drafted_players.nlargest(10, 'draft_value_ratio')[
        ['PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'DRAFT_YEAR', 'DRAFT_NUMBER', 
         'value_score', 'draft_value_ratio', 'PTS', 'REB', 'AST', 'career_length']
    ]
    
    for i, (_, player) in enumerate(top_roi_players.iterrows(), 1):
        print(f"{i:2d}. {player['PLAYER_FIRST_NAME']} {player['PLAYER_LAST_NAME']}")
        print(f"     ROI: {player['draft_value_ratio']:.1f}")
        print(f"     Draft: {player['DRAFT_YEAR']:.0f} (#{int(player['DRAFT_NUMBER'])})")
        print(f"     Career: {player['career_length']} years")
        print(f"     Stats: {player['PTS']:.1f} PTS, {player['REB']:.1f} REB, {player['AST']:.1f} AST")
        print(f"     Value Score: {player['value_score']:.1f}")
        print()

def analyze_draft_rounds_roi(df):
    """
    Analyze which draft rounds deliver the most ROI on average
    
    Args:
        df (pd.DataFrame): DataFrame with value metrics
    """
    
    print("=" * 50)
    print("AVERAGE ROI BY DRAFT ROUND")
    print("=" * 50)
    
    # Filter only drafted players with valid ROI
    drafted_players = df[df['draft_value_ratio'].notna()]
    
    if len(drafted_players) == 0:
        print("No drafted players with valid ROI found.")
        return
    
    # Group by draft round and calculate average ROI
    roi_by_round = drafted_players.groupby('DRAFT_ROUND')['draft_value_ratio'].agg([
        'count', 'mean', 'median', 'std'
    ]).round(2)
    
    # Sort by mean ROI (descending)
    roi_by_round_sorted = roi_by_round.sort_values('mean', ascending=False)
    
    print(f"{'Round':<8} {'Players':<8} {'Avg ROI':<10} {'Median ROI':<12} {'Std Dev':<10}")
    print("-" * 50)
    
    for round_num, stats in roi_by_round_sorted.iterrows():
        print(f"{int(round_num):<8} {int(stats['count']):<8} {stats['mean']:<10.1f} {stats['median']:<12.1f} {stats['std']:<10.1f}")
    
    print(f"\nKey Insights:")
    best_round = roi_by_round_sorted.index[0]
    best_roi = roi_by_round_sorted.iloc[0]['mean']
    print(f"• Best ROI Round: Round {int(best_round)} (Average ROI: {best_roi:.1f})")
    
    # Show rounds with most players
    most_players_round = roi_by_round_sorted.sort_values('count', ascending=False).index[0]
    most_players_count = roi_by_round_sorted.sort_values('count', ascending=False).iloc[0]['count']
    print(f"• Most Players: Round {int(most_players_round)} ({int(most_players_count)} players)")

def analyze_teams_drafting(df):
    """
    Analyze which teams drafted well historically
    
    Args:
        df (pd.DataFrame): DataFrame with value metrics
    """
    
    print("=" * 50)
    print("TEAMS WITH BEST HISTORICAL DRAFTING")
    print("=" * 50)
    
    # Filter only drafted players with valid ROI
    drafted_players = df[df['draft_value_ratio'].notna()]
    
    if len(drafted_players) == 0:
        print("No drafted players with valid ROI found.")
        return
    
    # Group by team and calculate drafting metrics
    team_drafting = drafted_players.groupby('TEAM_NAME').agg({
        'draft_value_ratio': ['count', 'mean', 'median', 'sum'],
        'value_score': 'mean',
        'DRAFT_NUMBER': 'mean'
    }).round(2)
    
    # Flatten column names
    team_drafting.columns = ['players_drafted', 'avg_roi', 'median_roi', 'total_roi', 'avg_value_score', 'avg_draft_position']
    
    # Filter teams with at least 10 drafted players for meaningful analysis
    min_players = 10
    qualified_teams = team_drafting[team_drafting['players_drafted'] >= min_players]
    
    if len(qualified_teams) == 0:
        print(f"No teams with at least {min_players} drafted players found.")
        return
    
    # Sort by average ROI
    best_drafting_teams = qualified_teams.sort_values('avg_roi', ascending=False)
    
    print(f"Teams with at least {min_players} drafted players:")
    print()
    print(f"{'Rank':<5} {'Team':<20} {'Players':<8} {'Avg ROI':<10} {'Total ROI':<12} {'Avg Draft Pos':<15}")
    print("-" * 75)
    
    for i, (team, stats) in enumerate(best_drafting_teams.head(15).iterrows(), 1):
        print(f"{i:<5} {team:<20} {int(stats['players_drafted']):<8} {stats['avg_roi']:<10.1f} {stats['total_roi']:<12.1f} {stats['avg_draft_position']:<15.1f}")
    
    print(f"\nTop 5 Teams by Average ROI:")
    for i, (team, stats) in enumerate(best_drafting_teams.head(5).iterrows(), 1):
        print(f"{i}. {team}: {stats['avg_roi']:.1f} avg ROI ({int(stats['players_drafted'])} players)")
    
    # Also show teams by total ROI (volume of good picks)
    print(f"\nTop 5 Teams by Total ROI (volume of good picks):")
    best_total_roi = qualified_teams.sort_values('total_roi', ascending=False)
    for i, (team, stats) in enumerate(best_total_roi.head(5).iterrows(), 1):
        print(f"{i}. {team}: {stats['total_roi']:.1f} total ROI ({int(stats['players_drafted'])} players)")

def main():
    """
    Main function to run all analysis
    """
    
    try:
        # Load data with value metrics
        print("Loading NBA data with value metrics...")
        df = pd.read_csv("NBAStats_with_value_metrics.csv")
        print(f"Loaded data with {len(df)} players")
        
        # Check if required columns exist
        required_columns = ['value_score', 'draft_value_ratio']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Error: Missing columns {missing_columns}")
            print("Please run value_metrics.py first to generate the value metrics.")
            return
        
        print(f"Found {len(df[df['draft_value_ratio'].notna()])} players with valid ROI data")
        print()
        
        # Run all analyses
        analyze_top_roi_players(df)
        print()
        analyze_draft_rounds_roi(df)
        print()
        analyze_teams_drafting(df)
        
        print("\n" + "=" * 50)
        print("ANALYSIS COMPLETE")
        print("=" * 50)
        
    except FileNotFoundError:
        print("Error: Could not find 'NBAStats_with_value_metrics.csv'")
        print("Please run value_metrics.py first to generate the value metrics.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
