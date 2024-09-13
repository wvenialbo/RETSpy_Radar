##
## Build the project
##

# To build a single executable:
# .\build.ps1 -UseOneFile
#
# To build with separate files:
# .\build.ps1

param (
    [switch]$UseOneFile
)

# Activate the virtual environment

& ./.venv/Scripts/Activate.ps1

# Install/Update the `pyinstaller` tool package

pip install pyinstaller --upgrade

# Set the PyInstaller option based on user choice

if ($UseOneFile) {

    # Build the application as a single executable

    pyinstaller --onefile --name cbrpy cbrpy.py

} else {

    # Build the application with separate files

    pyinstaller --onedir --name cbrpy cbrpy.py

}
