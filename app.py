from flask import Flask, render_template, request
import re
import random
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from typing import List
import os # Import os for path manipulation
import sys # Import sys for controlled exit on failure

# Initialize Flask app
app = Flask(__name__)

# --- CRITICAL NLTK Data Configuration for Vercel ---
# Vercel places bundled files, like 'nltk_data', in the root of the Lambda execution environment.
# We must explicitly tell NLTK where to look.
try:
    # 1. Set the path to the bundled nltk_data directory
    nltk_data_path = os.path.join(os.getcwd(), "nltk_data")
    
    if os.path.isdir(nltk_data_path):
        nltk.data.path.append(nltk_data_path)
        print(f"INFO: NLTK data path successfully added: {nltk_data_path}")
    else:
        # This should only happen if vercel.json or the nltk_data folder is missing
        print(f"FATAL WARNING: NLTK data path not found at {nltk_data_path}.")
    
    # 2. Force a test load of all required components to raise any LookupError early.
    # We use these modules later: punkt (for tokenizing), averaged_perceptron_tagger (for pos_tag), wordnet.
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('taggers/averaged_perceptron_tagger')
    nltk.data.find('corpora/wordnet')
    print("INFO: All required NLTK data verified.")

except LookupError as e:
    # This is the most likely failure mode on Vercel: data is missing or path is wrong.
    print(f"FATAL ERROR: NLTK data missing: {e}. Please ensure the 'nltk_data' folder is bundled and contains all required files (punkt, averaged_perceptron_tagger, wordnet).")
    # For a critical dependency like this, it's better to crash explicitly for debugging
    # than to have a silent Internal Server Error on every request.
    sys.exit(1) # Crash the application startup
except Exception as e:
    # General catch for other initialization issues
    print(f"NLTK configuration failed for an unknown reason: {e}.")
    sys.exit(1) # Crash the application startup


class TextHumanizer:
# ... (The rest of your TextHumanizer class methods are already fine) ...
# I am including the full class below for completeness but it is unchanged.

    def __init__(self):
        # List of functions used for sentence-level variation
        self.sentence_variations = [
            self.vary_sentence_lengths,
            self.add_academic_transitions,
            self.use_synonyms,
            self.restructure_sentences,
            self.add_academic_depth,
            self.vary_connectors,
            self.add_scholarly_elements,
            self.add_mock_citations, 
            self.add_quantitative_language
        ]
    
    def split_into_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs based on double line breaks"""
        paragraphs = re.split(r'\n\s*\n|\r\n\s*\r\n', text.strip())
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        return paragraphs
    
    def humanize(self, text: str, intensity: int = 3) -> str:
        """Applies a single humanization pass across paragraphs and sentences."""
        paragraphs = self.split_into_paragraphs(text)
        humanized_paragraphs = []
        
        # Max intensity is 5 (5 variations applied per sentence)
        intensity = min(max(1, intensity), 5)

        for paragraph in paragraphs:
            sentences = sent_tokenize(paragraph)
            humanized_sentences = []
            
            for sentence in sentences:
                current_sentence = sentence
                # Apply 'intensity' number of random transformations
                for _ in range(intensity):
                    transform = random.choice(self.sentence_variations)
                    current_sentence = transform(current_sentence)
                
                humanized_sentences.append(current_sentence)
            
            paragraph_text = ' '.join(humanized_sentences)
            paragraph_text = self.add_human_touches(paragraph_text)
            humanized_paragraphs.append(paragraph_text)
        
        return '\n\n'.join(humanized_paragraphs)
    
    def deep_think_humanize(self, text: str, cycles: int = 5) -> str:
        """
        Deep Think Mode: Iteratively humanizes text multiple times, applying 
        maximum intensity in each cycle to achieve highly sophisticated output.
        """
        current_text = text
        cycles = min(max(1, cycles), 8) # Limit cycles to 8 for performance

        for cycle in range(cycles):
            # Apply standard humanization with high intensity
            current_text = self.humanize(current_text, intensity=5)
            
            # Apply cycle variation for layering effects (structural shifts)
            if cycle < cycles - 1:
                current_text = self.add_cycle_variation(current_text, cycle)
            
        return current_text
    
    def add_cycle_variation(self, text: str, cycle_num: int) -> str:
        """Adds subtle, structural variations between deep think cycles."""
        paragraphs = self.split_into_paragraphs(text)
        varied_paragraphs = []
        
        for paragraph in paragraphs:
            # Different structural variations for different cycles
            if cycle_num % 2 == 0:
                paragraph = self.vary_academic_rhythm(paragraph)
            elif cycle_num % 3 == 0:
                paragraph = self.add_analytical_elements(paragraph)
            else:
                paragraph = self.add_academic_transitions(paragraph) 
            
            varied_paragraphs.append(paragraph)
        
        return '\n\n'.join(varied_paragraphs)
    
    # --- CORE TRANSFORMATION METHODS ---

    def add_mock_citations(self, text: str) -> str:
        """NEW FEATURE: Inserts mock parenthetical citations (Author, Year)."""
        if random.random() < 0.2: # 20% chance per call
            citations = [
                "(Smith, 2023)", "(Chen & Li, 2021)", "(Brown et al., 2024)", 
                "(Johnson, 2022)", "(Williams, 2020)", "(Data Source, n.d.)"
            ]
            sentences = sent_tokenize(text)
            
            for i, sentence in enumerate(sentences):
                # Try to place the citation before the end of a sentence
                if random.random() < 0.3:
                    period_index = sentence.rfind('.')
                    if period_index != -1 and len(sentence.split()) > 5:
                        # Insert citation just before the final period
                        sentences[i] = sentence[:period_index] + " " + random.choice(citations) + sentence[period_index:]
                        break # Only add one citation per setence call
            text = ' '.join(sentences)

        return text

    def add_quantitative_language(self, text: str) -> str:
        """NEW FEATURE: Adds quantitative modifiers to make statements less absolute."""
        quantitative_modifiers = [
            "approximately", "nearly", "a significant proportion of", 
            "a majority of", "substantially", "marginally"
        ]
        
        # Target common starting phrases or verbs
        patterns = {
            r'(The evidence|Data) (shows|suggests)': r'\1 strongly indicates that',
            r'(It is|This is) (a|the) (key|major)': lambda m: f"{m.group(1)} {random.choice(quantitative_modifiers)} {m.group(2)} {m.group(3)}",
            r'All (\w+) are': r'Nearly all \1 are',
            r'Every (\w+) is': r'A majority of \1 are'
        }

        for pattern, replacement in patterns.items():
            if re.search(pattern, text, re.IGNORECASE) and random.random() < 0.3:
                # Replacement can be a string or a function, handle both
                if callable(replacement):
                    text = re.sub(pattern, replacement, text, 1, re.IGNORECASE)
                else:
                    text = re.sub(pattern, replacement, text, 1, re.IGNORECASE)
                break
        
        return text

    def add_academic_transitions(self, text: str) -> str:
        """Add academic transition phrases (e.g., 'Furthermore,', 'Moreover,') to sentences."""
        academic_transitions = [
            ('Furthermore,', 0.2), ('Moreover,', 0.15), ('Additionally,', 0.2), 
            ('In contrast,', 0.1), ('Subsequently,', 0.1), ('Consequently,', 0.1), 
            ('Nevertheless,', 0.1), ('Thus,', 0.15), ('Hence,', 0.1)
        ]
        
        sentences = sent_tokenize(text)
        if len(sentences) > 1 and random.random() < 0.4:
            idx = random.randint(1, len(sentences) - 1)
            phrase, _ = random.choice(academic_transitions)
            
            # Simple check to avoid double-transition words
            if not sentences[idx].lower().startswith(tuple(p[0].lower() for p in academic_transitions)):
                # Capitalize the transition word, then make the start of the next word lowercase
                # to fix capitalization issues introduced by word_tokenize's default output.
                sent_start = sentences[idx].strip()
                if sent_start and sent_start[0].isupper():
                    sentences[idx] = phrase + ' ' + sent_start[0].lower() + sent_start[1:]
                else:
                    sentences[idx] = phrase + ' ' + sent_start
            
        return ' '.join(sentences)
    
    def add_scholarly_elements(self, text: str) -> str:
        """Add scholarly depth and academic language prefixes."""
        scholarly_phrases = [
            "It is important to note that", "Research indicates that", 
            "Studies have shown that", "Evidence suggests that", 
            "Analysis reveals that", "It can be argued that", 
            "This demonstrates that", "The findings indicate that"
        ]
        
        if random.random() < 0.25:
            phrase = random.choice(scholarly_phrases)
            sentences = sent_tokenize(text)
            if sentences and not sentences[0].startswith(tuple(p.split()[0] for p in scholarly_phrases)):
                # Ensure capitalization is handled correctly after prefix
                start_of_sentence = sentences[0].split()
                if start_of_sentence:
                    start_of_sentence[0] = start_of_sentence[0].lower()
                    sentences[0] = phrase + " " + ' '.join(start_of_sentence)
                
            text = ' '.join(sentences)
        
        return text
    
    def vary_academic_rhythm(self, text: str) -> str:
        """Create varied academic sentence structures by adding connectors."""
        sentences = sent_tokenize(text)
        varied_sentences = []
        
        for i, sentence in enumerate(sentences):
            if i > 0 and random.random() < 0.15:
                # Add academic connectors
                connectors = ["Furthermore,", "In addition,", "Similarly,", "Conversely,", "Notably,"]
                if not sentence.startswith(tuple(c.strip() for c in connectors)):
                    # Ensure capitalization is handled correctly
                    start_of_sentence = sentence.strip()
                    if start_of_sentence and start_of_sentence[0].isupper():
                        sentence = random.choice(connectors) + " " + start_of_sentence[0].lower() + start_of_sentence[1:]
                    else:
                        sentence = random.choice(connectors) + " " + start_of_sentence
            varied_sentences.append(sentence)
        
        return ' '.join(varied_sentences)
    
    def add_analytical_elements(self, text: str) -> str:
        """Add analytical and critical thinking elements as follow-up phrases."""
        analytical_additions = [
            " This analysis suggests", " These findings imply", 
            " The evidence demonstrates", " This examination reveals", 
            " The data indicates"
        ]
        
        sentences = sent_tokenize(text)
        if sentences and random.random() < 0.2:
            last_sentence = sentences[-1]
            if last_sentence.endswith('.'):
                addition = random.choice(analytical_additions)
                analytical_conclusions = [
                    " significant implications for the field.", " the complexity of the subject matter.", 
                    " important considerations for future research.", 
                    " the need for further investigation.", 
                    " valuable insights into the phenomenon."
                ]
                conclusion = random.choice(analytical_conclusions)
                
                # Combine the last sentence with a new analytical statement
                sentences[-1] = last_sentence[:-1] + "." + addition + conclusion
        
        return ' '.join(sentences)
    
    def get_synonyms(self, word: str, pos: str = None) -> List[str]:
        """Retrieve single-word synonyms for a given word and POS tag using WordNet."""
        synonyms = set()
        pos_mapping = {
            'NN': wordnet.NOUN, 'JJ': wordnet.ADJ, 
            'VB': wordnet.VERB, 'RB': wordnet.ADV
        }
        
        wordnet_pos = pos_mapping.get(pos[:2], None) if pos else None
        
        try:
            for syn in wordnet.synsets(word, pos=wordnet_pos):
                for lemma in syn.lemmas():
                    synonym = lemma.name().replace('_', ' ')
                    # Ensure the synonym is a single word and different from the original
                    if synonym.lower() != word.lower() and len(synonym.split()) == 1:
                        synonyms.add(synonym)
        except:
            # Handle potential NLTK LookupError if data is missing
            pass 
        return list(synonyms)
    
    def vary_sentence_lengths(self, text: str) -> str:
        """Break up complex sentences into multiple, shorter ones or merge short ones."""
        
        # 30% chance to break up long sentences
        if random.random() < 0.3:
            clauses = re.split(r'[,;]', text)
            if len(clauses) > 1 and random.random() < 0.5:
                # Rejoin as separate sentences
                return '. '.join([c.strip().capitalize() for c in clauses if c.strip()]) + '.'
        
        # 10% chance to merge two sentences (if short enough)
        sentences = sent_tokenize(text)
        if len(sentences) >= 2 and random.random() < 0.1:
            # Merge the first two sentences using a formal connector
            if len(sentences[0].split()) < 15 and len(sentences[1].split()) < 15:
                connector = random.choice(["consequently,", "nonetheless,", "similarly,", "furthermore,"])
                s1 = sentences[0].rstrip('.')
                s2 = sentences[1].strip().lower()
                new_sentence = f"{s1}; {connector} {s2}"
                return new_sentence + ' '.join(sentences[2:])

        return text
    
    def add_academic_depth(self, text: str) -> str:
        """Adds academic depth and elaboration within a sentence."""
        depth_phrases = [
            'which is further supported by the data', 
            'a position consistent with extant literature', 
            'thus emphasizing the complexity of the phenomenon', 
            'thereby forming the basis of this investigation'
        ]
        
        # Target internal comma points or phrase transitions
        if random.random() < 0.2:
            insertions = re.split(r',', text, 1) # Split on first comma
            if len(insertions) == 2:
                text = insertions[0] + ', ' + random.choice(depth_phrases) + ', ' + insertions[1]
            
        return text
    
    def use_synonyms(self, text: str) -> str:
        """Replace nouns, adjectives, and verbs with appropriate synonyms."""
        words = word_tokenize(text)
        
        try:
            pos_tags = nltk.pos_tag(words)
        except:
            return text
        
        new_words = []
        for word, tag in pos_tags:
            # Target Nouns (NN), Adjectives (JJ), and Verbs (VB)
            if tag.startswith('NN') or tag.startswith('JJ') or tag.startswith('VB'):
                if random.random() < 0.3:
                    syns = self.get_synonyms(word, tag)
                    if syns:
                        new_words.append(random.choice(syns))
                        continue
            new_words.append(word)
        
        # Rejoin tokens while preserving punctuation spacing
        text_rejoined = ' '.join(new_words)
        text_rejoined = re.sub(r'\s([.,;:])', r'\1', text_rejoined)
        text_rejoined = re.sub(r'([$(])\s', r'\1', text_rejoined)
        text_rejoined = re.sub(r'\s([$)])', r'\1', text_rejoined)
        return text_rejoined
    
    def restructure_sentences(self, text: str) -> str:
        """Change informal or simple sentence structures to more formal, academic patterns."""
        patterns = [
            (r'(\w+) is (\w+)', r'\1 can be characterized as \2'),
            (r'It is (.*?) that', r'Research demonstrates that'),
            (r'There are (.*?) that', r'Analysis reveals \1 which'),
            (r'The (.*?) of (.*?) is', r'\2 exhibits a \1 that is'),
            (r'This shows', r'This evidence demonstrates'),
            (r'We can see', r'It becomes evident'),
            (r'It\'s clear that', r'The data clearly indicates that')
        ]
        
        for pattern, replacement in patterns:
            if re.search(pattern, text, re.IGNORECASE) and random.random() < 0.4:
                text = re.sub(pattern, replacement, text, 1, re.IGNORECASE) # Replace only once
                break
        return text
    
    def vary_connectors(self, text: str) -> str:
        """Vary common connectors (like 'but', 'so') to more formal equivalents."""
        connectors = {
            'however': ['nevertheless', 'nonetheless', 'conversely', 'in contrast'],
            'therefore': ['consequently', 'thus', 'hence', 'as a result'],
            'additionally': ['furthermore', 'moreover', 'in addition', 'similarly'],
            'but': ['however', 'nevertheless', 'conversely', 'in contrast'],
            'so': ['therefore', 'consequently', 'thus', 'hence']
        }
        
        # Use regex to target words followed by a comma (common connector pattern)
        for informal, formal_list in connectors.items():
            pattern = re.compile(rf'\b{informal}\s*,', re.IGNORECASE)
            if re.search(pattern, text) and random.random() < 0.6:
                replacement = random.choice(formal_list).capitalize() + ','
                text = re.sub(pattern, replacement, text, 1)
        
        return text
    
    def add_human_touches(self, text: str) -> str:
        """Final cleanup and addition of general academic writing features."""
        
        # Add formal qualifiers to the end of a sentence
        if random.random() < 0.15:
            qualifiers = [
                ' according to current research', ' based on available evidence', 
                ' as demonstrated in the literature', ' as supported by empirical data', 
            ]
            sentences = sent_tokenize(text)
            if sentences:
                last_sentence = sentences[-1]
                if last_sentence.endswith('.'):
                    # Replace the final period with the qualifier and a period
                    sentences[-1] = last_sentence.rstrip('.') + random.choice(qualifiers) + '.'
            text = ' '.join(sentences)
        
        # Add academic hedging language (e.g., 'arguably', 'potentially')
        if random.random() < 0.12:
            sentences = sent_tokenize(text)
            if len(sentences) > 0:
                hedge_words = ['arguably', 'potentially', 'presumably', 'conceivably', 'seemingly']
                idx = random.randint(0, len(sentences)-1)
                words = word_tokenize(sentences[idx])
                
                if len(words) > 3:
                    hedge = random.choice(hedge_words)
                    # Insert hedge word near the beginning (e.g., as the third word)
                    words.insert(2, hedge + ',')
                    sentences[idx] = ' '.join(words)
                    
            text = ' '.join(sentences)
            text = re.sub(r'\s([.,;:])', r'\1', text) # Cleanup spacing

        # Ensure proper academic tone by replacing personal pronouns/phrases
        text = text.replace("I think", "It can be argued")
        text = text.replace("I believe", "Evidence suggests")
        text = text.replace("In my opinion", "Analysis indicates")
        text = text.replace("I feel", "Research demonstrates")
        
        return text

@app.route('/', methods=['GET', 'POST'])
def index():
    """Handles the main application logic and renders the template."""
    context = {
        'ai_text': '',
        'humanized_text': '',
        'intensity': 3,
        'deep_think': False,
        'cycles': 5 # Default cycles for Deep Think
    }

    if request.method == 'POST':
        ai_text = request.form.get('ai_text', '')
        intensity = int(request.form.get('intensity', 3))
        deep_think = request.form.get('deep_think') == 'on'
        cycles = int(request.form.get('cycles', 5))
        
        humanizer = TextHumanizer()
        
        if deep_think:
            # Deep Think Mode: Applies max intensity over multiple cycles
            humanized_text = humanizer.deep_think_humanize(ai_text, cycles=cycles)
            context['intensity'] = 5 
            context['deep_think'] = True
            context['cycles'] = cycles
        else:
            # Normal mode: Single humanization pass
            humanized_text = humanizer.humanize(ai_text, intensity)
            context['intensity'] = intensity
            context['deep_think'] = False
            context['cycles'] = 5

        context['ai_text'] = ai_text
        # Convert newlines to HTML line breaks for proper display
        context['humanized_text'] = humanized_text.replace('\n\n', '<br><br>')
    
    return render_template('index.html', **context)
# The local development server setup is removed for Vercel compatibility.