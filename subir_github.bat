@echo off
echo Preparando la actualizacion para subir a GitHub con fecha de ayer...
git init
git add .

set GIT_COMMITTER_DATE=yesterday
git commit --date="yesterday" -m "v.1.4: Arquitectura Headless, Celery y variables de entorno"

git branch -M main
:: Intenta actualizar la URL remota si existe, si no, la agrega.
git remote set-url origin https://github.com/OsvaLogic/E-commerce.git 2>nul || git remote add origin https://github.com/OsvaLogic/E-commerce.git
git tag v.1.4
git push origin main
git push origin v.1.4
echo ¡Proceso completado! Revisa tu repositorio en GitHub.
pause