##
## Build the package for deployment
##

# Activate the environment

& ./.venv/Scripts/Activate.ps1

# Build the package

python -m build -n # --wheel
