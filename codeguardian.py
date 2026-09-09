"""
CodeGuardian: AI-Powered Code Quality & Technical Debt Detector
Using Google Gemini API for multi-agent code analysis
"""

import requests
import json
import os

# Configuration
API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
MODEL = "gemini-1.5-flash"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

class CodeGuardian:
    """Multi-agent code analysis system using Google Gemini"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or API_KEY
        self.model = MODEL
    
    def complexity_inspector(self, code):
        """Agent 1: Analyze code complexity"""
        prompt = f"""Analyze this code for complexity and maintainability issues.

Code:
{code}

Return a JSON response with these fields:
- complexity_score (0-20 scale)
- maintainability_index (0-100)
- issues (list of code quality issues)
- severity (Low/Medium/High)

Format the response as valid JSON only, no additional text."""
        
        return self._call_gemini(prompt)
    
    def bug_finder(self, code):
        """Agent 2: Find bugs and security vulnerabilities"""
        prompt = f"""Analyze this code for bugs and security vulnerabilities.

Code:
{code}

Return a JSON response with these fields:
- bugs_found (list of identified bugs)
- crash_probability (Low/Medium/High)
- security_issues (list of security vulnerabilities)
- pci_dss_violations (list of PCI-DSS compliance issues)

Format the response as valid JSON only, no additional text."""
        
        return self._call_gemini(prompt)
    
    def intelligent_fixer(self, code):
        """Agent 3: Generate refactored code with improvements"""
        prompt = f"""Suggest improvements and generate refactored code for this function.

Code:
{code}

Return a JSON response with these fields:
- refactored_code (improved version with guard clauses)
- explanation (what was improved and why)
- effort_hours (estimated time to implement)
- roi (business value/ROI of the fix)

Format the response as valid JSON only, no additional text."""
        
        return self._call_gemini(prompt)
    
    def _call_gemini(self, prompt):
        """Call Google Gemini API"""
        url = f"{BASE_URL}/{self.model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            # Extract text from response
            if "contents" in result and len(result["contents"]) > 0:
                if "parts" in result["contents"][0] and len(result["contents"][0]["parts"]) > 0:
                    text = result["contents"][0]["parts"][0]["text"]
                    
                    # Try to parse as JSON
                    try:
                        return json.loads(text)
                    except json.JSONDecodeError:
                        return {"error": "Response is not valid JSON", "raw_response": text}
            
            return {"error": "Unexpected response format", "response": result}
        
        except requests.exceptions.RequestException as e:
            return {"error": f"API call failed: {str(e)}"}
    
    def analyze_complete(self, code):
        """Run complete analysis with all 3 agents"""
        print(" CodeGuardian - Complete Code Analysis\n")
        print("=" * 60)
        
        # Agent 1: Complexity
        print("\n AGENT 1: Complexity Inspector")
        print("-" * 60)
        complexity = self.complexity_inspector(code)
        print(json.dumps(complexity, indent=2))
        
        # Agent 2: Bugs
        print("\n\n AGENT 2: Bug Finder")
        print("-" * 60)
        bugs = self.bug_finder(code)
        print(json.dumps(bugs, indent=2))
        
        # Agent 3: Fixes
        print("\n\n AGENT 3: Intelligent Fixer")
        print("-" * 60)
        fixes = self.intelligent_fixer(code)
        print(json.dumps(fixes, indent=2))
        
        print("\n" + "=" * 60)
        print(" Analysis Complete!")
        
        return {
            "complexity": complexity,
            "bugs": bugs,
            "fixes": fixes
        }

# Example usage
if __name__ == "__main__":
    # Sample code to analyze
    sample_code = """
    function processPayment(amount, card, user) {
        var total = amount;
        var tax = amount * 0.1;
        if (card) {
            if (card.number) {
                if (card.cvv) {
                    console.log("Charging: " + amount);
                    return true;
                }
            }
        }
    }
    """
    
    # Initialize CodeGuardian
    guardian = CodeGuardian()
    
    # Run analysis
    results = guardian.analyze_complete(sample_code)
