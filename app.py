from flask import Flask, render_template, request
import re
import random
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from typing import List
import os

# Initialize Flask app
app = Flask(__name__)

# Set NLTK data path to local folder
nltk_data_path = os.path.join(os.path.dirname(__file__), 'nltk_data')
nltk.data.path.append(nltk_data_path)

# Verify NLTK data is available (optional - for debugging)
try:
    # Test if the data is accessible
    word_tokenize("test")
    wordnet.synsets("test")
    print("NLTK data loaded successfully from local folder")
except Exception as e:
    print(f"Warning: Error loading NLTK data - {e}")
    print(f"NLTK data paths: {nltk.data.path}")

class TextHumanizer:
    def __init__(self):
        self.sentence_variations = [
            self.vary_sentence_lengths,
            self.add_academic_transitions,
            self.use_synonyms,
            self.restructure_sentences,
            self.add_academic_depth,
            self.vary_connectors,
            self.add_scholarly_elements
        ]
    
    def split_into_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs based on double line breaks"""
        # Split by double newlines, single newlines, or multiple spaces that might indicate paragraphs
        paragraphs = re.split(r'\n\s*\n|\r\n\s*\r\n', text.strip())
        # Clean up paragraphs and remove empty ones
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        return paragraphs
    
    def humanize(self, text: str, intensity: int = 3) -> str:
        """Single humanization pass - now handles paragraphs"""
        paragraphs = self.split_into_paragraphs(text)
        humanized_paragraphs = []
        
        for paragraph in paragraphs:
            sentences = sent_tokenize(paragraph)
            humanized_sentences = []
            
            for sentence in sentences:
                for _ in range(intensity):
                    transform = random.choice(self.sentence_variations)
                    sentence = transform(sentence)
                humanized_sentences.append(sentence)
            
            paragraph_text = ' '.join(humanized_sentences)
            paragraph_text = self.add_human_touches(paragraph_text)
            humanized_paragraphs.append(paragraph_text)
        
        # Join paragraphs with double line breaks
        return '\n\n'.join(humanized_paragraphs)
    
    def deep_think_humanize(self, text: str, cycles: int = 5) -> str:
        """
        Deep Think Mode: Humanize text multiple times with maximum intensity
        Each cycle processes the output of the previous cycle - now preserves paragraphs
        """
        current_text = text
        
        for cycle in range(cycles):
            # Always use maximum intensity (5) for deep think mode
            current_text = self.humanize(current_text, intensity=5)
            
            # Add some variation between cycles to prevent repetitive patterns
            if cycle < cycles - 1:  # Don't add extra variation on the last cycle
                current_text = self.add_cycle_variation(current_text, cycle)
        
        return current_text
    
    def add_cycle_variation(self, text: str, cycle_num: int) -> str:
        """Add subtle variations between deep think cycles - handles paragraphs"""
        paragraphs = self.split_into_paragraphs(text)
        varied_paragraphs = []
        
        for paragraph in paragraphs:
            # Different types of variations for different cycles
            if cycle_num == 0:
                # First cycle: focus on academic structure
                paragraph = self.add_academic_transitions(paragraph)
            elif cycle_num == 1:
                # Second cycle: add scholarly depth
                paragraph = self.add_scholarly_elements(paragraph)
            elif cycle_num == 2:
                # Third cycle: vary academic rhythm
                paragraph = self.vary_academic_rhythm(paragraph)
            elif cycle_num == 3:
                # Fourth cycle: add analytical elements
                paragraph = self.add_analytical_elements(paragraph)
            
            varied_paragraphs.append(paragraph)
        
        return '\n\n'.join(varied_paragraphs)
    
    def add_academic_transitions(self, text: str) -> str:
        """Add academic transition phrases and formal language"""
        academic_transitions = [
            ('Furthermore,', 0.2),
            ('Moreover,', 0.15),
            ('Additionally,', 0.2),
            ('In contrast,', 0.1),
            ('Subsequently,', 0.1),
            ('Consequently,', 0.1),
            ('Nevertheless,', 0.1),
            ('Thus,', 0.15),
            ('Hence,', 0.1)
        ]
        
        sentences = sent_tokenize(text)
        if len(sentences) > 1 and random.random() < 0.4:
            for phrase, prob in academic_transitions:
                if random.random() < prob:
                    # Add transition to a middle sentence
                    idx = random.randint(1, len(sentences) - 1)
                    if not sentences[idx].startswith(('Furthermore', 'Moreover', 'Additionally', 'In contrast', 'Subsequently', 'Consequently', 'Nevertheless', 'Thus', 'Hence')):
                        sentences[idx] = phrase + ' ' + sentences[idx].lower()
                    break
        
        return ' '.join(sentences)
    
    def add_scholarly_elements(self, text: str) -> str:
        """Add scholarly depth and academic language"""
        scholarly_phrases = [
            "It is important to note that",
            "Research indicates that",
            "Studies have shown that",
            "Evidence suggests that",
            "Analysis reveals that",
            "It can be argued that",
            "This demonstrates that",
            "The findings indicate that"
        ]
        
        if random.random() < 0.25:
            phrase = random.choice(scholarly_phrases)
            sentences = sent_tokenize(text)
            if sentences and not sentences[0].startswith(tuple(p.split()[0] for p in scholarly_phrases)):
                sentences[0] = phrase + " " + sentences[0].lower()
                text = ' '.join(sentences)
        
        return text
    
    def vary_academic_rhythm(self, text: str) -> str:
        """Create varied academic sentence structures"""
        sentences = sent_tokenize(text)
        varied_sentences = []
        
        for i, sentence in enumerate(sentences):
            if i > 0 and random.random() < 0.15:
                # Add academic connectors
                connectors = ["Furthermore,", "In addition,", "Similarly,", "Conversely,", "Notably,"]
                if not sentence.startswith(tuple(connectors)):
                    sentence = random.choice(connectors) + " " + sentence.lower()
            varied_sentences.append(sentence)
        
        return ' '.join(varied_sentences)
    
    def add_analytical_elements(self, text: str) -> str:
        """Add analytical and critical thinking elements"""
        analytical_additions = [
            " This analysis suggests",
            " These findings imply",
            " The evidence demonstrates",
            " This examination reveals",
            " The data indicates"
        ]
        
        sentences = sent_tokenize(text)
        if sentences and random.random() < 0.2:
            last_sentence = sentences[-1]
            if last_sentence.endswith('.'):
                addition = random.choice(analytical_additions)
                # Create a follow-up analytical sentence
                analytical_conclusions = [
                    " significant implications for the field.",
                    " the complexity of the subject matter.",
                    " important considerations for future research.",
                    " the need for further investigation.",
                    " valuable insights into the phenomenon."
                ]
                conclusion = random.choice(analytical_conclusions)
                sentences[-1] = last_sentence[:-1] + "." + addition + conclusion
        
        return ' '.join(sentences)
    
    def get_synonyms(self, word: str, pos: str = None) -> List[str]:
        synonyms = set()
        pos_mapping = {
            'NN': wordnet.NOUN,
            'JJ': wordnet.ADJ,
            'VB': wordnet.VERB,
            'RB': wordnet.ADV
        }
        
        if pos:
            wordnet_pos = pos_mapping.get(pos[:2], None)
            if wordnet_pos:
                for syn in wordnet.synsets(word, pos=wordnet_pos):
                    for lemma in syn.lemmas():
                        synonym = lemma.name().replace('_', ' ')
                        if synonym.lower() != word.lower() and len(synonym.split()) == 1:
                            synonyms.add(synonym)
        else:
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    synonym = lemma.name().replace('_', ' ')
                    if synonym.lower() != word.lower() and len(synonym.split()) == 1:
                        synonyms.add(synonym)
        return list(synonyms)
    
    def vary_sentence_lengths(self, text: str) -> str:
        """Break up or combine sentences to vary length"""
        if random.random() < 0.3:
            clauses = re.split(r'[,;]', text)
            if len(clauses) > 1 and random.random() < 0.5:
                return '. '.join([c.strip().capitalize() for c in clauses if c.strip()]) + '.'
        return text
    
    def add_academic_depth(self, text: str) -> str:
        """Add academic depth and elaboration"""
        depth_phrases = [
            ('It is essential to understand that', 0.1),
            ('This concept can be further explained by', 0.08),
            ('The significance of this lies in', 0.1),
            ('A deeper examination reveals that', 0.08),
            ('This approach demonstrates that', 0.1),
            ('The implications of this include', 0.08)
        ]
        
        for phrase, prob in depth_phrases:
            if random.random() < prob:
                words = word_tokenize(text)
                if len(words) > 10:  # Only add to longer sentences
                    insert_pos = random.randint(len(words)//2, len(words)-1)
                    phrase_words = phrase.split()
                    for i, word in enumerate(phrase_words):
                        words.insert(insert_pos + i, word)
                    text = ' '.join(words)
                    break
        return text
    
    def use_synonyms(self, text: str) -> str:
        """Replace words with synonyms where appropriate"""
        words = word_tokenize(text)
        pos_tags = nltk.pos_tag(words)
        
        for i, (word, tag) in enumerate(pos_tags):
            if tag.startswith('NN') or tag.startswith('JJ') or tag.startswith('VB'):
                if random.random() < 0.3:
                    syns = self.get_synonyms(word, tag)
                    if syns:
                        words[i] = random.choice(syns)
        
        return ' '.join(words)
    
    def restructure_sentences(self, text: str) -> str:
        """Change sentence structure to more academic patterns"""
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
            if re.search(pattern, text):
                if random.random() < 0.4:
                    text = re.sub(pattern, replacement, text)
                    break
        return text
    
    def vary_connectors(self, text: str) -> str:
        """Vary sentence connectors to be more academic"""
        connectors = {
            'however': ['nevertheless', 'nonetheless', 'conversely', 'in contrast'],
            'therefore': ['consequently', 'thus', 'hence', 'as a result'],
            'additionally': ['furthermore', 'moreover', 'in addition', 'similarly'],
            'moreover': ['furthermore', 'additionally', 'in addition', 'what is more'],
            'furthermore': ['moreover', 'additionally', 'in addition', 'beyond this'],
            'also': ['additionally', 'furthermore', 'likewise', 'similarly'],
            'but': ['however', 'nevertheless', 'conversely', 'in contrast'],
            'so': ['therefore', 'consequently', 'thus', 'hence']
        }
        
        words = word_tokenize(text)
        for i, word in enumerate(words):
            lower_word = word.lower()
            if lower_word in connectors and random.random() < 0.6:
                words[i] = random.choice(connectors[lower_word])
        return ' '.join(words)
    
    def add_human_touches(self, text: str) -> str:
        """Final cleanup and addition of academic writing features"""
        # Add formal qualifiers
        if random.random() < 0.15:
            qualifiers = [
                ' according to current research',
                ' based on available evidence',
                ' as demonstrated in the literature',
                ' as supported by empirical data',
                ' in accordance with established theory',
                ' as evidenced by recent studies'
            ]
            insert_pos = text.rfind('.')
            if insert_pos != -1:
                text = text[:insert_pos] + random.choice(qualifiers) + text[insert_pos:]
        
        # Add academic hedging language
        if random.random() < 0.12:
            sentences = sent_tokenize(text)
            if len(sentences) > 1:
                hedge_words = ['arguably', 'potentially', 'presumably', 'conceivably', 'seemingly']
                idx = random.randint(0, len(sentences)-1)
                words = word_tokenize(sentences[idx])
                if len(words) > 3:
                    hedge = random.choice(hedge_words)
                    words.insert(2, hedge)
                    sentences[idx] = ' '.join(words)
                text = ' '.join(sentences)
        
        # Ensure proper academic tone
        text = text.replace("I think", "It can be argued")
        text = text.replace("I believe", "Evidence suggests")
        text = text.replace("In my opinion", "Analysis indicates")
        text = text.replace("I feel", "Research demonstrates")
        
        return text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ai_text = request.form.get('ai_text', '')
        intensity = int(request.form.get('intensity', 3))
        deep_think = request.form.get('deep_think') == 'on'
        
        humanizer = TextHumanizer()
        
        if deep_think:
            # Deep Think Mode: Always use intensity 5 and process 5 times
            humanized_text = humanizer.deep_think_humanize(ai_text, cycles=5)
            intensity = 5  # Override intensity for deep think mode
        else:
            # Normal mode: Single humanization pass
            humanized_text = humanizer.humanize(ai_text, intensity)
        
        # Convert newlines to HTML line breaks for proper display
        humanized_text_html = humanized_text.replace('\n\n', '<br><br>')
        
        return render_template('index.html', 
                            ai_text=ai_text,
                            humanized_text=humanized_text_html,
                            intensity=intensity,
                            deep_think=deep_think)
    
    return render_template('index.html')

# Vercel serverless function handler
if __name__ == '__main__':
    app.run()