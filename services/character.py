from utils.logger import logger

class CharacterExtractor:
    @staticmethod
    def extract_name_from_filename(filename):
        """Extract potential character name from filename"""
        try:
            # Remove file extension and common prefixes/suffixes
            name = filename.lower()
            name = name.replace('.txt', '')
            name = name.replace('interview_', '')
            name = name.replace('transcript_', '')
            name = name.replace('_interview', '')
            name = name.replace('_transcript', '')
            
            # Split on common separators and get the longest part
            parts = name.replace('_', ' ').replace('-', ' ').split()
            if parts:
                # Get the longest word that's not a common word
                common_words = {'with', 'and', 'the', 'transcript', 'interview'}
                potential_names = [p for p in parts if p not in common_words and len(p) > 2]
                if potential_names:
                    return max(potential_names, key=len).title()
            return None
        except Exception as e:
            logger.error(f"Error extracting name from filename: {str(e)}")
            return None

    @staticmethod
    def is_likely_interviewer(name):
        """Check if the name appears to be an interviewer designation"""
        interviewer_terms = {'interviewer', 'moderator', 'host', 'questioner', 'reporter', 'journalist'}
        name_lower = name.lower()
        return any(term in name_lower for term in interviewer_terms)

    @staticmethod
    def extract_characters(content, filename=None):
        """Extract character names from text and filename"""
        try:
            potential_chars = set()
            lines = content.split("\n")
            speaker_counts = {}  # Track how often each speaker appears
            
            # First pass: count speaker occurrences
            for line in lines:
                if ':' in line:
                    speaker = line.split(":")[0].strip()
                    # Remove any parenthetical notes
                    if '(' in speaker:
                        speaker = speaker.split('(')[0].strip()
                    if speaker:
                        # Convert to title case but preserve internal spacing
                        speaker = ' '.join(word.capitalize() for word in speaker.split())
                        speaker_counts[speaker] = speaker_counts.get(speaker, 0) + 1

            # Second pass: analyze the content more thoroughly
            for i, line in enumerate(lines):
                # Look for dialogue patterns
                if ':' in line:
                    speaker = line.split(":")[0].strip()
                    if '(' in speaker:
                        speaker = speaker.split('(')[0].strip()
                    # Convert to title case preserving internal spacing
                    speaker = ' '.join(word.capitalize() for word in speaker.split())
                    
                    # Only consider speakers that appear multiple times and aren't likely interviewers
                    if (speaker_counts.get(speaker, 0) >= 2 and
                        len(speaker) > 1 and
                        not CharacterExtractor.is_likely_interviewer(speaker) and
                        not any(char.isdigit() for char in speaker) and
                        not any(char in speaker for char in '[]{}<>/@#$%^&*')):
                        potential_chars.add(speaker)
                
                # Look for screenplay format - now supports mixed case properly formatted names
                elif len(line.strip()) > 1:
                    # Split into words and check if it looks like a name (1-3 words, all alphabetic)
                    words = line.strip().split()
                    if (1 <= len(words) <= 3 and  # Allow for middle names/initials
                        all(word.isalpha() for word in words) and
                        i < len(lines) - 1 and 
                        lines[i + 1].strip() and 
                        not all(w.isupper() for w in lines[i + 1].strip().split())):
                        
                        potential_char = ' '.join(word.capitalize() for word in words)
                        if (len(potential_char) > 1 and
                            not CharacterExtractor.is_likely_interviewer(potential_char) and
                            not any(char.isdigit() for char in potential_char) and
                            not any(char in potential_char for char in '[]{}<>/@#$%^&*')):
                            potential_chars.add(potential_char)

            # Add name from filename if it exists
            if filename:
                name_from_file = CharacterExtractor.extract_name_from_filename(filename)
                if name_from_file:
                    potential_chars.add(name_from_file)

            # Remove any characters that appear to be interviewers
            final_chars = {char for char in potential_chars 
                         if not CharacterExtractor.is_likely_interviewer(char)}

            logger.debug(f"Extracted characters: {final_chars}")
            return final_chars
        except Exception as e:
            logger.error(f"Error extracting characters: {str(e)}")
            raise Exception(f"Error extracting characters: {str(e)}")