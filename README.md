# UNAL_Consolidacion

## Sobre los formatos

### Formatos válidos

El código esta pensado para recibir los datos de carga en los siguientes formatos 

- **byprobe**: Almacena los datos de consolidación de una única muestra en un único archivo `txt`. 
- **simultaneous**: Almacena simultáneamente los datos de consolidación de diferentes muestras, previamente identificadas, en un mismo archivo `txt`.

Por defecto los 

### ¿Cómo nombrar los archivos adecuadamente?

Para los bancos de carga antiguos solo se recibiran formatos tipo `txt` con la siguiente nomenclatura:

`número de banco_responsable_proyecto_muestra_carga en kg.txt`

Si se esta cargando mas de un banco, utilice el símbolo **-** como separador. Algunos ejemplos se encuentran abajo

- `2_LAB_UNAL_S1M1_4.txt`
- `1_LAB_UNAL_S1M1_16-2_LAB_UNAL_S1M2_16-3_LAB_UNAL_S1M3_16-4_LAB_UNAL_S1M4_16.txt`

Siempre revisar que la primera y última fila no estén incompletas