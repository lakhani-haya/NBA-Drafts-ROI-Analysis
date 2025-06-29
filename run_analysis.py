import pandas as pd
import numpy as np

def main():
    """
    Run value metrics analysis without plotting (for troubleshooting)
    """
    
    try:
        print("Loading cleaned NBA data...")
        df = pd.read_csv("NBAStats_cleaned.csv")
        print(f"Loaded data with {len(df)} players")
        
        # Calculate value score = (PTS + REB + AST) * career_length
        print("\nCalculating value metrics...")
        df['value_score'] = (df['PTS'] + df['REB'] + df['AST']) * df['career_length']
        print(f"Value score range: {df['value_score'].min():.1f} to {df['value_score'].max():.1f}")
        
        # Calculate ROI for drafted players
        drafted_players = df[df['DRAFT_NUMBER'].notna() & (df['DRAFT_NUMBER'] > 0)]
        print(f"Found {len(drafted_players)} drafted players")
        
        df['draft_value_ratio'] = np.nan
        valid_draft_mask = (df['DRAFT_NUMBER'].notna()) & (df['DRAFT_NUMBER'] > 0)
        df.loc[valid_draft_mask, 'draft_value_ratio'] = (
            df.loc[valid_draft_mask, 'value_score'] / df.loc[valid_draft_mask, 'DRAFT_NUMBER']
        )
        
        print("ROI calculated successfully!")
        
        # Display top results
        print("\n" + "="*60)
        print("TOP 10 PLAYERS BY VALUE SCORE")
        print("="*60)
        
        top_players = df.nlargest(10, 'value_score')[
            ['PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'DRAFT_YEAR', 'DRAFT_NUMBER', 'value_score']
        ]
        
        for i, (_, player) in enumerate(top_players.iterrows(), 1):
            draft_info = f"#{int(player['DRAFT_NUMBER'])}" if pd.notna(player['DRAFT_NUMBER']) else "Undrafted"
            print(f"{i:2d}. {player['PLAYER_FIRST_NAME']} {player['PLAYER_LAST_NAME']}: {player['value_score']:.1f}")
            print(f"     Draft: {player['DRAFT_YEAR']:.0f} ({draft_info})")
        
        # Display top ROI
        print("\n" + "="*60)
        print("TOP 10 PLAYERS BY DRAFT ROI")
        print("="*60)
        
        drafted_only = df[df['draft_value_ratio'].notna()]
        top_roi = drafted_only.nlargest(10, 'draft_value_ratio')[
            ['PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'DRAFT_YEAR', 'DRAFT_NUMBER', 'draft_value_ratio']
        ]
        
        for i, (_, player) in enumerate(top_roi.iterrows(), 1):
            print(f"{i:2d}. {player['PLAYER_FIRST_NAME']} {player['PLAYER_LAST_NAME']}: ROI = {player['draft_value_ratio']:.1f}")
            print(f"     Draft: {player['DRAFT_YEAR']:.0f} (#{int(player['DRAFT_NUMBER'])})")
        
        # Save results
        output_file = "NBAStats_with_value_metrics.csv"
        df.to_csv(output_file, index=False)
        print(f"\n✓ Data with value metrics saved to: {output_file}")
        
        # Basic statistics
        print("\n" + "="*40)
        print("SUMMARY STATISTICS")
        print("="*40)
        print(f"Total players: {len(df)}")
        print(f"Drafted players: {len(drafted_only)}")
        print(f"Average value score: {df['value_score'].mean():.1f}")
        print(f"Average ROI (drafted players): {drafted_only['draft_value_ratio'].mean():.1f}")
        
        print("\n✓ Analysis completed successfully!")
        print("✓ Run the full value_metrics.py for detailed analysis and visualizations")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
