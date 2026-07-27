# importamos las librerías correspondientes -1- pandas
import pandas as pd
df = pd.read_csv('/Users/macbookair/Desktop/PCA/entertainment_clean.csv')
print(df.head(20))

data = df.iloc[:, 1:]
print(data.head(5))
print(data.describe())
print(data.mean())

data_centrada = data - data.mean()
data_centrada.head()

from sklearn.decomposition import PCA
pca = PCA(n_components=2)
pca.fit(data_centrada)
print(pca.explained_variance_ratio_)

pca2 = PCA(n_components=2)
pca2.fit(data_centrada)
print(pca2.explained_variance_ratio_)
sum(pca2.explained_variance_ratio_)
print(pca2.components_)
print(data_centrada.columns)

data_transformada = pd.DataFrame(pca.transform(data_centrada), columns=['pc1', 'pc2'])
print(data_transformada.head(10))

# --- Visualización 1: scatterplot ---
import matplotlib.pyplot as plt
import seaborn as sns

sns.scatterplot(x='pc1', y='pc2', data=data_transformada)
plt.xlabel('PC1 - más libros y videojuegos')
plt.ylabel('PC2 - más programas de tv y videojuegos')
plt.title('Gráfico de dispersión de los datos transformados por PCA')
plt.show()

# --- Visualización 2: scree plot ---
componentes = range(1, len(pca2.explained_variance_ratio_) + 1)
plt.figure()
plt.bar(componentes, pca2.explained_variance_ratio_, color='orange')
plt.plot(componentes, pca2.explained_variance_ratio_.cumsum(), color='blue', marker='x')
plt.xlabel('Componentes Principales')
plt.ylabel('Varianza Explicada')
plt.title('Varianza Explicada por cada Componente Principal')
plt.xticks(componentes)
plt.show()

# --- Definimos biplot ---
import numpy as np

def biplot(scores, loadings, labels):
    xs = scores[:, 0]
    ys = scores[:, 1]
    plt.figure(figsize=(8, 6))
    plt.scatter(xs, ys, alpha=0.6, color='gray')
    for i, label in enumerate(labels):
        plt.arrow(0, 0, loadings[i, 0] * max(xs), loadings[i, 1] * max(ys),
                  color='black', head_width=0.05)
        plt.text(loadings[i, 0] * max(xs) * 1.15, loadings[i, 1] * max(ys) * 1.15,
                  label, color='black', fontsize=10)
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.title('Biplot de PCA')
    plt.axhline(0, color='grey', lw=1)
    plt.axvline(0, color='grey', lw=1)
    plt.show()

# --- Visualización 3: biplot ---
scores = pca2.transform(data_centrada)
loadings = pca2.components_.T
biplot(scores, loadings, data_centrada.columns)

# --- Visualización 4: heatmap de loadings ---
loadings_df = pd.DataFrame(pca2.components_.T,
                            columns=[f'PC{i+1}' for i in range(pca2.n_components_)],
                            index=data_centrada.columns)
plt.figure(figsize=(6, 4))
sns.heatmap(loadings_df, annot=True, cmap='Greys', center=0)
plt.title('Loadings de cada variable en los componentes')
plt.show()
# --- Visualización complementaria 5: Círculo de correlaciones
plt.figure(figsize=(6, 6))
circle = plt.Circle((0,0), 1, color = 'gray', fill = False, linestyle='--', linewidth=1)
plt.gca().add_patch(circle)
# Visualización de coordenadas de PC1 y PC2:
loadings_circle = pca2.components_.T
for i, var in enumerate(data_centrada.columns):
    x = loadings_circle[i, 0]
    y = loadings_circle[i, 1]
    plt.arrow(0, 0, x, y, color='black', head_width=0.05, length_includes_head=True)
    plt.text(x * 1.15, y * 1.15, var, color = 'black', fontsize=10, ha='center', va='center')
    plt.xlim(-1.2, 1.2)
    plt.ylim(-1.2, 1.2)
    plt.axhline(0, color='grey', lw=1)
    plt.axvline(0, color='grey', lw=1)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('Círculo de Correlaciones')
plt.grid()
plt.show()
# Visualización de contribución de variables coseno de los vectores de loadings
contrib_df = pd.DataFrame(
    pca2.components_.T ** 2,
    columns = [f'PC{i+1}' for i in range(pca2.n_components_)],
    index=data_centrada.columns
)
contrib_df.plot(kind='bar', figsize=(8, 5), color=
                ['steelblue', 'coral'], edgecolor= 'black')
plt.ylabel('Contribución relativa')
plt.title('Contribución individual por componente a los componentes principales')
plt.ylim(0,1)
plt.axhline(1/ len(data_centrada.columns), color='red', linestyle='--',
                        label=f'Umbral medio ({1/len(data_centrada.columns):.2f})')
plt.legend()
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
# Visualización 7. Calidad de representación de individupales (cos2)
scores = pca2.transform(data_centrada)
# distancia al origen del plano cartesiano de los dos primeros componentes principales
dist_plan = scores[:, 0]**2 + scores[:, 1]**2
# distancia al origen en el espacio original - datos centrados
dist_total = np.sum(data_centrada.values**2, axis=1)
# coseno al cuadrado = proporcion de la distancia total recuperada en el plano
cos2 = dist_plan / dist_total
plt.figure(figsize=(8,6))
scatter = plt.scatter(scores[:, 0], scores[:, 1],
                    c=cos2, cmap='viridis',
                    edgecolor='k', alpha=0.8,
                s=60)
cbar = plt.colorbar(scatter)
cbar.set_label('cos2 (Calidad de representación)')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('Calidad de representación de los individuos en el plano PCA')
plt.axhline(0, color='grey', lw=1)
plt.axvline(0, color='grey', lw=1)
plt.grid()
plt.show()
