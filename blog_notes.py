import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy import stats as st
from IPython.display import display
from scipy.stats import ttest_ind

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

# 3.6 ¿Qué plataformas son líderes en ventas? ¿Cuáles crecen y cuáles se reducen? Elige varias plataformas potencialmente rentables.
# Crear el gráfico de dispersión con Seaborn
plt.figure(figsize=(10, 6))
sns.boxplot(data=games, x= 'sales_all', y = 'platform')

# Configurar el título del gráfico
plt.title('Fecuendias de las Plataformas')

# Configurar los ejes y etiquetas
plt.xlabel('Sales_all')
plt.ylabel('Platform')

# Mostrar la gráfica
plt.grid(True)
plt.tight_layout()
plt.show()

# Crear el gráfico de dispersión con Seaborn
plt.figure(figsize=(10, 6))
sns.boxplot(data=games, x= 'sales_all', y = 'platform', showfliers=False)

# Configurar el título del gráfico
plt.title('Fecuendias de las Plataformas')

# Configurar los ejes y etiquetas
plt.xlabel('Sales_all')
plt.ylabel('Platform')

# Mostrar la gráfica
plt.grid(True)
plt.tight_layout()
plt.show()


# 3.8 Mira cómo las reseñas de usuarios y profesionales afectan las ventas de una plataforma popular (tu elección). Crea un gráfico de dispersión y calcula la correlación entre las reseñas y las ventas. Saca conclusiones.

# Lo que hacemos en este codigo es crear un cuadro en el que mustre las columnas de critic_score	platform	year_of_release
popular_df = games[['critic_score', 'platform', 'year_of_release']].copy()
popular_df_ps2 = popular_df[popular_df['platform'] == 'PS2']
popular_df_ps2

# Crear el gráfico de dispersión con Seaborn
plt.figure(figsize=(10, 6))
sns.scatterplot(data=popular_df_ps2, x='year_of_release', y='critic_score', alpha=0.7)

# Configurar el título del gráfico
plt.title('Puntuación de Críticos vs Año de Lanzamiento para Juegos de PS2')

# Configurar los ejes y etiquetas
plt.xlabel('Año de Lanzamiento')
plt.ylabel('Puntuación de los Críticos')

# Mostrar la gráfica
plt.grid(True)
plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 6))
sns.lineplot(data=popular_df_ps2, x='year_of_release', y='critic_score')

# Configurar el título del gráfico
plt.title('Puntuación de los Críticos a lo largo de los Años (PS2)')

# Configurar los ejes y etiquetas
plt.xlabel('Año de Lanzamiento')
plt.ylabel('Puntuación de los Críticos')

# Mostrar la gráfica
plt.grid(True)
plt.tight_layout()
plt.show()

# 3.10 Echa un vistazo a la distribución general de los juegos por género. ¿Qué se puede decir de los géneros más rentables? ¿Puedes generalizar acerca de los géneros con ventas altas y bajas?.

# Creamos un Nuevo dataframe llamado genre_df que contenga las columnas 'name','genre','platform', 'year_of_release', 'sales_all'
genre_df = games[[ 'name','genre','platform', 'year_of_release', 'sales_all']].copy()
genre_df

# Imprime un grafico de barras
plt.figure(figsize=(12, 7))
sns.barplot(data=genre_df, x='genre', y='sales_all', hue='genre', palette='colorblind', legend=False)

##### Paso 4. Crea un perfil de usuario para cada región------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 4.1 Plataformas principales
#Creamos un df llamado marquet_sales y agrupamos las columnas platform y na_sales	jp_sale
market_sales =  games.groupby('platform').agg({'na_sales': 'sum',
                                               'jp_sales':'sum'}).reset_index()
market_sales

# Convertimos la columnas market en las ventas de na_sales y jp_sales, y en sales sus ventas numericas 
market_sales = pd.melt(market_sales, id_vars = ['platform'], value_vars = ['na_sales', 'jp_sales'], var_name = 'market', value_name = 'sales')
market_sales

# Creamos un grafico de barras con el df market_sales
plt.figure(figsize=(10, 7))
sns.barplot(market_sales, x='market', y='sales', hue='platform')

# 4.2 Géneros principales
#Creamos un df llamado genre_sales y agrupamos las columnas genre y na_sales, jp_sale
genre_sales =  games.groupby('genre').agg({'na_sales': 'sum',
                                               'jp_sales':'sum'}).reset_index()
genre_sales

# Convertimos la columnas market en las ventas de na_sales y jp_sales, y en sales sus ventas numericas 
genre_sales = pd.melt(genre_sales, id_vars = ['genre'], value_vars = ['na_sales', 'jp_sales'], var_name = 'market', value_name = 'sales')
genre_sales

# Creamos un grafico de barras del df genre_sales
plt.figure(figsize=(10, 7))
sns.barplot(data=genre_sales, x='market', y='sales', hue='genre')
plt.show()

# 4.3 Si las clasificaciones de ESRB afectan a las ventas en regiones individuales.
#Creamos un df llamado rating_sales y agrupamos las columnas rating y na_sales, jp_sale
rating_sales =  games.groupby('rating').agg({'na_sales': 'sum',
                                               'jp_sales':'sum'}).reset_index()
rating_sales

# Convertimos la columnas market en las ventas de na_sales y jp_sales, y en sales sus ventas numericas
rating_sales = pd.melt(rating_sales, id_vars = ['rating'], value_vars = ['na_sales', 'jp_sales'], var_name = 'market', value_name = 'sales')
rating_sales

# Creamos un grafico de barras con el df rating_sales
plt.figure(figsize=(10, 7))
sns.barplot(data=rating_sales, x='market', y='sales', hue='rating')
plt.show()

#### Paso 5. Prueba las siguientes hipótesis: --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Hipotesis 1:
# Este código devuelve todos los valores únicos que están presentes en la columna platform
df_game['platform'].unique()

# Estos fragmentos de código te permiten obtener las puntuaciones de los usuarios para los juegos en las plataformas Xbox One y PC
calificasion_XOne = df_game[df_game['platform'] == 'XOne']['user_score'].dropna()
calificasion_PC = df_game[df_game['platform'] == 'PC']['user_score'].dropna()

calificasion_XOne
calificasion_PC

# Este codigo realiza la prueva de hipotesis
alpha = 0.5
stat, p_value = ttest_ind(
    calificasion_XOne,
    calificasion_PC
)
print(f"""
      La calificasion promedio de profecionales para Xbox es: {calificasion_XOne.mean()}
      La calificasion promedio de profecionales para PC es: {calificasion_PC.mean()}
      
      t-statistic: {stat}
      p-value: {p_value}""")

if p_value < alpha:
    print('Rechasamos nuestra Hipotesis nula')
else:
    print('No Rechasamos nuestra Hipotesis nula')
    
# Hipotesis 2
# Este código devuelve todos los valores únicos que están presentes en la columna genre
df_game['genre'].unique()

# Estos fragmentos de código te permiten obtener las puntuaciones de los usuarios para los generos en las plataformas sport y action
genre_Sport = df_game[df_game['genre'] == 'Sports']['user_score'].dropna()
genre_Action = df_game[df_game['genre'] == 'Action']['user_score'].dropna()

# Este codigo realiza la prueva de hipotesis
alpha = 0.5
stat, p_value = ttest_ind(
    genre_Sport,
    genre_Action
)
print(f"""
      La calificasion promedio de profecionales para Deportes es: {genre_Sport.mean()}
      La calificasion promedio de profecionales para Accion es: {genre_Action.mean()}
      
      t-statistic: {stat}
      p-value: {p_value}""")

if p_value < alpha:
    print('Rechasamos nuestra Hipotesis nula')
else:
    print('No Rechasamos nuestra hipotesis nula')