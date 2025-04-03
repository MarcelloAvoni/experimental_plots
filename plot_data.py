import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker  # Import for ScalarFormatter
from scipy.stats import t

# Set global plot parameters
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['figure.autolayout'] = True  # Automatically adjust subplot parameters to give specified padding
plt.rcParams['axes.grid'] = True  # Enable grid for all plots
plt.rcParams['grid.alpha'] = 0.75  # Set grid transparency
plt.rcParams['grid.linestyle'] = '-'  # Set grid line style

font_size = 18  # Define the font size for labels

# Create a ScalarFormatter for scientific notation
formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((-1, 1))

# Filepaths for the old CSV files (foot data)
foot_filepaths = [
    r"c:/Users/marce/OneDrive/Desktop/Tesi/Codice/experimental_plots/data/1_phalanges_model_foot.csv",
    r"c:/Users/marce/OneDrive/Desktop/Tesi/Codice/experimental_plots/data/2_phalanges_model_foot.csv",
    r"c:/Users/marce/OneDrive/Desktop/Tesi/Codice/experimental_plots/data/3_phalanges_model_foot.csv"
]

# Filepaths for the new CSV files (hand data)
hand_filepaths = [
    r"c:/Users/marce/OneDrive/Desktop/Tesi/Codice/experimental_plots/data/1_phalanges_model_hand.csv",
    r"c:/Users/marce/OneDrive/Desktop/Tesi/Codice/experimental_plots/data/2_phalanges_model_hand.csv",
    r"c:/Users/marce/OneDrive/Desktop/Tesi/Codice/experimental_plots/data/3_phalanges_model_hand.csv"
]


# Function to process and plot data
def process_and_plot(filepaths, x_label, y_label, output_filename, x_column_index, y_columns_range):
    x_data = []
    means = []
    std_devs = []
    margins_of_error = []

    for filepath in filepaths:
        # Read the CSV file, skipping the first two rows
        df = pd.read_csv(filepath, delimiter=';', skiprows=2)
        
        # Replace commas with dots for numeric conversion
        df = df.replace(',', '.', regex=True)
        
        # Convert all values to numeric, coercing invalid entries (e.g., '-') to NaN
        df = df.apply(pd.to_numeric, errors='coerce')
        
        # Extract the x-axis column
        x = df.iloc[:, x_column_index]
        
        # Extract y-axis columns (specified range)
        y_data = df.iloc[:, y_columns_range]
        
        # Calculate the mean and standard deviation for y-axis data, ignoring NaN values
        mean = y_data.mean(axis=1)
        std_dev = y_data.std(axis=1,ddof=1)
        n = y_data.count(axis=1)  # Count non-NaN values for each row

        # Calculate the margin of error for the confidence interval (95% CI)
        confidence = 0.99
        t_score = t.ppf(1 - (1-confidence)/2,df=n-1)  # t-score for 95% CI
        margin_of_error = t_score * (std_dev / np.sqrt(n))
        
        # Append the processed data to the lists
        x_data.append(x)
        means.append(mean)
        std_devs.append(std_dev)
        margins_of_error.append(margin_of_error)

    # Plot the data
    plt.figure(figsize=(10, 6))
    labels = ['1 Phalanx', '2 Phalanges', '3 Phalanges']
    colors = ['red', 'green', 'blue']  # Standard colors

    for i in range(len(filepaths)):
        plt.errorbar(
            x_data[i], 
            means[i], 
            yerr=margin_of_error[i], 
            fmt='o-', 
            label=labels[i], 
            color=colors[i],
            elinewidth=2,  # Increase the thickness of the error bars
            capsize=5,     # Add caps to the error bars
            capthick=2     # Increase the thickness of the caps
        )

    # Add labels, legend, and grid
    plt.xlabel(x_label, fontsize=font_size)
    plt.ylabel(y_label, fontsize=font_size)
    plt.legend(fontsize=font_size - 2)

    # Apply the ScalarFormatter to the y-axis
    ax = plt.gca()  # Get the current axis
    ax.yaxis.set_major_formatter(formatter)

    # Save the plot as a PDF in the saved_plots folder
    plt.savefig(output_filename, format='pdf')

    # Show the plot
    plt.show()

# Process and plot the foot files (Applied Torque vs Motor Torque)
process_and_plot(
    foot_filepaths,
    x_label='Applied Torque [Nm]',
    y_label='Motor Torque [Nm]',
    output_filename=r'c:/Users/marce/OneDrive/Desktop/Tesi/Codice/experimental_plots/saved_plots/motor_torque_vs_applied_torque.pdf',
    x_column_index=1,  # Second column (index 1)
    y_columns_range=slice(7, 12)  # Columns 8 to 12 (0-based index)
)

# Process and plot the hand files (Mass vs Motor Torque)
process_and_plot(
    hand_filepaths,
    x_label='Hung Mass [kg]',
    y_label='Motor Torque [Nm]',
    output_filename=r'c:/Users/marce/OneDrive/Desktop/Tesi/Codice/experimental_plots/saved_plots/motor_torque_vs_mass.pdf',
    x_column_index=0,  # First column (index 0)
    y_columns_range=slice(6, 11)  # Columns 7 to 11 (0-based index)
)