import papermill as pm
import os

# Path to the notebook file on GitHub
notebook_path = "https://github.com/philomath18/new_project_24/blob/main/crypto_portfolio_tracker.ipynb"  # Update with your GitHub notebook path
#output_notebook = "https://github.com/philomath18/new_project_24/crpyto_tracker_output.ipynb"  # Name for the executed notebook output
output_notebook = '/tmp/crypto_portfolio_updated.ipynb'
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
