import advanced_stress_predictor
import builtins

# Store original input function
original_input = builtins.input

# Define a list of inputs to simulate user input
simulated_inputs = [
    "30",  # Age
    "Male",  # Gender
    "7.5",  # Sleep hours
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
