hotmart_processo_seletivo
==============================

Esse repositório é utilizado para responder as perguntas do processo seletivo da Hotmart.
O foco dado nas análises foi no entendimento da dependência da Hotmart com os produtos de maior faturamento e na geração de um modelo de Machine Learning, para indicar as principais variáveis, que indicam o faturamento de um produto.

O modelo de faturamento foi gerado, mas os resultados não foram satisfatórios, e não sobrou tempo para implementar o modelo no Dashboard.

Guia de Instalação
------------
Windows:

    Clicar no arquivo install.bat vai instalar as bibliotecas do requirements em um venv chamado hotmart_venv

Linux:

    No diretorio do projeto rodar """./setup_hotmart.sh""" para instalar as bibliotecas em um venv chamado hotmart_venv


Utilizando o Dashboard
------------
    1- Va no diretorio do Dashboard
    2- No prompt de comando, chame python index.py
    3- Digitar o endereço do servidor local gerado pelo Dashboard


Project Organization
------------
    |── Dashboard          <- Dashboard used to present the data
    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. 
    │                       
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    └── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── data           <- Scripts to download data
        │   └── get_raw_data.py
        │
        ├── features       <- Scripts to turn raw data into features for modeling
        │   └── build_features.py
        │
        ├── models         <- Scripts to train models and then use trained models to make
            │                 predictions
            ├── predict_model.py
            └── train_model.py
   


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
