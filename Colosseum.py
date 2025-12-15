# ===============================================================================
#  THE COLOSSEUM OF INFINITY - TEXT ANALYZER
#  Where the Mad Titan Meets the Gladiator
# ===============================================================================

import string
from collections import Counter

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from PIL import Image, ImageDraw, ImageFont
    GRAPHICS_AVAILABLE = True
except ImportError:
    GRAPHICS_AVAILABLE = False


class GraphicsGenerator:
    """Generate themed graphics for the Colosseum of Infinity."""
    
    PURPLE = '#6B3FA0'
    DARK_PURPLE = '#4A2870'
    GOLD = '#FFD700'
    DARK_GOLD = '#B8860B'
    BLACK = '#1A1A2E'
    WHITE = '#FFFFFF'
    
    @staticmethod
    def create_banner(title="THE COLOSSEUM OF INFINITY", 
                      subtitle="Where the Mad Titan Meets the Gladiator", 
                      filename="colosseum_banner.png"):
        if not GRAPHICS_AVAILABLE:
            print("Graphics libraries not available. Install with: pip install matplotlib pillow")
            return None
        
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 4)
        ax.set_facecolor(GraphicsGenerator.BLACK)
        fig.patch.set_facecolor(GraphicsGenerator.BLACK)
        ax.axis('off')
        
        gradient = patches.Rectangle((0, 0), 12, 4, facecolor=GraphicsGenerator.DARK_PURPLE)
        ax.add_patch(gradient)
        
        border = patches.Rectangle((0.1, 0.1), 11.8, 3.8, fill=False, 
                                    edgecolor=GraphicsGenerator.GOLD, linewidth=4)
        ax.add_patch(border)
        
        ax.text(6, 2.5, title, fontsize=24, fontweight='bold', 
                color=GraphicsGenerator.GOLD, ha='center', va='center')
        ax.text(6, 1.5, subtitle, fontsize=14, fontstyle='italic',
                color=GraphicsGenerator.WHITE, ha='center', va='center')
        
        stone_colors = ['#FF0000', '#FF8C00', '#FFFF00', '#00FF00', '#0000FF', '#9400D3']
        for i, color in enumerate(stone_colors):
            circle = patches.Circle((1.5 + i * 1.7, 0.5), 0.2, 
                                     facecolor=color, edgecolor=GraphicsGenerator.GOLD)
            ax.add_patch(circle)
        
        plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor=GraphicsGenerator.BLACK)
        plt.close()
        print(f"Banner saved to {filename}")
        return filename
    
    @staticmethod
    def create_stats_chart(analyzer, filename="stats_chart.png"):
        if not GRAPHICS_AVAILABLE:
            print("Graphics libraries not available. Install with: pip install matplotlib pillow")
            return None
        
        stats = {
            'Words': analyzer.word_count(),
            'Sentences': analyzer.sentence_count(),
            'Paragraphs': analyzer.paragraph_count(),
            'Unique Words': analyzer.unique_words(),
            'Vowels': analyzer.vowel_count(),
            'Consonants': analyzer.consonant_count()
        }
        
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor(GraphicsGenerator.BLACK)
        ax.set_facecolor(GraphicsGenerator.BLACK)
        
        bars = ax.bar(stats.keys(), stats.values(), color=GraphicsGenerator.PURPLE, 
                      edgecolor=GraphicsGenerator.GOLD, linewidth=2)
        
        ax.set_title('POWER STONE - Text Statistics', fontsize=16, fontweight='bold', 
                     color=GraphicsGenerator.GOLD, pad=20)
        ax.tick_params(colors=GraphicsGenerator.WHITE)
        ax.spines['bottom'].set_color(GraphicsGenerator.GOLD)
        ax.spines['left'].set_color(GraphicsGenerator.GOLD)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        for bar, value in zip(bars, stats.values()):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{value:,}', ha='center', va='bottom',
                    color=GraphicsGenerator.WHITE, fontweight='bold')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(filename, dpi=150, facecolor=GraphicsGenerator.BLACK)
        plt.close()
        print(f"Stats chart saved to {filename}")
        return filename
    
    @staticmethod
    def create_word_frequency_chart(analyzer, top_n=10, filename="word_frequency.png"):
        if not GRAPHICS_AVAILABLE:
            print("Graphics libraries not available. Install with: pip install matplotlib pillow")
            return None
        
        common_words = analyzer.most_common_words(top_n)
        if not common_words:
            print("No words to chart.")
            return None
        
        words = [w[0] for w in common_words][::-1]
        counts = [w[1] for w in common_words][::-1]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor(GraphicsGenerator.BLACK)
        ax.set_facecolor(GraphicsGenerator.BLACK)
        
        bars = ax.barh(words, counts, color=GraphicsGenerator.PURPLE, 
                       edgecolor=GraphicsGenerator.GOLD, linewidth=2)
        
        ax.set_title('MIND STONE - Champion Words', fontsize=16, fontweight='bold',
                     color=GraphicsGenerator.GOLD, pad=20)
        ax.tick_params(colors=GraphicsGenerator.WHITE)
        ax.spines['bottom'].set_color(GraphicsGenerator.GOLD)
        ax.spines['left'].set_color(GraphicsGenerator.GOLD)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        for bar, count in zip(bars, counts):
            ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                    f'{count}', va='center', color=GraphicsGenerator.WHITE, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=150, facecolor=GraphicsGenerator.BLACK)
        plt.close()
        print(f"Word frequency chart saved to {filename}")
        return filename
    
    @staticmethod
    def create_letter_pie_chart(analyzer, filename="letter_distribution.png"):
        if not GRAPHICS_AVAILABLE:
            print("Graphics libraries not available. Install with: pip install matplotlib pillow")
            return None
        
        freq = analyzer.letter_frequency().most_common(8)
        if not freq:
            print("No letters to chart.")
            return None
        
        letters = [f[0].upper() for f in freq]
        counts = [f[1] for f in freq]
        colors = ['#FF0000', '#FF8C00', '#FFFF00', '#00FF00', 
                  '#0000FF', '#9400D3', '#FF1493', '#00CED1']
        
        fig, ax = plt.subplots(figsize=(8, 8))
        fig.patch.set_facecolor(GraphicsGenerator.BLACK)
        
        wedges, texts, autotexts = ax.pie(counts, labels=letters, autopct='%1.1f%%',
            colors=colors[:len(letters)],
            wedgeprops={'edgecolor': GraphicsGenerator.GOLD, 'linewidth': 2})
        
        for text in texts:
            text.set_color(GraphicsGenerator.WHITE)
            text.set_fontweight('bold')
        for autotext in autotexts:
            autotext.set_color(GraphicsGenerator.BLACK)
            autotext.set_fontweight('bold')
        
        ax.set_title('SPACE STONE - Letter Distribution', fontsize=16, fontweight='bold',
                     color=GraphicsGenerator.GOLD, pad=20)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=150, facecolor=GraphicsGenerator.BLACK)
        plt.close()
        print(f"Letter distribution chart saved to {filename}")
        return filename
    
    @staticmethod
    def create_gladiator_rank_card(analyzer, filename="gladiator_rank.png"):
        if not GRAPHICS_AVAILABLE:
            print("Graphics libraries not available. Install with: pip install matplotlib pillow")
            return None
        
        rank = analyzer.get_gladiator_rank()
        word_count = analyzer.word_count()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor(GraphicsGenerator.BLACK)
        ax.set_facecolor(GraphicsGenerator.DARK_PURPLE)
        ax.set_xlim(0, 8)
        ax.set_ylim(0, 5)
        ax.axis('off')
        
        border = patches.Rectangle((0.1, 0.1), 7.8, 4.8, fill=False,
                                    edgecolor=GraphicsGenerator.GOLD, linewidth=4)
        ax.add_patch(border)
        
        ax.text(4, 4, 'GLADIATOR RANK', fontsize=18, fontweight='bold',
                color=GraphicsGenerator.GOLD, ha='center', va='center')
        ax.text(4, 2.5, rank, fontsize=22, fontweight='bold',
                color=GraphicsGenerator.WHITE, ha='center', va='center')
        ax.text(4, 1.2, f'Words: {word_count:,}', fontsize=14,
                color=GraphicsGenerator.GOLD, ha='center', va='center')
        
        plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor=GraphicsGenerator.BLACK)
        plt.close()
        print(f"Gladiator rank card saved to {filename}")
        return filename
    
    @staticmethod
    def create_full_report_graphic(analyzer, filename="full_report.png"):
        if not GRAPHICS_AVAILABLE:
            print("Graphics libraries not available. Install with: pip install matplotlib pillow")
            return None
        
        fig = plt.figure(figsize=(16, 12))
        fig.patch.set_facecolor(GraphicsGenerator.BLACK)
        fig.suptitle('THE COLOSSEUM OF INFINITY - ANALYSIS REPORT', 
                     fontsize=24, fontweight='bold', color=GraphicsGenerator.GOLD, y=0.98)
        
        gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
        
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.set_facecolor(GraphicsGenerator.BLACK)
        stats = {'Words': analyzer.word_count(), 'Sentences': analyzer.sentence_count(),
                 'Unique': analyzer.unique_words(), 'Paragraphs': analyzer.paragraph_count()}
        ax1.bar(stats.keys(), stats.values(), color=GraphicsGenerator.PURPLE, 
                edgecolor=GraphicsGenerator.GOLD, linewidth=2)
        ax1.set_title('POWER STONE', color=GraphicsGenerator.GOLD, fontweight='bold')
        ax1.tick_params(colors=GraphicsGenerator.WHITE)
        for spine in ax1.spines.values():
            spine.set_color(GraphicsGenerator.GOLD)
        
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.set_facecolor(GraphicsGenerator.BLACK)
        common = analyzer.most_common_words(5)
        if common:
            words = [w[0] for w in common][::-1]
            counts = [w[1] for w in common][::-1]
            ax2.barh(words, counts, color=GraphicsGenerator.PURPLE, 
                     edgecolor=GraphicsGenerator.GOLD, linewidth=2)
        ax2.set_title('MIND STONE', color=GraphicsGenerator.GOLD, fontweight='bold')
        ax2.tick_params(colors=GraphicsGenerator.WHITE)
        for spine in ax2.spines.values():
            spine.set_color(GraphicsGenerator.GOLD)
        
        ax3 = fig.add_subplot(gs[0, 2])
        ax3.set_facecolor(GraphicsGenerator.BLACK)
        freq = analyzer.letter_frequency().most_common(6)
        if freq:
            letters = [f[0].upper() for f in freq]
            lcounts = [f[1] for f in freq]
            colors = ['#FF0000', '#FF8C00', '#FFFF00', '#00FF00', '#0000FF', '#9400D3']
            ax3.pie(lcounts, labels=letters, colors=colors[:len(letters)],
                    wedgeprops={'edgecolor': GraphicsGenerator.GOLD})
        ax3.set_title('SPACE STONE', color=GraphicsGenerator.GOLD, fontweight='bold')
        
        ax4 = fig.add_subplot(gs[1, 0])
        ax4.set_facecolor(GraphicsGenerator.DARK_PURPLE)
        ax4.axis('off')
        metrics_text = f"""SOUL STONE - Lexical Depth

Lexical Diversity: {analyzer.lexical_diversity():.2%}
Avg Word Length: {analyzer.average_word_length():.2f}
Avg Sentence Length: {analyzer.average_sentence_length():.1f}"""
        ax4.text(0.5, 0.5, metrics_text, transform=ax4.transAxes, fontsize=12,
                 color=GraphicsGenerator.WHITE, ha='center', va='center',
                 bbox=dict(boxstyle='round', facecolor=GraphicsGenerator.DARK_PURPLE, 
                          edgecolor=GraphicsGenerator.GOLD, linewidth=2))
        
        ax5 = fig.add_subplot(gs[1, 1])
        ax5.set_facecolor(GraphicsGenerator.DARK_PURPLE)
        ax5.axis('off')
        time_text = f"""TIME STONE - Temporal Metrics

Reading Time: {analyzer.reading_time():.1f} min
Speaking Time: {analyzer.speaking_time():.1f} min
Complexity: {analyzer.simple_readability_score():.1f}"""
        ax5.text(0.5, 0.5, time_text, transform=ax5.transAxes, fontsize=12,
                 color=GraphicsGenerator.WHITE, ha='center', va='center',
                 bbox=dict(boxstyle='round', facecolor=GraphicsGenerator.DARK_PURPLE,
                          edgecolor=GraphicsGenerator.GOLD, linewidth=2))
        
        ax6 = fig.add_subplot(gs[1, 2])
        ax6.set_facecolor(GraphicsGenerator.DARK_PURPLE)
        ax6.axis('off')
        rank_text = f"""GLADIATOR RANK

{analyzer.get_gladiator_rank()}

"Are you not entertained?!"
- Maximus"""
        ax6.text(0.5, 0.5, rank_text, transform=ax6.transAxes, fontsize=12,
                 color=GraphicsGenerator.WHITE, ha='center', va='center', fontweight='bold',
                 bbox=dict(boxstyle='round', facecolor=GraphicsGenerator.DARK_PURPLE,
                          edgecolor=GraphicsGenerator.GOLD, linewidth=2))
        
        plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor=GraphicsGenerator.BLACK)
        plt.close()
        print(f"Full report graphic saved to {filename}")
        return filename


class ColosseumsTextAnalyzer:
    """The Arena where texts are judged by the Mad Titan himself."""
    
    INFINITY_STONES = {
        "SPACE": "Character Analysis",
        "MIND": "Word Intelligence", 
        "REALITY": "Reading Metrics",
        "POWER": "Text Statistics",
        "TIME": "Time Estimates",
        "SOUL": "Lexical Depth"
    }
    
    GLADIATOR_RANKS = [
        ("Tiro (Novice)", 0),
        ("Gregarius (Common)", 100),
        ("Veteranus (Veteran)", 500),
        ("Primus Palus (Champion)", 1000),
        ("Rudiarius (Freed Legend)", 5000),
        ("Maximus Decimus Meridius", 10000)
    ]

    def __init__(self, text=""):
        self.text = text
        self.words = self._extract_words()
        self.lines = text.split('\n') if text else []
        self.sentences = self._extract_sentences()
    
    def _extract_words(self):
        if not self.text:
            return []
        translator = str.maketrans('', '', string.punctuation)
        cleaned = self.text.translate(translator).lower()
        return cleaned.split()
    
    def _extract_sentences(self):
        if not self.text:
            return []
        sentences = []
        current = ""
        for char in self.text:
            current += char
            if char in '.!?':
                if current.strip():
                    sentences.append(current.strip())
                current = ""
        if current.strip():
            sentences.append(current.strip())
        return sentences

    def character_count(self, include_spaces=True):
        if include_spaces:
            return len(self.text)
        return len(self.text.replace(' ', '').replace('\n', ''))
    
    def word_count(self):
        return len(self.words)
    
    def line_count(self):
        return len(self.lines)
    
    def sentence_count(self):
        return len(self.sentences)
    
    def paragraph_count(self):
        if not self.text:
            return 0
        paragraphs = [p for p in self.text.split('\n\n') if p.strip()]
        return len(paragraphs)

    def unique_words(self):
        return len(set(self.words))
    
    def most_common_words(self, n=10):
        if not self.words:
            return []
        return Counter(self.words).most_common(n)
    
    def longest_word(self):
        if not self.words:
            return ""
        return max(self.words, key=len)
    
    def shortest_word(self):
        if not self.words:
            return ""
        return min(self.words, key=len)
    
    def average_word_length(self):
        if not self.words:
            return 0
        return sum(len(word) for word in self.words) / len(self.words)

    def letter_frequency(self):
        letters = [c.lower() for c in self.text if c.isalpha()]
        return Counter(letters)
    
    def vowel_count(self):
        vowels = 'aeiouAEIOU'
        return sum(1 for c in self.text if c in vowels)
    
    def consonant_count(self):
        consonants = 'bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
        return sum(1 for c in self.text if c in consonants)
    
    def digit_count(self):
        return sum(1 for c in self.text if c.isdigit())
    
    def special_char_count(self):
        return sum(1 for c in self.text if c in string.punctuation)

    def lexical_diversity(self):
        if not self.words:
            return 0
        return self.unique_words() / len(self.words)
    
    def average_sentence_length(self):
        if not self.sentences:
            return 0
        total_words = sum(len(s.split()) for s in self.sentences)
        return total_words / len(self.sentences)

    def reading_time(self, wpm=200):
        return self.word_count() / wpm
    
    def speaking_time(self, wpm=150):
        return self.word_count() / wpm

    def simple_readability_score(self):
        if not self.words or not self.sentences:
            return 0
        avg_word = self.average_word_length()
        avg_sent = self.average_sentence_length()
        return (avg_word * 10) + (avg_sent * 0.5)

    def get_gladiator_rank(self):
        wc = self.word_count()
        rank = "Tiro (Novice)"
        for title, threshold in self.GLADIATOR_RANKS:
            if wc >= threshold:
                rank = title
        return rank

    def snap_analysis(self):
        border = "=" * 70
        thin_border = "-" * 70
        
        report = f"""
{border}
    THE COLOSSEUM OF INFINITY - TEXT ANALYSIS
    "What we analyze in life, echoes in eternity... perfectly balanced."
{border}

    GLADIATOR RANK: {self.get_gladiator_rank()}
    
{thin_border}
    POWER STONE - Raw Statistics
{thin_border}
    Total Characters (with spaces):    {self.character_count(True):,}
    Total Characters (no spaces):      {self.character_count(False):,}
    Total Words:                       {self.word_count():,}
    Total Lines:                       {self.line_count():,}
    Total Sentences:                   {self.sentence_count():,}
    Total Paragraphs:                  {self.paragraph_count():,}

{thin_border}
    MIND STONE - Word Intelligence  
{thin_border}
    Unique Words:                      {self.unique_words():,}
    Longest Word:                      "{self.longest_word()}"
    Shortest Word:                     "{self.shortest_word()}"
    Average Word Length:               {self.average_word_length():.2f} characters

    TOP 10 CHAMPION WORDS:
"""
        for i, (word, count) in enumerate(self.most_common_words(10), 1):
            report += f'    {i:2}. "{word}" - {count} appearances\n'

        report += f"""
{thin_border}
    SPACE STONE - Character Analysis
{thin_border}
    Vowels:                            {self.vowel_count():,}
    Consonants:                        {self.consonant_count():,}
    Digits:                            {self.digit_count():,}
    Special Characters:                {self.special_char_count():,}

    TOP 5 LETTERS:
"""
        for letter, count in self.letter_frequency().most_common(5):
            report += f'    "{letter.upper()}" - {count:,} occurrences\n'

        report += f"""
{thin_border}
    SOUL STONE - Lexical Depth
{thin_border}
    Lexical Diversity:                 {self.lexical_diversity():.2%}
    Average Sentence Length:           {self.average_sentence_length():.1f} words

{thin_border}
    TIME STONE - Temporal Metrics
{thin_border}
    Estimated Reading Time:            {self.reading_time():.1f} minutes
    Estimated Speaking Time:           {self.speaking_time():.1f} minutes

{thin_border}
    REALITY STONE - Readability
{thin_border}
    Complexity Score:                  {self.simple_readability_score():.1f}
    Rating: {"Simple" if self.simple_readability_score() < 50 else "Moderate" if self.simple_readability_score() < 70 else "Complex"}

{border}
    "ARE YOU NOT ENTERTAINED?!" - Maximus
    "I am... inevitable." - Thanos
    
    *SNAP* Analysis Complete. Half of all unnecessary words... gone.
{border}
"""
        return report


def display_intro():
    print("\n" + "=" * 70)
    print("    THE COLOSSEUM OF INFINITY")
    print("    Where the Mad Titan Meets the Gladiator")
    print("    'What we analyze in life, echoes in eternity... perfectly balanced.'")
    print("=" * 70)
    
    if GRAPHICS_AVAILABLE:
        print("\n    [Graphics libraries loaded - visual reports available]")
    else:
        print("\n    [Install matplotlib and pillow for graphics: pip install matplotlib pillow]")


def main():
    display_intro()
    
    while True:
        print("\n    CHOOSE YOUR BATTLE")
        print("    " + "-" * 40)
        print("    [1] Analyze a Text File")
        print("    [2] Enter Text Directly")
        print("    [3] Generate Graphics Only")
        print("    [4] Exit the Arena")
        print("    " + "-" * 40)
        
        choice = input("\n    Enter your choice (1-4): ").strip()
        
        if choice == "1":
            filepath = input("\n    Enter the path to your text file: ").strip()
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()
                if not text.strip():
                    print("\n    WARNING: The scroll is empty!")
                    continue
                analyzer = ColosseumsTextAnalyzer(text)
                print(analyzer.snap_analysis())
                
                if GRAPHICS_AVAILABLE:
                    gen_graphics = input("\n    Generate graphics? (y/n): ").strip().lower()
                    if gen_graphics == 'y':
                        print("\n    Generating visual reports...")
                        GraphicsGenerator.create_banner()
                        GraphicsGenerator.create_stats_chart(analyzer)
                        GraphicsGenerator.create_word_frequency_chart(analyzer)
                        GraphicsGenerator.create_letter_pie_chart(analyzer)
                        GraphicsGenerator.create_gladiator_rank_card(analyzer)
                        GraphicsGenerator.create_full_report_graphic(analyzer)
                        print("\n    All graphics generated!")
                
                save = input("\n    Save text report to file? (y/n): ").strip().lower()
                if save == 'y':
                    output_path = input("    Enter output filename: ").strip()
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(analyzer.snap_analysis())
                    print(f"\n    Report saved to {output_path}")
                    
            except FileNotFoundError:
                print(f"\n    ERROR: File not found: {filepath}")
            except Exception as e:
                print(f"\n    ERROR: {e}")
        
        elif choice == "2":
            print("\n    Enter your text (type 'DONE' on a new line when finished):")
            print("    " + "-" * 40)
            lines = []
            while True:
                line = input()
                if line.strip().upper() == "DONE":
                    break
                lines.append(line)
            
            text = '\n'.join(lines)
            if not text.strip():
                print("\n    WARNING: No text entered!")
                continue
            
            analyzer = ColosseumsTextAnalyzer(text)
            print(analyzer.snap_analysis())
            
            if GRAPHICS_AVAILABLE:
                gen_graphics = input("\n    Generate graphics? (y/n): ").strip().lower()
                if gen_graphics == 'y':
                    print("\n    Generating visual reports...")
                    GraphicsGenerator.create_banner()
                    GraphicsGenerator.create_stats_chart(analyzer)
                    GraphicsGenerator.create_word_frequency_chart(analyzer)
                    GraphicsGenerator.create_letter_pie_chart(analyzer)
                    GraphicsGenerator.create_gladiator_rank_card(analyzer)
                    GraphicsGenerator.create_full_report_graphic(analyzer)
                    print("\n    All graphics generated!")
        
        elif choice == "3":
            if not GRAPHICS_AVAILABLE:
                print("\n    ERROR: Graphics libraries not installed.")
                print("    Run: pip install matplotlib pillow")
                continue
            
            print("\n    Generate which graphic?")
            print("    [1] Banner")
            print("    [2] Stats Chart")
            print("    [3] Word Frequency Chart")
            print("    [4] Letter Distribution Pie")
            print("    [5] Gladiator Rank Card")
            print("    [6] Full Report")
            print("    [7] All of the above")
            
            gchoice = input("\n    Enter choice: ").strip()
            
            if gchoice in ['2', '3', '4', '5', '6', '7']:
                print("\n    Enter text to analyze (type 'DONE' when finished):")
                lines = []
                while True:
                    line = input()
                    if line.strip().upper() == "DONE":
                        break
                    lines.append(line)
                text = '\n'.join(lines)
                if not text.strip():
                    print("\n    WARNING: No text entered!")
                    continue
                analyzer = ColosseumsTextAnalyzer(text)
            
            if gchoice == '1':
                GraphicsGenerator.create_banner()
            elif gchoice == '2':
                GraphicsGenerator.create_stats_chart(analyzer)
            elif gchoice == '3':
                GraphicsGenerator.create_word_frequency_chart(analyzer)
            elif gchoice == '4':
                GraphicsGenerator.create_letter_pie_chart(analyzer)
            elif gchoice == '5':
                GraphicsGenerator.create_gladiator_rank_card(analyzer)
            elif gchoice == '6':
                GraphicsGenerator.create_full_report_graphic(analyzer)
            elif gchoice == '7':
                GraphicsGenerator.create_banner()
                GraphicsGenerator.create_stats_chart(analyzer)
                GraphicsGenerator.create_word_frequency_chart(analyzer)
                GraphicsGenerator.create_letter_pie_chart(analyzer)
                GraphicsGenerator.create_gladiator_rank_card(analyzer)
                GraphicsGenerator.create_full_report_graphic(analyzer)
                print("\n    All graphics generated!")
        
        elif choice == "4":
            print("\n" + "=" * 70)
            print("    'Now we are free. I will see you again... but not yet. Not yet.'")
            print("    *closes Infinity Gauntlet*")
            print("    The Colosseum falls silent. Balance has been achieved.")
            print("=" * 70 + "\n")
            break
        
        else:
            print("\n    WARNING: Invalid choice. Select 1-4.")


if __name__ == "__main__":
    main()





            
            























































































































