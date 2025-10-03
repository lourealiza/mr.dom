"""
Sistema de Analytics e Logs para testes
"""
import json
import csv
from datetime import datetime, timedelta
from typing import Dict, Any, List
from pathlib import Path

class TestAnalytics:
    """Sistema de analytics para testes da trilha"""
    
    def __init__(self, output_dir: str = "test_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.events = []
        self.conversations = []
        self.leads = []
        self.meetings = []
        self.followups = []
        
    def log_event(self, event_type: str, properties: Dict[str, Any], user_id: str = None):
        """Log de evento"""
        event = {
            "id": f"evt_{len(self.events) + 1}",
            "event_type": event_type,
            "properties": properties,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "session_id": properties.get("session_id", "default")
        }
        self.events.append(event)
        
    def log_conversation(self, conversation_data: Dict[str, Any]):
        """Log de conversa"""
        conversation = {
            "id": f"conv_{len(self.conversations) + 1}",
            "timestamp": datetime.now().isoformat(),
            **conversation_data
        }
        self.conversations.append(conversation)
        
    def log_lead(self, lead_data: Dict[str, Any]):
        """Log de lead"""
        lead = {
            "id": f"lead_{len(self.leads) + 1}",
            "timestamp": datetime.now().isoformat(),
            **lead_data
        }
        self.leads.append(lead)
        
    def log_meeting(self, meeting_data: Dict[str, Any]):
        """Log de reunião"""
        meeting = {
            "id": f"meeting_{len(self.meetings) + 1}",
            "timestamp": datetime.now().isoformat(),
            **meeting_data
        }
        self.meetings.append(meeting)
        
    def log_followup(self, followup_data: Dict[str, Any]):
        """Log de follow-up"""
        followup = {
            "id": f"followup_{len(self.followups) + 1}",
            "timestamp": datetime.now().isoformat(),
            **followup_data
        }
        self.followups.append(followup)
    
    def generate_report(self) -> Dict[str, Any]:
        """Gera relatório completo dos testes"""
        report = {
            "summary": self._generate_summary(),
            "conversion_funnel": self._analyze_conversion_funnel(),
            "channel_performance": self._analyze_channel_performance(),
            "error_analysis": self._analyze_errors(),
            "timing_analysis": self._analyze_timing(),
            "recommendations": self._generate_recommendations()
        }
        
        return report
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Gera resumo dos testes"""
        total_conversations = len(self.conversations)
        total_leads = len(self.leads)
        total_meetings = len(self.meetings)
        total_followups = len(self.followups)
        
        conversion_rate = (total_meetings / total_conversations * 100) if total_conversations > 0 else 0
        lead_rate = (total_leads / total_conversations * 100) if total_conversations > 0 else 0
        
        return {
            "total_conversations": total_conversations,
            "total_leads": total_leads,
            "total_meetings": total_meetings,
            "total_followups": total_followups,
            "conversion_rate": round(conversion_rate, 2),
            "lead_rate": round(lead_rate, 2),
            "test_duration": self._calculate_test_duration()
        }
    
    def _analyze_conversion_funnel(self) -> Dict[str, Any]:
        """Analisa funil de conversão"""
        # Agrupar por origem
        origins = {}
        for conv in self.conversations:
            origin = conv.get("origem", "unknown")
            if origin not in origins:
                origins[origin] = {"conversations": 0, "leads": 0, "meetings": 0}
            origins[origin]["conversations"] += 1
        
        # Contar leads por origem
        for lead in self.leads:
            origin = lead.get("origem", "unknown")
            if origin in origins:
                origins[origin]["leads"] += 1
        
        # Contar meetings por origem
        for meeting in self.meetings:
            origin = meeting.get("origem", "unknown")
            if origin in origins:
                origins[origin]["meetings"] += 1
        
        # Calcular taxas
        for origin, data in origins.items():
            if data["conversations"] > 0:
                data["lead_rate"] = round(data["leads"] / data["conversations"] * 100, 2)
                data["conversion_rate"] = round(data["meetings"] / data["conversations"] * 100, 2)
            else:
                data["lead_rate"] = 0
                data["conversion_rate"] = 0
        
        return origins
    
    def _analyze_channel_performance(self) -> Dict[str, Any]:
        """Analisa performance por canal"""
        channels = {}
        
        for conv in self.conversations:
            channel = conv.get("canal", "unknown")
            if channel not in channels:
                channels[channel] = {
                    "conversations": 0,
                    "avg_response_time": 0,
                    "completion_rate": 0,
                    "errors": 0
                }
            channels[channel]["conversations"] += 1
        
        # Calcular métricas por canal
        for channel, data in channels.items():
            channel_convs = [c for c in self.conversations if c.get("canal") == channel]
            completed_convs = [c for c in channel_convs if c.get("status") == "completed"]
            
            data["completion_rate"] = round(len(completed_convs) / len(channel_convs) * 100, 2) if channel_convs else 0
            
            # Calcular tempo médio de resposta (simulado)
            data["avg_response_time"] = round(sum(c.get("response_time", 2) for c in channel_convs) / len(channel_convs), 2) if channel_convs else 0
        
        return channels
    
    def _analyze_errors(self) -> Dict[str, Any]:
        """Analisa erros encontrados"""
        errors = []
        
        # Analisar eventos de erro
        error_events = [e for e in self.events if "error" in e["event_type"].lower()]
        
        for event in error_events:
            errors.append({
                "type": event["event_type"],
                "message": event["properties"].get("message", ""),
                "timestamp": event["timestamp"],
                "user_id": event["user_id"]
            })
        
        # Agrupar por tipo de erro
        error_types = {}
        for error in errors:
            error_type = error["type"]
            if error_type not in error_types:
                error_types[error_type] = 0
            error_types[error_type] += 1
        
        return {
            "total_errors": len(errors),
            "error_types": error_types,
            "error_details": errors
        }
    
    def _analyze_timing(self) -> Dict[str, Any]:
        """Analisa timing dos testes"""
        if not self.conversations:
            return {}
        
        # Calcular duração média das conversas
        durations = []
        for conv in self.conversations:
            if "start_time" in conv and "end_time" in conv:
                start = datetime.fromisoformat(conv["start_time"])
                end = datetime.fromisoformat(conv["end_time"])
                duration = (end - start).total_seconds()
                durations.append(duration)
        
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            "avg_conversation_duration": round(avg_duration, 2),
            "total_test_duration": self._calculate_test_duration(),
            "peak_hours": self._find_peak_hours()
        }
    
    def _calculate_test_duration(self) -> str:
        """Calcula duração total dos testes"""
        if not self.events:
            return "0s"
        
        start_time = min(datetime.fromisoformat(e["timestamp"]) for e in self.events)
        end_time = max(datetime.fromisoformat(e["timestamp"]) for e in self.events)
        duration = end_time - start_time
        
        return str(duration)
    
    def _find_peak_hours(self) -> List[str]:
        """Encontra horários de pico"""
        hours = {}
        for event in self.events:
            hour = datetime.fromisoformat(event["timestamp"]).hour
            hours[hour] = hours.get(hour, 0) + 1
        
        # Retornar top 3 horários
        sorted_hours = sorted(hours.items(), key=lambda x: x[1], reverse=True)
        return [f"{hour}:00" for hour, _ in sorted_hours[:3]]
    
    def _generate_recommendations(self) -> List[str]:
        """Gera recomendações baseadas nos dados"""
        recommendations = []
        
        summary = self._generate_summary()
        funnel = self._analyze_conversion_funnel()
        channels = self._analyze_channel_performance()
        errors = self._analyze_errors()
        
        # Recomendações baseadas na taxa de conversão
        if summary["conversion_rate"] < 80:
            recommendations.append("Taxa de conversão abaixo de 80%. Revisar fluxo de qualificação.")
        
        # Recomendações baseadas em canais
        for channel, data in channels.items():
            if data["completion_rate"] < 70:
                recommendations.append(f"Canal {channel} com baixa taxa de conclusão ({data['completion_rate']}%).")
        
        # Recomendações baseadas em erros
        if errors["total_errors"] > 0:
            recommendations.append(f"Encontrados {errors['total_errors']} erros. Revisar logs de erro.")
        
        # Recomendações baseadas no funil
        for origin, data in funnel.items():
            if data["lead_rate"] < 50:
                recommendations.append(f"Origem {origin} com baixa taxa de leads ({data['lead_rate']}%).")
        
        return recommendations
    
    def export_results(self, format: str = "json") -> str:
        """Exporta resultados em diferentes formatos"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == "json":
            filename = f"test_results_{timestamp}.json"
            filepath = self.output_dir / filename
            
            results = {
                "report": self.generate_report(),
                "raw_data": {
                    "events": self.events,
                    "conversations": self.conversations,
                    "leads": self.leads,
                    "meetings": self.meetings,
                    "followups": self.followups
                }
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            return str(filepath)
        
        elif format == "csv":
            filename = f"test_results_{timestamp}.csv"
            filepath = self.output_dir / filename
            
            # Preparar dados para CSV
            csv_data = []
            for conv in self.conversations:
                csv_data.append({
                    "conversation_id": conv["id"],
                    "origem": conv.get("origem", ""),
                    "canal": conv.get("canal", ""),
                    "status": conv.get("status", ""),
                    "timestamp": conv["timestamp"]
                })
            
            if csv_data:
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
                    writer.writeheader()
                    writer.writerows(csv_data)
            
            return str(filepath)
        
        else:
            raise ValueError(f"Formato {format} não suportado")
    
    def create_bug_report(self, bug_data: Dict[str, Any]) -> str:
        """Cria relatório de bug"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"bug_report_{timestamp}.md"
        filepath = self.output_dir / filename
        
        bug_report = f"""# Bug Report - {bug_data.get('titulo', 'Bug não especificado')}

## Informações Gerais
- **Data/Hora**: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
- **Severidade**: {bug_data.get('severidade', 'Não especificada')}
- **Área**: {bug_data.get('area', 'Não especificada')}

## Descrição
{bug_data.get('descricao', 'Descrição não fornecida')}

## Etapas para Reproduzir
{bug_data.get('etapas', 'Etapas não fornecidas')}

## Comportamento Esperado
{bug_data.get('esperado', 'Comportamento esperado não especificado')}

## Comportamento Obtido
{bug_data.get('obtido', 'Comportamento obtido não especificado')}

## Ambiente
- **Canal**: {bug_data.get('canal', 'Não especificado')}
- **Data/Hora**: {bug_data.get('data_hora', 'Não especificada')}
- **Versão do Fluxo**: {bug_data.get('versao_fluxo', 'Não especificada')}

## Evidências
{bug_data.get('evidencias', 'Evidências não fornecidas')}

## Logs Relacionados
```json
{json.dumps(bug_data.get('logs', {}), indent=2)}
```

## Status
- [ ] Confirmado
- [ ] Em investigação
- [ ] Corrigido
- [ ] Testado
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(bug_report)
        
        return str(filepath)

# Instância global para uso nos testes
test_analytics = TestAnalytics()
