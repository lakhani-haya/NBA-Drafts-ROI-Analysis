import pandas as pd
import numpy as np

def load_and_clean_data(file_path):
    """
    Load and clean NBA Stats data
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    
    # Read the CSV file
    print("Loading CSV file...")
    df = pd.read_csv(file_path)
    print(f"Original data shape: {df.shape}")
    
    # Display basic info about the dataset
    print("\nDataset Info:")
    print(df.info())
    
    # Convert DRAFT_NUMBER to numeric 
    print("\nCleaning DRAFT_NUMBER column...")
    print(f"DRAFT_NUMBER unique values before cleaning: {df['DRAFT_NUMBER'].unique()[:20]}")  # Show first 20 unique values
    
    # Convert DRAFT_NUMBER to numeric, coercing errors to NaN
    df['DRAFT_NUMBER'] = pd.to_numeric(df['DRAFT_NUMBER'], errors='coerce')
    
    print(f"Number of null values in DRAFT_NUMBER after conversion: {df['DRAFT_NUMBER'].isnull().sum()}")
    
    # Calculate career_length = TO_YEAR - FROM_YEAR
    print("\nCalculating career_length...")
    df['career_length'] = df['TO_YEAR'] - df['FROM_YEAR']
    
    # Display career length statistics
    print(f"Career length statistics:")
    print(df['career_length'].describe())
    
    # Handle missing values
    print("\nHandling missing values...")
    
    # Check for missing values in all columns
    missing_values = df.isnull().sum()
    print("Missing values per column:")
    print(missing_values[missing_values > 0])
    
    # Handle specific missing value cases
    
    # For DRAFT_YEAR, DRAFT_ROUND, DRAFT_NUMBER - these might be legitimate NaN for undrafted players
    undrafted_players = df[df['DRAFT_YEAR'].isnull()].shape[0]
    print(f"\nNumber of undrafted players (no DRAFT_YEAR): {undrafted_players}")
    
    # For HEIGHT and WEIGHT - convert to numeric if they're not already
    if df['HEIGHT'].dtype == 'object':
        # Convert height from format like "6-10" to inches
        df['HEIGHT_INCHES'] = df['HEIGHT'].apply(convert_height_to_inches)
    
    if df['WEIGHT'].dtype == 'object':
        df['WEIGHT'] = pd.to_numeric(df['WEIGHT'], errors='coerce')
    
    # Fill missing values for key statistics with 0 (assuming missing stats mean 0)
    stats_columns = ['PTS', 'REB', 'AST']
    for col in stats_columns:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    
    # Display final statistics
    print(f"\nFinal data shape: {df.shape}")
    print(f"Total missing values remaining: {df.isnull().sum().sum()}")
    
    return df

def convert_height_to_inches(height_str):
    """
    Convert height from format like "6-10" to total inches
    
    Args:
        height_str (str): Height in format "feet-inches"
        
    Returns:
        float: Height in inches, or NaN if conversion fails
    """
    if pd.isnull(height_str):
        return np.nan
    
    try:
        if '-' in str(height_str):
            feet, inches = height_str.split('-')
            return int(feet) * 12 + int(inches)
        else:
            # If no dash, assume it's already in inches or invalid format
            return pd.to_numeric(height_str, errors='coerce')
    except:
        return np.nan

def display_data_summary(df):
    """
    Display summary statistics and insights about the cleaned data
    
    Args:
        df (pd.DataFrame): Cleaned DataFrame
    """
    
    print("=" * 50)
    print("DATA SUMMARY AFTER CLEANING")
    print("=" * 50)
    
    # Basic statistics
    print(f"Total number of players: {df.shape[0]}")
    print(f"Total number of features: {df.shape[1]}")
    
    # Draft statistics
    drafted_players = df[df['DRAFT_YEAR'].notna()]
    print(f"\nDrafted players: {len(drafted_players)}")
    print(f"Undrafted players: {len(df) - len(drafted_players)}")
    
    if len(drafted_players) > 0:
        print(f"Draft years range: {drafted_players['DRAFT_YEAR'].min():.0f} - {drafted_players['DRAFT_YEAR'].max():.0f}")
        print(f"Average draft position: {drafted_players['DRAFT_NUMBER'].mean():.1f}")
    
    # Career length statistics
    print(f"\nCareer length statistics:")
    print(f"Average career length: {df['career_length'].mean():.1f} years")
    print(f"Longest career: {df['career_length'].max()} years")
    print(f"Shortest career: {df['career_length'].min()} years")
    
    # Performance statistics
    print(f"\nPerformance statistics (career averages):")
    print(f"Average points per game: {df['PTS'].mean():.1f}")
    print(f"Average rebounds per game: {df['REB'].mean():.1f}")
    print(f"Average assists per game: {df['AST'].mean():.1f}")

def main():
    """
    Main function to execute the data cleaning process
    """
    
    # File path
    file_path = "NBAStats.csv"
    
    try:
        # Load and clean the data
        cleaned_df = load_and_clean_data(file_path)
        
        # Display summary
        display_data_summary(cleaned_df)
        
        # Save cleaned data
        output_file = "NBAStats_cleaned.csv"
        cleaned_df.to_csv(output_file, index=False)
        print(f"\nCleaned data saved to: {output_file}")
        
        return cleaned_df
        
    except FileNotFoundError:
        print(f"Error: Could not find file {file_path}")
        print("Please make sure the CSV file is in the same directory as this script.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    cleaned_data = main()
