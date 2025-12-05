import unittest
import json
from io import StringIO
from unittest.mock import patch
from care_ultra import CareUltra

class TestCareUltra(unittest.TestCase):
    def setUp(self):
        self.app = CareUltra()

    def get_json_output(self, input_text):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.app.analyze(input_text)
            output = fake_out.getvalue()
            # Extract JSON from the end
            lines = output.strip().split('\n')
            # Find the start of JSON (last block)
            json_str = ""
            capture = False
            for line in lines:
                if line.strip().startswith('{'):
                    capture = True
                if capture:
                    json_str += line + "\n"
            
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                return None

    def test_triage_low_urgency(self):
        data = self.get_json_output("I have a mild cough")
        self.assertEqual(data['mode'], 'triage')
        self.assertEqual(data['urgency'], 'LOW')
        self.assertEqual(data['red_flags'], [])

    def test_triage_high_urgency_red_flag(self):
        data = self.get_json_output("I have chest pain")
        self.assertEqual(data['mode'], 'triage')
        self.assertEqual(data['urgency'], 'HIGH')
        self.assertIn("chest pain", data['red_flags'])

    def test_mental_sadness(self):
        data = self.get_json_output("I feel very sad and lonely")
        self.assertEqual(data['mode'], 'mental')
        self.assertEqual(data['emotion'], 'sad')
        self.assertFalse(data['risk_detected'])

    def test_mental_risk(self):
        data = self.get_json_output("I want to end my life")
        self.assertEqual(data['mode'], 'mental')
        self.assertTrue(data['risk_detected'])
        self.assertIsNotNone(data['emergency_instructions'])

    def test_both_modes(self):
        data = self.get_json_output("I have a broken leg and I am depressed")
        self.assertEqual(data['mode'], 'both')
        self.assertIsNotNone(data['urgency'])
        self.assertEqual(data['emotion'], 'sad')

    def test_unknown_mode(self):
        # We need to capture stdout to check for the clarification message
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.app.analyze("I like apples")
            output = fake_out.getvalue()
            self.assertIn("not sure if you are describing physical symptoms", output)

if __name__ == '__main__':
    unittest.main()
