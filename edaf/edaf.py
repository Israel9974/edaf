##############################################################################################
#
#
# @copyright Israel Cornejo
#
#
##############################################################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from matplotlib.backends.backend_pdf import PdfPages
from multiprocessing import Process, Queue
import time
import warnings # para envitar warnings de kdeplot
import statsmodels.api as sm


#CONTADOR DE MISSING VALUES
def contador_de_missing(x):
    missing = x.isna().sum()
    return missing[missing > 0]

# CLASIFICADOR DE OBJECTS Y BOOLS

def variables_categoricas(x):
    return x.select_dtypes(include=['object', 'bool'])

#CLASIFICADOR DE INT Y FLOATS
def variables_numericas(x):
    return x.select_dtypes(include=['int', 'float'])

#DESCRIPCIÓN DE VARIABLES CATEGÓRICAS

def mostrar_value_counts(x, variables):
    for columna in variables:
        print(x[columna].value_counts(normalize=False, dropna=True))
        print('------------------------------------')
        print(x[columna].value_counts(normalize=True, dropna=True))
        print('\n__\n')


#EVALUAR SI SE PUEDE HACER HISTOGRAMA

def evaluar_variable_histograma(serie, threshold_zero_ratio=0.5, threshold_outlier_pct=0.1):
    # Porcentaje de ceros
    zero_ratio = (serie == 0).mean()

    # Porcentaje de outliers según IQR
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    lower = q1 - 1.5 * iqr
    outlier_ratio = ((serie > upper) | (serie < lower)).mean()

    # Número de valores únicos
    n_unique = serie.nunique()

    return {
        'zero_ratio': zero_ratio,
        'outlier_ratio': outlier_ratio,
        'n_unique': n_unique,
        'prob_histograma_lento': (
            zero_ratio > threshold_zero_ratio or 
            outlier_ratio > threshold_outlier_pct 
        )
    }

#RESUMEN DE VARIABLES
def resumen_variable(x, col):
    total = len(x)  # Total original (incluye missing)
    serie = x[col]
    serie_sin_na = serie.dropna()

    # Missing values
    n_missing = serie.isna().sum()
    pct_missing = n_missing / total * 100

    # Ceros
    n_zeros = (serie_sin_na == 0).sum()
    pct_zeros = n_zeros / len(serie_sin_na) * 100

    # Outliers (según IQR)
    q1 = serie_sin_na.quantile(0.25)
    q3 = serie_sin_na.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    n_outliers = ((serie_sin_na < lower) | (serie_sin_na > upper)).sum()
    pct_outliers = n_outliers / len(serie_sin_na) * 100

    # Valores únicos
    n_unique = serie_sin_na.nunique()
    pct_unique = n_unique / len(serie_sin_na) * 100

    # Construir DataFrame resumen
    resumen = pd.DataFrame({
        'Caracteristica': ['Missing Values', 'Zeros', 'Outliers', 'Valores unicos'],
        'Cantidad': [n_missing, n_zeros, n_outliers, n_unique],
        'Porcentaje (%)': [pct_missing, pct_zeros, pct_outliers, pct_unique]
    })

    return resumen[['Caracteristica', 'Cantidad', 'Porcentaje (%)']]




# GENERACIÓN DE PDF CON GRÁFICOS Y ESTADÍSTICAS DESCRIPTIVAS

def edafreport(df, filename='ReporteEDA.pdf'):
    import warnings
    numeric_cols = df.select_dtypes(include='number').columns
    total = len(numeric_cols)

    with PdfPages(filename) as pdf:
        for idx, col in enumerate(numeric_cols, 1):
            fig, axes = plt.subplots(2, 3, figsize=(18, 8))  # 2 filas, 3 columnas

            # --- Boxplot ---
            sns.boxplot(x=df[col], ax=axes[0, 0], color='skyblue')
            axes[0, 0].set_title(f'Boxplot de {col}')
            axes[0, 0].set_xlabel(col)
            axes[0, 0].grid(True)

            # --- Histograma o KDE ---
            resultado = evaluar_variable_histograma(df[col])
            if resultado['prob_histograma_lento']:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=UserWarning)
                    sns.kdeplot(df[col], ax=axes[0, 1], color='lightgreen')
                axes[0, 1].set_title(f'KDE de {col}')
            else:
                sns.histplot(df[col], ax=axes[0, 1], kde=True, color='lightgreen')
                axes[0, 1].set_title(f'Histograma de {col}')
            axes[0, 1].set_xlabel(col)
            axes[0, 1].grid(True)

            # --- Estadísticas descriptivas (describe) ---
            description = pd.DataFrame(df[col].describe()).reset_index()
            axes[0, 2].axis('tight')
            axes[0, 2].axis('off')
            table1 = axes[0, 2].table(
                cellText=description.values,
                colLabels=description.columns,
                cellLoc='center',
                loc='center'
            )
            table1.auto_set_font_size(False)
            table1.set_fontsize(9)
            for i in range(len(description.columns)):
                cell = table1[(0, i)]
                cell.set_facecolor('#c00000')
                cell.set_text_props(color='white')
            axes[0, 2].set_title("Describe", fontsize=12, fontweight='bold')

            # Resumen Variable (missing, ceros, outliers, únicos) ---
            resumenVar = resumen_variable(df, col)
            axes[1, 0].axis('tight')
            axes[1, 0].axis('off')
            table2 = axes[1, 0].table(
                cellText=resumenVar.values,
                colLabels=resumenVar.columns,
                cellLoc='center',
                loc='center'
            )
            table2.auto_set_font_size(False)
            table2.set_fontsize(9)
            for i in range(len(resumenVar.columns)):
                cell = table2[(0, i)]
                cell.set_facecolor('#c00000')
                cell.set_text_props(color='white')
            axes[1, 0].set_title("Resumen Variable", fontsize=12, fontweight='bold')

            # --- QQ Plot ---
            sm.qqplot(df[col].dropna(),ax=axes[1,1], line='s')
            axes[1, 1].set_title(f'QQ Plot de {col}')
            axes[1, 1].grid(False)

            #  Vaciar los otros dos ejes 
            #axes[1, 1].axis('off')
            axes[1, 2].axis('off')
            fig.text(0.98, 0.01, 'Elaborado por: Israel Cornejo', ha='right', fontsize=9, color='gray')

            plt.tight_layout()
            pdf.savefig(fig)
            plt.close(fig)

            # Progreso
            porcentaje = (idx / total) * 100
            msg = f"Progreso: {porcentaje:.1f}% completado | Variable: {col}"
            print('\r' + msg + ' ' * 10, end='', flush=True)
            print()

        

    print(f"\n📊 PDF generado: {filename}")