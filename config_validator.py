import os
from typing import List, Dict

class ConfigValidator:
    @staticmethod
    def validate_environment() -> Dict[str, List[str]]:
        """
        Validates that all required environment variables are set.
        Returns a dictionary with 'missing' and 'present' lists of variables.
        """
        required_vars = {
            'FLASK_ENV': 'Application environment (development/production)',
            'PORT': 'Port number for the application to run on',
            'MISTRAL_API_URL': 'Mistral API endpoint URL',
            'MISTRAL_API_KEY': 'Authentication key for Mistral API'
        }
        
        missing = []
        present = []
        
        for var, description in required_vars.items():
            if not os.getenv(var):
                missing.append(f"{var} - {description}")
            else:
                present.append(var)
        
        return {
            'missing': missing,
            'present': present
        }

    @staticmethod
    def check_configuration() -> bool:
        """
        Checks if all required configuration is present.
        Returns True if all required variables are set, False otherwise.
        """
        validation_results = ConfigValidator.validate_environment()
        
        if validation_results['missing']:
            print("❌ Missing required environment variables:")
            for var in validation_results['missing']:
                print(f"   - {var}")
            print("\n✅ Present environment variables:")
            for var in validation_results['present']:
                print(f"   - {var}")
            return False
        
        print("✅ All required environment variables are set:")
        for var in validation_results['present']:
            print(f"   - {var}")
        return True