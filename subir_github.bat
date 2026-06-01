@echo off
echo Preparando la version v.1.2 para subir a GitHub...
git init
git add .
git commit -m "v.1.2"
git branch -M main
:: Intenta actualizar la URL remota si existe, si no, la agrega.
git remote set-url origin https://github.com/OsvaLogic/E-commerce.git 2>nul || git remote add origin https://github.com/OsvaLogic/E-commerce.git
git push -u origin main --force
echo ¡Proceso completado! Revisa tu repositorio en GitHub.
pause