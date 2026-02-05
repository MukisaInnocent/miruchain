import os
import sys
import django

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miruchain.settings')

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Python executable:", sys.executable)
print("Python path:", sys.path)

try:
    print("\n1. Setting up Django...")
    django.setup()
    print("✓ Django setup successful!")
    
    print("\n2. Importing apps...")
    from django.apps import apps
    print("✓ Apps imported!")
    
    print("\n3. Getting app configs...")
    for app_config in apps.get_app_configs():
        print(f"  - {app_config.name}")
    
    print("\n4. Checking models...")
    from django.core.management import call_command
    call_command('check')
    print("✓ Check passed!")
    
    print("\n✓✓✓ Everything works! Ready for migrations!")
    
except Exception as e:
    print(f"\n✗ Error: {type(e).__name__}")
    print(f"  Message: {e}")
    import traceback
    traceback.print_exc()
