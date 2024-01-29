# Egresados de Educación Superior Chile

Este código procesa la información y obtiene un reporte en pdf de los egresados  de educación superior de universidades Chilenas, la información se descarga de forma automática en la siguiente dirección web: https://datosabiertos.mineduc.cl/titulados-en-educacion-superior/. Se solicitará ingresar el año por pantalla (ejemplo:2012)

Este código se realizó con la versión de python 3.10.12


# Pasos para ejecutar el código

## Paso:1 Redirigete a la carpeta del proyecto desde la terminal
 
## Paso 2: Cree el ambiente virtual
###     En MacOS y Linux:
    python3 -m venv myenv
###     En Windows:
    python -m venv myenv

## Paso 3: Active el ambiente virtual
###     En MacOS y Linux:
    source myenv/bin/activate
###     En Windows:
    myenv\Scripts\activate

## Paso 4: Instalar las librerias del archivo requirements.txt
###     En MacOS y Linux:
    pip3 install -r requirements.txt
###     En Windows:
    pip install -r requirements.txt