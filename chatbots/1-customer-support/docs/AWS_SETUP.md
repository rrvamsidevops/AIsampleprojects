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

### Option 3: Ask Your AWS Admin

If you don't have IAM permissions to add policies, ask your AWS account administrator to attach the policy above to your user.

---

## Verification

Once the policy is attached, test the permission:

```bash
aws iam list-user-policies --user-name gbsuser001
```

You should see `BedrockInvokeModelPolicy` in the output.

---

## What This Policy Does

- `bedrock:InvokeModel` - Allows you to call Bedrock models (like Claude)
- `bedrock:InvokeModelWithResponseStream` - Allows streaming responses
- `Resource: arn:aws:bedrock:us-east-1::foundation-model/*` - Applies to all Bedrock models in us-east-1

---

## After Adding the Policy

1. **Wait 1-2 minutes** for the policy to propagate
2. **Run the chatbot again:**
   ```bash
   source venv/bin/activate
   python app.py
   ```
3. Try: `how to reset my password?`

---

## Still Getting Errors?

If you still get permission errors:

1. **Check your configured credentials:**
   ```bash
   aws sts get-caller-identity
   ```
   Make sure the user matches `gbsuser001`

2. **Refresh credentials:**
   ```bash
   aws configure
   ```
   Re-enter your Access Key and Secret

3. **Check region:**
   Make sure your region is `us-east-1` (where Bedrock is available)

---

## Supported Bedrock Regions

Bedrock is available in these regions:
- us-east-1 ✓ (recommended)
- us-west-2
- eu-west-1
- ap-northeast-1

---

**Need help?** Contact your AWS administrator or visit: https://docs.aws.amazon.com/bedrock/
