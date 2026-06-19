Set-Location $PSScriptRoot
Write-Host "Recetario Video Lab - servidor local en http://localhost:8000"
python -m http.server 8000
