import pandas as pd
import matplotlib.pyplot as plt

# File paths
file_paths = [
    'combined_processed_A319.csv',
    'combined_processed_A320.csv',
    'combined_processed_A321.csv',
    'combined_processed_B737.csv',
    'combined_processed_B738.csv',
    'combined_processed_B739.csv'
]

# Aircraft labels corresponding to the files
labels = ['A319', 'A320', 'A321', 'B737', 'B738', 'B739']

# Plot the frequency distribution for each file
plt.figure(figsize=(12, 8))

for file_path, label in zip(file_paths, labels):
    df = pd.read_csv(file_path)
    true_airspeed_knots = df['true_airspeed_knots']
    plt.hist(true_airspeed_knots, bins=30, alpha=0.5, label=label, edgecolor='black')

plt.title('Frequency Distribution of True Airspeed Knots for Various Aircraft')
plt.xlabel('True Airspeed Knots')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.show()
