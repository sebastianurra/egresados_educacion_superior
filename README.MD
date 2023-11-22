## Paso 1: Redirigete a la carpeta del proyecto con CD.
 
## Paso 2: Cree el ambiente virtual.
python -m venv myenv

## Paso 3: Activar el entorno virtual.
myenv\Scripts\activate

### Observacion: si está en MacOS debe utilizar el siguiente comando:
source myenv/bin/activate

## Paso 4: Instalar las librerias del archivo requirements.txt.
pip install -r requirements.txt

## Paso 5: Luego debe descargar el csv más reciente de la siguiente URL y guardelo en la carpeta del repositorio.
https://datosabiertos.mineduc.cl/titulados-en-educacion-superior/

## Paso 6: Ejercutar la aplicación get_excel_resumen_es.py
python get_excel_resumen_es.py

