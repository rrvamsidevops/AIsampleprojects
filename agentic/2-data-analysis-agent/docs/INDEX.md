# Documentation Index

## Quick Navigation

### Getting Started
- **[README](../README.md)** - Project overview & quick start
- **[SETUP.md](SETUP.md)** - Detailed setup & configuration
- **[TESTING.md](TESTING.md)** - Testing strategies & validation

### Architecture
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design & components (if available)

---

## Common Tasks

### I want to...

**Run the application**
```bash
source venv/bin/activate
python app.py
```

**Run tests**
```bash
# Unit tests
python test_*.py

# All tests
ls test_*.py | xargs -I {} python {}
```

**Update dependencies**
```bash
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

**Check logs**
```bash
tail -f logs/*.log
```

**Configure AWS credentials**
```bash
aws configure
```

---

## Project Structure

```
├── README.md                # Project overview
├── docs/                    # Documentation
│   ├── INDEX.md            # This file
│   ├── SETUP.md            # Detailed setup
│   ├── TESTING.md          # Testing guide
│   └── ARCHITECTURE.md     # System design
├── app.py / agent.py       # Main application
├── config.py               # Configuration
├── requirements.txt        # Dependencies
├── setup.sh / setup.bat    # Automated setup
├── test_*.py              # Test files
├── prompts/               # LLM prompts & examples
├── utils/                 # Utility modules
├── data/                  # Sample/test data
├── logs/                  # Application logs
└── venv/                  # Virtual environment
```

---

## Virtual Environment

This project uses isolated virtual environments:

```bash
# Activate
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

# Deactivate
deactivate
```

**Benefits:**
- ✅ Dependency isolation
- ✅ No system Python conflicts
- ✅ Easy reproducibility
- ✅ Project-specific packages

---

## Troubleshooting

### Virtual Environment Issues
```bash
# Recreate from scratch
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Python/Dependency Issues
```bash
# Check Python version
python --version  # Should be 3.9+

# Upgrade pip
pip install --upgrade pip

# Check installed packages
pip list
```

### AWS/API Issues
```bash
# Verify credentials
aws sts get-caller-identity

# Reconfigure
aws configure
```

---

## Next Steps

1. Read [README.md](../README.md) for project overview
2. Follow [SETUP.md](SETUP.md) for configuration
3. Run [TESTING.md](TESTING.md) to validate setup
4. Review [ARCHITECTURE.md](ARCHITECTURE.md) to understand design
5. Start developing!

---

**For questions**, check the relevant documentation file above or the project README.
