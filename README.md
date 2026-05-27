# 🤖 Aprendizaje No Supervisado
### Universidad Politécnica Metropolitana de Hidalgo (UPMH)
**Dr. Marcos Yamir Gomez** · Tercer Cuatrimestre

> Repositorio de proyectos, reportes y materiales del programa de Aprendizaje No Supervisado. El paradigma central: inferir estructura latente a partir de datos no etiquetados, sin función objetivo explícita, para descubrir representaciones comprimidas, agrupaciones o reglas de asociación ocultas.

---

## 👥 Integrantes

| Nombre | Rol |
|--------|-----|
| Jessica Melani Romero Lora | Estudiante |
| Victor Manuel Santos Martínez | Estudiante |

---

## 📁 Estructura del repositorio

```
aprendizaje-no-supervisado/
│
├── 📂 proyectos/
│   ├── 01_segmentacion_clientes/       # K-Means sobre datos de e-commerce
│   │   ├── notebook.ipynb
│   │   ├── data/
│   │   └── informe/
│   └── ...                             # Proyectos futuros
│
├── 📂 notas/
│   ├── metricas_distancia.md           # Euclidiana, Manhattan, Coseno, Mahalanobis, Jaccard
│   ├── mapa_conceptual_ANS.png         # Mapa visual del paradigma ANS
│   └── ...
│
├── 📂 recursos/
│   └── referencias.md
│
└── README.md
```

---

## ✅ Proyectos completados

### 01 · Segmentación de Clientes con K-Means
**Archivo:** `proyectos/01_segmentacion_clientes/`

Pipeline de segmentación sobre una base de datos sintética de e-commerce con **50 registros** y 3 variables comportamentales/demográficas.

**Variables de entrada:**
- Tiempo en App (hrs/semana)
- Compras Mensuales
- Edad

**Metodología:**
1. EDA con histogramas y matriz de correlación de Pearson
2. Preprocesamiento con `StandardScaler`
3. Selección de *k* mediante **Método del Codo** + **Coeficiente de Silhouette** → k = 3 (score = 0.598)
4. Aplicación de K-Means (`random_state=42`, `n_init=10`)

**Segmentos identificados:**

| Segmento | Edad aprox. | Compras | Tiempo en App | Categoría principal |
|----------|-------------|---------|---------------|---------------------|
| 🟦 Exploradores Digitales | ~20 años | Baja | Alta | Electrónica / Videojuegos |
| 🟧 Compradores Generacionales | ~30 años | Moderada | Moderado | Ropa / Hogar |
| 🟩 Compradores Intensivos | ~45 años | Alta | Baja | Hogar / Electrodomésticos |

**Stack:** `pandas` · `scikit-learn` · `matplotlib` · `seaborn`

---

## 📚 Temas cubiertos

### Paradigma central — Aprendizaje No Supervisado
El modelo infiere estructura latente a partir de datos **no etiquetados**, sin función objetivo explícita. Su objetivo es descubrir representaciones comprimidas, agrupaciones o reglas de asociación ocultas.

| Área | Algoritmos / Técnicas |
|------|-----------------------|
| **Clustering** | K-Means, DBSCAN, Agrupamiento jerárquico |
| **Reducción de dimensionalidad** | PCA, t-SNE, UMAP |
| **Reglas de asociación** | Apriori, FP-Growth, Market Basket |
| **Detección de anomalías** | Isolation Forest, LOF, Autoencoders |
| **Modelos generativos** | GMM (EM), VAE, GAN |
| **Embeddings** | Word2Vec, BERT, SimCLR |

### Métricas de distancia en ML

| Métrica | Tipo de dato ideal | Sensibilidad a escala | Uso típico |
|---------|-------------------|----------------------|------------|
| **Euclidiana (L²)** | Numérico continuo | Alta | k-NN, k-Means, PCA |
| **Manhattan (L¹)** | Numérico / ordinal | Alta | LASSO, DBSCAN, detección de fraude |
| **Coseno** | Vectores densos (texto, embeddings) | Nula | NLP, sistemas de recomendación |
| **Mahalanobis** | Numérico con correlaciones | Nula | Detección de anomalías multivariadas |
| **Jaccard** | Conjuntos binarios | Nula | Genómica, deduplicación de texto |

### Métricas de evaluación (sin etiquetas)
- **Índice de Silhouette** — separación relativa entre clusters (rango: −1 a +1)
- **Davies-Bouldin** — razón entre dispersión intra-cluster y separación inter-cluster
- **Calinski-Harabasz** — varianza entre grupos vs. varianza dentro de grupos
- **Índice de Rand ajustado** — cuando existe *ground truth* parcial

---

## 🛠️ Configuración del entorno

```bash
# Clonar el repositorio
git clone https://github.com/<usuario>/aprendizaje-no-supervisado.git
cd aprendizaje-no-supervisado

# Instalar dependencias
pip install -r requirements.txt
```

**`requirements.txt` recomendado:**
```
pandas
numpy
scikit-learn
matplotlib
seaborn
jupyter
umap-learn
```

---

## 🗓️ Proyectos futuros (planeados)

- [ ] **02 · Reducción de dimensionalidad** — PCA + t-SNE sobre datos de alta dimensión
- [ ] **03 · Detección de anomalías** — Isolation Forest aplicado a transacciones financieras
- [ ] **04 · Reglas de asociación** — Market Basket Analysis con Apriori / FP-Growth
- [ ] **05 · Modelos generativos** — GMM y comparación con K-Means
- [ ] **06 · Embeddings y transfer learning** — Representaciones semánticas con BERT

---

## 📖 Referencias

1. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer.
2. Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.). Springer. [https://hastie.su.domains/ElemStatLearn/](https://hastie.su.domains/ElemStatLearn/)
3. Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press.
4. Deisenroth, M. P., Faisal, A. A., & Ong, C. S. (2020). *Mathematics for Machine Learning*. Cambridge University Press. [https://mml-book.github.io/](https://mml-book.github.io/)
5. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/)
6. Beyer, K. et al. (1999). When is 'nearest neighbor' meaningful? *Proceedings of ICDT*, 217–235.

---

<p align="center">
  Elaborado por Jessica Melani Romero Lora & Victor Manuel Santos Martínez · UPMH · 2026
</p>
