import os

class NameChecker:
    def __init__(self):
        self.common_names = set()
        self._load_names()

    def _load_names(self):
        """Load common English names from namedb file"""
        try:
            namedb_path = os.path.join(os.path.dirname(__file__), 'namedb.txt')
            if os.path.exists(namedb_path):
                with open(namedb_path, 'r') as f:
                    self.common_names = {name.strip().lower() for name in f.readlines()}
            else:
                # Fallback to basic common names if file doesn't exist
                self.common_names = {
                    'james', 'john', 'robert', 'michael', 'william', 'david', 'richard', 'joseph',
                    'thomas', 'charles', 'mary', 'patricia', 'jennifer', 'linda', 'elizabeth',
                    'barbara', 'susan', 'jessica', 'sarah', 'karen', 'margaret', 'lisa', 'betty',
                    'dorothy', 'sandra', 'ashley', 'kimberly', 'donna', 'emily', 'michelle',
                    'carol', 'amanda', 'melissa', 'deborah', 'stephanie', 'rebecca', 'laura',
                    'helen', 'sharon', 'cynthia', 'amy', 'shirley', 'angela', 'anna', 'ruth',
                    'jack', 'peter', 'paul', 'mark', 'donald', 'george', 'kenneth', 'steven',
                    'edward', 'brian', 'ronald', 'anthony', 'kevin', 'jason', 'matthew', 'gary',
                    'timothy', 'jose', 'larry', 'jeffrey', 'frank', 'scott', 'eric', 'stephen',
                    'andrew', 'raymond', 'gregory', 'joshua', 'jerry', 'dennis', 'walter', 'patrick',
                    'peter', 'harold', 'douglas', 'henry', 'carl', 'arthur', 'ryan', 'roger'
                }
        except Exception as e:
            print(f"Error loading names: {str(e)}")
            self.common_names = set()

    def is_name(self, word):
        """Check if a word is likely a name"""
        return word.lower() in self.common_names

    def extract_names(self, text):
        """Extract likely names from a piece of text"""
        # Split text into words
        words = text.replace('-', ' ').replace('_', ' ').split()
        
        # Look for consecutive capitalized words that might be names
        names = []
        for i in range(len(words)):
            word = words[i].strip('.,!?()[]{}')
            if (word and word[0].isupper() and  # Word is capitalized
                (self.is_name(word) or          # Is in our name database
                 (i > 0 and words[i-1][0].isupper() and self.is_name(words[i-1])))):  # Previous word was a name
                names.append(word)
        
        # Join consecutive name words
        result = []
        current_name = []
        for name in names:
            if not current_name or (len(current_name) == 1 and self.is_name(name)):
                current_name.append(name)
            else:
                if current_name:
                    result.append(' '.join(current_name))
                current_name = [name]
        
        if current_name:
            result.append(' '.join(current_name))
        
        return result