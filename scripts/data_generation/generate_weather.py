"""
Generate Weather Data
Creates synthetic historical weather data for agricultural districts
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker()
np.random.seed(44)
random.seed(44)

# Uganda Districts (Subset for efficiency or full list)
UGANDA_DISTRICTS = [
    "Kampala", "Wakiso", "Mukono", "Jinja", "Mbale", "Gulu", "Lira", "Mbarara",
    "Masaka", "Kasese", "Hoima", "Soroti", "Arua", "Kabale", "Tororo", "Iganga"
]

WEATHER_CONDITIONS = ['Sunny', 'Cloudy', 'Rainy', 'Stormy', 'Partly Cloudy']

def generate_weather(num_days=365, output_dir="../../data"):
    """
    Generate synthetic weather data
    
    Args:
        num_days: Number of days of history to generate
        output_dir: Output directory
    """
    print(f"Generating weather records for {len(UGANDA_DISTRICTS)} districts over {num_days} days...")
    
    weather_data = []
    
    start_date = datetime.now() - timedelta(days=num_days)
    
    count = 0
    for district in UGANDA_DISTRICTS:
        # Simulate local climate variations
        base_temp = random.uniform(20, 28)
        base_rain = random.uniform(0, 100)
        
        for i in range(num_days):
            current_date = start_date + timedelta(days=i)
            count += 1
            weather_id = f"WTH{str(count).zfill(8)}"
            
            # Seasonality (simplified)
            month = current_date.month
            is_rainy_season = month in [3, 4, 5, 9, 10, 11]
            
            # Temp
            day_variation = random.uniform(-2, 3)
            temp_avg = round(base_temp + day_variation, 2)
            temp_min = round(temp_avg - random.uniform(5, 8), 2)
            temp_max = round(temp_avg + random.uniform(5, 8), 2)
            
            # Rain
            if is_rainy_season:
                rainfall_mm = round(max(0, np.random.normal(15, 20)), 2) if random.random() > 0.4 else 0.0
            else:
                rainfall_mm = round(max(0, np.random.normal(5, 10)), 2) if random.random() > 0.7 else 0.0
            
            humidity = round(random.uniform(50, 90), 2)
            wind_speed = round(random.uniform(0, 20), 2)
            
            if rainfall_mm > 10:
                condition = 'Rainy' if rainfall_mm < 30 else 'Stormy'
            elif rainfall_mm > 0:
                condition = 'Cloudy' # Light rain
            else:
                condition = random.choice(['Sunny', 'Partly Cloudy', 'Cloudy'])
            
            record = {
                'weather_id': weather_id,
                'district': district,
                'weather_date': current_date.strftime('%Y-%m-%d'),
                'temperature_min': temp_min,
                'temperature_max': temp_max,
                'temperature_avg': temp_avg,
                'rainfall_mm': rainfall_mm,
                'humidity_pct': humidity,
                'wind_speed_kmh': wind_speed,
                'weather_condition': condition,
                'source': 'AgriMet Service',
                'loaded_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            weather_data.append(record)
            
    weather_df = pd.DataFrame(weather_data)
    
    # Save to CSV
    os.makedirs(output_dir, exist_ok=True)
    csv_path = f"{output_dir}/weather.csv"
    weather_df.to_csv(csv_path, index=False)
    print(f"  Saved to {csv_path} ({len(weather_df)} records)")
    
    return weather_df

if __name__ == "__main__":
    generate_weather()
