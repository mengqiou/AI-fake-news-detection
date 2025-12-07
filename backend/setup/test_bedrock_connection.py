"""
Simple test to verify AWS Bedrock connection with Titan model.

Just sends "Hi" to the model to verify credentials and access.
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("\n" + "=" * 70)
print("AWS BEDROCK CONNECTION TEST - Amazon Nova Micro")
print("=" * 70 + "\n")

# Check environment variables
print("Checking configuration...")
print(f"  AWS Region: {os.getenv('AWS_REGION', 'NOT SET')}")
print(f"  AWS Access Key: {os.getenv('AWS_ACCESS_KEY_ID', 'NOT SET')[:10]}...")
print(f"  AWS Secret Key: {'SET' if os.getenv('AWS_SECRET_ACCESS_KEY') else 'NOT SET'}")
print()

# Test Bedrock connection
try:
    print("Importing langchain_aws...")
    from langchain_aws import ChatBedrock
    print("✅ langchain_aws imported successfully\n")
    
    print("Creating Bedrock client...")
    llm = ChatBedrock(
        model_id="amazon.nova-micro-v1:0",
        region_name=os.getenv('AWS_REGION', 'ap-southeast-2'),
        model_kwargs={
            "temperature": 0.5,
            "max_new_tokens": 512
        }
    )
    print("✅ Bedrock client created successfully\n")
    
    print("=" * 70)
    print("Sending test message: 'Hi'")
    print("=" * 70 + "\n")
    
    response = llm.invoke("Hi")
    
    print("✅ SUCCESS! Received response from Bedrock:\n")
    print("=" * 70)
    print("MODEL RESPONSE:")
    print("=" * 70)
    print(response.content)
    print("=" * 70 + "\n")
    
    print("✅ AWS Bedrock connection is working!")
    print("✅ Nova Micro model is accessible!")
    print("\nYou can now run the full agent tests:")
    print("  python tests/quick_test.py")
    print("  python tests/test_platform_verification.py")
    print()
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("\nInstall required package:")
    print("  pip install langchain-aws")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ ERROR: {e}\n")
    
    error_str = str(e).lower()
    
    if "credentials" in error_str or "access" in error_str:
        print("Credential Issue Detected!")
        print("\nTroubleshooting:")
        print("1. Check your .env file has:")
        print("   AWS_REGION=ap-southeast-2")
        print("   AWS_ACCESS_KEY_ID=your_key")
        print("   AWS_SECRET_ACCESS_KEY=your_secret")
        print("\n2. Verify credentials are active in AWS Console")
        print("3. Ensure IAM user has bedrock:InvokeModel permission")
        
    elif "not found" in error_str or "does not exist" in error_str:
        print("Model Access Issue Detected!")
        print("\nTroubleshooting:")
        print("1. Enable Titan Text Express in AWS Bedrock Console")
        print("2. Go to: AWS Bedrock > Model access")
        print("3. Request access to Amazon Titan models")
        print("4. Wait for approval (usually instant)")
        
    elif "region" in error_str:
        print("Region Issue Detected!")
        print("\nTroubleshooting:")
        print("1. Verify Bedrock is available in your region")
        print("2. Try using us-east-1 or us-west-2")
        
    else:
        print("Unknown Error!")
        print("\nFull error details:")
        import traceback
        traceback.print_exc()
    
    sys.exit(1)

print("=" * 70 + "\n")
