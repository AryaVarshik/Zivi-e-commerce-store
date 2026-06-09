import os
import sys
import subprocess

def run_command(command_args):
    print(f"\n>>> Running command: {' '.join(command_args)}")
    # Use shell=True for Windows compatibility
    result = subprocess.run(command_args, shell=True)
    if result.returncode != 0:
        print(f"\n[ERROR] Command failed with exit code {result.returncode}: {' '.join(command_args)}")
        sys.exit(result.returncode)

def main():
    print("==========================================================")
    print("                 Zivi Bootstrap Runner                   ")
    print("==========================================================")
    
    # 1. Locate python inside virtual environment
    if sys.platform == "win32":
        python_bin = os.path.join("venv", "Scripts", "python.exe")
    else:
        python_bin = os.path.join("venv", "bin", "python")
        
    if not os.path.exists(python_bin):
        print(f"[ERROR] Virtual environment python executable not found at: {python_bin}")
        print("Please ensure you set up the venv first.")
        sys.exit(1)
        
    print(f"Using virtual environment Python: {python_bin}")
    
    # 2. Make migrations for the store app
    run_command([python_bin, "manage.py", "makemigrations", "store"])
    
    # 3. Apply database migrations
    run_command([python_bin, "manage.py", "migrate"])
    
    # 4. Run seeding script (generates 240+ products, categories, reviews, and superuser)
    run_command([python_bin, "seed_data.py"])
    
    # 5. Start Development Server
    print("\n==========================================================")
    print("Starting Django development server at http://127.0.0.1:8000/")
    print("Default Superuser credentials: admin / admin123")
    print("==========================================================")
    run_command([python_bin, "manage.py", "runserver"])

if __name__ == "__main__":
    main()
