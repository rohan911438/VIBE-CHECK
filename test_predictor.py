import advanced_stress_predictor
import builtins

# Store original input function
original_input = builtins.input

# Define a list of inputs to simulate user input
simulated_inputs = [
    "30",  # Age
    "Male",  # Gender
    "7.5",  # Sleep Duration
    "8",   # Quality of Sleep
    "1.0", # Physical Activity Level
    "70",  # Heart Rate
    "8000",# Daily Steps
    "120", # Systolic Blood Pressure
    "80",  # Diastolic Blood Pressure
    "Software Engineer", # Occupation (Ensured to be one of the unique occupations)
    "Normal Weight", # BMI Category (Ensured to be one of the unique BMI categories)
    "None",  # Sleep Disorder (Ensured to be one of the unique sleep disorders)
    "100", # Caffeine (mg)
    "2.0", # Social Hours
    "1.0", # Social Media Hours
    "1.5", # Outing Hours
    "7"    # Mood Rating
]

# Custom input function that returns values from the list
input_index = 0
def mock_input(prompt):
    global input_index
    print(prompt + simulated_inputs[input_index]) # Print prompt and the simulated input
    value = simulated_inputs[input_index]
    input_index += 1
    return value

# Replace the built-in input function
builtins.input = mock_input

# Run the main function of the predictor
print("\n--- Running Advanced Stress Predictor with Simulated Inputs ---")
advanced_stress_predictor.main()

# Restore the original input function
builtins.input = original_input