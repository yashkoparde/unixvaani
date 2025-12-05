# CARE-ULTRA Implementation

This repository contains a Python implementation of the **CARE-ULTRA** AI Healthcare Companion logic.

## Logic Overview

The system acts as a triage and support bot that:
1.  **Analyzes Input**: Detects if the user is describing physical symptoms, emotional distress, or both.
2.  **Routes**: Runs `Triage Mode` (Physical) or `Mental Health Mode` (Emotional) logic.
3.  **Generates Output**: Produces a visual ASCII card and a structured JSON payload.

## Usage

Run the script from the command line, providing the user input string as an argument.

```bash
python3 care_ultra.py "I have a severe headache"
```

### Examples

**Physical Symptom (Triage Mode)**
```bash
python3 care_ultra.py "I have a fever and my stomach hurts"
```

**Emotional Support (Mental Health Mode)**
```bash
python3 care_ultra.py "I feel so anxious and stressed about work"
```

**Mixed Input (Both Modes)**
```bash
python3 care_ultra.py "My back hurts and I am feeling very depressed"
```

**Emergency/Crisis (High Urgency)**
```bash
python3 care_ultra.py "I have chest pain and difficulty breathing"
```
```bash
python3 care_ultra.py "I want to end my life"
```

## JSON Output

The script outputs a JSON object at the end of execution, which can be parsed by other applications.

```json
{
  "mode": "triage",
  "urgency": "HIGH",
  "red_flags": ["chest pain"],
  ...
}
```

## Disclaimer

**This tool is NOT a medical device.** It is a prototype for demonstration purposes only. Always seek professional medical help for emergencies.
