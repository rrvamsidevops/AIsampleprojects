# AWS Bedrock IAM Policy Setup

## Error
```
User: arn:aws:iam::873601341078:user/gbsuser001 is not authorized to perform: 
bedrock:InvokeModel on resource: 
arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0
```

## Solution

Your AWS user needs the `bedrock:InvokeModel` permission. Follow these steps:

### Option 1: Add Policy via AWS Console (Recommended)

1. **Go to IAM Console:**
   - Open AWS Console: https://console.aws.amazon.com/iam/
   - Navigate to: Users → gbsuser001

2. **Add Inline Policy:**
   - Click "Add inline policy"
   - Choose "JSON" tab
   - Paste the policy below:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "BedrockAccess",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": "arn:aws:bedrock:us-east-1::foundation-model/*"
        }
    ]
}
```

3. **Review and Create:**
   - Click "Review policy"
   - Name it: `BedrockInvokeModelPolicy`
   - Click "Create policy"

### Option 2: Command Line (AWS CLI)

```bash
# Create a policy file
cat > bedrock-policy.json << 'EOF'
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "BedrockAccess",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": "arn:aws:bedrock:us-east-1::foundation-model/*"
        }
    ]
}
EOF

# Add inline policy to your user
aws iam put-user-policy \
    --user-name gbsuser001 \
    --policy-name BedrockInvokeModelPolicy \
    --policy-document file://bedrock-policy.json
```

---

## After Adding the Policy

1. **Wait 1-2 minutes** for the policy to propagate
2. **Run the chatbot:**
   ```bash
   source venv/bin/activate
   python app.py
   ```

---

**Need help?** Contact your AWS administrator or visit: https://docs.aws.amazon.com/bedrock/
