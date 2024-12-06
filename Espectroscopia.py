from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import sys
import os  # Importar os para manejar el nombre del archivo

archivos_fits = '/Users/gaelgarciachavez/TiposEspectrales/c_t_18abr_0083o.ms.fits'

with fits.open(archivos_fits) as hdul:
    # Muestra la información del encabezado
    hdul.info()
    
    # Accede a la primera extensión de datos
    datos = hdul[0].data
    encabezado = hdul[0].header

print("Encabezado:")
print(encabezado)
print("Dimensiones de los datos:", datos.shape)

# Asegúrate de que los datos son de la forma (4, 1, 825)
if datos.ndim == 3 and datos.shape == (4, 1, 825):
    try:
        # Obtener el rango de longitudes de onda del encabezado
        crval1 = encabezado['CRVAL1']  # Valor inicial de longitud de onda
        try:
            cdelt1 = encabezado['CDELT1']
        except KeyError:
            cdelt1 = encabezado['CD1_1']  # Usar CD1_1 como alternativa
        
    except KeyError as e:
        print(f"Error: La clave {e} no se encuentra en el encabezado.")
        sys.exit()

    num_puntos = datos.shape[2]     # Número de puntos en el eje x (825 en este caso)

    # Generar el array de longitudes de onda en Angstroms
    longitudes_onda = crval1 + np.arange(num_puntos) * cdelt1

    plt.figure(figsize=(12, 8))
    
    for i in range(datos.shape[0]):  # Iterar sobre la primera dimensión (4)
        plt.plot(longitudes_onda, datos[i, 0], label=f'Serie {i+1}')  # Usamos longitudes de onda en el eje x
        
    # Obtener el nombre del archivo sin la ruta
    nombre_archivo = os.path.basename(archivos_fits)
    
    # Modificar el título del gráfico para incluir el nombre del archivo
    plt.title(f'Visualización de datos de {nombre_archivo}')
    plt.xlabel('Longitud de onda (Angstroms)')
    plt.ylabel('Intensidad Relativa')
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    print("Los datos no tienen la forma esperada.")
    
# Análisis estadístico
for i in range(datos.shape[0]):
    media = np.mean(datos[i, 0])
    desviacion_estandar = np.std(datos[i, 0])
    print(f'Serie {i+1} - Media: {media}, Desviación estándar: {desviacion_estandar}')