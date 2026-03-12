# Análisis Dinámico de la Cuenta Corriente y Desequilibrios Globales

Esta herramienta analítica, desarrollada en **Python** utilizando **Streamlit**, permite la exploración interactiva, visualización y modelado econométrico de datos macroeconómicos para 32 economías clave (1990-2024). El objetivo es proveer una plataforma robusta para investigar los determinantes de la Cuenta Corriente, combinando econometría tradicional con técnicas de Machine Learning para respaldar decisiones y análisis en el ámbito de la banca central y la política económica.

---

## Capacidades Principales

* **Análisis Temporal y Transversal:** Evolución histórica y distribución global de indicadores macroeconómicos (PIB, Consumo, Inversión, Activos Externos Netos, etc.).
* **Agrupación Multivariable Inteligente:** Motor de visualización que clasifica automáticamente las variables seleccionadas por su escala (tasas, valores nominales, índices) para permitir comparaciones estructurales sin distorsión visual.
* **Relaciones Causal-Estadísticas (OLS & Diferencias):** Visualización bivariada con regresiones lineales.
* **Machine Learning (Feature Importance):** Integración de un modelo *Random Forest Regressor* entrenado en tiempo real para rankear el poder predictivo de las variables sobre la Cuenta Corriente, incorporando filtros anti *data-leakage*.
* **Diagnóstico de Multicolinealidad:** Generación dinámica de matrices de correlación de Pearson para la validación previa de modelos econométricos.

---

## Arquitectura del Proyecto

El proyecto sigue una estructura centralizada diseñada para despliegues rápidos en la nube (Streamlit Cloud):

```text
├── d.py                                 # Interfaz web principal, lógica analítica y modelos ML
├── global_imbalances_panel_filled.xlsx  # Dataset en panel y codebook (diccionario de variables)
├── requirements.txt                     # Dependencias del entorno (pandas, plotly, scikit-learn, etc.)
└── README.md                            # Documentación técnica y metodológica
