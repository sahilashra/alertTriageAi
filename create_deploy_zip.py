import zipfile
import os
from pathlib import Path

def create_deployment_zip():
    """Create deployment ZIP excluding problematic files"""

    zip_path = "alert-triage-ai-v2.zip"

    # Remove old zip if exists
    if os.path.exists(zip_path):
        os.remove(zip_path)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add application.py
        zipf.write('application.py', 'application.py')

        # Add Procfile
        zipf.write('Procfile', 'Procfile')

        # Add requirements.txt
        zipf.write('requirements.txt', 'requirements.txt')

        # Add backend directory (excluding __pycache__ and nul)
        for root, dirs, files in os.walk('backend'):
            # Skip __pycache__ and problematic directories
            dirs[:] = [d for d in dirs if d != '__pycache__']

            for file in files:
                # Skip problematic files
                if file in ['nul', '.pyc'] or file.endswith('.pyc'):
                    continue

                file_path = os.path.join(root, file)
                arcname = file_path
                try:
                    zipf.write(file_path, arcname)
                except Exception as e:
                    print(f"Skipping {file_path}: {e}")

        # Add data directory
        for root, dirs, files in os.walk('data'):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path)

        # Add frontend directory
        for root, dirs, files in os.walk('frontend'):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path)

        # Add .ebextensions if exists
        if os.path.exists('.ebextensions'):
            for root, dirs, files in os.walk('.ebextensions'):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, file_path)

    print(f"Created {zip_path}")
    print(f"Size: {os.path.getsize(zip_path) / 1024:.2f} KB")

if __name__ == "__main__":
    create_deployment_zip()
