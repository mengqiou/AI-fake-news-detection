"""
Ultra-simple test using boto3 directly (no LangChain).

Tests raw AWS Bedrock API access with Titan model.
"""

import json
import os
import sys

from dotenv import load_dotenv

load_dotenv()

print("\n" + "=" * 70)
print("AWS BEDROCK RAW API TEST (using boto3)")
print("=" * 70 + "\n")

print("Configuration:")
print(f"  Region: {os.getenv('AWS_REGION', 'NOT SET')}")
print(f"  Model: amazon.nova-micro-v1:0 (Amazon Nova Micro)")
print()

try:
    import boto3

    print("✅ boto3 imported\n")

    # Create bedrock-runtime client
    print("Creating Bedrock Runtime client...")
    bedrock = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "ap-southeast-2"),
    )
    print("✅ Client created\n")

    # Prepare request (Nova uses Converse API format)
    print("Preparing request...")
    body = json.dumps(
        {
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": "Hi"}],  # Content must be an array
                }
            ],
            "inferenceConfig": {
                "max_new_tokens": 512,
                "temperature": 0.5,
                "top_p": 0.9,
            },
        }
    )

    # Invoke model
    print("Invoking Nova Micro model with: 'Hi'")
    print("=" * 70 + "\n")

    response = bedrock.invoke_model(
        modelId="amazon.nova-micro-v1:0",
        body=body,
        contentType="application/json",
        accept="application/json",
    )

    # Parse response (Nova format)
    response_body = json.loads(response["body"].read())
    output_text = response_body["output"]["message"]["content"][0]["text"]

    print("✅ SUCCESS!\n")
    print("=" * 70)
    print("TITAN RESPONSE:")
    print("=" * 70)
    print(output_text)
    print("=" * 70 + "\n")

    print("✅ AWS Bedrock is working!")
    print("✅ Your credentials are valid!")
    print("✅ Nova Micro model is accessible!")
    print("\nYou can now run:")
    print("  python tests/test_bedrock_connection.py  (LangChain test)")
    print("  python tests/quick_test.py               (Full agent test)")
    print()

except ImportError:
    print("❌ boto3 not found")
    print("\nInstall it:")
    print("  pip install boto3")
    sys.exit(1)

except Exception as e:
    print(f"❌ ERROR: {e}\n")

    error_str = str(e).lower()

    if "credentials" in error_str or "signature" in error_str:
        print("🔑 Credentials Issue!")
        print("\nCheck:")
        print("  1. AWS_ACCESS_KEY_ID in .env")
        print("  2. AWS_SECRET_ACCESS_KEY in .env")
        print("  3. Keys are active (not expired)")

    elif "accessdenied" in error_str or "forbidden" in error_str:
        print("🚫 Permission Issue!")
        print("\nYour IAM user needs permission:")
        print("  bedrock:InvokeModel")
        print("\nAdd this policy to your IAM user:")
        print("""
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": "bedrock:InvokeModel",
        "Resource": "*"
      }
    ]
  }
        """)

    elif "validationexception" in error_str or "not found" in error_str:
        print("🔍 Model Not Found!")
        print("\nSteps:")
        print("  1. Go to AWS Bedrock Console")
        print("  2. Navigate to 'Model access'")
        print("  3. Enable 'Amazon Titan Text Express'")
        print("  4. Wait for approval (usually instant)")

    else:
        print("❓ Unknown Error")
        import traceback

        traceback.print_exc()

    sys.exit(1)

print("=" * 70 + "\n")
