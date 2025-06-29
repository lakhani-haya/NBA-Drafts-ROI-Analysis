import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_value_metrics(df):
    """
    Calculate value metrics for NBA players including value score and draft ROI
    
    Args:
        df (pd.DataFrame): Cleaned NBA stats dataframe
        
    Returns:
        pd.DataFrame: DataFrame with added value metrics
    """
    
    # Create a copy to avoid modifying the original dataframe
    df_metrics = df.copy()
    
    print("Calculating value metrics...")
    print(f"Starting with {len(df_metrics)} players")
    
    # Calculate value score = (PTS + REB + AST) * career_length
    df_metrics['value_score'] = (df_metrics['PTS'] + df_metrics['REB'] + df_metrics['AST']) * df_metrics['career_length']
    
    print(f"Value score calculated for all players")
    print(f"Value score range: {df_metrics['value_score'].min():.1f} to {df_metrics['value_score'].max():.1f}")
    
    # Calculate draft_value_ratio = value_score / DRAFT_NUMBER
    # Only for drafted players (those with valid DRAFT_NUMBER)
    drafted_players = df_metrics[df_metrics['DRAFT_NUMBER'].notna() & (df_metrics['DRAFT_NUMBER'] > 0)]
    
    print(f"\nCalculating ROI for {len(drafted_players)} drafted players...")
    
    # Calculate draft value ratio for drafted players
    df_metrics['draft_value_ratio'] = np.nan  # Initialize with NaN
    
    # Only calculate for players with valid draft numbers
    valid_draft_mask = (df_metrics['DRAFT_NUMBER'].notna()) & (df_metrics['DRAFT_NUMBER'] > 0)
    df_metrics.loc[valid_draft_mask, 'draft_value_ratio'] = (
        df_metrics.loc[valid_draft_mask, 'value_score'] / df_metrics.loc[valid_draft_mask, 'DRAFT_NUMBER']
    )
    
    print(f"Draft value ratio calculated for drafted players")
    print(f"Draft value ratio range: {df_metrics['draft_value_ratio'].min():.1f} to {df_metrics['draft_value_ratio'].max():.1f}")
    
    return df_metrics

def analyze_value_metrics(df_metrics):
    """
    Analyze and display insights about the calculated value metrics
    
    Args:
        df_metrics (pd.DataFrame): DataFrame with calculated value metrics
    """
    
    print("=" * 60)
    print("VALUE METRICS ANALYSIS")
    print("=" * 60)
    
    # Overall value score statistics
    print("\n1. VALUE SCORE STATISTICS")
    print("-" * 30)
    print(f"Mean value score: {df_metrics['value_score'].mean():.1f}")
    print(f"Median value score: {df_metrics['value_score'].median():.1f}")
    print(f"Standard deviation: {df_metrics['value_score'].std():.1f}")
    
    # Top performers by value score
    print("\n2. TOP 10 PLAYERS BY VALUE SCORE")
    print("-" * 40)
    top_value_players = df_metrics.nlargest(10, 'value_score')[
        ['PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'DRAFT_YEAR', 'DRAFT_NUMBER', 
         'career_length', 'PTS', 'REB', 'AST', 'value_score']
    ]
    
    for idx, player in top_value_players.iterrows():
        draft_info = f"#{int(player['DRAFT_NUMBER'])}" if pd.notna(player['DRAFT_NUMBER']) else "Undrafted"
        print(f"{player['PLAYER_FIRST_NAME']} {player['PLAYER_LAST_NAME']}: {player['value_score']:.1f}")
        print(f"   Draft: {player['DRAFT_YEAR']:.0f} ({draft_info}), Career: {player['career_length']} years")
        print(f"   Stats: {player['PTS']:.1f} PTS, {player['REB']:.1f} REB, {player['AST']:.1f} AST")
        print()
    
    # Draft ROI analysis (only for drafted players)
    drafted_players = df_metrics[df_metrics['draft_value_ratio'].notna()]
    
    if len(drafted_players) > 0:
        print("\n3. DRAFT ROI STATISTICS")
        print("-" * 25)
        print(f"Players with draft ROI calculated: {len(drafted_players)}")
        print(f"Mean draft value ratio: {drafted_players['draft_value_ratio'].mean():.1f}")
        print(f"Median draft value ratio: {drafted_players['draft_value_ratio'].median():.1f}")
        
        # Top ROI players
        print("\n4. TOP 10 PLAYERS BY DRAFT ROI")
        print("-" * 35)
        top_roi_players = drafted_players.nlargest(10, 'draft_value_ratio')[
            ['PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'DRAFT_YEAR', 'DRAFT_NUMBER', 
             'value_score', 'draft_value_ratio']
        ]
        
        for idx, player in top_roi_players.iterrows():
            print(f"{player['PLAYER_FIRST_NAME']} {player['PLAYER_LAST_NAME']}: ROI = {player['draft_value_ratio']:.1f}")
            print(f"   Draft: {player['DRAFT_YEAR']:.0f} (#{int(player['DRAFT_NUMBER'])})")
            print(f"   Value Score: {player['value_score']:.1f}")
            print()
        
        # Draft position analysis
        print("\n5. ROI BY DRAFT POSITION RANGES")
        print("-" * 35)
        
        # Create draft position bins
        drafted_players['draft_bin'] = pd.cut(
            drafted_players['DRAFT_NUMBER'], 
            bins=[0, 5, 10, 20, 30, 60, float('inf')], 
            labels=['1-5 (Lottery)', '6-10', '11-20', '21-30', '31-60', '60+']
        )
        
        roi_by_draft_position = drafted_players.groupby('draft_bin')['draft_value_ratio'].agg(['count', 'mean', 'median'])
        
        for draft_range, stats in roi_by_draft_position.iterrows():
            print(f"{draft_range}: {stats['count']} players")
            print(f"   Mean ROI: {stats['mean']:.1f}, Median ROI: {stats['median']:.1f}")
        
        # Identify steals and busts
        print("\n6. DRAFT STEALS AND BUSTS")
        print("-" * 30)
        
        # Steals: Late picks (30+) with high ROI
        steals = drafted_players[(drafted_players['DRAFT_NUMBER'] >= 30) & 
                                (drafted_players['draft_value_ratio'] >= drafted_players['draft_value_ratio'].quantile(0.8))]
        
        print(f"Draft Steals (picked 30+ with top 20% ROI): {len(steals)} players")
        if len(steals) > 0:
            top_steals = steals.nlargest(5, 'draft_value_ratio')[
                ['PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'DRAFT_YEAR', 'DRAFT_NUMBER', 'draft_value_ratio']
            ]
            for idx, player in top_steals.iterrows():
                print(f"   {player['PLAYER_FIRST_NAME']} {player['PLAYER_LAST_NAME']} "
                      f"(#{int(player['DRAFT_NUMBER'])}, {player['DRAFT_YEAR']:.0f}): ROI = {player['draft_value_ratio']:.1f}")
        
        # Busts: Early picks (1-10) with low ROI
        busts = drafted_players[(drafted_players['DRAFT_NUMBER'] <= 10) & 
                               (drafted_players['draft_value_ratio'] <= drafted_players['draft_value_ratio'].quantile(0.2))]
        
        print(f"\nDraft Busts (picked 1-10 with bottom 20% ROI): {len(busts)} players")
        if len(busts) > 0:
            worst_busts = busts.nsmallest(5, 'draft_value_ratio')[
                ['PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'DRAFT_YEAR', 'DRAFT_NUMBER', 'draft_value_ratio']
            ]
            for idx, player in worst_busts.iterrows():
                print(f"   {player['PLAYER_FIRST_NAME']} {player['PLAYER_LAST_NAME']} "
                      f"(#{int(player['DRAFT_NUMBER'])}, {player['DRAFT_YEAR']:.0f}): ROI = {player['draft_value_ratio']:.1f}")

def create_value_visualizations(df_metrics, save_plots=True):
    """
    Create visualizations for value metrics analysis
    
    Args:
        df_metrics (pd.DataFrame): DataFrame with calculated value metrics
        save_plots (bool): Whether to save plots to files
    """
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create a figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('NBA Draft ROI Analysis', fontsize=16, fontweight='bold')
    
    # 1. Value Score Distribution
    axes[0, 0].hist(df_metrics['value_score'], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0, 0].set_title('Distribution of Value Scores')
    axes[0, 0].set_xlabel('Value Score')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Draft Value Ratio vs Draft Position
    drafted_players = df_metrics[df_metrics['draft_value_ratio'].notna()]
    if len(drafted_players) > 0:
        axes[0, 1].scatter(drafted_players['DRAFT_NUMBER'], drafted_players['draft_value_ratio'], 
                          alpha=0.6, color='coral')
        axes[0, 1].set_title('Draft ROI vs Draft Position')
        axes[0, 1].set_xlabel('Draft Number')
        axes[0, 1].set_ylabel('Draft Value Ratio (ROI)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Add trend line
        z = np.polyfit(drafted_players['DRAFT_NUMBER'], drafted_players['draft_value_ratio'], 1)
        p = np.poly1d(z)
        axes[0, 1].plot(drafted_players['DRAFT_NUMBER'], p(drafted_players['DRAFT_NUMBER']), 
                       "r--", alpha=0.8, linewidth=2)
    
    # 3. Career Length vs Value Score
    axes[1, 0].scatter(df_metrics['career_length'], df_metrics['value_score'], alpha=0.6, color='lightgreen')
    axes[1, 0].set_title('Career Length vs Value Score')
    axes[1, 0].set_xlabel('Career Length (Years)')
    axes[1, 0].set_ylabel('Value Score')
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. ROI by Draft Position Bins
    if len(drafted_players) > 0:
        drafted_players['draft_bin'] = pd.cut(
            drafted_players['DRAFT_NUMBER'], 
            bins=[0, 5, 10, 20, 30, 60, float('inf')], 
            labels=['1-5', '6-10', '11-20', '21-30', '31-60', '60+']
        )
        
        roi_by_bin = drafted_players.groupby('draft_bin')['draft_value_ratio'].mean()
        roi_by_bin.plot(kind='bar', ax=axes[1, 1], color='gold', alpha=0.8)
        axes[1, 1].set_title('Average ROI by Draft Position')
        axes[1, 1].set_xlabel('Draft Position Range')
        axes[1, 1].set_ylabel('Average Draft Value Ratio')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_plots:
        plt.savefig('nba_roi_analysis.png', dpi=300, bbox_inches='tight')
        print("Visualizations saved as 'nba_roi_analysis.png'")
    
    plt.show()

def main():
    """
    Main function to execute value metrics calculation and analysis
    """
    
    try:
        # Load cleaned data
        print("Loading cleaned NBA data...")
        df = pd.read_csv("NBAStats_cleaned.csv")
        print(f"Loaded data with {len(df)} players")
        
        # Calculate value metrics
        df_with_metrics = calculate_value_metrics(df)
        
        # Analyze the metrics
        analyze_value_metrics(df_with_metrics)
        
        # Create visualizations
        print("\nCreating visualizations...")
        create_value_visualizations(df_with_metrics)
        
        # Save the enhanced dataset
        output_file = "NBAStats_with_value_metrics.csv"
        df_with_metrics.to_csv(output_file, index=False)
        print(f"\nData with value metrics saved to: {output_file}")
        
        return df_with_metrics
        
    except FileNotFoundError:
        print("Error: Could not find 'NBAStats_cleaned.csv'")
        print("Please make sure you've run the data_cleaning.py script first.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    df_with_metrics = main()
