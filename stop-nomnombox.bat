@echo off
echo Stopping NomNomBox application and removing volumes...
docker-compose down -v

echo NomNomBox services stopped and volumes removed.
pause 