import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


plt.style.use('default')
sns.set_palette("Set2")

COLORS = {
    'primary': '#C8102E',      # NBA red
    'secondary': '#1D428A',    # Royal blue (classic basketball)
    'accent': '#FDB927',       # Lakers gold (championship legacy)
    'success': '#00788C',      # Teal (modern basketball courts)
    'warning': '#FF6900',      # Phoenix orange (energy)
    'danger': '#CE1141',       # Houston red (intensity)
    'light': '#F7F7F7',        # Court white
    'medium': '#8B8680',       # Neutral gray
    'dark': '#0C2340',         # Deep navy (premi
    'gradient_start': '#C8102E', # Red to blue gradient
    'gradient_end': '#1D428A',
    'court_wood': '#D4A574',   # Basketball court wood
    'net_white': '#FFFFFF',    # Net color
    'chart_colors': ['#C8102E', '#1D428A', '#FDB927', '#00788C', '#FF6900', '#CE1141', '#6F263D', '#0E2240', '#753BBD', '#E56020']
}

def set_plot_style():
    """Set consistent styling for all plots with premium NBA aesthetics"""
    plt.rcParams.update({
        'figure.facecolor': 'white',
        'axes.facecolor': COLORS['light'],
        'axes.edgecolor': COLORS['dark'],
        'axes.linewidth': 1.5,
        'grid.color': COLORS['medium'],
        'grid.alpha': 0.25,
        'grid.linestyle': '--',
        'text.color': COLORS['dark'],
        'axes.labelcolor': COLORS['dark'],
        'xtick.color': COLORS['dark'],
        'ytick.color': COLORS['dark'],
        'font.family': 'sans-serif',
        'font.size': 11,
        'axes.titlesize': 18,
        'axes.titleweight': 'bold',
        'axes.labelsize': 13,
        'axes.labelweight': 'bold',
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 11,
        'legend.framealpha': 0.9,
        'legend.fancybox': True,
        'legend.shadow': True
    })

def create_scatter_plot(df):
    """
    Create scatter plot of Draft Number vs Value Score with professional styling
    
    Args:
        df (pd.DataFrame): DataFrame with value metrics
    """
    set_plot_style()
    
    # Filter drafted players only
    drafted_players = df[df['DRAFT_NUMBER'].notna() & (df['DRAFT_NUMBER'] > 0)]
    
    if len(drafted_players) == 0:
        print("No drafted players found for scatter plot.")
        return
    
    plt.figure(figsize=(12, 8))
    
    # Create scatter plot with color mapping
    scatter = plt.scatter(drafted_players['DRAFT_NUMBER'], drafted_players['value_score'], 
                         c=drafted_players['value_score'], 
                         cmap='RdYlBu_r',  # Premium red-yellow-blue colormap
                         alpha=0.8, 
                         s=85,
                         edgecolors=COLORS['dark'],
                         linewidths=0.8)
    
    plt.title('NBA Draft Position vs Player Value Score\nEvaluating Draft Efficiency & Hidden Gems', 
              fontsize=18, fontweight='bold', pad=20, color=COLORS['dark'])
    plt.xlabel('Draft Position', fontsize=14, fontweight='bold')
    plt.ylabel('Value Score', fontsize=14, fontweight='bold')
    
    # Add colorbar with premium styling
    cbar = plt.colorbar(scatter, shrink=0.8, pad=0.02)
    cbar.set_label('Value Score', fontweight='bold', fontsize=12, 
                   color=COLORS['dark'])
    cbar.ax.tick_params(labelsize=10, colors=COLORS['dark'])
    
    # Enhanced grid with court-inspired styling
    plt.grid(True, alpha=0.3, linestyle='--', linewidth=0.7, color=COLORS['medium'])
    
    # Add trend line with professional styling
    z = np.polyfit(drafted_players['DRAFT_NUMBER'], drafted_players['value_score'], 1)
    p = np.poly1d(z)
    plt.plot(drafted_players['DRAFT_NUMBER'], p(drafted_players['DRAFT_NUMBER']), 
             color=COLORS['primary'], 
             linestyle='-', 
             linewidth=3.5, 
             alpha=0.9,
             label=f'Trend Line (slope: {z[0]:.3f})')
    
    # Add subtle background styling
    ax = plt.gca()
    ax.set_facecolor(COLORS['light'])
    
    plt.legend(loc='upper right', frameon=True, fancybox=True, shadow=True,
               facecolor='white', edgecolor=COLORS['medium'])
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('draft_number_vs_value_score.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Enhanced scatter plot saved as 'draft_number_vs_value_score.png'")
    plt.close()

def create_top_roi_bar_chart(df):
    """
    Create bar chart of Top 10 ROI players with professional styling
    
    Args:
        df (pd.DataFrame): DataFrame with value metrics
    """
    set_plot_style()
    
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
    
    # Create gradient colors for bars using NBA color scheme
    colors = []
    for i in range(len(player_names)):
        if i < 3:  # Top 3 get special colors
            colors.append(COLORS['chart_colors'][i])
        else:
            # Create gradient for remaining bars
            alpha = 1 - (i - 3) * 0.1
            colors.append(COLORS['primary'] + f"{int(alpha * 255):02x}")
    
    # Create bar chart with premium NBA styling
    bars = plt.bar(range(len(player_names)), top_10_roi['draft_value_ratio'], 
                   color=COLORS['chart_colors'][:len(player_names)], 
                   alpha=0.85,
                   edgecolor=COLORS['dark'],
                   linewidth=1.2)
    
    plt.title('Top 10 Players by Draft ROI\nHighest Value Relative to Draft Position', 
              fontsize=18, fontweight='bold', pad=20, color=COLORS['dark'])
    plt.xlabel('Players', fontsize=14, fontweight='bold')
    plt.ylabel('Draft ROI (Value Score / Draft Position)', fontsize=14, fontweight='bold')
    plt.xticks(range(len(player_names)), player_names, rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y', linestyle='--', color=COLORS['medium'])
    
    # Set background
    ax = plt.gca()
    ax.set_facecolor(COLORS['light'])
    
    # Add value labels on top of bars with enhanced styling
    for i, (bar, roi_value) in enumerate(zip(bars, top_10_roi['draft_value_ratio'])):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + roi_value*0.01,
                f'{roi_value:.2f}', ha='center', va='bottom', fontsize=11, 
                fontweight='bold', color=COLORS['dark'])
    
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('top_10_roi_players.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Enhanced bar chart saved as 'top_10_roi_players.png'")
    plt.close()

def create_avg_roi_by_round_line_plot(df):
    """
    Create line plot of Average ROI by Draft Round with professional styling
    
    Args:
        df (pd.DataFrame): DataFrame with value metrics
    """
    set_plot_style()
    
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
    
    # Create line plot with premium NBA styling
    plt.plot(avg_roi_by_round.index, avg_roi_by_round.values, 
             marker='o', 
             linewidth=4, 
             markersize=12, 
             color=COLORS['primary'],
             markerfacecolor=COLORS['accent'],
             markeredgecolor=COLORS['dark'],
             markeredgewidth=2.5,
             alpha=0.95)
    
    # Fill area under the curve for visual appeal with gradient
    plt.fill_between(avg_roi_by_round.index, avg_roi_by_round.values, 
                     alpha=0.25, color=COLORS['primary'])
    
    plt.title('Average ROI by Draft Round\nRound 1 vs Later Rounds Performance Analysis', 
              fontsize=18, fontweight='bold', pad=20, color=COLORS['dark'])
    plt.xlabel('Draft Round', fontsize=14, fontweight='bold')
    plt.ylabel('Average ROI (Value Score / Draft Position)', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--', color=COLORS['medium'])
    
    # Set background
    ax = plt.gca()
    ax.set_facecolor(COLORS['light'])
    
    # Add value labels on points with premium styling
    for round_num, roi_value in avg_roi_by_round.items():
        plt.annotate(f'{roi_value:.2f}', 
                    (round_num, roi_value), 
                    textcoords="offset points", 
                    xytext=(0,18), 
                    ha='center', 
                    fontsize=12,
                    fontweight='bold',
                    color=COLORS['dark'],
                    bbox=dict(boxstyle="round,pad=0.4", 
                             facecolor='white', 
                             edgecolor=COLORS['primary'],
                             alpha=0.9,
                             linewidth=2))
    
    # Set x-axis to show integer rounds
    plt.xticks(avg_roi_by_round.index)
    
    # Add a horizontal line at y=0 for reference
    plt.axhline(y=0, color=COLORS['secondary'], linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('avg_roi_by_draft_round.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Enhanced line plot saved as 'avg_roi_by_draft_round.png'")
    plt.close()

def create_all_visualizations(df):
    """
    Create all three requested visualizations with professional styling
    
    Args:
        df (pd.DataFrame): DataFrame with value metrics
    """
    
    print("� Creating premium NBA-inspired visualizations...")
    print("=" * 60)
    
    # Create all three plots
    create_scatter_plot(df)
    print()
    
    create_top_roi_bar_chart(df)
    print()
    
    create_avg_roi_by_round_line_plot(df)
    print()
    
    print("=" * 60)
    print("🏆 All premium NBA visualizations completed!")
    print("📊 Championship-quality charts created:")
    print("   • draft_number_vs_value_score.png (NBA-Styled Scatter Plot)")
    print("   • top_10_roi_players.png (Team Colors Bar Chart)") 
    print("   • avg_roi_by_draft_round.png (Court-Inspired Line Plot)")
    print("\n🎯 Premium NBA features:")
    print("   • Official NBA color scheme (Red/Blue/Gold)")
    print("   • Professional basketball court aesthetics")
    print("   • Enhanced typography and premium layout")
    print("   • Championship-quality styling and annotations")
    print("   • Ultra high-resolution output (300 DPI)")

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
