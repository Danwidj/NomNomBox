@echo off
echo Starting NomNomBox application...
docker-compose up -d

echo NomNomBox services started. To view logs use: docker-compose logs -f
echo To stop services use: stop-nomnombox.bat
pause 