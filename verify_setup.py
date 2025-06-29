#!/usr/bin/env python3
"""
Simple verification script to check if NBA draft ROI analysis is working
"""

def check_files():
    """Check if all required files exist"""
    import os
    
    required_files = [
        'NBAStats.csv',
        'NBAStats_cleaned.csv', 
        'data_cleaning.py',
        'value_metrics.py'
    ]
    
    print("CHECKING FILES:")
    print("-" * 20)
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
    print()

def check_data():
    """Check if data is properly cleaned and ready for analysis"""
    try:
        import pandas as pd
        
        print("CHECKING DATA:")
        print("-" * 15)
        
        # Load cleaned data
        df = pd.read_csv('NBAStats_cleaned.csv')
        print(f"✓ Loaded {len(df)} players from cleaned data")
        
        # Check for career_length column (created by data_cleaning.py)
        if 'career_length' in df.columns:
            print("✓ career_length column exists")
            print(f"  Career length range: {df['career_length'].min()} to {df['career_length'].max()} years")
        else:
            print("✗ career_length column missing - run data_cleaning.py")
            return False
        
        # Check required columns for value metrics
        required_cols = ['PTS', 'REB', 'AST', 'DRAFT_NUMBER']
        for col in required_cols:
            if col in df.columns:
                print(f"✓ {col} column exists")
            else:
                print(f"✗ {col} column missing")
                return False
        
        print()
        return True
        
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return False

def run_quick_analysis():
    """Run a quick version of the value metrics analysis"""
    try:
        import pandas as pd
        import numpy as np
        
        print("RUNNING QUICK ANALYSIS:")
        print("-" * 25)
        
        df = pd.read_csv('NBAStats_cleaned.csv')
        
        # Calculate value score
        df['value_score'] = (df['PTS'] + df['REB'] + df['AST']) * df['career_length']
        print(f"✓ Value scores calculated")
        print(f"  Value score range: {df['value_score'].min():.1f} to {df['value_score'].max():.1f}")
        
        # Calculate ROI for drafted players
        drafted = df[df['DRAFT_NUMBER'].notna() & (df['DRAFT_NUMBER'] > 0)]
        print(f"✓ Found {len(drafted)} drafted players")
        
        if len(drafted) > 0:
            drafted['roi'] = drafted['value_score'] / drafted['DRAFT_NUMBER']
            print(f"✓ ROI calculated")
            print(f"  ROI range: {drafted['roi'].min():.1f} to {drafted['roi'].max():.1f}")
            
            # Show top 3 by value score
            print(f"\nTOP 3 BY VALUE SCORE:")
            top_players = df.nlargest(3, 'value_score')[['PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'value_score']]
            for _, player in top_players.iterrows():
                print(f"  {player['PLAYER_FIRST_NAME']} {player['PLAYER_LAST_NAME']}: {player['value_score']:.1f}")
            
            # Show top 3 by ROI
            print(f"\nTOP 3 BY ROI:")
            top_roi = drafted.nlargest(3, 'roi')[['PLAYER_FIRST_NAME', 'PLAYER_LAST_NAME', 'DRAFT_NUMBER', 'roi']]
            for _, player in top_roi.iterrows():
                print(f"  {player['PLAYER_FIRST_NAME']} {player['PLAYER_LAST_NAME']} (#{int(player['DRAFT_NUMBER'])}): {player['roi']:.1f}")
        
        print("\n✓ Quick analysis completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error in analysis: {e}")
        return False

def main():
    """Main verification function"""
    print("NBA DRAFT ROI ANALYSIS - VERIFICATION")
    print("=" * 40)
    print()
    
    # Check files
    check_files()
    
    # Check data
    data_ok = check_data()
    
    # Run quick analysis if data is ok
    if data_ok:
        analysis_ok = run_quick_analysis()
        
        print("\nVERIFICATION SUMMARY:")
        print("=" * 20)
        if analysis_ok:
            print("✓ Everything is working correctly!")
            print("✓ You can now run: python value_metrics.py")
            print("✓ This will generate detailed analysis and visualizations")
        else:
            print("✗ Analysis failed - check error messages above")
    else:
        print("\nVERIFICATION SUMMARY:")
        print("=" * 20)
        print("✗ Data issues found - run data_cleaning.py first")

if __name__ == "__main__":
    main()
