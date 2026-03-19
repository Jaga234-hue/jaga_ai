import boto3
import json

client = boto3.client("bedrock-runtime", region_name="us-east-1")

response = client.invoke_model(
    modelId="openai.gpt-oss-120b-1:0",
    body=json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "hi , my name is jaga"
            }
        ],
        "max_tokens": 400,   # ✅ increased
        "temperature": 0.7
    })
)

result = json.loads(response["body"].read())

output = result["choices"][0]["message"]["content"]

# ✅ Remove reasoning if present
output = result["choices"][0]["message"]["content"]

# ✅ Safe cleaning
if "<reasoning>" in output:
    parts = output.split("</reasoning>")
    if len(parts) > 1:
        output = parts[-1]
    else:
        output = output  # keep original if broken

# ✅ Check empty
if not output.strip():
    print("⚠️ Model returned empty output. Try increasing max_tokens.")
else:
    print(output.strip())

