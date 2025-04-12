import os
import subprocess

def run_command(command):
    process = subprocess.Popen(command, shell=True)
    process.wait()

# Change to the project directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Run migrations
run_command('python manage.py makemigrations')
run_command('python manage.py migrate')

# Start the development server
run_command('python manage.py runserver') 