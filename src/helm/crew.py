from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.tools import BaseTool
from typing import List
import subprocess
import json
import yaml
import os
import requests
from datetime import datetime, timedelta

# Custom Tools for Kubernetes Log Analysis
class KubernetesLogCollectorTool(BaseTool):
    name: str = "Kubernetes Log Collector"
    description: str = "Collect logs from Kubernetes pods across the entire cluster"

    def _run(self, namespaces: str = "ALL_NAMESPACES", since: str = "1h") -> str:
        """Collect logs from Kubernetes cluster"""
        try:
            all_logs = []
            
            # If ALL_NAMESPACES, get all namespaces first
            if namespaces == "ALL_NAMESPACES":
                # Get all namespaces
                ns_cmd = "kubectl get namespaces -o name"
                ns_result = subprocess.run(ns_cmd.split(), capture_output=True, text=True, timeout=30)
                
                if ns_result.returncode != 0:
                    return f"Error getting namespaces: {ns_result.stderr}"
                
                namespace_list = [ns.replace('namespace/', '') for ns in ns_result.stdout.strip().split('\n') if ns.strip()]
                all_logs.append(f"=== SCANNING {len(namespace_list)} NAMESPACES ===")
                
                # Limit to important namespaces to avoid timeout
                priority_namespaces = []
                for ns in namespace_list:
                    if any(important in ns.lower() for important in ['default', 'kube-system', 'monitoring', 'logging', 'ingress', 'cert-manager', 'prometheus', 'grafana']):
                        priority_namespaces.append(ns)
                
                # Add some other namespaces if we have few priority ones
                if len(priority_namespaces) < 5:
                    for ns in namespace_list:
                        if ns not in priority_namespaces and not ns.startswith('kube-'):
                            priority_namespaces.append(ns)
                            if len(priority_namespaces) >= 8:  # Limit to 8 namespaces
                                break
                
                namespaces_to_check = priority_namespaces[:8]  # Max 8 namespaces
                all_logs.append(f"=== PRIORITY NAMESPACES: {', '.join(namespaces_to_check)} ===\n")
            else:
                # Use specified namespaces
                namespaces_to_check = [ns.strip() for ns in namespaces.split(',')]
            
            total_pods_checked = 0
            
            for namespace in namespaces_to_check:
                try:
                    # Get pods in this namespace
                    cmd = f"kubectl get pods -n {namespace} -o name"
                    result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=20)
                    
                    if result.returncode != 0:
                        all_logs.append(f"=== NAMESPACE {namespace}: Error getting pods ===")
                        continue
                    
                    pods = [p.strip() for p in result.stdout.strip().split('\n') if p.strip()]
                    
                    if not pods:
                        all_logs.append(f"=== NAMESPACE {namespace}: No pods found ===")
                        continue
                    
                    all_logs.append(f"=== NAMESPACE {namespace}: Found {len(pods)} pods ===")
                    
                    # Get logs from first 2-3 pods per namespace
                    pods_to_check = pods[:3]
                    total_pods_checked += len(pods_to_check)
                    
                    for pod in pods_to_check:
                        if pod:
                            pod_name = pod.replace('pod/', '')
                            log_cmd = f"kubectl logs {pod_name} -n {namespace} --since={since} --tail=20"
                            log_result = subprocess.run(log_cmd.split(), capture_output=True, text=True, timeout=10)
                            
                            if log_result.stdout:
                                # Look for errors, warnings, or interesting content
                                log_content = log_result.stdout[:400]  # Limit content
                                if any(keyword in log_content.lower() for keyword in ['error', 'warn', 'fail', 'exception', 'crash', 'restart']):
                                    all_logs.append(f"--- {namespace}/{pod_name} (ISSUES FOUND) ---")
                                    all_logs.append(log_content)
                                elif len(log_content.strip()) > 10:
                                    all_logs.append(f"--- {namespace}/{pod_name} (Normal) ---")
                                    all_logs.append(log_content[:200] + "...")
                            elif log_result.stderr:
                                all_logs.append(f"--- {namespace}/{pod_name} (ERROR) ---")
                                all_logs.append(log_result.stderr[:200])
                            
                except subprocess.TimeoutExpired:
                    all_logs.append(f"=== NAMESPACE {namespace}: Timeout ===")
                    continue
                except Exception as e:
                    all_logs.append(f"=== NAMESPACE {namespace}: Error: {str(e)} ===")
                    continue
            
            summary = f"=== CLUSTER SCAN SUMMARY ===\n"
            summary += f"Namespaces scanned: {len(namespaces_to_check)}\n"
            summary += f"Total pods checked: {total_pods_checked}\n"
            summary += f"Time range: {since}\n"
            summary += f"Scan completed at: {datetime.now().strftime('%H:%M:%S')}\n\n"
            
            return summary + "\n".join(all_logs) if all_logs else "No logs collected from cluster"
            
        except Exception as e:
            return f"Error collecting cluster logs: {str(e)}"

class ClusterInfoTool(BaseTool):
    name: str = "Cluster Info Collector"
    description: str = "Get overall cluster information and status"

    def _run(self, info_type: str = "overview") -> str:
        """Get cluster overview information"""
        try:
            cluster_info = []
            
            # Get cluster info
            try:
                info_cmd = "kubectl cluster-info"
                info_result = subprocess.run(info_cmd.split(), capture_output=True, text=True, timeout=15)
                if info_result.returncode == 0:
                    cluster_info.append("=== CLUSTER INFO ===")
                    cluster_info.append(info_result.stdout[:300])
            except:
                pass
            
            # Get node status
            try:
                nodes_cmd = "kubectl get nodes -o wide"
                nodes_result = subprocess.run(nodes_cmd.split(), capture_output=True, text=True, timeout=15)
                if nodes_result.returncode == 0:
                    cluster_info.append("\n=== NODE STATUS ===")
                    cluster_info.append(nodes_result.stdout)
            except:
                pass
            
            # Get namespace summary
            try:
                ns_cmd = "kubectl get namespaces"
                ns_result = subprocess.run(ns_cmd.split(), capture_output=True, text=True, timeout=15)
                if ns_result.returncode == 0:
                    cluster_info.append("\n=== NAMESPACES ===")
                    cluster_info.append(ns_result.stdout)
            except:
                pass
            
            # Get recent events
            try:
                events_cmd = "kubectl get events --all-namespaces --sort-by=.lastTimestamp"
                events_result = subprocess.run(events_cmd.split(), capture_output=True, text=True, timeout=15)
                if events_result.returncode == 0:
                    events_lines = events_result.stdout.split('\n')
                    recent_events = events_lines[:20]  # Last 20 events
                    cluster_info.append("\n=== RECENT EVENTS ===")
                    cluster_info.append('\n'.join(recent_events))
            except:
                pass
            
            return '\n'.join(cluster_info) if cluster_info else "Unable to gather cluster information"
            
        except Exception as e:
            return f"Error getting cluster info: {str(e)}"

class SlackWebhookTool(BaseTool):
    name: str = "Slack Webhook Notifier"
    description: str = "Send notifications to Slack"

    def _run(self, message: str, severity: str = "info", title: str = "K8s Alert") -> str:
        """Send Slack notification"""
        webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        if not webhook_url:
            return f"ℹ️ Slack not configured. Alert: [{severity.upper()}] {title} - {message}"
        
        color_map = {
            "critical": "#FF0000", "high": "#FF6600", "medium": "#FFCC00",
            "low": "#0066CC", "info": "#36a64f"
        }
        
        emoji_map = {
            "critical": "🚨", "high": "⚠️", "medium": "🔶", "low": "🔵", "info": "ℹ️"
        }
        
        payload = {
            "username": "K8s Log Analyzer",
            "icon_emoji": ":kubernetes:",
            "attachments": [{
                "color": color_map.get(severity, "#36a64f"),
                "title": f"{emoji_map.get(severity, 'ℹ️')} {title}",
                "text": message,
                "fields": [
                    {"title": "Severity", "value": severity.upper(), "short": True},
                    {"title": "Time", "value": datetime.now().strftime("%H:%M:%S"), "short": True}
                ]
            }]
        }
        
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            if response.status_code == 200:
                return f"✅ Slack notification sent: [{severity.upper()}] {title}"
            else:
                return f"⚠️ Slack notification failed: {response.status_code}"
        except Exception as e:
            return f"⚠️ Slack error: {str(e)}"

@CrewBase
class KubernetesLogAnalysis():
    """Kubernetes Log Analysis crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        super().__init__()
        # Configure Azure OpenAI LLM
        self.llm = LLM(
            model="azure/gpt-4o",
            base_url=os.getenv("AZURE_API_BASE"),
            api_key=os.getenv("AZURE_API_KEY"),
            api_version=os.getenv("AZURE_API_VERSION")
        )

    @agent
    def log_collector(self) -> Agent:
        return Agent(
            config=self.agents_config['log_collector'],  # type: ignore[index]
            verbose=True,
            llm=self.llm,
            tools=[KubernetesLogCollectorTool(), ClusterInfoTool()]
        )

    @agent
    def log_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['log_analyzer'],  # type: ignore[index]
            verbose=True,
            llm=self.llm,
            tools=[]
        )

    @agent
    def alert_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['alert_manager'],  # type: ignore[index]
            verbose=True,
            llm=self.llm,
            tools=[SlackWebhookTool()]
        )

    @agent
    def report_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['report_generator'],  # type: ignore[index]
            verbose=True,
            llm=self.llm,
            tools=[]
        )

    @task
    def log_collection_task(self) -> Task:
        return Task(
            config=self.tasks_config['log_collection_task'],  # type: ignore[index]
        )

    @task
    def log_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['log_analysis_task'],  # type: ignore[index]
        )

    @task
    def alerting_task(self) -> Task:
        return Task(
            config=self.tasks_config['alerting_task'],  # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],  # type: ignore[index]
            output_file='kubernetes_log_analysis_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Kubernetes Log Analysis crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
