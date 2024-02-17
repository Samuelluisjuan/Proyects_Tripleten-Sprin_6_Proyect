import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy import stats as st
from IPython.display import display

# Lee los dataframes e imprime su informacion
df_game = pd.read_csv('games.csv')
display(df_game.head(20))
print('_____________________________________________________')
display(df_game.info())


#_____________________________________________________________________________________________________________________________________________

#### Paso 2. Prepara los datos
#Reemplaza los nombres de las columnas (ponlos en minúsculas).
df_game.columns = df_game.columns.str.lower()
display(df_game.head(10))

#Convierte los datos en los tipos necesarios.

# Limpiar la columna 'user_score'
df_game['user_score'] = pd.to_numeric(df_game['user_score'], errors='coerce')

# Convertir las columnas a tipo float
df_game['user_score'] = df_game['user_score'].astype(float)
display(df_game.info())

# Aqui estamos sacando el porsentaje de valores NAN en cada columna
100*df_game.isna().sum()/df_game.shape[0]

# Aqui estamos utilisando unique para obtener los valores únicos presentes en la columna 'user_score' 
df_game.user_score.unique()

# En esta parte estamos cambiando los valores 'tbd' a valores NAN
df_game['user_score'] = df_game['user_score'].replace('tbd', np.nan)
# Aqui estamos conbirtiendo de nuevo la columna 'user_score' a tipo de dato float
df_game['user_score'] = df_game['user_score'].astype(float)
df_game.user_score.unique()

# Visualisamos las colunmas del Dataframe
df_game.columns

# Con este codigo estamos sumando todas las ventas de cada pais, sumandolas y creando una nueva columna llamada 'sales_all'
df_game['sales_all'] = df_game['na_sales'] + df_game['eu_sales'] + df_game['jp_sales'] + df_game['other_sales']


#### Paso 3. Analiza los datos
# Con este codigo estamos agrupando la columna 'year_of_release' y contando los videojuegos de la columna 'name'
count_games =  df_game.groupby('year_of_release')['name'].count()
display(count_games.head())

#_____________________________________________________________________________________________________________________________________________
# Paso 3. Analiza los datos
# Crear el gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(count_games.index, count_games.values, color='skyblue')

plt.xlabel('Año de Lanzamiento')
plt.ylabel('Cantidad de Juegos Lanzados')
plt.title('Cantidad de Juegos Lanzados por Año')

plt.xlim(1980, 2015)

plt.xticks(range(1980, 2016, 5))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Con  este codigo estamos creando una tabla dinamica 
sales_by_console = df_game.pivot_table(index='platform', values='sales_all', aggfunc='sum')
display(sales_by_console.sort_values(by='sales_all', ascending=False).head())

# Con estos codigos estamos creando un nuevo dataframe llamado platform_distribution y estamos agrupandole las columnas 'year_of_release' y 'platform' junto con su suma total de ventas
platform_list = ('PS2', 'X360', 'PS3', 'Wii', 'DS')
games = df_game[df_game['platform'].isin(platform_list)]

platform_distribution = games.groupby(['year_of_release', 'platform'])['sales_all'].sum().reset_index()
platform_distribution.head()

sns.set(style="whitegrid")
# Crear el gráfico de líneas
plt.figure(figsize=(10, 6))
sns.lineplot(data=platform_distribution, hue='platform', x='year_of_release', y='sales_all')

# Configurar los ejes y etiquetas
plt.xlabel('Año de Lanzamiento', fontsize=12)
plt.ylabel('Ventas Totales', fontsize=12)
plt.title('Ventas Totales por Plataforma y Año', fontsize=14)

# Ajustar la leyenda
plt.legend(title='Plataforma', loc='upper left')

# Mostrar la gráfica
plt.tight_layout()
plt.show()