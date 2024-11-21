import papermill as pm
import os

# Path to the notebook file on GitHub
notebook_path = "path/to/your-notebook.ipynb"  # Update with your GitHub notebook path
output_notebook = "output.ipynb"  # Name for the executed notebook output

# Run the notebook using papermill
try:
    print(f"Running notebook: {notebook_path}")
    pm.execute_notebook(
        input_path=notebook_path,
        output_path=output_notebook,
        parameters={},  # Optional: Add notebook parameters here
    )
    print(f"Notebook executed successfully. Output saved as {output_notebook}")
except Exception as e:
    print(f"Failed to execute the notebook: {e}")
