import os

file_to_delete = "C:\Users\ABHINAV KUMAR\Desktop\Projects\Stress prediction\stress_predictor.py"

try:
    os.remove(file_to_delete)
    print(f"Successfully deleted {file_to_delete}")
except OSError as e:
    print(f"Error deleting file {file_to_delete}: {e}")
