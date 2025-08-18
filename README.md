

# K8s_Agent: Multi-Agent Kubernetes Automation

## Main Purpose

**K8s_Agent** is a modular, multi-agent framework designed to **automate and orchestrate Kubernetes cluster diagnostics, incident response, monitoring, and security analysis**. all agent roles and capabilities are defined in `src/helm/config/agents.yaml` and their workflows in `tasks.yaml`. The core purpose is to enable declarative, YAML-driven assignment of AI and automation tasks to different agents for a Kubernetes environment.

***

## Agent-Based Architecture

All agent definitions— their skills, tool access, LLM parameters, and operational focus—are maintained in `agents.yaml`. This means **the project can be adapted to various Kubernetes troubleshooting, monitoring, or workflow automation scenarios** by simply editing this YAML, rather than the codebase itself.

**Agent definitions typically include:**

- Role/name/goal
- Tools enabled (log collection, Slack alerting, custom)
- LLM configuration (model, prompts, temperature, etc.)
- Permissions or data scope

**Example Use Cases (controlled via agents.yaml):**


| Agent Type | Description/Typical Role |
| :-- | :-- |
| Log Collector | Gathers pod, node, and event logs across cluster or focused namespaces |
| Analyzer | Processes log data, looks for error patterns, anomalies |
| Reporter | Compiles Markdown or other reports for SRE/DevOps integration |
| Alert Manager | Sends Slack or webhook alerts when issues, thresholds, or patterns are found |
| Custom AI/Script Agent | Can be configured for advanced reasoning, remediation suggestions |

**These can be expanded, renamed, or reconfigured fully in the YAML file.**

***

## Key Principles

- **YAML-First**: The true core of the system is the agent/task configuration; code just provides an execution engine.
- **Customizable Workflows**: Add, remove, or change agent roles and behaviors via YAML edits only.
- **Kubernetes Focus**: All useful capabilities—log parsing, health checks, security scanning, event collation—are realized as agent tasks.
- **LLM-Driven**: Leverages large language models (e.g., OpenAI/Azure) for log interpretation, summary, and natural language output.

***

## How to Use and Extend

1. **Clone and set up the repo**.
2. **Edit `src/helm/config/agents.yaml`** to define:
    - Agent names, roles, model settings, available tools, and skills.
3. **Edit `src/helm/config/tasks.yaml`** to sequence agent actions for different scenarios (full scan, incident analysis, audit, reporting).
4. **Run**:

```sh
crewai run       # default workflow
```

5. **Modify/add agents or tasks** by updating only the YAML—no code changes required unless building completely new logic/tools.

***

## Summary Table: YAML-Driven Agent System

| Component | Location | Main Role | Editable by User? |
| :-- | :-- | :-- | :-- |
| Agents | `src/helm/config/agents.yaml` | Define AI agent roles, skills, tools, LLM | **Yes** |
| Tasks/Workflow | `src/helm/config/tasks.yaml` | Task assignment, sequence, conditions | **Yes** |
| Tools/Logic | `src/helm/tools/` (Python) | Underlying automation/scripts/APIs | Advanced |
| Execution Engine | `src/helm/crew.py`, `main.py` | Loads YAML, orchestrates agent/task running | Not required |


***

Edit `agents.yaml` and `tasks.yaml` to **transform K8s_Agent into any infrastructure AIOps workflow required**—from daily health checks to auto-incident investigation or compliance reporting. The provided directory and code are simply an execution harness for YOUR YAML-based automation.[^1][^2][^3][^4][^5][^6][^7][^8][^9][^10][^11][^12][^13][^14][^15][^16]

<div style="text-align: center">⁂</div>

[^1]: https://github.com/atharrvv/K8s

[^2]: https://github.com/atharrvv/K8s_Agent.git

[^3]: https://github.com/kagent-dev/kagent

[^4]: https://docs.newrelic.com/docs/kubernetes-pixie/kubernetes-integration/installation/k8s-agent-operator/

[^5]: https://octopus.com/docs/kubernetes/targets/kubernetes-agent

[^6]: https://github.com/newrelic/k8s-agents-automation

[^7]: https://docs.vantage.sh/kubernetes_agent/

[^8]: https://docs.gitlab.com/user/clusters/agent/work_with_agent/

[^9]: https://github.com/k8sgpt-ai/k8sgpt

[^10]: https://docs.gitlab.com/user/clusters/agent/install/

[^11]: https://kubernetes.io/docs/home/

[^12]: https://wandb.ai/byyoung3/crewai_git_documenter/reports/Building-a-Github-repo-summarizer-with-CrewAI--VmlldzoxMjY5Mzc5Ng

[^13]: https://github.com/atharrvv/K8s_Agent/blob/main/README.md

[^14]: https://github.com/atharrvv/K8s_Agent/blob/main/src/helm/main.py

[^15]: https://github.com/atharrvv/K8s_Agent/blob/main/src/helm/crew.py

[^16]: https://github.com/atharrvv/K8s_Agent/blob/main/pyproject.toml

