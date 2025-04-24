# Objtetivo de exemplemficar e garantir uma boa estrutura no código e sempre garantir um padrão

project_name/
│
├── README.md              # Descrição geral do projeto
├── requirements.txt       # Dependências do projeto
├── setup.py               # Script de instalação (para pacotes distribuíveis)
├── .gitignore             # Arquivos e pastas a serem ignorados pelo Git
├── src/                   # Diretório principal do código fonte
│   └── project_name/      # Módulo principal do projeto
│       ├── __init__.py    # Torna o diretório um pacote Python
│       ├── module1.py     # Módulos de código (pode dividir conforme necessário)
│       └── module2.py
├── tests/                 # Testes unitários e de integração
│   ├── __init__.py
│   └── test_module1.py    # Arquivos de teste para cada módulo
└── docs/                  # Documentação do projeto
    └── index.md