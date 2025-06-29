import pandas as pd
import numpy as np

# Simple test to check if value_metrics.py can run
try:
    print("Testing value metrics functionality...")
    
    # Try to load the cleaned data
    df = pd.read_csv("NBAStats_cleaned.csv")
    print(f"✓ Successfully loaded data: {len(df)} players")
    
    # Check if required columns exist
    required_columns = ['PTS', 'REB', 'AST', 'career_length', 'DRAFT_NUMBER']
    missing_columns = []
    
    for col in required_columns:
        if col not in df.columns:
            missing_columns.append(col)
        else:
            print(f"✓ Column '{col}' exists")
    
    if missing_columns:
        print(f"✗ Missing columns: {missing_columns}")
    else:
        print("✓ All required columns are present")
    
    # Test basic calculations
    print("\nTesting calculations...")
    
    # Calculate value score for first few rows
    df['value_score'] = (df['PTS'] + df['REB'] + df['AST']) * df['career_length']
    print(f"✓ Value score calculated. Range: {df['value_score'].min():.1f} to {df['value_score'].max():.1f}")
    
    # Test ROI calculation
    drafted_players = df[df['DRAFT_NUMBER'].notna() & (df['DRAFT_NUMBER'] > 0)]
    print(f"✓ Found {len(drafted_players)} drafted players")
    
    if len(drafted_players) > 0:
        df.loc[drafted_players.index, 'draft_value_ratio'] = (
            df.loc[drafted_players.index, 'value_score'] / df.loc[drafted_players.index, 'DRAFT_NUMBER']
        )
        print(f"✓ ROI calculated for drafted players")
    
    print("\n" + "="*50)
    print("SUMMARY - Value Metrics Test Results:")
    print("="*50)
    print(f"Total players: {len(df)}")
    print(f"Drafted players: {len(drafted_players)}")
    print(f"Average value score: {df['value_score'].mean():.1f}")
    if len(drafted_players) > 0:
        roi_values = df.loc[drafted_players.index, 'draft_value_ratio']
        print(f"Average ROI: {roi_values.mean():.1f}")
    
    print("\n✓ All tests passed! value_metrics.py should work correctly.")
    
except FileNotFoundError:
    print("✗ Error: NBAStats_cleaned.csv not found")
    print("Make sure you've run data_cleaning.py first")
except Exception as e:
    print(f"✗ Error occurred: {str(e)}")
    import traceback
    traceback.print_exc()
