# Development time packages:
# pip install -U build
# pip install -U findpydeps
# pip install -U jupyterlab # for prototyping
# pip install -U wheel

& ./.venv/Scripts/Activate.ps1

pip freeze > installed.txt

findpydeps -l -i retspy_smn > required.txt

# Read the content of required.txt and installed.txt into arrays
$requirements = Get-Content -Path 'required.txt'
$installed = Get-Content -Path 'installed.txt'

# Replace underscores with dashes in required.txt
$requirements = $requirements -replace '_', '-'

# Replace cv2 with opencv-* in required.txt
$requirements = $requirements -replace 'cv2', 'opencv-python-headless'
$requirements = $requirements -replace 'sklearn', 'scikit-learn'

# Create two empty arrays for the output
$requirementsProd = @()
$requirementsDev = @()

# Loop through each line in installed.txt
foreach ($line in $installed) {
    $packageName = $line.Split('==')[0] # Extract the package name

    # Check if the package name is in required.txt
    if ($requirements -contains $packageName) {
        $requirementsProd += $line  # Add to requirements.txt
    } else {
        $requirementsDev += $line  # Add to requirements-dev.txt
    }
}

# Write the results to separate text files
$requirementsProd | Set-Content -Path 'requirements.txt'
$requirementsDev | Set-Content -Path 'requirements-dev.txt'

# Replace '==' with '>=' for forward compatibility
(Get-Content 'requirements.txt').Replace('==', '>=') | Set-Content 'requirements.txt'
(Get-Content 'requirements-dev.txt').Replace('==', '>=') | Set-Content 'requirements-dev.txt'

# Clean up
$files = 'required.txt', 'installed.txt', 'requirements-dev.txt'

Foreach ($file in $files) {
    If (Test-Path $file) {
        Remove-Item $file #-verbose | Add-Content C:\mylog.txt
    }
    else {
        Write-Host "$file not found"
    }
}
