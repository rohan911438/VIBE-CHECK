import pandas as pd
import os

print(f"Current working directory: {os.getcwd()}")

# Load the datasets
try:
    sleep_df = pd.read_csv("Sleep_health_and_lifestyle_dataset.csv")
    mental_health_df = pd.read_csv("mental_health_analysis.csv")
    stress_df = pd.read_csv("Stress.csv")

    print("Sleep Health and Lifestyle Dataset:")
    print(sleep_df.head())
    print("\nMental Health Analysis Dataset:")
    print(mental_health_df.head())
    print("\nStress Dataset:")
    print(stress_df.head())

    print("\nSleep Health and Lifestyle Dataset Info:")
    sleep_df.info()
    print("\nMental Health Analysis Dataset Info:")
    mental_health_df.info()
    print("\nStress Dataset Info:")
    stress_df.info()

except FileNotFoundError as e:
    print(f"Error loading file: {e}. Please ensure the files are in the correct directory.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")