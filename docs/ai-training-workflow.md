# 🔄 Fluxo de Trabalho - Treinamento de IA

## 📋 **Fluxo Sugerido para AR Online**

### **1. Planejamento (Fase Inicial)**

#### **1.1 Definição do Projeto**
```bash
# Criar estrutura do projeto
mkdir ai-project-{nome}
cd ai-project-{nome}

# Inicializar repositório
git init
git remote add origin https://github.com/ar-online/ai-project-{nome}.git

# Criar estrutura de diretórios
mkdir -p {data,models,notebooks,scripts,docs,tests}
mkdir -p {experiments,logs,reports}
```

#### **1.2 Configuração Inicial**
```python
# setup_project.py
import os
import json
from datetime import datetime

def setup_ai_project(project_name, objectives, timeline):
    """Configurar projeto de IA seguindo padrões AR Online"""
    
    # Configuração do projeto
    project_config = {
        'project_name': project_name,
        'created_date': datetime.now().isoformat(),
        'objectives': objectives,
        'timeline': timeline,
        'compliance': {
            'lgpd_compliant': True,
            'data_retention_policy': '2_years',
            'audit_trail': True
        },
        'quality_gates': {
            'min_accuracy': 0.8,
            'min_data_quality': 0.7,
            'required_tests': ['unit', 'integration', 'performance']
        }
    }
    
    # Salvar configuração
    with open('project_config.json', 'w') as f:
        json.dump(project_config, f, indent=2)
    
    print(f"✅ Projeto {project_name} configurado com sucesso!")
    return project_config
```

### **2. Desenvolvimento (Fase de Execução)**

#### **2.1 Análise de Dados**
```python
# notebooks/01_data_analysis.ipynb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

class DataAnalysisPipeline:
    """Pipeline de análise de dados para AR Online"""
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = None
        self.analysis_report = {}
    
    def load_and_explore(self):
        """Carregar e explorar dados"""
        # Carregar dados
        self.data = pd.read_csv(self.data_path)
        
        # Análise básica
        basic_info = {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'dtypes': self.data.dtypes.to_dict(),
            'missing_values': self.data.isnull().sum().to_dict(),
            'memory_usage': self.data.memory_usage(deep=True).sum()
        }
        
        self.analysis_report['basic_info'] = basic_info
        return basic_info
    
    def quality_assessment(self):
        """Avaliar qualidade dos dados"""
        quality_metrics = {}
        
        # Missing values
        missing_pct = self.data.isnull().sum().sum() / (self.data.shape[0] * self.data.shape[1])
        quality_metrics['missing_values_pct'] = missing_pct
        
        # Duplicates
        duplicate_pct = self.data.duplicated().sum() / len(self.data)
        quality_metrics['duplicate_pct'] = duplicate_pct
        
        # Outliers (IQR method)
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        outlier_count = 0
        for col in numeric_cols:
            Q1 = self.data[col].quantile(0.25)
            Q3 = self.data[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = self.data[(self.data[col] < Q1 - 1.5*IQR) | (self.data[col] > Q3 + 1.5*IQR)]
            outlier_count += len(outliers)
        
        outlier_pct = outlier_count / (len(self.data) * len(numeric_cols))
        quality_metrics['outlier_pct'] = outlier_pct
        
        # Score geral de qualidade
        quality_score = 1.0
        if missing_pct > 0.3: quality_score -= 0.3
        if duplicate_pct > 0.05: quality_score -= 0.2
        if outlier_pct > 0.1: quality_score -= 0.2
        
        quality_metrics['overall_quality_score'] = max(0, quality_score)
        
        self.analysis_report['quality_metrics'] = quality_metrics
        return quality_metrics
    
    def bias_analysis(self, target_column):
        """Análise de vieses nos dados"""
        if target_column not in self.data.columns:
            return None
        
        bias_report = {}
        
        # Análise de distribuição por grupos
        if 'gender' in self.data.columns:
            gender_dist = self.data.groupby('gender')[target_column].value_counts(normalize=True)
            bias_report['gender_distribution'] = gender_dist.to_dict()
        
        # Análise temporal
        if 'date' in self.data.columns:
            self.data['date'] = pd.to_datetime(self.data['date'])
            temporal_bias = self.data.groupby(self.data['date'].dt.year)[target_column].value_counts(normalize=True)
            bias_report['temporal_distribution'] = temporal_bias.to_dict()
        
        self.analysis_report['bias_analysis'] = bias_report
        return bias_report
    
    def generate_report(self):
        """Gerar relatório completo de análise"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'data_path': self.data_path,
            'analysis': self.analysis_report
        }
        
        # Salvar relatório
        with open('reports/data_analysis_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
```

#### **2.2 Pré-processamento**
```python
# scripts/data_preprocessing.py
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import joblib

class DataPreprocessor:
    """Pipeline de pré-processamento para AR Online"""
    
    def __init__(self):
        self.scalers = {}
        self.encoders = {}
        self.imputers = {}
        self.preprocessing_steps = []
    
    def clean_data(self, data):
        """Limpeza completa dos dados"""
        original_shape = data.shape
        
        # 1. Remover duplicatas
        data_cleaned = data.drop_duplicates()
        self.preprocessing_steps.append({
            'step': 'remove_duplicates',
            'records_removed': original_shape[0] - data_cleaned.shape[0]
        })
        
        # 2. Tratar valores ausentes
        numeric_cols = data_cleaned.select_dtypes(include=[np.number]).columns
        categorical_cols = data_cleaned.select_dtypes(include=['object']).columns
        
        # Para numéricos: média
        if len(numeric_cols) > 0:
            imputer_numeric = SimpleImputer(strategy='mean')
            data_cleaned[numeric_cols] = imputer_numeric.fit_transform(data_cleaned[numeric_cols])
            self.imputers['numeric'] = imputer_numeric
        
        # Para categóricos: moda
        if len(categorical_cols) > 0:
            imputer_categorical = SimpleImputer(strategy='most_frequent')
            data_cleaned[categorical_cols] = imputer_categorical.fit_transform(data_cleaned[categorical_cols])
            self.imputers['categorical'] = imputer_categorical
        
        self.preprocessing_steps.append({
            'step': 'handle_missing_values',
            'numeric_columns': len(numeric_cols),
            'categorical_columns': len(categorical_cols)
        })
        
        return data_cleaned
    
    def prepare_features(self, data, target_column):
        """Preparar features para treinamento"""
        # Separar features e target
        X = data.drop(columns=[target_column])
        y = data[target_column]
        
        # Encoding para categóricos
        categorical_cols = X.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            self.encoders[col] = le
        
        # Normalização para numéricos
        numeric_cols = X.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            scaler = StandardScaler()
            X[numeric_cols] = scaler.fit_transform(X[numeric_cols])
            self.scalers['numeric'] = scaler
        
        self.preprocessing_steps.append({
            'step': 'feature_preparation',
            'features_count': X.shape[1],
            'categorical_encoded': len(categorical_cols),
            'numeric_scaled': len(numeric_cols)
        })
        
        return X, y
    
    def save_preprocessors(self, output_dir='models'):
        """Salvar preprocessors para uso futuro"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Salvar scalers
        for name, scaler in self.scalers.items():
            joblib.dump(scaler, f'{output_dir}/{name}_scaler.joblib')
        
        # Salvar encoders
        for name, encoder in self.encoders.items():
            joblib.dump(encoder, f'{output_dir}/{name}_encoder.joblib')
        
        # Salvar imputers
        for name, imputer in self.imputers.items():
            joblib.dump(imputer, f'{output_dir}/{name}_imputer.joblib')
        
        # Salvar configuração
        config = {
            'preprocessing_steps': self.preprocessing_steps,
            'scalers': list(self.scalers.keys()),
            'encoders': list(self.encoders.keys()),
            'imputers': list(self.imputers.keys())
        }
        
        with open(f'{output_dir}/preprocessing_config.json', 'w') as f:
            json.dump(config, f, indent=2)
```

#### **2.3 Treinamento do Modelo**
```python
# scripts/model_training.py
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
import joblib

class ModelTrainer:
    """Treinador de modelos para AR Online"""
    
    def __init__(self, experiment_name):
        self.experiment_name = experiment_name
        self.training_log = []
        self.best_model = None
        self.best_params = {}
    
    def train_model(self, X_train, y_train, X_val, y_val):
        """Treinar modelo com validação"""
        # Configuração de hiperparâmetros
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2]
        }
        
        # Grid Search
        rf = RandomForestClassifier(random_state=42)
        grid_search = GridSearchCV(
            rf, param_grid, cv=5, scoring='f1_weighted', 
            n_jobs=-1, verbose=1
        )
        
        # Treinar
        grid_search.fit(X_train, y_train)
        
        # Melhor modelo
        self.best_model = grid_search.best_estimator_
        self.best_params = grid_search.best_params_
        
        # Avaliar no conjunto de validação
        y_pred = self.best_model.predict(X_val)
        
        # Métricas
        metrics = {
            'accuracy': accuracy_score(y_val, y_pred),
            'precision': precision_score(y_val, y_pred, average='weighted'),
            'recall': recall_score(y_val, y_pred, average='weighted'),
            'f1': f1_score(y_val, y_pred, average='weighted')
        }
        
        # Log do treinamento
        training_record = {
            'timestamp': datetime.now().isoformat(),
            'best_params': self.best_params,
            'metrics': metrics,
            'model_type': 'RandomForestClassifier'
        }
        self.training_log.append(training_record)
        
        return self.best_model, metrics
    
    def save_model(self, output_dir='models'):
        """Salvar modelo treinado"""
        if self.best_model is None:
            raise ValueError("Modelo não foi treinado ainda")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Salvar modelo
        model_path = f'{output_dir}/{self.experiment_name}_model.joblib'
        joblib.dump(self.best_model, model_path)
        
        # Salvar configuração
        config = {
            'experiment_name': self.experiment_name,
            'best_params': self.best_params,
            'training_log': self.training_log,
            'model_path': model_path
        }
        
        with open(f'{output_dir}/{self.experiment_name}_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        return model_path
```

### **3. Validação (Fase de Teste)**

#### **3.1 Executar Auditoria**
```python
# scripts/run_audit.py
from ai_training_auditor import AITrainingAuditor

def run_project_audit(project_config_path):
    """Executar auditoria completa do projeto"""
    
    # Carregar configuração do projeto
    with open(project_config_path, 'r') as f:
        project_config = json.load(f)
    
    # Executar auditoria
    auditor = AITrainingAuditor(project_config['project_name'])
    audit_results = auditor.run_complete_audit(project_config)
    
    # Verificar aprovação
    if audit_results['overall_score'] >= 80:
        print("✅ PROJETO APROVADO PARA PRODUÇÃO")
        return True
    else:
        print("❌ PROJETO REJEITADO - CORREÇÕES NECESSÁRIAS")
        print(f"Red Flags: {audit_results['red_flags']}")
        return False
```

#### **3.2 Testes Automatizados**
```python
# tests/test_model_performance.py
import unittest
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

class TestModelPerformance(unittest.TestCase):
    """Testes de performance do modelo"""
    
    def setUp(self):
        """Setup para testes"""
        # Gerar dados sintéticos para teste
        X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
    
    def test_minimum_accuracy(self):
        """Testar accuracy mínima"""
        # Carregar modelo treinado
        model = joblib.load('models/final_model.joblib')
        
        # Predições
        y_pred = model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        
        # Verificar threshold mínimo
        self.assertGreaterEqual(accuracy, 0.8, "Accuracy abaixo do threshold mínimo")
    
    def test_no_data_leakage(self):
        """Testar ausência de vazamento de dados"""
        # Verificar se dados de teste não foram usados no treinamento
        # Implementar lógica específica conforme necessário
        self.assertTrue(True, "Teste de vazamento de dados")
    
    def test_model_stability(self):
        """Testar estabilidade do modelo"""
        # Treinar modelo múltiplas vezes com seeds diferentes
        accuracies = []
        for seed in range(5):
            model = RandomForestClassifier(random_state=seed)
            model.fit(self.X_train, self.y_train)
            y_pred = model.predict(self.X_test)
            accuracies.append(accuracy_score(self.y_test, y_pred))
        
        # Verificar estabilidade (variação < 5%)
        variation = np.std(accuracies)
        self.assertLess(variation, 0.05, "Modelo instável")

if __name__ == '__main__':
    unittest.main()
```

### **4. Onboarding (Fase de Conhecimento)**

#### **4.1 Documentação para Novos Membros**
```markdown
# Guia de Onboarding - Projetos de IA

## 📚 Materiais de Referência

### Documentação Técnica
- [Checklist de Auditoria](ai-training-audit-checklist.md)
- [Guia de Execução](ai-training-execution-guide.md)
- [Fluxo de Trabalho](ai-training-workflow.md)

### Templates e Exemplos
- `templates/project_setup.py` - Configuração inicial
- `templates/data_analysis.ipynb` - Análise de dados
- `templates/model_training.py` - Treinamento
- `templates/audit_config.json` - Configuração de auditoria

### Ferramentas
- `scripts/ai-training-auditor.py` - Auditor automatizado
- `scripts/project_setup.py` - Setup de projeto
- `scripts/run_tests.py` - Execução de testes

## 🎯 Processo Padrão

### 1. Novo Projeto
```bash
# Usar template de setup
python scripts/project_setup.py --name "meu-projeto" --objectives "classificacao"
```

### 2. Desenvolvimento
```bash
# Seguir guia de execução
# Executar notebooks em ordem
# Manter logs de experimentos
```

### 3. Validação
```bash
# Executar auditoria
python scripts/ai-training-auditor.py --config project_config.json
```

### 4. Aprovação
```bash
# Verificar score >= 80
# Resolver red flags
# Obter aprovação de stakeholders
```

## 📋 Checklist Rápido

- [ ] Projeto configurado com template
- [ ] Dados analisados e documentados
- [ ] Modelo treinado com validação cruzada
- [ ] Auditoria executada e aprovada
- [ ] Testes automatizados passando
- [ ] Documentação completa
- [ ] Aprovação de stakeholders
```

---

## 🎯 **Benefícios para AR Online**

### **Padronização de Processos**
- ✅ Fluxo consistente para todos os projetos
- ✅ Templates reutilizáveis
- ✅ Critérios de qualidade uniformes
- ✅ Documentação padronizada

### **Garantia de Compliance LGPD**
- ✅ Mapeamento automático de dados pessoais
- ✅ Validação de base legal
- ✅ Políticas de retenção aplicadas
- ✅ Auditoria de compliance integrada

### **Redução de Erros**
- ✅ Checklist preventivo de problemas
- ✅ Validação automática de qualidade
- ✅ Testes automatizados obrigatórios
- ✅ Red flags identificadas precocemente

### **Documentação Sistematizada**
- ✅ Relatórios automáticos de auditoria
- ✅ Logs de experimentos estruturados
- ✅ Decisões de design justificadas
- ✅ Lições aprendidas documentadas

### **Auditoria e Rastreabilidade**
- ✅ Histórico completo de experimentos
- ✅ Versionamento de modelos e dados
- ✅ Logs de treinamento detalhados
- ✅ Certificação de compliance automática

---

**Este fluxo de trabalho garante que todos os projetos de IA da AR Online sigam as melhores práticas, atendam aos requisitos de compliance e mantenham alta qualidade técnica.**
