import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def create_scatter_plot(df):
    """
    Create scatter plot of Draft Number vs Value Score
    
    Args:
        df (pd.DataFrame): DataFrame with value metrics
    """
    
    # Filter drafted players only
    drafted_players = df[df['DRAFT_NUMBER'].notna() & (df['DRAFT_NUMBER'] > 0)]
    
    if len(drafted_players) == 0:
        print("No drafted players found for scatter plot.")
        return
    
    plt.figure(figsize=(12, 8))
    
    # Create scatter plot
    plt.scatter(drafted_players['DRAFT_NUMBER'], drafted_players['value_score'], 
                alpha=0.6, color='blue', s=50)
    
    plt.title('Draft Number vs Value Score', fontsize=16, fontweight='bold')
    plt.xlabel('Draft Number (Position)', fontsize=12)
    plt.ylabel('Value Score', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Add trend line
    z = np.polyfit(drafted_players['DRAFT_NUMBER'], drafted_players['value_score'], 1)
    p = np.poly1d(z)
    plt.plot(drafted_players['DRAFT_NUMBER'], p(drafted_players['DRAFT_NUMBER']), 
             "r--", alpha=0.8, linewidth=2, label='Trend Line')
    
    plt.legend()
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('draft_number_vs_value_score.png', dpi=300, bbox_inches='tight')
    print("✓ Scatter plot saved as 'draft_number_vs_value_score.png'")
    
    plt.show()

def create_top_roi_bar_chart(df):
    """
    Create bar chart of Top 10 ROI players
    
    Args:
        df (pd.DataFrame): DataFrame with value metrics
    """
    
    # Filter drafted players with valid ROI
    drafted_players = df[df['draft_value_ratio'].notna()]
    
    if len(drafted_players) == 0:
        print("No players with valid ROI found for bar chart.")
        return
    
    # Get top 10 ROI players
    top_10_roi = drafted_players.nlargest(10, 'draft_value_ratio')
    
    plt.figure(figsize=(14, 8))
    
    # Create player names for x-axis
    player_names = [f"{row['PLAYER_FIRST_NAME']} {row['PLAYER_LAST_NAME']}" 
                   for _, row in top_10_roi.iterrows()]
    
    # Create bar chart
    bars = plt.bar(range(len(player_names)), top_10_roi['draft_value_ratio'], 
                   color='green', alpha=0.7)
    
    plt.title('Top 10 Players by Draft ROI', fontsize=16, fontweight='bold')
    plt.xlabel('Players', fontsize=12)
    plt.ylabel('Draft ROI (Value Score / Draft Number)', fontsize=12)
    plt.xticks(range(len(player_names)), player_names, rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on top of bars
    for i, (bar, roi_value) in enumerate(zip(bars, top_10_roi['draft_value_ratio'])):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + roi_value*0.01,
                f'{roi_value:.1f}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('top_10_roi_players.png', dpi=300, bbox_inches='tight')
    print("✓ Bar chart saved as 'top_10_roi_players.png'")
    
    plt.show()

def create_avg_roi_by_round_line_plot(df):
    """
    Create line plot of Average ROI by Draft Round
    
    Args:
        df (pd.DataFrame): DataFrame with value metrics
    """
    
    # Filter drafted players with valid ROI
    drafted_players = df[df['draft_value_ratio'].notna()]
    
    if len(drafted_players) == 0:
        print("No players with valid ROI found for line plot.")
        return
    
    # Calculate average ROI by draft round
    avg_roi_by_round = drafted_players.groupby('DRAFT_ROUND')['draft_value_ratio'].mean().sort_index()
    
    if len(avg_roi_by_round) == 0:
        print("No draft round data found for line plot.")
        return
    
    plt.figure(figsize=(12, 8))
    
    # Create line plot
    plt.plot(avg_roi_by_round.index, avg_roi_by_round.values, 
             marker='o', linewidth=2, markersize=8, color='red')
    
    plt.title('Average ROI by Draft Round', fontsize=16, fontweight='bold')
    plt.xlabel('Draft Round', fontsize=12)
    plt.ylabel('Average ROI (Value Score / Draft Number)', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Add value labels on points
    for round_num, roi_value in avg_roi_by_round.items():
        plt.annotate(f'{roi_value:.1f}', 
                    (round_num, roi_value), 
                    textcoords="offset points", 
                    xytext=(0,10), 
                    ha='center', fontsize=10)
    
    # Set x-axis to show integer rounds
    plt.xticks(avg_roi_by_round.index)
    
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('avg_roi_by_draft_round.png', dpi=300, bbox_inches='tight')
    print("✓ Line plot saved as 'avg_roi_by_draft_round.png'")
    
    plt.show()

def create_all_visualizations(df):
    """
    Create all three requested visualizations
    
    Args:
        df (pd.DataFrame): DataFrame with value metrics
    """
    
    print("Creating visualizations...")
    print("=" * 50)
    
    # Create all three plots
    create_scatter_plot(df)
    print()
    
    create_top_roi_bar_chart(df)
    print()
    
    create_avg_roi_by_round_line_plot(df)
    print()
    
    print("=" * 50)
    print("All visualizations completed!")
    print("Files created:")
    print("• draft_number_vs_value_score.png")
    print("• top_10_roi_players.png") 
    print("• avg_roi_by_draft_round.png")

def main():
    """
    Main function to create all visualizations
    """
    
    try:
        # Load data with value metrics
        print("Loading NBA data with value metrics...")
        df = pd.read_csv("NBAStats_with_value_metrics.csv")
        print(f"Loaded data with {len(df)} players")
        
        # Check if required columns exist
        required_columns = ['value_score', 'draft_value_ratio', 'DRAFT_NUMBER', 'DRAFT_ROUND']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Error: Missing columns {missing_columns}")
            print("Please run value_metrics.py first to generate the value metrics.")
            return
        
        drafted_count = len(df[df['draft_value_ratio'].notna()])
        print(f"Found {drafted_count} players with valid ROI data")
        print()
        
        # Create all visualizations
        create_all_visualizations(df)
        
    except FileNotFoundError:
        print("Error: Could not find 'NBAStats_with_value_metrics.csv'")
        print("Please run value_metrics.py first to generate the value metrics.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
