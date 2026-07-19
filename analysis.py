import pandas as pd
import matplotlib.pyplot as plt
import ssl

# --- Fix Mac SSL certificate verification issues ---
ssl._create_default_https_context = ssl._create_unverified_context

print("1. Downloading OWID Energy Dataset...")
url_energy = "https://nyc3.digitaloceanspaces.com/owid-public/data/energy/owid-energy-data.csv"
df_energy = pd.read_csv(url_energy)

print("2. Downloading OWID CO2 & Emissions Dataset...")
url_co2 = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
df_co2 = pd.read_csv(url_co2)

# Standardize column name before merging
df_co2 = df_co2.rename(columns={'location': 'country'})

# --- Merge datasets on Country and Year ---
print("3. Merging datasets together...")
df_merged = pd.merge(df_energy, df_co2, on=['country', 'year'], how='inner')

# --- Filter to your target countries and timeframe ---
countries = [
    'United States', 'China', 'Germany', 
    'United Arab Emirates', 'Saudi Arabia', 'World'
]
df_filtered = df_merged[df_merged['country'].isin(countries)].copy()
df_filtered = df_filtered[df_filtered['year'] >= 2000]

# --- Define desired columns and filter only by what is found ---
desired_cols = [
    'country', 'year',
    'renewables_share_energy',
    'fossil_share_energy',
    'solar_share_energy',
    'wind_share_energy',
    'energy_per_capita',
    'primary_energy_consumption_per_capita__kwh',
    'co2_per_capita'
]

# Select only the columns that are actually present in the merged dataset
available_cols = [col for col in desired_cols if col in df_filtered.columns]
df_clean = df_filtered[available_cols].dropna(subset=['renewables_share_energy'])

# --- Save final output for Tableau ---
output_path = '/Users/ashraf/Desktop/Internships/Tableu Project/energy_clean.csv'
df_clean.to_csv(output_path, index=False)
print(f"\nSuccess! 'energy_clean.csv' generated with {df_clean.shape[0]} rows.")
print("Columns exported to CSV:", df_clean.columns.tolist())

# ==========================================================
# Sheet 1: Line Chart — Renewables Share Over Time
# ==========================================================
fig1, ax1 = plt.subplots(figsize=(10, 5))
for country in countries:
    data = df_clean[df_clean['country'] == country]
    ax1.plot(data['year'], data['renewables_share_energy'], linewidth=2, label=country)

ax1.set_title('Sheet 1: Renewable Energy Share Over Time (2000–2022)', fontsize=12, fontweight='bold')
ax1.set_xlabel('Year')
ax1.set_ylabel('Renewables Share (% of total energy)')
ax1.legend()
ax1.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/Users/ashraf/Desktop/Internships/Tableu Project/renewables_share_line.png', dpi=150)
plt.show()

# ==========================================================
# Sheet 2: Bar Chart — 2022 Renewable Share Snapshot
# ==========================================================
fig2, ax2 = plt.subplots(figsize=(9, 5))
df_2022 = df_clean[df_clean['year'] == 2022].sort_values(by='renewables_share_energy', ascending=False)

ax2.bar(df_2022['country'], df_2022['renewables_share_energy'], color='forestgreen', alpha=0.8)
ax2.set_title('Sheet 2: Renewable Share Across Countries (2022 Snapshot)', fontsize=12, fontweight='bold')
ax2.set_xlabel('Country')
ax2.set_ylabel('Renewables Share (% of total energy)')
ax2.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/Users/ashraf/Desktop/Internships/Tableu Project/renewables_2022_bar.png', dpi=150)
plt.show()

# ==========================================================
# Sheet 3: Scatter Plot — CO2 Per Capita vs. Renewable Share
# ==========================================================
fig3, ax3 = plt.subplots(figsize=(10, 6))
colors_map = {'United States':'blue', 'China':'red', 'Germany':'orange', 
              'United Arab Emirates':'teal', 'Saudi Arabia':'purple', 'World':'grey'}

for country in countries:
    data = df_clean[df_clean['country'] == country]
    ax3.scatter(data['renewables_share_energy'], data['co2_per_capita'], 
               color=colors_map[country], alpha=0.6, label=country, s=60)
    ax3.plot(data['renewables_share_energy'], data['co2_per_capita'], color=colors_map[country], alpha=0.3)

ax3.set_title('Sheet 3: CO₂ Per Capita vs. Renewable Share (2000–2022)', fontsize=12, fontweight='bold')
ax3.set_xlabel('Renewables Share (% of total energy)')
ax3.set_ylabel('CO₂ Per Capita (tonnes)')
ax3.legend()
ax3.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/Users/ashraf/Desktop/Internships/Tableu Project/co2_vs_renewables_scatter.png', dpi=150)
plt.show()
