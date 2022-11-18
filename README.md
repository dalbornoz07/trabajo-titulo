Trabajo de título: Caracterización de los estudiantes de programación según su desempeño: un modelo predictivo 
==============================

Trabajo de título realizado por  el estudiante Diego Albornoz Ley para optar al título de Ingniero Civil Informático en la Universidad Técnica Federico Santa María.


Hoy en día, para las carreras y universidades un alto índice de reprobación puede significar en la reducción de años de acreditación que posee, afectar el ambiente universitario, como también generar un desfase respecto a la malla curricular por parte del estudiante. Es por ello que la asignatura de programación IWI-131 de la Universidad Técnica Federico Santa María requiere contar con herramientas o mecanismos que permitan detectar tempranamente aquellos estudiantes con mayor probabilidad de reprobar, para ello se utilizó un enfoque de minería de datos para obtener una caracterización del comportamiento de los estudiantes y
la influencia que tiene en el rendimiento de la asignatura, generando agrupamientos, reglas de asociación, entre otros; logrando así identificar grupos de comportamientos y tendencias que permitirán tomar decisiones en base a ellos.

Keywords: Caracterización, rendimiento académico estudiantes, Minería de datos Educacional


Organización de proyecto
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    └── src                <- Source code for use in this project.
       ├── __init__.py    <- Makes src a Python module
       │
       ├── data           <- Scripts to download or generate data
       │   └── make_dataset.py
       │
       ├── features       <- Scripts to turn raw data into features for modeling
       │   └── build_features.py
       │
       ├── models         <- Scripts to train models and then use trained models to make
       │   │                 predictions
       │   ├── predict_model.py
       │   └── train_model.py
       │
       └── visualization  <- Scripts to create exploratory and results oriented visualizations
           └── visualize.py


