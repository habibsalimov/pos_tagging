#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evaluation and Comparison Script for Turkish POS Taggers
Compares legacy Brill tagger with modern transformer-based approaches
"""

import time
import statistics
from typing import List, Tuple, Dict, Any
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict, Counter
import pandas as pd

# Import both old and new taggers
try:
    from pos_tagger import tag as legacy_tag
    LEGACY_AVAILABLE = True
except ImportError:
    print("Warning: Legacy tagger not available")
    LEGACY_AVAILABLE = False

from modern_pos_tagger import ModernTurkishPOSTagger

class POSTaggerEvaluator:
    """Comprehensive evaluation system for POS taggers"""
    
    def __init__(self):
        self.results = {}
        self.test_sentences = [
            "Bunu başından beri biliyordum zaten .",
            "Ali koştu ve parkta oynadı .",
            "Güzel bir günde bahçede oturuyoruz .",
            "Bu kitabı okumak çok zevkli .",
            "Yarın İstanbul'a gideceğim .",
            "Çocuklar bahçede top oynuyor .",
            "Annem yemek pişiriyor şimdi .",
            "Türkiye güzel bir ülkedir .",
            "Öğretmen öğrencilere ders anlatıyor .",
            "Kedi bahçede uyuyor sessizce .",
            "Pazartesi günü işe gideceğim .",
            "Bu çanta çok pahalı değil mi ?",
            "Arkadaşlarımla sinema gittik dün .",
            "Yağmur yağıyor ve hava soğuk .",
            "Müzik dinlemeyi çok seviyorum ."
        ]
        
    def evaluate_tagger(self, tagger_name: str, tag_function, sentences: List[str]) -> Dict[str, Any]:
        """Evaluate a single tagger"""
        print(f"\n=== Evaluating {tagger_name} ===")
        
        results = {
            'name': tagger_name,
            'sentences_processed': 0,
            'total_tokens': 0,
            'processing_times': [],
            'tag_distribution': Counter(),
            'examples': [],
            'errors': []
        }
        
        for sentence in sentences:
            try:
                start_time = time.time()
                tagged_result = tag_function(sentence)
                processing_time = time.time() - start_time
                
                results['processing_times'].append(processing_time)
                results['sentences_processed'] += 1
                results['total_tokens'] += len(tagged_result)
                
                # Count tag distribution
                for word, tag in tagged_result:
                    results['tag_distribution'][tag] += 1
                
                # Store examples
                results['examples'].append({
                    'sentence': sentence,
                    'result': tagged_result,
                    'processing_time': processing_time
                })
                
                print(f"✓ {sentence[:30]}... -> {len(tagged_result)} tokens ({processing_time:.4f}s)")
                
            except Exception as e:
                results['errors'].append({
                    'sentence': sentence,
                    'error': str(e)
                })
                print(f"✗ Error processing: {sentence[:30]}... -> {e}")
        
        # Calculate statistics
        if results['processing_times']:
            results['avg_processing_time'] = statistics.mean(results['processing_times'])
            results['total_processing_time'] = sum(results['processing_times'])
            results['tokens_per_second'] = results['total_tokens'] / results['total_processing_time'] if results['total_processing_time'] > 0 else 0
        
        return results
    
    def compare_taggers(self) -> Dict[str, Any]:
        """Compare all available taggers"""
        comparison_results = {}
        
        # Test legacy tagger
        if LEGACY_AVAILABLE:
            try:
                comparison_results['legacy'] = self.evaluate_tagger(
                    "Legacy Brill Tagger", 
                    legacy_tag, 
                    self.test_sentences
                )
            except Exception as e:
                print(f"Legacy tagger evaluation failed: {e}")
        
        # Test modern taggers
        try:
            modern_tagger = ModernTurkishPOSTagger(model_type="legacy")  # Fallback to legacy for comparison
            comparison_results['modern_legacy'] = self.evaluate_tagger(
                "Modern Legacy Implementation",
                modern_tagger.tag,
                self.test_sentences
            )
        except Exception as e:
            print(f"Modern legacy tagger evaluation failed: {e}")
        
        try:
            bert_tagger = ModernTurkishPOSTagger(model_type="berturk")
            comparison_results['berturk'] = self.evaluate_tagger(
                "BERTurk-based Tagger",
                bert_tagger.tag,
                self.test_sentences
            )
        except Exception as e:
            print(f"BERTurk tagger evaluation failed: {e}")
        
        return comparison_results
    
    def generate_comparison_report(self, results: Dict[str, Any]) -> str:
        """Generate detailed comparison report"""
        report = []
        report.append("=" * 80)
        report.append("TURKISH POS TAGGER COMPARISON REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Summary table
        report.append("PERFORMANCE SUMMARY:")
        report.append("-" * 50)
        
        summary_data = []
        for tagger_name, data in results.items():
            if 'avg_processing_time' in data:
                summary_data.append({
                    'Tagger': data['name'],
                    'Sentences': data['sentences_processed'],
                    'Tokens': data['total_tokens'],
                    'Avg Time (s)': f"{data['avg_processing_time']:.4f}",
                    'Tokens/sec': f"{data['tokens_per_second']:.1f}",
                    'Errors': len(data['errors'])
                })
        
        if summary_data:
            df = pd.DataFrame(summary_data)
            report.append(df.to_string(index=False))
        
        report.append("")
        
        # Detailed results for each tagger
        for tagger_name, data in results.items():
            report.append(f"\n{data['name'].upper()} DETAILED RESULTS:")
            report.append("-" * 40)
            
            # Tag distribution
            report.append("\nTag Distribution:")
            total_tags = sum(data['tag_distribution'].values())
            for tag, count in data['tag_distribution'].most_common():
                percentage = (count / total_tags) * 100 if total_tags > 0 else 0
                report.append(f"  {tag:12}: {count:4} ({percentage:5.1f}%)")
            
            # Example outputs
            report.append("\nExample Outputs:")
            for i, example in enumerate(data['examples'][:3], 1):
                report.append(f"\n  Example {i}: {example['sentence']}")
                report.append(f"  Result: {example['result']}")
                report.append(f"  Time: {example['processing_time']:.4f}s")
            
            # Errors
            if data['errors']:
                report.append(f"\nErrors ({len(data['errors'])}):")
                for error in data['errors'][:3]:
                    report.append(f"  - {error['sentence'][:50]}... -> {error['error']}")
        
        return "\n".join(report)
    
    def create_visualizations(self, results: Dict[str, Any]):
        """Create comparison visualizations"""
        try:
            # Set up the plotting style
            plt.style.use('seaborn-v0_8')
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('Turkish POS Tagger Comparison', fontsize=16, fontweight='bold')
            
            # 1. Processing Time Comparison
            tagger_names = []
            avg_times = []
            for tagger_name, data in results.items():
                if 'avg_processing_time' in data:
                    tagger_names.append(data['name'])
                    avg_times.append(data['avg_processing_time'])
            
            if tagger_names:
                axes[0, 0].bar(tagger_names, avg_times, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
                axes[0, 0].set_title('Average Processing Time per Sentence')
                axes[0, 0].set_ylabel('Time (seconds)')
                axes[0, 0].tick_params(axis='x', rotation=45)
            
            # 2. Tokens per Second Comparison
            tokens_per_sec = []
            for tagger_name, data in results.items():
                if 'tokens_per_second' in data:
                    tokens_per_sec.append(data['tokens_per_second'])
            
            if tagger_names and tokens_per_sec:
                axes[0, 1].bar(tagger_names, tokens_per_sec, color=['#96CEB4', '#FFEAA7', '#DDA0DD'])
                axes[0, 1].set_title('Processing Speed (Tokens per Second)')
                axes[0, 1].set_ylabel('Tokens/sec')
                axes[0, 1].tick_params(axis='x', rotation=45)
            
            # 3. Tag Distribution (for first available tagger)
            first_result = next(iter(results.values()))
            if 'tag_distribution' in first_result:
                tags = list(first_result['tag_distribution'].keys())[:10]  # Top 10 tags
                counts = [first_result['tag_distribution'][tag] for tag in tags]
                
                axes[1, 0].pie(counts, labels=tags, autopct='%1.1f%%', startangle=90)
                axes[1, 0].set_title(f'Tag Distribution - {first_result["name"]}')
            
            # 4. Error Rate Comparison
            error_rates = []
            for tagger_name, data in results.items():
                if 'sentences_processed' in data:
                    total_attempts = data['sentences_processed'] + len(data['errors'])
                    error_rate = (len(data['errors']) / total_attempts * 100) if total_attempts > 0 else 0
                    error_rates.append(error_rate)
            
            if tagger_names and error_rates:
                axes[1, 1].bar(tagger_names, error_rates, color=['#FF7675', '#FDCB6E', '#6C5CE7'])
                axes[1, 1].set_title('Error Rate (%)')
                axes[1, 1].set_ylabel('Error Rate (%)')
                axes[1, 1].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.savefig('tagger_comparison_report.png', dpi=300, bbox_inches='tight')
            print("\n📊 Visualization saved as 'tagger_comparison_report.png'")
            
        except Exception as e:
            print(f"Visualization creation failed: {e}")
    
    def run_comprehensive_evaluation(self):
        """Run complete evaluation and generate reports"""
        print("🚀 Starting Comprehensive Turkish POS Tagger Evaluation")
        print("=" * 60)
        
        # Run comparisons
        results = self.compare_taggers()
        
        if not results:
            print("❌ No taggers could be evaluated successfully")
            return
        
        # Generate text report
        report = self.generate_comparison_report(results)
        
        # Save report to file
        with open('tagger_evaluation_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("\n📝 Detailed report saved as 'tagger_evaluation_report.txt'")
        
        # Create visualizations
        self.create_visualizations(results)
        
        # Print summary to console
        print("\n" + "=" * 60)
        print("EVALUATION SUMMARY")
        print("=" * 60)
        
        for tagger_name, data in results.items():
            print(f"\n{data['name']}:")
            print(f"  ✓ Processed: {data['sentences_processed']} sentences")
            print(f"  ✓ Total tokens: {data['total_tokens']}")
            if 'avg_processing_time' in data:
                print(f"  ✓ Avg time: {data['avg_processing_time']:.4f}s per sentence")
                print(f"  ✓ Speed: {data['tokens_per_second']:.1f} tokens/sec")
            print(f"  ✗ Errors: {len(data['errors'])}")
        
        print(f"\n🎯 Evaluation completed! Check the generated files:")
        print("   - tagger_evaluation_report.txt (detailed report)")
        print("   - tagger_comparison_report.png (visualizations)")

def quick_demo():
    """Quick demonstration of both taggers"""
    print("🔥 QUICK TURKISH POS TAGGER DEMO")
    print("=" * 40)
    
    test_sentence = "Bunu başından beri biliyordum zaten ."
    print(f"Test sentence: {test_sentence}\n")
    
    # Test legacy
    if LEGACY_AVAILABLE:
        try:
            print("1️⃣  Legacy Brill Tagger:")
            start = time.time()
            result = legacy_tag(test_sentence)
            elapsed = time.time() - start
            print(f"   Result: {result}")
            print(f"   Time: {elapsed:.4f}s\n")
        except Exception as e:
            print(f"   ❌ Failed: {e}\n")
    
    # Test modern
    try:
        print("2️⃣  Modern Tagger (Legacy mode):")
        tagger = ModernTurkishPOSTagger(model_type="legacy")
        start = time.time()
        result = tagger.tag(test_sentence)
        elapsed = time.time() - start
        print(f"   Result: {result}")
        print(f"   Time: {elapsed:.4f}s")
        print(f"   Info: {tagger.get_model_info()}\n")
    except Exception as e:
        print(f"   ❌ Failed: {e}\n")
    
    # Test BERT
    try:
        print("3️⃣  Modern Tagger (BERTurk mode):")
        bert_tagger = ModernTurkishPOSTagger(model_type="berturk")
        start = time.time()
        result = bert_tagger.tag(test_sentence)
        elapsed = time.time() - start
        print(f"   Result: {result}")
        print(f"   Time: {elapsed:.4f}s")
        print(f"   Info: {bert_tagger.get_model_info()}\n")
    except Exception as e:
        print(f"   ❌ Failed: {e}\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        quick_demo()
    else:
        evaluator = POSTaggerEvaluator()
        evaluator.run_comprehensive_evaluation()