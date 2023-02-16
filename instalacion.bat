@echo off
echo ANTES DE CONTINUAR, asegurate de tener python instalado, de ser así ignora la pagina "https://www.python.org/downloads/"
start "https://www.python.org/downloads/"
pause
echo Instalando OpenCV...
pip install opencv-python
pip install opencv-contrib-python

echo Instalando imutils...
pip install imutils

echo Instalando Cmake
pip install CMake

echo Instalando face-recognition...
pip install face-recognition

echo Instalación terminada.
pause