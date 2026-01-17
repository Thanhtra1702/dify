@echo off
echo Building custom Dify images...

echo.
echo [1/2] Building dify-api:1.11.2-custom...
docker build -f ..\api\Dockerfile -t dify-api:1.11.2-custom ..\api

echo.
echo [2/2] Building dify-web:1.11.2-custom...
docker build -f ..\web\Dockerfile -t dify-web:1.11.2-custom ..\web

echo.
echo Build complete. Images:
echo - dify-api:1.11.2-custom
echo - dify-web:1.11.2-custom
echo.
echo Next step: Update docker-compose.yaml to use these images
