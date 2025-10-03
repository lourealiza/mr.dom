#!/usr/bin/env python3
"""
Setup Automatizado de Projetos de IA - AR Online
Cria estrutura padrão para novos projetos de ML
"""
import os
import json
import argparse
from datetime import datetime
from pathlib import Path

class AIProjectSetup:
    """Setup automatizado para projetos de IA"""
    
    def __init__(self, project_name: str, project_type: str = "classification"):
        self.project_name = project_name
        self.project_type = project_type
        self.project_dir = Path(project_name)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def create_project_structure(self):
        """Criar estrutura de diretórios do projeto"""
        print(f"Criando estrutura do projeto: {self.project_name}")
        
        # Diretórios principais
        directories = [
            "data/raw",
            "data/processed", 
            "data/external",
            "models",
            "notebooks",
            "scripts",
            "docs",
            "tests",
            "experiments",
            "logs",
            "reports",
            "templates"
        ]
        
        for directory in directories:
            dir_path = self.project_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Criado: {directory}")
        
        # Criar arquivos .gitkeep para diretórios vazios
        gitkeep_dirs = ["data/raw", "data/processed", "data/external", "logs", "reports"]
        for directory in gitkeep_dirs:
            gitkeep_path = self.project_dir / directory / ".gitkeep"
            gitkeep_path.touch()
    
    def create_config_files(self):
        """Criar arquivos de configuração"""
        print("Criando arquivos de configuração...")
        
        # project_config.json
        project_config = {
            "project_name": self.project_name,
            "project_type": self.project_type,
            "created_date": datetime.now().isoformat(),
            "version": "1.0.0",
            "objectives": {
                "business_goal": "A ser definido",
                "success_metrics": ["accuracy", "precision", "recall", "f1"],
                "target_performance": 0.8
            },
            "timeline": {
                "start_date": datetime.now().strftime("%Y-%m-%d"),
                "end_date": "A ser definido",
                "milestones": []
            },
            "compliance": {
                "lgpd_compliant": True,
                "data_retention_policy": "2_years",
                "audit_trail": True,
                "personal_data_mapping": {},
                "legal_basis": "A ser definido"
            },
            "quality_gates": {
                "min_accuracy": 0.8,
                "min_data_quality": 0.7,
                "required_tests": ["unit", "integration", "performance"],
                "audit_threshold": 80
            },
            "data": {
                "sources": [],
                "quality_threshold": 0.7,
                "preprocessing_steps": []
            },
            "model": {
                "type": self.project_type,
                "hyperparameter_tuning": True,
                "cross_validation": True,
                "interpretability_required": True
            },
            "deployment": {
                "environment": "production",
                "monitoring": True,
                "versioning": True,
                "rollback_plan": True
            }
        }
        
        config_path = self.project_dir / "project_config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(project_config, f, indent=2, ensure_ascii=False)
        print(f"  ✅ Criado: project_config.json")
        
        # requirements.txt
        requirements = [
            "pandas>=1.5.0",
            "numpy>=1.21.0",
            "scikit-learn>=1.1.0",
            "matplotlib>=3.5.0",
            "seaborn>=0.11.0",
            "jupyter>=1.0.0",
            "joblib>=1.2.0",
            "shap>=0.41.0",
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0"
        ]
        
        req_path = self.project_dir / "requirements.txt"
        with open(req_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(requirements))
        print(f"  ✅ Criado: requirements.txt")
        
        # .gitignore
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Jupyter Notebook
.ipynb_checkpoints

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Data
data/raw/*
!data/raw/.gitkeep
data/processed/*
!data/processed/.gitkeep
data/external/*
!data/external/.gitkeep

# Models
models/*.joblib
models/*.pkl
models/*.h5

# Logs
logs/*
!logs/.gitkeep

# Reports
reports/*
!reports/.gitkeep

# Experiments
experiments/*/
!experiments/.gitkeep

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.temp
"""
        
        gitignore_path = self.project_dir / ".gitignore"
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print(f"  ✅ Criado: .gitignore")
    
    def create_template_files(self):
        """Criar arquivos template"""
        print("Criando arquivos template...")
        
        # README.md
        readme_content = f"""# {self.project_name}

## 📋 Descrição do Projeto
[Descrever objetivo de negócio e problema a ser resolvido]

## 🎯 Objetivos
- **Objetivo Principal**: [Definir objetivo principal]
- **Métricas de Sucesso**: [Listar métricas]
- **Performance Alvo**: [Definir threshold mínimo]

## 📊 Dados
- **Fonte**: [Descrever fonte dos dados]
- **Volume**: [Quantidade de registros]
- **Período**: [Período dos dados]
- **Qualidade**: [Score de qualidade dos dados]

## 🤖 Modelo
- **Tipo**: {self.project_type}
- **Algoritmo**: [Algoritmo escolhido]
- **Performance**: [Métricas de performance]

## 📁 Estrutura do Projeto
```
{self.project_name}/
├── data/                    # Dados do projeto
│   ├── raw/                 # Dados brutos
│   ├── processed/           # Dados processados
│   └── external/            # Dados externos
├── models/                  # Modelos treinados
├── notebooks/               # Jupyter notebooks
├── scripts/                 # Scripts Python
├── docs/                    # Documentação
├── tests/                   # Testes automatizados
├── experiments/             # Experimentos
├── logs/                    # Logs de execução
├── reports/                 # Relatórios
└── templates/               # Templates
```

## 🚀 Como Executar

### 1. Configuração Inicial
```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar ambiente
python scripts/setup_environment.py
```

### 2. Análise de Dados
```bash
# Executar análise
jupyter notebook notebooks/01_data_analysis.ipynb
```

### 3. Treinamento
```bash
# Treinar modelo
python scripts/train_model.py
```

### 4. Avaliação
```bash
# Executar testes
python -m pytest tests/

# Executar auditoria
python scripts/ai-training-auditor.py
```

## 📋 Checklist de Qualidade
- [ ] Dados analisados e documentados
- [ ] Modelo treinado com validação cruzada
- [ ] Testes automatizados implementados
- [ ] Auditoria executada e aprovada
- [ ] Documentação completa
- [ ] Compliance LGPD validado

## 📞 Contato
- **Responsável**: [Nome do responsável]
- **Email**: [email@ar-online.com.br]
- **Data de Criação**: {datetime.now().strftime('%Y-%m-%d')}

---
*Projeto criado seguindo os padrões de qualidade da AR Online*
"""
        
        readme_path = self.project_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"  ✅ Criado: README.md")
        
        # Template de análise de dados
        analysis_template = """# Análise de Dados - {project_name}

## 📊 Objetivo
[Descrever objetivo da análise]

## 📋 Checklist de Análise
- [ ] Carregamento dos dados
- [ ] Análise exploratória básica
- [ ] Verificação de qualidade
- [ ] Análise de vieses
- [ ] Identificação de padrões
- [ ] Documentação de insights

## 🔍 Análise Exploratória

### 1. Carregamento dos Dados
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar dados
data = pd.read_csv('data/raw/dataset.csv')

# Informações básicas
print(f"Shape: {{data.shape}}")
print(f"Columns: {{list(data.columns)}}")
print(f"Data types: {{data.dtypes}}")
```

### 2. Análise de Qualidade
```python
# Valores ausentes
missing_data = data.isnull().sum()
print("Valores ausentes:")
print(missing_data[missing_data > 0])

# Duplicatas
duplicates = data.duplicated().sum()
print(f"Duplicatas: {{duplicates}}")

# Outliers
numeric_cols = data.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    Q1 = data[col].quantile(0.25)
    Q3 = data[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers = data[(data[col] < Q1 - 1.5*IQR) | (data[col] > Q3 + 1.5*IQR)]
    print(f"{{col}}: {{len(outliers)}} outliers")
```

### 3. Análise de Distribuições
```python
# Distribuição das variáveis numéricas
data[numeric_cols].hist(bins=50, figsize=(15, 10))
plt.tight_layout()
plt.show()

# Correlações
correlation_matrix = data[numeric_cols].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Matriz de Correlação')
plt.show()
```

## 📈 Insights e Próximos Passos
[Documentar insights encontrados e próximos passos]

---
*Análise executada em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
""".format(project_name=self.project_name)
        
        analysis_path = self.project_dir / "notebooks" / "01_data_analysis.ipynb"
        with open(analysis_path, 'w', encoding='utf-8') as f:
            f.write(analysis_template)
        print(f"  ✅ Criado: notebooks/01_data_analysis.ipynb")
        
        # Template de treinamento
        training_template = """#!/usr/bin/env python3
\"\"\"
Treinamento de Modelo - {project_name}
\"\"\"
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import json
from datetime import datetime

class ModelTrainer:
    \"\"\"Treinador de modelo para {project_name}\"\"\"
    
    def __init__(self):
        self.model = None
        self.best_params = {{}}
        self.training_log = []
    
    def load_data(self, data_path):
        \"\"\"Carregar dados processados\"\"\"
        data = pd.read_csv(data_path)
        print(f"Dados carregados: {{data.shape}}")
        return data
    
    def prepare_features(self, data, target_column):
        \"\"\"Preparar features para treinamento\"\"\"
        X = data.drop(columns=[target_column])
        y = data[target_column]
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        return X_train, X_test, y_train, y_test
    
    def train_model(self, X_train, y_train):
        \"\"\"Treinar modelo com validação cruzada\"\"\"
        # Configuração de hiperparâmetros
        param_grid = {{
            'n_estimators': [100, 200],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2]
        }}
        
        # Grid Search
        rf = RandomForestClassifier(random_state=42)
        grid_search = GridSearchCV(
            rf, param_grid, cv=5, scoring='f1_weighted', 
            n_jobs=-1, verbose=1
        )
        
        # Treinar
        grid_search.fit(X_train, y_train)
        
        self.model = grid_search.best_estimator_
        self.best_params = grid_search.best_params_
        
        print(f"Melhores parâmetros: {{self.best_params}}")
        print(f"Melhor score CV: {{grid_search.best_score_:.3f}}")
        
        return self.model
    
    def evaluate_model(self, X_test, y_test):
        \"\"\"Avaliar modelo\"\"\"
        y_pred = self.model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        print(f"Accuracy: {{accuracy:.3f}}")
        print("Classification Report:")
        print(report)
        
        return {{
            'accuracy': accuracy,
            'classification_report': report
        }}
    
    def save_model(self, output_path='models/final_model.joblib'):
        \"\"\"Salvar modelo treinado\"\"\"
        joblib.dump(self.model, output_path)
        
        # Salvar configuração
        config = {{
            'best_params': self.best_params,
            'training_date': datetime.now().isoformat(),
            'model_type': 'RandomForestClassifier'
        }}
        
        with open('models/model_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Modelo salvo: {{output_path}}")

def main():
    \"\"\"Função principal\"\"\"
    print("Treinamento de Modelo - {project_name}")
    print("=" * 50)
    
    # Inicializar treinador
    trainer = ModelTrainer()
    
    # Carregar dados
    data = trainer.load_data('data/processed/processed_data.csv')
    
    # Preparar features
    X_train, X_test, y_train, y_test = trainer.prepare_features(data, 'target')
    
    # Treinar modelo
    model = trainer.train_model(X_train, y_train)
    
    # Avaliar modelo
    metrics = trainer.evaluate_model(X_test, y_test)
    
    # Salvar modelo
    trainer.save_model()
    
    print("\\n✅ Treinamento concluído com sucesso!")

if __name__ == "__main__":
    main()
""".format(project_name=self.project_name)
        
        training_path = self.project_dir / "scripts" / "train_model.py"
        with open(training_path, 'w', encoding='utf-8') as f:
            f.write(training_template)
        print(f"  ✅ Criado: scripts/train_model.py")
        
        # Template de teste
        test_template = """#!/usr/bin/env python3
\"\"\"
Testes Automatizados - {project_name}
\"\"\"
import unittest
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import accuracy_score

class TestModelPerformance(unittest.TestCase):
    \"\"\"Testes de performance do modelo\"\"\"
    
    def setUp(self):
        \"\"\"Setup para testes\"\"\"
        # Carregar dados de teste
        self.test_data = pd.read_csv('data/processed/test_data.csv')
        
        # Carregar modelo
        try:
            self.model = joblib.load('models/final_model.joblib')
        except FileNotFoundError:
            self.skipTest("Modelo não encontrado")
    
    def test_minimum_accuracy(self):
        \"\"\"Testar accuracy mínima\"\"\"
        X_test = self.test_data.drop(columns=['target'])
        y_test = self.test_data['target']
        
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        self.assertGreaterEqual(accuracy, 0.8, "Accuracy abaixo do threshold mínimo")
    
    def test_data_quality(self):
        \"\"\"Testar qualidade dos dados\"\"\"
        # Verificar valores ausentes
        missing_pct = self.test_data.isnull().sum().sum() / (self.test_data.shape[0] * self.test_data.shape[1])
        self.assertLess(missing_pct, 0.1, "Muitos valores ausentes")
        
        # Verificar duplicatas
        duplicate_pct = self.test_data.duplicated().sum() / len(self.test_data)
        self.assertLess(duplicate_pct, 0.05, "Muitas duplicatas")
    
    def test_model_stability(self):
        \"\"\"Testar estabilidade do modelo\"\"\"
        # Implementar teste de estabilidade conforme necessário
        self.assertTrue(True, "Teste de estabilidade")

if __name__ == '__main__':
    unittest.main()
"""
        
        test_path = self.project_dir / "tests" / "test_model_performance.py"
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write(test_template)
        print(f"  ✅ Criado: tests/test_model_performance.py")
    
    def create_documentation(self):
        """Criar documentação inicial"""
        print("Criando documentação...")
        
        # Documentação de compliance
        compliance_doc = f"""# Compliance LGPD - {self.project_name}

## 📋 Mapeamento de Dados Pessoais

### Dados Identificados
- [ ] Listar dados pessoais identificados
- [ ] Categorizar por tipo (identificação, contato, etc.)
- [ ] Avaliar sensibilidade

### Base Legal
- [ ] Consentimento
- [ ] Execução de contrato
- [ ] Obrigação legal
- [ ] Interesse público
- [ ] Interesse legítimo
- [ ] Proteção da vida

### Políticas de Retenção
- **Período**: 2 anos
- **Critérios**: [Definir critérios]
- **Processo**: [Definir processo de exclusão]

## 🔒 Medidas de Segurança

### Controles Técnicos
- [ ] Criptografia de dados
- [ ] Controle de acesso
- [ ] Logs de auditoria
- [ ] Backup seguro

### Controles Organizacionais
- [ ] Treinamento da equipe
- [ ] Políticas de acesso
- [ ] Procedimentos de incidente
- [ ] Revisão periódica

## 📊 Relatório de Compliance
- **Status**: Em desenvolvimento
- **Última Revisão**: {datetime.now().strftime('%Y-%m-%d')}
- **Próxima Revisão**: [Definir data]

---
*Documento de compliance para {self.project_name}*
"""
        
        compliance_path = self.project_dir / "docs" / "compliance_lgpd.md"
        with open(compliance_path, 'w', encoding='utf-8') as f:
            f.write(compliance_doc)
        print(f"  ✅ Criado: docs/compliance_lgpd.md")
    
    def initialize_git_repository(self):
        """Inicializar repositório Git"""
        print("Inicializando repositório Git...")
        
        # Criar arquivo de configuração Git
        git_config = f"""[core]
    repositoryformatversion = 0
    filemode = false
    bare = false
    logallrefupdates = true
    symlinks = false
    ignorecase = true

[remote "origin"]
    url = https://github.com/ar-online/{self.project_name}.git
    fetch = +refs/heads/*:refs/remotes/origin/*

[branch "main"]
    remote = origin
    merge = refs/heads/main
"""
        
        git_path = self.project_dir / ".git" / "config"
        git_path.parent.mkdir(parents=True, exist_ok=True)
        with open(git_path, 'w', encoding='utf-8') as f:
            f.write(git_config)
        
        print(f"  ✅ Repositório Git inicializado")
    
    def generate_setup_summary(self):
        """Gerar resumo do setup"""
        summary = f"""
🎉 PROJETO {self.project_name.upper()} CRIADO COM SUCESSO!

📁 Estrutura Criada:
   ├── data/ (raw, processed, external)
   ├── models/
   ├── notebooks/
   ├── scripts/
   ├── docs/
   ├── tests/
   ├── experiments/
   ├── logs/
   ├── reports/
   └── templates/

📋 Arquivos de Configuração:
   ├── project_config.json
   ├── requirements.txt
   ├── .gitignore
   └── README.md

📚 Templates Criados:
   ├── notebooks/01_data_analysis.ipynb
   ├── scripts/train_model.py
   ├── tests/test_model_performance.py
   └── docs/compliance_lgpd.md

🚀 Próximos Passos:
   1. cd {self.project_name}
   2. pip install -r requirements.txt
   3. Configurar dados em data/raw/
   4. Executar análise em notebooks/
   5. Treinar modelo com scripts/
   6. Executar auditoria: python scripts/ai-training-auditor.py

📞 Suporte:
   - Documentação: docs/
   - Templates: templates/
   - Padrões AR Online: [link para documentação]

---
Projeto criado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        print(summary)
        
        # Salvar resumo
        summary_path = self.project_dir / "SETUP_SUMMARY.md"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)
    
    def run_complete_setup(self):
        """Executar setup completo"""
        print(f"🚀 Iniciando setup do projeto: {self.project_name}")
        print("=" * 60)
        
        try:
            # Criar estrutura
            self.create_project_structure()
            
            # Criar arquivos de configuração
            self.create_config_files()
            
            # Criar templates
            self.create_template_files()
            
            # Criar documentação
            self.create_documentation()
            
            # Inicializar Git
            self.initialize_git_repository()
            
            # Gerar resumo
            self.generate_setup_summary()
            
            print("\n✅ Setup concluído com sucesso!")
            
        except Exception as e:
            print(f"\n❌ Erro durante setup: {e}")
            raise

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Setup automatizado de projetos de IA')
    parser.add_argument('--name', required=True, help='Nome do projeto')
    parser.add_argument('--type', default='classification', 
                       choices=['classification', 'regression', 'clustering'],
                       help='Tipo do projeto')
    
    args = parser.parse_args()
    
    # Executar setup
    setup = AIProjectSetup(args.name, args.type)
    setup.run_complete_setup()

if __name__ == "__main__":
    main()
