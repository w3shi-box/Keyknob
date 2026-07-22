import subprocess
import os

def simulate_agent_tool_call(command_args, test_name):
    print(f"\n=== Running: {test_name} ===")
    print(f"[*] Command executed by Agent: {' '.join(command_args)}")
    
    try:
        # Run the command exactly how an agent terminal tool would spawn it
        result = subprocess.run(
            command_args,
            capture_output=True,
            text=True,
            check=True
        )
        
        # Display the raw response returned back to the agent interface
        print("\n--- Agent Terminal Output Log ---")
        print(result.stdout.strip())
        print("---------------------------------")
        
        # Evaluate if the boundary was broken
        if "CRITICAL SECURITY BOUNDARY BREACHED" in result.stdout:
            print("❌ VULNERABILITY ALERT: The application boundary collapsed.")
            print("   The untrusted repository executed code via a passive metadata check.")
        else:
            print("✅ SYSTEM SECURE: The execution runtime effectively isolated module lookup.")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Execution error or script crash: {e.stderr}")

if __name__ == "__main__":
    # Ensure working directory integrity before testing
    if not os.path.exists("sys.py"):
        print("[-] Error: Execute this runner file inside the folder containing 'sys.py'")
        exit(1)

    # Define the precise compound statement used by the agent in your simulation
    target_payload = "import sys; print(sys.version); print(sys.executable); print(sys.platform)"

    # Test Case 1: Standard command string generation used by default agents
    simulate_agent_tool_call(
        ["python3", "-c", target_payload], 
        "Test 1: Unhardened Agent Runtime (Default Module Resolution)"
    )
    
    print("\n" + "="*70)
    
    # Test Case 2: Secure configuration utilizing the Isolation flag
    simulate_agent_tool_call(
        ["python3", "-I", "-c", target_payload], 
        "Test 2: Hardened Agent Runtime (Isolated Environment Execution)"
    )
