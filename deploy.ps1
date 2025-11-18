Write-Host "🚀 Building and starting containers..."
docker compose down
docker compose up --build -d
Write-Host "✅ Deployment finished."