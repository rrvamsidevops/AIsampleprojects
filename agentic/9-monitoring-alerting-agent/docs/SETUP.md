# Setup Guide: Monitoring & Alerting Agent

## Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- AWS Account with Bedrock access
- `.env` file with AWS credentials

## Installation Steps

### 1. Create Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure AWS Credentials
Create a `.env` file in the project root:
```
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

Or use AWS CLI configuration:
```bash
aws configure
```

### 4. Verify Installation
```bash
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

python -m pytest test_*.py -v
```

## Running the Application

### Interactive Mode
```bash
source venv/bin/activate
python app.py
```

### With Logging
```bash
export LOG_LEVEL=DEBUG  # macOS/Linux
# OR
set LOG_LEVEL=DEBUG  # Windows
python app.py
```

## Troubleshooting

### "No module named 'boto3'"
- Ensure venv is activated: `source venv/bin/activate`
- Reinstall requirements: `pip install -r requirements.txt`

### AWS Credentials Error
- Verify `.env` file exists and has correct credentials
- Check AWS_REGION is set to `us-east-1`
- Run: `aws sts get-caller-identity` to verify AWS access

### Bedrock Model Not Found
- Confirm Bedrock is available in your AWS region (us-east-1 recommended)
- Check IAM permissions for `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream`

## Project Dependencies
```
[
  "boto3>=1.28.0",
  "python-dotenv"
]
```

See `requirements.txt` for the complete dependency list.
