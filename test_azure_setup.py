#!/usr/bin/env python3
"""
Test Azure OpenAI and Slack Integration for Kubernetes Log Analyzer
"""

import os
import sys
from datetime import datetime

def test_environment_variables():
    """Test if all required environment variables are set"""
    print("🔍 Checking Environment Variables...")
    print("-" * 40)
    
    required_vars = {
        'AZURE_API_BASE': 'Azure OpenAI endpoint',
        'AZURE_API_KEY': 'Azure OpenAI API key',
        'AZURE_API_VERSION': 'Azure OpenAI API version'
    }
    
    optional_vars = {
        'SLACK_WEBHOOK_URL': 'Slack webhook URL'
    }
    
    all_good = True
    
    # Check required variables
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            if 'KEY' in var:
                print(f"✅ {var}: ****** (hidden)")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set ({description})")
            all_good = False
    
    # Check optional variables
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            if 'WEBHOOK' in var:
                print(f"✅ {var}: {value[:50]}... (Slack integration enabled)")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"⚠️  {var}: Not set ({description}) - Slack notifications disabled")
    
    return all_good

def test_crewai_import():
    """Test if CrewAI can be imported and LLM configured"""
    print("\n🧪 Testing CrewAI Import and LLM Configuration...")
    print("-" * 50)
    
    try:
        from crewai import LLM, Agent
        print("✅ CrewAI imported successfully")
        
        # Test LLM configuration
        llm = LLM(
            model="azure/gpt-4o",
            base_url=os.getenv("AZURE_API_BASE"),
            api_key=os.getenv("AZURE_API_KEY"),
            api_version=os.getenv("AZURE_API_VERSION")
        )
        print("✅ Azure OpenAI LLM configured successfully")
        
        # Test agent creation with LLM
        test_agent = Agent(
            role="Test Agent",
            goal="Test Azure OpenAI integration",
            backstory="This is a test agent to verify Azure OpenAI works",
            llm=llm
        )
        print("✅ Agent created with Azure OpenAI LLM")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import CrewAI: {e}")
        print("   Run: pip install crewai[tools]")
        return False
    except Exception as e:
        print(f"❌ Failed to configure Azure OpenAI LLM: {e}")
        print("   Check your Azure OpenAI credentials")
        return False

def test_kubernetes_tools():
    """Test if kubectl is available and working"""
    print("\n⚙️  Testing Kubernetes Tools...")
    print("-" * 35)
    
    import subprocess
    
    try:
        # Test kubectl
        result = subprocess.run(['kubectl', 'version', '--client'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✅ kubectl available: {version}")
        else:
            print("❌ kubectl not working properly")
            return False
        
        # Test cluster connection
        result = subprocess.run(['kubectl', 'cluster-info'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            cluster_info = result.stdout.split('\n')[0]
            print(f"✅ Kubernetes cluster connected: {cluster_info}")
        else:
            print("⚠️  kubectl not connected to cluster (this is OK for testing)")
        
        return True
        
    except FileNotFoundError:
        print("❌ kubectl not found in PATH")
        print("   Install kubectl: https://kubernetes.io/docs/tasks/tools/")
        return False
    except subprocess.TimeoutExpired:
        print("⚠️  kubectl command timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing kubectl: {e}")
        return False

def test_slack_integration():
    """Test Slack webhook if configured"""
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("\n💬 Slack Integration: Not configured (optional)")
        return True
    
    print("\n💬 Testing Slack Integration...")
    print("-" * 32)
    
    try:
        import requests
        
        # Test webhook with a simple message
        payload = {
            "username": "K8s Log Analyzer",
            "icon_emoji": ":kubernetes:",
            "text": "🧪 Test message from Kubernetes Log Analyzer setup",
            "attachments": [
                {
                    "color": "#36a64f",
                    "title": "✅ Azure OpenAI + Slack Integration Test",
                    "text": "Your Kubernetes Log Analyzer is ready with Azure OpenAI!",
                    "fields": [
                        {
                            "title": "Status",
                            "value": "Testing Complete",
                            "short": True
                        },
                        {
                            "title": "LLM Provider",
                            "value": "Azure OpenAI",
                            "short": True
                        },
                        {
                            "title": "Test Time",
                            "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "short": True
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("✅ Slack webhook test successful!")
            print("   Check your Slack channel for the test message")
            return True
        else:
            print(f"❌ Slack webhook test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except ImportError:
        print("❌ requests library not installed")
        print("   Run: pip install requests")
        return False
    except Exception as e:
        print(f"❌ Slack webhook test error: {e}")
        return False

def test_project_structure():
    """Test if all required project files exist"""
    print("\n📁 Testing Project Structure...")
    print("-" * 33)
    
    required_files = [
        'main.py',
        'crew.py', 
        'agents.yaml',
        'tasks.yaml'
    ]
    
    optional_files = [
        '.env',
        'test_slack.py',
        'requirements.txt'
    ]
    
    all_good = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}: Found")
        else:
            print(f"❌ {file}: Missing (required)")
            all_good = False
    
    for file in optional_files:
        if os.path.exists(file):
            print(f"✅ {file}: Found")
        else:
            print(f"⚠️  {file}: Missing (optional)")
    
    return all_good

def test_full_integration():
    """Test creating a simple crew with Azure OpenAI"""
    print("\n🚀 Testing Full Integration...")
    print("-" * 30)
    
    try:
        from helm.crew import KubernetesLogAnalysis
        
        print("✅ KubernetesLogAnalysis class imported successfully")
        
        # Try to create the crew instance
        log_analyzer = KubernetesLogAnalysis()
        print("✅ KubernetesLogAnalysis instance created")
        
        # Try to access the LLM
        if hasattr(log_analyzer, 'llm'):
            print("✅ Azure OpenAI LLM configured in crew")
        else:
            print("⚠️  LLM not found in crew instance")
        
        # Try to create the crew
        crew = log_analyzer.crew()
        print("✅ Crew created successfully")
        
        print(f"✅ Crew has {len(crew.agents)} agents and {len(crew.tasks)} tasks")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import KubernetesLogAnalysis: {e}")
        return False
    except Exception as e:
        print(f"❌ Error creating crew: {e}")
        return False

def run_quick_demo():
    """Run a quick demo if everything is working"""
    print("\n🎯 Quick Demo Test...")
    print("-" * 20)
    
    try:
        from helm.crew import KubernetesLogAnalysis
        
        # Sample inputs for testing
        test_inputs = {
            'namespaces': 'default',
            'time_range': '5m',  # Very short for testing
            'log_levels': 'ERROR,WARN',
            'focus_area': 'testing integration',
            'cluster_context': 'Test cluster',
            'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'priority_issues': 'none (testing)',
            'alert_channels': '#test',
            'oncall_info': 'Test team',
            'severity_thresholds': 'Test thresholds',
            'report_audience': 'Test audience',
            'report_format': 'markdown',
            'include_charts': 'no'
        }
        
        print("Creating KubernetesLogAnalysis crew...")
        analyzer = KubernetesLogAnalysis()
        crew = analyzer.crew()
        
        print("✅ Demo setup complete!")
        print("   The crew is ready to run log analysis")
        print("   To run a full analysis, use: python main.py run --since 30m")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo test failed: {e}")
        return False

def main():
    """Run all tests and provide summary"""
    print("🚀 Kubernetes Log Analyzer - Azure OpenAI Setup Test")
    print("=" * 55)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("CrewAI and Azure OpenAI", test_crewai_import),
        ("Kubernetes Tools", test_kubernetes_tools),
        ("Slack Integration", test_slack_integration),
        ("Project Structure", test_project_structure),
        ("Full Integration", test_full_integration),
        ("Quick Demo", run_quick_demo)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    failed_tests = []
    
    for test_name, test_func in tests:
        print(f"\n🔄 Running: {test_name}")
        print("=" * (len(test_name) + 11))
        
        try:
            if test_func():
                passed_tests += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
                failed_tests.append(test_name)
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
            failed_tests.append(test_name)
    
    # Final summary
    print("\n" + "=" * 55)
    print("📊 TEST SUMMARY")
    print("=" * 55)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Your Kubernetes Log Analyzer is ready with Azure OpenAI!")
        print("\n🚀 Next Steps:")
        print("1. Run: python main.py run --since 30m")
        print("2. Try: python main.py health")
        print("3. Set up automated monitoring")
        print("\n💡 Pro Tips:")
        print("- Use shorter time ranges (--since 15m) for faster testing")
        print("- Check Slack channel for notifications")
        print("- Monitor Azure OpenAI usage in Azure portal")
        
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed:")
        for failed_test in failed_tests:
            print(f"   - {failed_test}")
        
        print("\n🔧 Troubleshooting:")
        if "Environment Variables" in failed_tests:
            print("- Set Azure OpenAI credentials: run setup_environment.sh")
        if "CrewAI and Azure OpenAI" in failed_tests:
            print("- Install dependencies: pip install crewai[tools]")
            print("- Check Azure OpenAI endpoint and API key")
        if "Kubernetes Tools" in failed_tests:
            print("- Install kubectl and configure cluster access")
        if "Slack Integration" in failed_tests:
            print("- Verify Slack webhook URL is correct")
        if "Project Structure" in failed_tests:
            print("- Ensure you're in the correct project directory")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    print("🔧 Kubernetes Log Analyzer - Setup Test")
    print()
    
    # Quick environment check
    if not os.getenv("AZURE_API_KEY"):
        print("❌ AZURE_API_KEY not found!")
        print("💡 Run setup script first: ./setup_environment.sh")
        print("   Or load environment: source .env")
        sys.exit(1)
    
    # Run all tests
    success = main()
    
    if success:
        print("\n🚀 Ready to analyze Kubernetes logs with Azure OpenAI!")
    else:
        print("\n🔧 Please fix the issues above and run the test again")
        sys.exit(1)
