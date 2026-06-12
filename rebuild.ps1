# Clean old builds
Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
Remove-Item lambda_package.zip -ErrorAction SilentlyContinue

# Create build folder
New-Item -ItemType Directory -Path build | Out-Null

# Copy source code
Copy-Item -Recurse -Path src -Destination build/src

# Install dependencies into build folder
pip install requests python-dotenv -t build

# Remove cache files
Get-ChildItem -Path build -Include "__pycache__" -Recurse -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
Get-ChildItem -Path build -Include "*.pyc" -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force

# Create deployment zip
Compress-Archive -Path build\* -DestinationPath lambda_package.zip -Force

# Show final zip size
$zip = Get-Item lambda_package.zip
Write-Host ""
Write-Host "ZIP SIZE:" ([math]::Round($zip.Length / 1MB, 2)) "MB"
Write-Host ""

Write-Host "✅ Build complete: lambda_package.zip"