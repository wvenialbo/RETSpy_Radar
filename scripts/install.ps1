# Create a virtual environment

python -m venv .venv

# Activate the environment

& ./.venv/Scripts/Activate.ps1

# Install development time packages

pip install -U build

pip install -U findpydeps

pip install -U jupyterlab # for prototyping

pip install -U wheel

# Install requirements if any

$files = 'requirements.txt', 'requirements-dev.txt'

Foreach ($file in $files) {
    If (Test-Path $file) {
        pip install -r $file
    }
}
