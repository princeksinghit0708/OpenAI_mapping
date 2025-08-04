#!/usr/bin/env python3
"""
LiteLLM Decision and Setup Helper
Interactive script to help decide whether to use LiteLLM and configure it
"""

import os
import sys
from pathlib import Path
import subprocess


def check_current_setup():
    """Check current system setup"""
    print("🔍 Analyzing your current setup...")
    
    # Check if LiteLLM is installed
    try:
        import litellm
        litellm_installed = True
        litellm_version = litellm.__version__
    except ImportError:
        litellm_installed = False
        litellm_version = "Not installed"
    
    # Check API keys
    api_keys = {
        "OpenAI": bool(os.getenv("OPENAI_API_KEY")),
        "Anthropic": bool(os.getenv("ANTHROPIC_API_KEY")),
        "Google": bool(os.getenv("GOOGLE_API_KEY")),
        "Azure": bool(os.getenv("AZURE_OPENAI_API_KEY"))
    }
    
    # Check current requirements
    requirements_file = Path("requirements.txt")
    enhanced_requirements_file = Path("requirements_enhanced.txt")
    
    print("\n📊 Current Setup Analysis:")
    print(f"   LiteLLM installed: {'✅' if litellm_installed else '❌'} ({litellm_version})")
    print(f"   Standard requirements: {'✅' if requirements_file.exists() else '❌'}")
    print(f"   Enhanced requirements: {'✅' if enhanced_requirements_file.exists() else '❌'}")
    
    print(f"\n🔑 API Keys Available:")
    for provider, available in api_keys.items():
        print(f"   {provider}: {'✅' if available else '❌'}")
    
    available_providers = sum(api_keys.values())
    
    return {
        "litellm_installed": litellm_installed,
        "api_keys": api_keys,
        "available_providers": available_providers,
        "enhanced_requirements": enhanced_requirements_file.exists()
    }


def assess_use_case():
    """Interactive assessment of use case"""
    print("\n🎯 Let's assess your use case to make the best recommendation...")
    
    questions = [
        {
            "question": "What's your primary use case?",
            "options": [
                "1. Learning/experimenting with the system",
                "2. Building an MVP or prototype", 
                "3. Developing a production application",
                "4. Enterprise-grade system with high availability needs"
            ],
            "weights": [1, 2, 4, 5]
        },
        {
            "question": "What's your expected usage volume?",
            "options": [
                "1. Low (< 100 requests/day)",
                "2. Medium (100-1000 requests/day)",
                "3. High (1000-10000 requests/day)",
                "4. Very High (> 10000 requests/day)"
            ],
            "weights": [1, 2, 4, 5]
        },
        {
            "question": "How important is cost optimization?",
            "options": [
                "1. Not important (cost is not a concern)",
                "2. Somewhat important (want to be cost-aware)",
                "3. Very important (need significant cost savings)",
                "4. Critical (cost optimization is a key requirement)"
            ],
            "weights": [1, 2, 4, 5]
        },
        {
            "question": "What's your tolerance for system downtime?",
            "options": [
                "1. High (occasional downtime is acceptable)",
                "2. Medium (prefer high uptime but some downtime OK)",
                "3. Low (need very high availability)",
                "4. Zero (system must be always available)"
            ],
            "weights": [1, 2, 4, 5]
        },
        {
            "question": "How complex can your setup be?",
            "options": [
                "1. Simple only (want minimal complexity)",
                "2. Moderate (some complexity is OK)",
                "3. Complex (comfortable with advanced setups)",
                "4. Very complex (can handle enterprise-level complexity)"
            ],
            "weights": [1, 2, 4, 5]
        }
    ]
    
    total_score = 0
    answers = []
    
    for i, q in enumerate(questions):
        print(f"\n{i+1}. {q['question']}")
        for option in q['options']:
            print(f"   {option}")
        
        while True:
            try:
                choice = int(input("   Your choice (1-4): ")) - 1
                if 0 <= choice < 4:
                    total_score += q['weights'][choice]
                    answers.append(choice + 1)
                    break
                else:
                    print("   Please enter 1, 2, 3, or 4")
            except ValueError:
                print("   Please enter a number")
    
    return total_score, answers


def make_recommendation(setup_info, score, answers):
    """Make recommendation based on assessment"""
    print(f"\n📊 Assessment Score: {score}/25")
    
    # Decision logic
    if score <= 8:
        recommendation = "current"
        title = "Stick with Current Structure"
        reasoning = "Your needs are well-served by the current simple approach"
    elif score <= 15:
        recommendation = "pragmatic"
        title = "Upgrade to Pragmatic Enhanced"
        reasoning = "Good balance of features and complexity for your use case"
    else:
        recommendation = "multi_provider"
        title = "Full Multi-Provider Setup"
        reasoning = "Your requirements justify the advanced multi-provider approach"
    
    # Adjust based on available providers
    if recommendation == "multi_provider" and setup_info["available_providers"] < 2:
        recommendation = "pragmatic"
        title = "Pragmatic Enhanced (Limited Providers)"
        reasoning += " - Limited API keys available, but pragmatic approach still beneficial"
    
    print(f"\n🎯 **RECOMMENDATION: {title}**")
    print(f"📝 **Reasoning: {reasoning}**")
    
    return recommendation, title, reasoning


def show_implementation_plan(recommendation, setup_info):
    """Show specific implementation plan"""
    print(f"\n🚀 Implementation Plan for {recommendation.title()} Approach:")
    print("-" * 50)
    
    if recommendation == "current":
        print("✅ **You're already set up well!**")
        print("\n📋 Optional improvements you can make:")
        print("   1. Add basic retry logic with tenacity:")
        print("      pip install tenacity")
        print("   2. Add simple cost tracking")
        print("   3. Implement basic error handling")
        
        print(f"\n⏱️ **Time investment:** 1-2 hours")
        print(f"💰 **Additional cost:** $0/month")
        
    elif recommendation == "pragmatic":
        print("🔧 **Pragmatic Enhanced Setup:**")
        print("\n📦 1. Install additional dependencies:")
        print("      pip install tenacity")
        if not setup_info["litellm_installed"]:
            print("      pip install litellm  # Optional, for future use")
        
        print(f"\n🔧 2. Update your agent implementation:")
        print("      - Replace BaseAgent with PragmaticEnhancedAgent")
        print("      - Enable cost tracking and fallbacks")
        print("      - Add basic multi-provider support (future-ready)")
        
        print(f"\n⚙️ 3. Environment configuration:")
        print("      - Keep your existing OPENAI_API_KEY")
        print("      - Add ENABLE_MULTI_PROVIDER=false")
        print("      - Add other provider keys when ready")
        
        print(f"\n⏱️ **Time investment:** 4-8 hours")  
        print(f"💰 **Cost savings:** 10-20% through better optimization")
        
    else:  # multi_provider
        print("🌟 **Full Multi-Provider Setup:**")
        print("\n📦 1. Install enhanced dependencies:")
        print("      pip install -r requirements_enhanced.txt")
        
        print(f"\n🔑 2. Setup multiple API keys:")
        missing_keys = [k for k, v in setup_info["api_keys"].items() if not v]
        if missing_keys:
            print(f"      Missing API keys: {', '.join(missing_keys)}")
            print("      Get keys from:")
            if "OpenAI" in missing_keys:
                print("      - OpenAI: https://platform.openai.com/api-keys")
            if "Anthropic" in missing_keys:
                print("      - Anthropic: https://console.anthropic.com/")
            if "Google" in missing_keys:
                print("      - Google: https://makersuite.google.com/app/apikey")
        
        print(f"\n🔧 3. Update implementation:")
        print("      - Use PragmaticEnhancedAgent with multi_provider=True")
        print("      - Configure intelligent routing")
        print("      - Set up cost optimization rules")
        
        print(f"\n⚙️ 4. Environment configuration:")
        print("      - Set ENABLE_MULTI_PROVIDER=true")
        print("      - Configure cost limits and routing preferences")
        
        print(f"\n⏱️ **Time investment:** 1-2 days")
        print(f"💰 **Cost savings:** 30-50% through intelligent routing")


def setup_environment(recommendation):
    """Help setup environment based on recommendation"""
    print(f"\n🔧 Environment Setup for {recommendation.title()} approach:")
    
    env_file = Path(".env")
    env_example = Path("env_template.txt")
    
    # Read existing .env or create from template
    env_content = []
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_content = f.readlines()
    elif env_example.exists():
        with open(env_example, 'r') as f:
            env_content = f.readlines()
    
    # Add recommendation-specific settings
    new_settings = []
    
    if recommendation == "current":
        new_settings = [
            "\n# Current Structure Settings",
            "ENABLE_MULTI_PROVIDER=false",
            "ENABLE_COST_TRACKING=true",
            "ENABLE_FALLBACKS=true"
        ]
    elif recommendation == "pragmatic":
        new_settings = [
            "\n# Pragmatic Enhanced Settings", 
            "ENABLE_MULTI_PROVIDER=false",
            "ENABLE_COST_TRACKING=true",
            "ENABLE_FALLBACKS=true",
            "MAX_COST_PER_REQUEST=0.50"
        ]
    else:  # multi_provider
        new_settings = [
            "\n# Multi-Provider Settings",
            "ENABLE_MULTI_PROVIDER=true", 
            "ENABLE_COST_TRACKING=true",
            "ENABLE_FALLBACKS=true",
            "MAX_COST_PER_REQUEST=0.30",
            "DAILY_COST_LIMIT=100.0"
        ]
    
    # Write updated .env file
    try:
        with open(env_file, 'w') as f:
            f.writelines(env_content)
            f.write('\n'.join(new_settings) + '\n')
        
        print(f"✅ Updated .env file with {recommendation} settings")
        
    except Exception as e:
        print(f"❌ Could not update .env file: {e}")
        print("🔧 Manually add these settings to your .env file:")
        for setting in new_settings:
            if setting.startswith('#'):
                print(f"   {setting}")
            else:
                print(f"   {setting}")


def install_dependencies(recommendation):
    """Install required dependencies"""
    print(f"\n📦 Installing dependencies for {recommendation} approach...")
    
    try:
        if recommendation == "current":
            # Just add tenacity for retries
            subprocess.run([sys.executable, "-m", "pip", "install", "tenacity"], check=True)
            print("✅ Installed tenacity for retry logic")
            
        elif recommendation == "pragmatic":
            # Install basic enhancements
            packages = ["tenacity", "litellm"]
            for package in packages:
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
                    print(f"✅ Installed {package}")
                except subprocess.CalledProcessError:
                    print(f"⚠️ Failed to install {package} - you can install it manually later")
            
        else:  # multi_provider
            # Install full enhanced requirements
            if Path("requirements_enhanced.txt").exists():
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_enhanced.txt"], check=True)
                print("✅ Installed enhanced requirements")
            else:
                print("⚠️ requirements_enhanced.txt not found - installing key packages...")
                key_packages = ["litellm", "tenacity", "prometheus-client"]
                for package in key_packages:
                    try:
                        subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
                        print(f"✅ Installed {package}")
                    except subprocess.CalledProcessError:
                        print(f"⚠️ Failed to install {package}")
                        
    except Exception as e:
        print(f"❌ Installation error: {e}")
        print("🔧 Please install dependencies manually")


def main():
    """Main setup flow"""
    print("🎯 LiteLLM Decision Helper for Agentic Mapping AI")
    print("=" * 60)
    print("This tool will help you decide whether to use LiteLLM and set it up properly.")
    
    # Step 1: Check current setup
    setup_info = check_current_setup()
    
    # Step 2: Assess use case
    score, answers = assess_use_case()
    
    # Step 3: Make recommendation
    recommendation, title, reasoning = make_recommendation(setup_info, score, answers)
    
    # Step 4: Show implementation plan
    show_implementation_plan(recommendation, setup_info)
    
    # Step 5: Offer to configure
    print(f"\n❓ Would you like to configure your system for the {title} approach?")
    configure = input("Configure now? (y/n): ").lower().startswith('y')
    
    if configure:
        # Setup environment
        setup_environment(recommendation)
        
        # Install dependencies
        install_deps = input("\n📦 Install required dependencies? (y/n): ").lower().startswith('y')
        if install_deps:
            install_dependencies(recommendation)
        
        print(f"\n🎉 Setup complete! Your system is configured for the {title} approach.")
        print(f"\n📖 Next steps:")
        print("   1. Review the updated .env file")
        print("   2. Test the setup with: python examples/litellm_comparison_demo.py")
        print("   3. Start using PragmaticEnhancedAgent in your code")
        print("   4. Monitor performance and costs")
        
    else:
        print(f"\n📝 Manual setup instructions saved. You can configure later using:")
        print(f"   - Recommendation: {title}")
        print(f"   - See LITELLM_ANALYSIS.md for detailed guidance")
    
    print(f"\n✅ Decision helper completed!")


if __name__ == "__main__":
    main()