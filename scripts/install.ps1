##
## Install and initialize the development environment
##

# Create a virtual environment, if not exists

$venv = '.venv'

If (-not (Test-Path -Path $venv)) {
    python -m venv $venv
}

# Activate the environment

& ./.venv/Scripts/Activate.ps1

# Install development time packages, if any

$packages = 'build', 'findpydeps', 'wheel', 'jupyterlab' # for prototyping

Foreach ($package in $packages) {
    pip install $package --upgrade
}

# Install requirements, if any

$files = 'requirements.txt', 'requirements-dev.txt'

Foreach ($file in $files) {
    If (Test-Path -Path $file) {
        pip install -r $file --upgrade
    }
}
