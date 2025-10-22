import pandas as pd
import numpy as np

def calculate_value_metrics(df):
    """
    Calculate value metrics for NBA players including value score and draft ROI
    
    Args:
        df (pd.DataFrame): Cleaned NBA stats dataframe
        
    Returns:
        pd.DataFrame: DataFrame with added value metrics
    """
    
    #  to avoid modifying the original dataframe
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

def main():
    """
    Main function to execute value metrics calculation
    """
    
    try:
        # Load cleaned data
        print("Loading cleaned NBA data...")
        df = pd.read_csv("NBAStats_cleaned.csv")
        print(f"Loaded data with {len(df)} players")
        
        # Calculate value metrics
        df_with_metrics = calculate_value_metrics(df)
        
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
