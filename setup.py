from setuptools import setup, find_packages

setup(
    name='edaf',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0.0',
        'numpy>=1.18.0',
        'matplotlib>=3.0.0',
        'seaborn>=0.10.0',
        'scipy>=1.4.0',
        'statsmodels>=0.11.0',
        'Pillow>=9.2.0'
    ],  # Aquí puedes poner dependencias si las hay
    author='Israel Cornejo',
    description='Genera un reporte en PDF para Análisis Exploratorio de Variables int y float',
    url='https://github.com/Israel9974/edaf',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='EDA, PDF, análisis exploratorio, pandas, numpy, matplotlib, seaborn, scipy, statsmodels',
    include_package_data=True,
)



