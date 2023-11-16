import os

def delete_migration_files():
    project_path = "."
    excluded_paths = ["venv", ".venv"]

    for root, dirs, files in os.walk(project_path):
        if any(excluded_dir in root for excluded_dir in excluded_paths):
            continue

        for file in files:
            if file.endswith(".py") and 'migrations' in root and file != "__init__.py":
                file_path = os.path.join(root, file)
                print(f"Deleting {file_path}")
                os.remove(file_path)

if __name__ == "__main__":
    delete_migration_files()