##
## Generate model schema files
##

# Activate the environment

& ./.venv/Scripts/Activate.ps1

# Install/Update the `datamodel-code-generator` tool package

pip install datamodel-code-generator --upgrade

# Generate schema files

$schema = ./schema
$models = ./models

datamodel-codegen  --input $schema --output $models --field-constraints --input-file-type jsonschema --target-python-version 3.12 --output-model-type pydantic_v2.BaseModel
