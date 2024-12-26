# Análisis y Diseño de algoritmos II - Proyecto II

## Integrantes

- Víctor Hernandez - 2259520
- Nicolas Rojas - 2259460
- Esteban Revelo  - 2067507


# Configuración del Proyecto

Para ejecutar correctamente este proyecto, sigue estos pasos después de clonar el repositorio.

## 1. Crear un Entorno Virtual

Para evitar conflictos con dependencias globales, es necesario trabajar dentro de un entorno virtual.

1. Crea el entorno virtual:


python -m venv env


2. Activa el entorno virtual:

    - En Windows:
    
    env\Scripts\activate
    

    - En Mac/Linux:
    
    source env/bin/activate
    `
    

Si el entorno virtual se activó correctamente, verás algo como (env) al inicio de tu línea de comandos.

## 2. Instalar Dependencias

Una vez que el entorno virtual esté activo, instala las dependencias necesarias para el proyecto ejecutando:


pip install -r requirements.txt


Esto instalará todas las librerías necesarias que el proyecto utiliza.

## 3. Ejecutar el Proyecto

Con el entorno virtual activado y las dependencias instaladas, puedes ejecutar el proyecto con el siguiente comando:


python interfaz.py
