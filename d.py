# 1. Primero importamos la librería pandas (usualmente se le pone el alias 'pd')
import pandas as pd

# 2. Cargamos el archivo principal (el panel de datos)
# Nota: pd.read_csv lee archivos separados por comas. 
df_panel = pd.read_csv('global_imbalances_panel_filled.xlsx - panel.csv')

# 3. (Opcional) Cargamos el libro de códigos por si queremos consultar la descripción de las variables
df_codebook = pd.read_csv('global_imbalances_panel_filled.xlsx - codebook.csv')

# 4. Revisamos las primeras 5 filas para asegurarnos de que cargó correctamente (equivalente a head() en R)
print(df_panel.head())

# 5. Vemos un resumen de las columnas, valores no nulos y tipos de datos (equivalente a str() o glimpse() en R)
print(df_panel.info())
