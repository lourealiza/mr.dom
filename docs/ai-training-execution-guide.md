# 🚀 Guia de Execução - Treinamento de IA

## 📋 **Instruções Práticas Passo-a-Passo**

### **Fase 1: Planejamento e Preparação**

#### **1.1 Definição de Objetivos**
```python
# template_objectives.py
class ProjectObjectives:
    def __init__(self):
        self.business_objective = ""
        self.success_metrics = []
        self.acceptance_criteria = {}
        self.timeline = {}
    
    def validate_objectives(self):
        """Validar se objetivos estão bem definidos"""
        checks = [
            len(self.business_objective) > 50,
            len(self.success_metrics) >= 3,
            len(self.acceptance_criteria) >= 2,
            'start_date' in self.timeline,
            'end_date' in self.timeline
        ]
        return all(checks)
```

#### **1.2 Análise de Dados**
```python
# data_analysis.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

class DataAnalyzer:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.analysis_report = {}
    
    def basic_analysis(self):
        """Análise básica dos dados"""
        report = {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'dtypes': self.data.dtypes.to_dict(),
            'missing_values': self.data.isnull().sum().to_dict(),
            'duplicates': self.data.duplicated().sum(),
            'memory_usage': self.data.memory_usage(deep=True).sum()
        }
        self.analysis_report['basic'] = report
        return report
    
    def quality_assessment(self):
        """Avaliação de qualidade dos dados"""
        quality_score = 0
        total_checks = 5
        
        # Check 1: Missing values < 30%
        missing_pct = self.data.isnull().sum().sum() / (self.data.shape[0] * self.data.shape[1])
        if missing_pct < 0.3:
            quality_score += 1
        
        # Check 2: Duplicates < 5%
        duplicate_pct = self.data.duplicated().sum() / len(self.data)
        if duplicate_pct < 0.05:
            quality_score += 1
        
        # Check 3: Sufficient samples
        if len(self.data) >= 1000:
            quality_score += 1
        
        # Check 4: Balanced classes (for classification)
        if 'target' in self.data.columns:
            class_balance = self.data['target'].value_counts().min() / self.data['target'].value_counts().max()
            if class_balance > 0.1:
                quality_score += 1
        
        # Check 5: No extreme outliers
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        outlier_count = 0
        for col in numeric_cols:
            Q1 = self.data[col].quantile(0.25)
            Q3 = self.data[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = self.data[(self.data[col] < Q1 - 1.5*IQR) | (self.data[col] > Q3 + 1.5*IQR)]
            outlier_count += len(outliers)
        
        outlier_pct = outlier_count / (len(self.data) * len(numeric_cols))
        if outlier_pct < 0.1:
            quality_score += 1
        
        self.analysis_report['quality_score'] = quality_score / total_checks
        return quality_score / total_checks
```

#### **1.3 Compliance LGPD**
```python
# lgpd_compliance.py
class LGPDCompliance:
    def __init__(self):
        self.personal_data_mapping = {}
        self.legal_basis = {}
        self.consent_records = {}
        self.retention_policy = {}
    
    def identify_personal_data(self, data_columns):
        """Identificar dados pessoais nas colunas"""
        personal_data_indicators = [
            'cpf', 'cnpj', 'email', 'telefone', 'endereco', 'nome',
            'rg', 'data_nascimento', 'cep', 'cidade', 'estado'
        ]
        
        personal_columns = []
        for col in data_columns:
            col_lower = col.lower()
            if any(indicator in col_lower for indicator in personal_data_indicators):
                personal_columns.append(col)
        
        self.personal_data_mapping = {
            'columns': personal_columns,
            'count': len(personal_columns),
            'percentage': len(personal_columns) / len(data_columns) * 100
        }
        return self.personal_data_mapping
    
    def validate_legal_basis(self):
        """Validar base legal para processamento"""
        required_basis = [
            'consentimento',
            'execucao_contrato',
            'obrigacao_legal',
            'interesse_publico',
            'interesse_legitimo',
            'protecao_vida'
        ]
        
        # Verificar se pelo menos uma base legal está definida
        has_basis = any(basis in self.legal_basis for basis in required_basis)
        
        return {
            'has_legal_basis': has_basis,
            'defined_basis': list(self.legal_basis.keys()),
            'compliance_status': 'COMPLIANT' if has_basis else 'NON_COMPLIANT'
        }
```

### **Fase 2: Preparação dos Dados**

#### **2.1 Coleta e Validação**
```python
# data_collection.py
import logging
from datetime import datetime

class DataCollector:
    def __init__(self):
        self.logger = self._setup_logging()
        self.collection_log = []
    
    def _setup_logging(self):
        """Configurar logging para auditoria"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('data_collection.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def collect_data(self, source_config):
        """Coletar dados de fonte autorizada"""
        try:
            self.logger.info(f"Iniciando coleta de dados de: {source_config['source']}")
            
            # Simular coleta (implementar conforme fonte real)
            data = self._fetch_data(source_config)
            
            # Log da coleta
            collection_record = {
                'timestamp': datetime.now().isoformat(),
                'source': source_config['source'],
                'records_collected': len(data),
                'status': 'SUCCESS'
            }
            self.collection_log.append(collection_record)
            
            self.logger.info(f"Coleta concluída: {len(data)} registros")
            return data
            
        except Exception as e:
            self.logger.error(f"Erro na coleta: {str(e)}")
            collection_record = {
                'timestamp': datetime.now().isoformat(),
                'source': source_config['source'],
                'error': str(e),
                'status': 'ERROR'
            }
            self.collection_log.append(collection_record)
            raise
    
    def _fetch_data(self, config):
        """Implementar coleta real conforme fonte"""
        # Implementar conforme necessidade
        pass
```

#### **2.2 Limpeza e Preprocessamento**
```python
# data_preprocessing.py
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer

class DataPreprocessor:
    def __init__(self):
        self.preprocessing_steps = []
        self.scalers = {}
        self.encoders = {}
    
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
        
        # Para categóricos: moda
        if len(categorical_cols) > 0:
            imputer_categorical = SimpleImputer(strategy='most_frequent')
            data_cleaned[categorical_cols] = imputer_categorical.fit_transform(data_cleaned[categorical_cols])
        
        self.preprocessing_steps.append({
            'step': 'handle_missing_values',
            'numeric_columns': len(numeric_cols),
            'categorical_columns': len(categorical_cols)
        })
        
        # 3. Tratar outliers (IQR method)
        for col in numeric_cols:
            Q1 = data_cleaned[col].quantile(0.25)
            Q3 = data_cleaned[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = data_cleaned[(data_cleaned[col] < lower_bound) | (data_cleaned[col] > upper_bound)]
            if len(outliers) > 0:
                # Cap outliers instead of removing
                data_cleaned[col] = data_cleaned[col].clip(lower_bound, upper_bound)
        
        self.preprocessing_steps.append({
            'step': 'handle_outliers',
            'method': 'IQR_capping'
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
```

#### **2.3 Divisão de Dados**
```python
# data_splitting.py
from sklearn.model_selection import train_test_split, StratifiedKFold

class DataSplitter:
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.splits = {}
    
    def split_data(self, X, y, test_size=0.2, val_size=0.2):
        """Divisão estratificada dos dados"""
        # Primeiro split: treino + validação vs teste
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state, stratify=y
        )
        
        # Segundo split: treino vs validação
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_size/(1-test_size), 
            random_state=self.random_state, stratify=y_temp
        )
        
        self.splits = {
            'X_train': X_train, 'X_val': X_val, 'X_test': X_test,
            'y_train': y_train, 'y_val': y_val, 'y_test': y_test,
            'train_size': len(X_train), 'val_size': len(X_val), 'test_size': len(X_test)
        }
        
        # Validar distribuição
        self._validate_distribution(y_train, y_val, y_test)
        
        return self.splits
    
    def _validate_distribution(self, y_train, y_val, y_test):
        """Validar se distribuição foi mantida"""
        train_dist = y_train.value_counts(normalize=True)
        val_dist = y_val.value_counts(normalize=True)
        test_dist = y_test.value_counts(normalize=True)
        
        # Verificar se distribuições são similares
        max_diff = max([
            abs(train_dist[cls] - val_dist[cls]) for cls in train_dist.index
        ])
        
        if max_diff > 0.05:  # 5% de tolerância
            print(f"⚠️ Aviso: Diferença na distribuição entre splits: {max_diff:.3f}")
        else:
            print("✅ Distribuição estratificada mantida")
```

### **Fase 3: Seleção e Configuração do Modelo**

#### **3.1 Seleção de Arquitetura**
```python
# model_selection.py
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

class ModelSelector:
    def __init__(self):
        self.models = {
            'logistic_regression': LogisticRegression(random_state=42),
            'random_forest': RandomForestClassifier(random_state=42),
            'gradient_boosting': GradientBoostingClassifier(random_state=42),
            'svm': SVC(random_state=42)
        }
        self.results = {}
    
    def evaluate_models(self, X_train, X_val, y_train, y_val):
        """Avaliar múltiplos modelos"""
        for name, model in self.models.items():
            print(f"Treinando {name}...")
            
            # Treinar modelo
            model.fit(X_train, y_train)
            
            # Predições
            y_pred = model.predict(X_val)
            
            # Métricas
            metrics = {
                'accuracy': accuracy_score(y_val, y_pred),
                'precision': precision_score(y_val, y_pred, average='weighted'),
                'recall': recall_score(y_val, y_pred, average='weighted'),
                'f1': f1_score(y_val, y_pred, average='weighted')
            }
            
            self.results[name] = {
                'model': model,
                'metrics': metrics
            }
            
            print(f"{name}: Accuracy = {metrics['accuracy']:.3f}")
        
        return self.results
    
    def select_best_model(self):
        """Selecionar melhor modelo baseado em F1-score"""
        best_model = None
        best_score = 0
        best_name = None
        
        for name, result in self.results.items():
            f1_score = result['metrics']['f1']
            if f1_score > best_score:
                best_score = f1_score
                best_model = result['model']
                best_name = name
        
        print(f"✅ Melhor modelo: {best_name} (F1-score: {best_score:.3f})")
        return best_name, best_model
```

#### **3.2 Otimização de Hiperparâmetros**
```python
# hyperparameter_tuning.py
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.metrics import make_scorer

class HyperparameterTuner:
    def __init__(self):
        self.best_params = {}
        self.tuning_history = []
    
    def tune_model(self, model, param_grid, X_train, y_train, cv=5):
        """Otimização de hiperparâmetros"""
        # Usar F1-score como métrica principal
        scorer = make_scorer(f1_score, average='weighted')
        
        # Grid Search
        grid_search = GridSearchCV(
            model, param_grid, cv=cv, scoring=scorer, 
            n_jobs=-1, verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        self.best_params = grid_search.best_params_
        self.tuning_history.append({
            'method': 'grid_search',
            'best_score': grid_search.best_score_,
            'best_params': grid_search.best_params_,
            'cv_results': grid_search.cv_results_
        })
        
        print(f"✅ Melhores parâmetros: {self.best_params}")
        print(f"✅ Melhor score CV: {grid_search.best_score_:.3f}")
        
        return grid_search.best_estimator_
```

### **Fase 4: Treinamento**

#### **4.1 Configuração do Ambiente**
```python
# training_environment.py
import os
import json
from datetime import datetime
import joblib

class TrainingEnvironment:
    def __init__(self, experiment_name):
        self.experiment_name = experiment_name
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.experiment_dir = f"experiments/{experiment_name}_{self.timestamp}"
        self.setup_environment()
    
    def setup_environment(self):
        """Configurar ambiente de treinamento"""
        # Criar diretório do experimento
        os.makedirs(self.experiment_dir, exist_ok=True)
        os.makedirs(f"{self.experiment_dir}/models", exist_ok=True)
        os.makedirs(f"{self.experiment_dir}/logs", exist_ok=True)
        os.makedirs(f"{self.experiment_dir}/checkpoints", exist_ok=True)
        
        # Configurar logging
        self.setup_logging()
        
        # Salvar configuração
        self.save_config()
    
    def setup_logging(self):
        """Configurar logging detalhado"""
        import logging
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"{self.experiment_dir}/logs/training.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.experiment_name)
    
    def save_config(self):
        """Salvar configuração do experimento"""
        config = {
            'experiment_name': self.experiment_name,
            'timestamp': self.timestamp,
            'python_version': os.sys.version,
            'environment': os.environ.get('CONDA_DEFAULT_ENV', 'base')
        }
        
        with open(f"{self.experiment_dir}/config.json", 'w') as f:
            json.dump(config, f, indent=2)
    
    def save_model(self, model, model_name):
        """Salvar modelo treinado"""
        model_path = f"{self.experiment_dir}/models/{model_name}.joblib"
        joblib.dump(model, model_path)
        self.logger.info(f"Modelo salvo: {model_path}")
        return model_path
```

#### **4.2 Execução do Treinamento**
```python
# model_training.py
import time
from sklearn.metrics import classification_report, confusion_matrix

class ModelTrainer:
    def __init__(self, environment):
        self.env = environment
        self.training_log = []
    
    def train_model(self, model, X_train, y_train, X_val, y_val):
        """Executar treinamento completo"""
        start_time = time.time()
        
        self.env.logger.info("Iniciando treinamento...")
        
        # Treinar modelo
        model.fit(X_train, y_train)
        
        # Avaliar no conjunto de validação
        y_pred = model.predict(X_val)
        
        # Calcular métricas
        metrics = self._calculate_metrics(y_val, y_pred)
        
        # Tempo de treinamento
        training_time = time.time() - start_time
        
        # Log do treinamento
        training_record = {
            'timestamp': datetime.now().isoformat(),
            'training_time': training_time,
            'metrics': metrics,
            'model_type': type(model).__name__
        }
        self.training_log.append(training_record)
        
        # Salvar modelo
        model_path = self.env.save_model(model, 'final_model')
        
        # Gerar relatório
        self._generate_report(y_val, y_pred, metrics, training_time)
        
        self.env.logger.info(f"Treinamento concluído em {training_time:.2f}s")
        return model, metrics
    
    def _calculate_metrics(self, y_true, y_pred):
        """Calcular métricas de performance"""
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        return {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted'),
            'recall': recall_score(y_true, y_pred, average='weighted'),
            'f1': f1_score(y_true, y_pred, average='weighted')
        }
    
    def _generate_report(self, y_true, y_pred, metrics, training_time):
        """Gerar relatório de treinamento"""
        report = {
            'training_summary': {
                'timestamp': datetime.now().isoformat(),
                'training_time': training_time,
                'metrics': metrics
            },
            'classification_report': classification_report(y_true, y_pred, output_dict=True),
            'confusion_matrix': confusion_matrix(y_true, y_pred).tolist()
        }
        
        # Salvar relatório
        import json
        with open(f"{self.env.experiment_dir}/training_report.json", 'w') as f:
            json.dump(report, f, indent=2)
```

### **Fase 5: Avaliação e Validação**

#### **5.1 Avaliação Completa**
```python
# model_evaluation.py
from sklearn.metrics import roc_auc_score, roc_curve
import matplotlib.pyplot as plt

class ModelEvaluator:
    def __init__(self, environment):
        self.env = environment
        self.evaluation_results = {}
    
    def comprehensive_evaluation(self, model, X_test, y_test):
        """Avaliação completa do modelo"""
        # Predições
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None
        
        # Métricas básicas
        basic_metrics = self._calculate_basic_metrics(y_test, y_pred)
        
        # Métricas avançadas
        advanced_metrics = self._calculate_advanced_metrics(y_test, y_pred, y_pred_proba)
        
        # Análise de erro
        error_analysis = self._analyze_errors(y_test, y_pred)
        
        # Robustez
        robustness_tests = self._test_robustness(model, X_test, y_test)
        
        self.evaluation_results = {
            'basic_metrics': basic_metrics,
            'advanced_metrics': advanced_metrics,
            'error_analysis': error_analysis,
            'robustness_tests': robustness_tests
        }
        
        # Gerar relatório
        self._generate_evaluation_report()
        
        return self.evaluation_results
    
    def _calculate_basic_metrics(self, y_true, y_pred):
        """Calcular métricas básicas"""
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        return {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted'),
            'recall': recall_score(y_true, y_pred, average='weighted'),
            'f1': f1_score(y_true, y_pred, average='weighted')
        }
    
    def _calculate_advanced_metrics(self, y_true, y_pred, y_pred_proba):
        """Calcular métricas avançadas"""
        metrics = {}
        
        # AUC-ROC se disponível
        if y_pred_proba is not None and len(set(y_true)) == 2:
            metrics['auc_roc'] = roc_auc_score(y_true, y_pred_proba[:, 1])
        
        return metrics
    
    def _analyze_errors(self, y_true, y_pred):
        """Análise de erros"""
        errors = y_true != y_pred
        error_rate = errors.sum() / len(y_true)
        
        return {
            'error_rate': error_rate,
            'total_errors': errors.sum(),
            'correct_predictions': (~errors).sum()
        }
    
    def _test_robustness(self, model, X_test, y_test):
        """Testes de robustez"""
        # Teste com pequenas perturbações
        noise_levels = [0.01, 0.05, 0.1]
        robustness_results = {}
        
        for noise_level in noise_levels:
            X_noisy = X_test + np.random.normal(0, noise_level, X_test.shape)
            y_pred_noisy = model.predict(X_noisy)
            accuracy_noisy = accuracy_score(y_test, y_pred_noisy)
            
            robustness_results[f'noise_{noise_level}'] = {
                'accuracy': accuracy_noisy,
                'degradation': self.evaluation_results['basic_metrics']['accuracy'] - accuracy_noisy
            }
        
        return robustness_results
```

### **Fase 6: Interpretabilidade e Explicabilidade**

#### **6.1 Análise de Importância**
```python
# model_interpretability.py
import shap
import matplotlib.pyplot as plt

class ModelInterpreter:
    def __init__(self, environment):
        self.env = environment
        self.interpretation_results = {}
    
    def analyze_feature_importance(self, model, X_train, feature_names):
        """Análise de importância das features"""
        # Feature importance (para modelos que suportam)
        if hasattr(model, 'feature_importances_'):
            importance_scores = model.feature_importances_
            feature_importance = dict(zip(feature_names, importance_scores))
            
            # Ordenar por importância
            sorted_importance = dict(sorted(feature_importance.items(), 
                                          key=lambda x: x[1], reverse=True))
            
            self.interpretation_results['feature_importance'] = sorted_importance
            
            # Plot
            self._plot_feature_importance(sorted_importance)
        
        return self.interpretation_results
    
    def explain_predictions(self, model, X_test, sample_indices=None):
        """Explicar predições usando SHAP"""
        try:
            # Criar explainer
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_test)
            
            # Explicações para amostras específicas
            if sample_indices is None:
                sample_indices = [0, 1, 2]  # Primeiras 3 amostras
            
            explanations = {}
            for idx in sample_indices:
                explanations[f'sample_{idx}'] = {
                    'prediction': model.predict([X_test.iloc[idx]])[0],
                    'shap_values': shap_values[idx].tolist() if isinstance(shap_values, np.ndarray) else shap_values[0][idx].tolist()
                }
            
            self.interpretation_results['shap_explanations'] = explanations
            
            # Plot SHAP
            self._plot_shap_summary(shap_values, X_test)
            
        except Exception as e:
            self.env.logger.warning(f"SHAP não disponível: {e}")
            self.interpretation_results['shap_explanations'] = None
    
    def _plot_feature_importance(self, importance_dict):
        """Plot de importância das features"""
        features = list(importance_dict.keys())[:10]  # Top 10
        scores = [importance_dict[f] for f in features]
        
        plt.figure(figsize=(10, 6))
        plt.barh(features, scores)
        plt.xlabel('Importance Score')
        plt.title('Top 10 Feature Importance')
        plt.tight_layout()
        plt.savefig(f"{self.env.experiment_dir}/feature_importance.png")
        plt.close()
    
    def _plot_shap_summary(self, shap_values, X_test):
        """Plot SHAP summary"""
        plt.figure(figsize=(10, 8))
        shap.summary_plot(shap_values, X_test, show=False)
        plt.tight_layout()
        plt.savefig(f"{self.env.experiment_dir}/shap_summary.png")
        plt.close()
```

---

## 📋 **Checklist de Entregáveis Obrigatórios**

### **Documentação Técnica**
- [ ] Relatório de análise de dados
- [ ] Documentação de pré-processamento
- [ ] Relatório de seleção de modelo
- [ ] Logs de treinamento completos
- [ ] Relatório de avaliação
- [ ] Análise de interpretabilidade

### **Artefatos de Código**
- [ ] Scripts de coleta de dados
- [ ] Pipeline de pré-processamento
- [ ] Código de treinamento
- [ ] Scripts de avaliação
- [ ] Configurações versionadas

### **Modelos e Dados**
- [ ] Modelo treinado salvo
- [ ] Dados de treinamento versionados
- [ ] Métricas de performance
- [ ] Validação cruzada completa

### **Compliance**
- [ ] Mapeamento de dados pessoais
- [ ] Base legal documentada
- [ ] Política de retenção
- [ ] Relatório de compliance LGPD

---

## 🎯 **Configurações Seguras Recomendadas**

### **Validação Cruzada**
```python
# Configurações seguras para CV
CV_CONFIG = {
    'cv_folds': 5,
    'random_state': 42,
    'stratify': True,
    'shuffle': True
}
```

### **Divisão de Dados**
```python
# Proporções seguras
DATA_SPLIT = {
    'train_size': 0.7,
    'val_size': 0.15,
    'test_size': 0.15,
    'min_samples_per_class': 100
}
```

### **Hiperparâmetros Iniciais**
```python
# Valores seguros para início
SAFE_HYPERPARAMETERS = {
    'random_forest': {
        'n_estimators': [100, 200],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    },
    'logistic_regression': {
        'C': [0.1, 1, 10],
        'penalty': ['l1', 'l2'],
        'solver': ['liblinear']
    }
}
```

---

**Este guia garante que todos os projetos de ML da AR Online sejam executados seguindo as melhores práticas e atendam aos requisitos de qualidade e compliance.**
