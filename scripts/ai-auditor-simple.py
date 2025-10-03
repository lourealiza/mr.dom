#!/usr/bin/env python3
"""
Auditor Simples de Treinamento de IA - AR Online
Demonstração do sistema de auditoria
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any

class SimpleAIAuditor:
    """Auditor simplificado para demonstração"""
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.audit_results = {}
        self.red_flags = []
    
    def run_audit(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Executar auditoria simplificada"""
        print(f"Iniciando auditoria do projeto: {self.project_name}")
        
        # Fase 1: Planejamento
        planning_score = self._audit_planning(config)
        
        # Fase 2: Dados
        data_score = self._audit_data(config)
        
        # Fase 3: Modelo
        model_score = self._audit_model(config)
        
        # Fase 4: Treinamento
        training_score = self._audit_training(config)
        
        # Fase 5: Avaliação
        evaluation_score = self._audit_evaluation(config)
        
        # Consolidar resultados
        phase_scores = [planning_score, data_score, model_score, training_score, evaluation_score]
        overall_score = sum(phase_scores) / len(phase_scores)
        
        self.audit_results = {
            'project_name': self.project_name,
            'audit_date': datetime.now().isoformat(),
            'phase_scores': {
                'planning': planning_score,
                'data': data_score,
                'model': model_score,
                'training': training_score,
                'evaluation': evaluation_score
            },
            'overall_score': overall_score,
            'red_flags': self.red_flags,
            'recommendation': self._get_recommendation(overall_score)
        }
        
        return self.audit_results
    
    def _audit_planning(self, config: Dict[str, Any]) -> float:
        """Auditar fase de planejamento"""
        score = 0
        checks = 0
        
        # Verificar objetivos
        if 'objectives' in config and config['objectives']:
            score += 20
        checks += 1
        
        # Verificar timeline
        if 'timeline' in config and config['timeline']:
            score += 20
        checks += 1
        
        # Verificar compliance LGPD
        lgpd_items = ['personal_data_mapping', 'legal_basis', 'consent_records']
        lgpd_count = sum(1 for item in lgpd_items if item in config)
        score += (lgpd_count / len(lgpd_items)) * 20
        checks += 1
        
        # Verificar inventário de dados
        if 'data_inventory' in config and config['data_inventory']:
            score += 20
        checks += 1
        
        # Verificar métricas de sucesso
        if 'objectives' in config and 'metrics' in config['objectives']:
            metrics = config['objectives']['metrics']
            if len(metrics) >= 3:
                score += 20
        checks += 1
        
        return (score / checks) if checks > 0 else 0
    
    def _audit_data(self, config: Dict[str, Any]) -> float:
        """Auditar preparação dos dados"""
        score = 0
        checks = 0
        
        # Verificar qualidade dos dados
        if 'data_quality_report' in config:
            quality_score = config['data_quality_report'].get('overall_score', 0)
            if quality_score >= 0.7:
                score += 25
            else:
                self.red_flags.append("Qualidade dos dados abaixo do esperado")
        checks += 1
        
        # Verificar pré-processamento
        if 'preprocessing_steps' in config and config['preprocessing_steps']:
            score += 25
        checks += 1
        
        # Verificar divisão de dados
        if 'data_splits' in config:
            splits = config['data_splits']
            total = splits.get('train_size', 0) + splits.get('val_size', 0) + splits.get('test_size', 0)
            if abs(total - 1.0) < 0.01:
                score += 25
            else:
                self.red_flags.append("Divisão de dados inválida")
        checks += 1
        
        # Verificar análise de vieses
        if 'bias_analysis' in config and config['bias_analysis']:
            score += 25
        checks += 1
        
        return (score / checks) if checks > 0 else 0
    
    def _audit_model(self, config: Dict[str, Any]) -> float:
        """Auditar seleção de modelo"""
        score = 0
        checks = 0
        
        # Verificar justificativa
        if 'model_selection' in config and 'justification' in config['model_selection']:
            score += 25
        checks += 1
        
        # Verificar tuning de hiperparâmetros
        if 'hyperparameter_tuning' in config and config['hyperparameter_tuning']:
            score += 25
        checks += 1
        
        # Verificar baseline
        if 'baseline_performance' in config and config['baseline_performance']:
            score += 25
        checks += 1
        
        # Verificar validação cruzada
        if 'cross_validation' in config and config['cross_validation']:
            cv_folds = config['cross_validation'].get('cv_folds', 0)
            if cv_folds >= 5:
                score += 25
        checks += 1
        
        return (score / checks) if checks > 0 else 0
    
    def _audit_training(self, config: Dict[str, Any]) -> float:
        """Auditar fase de treinamento"""
        score = 0
        checks = 0
        
        # Verificar ambiente isolado
        if 'training_environment' in config and config['training_environment'].get('isolated', False):
            score += 25
        checks += 1
        
        # Verificar logs
        if 'training_logs' in config and config['training_logs']:
            score += 25
        checks += 1
        
        # Verificar checkpoints
        if 'checkpoints' in config and config['checkpoints']:
            score += 25
        checks += 1
        
        # Verificar overfitting
        if 'training_metrics' in config:
            metrics = config['training_metrics']
            train_acc = metrics.get('train_accuracy', 0)
            val_acc = metrics.get('val_accuracy', 0)
            if abs(train_acc - val_acc) <= 0.1:
                score += 25
            else:
                self.red_flags.append("Overfitting detectado")
        checks += 1
        
        return (score / checks) if checks > 0 else 0
    
    def _audit_evaluation(self, config: Dict[str, Any]) -> float:
        """Auditar fase de avaliação"""
        score = 0
        checks = 0
        
        # Verificar ausência de vazamento
        if 'data_leakage_check' in config and config['data_leakage_check']:
            score += 25
        else:
            self.red_flags.append("Possível vazamento de dados")
        checks += 1
        
        # Verificar métricas abrangentes
        if 'evaluation_metrics' in config:
            metrics = config['evaluation_metrics']
            required = ['accuracy', 'precision', 'recall', 'f1']
            if all(metric in metrics for metric in required):
                score += 25
        checks += 1
        
        # Verificar testes de robustez
        if 'robustness_tests' in config and config['robustness_tests']:
            score += 25
        checks += 1
        
        # Verificar performance adequada
        if 'performance_metrics' in config:
            perf = config['performance_metrics']
            if perf.get('accuracy', 0) >= 0.8:
                score += 25
            else:
                self.red_flags.append("Performance abaixo do threshold")
        checks += 1
        
        return (score / checks) if checks > 0 else 0
    
    def _get_recommendation(self, score: float) -> str:
        """Gerar recomendação baseada no score"""
        if score >= 90:
            return "APROVADO - Projeto atende todos os critérios"
        elif score >= 80:
            return "APROVADO COM RESSALVAS - Resolver red flags"
        elif score >= 70:
            return "REJEITADO - Correções significativas necessárias"
        else:
            return "REJEITADO - Projeto não atende critérios mínimos"
    
    def print_results(self):
        """Imprimir resultados da auditoria"""
        print(f"\n{'='*60}")
        print(f"RESULTADOS DA AUDITORIA - {self.project_name}")
        print(f"{'='*60}")
        
        print(f"Score Geral: {self.audit_results['overall_score']:.1f}/100")
        print(f"Recomendação: {self.audit_results['recommendation']}")
        
        print(f"\nScores por Fase:")
        for phase, score in self.audit_results['phase_scores'].items():
            status = "OK" if score >= 80 else "ERRO" if score >= 60 else "CRITICO"
            print(f"  {phase.title()}: {score:.1f}/100 {status}")
        
        if self.red_flags:
            print(f"\nRED FLAGS ({len(self.red_flags)}):")
            for i, flag in enumerate(self.red_flags, 1):
                print(f"  {i}. {flag}")
        else:
            print(f"\nOK: Nenhum red flag identificado")

def main():
    """Função principal para demonstração"""
    print("SISTEMA DE AUDITORIA DE TREINAMENTO DE IA - AR ONLINE")
    print("=" * 60)
    
    # Configuração de exemplo
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
        'robustness_tests': True
    }
    
    # Executar auditoria
    auditor = SimpleAIAuditor("Projeto_Exemplo")
    results = auditor.run_audit(example_config)
    
    # Imprimir resultados
    auditor.print_results()
    
    # Salvar relatório
    report_file = f"audit_report_{auditor.project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Relatório salvo: {report_file}")

if __name__ == "__main__":
    main()
