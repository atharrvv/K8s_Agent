# Kubernetes Log Analysis Agents 🤖📊
<img src="https://raw.githubusercontent.com/kubernetes/kubernetes/master/logo/logo.png" alt="Kubernetes Logo" width="80"/>


## Overview
This project provides an **AI-powered multi-agent system** for Kubernetes log analysis, security auditing, and incident investigation.  
It leverages **CrewAI** to coordinate agents that collect logs, analyze patterns, send alerts, and generate structured reports.

---

## 🔑 Key Functionalities

### 📝 Log Collection
- Collects logs from pods across **all namespaces** or specific ones.
- Prioritizes key namespaces (`default`, `kube-system`, `monitoring`, etc.).
- Detects issues such as **errors, crashes, warnings, and restarts**.

### 📊 Cluster Insights
- Gathers **cluster info**, including:
  - Node status
  - Namespace summary
  - Recent Kubernetes events
- Provides a **cluster-wide snapshot** of health and activity.

### 🚨 Alerting System
- Sends **Slack notifications** with severity levels:
  - Critical 🚨, High ⚠️, Medium 🔶, Low 🔵, Info ℹ️
- Notifies DevOps/SRE teams about incidents and anomalies.

### 📄 Automated Reporting
- Generates Markdown reports (`kubernetes_log_analysis_report.md`).
- Reports include:
  - Log analysis findings
  - Cluster insights
  - Alerts and recommendations

### 🔍 Specialized Analysis Modes
- **Incident Investigation**: Focus on a specific namespace or pod.
- **Health Check**: Routine cluster health and performance monitoring.
- **Security Audit**: Detects unauthorized access, authentication failures, and suspicious activity.

---

## 📂 Repository Structure
```
.
├── crew.py                  # Defines agents, tools, and CrewAI orchestration
├── main.py                  # CLI entry point for running different analyses
├── agents.yaml              # Agent & task configuration
└── kubernetes_log_analysis_report.md (generated)
```

---

## ⚡ Getting Started

### Prerequisites
- Python 3.9+
- Kubernetes cluster access (`kubectl` configured)
- [Trivy](https://aquasecurity.github.io/trivy/) (optional, for security scans)
- Slack Webhook URL (optional, for alerts)
- Azure OpenAI API credentials (`AZURE_API_KEY`, `AZURE_API_BASE`, `AZURE_API_VERSION`)

### Installation
```bash
# Clone the repo
git clone <your-repo-url>
cd <repo-directory>

# Install dependencies
crewai run
```

---

## 🧠 Agents

- **Log Collector** → Collects logs & cluster info.  
- **Log Analyzer** → Processes logs to detect anomalies.  
- **Alert Manager** → Sends Slack alerts.  
- **Report Generator** → Creates structured reports.  

---

## 📌 Future Enhancements
- Integration with Prometheus & Grafana for real-time monitoring.  
- Automated remediation (restart pods, scale workloads).  
- Support for AWS EKS & GCP GKE.  
- Rich visual reports with charts & dashboards.  

---

## 🤝 Contributing
Contributions are welcome! Please open issues or PRs for enhancements.

---

