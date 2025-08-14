#!/usr/bin/env python
import sys
import warnings
import argparse
from datetime import datetime, timedelta

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def get_default_inputs():
    """Get default input parameters for log analysis"""
    return {
        'namespaces': 'ALL_NAMESPACES',  # Search across entire cluster
        'time_range': '1h',
        'log_levels': 'ERROR,WARN,INFO',
        'focus_area': 'cluster-wide errors and performance issues',
        'cluster_context': 'Full Kubernetes cluster analysis',
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'priority_issues': 'pod crashes, deployment failures, resource constraints across cluster',
        'alert_channels': '#devops-alerts, #monitoring',
        'oncall_info': 'DevOps team',
        'severity_thresholds': 'Critical: Pod crashes, High: Resource limits, Medium: Warnings',
        'report_audience': 'DevOps engineers, SRE team',
        'report_format': 'markdown',
        'include_charts': 'no'
    }

def run_log_analysis(custom_inputs=None):
    """
    Run the Kubernetes log analysis crew.
    """
    # Import here to avoid issues if not properly configured
    try:
        from helm.crew import KubernetesLogAnalysis
    except ImportError as e:
        print(f"❌ Error importing KubernetesLogAnalysis: {e}")
        print("Make sure you're in the correct directory and dependencies are installed")
        return False
    
    inputs = get_default_inputs()
    
    # Override with custom inputs if provided
    if custom_inputs:
        inputs.update(custom_inputs)
    
    print("🚀 Starting Kubernetes Log Analysis...")
    print(f"📊 Analysis Parameters:")
    print(f"   - Namespaces: {inputs['namespaces']}")
    print(f"   - Time Range: {inputs['time_range']}")
    print(f"   - Log Levels: {inputs['log_levels']}")
    print(f"   - Focus Area: {inputs['focus_area']}")
    print(f"   - Current Time: {inputs['current_time']}")
    print()
    
    try:
        # Create and run the crew
        analyzer = KubernetesLogAnalysis()
        crew = analyzer.crew()
        result = crew.kickoff(inputs=inputs)
        
        print("✅ Log analysis completed successfully!")
        print("📄 Report generated: kubernetes_log_analysis_report.md")
        return result
        
    except Exception as e:
        print(f"❌ Error occurred during log analysis: {e}")
        # Print more detailed error info for debugging
        import traceback
        traceback.print_exc()
        raise Exception(f"An error occurred while running the log analysis crew: {e}")

def run_incident_investigation(namespace, pod_name=None, since="30m"):
    """
    Run focused incident investigation for specific namespace/pod.
    """
    inputs = get_default_inputs()
    inputs.update({
        'namespaces': namespace,
        'time_range': since,
        'focus_area': f'incident investigation in {namespace}' + (f' for pod {pod_name}' if pod_name else ''),
        'priority_issues': 'critical errors, pod failures, service disruptions',
        'log_levels': 'ERROR,WARN'
    })
    
    print(f"🔍 Starting incident investigation for namespace: {namespace}")
    if pod_name:
        print(f"🎯 Focusing on pod: {pod_name}")
    print(f"⏰ Time range: {since}")
    
    return run_log_analysis(inputs)

def run_health_check():
    """
    Run routine health check analysis.
    """
    inputs = get_default_inputs()
    inputs.update({
        'time_range': '6h',  # Shorter timeframe for health check
        'focus_area': 'routine health check and performance monitoring',
        'priority_issues': 'performance degradation, resource usage trends, warning patterns',
        'log_levels': 'ERROR,WARN,INFO'
    })
    
    print("🏥 Starting routine health check analysis...")
    return run_log_analysis(inputs)

def run_security_audit():
    """
    Run security-focused log analysis.
    """
    inputs = get_default_inputs()
    inputs.update({
        'time_range': '24h',  # 24 hours instead of 7 days to reduce load
        'focus_area': 'security events and unauthorized access attempts',
        'priority_issues': 'authentication failures, unauthorized access, security violations',
        'log_levels': 'ERROR,WARN',
        'report_audience': 'Security team, DevOps engineers'
    })
    
    print("🔒 Starting security audit analysis...")
    return run_log_analysis(inputs)

def run():
    """
    Run the crew with default parameters.
    """
    return run_log_analysis()

def train():
    """
    Train the crew for a given number of iterations.
    """
    from helm.crew import KubernetesLogAnalysis
    
    inputs = get_default_inputs()
    try:
        KubernetesLogAnalysis().crew().train(
            n_iterations=int(sys.argv[1]), 
            filename=sys.argv[2], 
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        from helm.crew import KubernetesLogAnalysis
        KubernetesLogAnalysis().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    from helm.crew import KubernetesLogAnalysis
    
    inputs = get_default_inputs()
    try:
        KubernetesLogAnalysis().crew().test(
            n_iterations=int(sys.argv[1]), 
            eval_llm=sys.argv[2], 
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def main():
    """
    Main function with command-line interface.
    """
    parser = argparse.ArgumentParser(description='Kubernetes Log Analysis Tool')
    parser.add_argument('action', nargs='?', default='run', 
                       choices=['run', 'incident', 'health', 'security', 'train', 'replay', 'test'],
                       help='Action to perform')
    parser.add_argument('--namespace', '-n', type=str, default='default',
                       help='Kubernetes namespace to analyze')
    parser.add_argument('--pod', '-p', type=str, 
                       help='Specific pod name to analyze')
    parser.add_argument('--since', '-s', type=str, default='1h',
                       help='Time range for log collection (e.g., 1h, 30m, 2d)')
    parser.add_argument('--namespaces', type=str, 
                       help='Comma-separated list of namespaces to analyze')
    parser.add_argument('--focus', type=str,
                       help='Focus area for analysis')
    
    args = parser.parse_args()
    
    # Basic environment check
    import os
    if not os.getenv("AZURE_API_KEY"):
        print("⚠️ AZURE_API_KEY not found. Make sure to set your Azure OpenAI credentials.")
        print("   Run: source .env  (if you have an .env file)")
        print("   Or: export AZURE_API_KEY='your-api-key'")
        print()
    
    if args.action == 'run':
        custom_inputs = {}
        if args.namespaces:
            custom_inputs['namespaces'] = args.namespaces
        if args.since:
            custom_inputs['time_range'] = args.since
        if args.focus:
            custom_inputs['focus_area'] = args.focus
        
        run_log_analysis(custom_inputs)
        
    elif args.action == 'incident':
        run_incident_investigation(args.namespace, args.pod, args.since)
        
    elif args.action == 'health':
        run_health_check()
        
    elif args.action == 'security':
        run_security_audit()
        
    elif args.action == 'train':
        train()
        
    elif args.action == 'replay':
        replay()
        
    elif args.action == 'test':
        test()

if __name__ == "__main__":
    main()
