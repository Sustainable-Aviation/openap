import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-deep')

# Load the CSV file
file_path = 'EEA/Data/EEA2019/ICL_EEA2019.csv'
df = pd.read_csv(file_path)

# Filter data for each aircraft type
a319_data = df[df['aircraft_type_icao'] == 'A319']
a320_data = df[df['aircraft_type_icao'] == 'A320']
a321_data = df[df['aircraft_type_icao'] == 'A321']
b737_data = df[df['aircraft_type_icao'] == 'B737']
b738_data = df[df['aircraft_type_icao'] == 'B738']
b739_data = df[df['aircraft_type_icao'] == 'B739']
b752_data = df[df['aircraft_type_icao'] == 'B752']
a332_data = df[df['aircraft_type_icao'] == 'A332']
a333_data = df[df['aircraft_type_icao'] == 'A333']
b789_data = df[df['aircraft_type_icao'] == 'B789']
b788_data = df[df['aircraft_type_icao'] == 'B788']

# Convert distances from km to nautical miles
conversion_factor = 0.539957
a319_data['Distance_nmi'] = a319_data['total_distance_km'] * conversion_factor
a320_data['Distance_nmi'] = a320_data['total_distance_km'] * conversion_factor
a321_data['Distance_nmi'] = a321_data['total_distance_km'] * conversion_factor
b737_data['Distance_nmi'] = b737_data['total_distance_km'] * conversion_factor
b738_data['Distance_nmi'] = b738_data['total_distance_km'] * conversion_factor
b739_data['Distance_nmi'] = b739_data['total_distance_km'] * conversion_factor
b752_data['Distance_nmi'] = b752_data['total_distance_km'] * conversion_factor
a332_data['Distance_nmi'] = a332_data['total_distance_km'] * conversion_factor
a333_data['Distance_nmi'] = a333_data['total_distance_km'] * conversion_factor
b789_data['Distance_nmi'] = b789_data['total_distance_km'] * conversion_factor
b788_data['Distance_nmi'] = b788_data['total_distance_km'] * conversion_factor

# Convert fuel burnt from kg to tonnes (1 tonne = 1000 kg)
fuel_burnt_data_tonnes = a319_data['Fuel_burnt (CCD) EEA'] / 1000
fuel_burnt_data_a320_tonnes = a320_data['Fuel_burnt (CCD) EEA'] / 1000
fuel_burnt_data_a321_tonnes = a321_data['Fuel_burnt (CCD) EEA'] / 1000
fuel_burnt_data_b737_tonnes = b737_data['Fuel_burnt (CCD) EEA'] / 1000
fuel_burnt_data_b738_tonnes = b738_data['Fuel_burnt (CCD) EEA'] / 1000
fuel_burnt_data_b739_tonnes = b739_data['Fuel_burnt (CCD) EEA'] / 1000
fuel_burnt_data_b752_tonnes = b752_data['Fuel_burnt (CCD) EEA'] / 1000
fuel_burnt_data_a332_tonnes = a332_data['Fuel_burnt (CCD) EEA'] / 1000
fuel_burnt_data_a333_tonnes = a333_data['Fuel_burnt (CCD) EEA'] / 1000
fuel_burnt_data_b789_tonnes = b789_data['Fuel_burnt (CCD) EEA'] / 1000
fuel_burnt_data_b788_tonnes = b788_data['Fuel_burnt (CCD) EEA'] / 1000

# Define markers for each aircraft type
markers = {
    'A319': 'o',
    'A320': 's',
    'A321': '^',
    'B737': 'D',
    'B738': 'P',
    'B739': 'X',
    'B752': '*',
    'A332': 'H',
    'A333': 'v',
    'B789': '<',
    'B788': '>'
}

Plot_narrow_body = False
Plot_wide_body = True

# Plot Range vs Fuel burnt for all aircraft
fig1 = plt.figure()
ax1 = fig1.gca()

if Plot_narrow_body:
    plt.scatter(a319_data['Distance_nmi'], fuel_burnt_data_tonnes, color='C0', edgecolor='black', s=120, marker=markers['A319'], label='A319')
    plt.scatter(a320_data['Distance_nmi'], fuel_burnt_data_a320_tonnes, color='C1', edgecolor='black', s=120, marker=markers['A320'], label='A320')
    plt.scatter(a321_data['Distance_nmi'], fuel_burnt_data_a321_tonnes, color='C2', edgecolor='black', s=120, marker=markers['A321'], label='A321')
    plt.scatter(b737_data['Distance_nmi'], fuel_burnt_data_b737_tonnes, color='C3', edgecolor='black', s=120, marker=markers['B737'], label='B737')
    plt.scatter(b738_data['Distance_nmi'], fuel_burnt_data_b738_tonnes, color='C4', edgecolor='black', s=120, marker=markers['B738'], label='B738')
    plt.scatter(b739_data['Distance_nmi'], fuel_burnt_data_b739_tonnes, color='C5', edgecolor='black', s=120, marker=markers['B739'], label='B739')

if Plot_wide_body:
    plt.scatter(b752_data['Distance_nmi'], fuel_burnt_data_b752_tonnes, color='C6', edgecolor='black', s=120, marker=markers['B752'], label='B752')
    plt.scatter(a332_data['Distance_nmi'], fuel_burnt_data_a332_tonnes, color='C7', edgecolor='black', s=120, marker=markers['A332'], label='A332')
    plt.scatter(a333_data['Distance_nmi'], fuel_burnt_data_a333_tonnes, color='C8', edgecolor='black', s=120, marker=markers['A333'], label='A333')
    plt.scatter(b789_data['Distance_nmi'], fuel_burnt_data_b789_tonnes, color='C9', edgecolor='black', s=120, marker=markers['B789'], label='B789')
    plt.scatter(b788_data['Distance_nmi'], fuel_burnt_data_b788_tonnes, color='C10', edgecolor='black', s=120, marker=markers['B788'], label='B788')

#plt.title('Range vs Fuel Burnt for Various Aircraft')
plt.xlabel('Distance (nmi)', fontname="Times New Roman", fontsize=20)
plt.ylabel('Fuel Burnt (tonnes)', fontname="Times New Roman", fontsize=20)
plt.legend(loc='upper left', bbox_to_anchor=(0, 1), ncol=6, prop={'family': 'Times New Roman', 'size': 14})

# Grid and minor ticks
ax1.grid(which='major', color='black', linestyle='-', linewidth='0.05')
ax1.minorticks_on()
ax1.grid(which='minor', color='black', linestyle=':', linewidth='0.05')

for axis in ['top', 'bottom', 'left', 'right']:
    ax1.spines[axis].set_linewidth(1.5)

#plt.legend(loc='upper left', prop={'family': 'Times New Roman', 'size': 14})

plt.xticks(fontname="Times New Roman", fontsize=16, rotation=45)
plt.yticks(fontname="Times New Roman", fontsize=16)


plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

F = plt.gcf()
Size = F.get_size_inches()
F.set_size_inches(Size[0]*1.7, Size[1]*1.5, forward=True)

plt.xlim([0, 7000])
plt.ylim([0, 80])

plt.tight_layout()
plt.savefig('Output/EEA/EEA_ICL_Wide_body.png',dpi=300)

plt.show()
