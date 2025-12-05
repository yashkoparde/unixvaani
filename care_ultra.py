#!/usr/bin/env python3
import sys
import json
import time

class CareUltra:
    def __init__(self):
        # Red flags: Key phrases that indicate high urgency
        self.red_flags = [
            "chest pain", "difficulty breathing", "hard to breathe", "shortness of breath",
            "sudden severe headache", "severe headache", "worst headache",
            "sudden confusion", "confused", "delirious",
            "uncontrolled bleeding", "bleeding heavily", "profuse bleeding",
            "fainting", "collapse", "passed out", "blacked out"
        ]
        
        self.physical_keywords = [
            "pain", "ache", "fever", "bleed", "broken", "stomach", "cough", 
            "cold", "flu", "dizzy", "vomit", "nausea", "rash", "swelling", 
            "burn", "hurt", "headache", "injury", "wound", "symptom", "temperature"
        ]
        
        self.mental_keywords = [
            "sad", "happy", "anxious", "stress", "depress", "cry", "fear", 
            "lonely", "overwhelm", "angry", "anger", "feeling", "mood", 
            "emotion", "upset", "nervous", "tired of life", "hopeless", 
            "despair", "grief", "guilt", "shame", "panic"
        ]
        
        self.risk_phrases = [
            "suicide", "want to die", "end my life", "kill myself", 
            "hurt myself", "take my own life", "better off dead"
        ]

    def analyze(self, user_input):
        print("⏳ Processing…")
        time.sleep(0.5)
        print("🔍 Analyzing input…")
        time.sleep(0.5)
        print("✨ Generating your report…")
        time.sleep(0.5)
        print("") # Newline

        mode = self.determine_mode(user_input)
        language = "English" # Note: Full multilingual support requires external NLP libraries.
        
        result_json = {
            "mode": mode,
            "language": language,
            "urgency": None,
            "red_flags": [],
            "possible_causes": [],
            "action_steps": None,
            "follow_up_questions": [],
            "emotion": None,
            "risk_detected": False,
            "coping_exercise": None,
            "affirmations": [],
            "emergency_instructions": None
        }

        triage_output = ""
        mental_output = ""

        if mode == "triage" or mode == "both":
            triage_data = self.run_triage_mode(user_input)
            result_json.update(triage_data)
            triage_output = self.format_triage_card(triage_data)

        if mode == "mental" or mode == "both":
            mental_data = self.run_mental_mode(user_input)
            result_json.update(mental_data)
            mental_output = self.format_mental_card(mental_data)

        if mode == "unknown":
            print("❓ I am not sure if you are describing physical symptoms or emotional distress.")
            print("Could you please clarify?")
            return

        # Visual Output
        if triage_output:
            print(triage_output)
        
        if mental_output:
            if triage_output:
                print("\n") # Separation
            print(mental_output)
            
        if mode == "both":
            print("\n━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("ℹ️  Merged Summary: You seem to be dealing with both physical and emotional challenges.")
            print("Please prioritize any high urgency physical symptoms and safety risks.")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━")

        # Final JSON
        print("\n" + json.dumps(result_json, indent=2))

    def determine_mode(self, text):
        text = text.lower()
        # Check for matches
        has_physical_kw = any(k in text for k in self.physical_keywords)
        has_red_flags = any(k in text for k in self.red_flags)
        
        has_mental_kw = any(k in text for k in self.mental_keywords)
        has_risk = any(k in text for k in self.risk_phrases)
        
        is_physical = has_physical_kw or has_red_flags
        is_mental = has_mental_kw or has_risk
        
        if is_physical and is_mental:
            return "both"
        elif is_physical:
            return "triage"
        elif is_mental:
            return "mental"
        else:
            return "unknown"

    def run_triage_mode(self, text):
        text = text.lower()
        detected_red_flags = [rf for rf in self.red_flags if rf in text]
        
        # Determine urgency
        if detected_red_flags:
            urgency = "HIGH"
            action = "Seek immediate emergency medical attention. Go to the ER or call emergency services."
            causes = ["Medical Emergency", "Severe Condition"]
        else:
            # Medium logic: severe pain, high fever
            if "severe" in text or "bad" in text or "high fever" in text or "extreme" in text:
                urgency = "MEDIUM"
                action = "Contact a healthcare provider today."
                causes = ["Acute Infection", "Inflammation", "Migraine/Pain"]
            else:
                urgency = "LOW"
                action = "Monitor symptoms. Rest and hydrate. Consult a doctor if symptoms persist."
                causes = ["Common Cold", "Minor Strain", "Fatigue", "Viral infection"]

        # Dynamic questions
        questions = []
        if urgency == "HIGH":
            questions = ["Are you alone right now?", "Can you call 911/Emergency Services?"]
        else:
            questions = ["How long have you had these symptoms?", "Is the pain getting worse?"]

        return {
            "urgency": urgency,
            "red_flags": detected_red_flags,
            "possible_causes": causes,
            "action_steps": action,
            "follow_up_questions": questions
        }

    def format_triage_card(self, data):
        red_flags_str = "Yes (" + ", ".join(data['red_flags']) + ")" if data['red_flags'] else "No"
        causes_str = "\n".join([f"• {c}" for c in data['possible_causes']])
        questions_str = "\n".join([f"{i+1}. {q}" for i, q in enumerate(data['follow_up_questions'])])

        return f"""🩺 SYMPTOM TRIAGE REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━
🌡 Summary: Analysis of reported physical symptoms.
🚨 Urgency Level: {data['urgency']}
⚠️ Red Flags Detected: {red_flags_str}
❤️‍🩹 Possible Causes:
{causes_str}
📌 Recommended Action:
{data['action_steps']}
❓ Follow-up:
{questions_str}
━━━━━━━━━━━━━━━━━━━━━━━━━
🔒 Not a diagnosis. Seek medical help for emergencies."""

    def run_mental_mode(self, text):
        text = text.lower()
        risk = any(p in text for p in self.risk_phrases)
        
        # Emotion mapping
        emotion = "neutral"
        if any(w in text for w in ["sad", "depress", "lonely", "grief", "hopeless", "despair"]): emotion = "sad"
        elif any(w in text for w in ["anxious", "fear", "nervous", "panic"]): emotion = "anxious"
        elif any(w in text for w in ["anger", "angry", "mad", "upset"]): emotion = "angry"
        elif any(w in text for w in ["stress", "overwhelm", "pressure"]): emotion = "stressed"
        elif any(w in text for w in ["happy", "good", "joy", "excited"]): emotion = "happy"
        
        # Fallback emotion if risk detected but no emotion found
        if risk and emotion == "neutral":
            emotion = "overwhelmed/crisis"

        coping = "Take a deep breath. Inhale for 4 seconds, hold for 7, exhale for 8."
        affirmations = ["You are strong.", "This feeling will pass."]
        emergency = None

        if risk:
            coping = "Please reach out for help immediately."
            affirmations = ["You are not alone.", "Help is available.", "Your life matters."]
            emergency = "CALL EMERGENCY SERVICES OR A SUICIDE PREVENTION HOTLINE IMMEDIATELY."

        return {
            "emotion": emotion,
            "risk_detected": risk,
            "coping_exercise": coping,
            "affirmations": affirmations,
            "emergency_instructions": emergency
        }

    def format_mental_card(self, data):
        risk_str = "YES" if data['risk_detected'] else "No"
        
        card = f"""💙 EMOTIONAL SUPPORT PANEL
━━━━━━━━━━━━━━━━━━━━━━━━━
🧭 Detected Emotion: {data['emotion']}
🌈 Supportive Message:
We are here for you. Your feelings are valid."""

        if data['risk_detected']:
            card += f"""
⚠️ Risk Check: {risk_str}
━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 CRISIS SAFETY ALERT 🚨
{data['emergency_instructions']}
Please contact a trusted person or emergency services now.
━━━━━━━━━━━━━━━━━━━━━━━━━"""
        else:
            aff_str = "\n".join([f"• {a}" for a in data['affirmations']])
            card += f"""
🧘 Coping Exercise:
{data['coping_exercise']}
✨ Personalized Affirmations:
{aff_str}
⚠️ Risk Check: {risk_str}
━━━━━━━━━━━━━━━━━━━━━━━━━"""
             
        return card

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        print("Please provide input as arguments.")
        sys.exit(1)
        
    app = CareUltra()
    app.analyze(user_input)
