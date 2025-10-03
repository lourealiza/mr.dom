#!/usr/bin/env python3
"""
Auditor de Treinamento de IA - AR Online
Sistema automatizado para validação de processos de ML
"""
import json
import os
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Tuple
import logging

class AITrainingAuditor:
    """Auditor completo para processos de treinamento de IA"""
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.audit_results = {}
        self.red_flags = []
        self.compliance_status = {}
        self.setup_logging()
    
    def setup_logging(self):
        """Configurar logging para auditoria"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'audit_{self.project_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(f'Auditor_{self.project_name}')
    
    def run_complete_audit(self, project_config: Dict[str, Any]) -> Dict[str, Any]:
        """Executar auditoria completa do projeto"""
        self.logger.info(f"Iniciando auditoria completa do projeto: {self.project_name}")
        
        # Fase 1: Planejamento e Preparação
        phase1_results = self.audit_planning_phase(project_config)
        
        # Fase 2: Preparação dos Dados
        phase2_results = self.audit_data_preparation(project_config)
        
        # Fase 3: Seleção de Modelo
        phase3_results = self.audit_model_selection(project_config)
        
        # Fase 4: Treinamento
        phase4_results = self.audit_training_phase(project_config)
        
        # Fase 5: Avaliação
        phase5_results = self.audit_evaluation_phase(project_config)
        
        # Fase 6: Interpretabilidade
        phase6_results = self.audit_interpretability(project_config)
        
        # Fase 7: Deployment
        phase7_results = self.audit_deployment_readiness(project_config)
        
        # Fase 8: Governança
        phase8_results = self.audit_governance(project_config)
        
        # Consolidar resultados
        self.audit_results = {
            'project_name': self.project_name,
            'audit_date': datetime.now().isoformat(),
            'phases': {
                'planning': phase1_results,
                'data_preparation': phase2_results,
                'model_selection': phase3_results,
                'training': phase4_results,
                'evaluation': phase5_results,
                'interpretability': phase6_results,
                'deployment': phase7_results,
                'governance': phase8_results
            },
            'red_flags': self.red_flags,
            'compliance_status': self.compliance_status
        }
        
        # Calcular score e recomendação após criar audit_results
        overall_score = self._calculate_overall_score()
        recommendation = self._generate_recommendation(overall_score)
        
        self.audit_results['overall_score'] = overall_score
        self.audit_results['recommendation'] = recommendation
        
        # Gerar relatório
        self._generate_audit_report()
        
        return self.audit_results
    
    def audit_planning_phase(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Auditar fase de planejamento"""
        self.logger.info("Auditando fase de planejamento...")
        
        results = {
            'objectives_defined': False,
            'success_metrics': [],
            'timeline_defined': False,
            'lgpd_compliance': False,
            'data_inventory': False,
            'score': 0
        }
        
        # Verificar objetivos
        if 'objectives' in config and config['objectives']:
            results['objectives_defined'] = True
            results['success_metrics'] = config['objectives'].get('metrics', [])
        
        # Verificar timeline
        if 'timeline' in config and config['timeline']:
            results['timeline_defined'] = True
        
        # Verificar compliance LGPD
        lgpd_checks = [
            'personal_data_mapping' in config,
            'legal_basis' in config,
            'consent_records' in config,
            'retention_policy' in config
        ]
        results['lgpd_compliance'] = all(lgpd_checks)
        
        # Verificar inventário de dados
        if 'data_inventory' in config and config['data_inventory']:
            results['data_inventory'] = True
        
        # Calcular score
        checks = [
            results['objectives_defined'],
            len(results['success_metrics']) >= 3,
            results['timeline_defined'],
            results['lgpd_compliance'],
            results['data_inventory']
        ]
        results['score'] = (sum(checks) / len(checks)) * 100
        
        # Red flags
        if results['score'] < 80:
            self.red_flags.append("Fase de planejamento incompleta")
        
        return results
    
    def audit_data_preparation(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Auditar preparação dos dados"""
        self.logger.info("Auditando preparação dos dados...")
        
        results = {
            'data_quality': 0,
            'preprocessing_documented': False,
            'data_splits_valid': False,
            'bias_analysis': False,
            'score': 0
        }
        
        # Verificar qualidade dos dados
        if 'data_quality_report' in config:
            quality_report = config['data_quality_report']
            quality_score = quality_report.get('overall_score', 0)
            results['data_quality'] = quality_score
            
            # Red flags para qualidade
            if quality_score < 0.7:
                self.red_flags.append("Qualidade dos dados abaixo do esperado")
        
        # Verificar documentação de pré-processamento
        if 'preprocessing_steps' in config and config['preprocessing_steps']:
            results['preprocessing_documented'] = True
        
        # Verificar divisão de dados
        if 'data_splits' in config:
            splits = config['data_splits']
            train_size = splits.get('train_size', 0)
            val_size = splits.get('val_size', 0)
            test_size = splits.get('test_size', 0)
            
            # Validar proporções
            if abs(train_size + val_size + test_size - 1.0) < 0.01:
                results['data_splits_valid'] = True
            else:
                self.red_flags.append("Divisão de dados inválida")
        
        # Verificar análise de vieses
        if 'bias_analysis' in config and config['bias_analysis']:
            results['bias_analysis'] = True
        
        # Calcular score
        checks = [
            results['data_quality'] >= 0.7,
            results['preprocessing_documented'],
            results['data_splits_valid'],
            results['bias_analysis']
        ]
        results['score'] = (sum(checks) / len(checks)) * 100
        
        return results
    
    def audit_model_selection(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Auditar seleção de modelo"""
        self.logger.info("Auditando seleção de modelo...")
        
        results = {
            'model_justification': False,
            'hyperparameter_tuning': False,
            'baseline_established': False,
            'cross_validation': False,
            'score': 0
        }
        
        # Verificar justificativa do modelo
        if 'model_selection' in config:
            model_info = config['model_selection']
            if 'justification' in model_info and model_info['justification']:
                results['model_justification'] = True
        
        # Verificar tuning de hiperparâmetros
        if 'hyperparameter_tuning' in config and config['hyperparameter_tuning']:
            results['hyperparameter_tuning'] = True
        
        # Verificar baseline
        if 'baseline_performance' in config and config['baseline_performance']:
            results['baseline_established'] = True
        
        # Verificar validação cruzada
        if 'cross_validation' in config and config['cross_validation']:
            cv_config = config['cross_validation']
            if cv_config.get('cv_folds', 0) >= 5:
                results['cross_validation'] = True
        
        # Calcular score
        checks = [
            results['model_justification'],
            results['hyperparameter_tuning'],
            results['baseline_established'],
            results['cross_validation']
        ]
        results['score'] = (sum(checks) / len(checks)) * 100
        
        return results
    
    def audit_training_phase(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Auditar fase de treinamento"""
        self.logger.info("Auditando fase de treinamento...")
        
        results = {
            'environment_isolated': False,
            'training_logs': False,
            'checkpoints_saved': False,
            'overfitting_detected': False,
            'score': 0
        }
        
        # Verificar ambiente isolado
        if 'training_environment' in config:
            env_config = config['training_environment']
            if env_config.get('isolated', False):
                results['environment_isolated'] = True
        
        # Verificar logs de treinamento
        if 'training_logs' in config and config['training_logs']:
            results['training_logs'] = True
        
        # Verificar checkpoints
        if 'checkpoints' in config and config['checkpoints']:
            results['checkpoints_saved'] = True
        
        # Verificar overfitting
        if 'training_metrics' in config:
            metrics = config['training_metrics']
            train_acc = metrics.get('train_accuracy', 0)
            val_acc = metrics.get('val_accuracy', 0)
            
            # Detectar overfitting (diferença > 10%)
            if abs(train_acc - val_acc) > 0.1:
                self.red_flags.append("Overfitting detectado no treinamento")
                results['overfitting_detected'] = True
        
        # Calcular score
        checks = [
            results['environment_isolated'],
            results['training_logs'],
            results['checkpoints_saved'],
            not results['overfitting_detected']
        ]
        results['score'] = (sum(checks) / len(checks)) * 100
        
        return results
    
    def audit_evaluation_phase(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Auditar fase de avaliação"""
        self.logger.info("Auditando fase de avaliação...")
        
        results = {
            'test_set_unused': True,
            'metrics_comprehensive': False,
            'robustness_tested': False,
            'performance_adequate': False,
            'score': 0
        }
        
        # Verificar se conjunto de teste não foi usado no treinamento
        if 'data_leakage_check' in config and config['data_leakage_check']:
            results['test_set_unused'] = True
        else:
            self.red_flags.append("Possível vazamento de dados - conjunto de teste pode ter sido usado")
        
        # Verificar métricas abrangentes
        if 'evaluation_metrics' in config:
            metrics = config['evaluation_metrics']
            required_metrics = ['accuracy', 'precision', 'recall', 'f1']
            if all(metric in metrics for metric in required_metrics):
                results['metrics_comprehensive'] = True
        
        # Verificar testes de robustez
        if 'robustness_tests' in config and config['robustness_tests']:
            results['robustness_tested'] = True
        
        # Verificar performance adequada
        if 'performance_metrics' in config:
            perf = config['performance_metrics']
            if perf.get('accuracy', 0) >= 0.8:  # Threshold mínimo
                results['performance_adequate'] = True
            else:
                self.red_flags.append("Performance do modelo abaixo do threshold mínimo")
        
        # Calcular score
        checks = [
            results['test_set_unused'],
            results['metrics_comprehensive'],
            results['robustness_tested'],
            results['performance_adequate']
        ]
        results['score'] = (sum(checks) / len(checks)) * 100
        
        return results
    
    def audit_interpretability(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Auditar interpretabilidade"""
        self.logger.info("Auditando interpretabilidade...")
        
        results = {
            'feature_importance': False,
            'model_explanations': False,
            'bias_analysis': False,
            'transparency_documented': False,
            'score': 0
        }
        
        # Verificar análise de importância das features
        if 'feature_importance' in config and config['feature_importance']:
            results['feature_importance'] = True
        
        # Verificar explicações do modelo
        if 'model_explanations' in config and config['model_explanations']:
            results['model_explanations'] = True
        
        # Verificar análise de vieses
        if 'bias_analysis' in config and config['bias_analysis']:
            results['bias_analysis'] = True
        
        # Verificar documentação de transparência
        if 'transparency_documentation' in config and config['transparency_documentation']:
            results['transparency_documented'] = True
        
        # Calcular score
        checks = [
            results['feature_importance'],
            results['model_explanations'],
            results['bias_analysis'],
            results['transparency_documented']
        ]
        results['score'] = (sum(checks) / len(checks)) * 100
        
        return results
    
    def audit_deployment_readiness(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Auditar preparação para deployment"""
        self.logger.info("Auditando preparação para deployment...")
        
        results = {
            'model_versioned': False,
            'api_documented': False,
            'monitoring_configured': False,
            'rollback_plan': False,
            'score': 0
        }
        
        # Verificar versionamento do modelo
        if 'model_versioning' in config and config['model_versioning']:
            results['model_versioned'] = True
        
        # Verificar documentação da API
        if 'api_documentation' in config and config['api_documentation']:
            results['api_documented'] = True
        
        # Verificar monitoramento
        if 'monitoring_config' in config and config['monitoring_config']:
            results['monitoring_configured'] = True
        
        # Verificar plano de rollback
        if 'rollback_plan' in config and config['rollback_plan']:
            results['rollback_plan'] = True
        
        # Calcular score
        checks = [
            results['model_versioned'],
            results['api_documented'],
            results['monitoring_configured'],
            results['rollback_plan']
        ]
        results['score'] = (sum(checks) / len(checks)) * 100
        
        return results
    
    def audit_governance(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Auditar governança"""
        self.logger.info("Auditando governança...")
        
        results = {
            'documentation_complete': False,
            'peer_review': False,
            'stakeholder_approval': False,
            'compliance_certified': False,
            'score': 0
        }
        
        # Verificar documentação completa
        required_docs = [
            'technical_documentation',
            'experiment_report',
            'design_decisions',
            'lessons_learned'
        ]
        
        docs_present = sum(1 for doc in required_docs if doc in config and config[doc])
        results['documentation_complete'] = docs_present >= 3
        
        # Verificar revisão por pares
        if 'peer_review' in config and config['peer_review']:
            results['peer_review'] = True
        
        # Verificar aprovação de stakeholders
        if 'stakeholder_approval' in config and config['stakeholder_approval']:
            results['stakeholder_approval'] = True
        
        # Verificar certificação de compliance
        if 'compliance_certification' in config and config['compliance_certification']:
            results['compliance_certified'] = True
        
        # Calcular score
        checks = [
            results['documentation_complete'],
            results['peer_review'],
            results['stakeholder_approval'],
            results['compliance_certified']
        ]
        results['score'] = (sum(checks) / len(checks)) * 100
        
        return results
    
    def _calculate_overall_score(self) -> float:
        """Calcular score geral do projeto"""
        if 'phases' not in self.audit_results:
            return 0.0
            
        phase_scores = []
        for phase_name, phase_results in self.audit_results['phases'].items():
            if isinstance(phase_results, dict) and 'score' in phase_results:
                phase_scores.append(phase_results['score'])
        
        if phase_scores:
            return sum(phase_scores) / len(phase_scores)
        return 0.0
    
    def _generate_recommendation(self, overall_score: float) -> str:
        """Gerar recomendação baseada no score geral"""
        
        if overall_score >= 90:
            return "APROVADO - Projeto atende todos os critérios de qualidade"
        elif overall_score >= 80:
            return "APROVADO COM RESSALVAS - Resolver red flags identificados"
        elif overall_score >= 70:
            return "REJEITADO - Necessárias correções significativas"
        else:
            return "REJEITADO - Projeto não atende critérios mínimos"
    
    def _generate_audit_report(self):
        """Gerar relatório de auditoria"""
        report_content = f"""# Relatório de Auditoria - Treinamento de IA

## Informações do Projeto
- **Nome**: {self.project_name}
- **Data da Auditoria**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Auditor**: Sistema Automatizado AR Online

## Resumo Executivo
- **Status**: {self.audit_results['recommendation']}
- **Score Geral**: {self.audit_results['overall_score']:.1f}/100
- **Red Flags**: {len(self.red_flags)} problemas críticos identificados

## Detalhamento por Fase

"""
        
        for phase_name, phase_results in self.audit_results['phases'].items():
            phase_score = phase_results.get('score', 0)
            status = "✅" if phase_score >= 80 else "❌" if phase_score >= 60 else "🚨"
            
            report_content += f"### {phase_name.replace('_', ' ').title()} {status}\n"
            report_content += f"- **Score**: {phase_score:.1f}/100\n"
            
            # Detalhar itens verificados
            for key, value in phase_results.items():
                if key != 'score':
                    status_icon = "✅" if value else "❌"
                    report_content += f"- {key.replace('_', ' ').title()}: {status_icon}\n"
            
            report_content += "\n"
        
        # Red Flags
        if self.red_flags:
            report_content += "## 🚨 Red Flags Identificados\n\n"
            for i, flag in enumerate(self.red_flags, 1):
                report_content += f"{i}. {flag}\n"
            report_content += "\n"
        
        # Recomendações
        report_content += "## 📋 Recomendações\n\n"
        if self.red_flags:
            report_content += "### Ações Imediatas\n"
            for flag in self.red_flags:
                report_content += f"- Resolver: {flag}\n"
            report_content += "\n"
        
        report_content += "### Próximos Passos\n"
        if self.audit_results['overall_score'] >= 80:
            report_content += "- Projeto aprovado para produção\n"
            report_content += "- Implementar monitoramento contínuo\n"
        else:
            report_content += "- Implementar ações corretivas\n"
            report_content += "- Re-executar auditoria após correções\n"
        
        report_content += f"""
## Aprovação
- **Data**: {datetime.now().strftime('%Y-%m-%d')}
- **Status Final**: {self.audit_results['recommendation']}
- **Score Final**: {self.audit_results['overall_score']:.1f}/100

---
*Relatório gerado automaticamente pelo Sistema de Auditoria AR Online*
"""
        
        # Salvar relatório
        filename = f"audit_report_{self.project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        self.logger.info(f"Relatório de auditoria salvo: {filename}")
        return filename

def main():
    """Função principal para demonstrar o auditor"""
    print("SISTEMA DE AUDITORIA DE TREINAMENTO DE IA - AR ONLINE")
    print("=" * 60)
    
    # Exemplo de configuração de projeto
    example_config = {
        'objectives': {
            'metrics': ['accuracy', 'precision', 'recall', 'f1']
        },
        'timeline': {
            'start_date': '2025-01-01',
            'end_date': '2025-01-31'
        },
        'personal_data_mapping': {
            'columns': ['email', 'telefone'],
            'count': 2
        },
        'legal_basis': 'consentimento',
        'data_quality_report': {
            'overall_score': 0.85
        },
        'preprocessing_steps': ['remove_duplicates', 'handle_missing'],
        'data_splits': {
            'train_size': 0.7,
            'val_size': 0.15,
            'test_size': 0.15
        },
        'model_selection': {
            'justification': 'Random Forest escolhido por interpretabilidade'
        },
        'hyperparameter_tuning': True,
        'baseline_performance': 0.75,
        'cross_validation': {
            'cv_folds': 5
        },
        'training_environment': {
            'isolated': True
        },
        'training_logs': True,
        'checkpoints': True,
        'training_metrics': {
            'train_accuracy': 0.95,
            'val_accuracy': 0.88
        },
        'data_leakage_check': True,
        'evaluation_metrics': {
            'accuracy': 0.88,
            'precision': 0.87,
            'recall': 0.89,
            'f1': 0.88
        },
        'performance_metrics': {
            'accuracy': 0.88
        },
        'feature_importance': True,
        'model_explanations': True,
        'model_versioning': True,
        'api_documentation': True,
        'monitoring_config': True,
        'rollback_plan': True,
        'technical_documentation': True,
        'experiment_report': True,
        'design_decisions': True,
        'peer_review': True,
        'stakeholder_approval': True,
        'compliance_certification': True
    }
    
    # Executar auditoria
    auditor = AITrainingAuditor("Projeto_Exemplo")
    results = auditor.run_complete_audit(example_config)
    
    print(f"\nScore Geral: {results['overall_score']:.1f}/100")
    print(f"Recomendação: {results['recommendation']}")
    print(f"Red Flags: {len(results['red_flags'])}")

if __name__ == "__main__":
    main()
