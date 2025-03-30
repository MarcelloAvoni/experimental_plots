import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker  # Import for ScalarFormatter

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

# Filepaths for the old CSV files (position vs motor load)
old_filepaths = [
    r"c:\Users\marce\OneDrive\Desktop\Tesi\Codice\experimental_plots\data\1_phalanges_model_foot.csv",
    r"c:\Users\marce\OneDrive\Desktop\Tesi\Codice\experimental_plots\data\2_phalanges_model_foot.csv",
    r"c:\Users\marce\OneDrive\Desktop\Tesi\Codice\experimental_plots\data\3_phalanges_model_foot.csv"
]

# Filepaths for the new CSV files (mass vs load)
new_filepaths = [
    r"c:\Users\marce\OneDrive\Desktop\Tesi\Codice\experimental_plots\data\1_phalanges_model_hand.csv",
    r"c:\Users\marce\OneDrive\Desktop\Tesi\Codice\experimental_plots\data\2_phalanges_model_hand.csv",
    r"c:\Users\marce\OneDrive\Desktop\Tesi\Codice\experimental_plots\data\3_phalanges_model_hand.csv"
]

# Function to process and plot data
def process_and_plot(filepaths, x_label, y_label, title, output_filename, x_column, y_start_column):
    x_data = []
    means = []
    std_devs = []

    for filepath in filepaths:
        # Read the CSV file, skipping the first two rows
        df = pd.read_csv(filepath, delimiter=';', skiprows=2)
        
        # Replace commas with dots for numeric conversion
        df = df.replace(',', '.', regex=True)
        
        # Convert all values to numeric, coercing invalid entries (e.g., '-') to NaN
        df = df.apply(pd.to_numeric, errors='coerce')
        
        # Extract the x-axis column
        x = df[x_column]
        
        # Extract y-axis columns (all columns starting from y_start_column)
        y_data = df.iloc[:, y_start_column:]
        
        # Calculate the mean and standard deviation for y-axis data, ignoring NaN values
        mean = y_data.mean(axis=1)
        std_dev = y_data.std(axis=1)
        
        # Append the processed data to the lists
        x_data.append(x)
        means.append(mean)
        std_devs.append(std_dev)

    # Plot the data
    plt.figure(figsize=(10, 6))
    labels = ['1 Phalanx', '2 Phalanges', '3 Phalanges']
    colors = ['blue', 'green', 'red']

    for i in range(len(filepaths)):
        plt.errorbar(
            x_data[i], 
            means[i], 
            yerr=std_devs[i], 
            fmt='o-', 
            label=labels[i], 
            color=colors[i],
            elinewidth=2,  # Increase the thickness of the error bars
            capsize=5,     # Add caps to the error bars
            capthick=2     # Increase the thickness of the caps
        )

    # Add labels, title, and legend
    plt.xlabel(x_label, fontsize=font_size)
    plt.ylabel(y_label, fontsize=font_size)
    plt.title(title, fontsize=font_size)
    plt.legend(fontsize=font_size - 2)

    # Apply the ScalarFormatter to the y-axis
    ax = plt.gca()  # Get the current axis
    ax.yaxis.set_major_formatter(formatter)

    # Save the plot as a PDF in the saved_plots folder
    plt.savefig(output_filename, format='pdf')

    # Show the plot
    plt.show()

# Process and plot the old files (position vs motor load)
process_and_plot(
    old_filepaths,
    x_label='Position [mm]',
    y_label='Motor Load [%]',
    title='Motor Load vs Position for Different Prototypes',
    output_filename=r'c:\Users\marce\OneDrive\Desktop\Tesi\Codice\experimental_plots\saved_plots\motor_load_vs_position.pdf',
    x_column='position [mm]',
    y_start_column=1
)

# Process and plot the new files (mass vs load)
process_and_plot(
    new_filepaths,
    x_label='Mass [kg]',
    y_label='Load [%]',
    title='Load vs Mass for Different Prototypes',
    output_filename=r'c:\Users\marce\OneDrive\Desktop\Tesi\Codice\experimental_plots\saved_plots\load_vs_mass.pdf',
    x_column='mass [kg]',
    y_start_column=1
)