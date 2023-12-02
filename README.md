# BigData-Spotify 
## Comandos 
Usar ```pip install -r requirements.txt``` para instalar los paquetes necesarios 
Usar ```pip freeze > requirements.txt``` para capturar los paquetes necesarios 

## Estructura 
├── functions           #Utilidades auxiliares de código 
│   ├── Analisis.py     #Análisis y graficación de datos 
│   ├── Letras.py       #Codigo Legacy a desguazar 
│   ├── Lyrics.py       #Obtención de letras de canciones 
│   ├── Promedio.py     #Codigo Legacy a desguazar y calculos 
│   ├── Spotify.py      #SpotifyAPI 
├── routes              #Para la gestión de rutas 
│   ├── templates       #Archivos.html 
│   ├── routes.py       #Magia de las rutas 
├── static              #Para las imagenes 
├── .env                #Para las variables de entorno 
├── app.py              #Punto principal de la app 
├── forms.py            #Formularios 
├── requirements.txt    #Descripción de paquetes necesarios 