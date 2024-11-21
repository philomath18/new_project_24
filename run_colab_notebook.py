import papermill as pm
import os

# Path to the notebook file on GitHub
notebook_path = "https://raw.githubusercontent.com/philomath18/new_project_24/refs/heads/main/crypto_portfolio_tracker.ipynb"
output_notebook = '/tmp/crypto_portfolio_updated.ipynb'
#output_notebook = 'https://github.com/philomath18/new_project_24/crypto_portfolio_updated.ipynb'

# Run the notebook using papermill
try:
    print(f"Running notebook: {notebook_path}")
    pm.execute_notebook(
        input_path=notebook_path,
        output_path=output_notebook,
        parameters={},  # Optional: Add notebook parameters here
    )
    print(f"Notebook executed successfully. Output saved as {output_notebook}")

    # Verify file creation
    if os.path.exists(output_notebook):
        print(f"Output notebook is available at: {output_notebook}")
    else:
        print("Failed to locate the output notebook.")
except Exception as e:
    print(f"Failed to execute the notebook: {e}")
