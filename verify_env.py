import os
import sys

print("🔍 --- DIAGNOSTIC START ---")

# 1. Check if .env file exists in current directory
env_path = os.path.join(os.getcwd(), '.env')
print(f"1. File Check: .env exists at {env_path}? -> {os.path.exists(env_path)}")

if not os.path.exists(env_path):
    print("❌ ERROR: .env file not found in current folder!")
    print("💡 Fix: Create the .env file in the same folder where you run this script.")
    sys.exit()

# 2. Check if python-dotenv is installed
try:
    from dotenv import load_dotenv
    print("2. Library Check: python-dotenv installed? -> ✅ Yes")
except ImportError:
    print("2. Library Check: python-dotenv installed? -> ❌ No")
    print("💡 Fix: Run 'pip install python-dotenv'")
    sys.exit()

# 3. Load the variables
print("3. Loading variables...")
load_dotenv()

# 4. Verify specific keys
keys_to_check = [
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "GROQ_API_KEY",
    "NVIDIA_API_KEY"
]

all_good = True
for key in keys_to_check:
    val = os.getenv(key)
    if val:
        # Mask the key for security, show first 5 and last 5 chars
        masked = f"{val[:5]}...{val[-5:]}" if len(val) > 10 else val
        print(f"   ✅ {key}: Found ({masked})")
    else:
        print(f"   ❌ {key}: MISSING or Empty")
        all_good = False

print("🔍 --- DIAGNOSTIC END ---")
if all_good:
    print("🎉 SUCCESS: All keys loaded correctly!")
else:
    print("⚠️ WARNING: Some keys are missing. Check your .env file spelling.")