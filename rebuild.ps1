# Clean old builds
Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
Remove-Item lambda_package.zip -ErrorAction SilentlyContinue

# Create build folder
New-Item -ItemType Directory -Path build | Out-Null

# Copy source
Copy-Item -Recurse -Path src -Destination build/src

# Install dependencies into build
pip install requests python-dotenv boto3 -t build

# Remove cache
Get-ChildItem -Path build -Include "__pycache__" -Recurse -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
Get-ChildItem -Path build -Include "*.pyc" -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force

# Create zip
Compress-Archive -Path build\* -DestinationPath lambda_package.zip -Force

Write-Output "✅ Build complete: lambda_package.zip"