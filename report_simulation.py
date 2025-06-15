#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Report Simulation for Turkish POS Tagger Project
Comprehensive testing and performance analysis for project report
"""

import time
import json
import os
import sys
from typing import List, Tuple, Dict, Any
from datetime import datetime
import logging

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from modern_pos_tagger import ModernTurkishPOSTagger, tag, create_tagger
except ImportError as e:
    print(f"⚠️  Warning: Could not import modern_pos_tagger: {e}")
    print("Creating mock implementation for demonstration...")
    
    class ModernTurkishPOSTagger:
        def __init__(self, model_type="legacy"):
            self.model_type = model_type
        
        def tag(self, sentence):
            # Mock implementation
            words = sentence.split()
            return [(word, "Noun" if word.istitle() else "Verb") for word in words if word.strip()]
        
        def batch_tag(self, sentences):
            return [self.tag(sentence) for sentence in sentences]
        
        def get_model_info(self):
            return {"model_type": self.model_type, "supports_batch": True, "language": "Turkish"}

class TurkishPOSTaggerReportSimulation:
    """Comprehensive test simulation for Turkish POS Tagger project"""
    
    def __init__(self):
        """Initialize the simulation with test data and models"""
        self.results = {}
        self.start_time = time.time()
        
        # Comprehensive Turkish test sentences
        self.test_sentences = [
            # Simple sentences
            "Merhaba dünya !",
            "Ali koştu .",
            "Bu kitap güzel .",
            
            # Complex sentences
            "Bunu başından beri biliyordum zaten .",
            "Çocuklar bahçede top oynuyorlar .",
            "Türkiye çok güzel bir ülkedir .",
            "Bu projeyi başarıyla tamamladık .",
            
            # Long sentences with multiple clauses
            "Geçen hafta arkadaşımla birlikte sinemaya gidip çok güzel bir film izledik .",
            "Profesörümüz bugün derste yeni bir konuyu anlattı ve ödev verdi .",
            "Yazın tatilde ailemle birlikte Antalya'ya gidip denizde yüzdük .",
            
            # Technical/academic sentences
            "Bu araştırmada makine öğrenmesi algoritmaları kullanıldı .",
            "Doğal dil işleme teknikleri Türkçe metinler için geliştirildi .",
            "Part-of-speech etiketleme sistemi yüksek doğruluk oranı elde etti .",
            
            # Questions and exclamations
            "Sen neredesin ?",
            "Ne kadar güzel bir gün !",
            "Bu nasıl mümkün olabilir ?",
            
            # Edge cases
            "123 sayısı çok büyük .",
            "E-posta adresi geçerli değil .",
            "COVID-19 pandemisi dünyayı etkiledi .",
        ]
        
        # Expected POS tag types
        self.expected_pos_types = {
            'Noun', 'Verb', 'Adj', 'Adv', 'Pron', 'Conj', 'Postp', 'Det', 
            'Num', 'Punc', 'Interj', 'X'
        }
        
        self.models_to_test = ["legacy", "fine_tuned", "berturk"]
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        print("🚀 Turkish POS Tagger Report Simulation Started")
        print("=" * 60)
    
    def test_model_initialization(self) -> Dict[str, Any]:
        """Test initialization of different models"""
        print("\n📦 Model Initialization Tests")
        print("-" * 40)
        
        init_results = {}
        
        for model_type in self.models_to_test:
            try:
                start_time = time.time()
                tagger = ModernTurkishPOSTagger(model_type=model_type)
                init_time = time.time() - start_time
                
                model_info = tagger.get_model_info()
                
                init_results[model_type] = {
                    "status": "success",
                    "initialization_time": init_time,
                    "model_info": model_info
                }
                
                print(f"✅ {model_type.upper()}: Initialized in {init_time:.3f}s")
                
            except Exception as e:
                init_results[model_type] = {
                    "status": "failed",
                    "error": str(e),
                    "initialization_time": None
                }
                print(f"❌ {model_type.upper()}: Failed - {e}")
        
        return init_results
    
    def test_basic_tagging_functionality(self) -> Dict[str, Any]:
        """Test basic tagging functionality across all models"""
        print("\n🏷️  Basic Tagging Functionality Tests")
        print("-" * 40)
        
        tagging_results = {}
        
        for model_type in self.models_to_test:
            try:
                tagger = ModernTurkishPOSTagger(model_type=model_type)
                model_results = {
                    "total_sentences": 0,
                    "total_tokens": 0,
                    "successful_tags": 0,
                    "unique_pos_tags": set(),
                    "average_tokens_per_sentence": 0,
                    "processing_time": 0,
                    "examples": []
                }
                
                start_time = time.time()
                
                for sentence in self.test_sentences[:10]:  # Test first 10 sentences
                    try:
                        result = tagger.tag(sentence)
                        
                        model_results["total_sentences"] += 1
                        model_results["total_tokens"] += len(result)
                        model_results["successful_tags"] += len(result)
                        
                        # Collect unique POS tags
                        for word, tag in result:
                            model_results["unique_pos_tags"].add(tag)
                        
                        # Store first 3 examples
                        if len(model_results["examples"]) < 3:
                            model_results["examples"].append({
                                "sentence": sentence,
                                "tagged_result": result
                            })
                    
                    except Exception as e:
                        print(f"⚠️  Error tagging sentence '{sentence[:30]}...': {e}")
                
                model_results["processing_time"] = time.time() - start_time
                model_results["unique_pos_tags"] = list(model_results["unique_pos_tags"])
                
                if model_results["total_sentences"] > 0:
                    model_results["average_tokens_per_sentence"] = (
                        model_results["total_tokens"] / model_results["total_sentences"]
                    )
                
                tagging_results[model_type] = model_results
                
                print(f"✅ {model_type.upper()}: {model_results['total_sentences']} sentences, "
                      f"{model_results['total_tokens']} tokens, "
                      f"{len(model_results['unique_pos_tags'])} unique POS tags")
                
            except Exception as e:
                tagging_results[model_type] = {"error": str(e)}
                print(f"❌ {model_type.upper()}: Failed - {e}")
        
        return tagging_results
    
    def test_performance_analysis(self) -> Dict[str, Any]:
        """Test performance characteristics of different models"""
        print("\n⚡ Performance Analysis")
        print("-" * 40)
        
        performance_results = {}
        
        # Test sentences of different lengths
        test_sets = {
            "short": [s for s in self.test_sentences if len(s.split()) <= 5],
            "medium": [s for s in self.test_sentences if 5 < len(s.split()) <= 10],
            "long": [s for s in self.test_sentences if len(s.split()) > 10]
        }
        
        for model_type in self.models_to_test:
            try:
                tagger = ModernTurkishPOSTagger(model_type=model_type)
                model_performance = {}
                
                for test_type, sentences in test_sets.items():
                    if not sentences:
                        continue
                    
                    # Time the processing
                    start_time = time.time()
                    total_tokens = 0
                    successful_sentences = 0
                    
                    for sentence in sentences:
                        try:
                            result = tagger.tag(sentence)
                            total_tokens += len(result)
                            successful_sentences += 1
                        except Exception:
                            pass
                    
                    processing_time = time.time() - start_time
                    
                    model_performance[test_type] = {
                        "sentences": len(sentences),
                        "successful_sentences": successful_sentences,
                        "total_tokens": total_tokens,
                        "processing_time": processing_time,
                        "tokens_per_second": total_tokens / processing_time if processing_time > 0 else 0,
                        "sentences_per_second": successful_sentences / processing_time if processing_time > 0 else 0
                    }
                
                performance_results[model_type] = model_performance
                
                print(f"✅ {model_type.upper()}: Performance analysis completed")
                
            except Exception as e:
                performance_results[model_type] = {"error": str(e)}
                print(f"❌ {model_type.upper()}: Performance test failed - {e}")
        
        return performance_results
    
    def test_batch_processing(self) -> Dict[str, Any]:
        """Test batch processing capabilities"""
        print("\n📦 Batch Processing Tests")
        print("-" * 40)
        
        batch_results = {}
        batch_sentences = self.test_sentences[:5]  # Use first 5 sentences for batch testing
        
        for model_type in self.models_to_test:
            try:
                tagger = ModernTurkishPOSTagger(model_type=model_type)
                
                # Test batch processing
                start_time = time.time()
                batch_result = tagger.batch_tag(batch_sentences)
                batch_time = time.time() - start_time
                
                # Test individual processing for comparison
                start_time = time.time()
                individual_results = []
                for sentence in batch_sentences:
                    individual_results.append(tagger.tag(sentence))
                individual_time = time.time() - start_time
                
                batch_results[model_type] = {
                    "batch_sentences": len(batch_sentences),
                    "batch_time": batch_time,
                    "individual_time": individual_time,
                    "speedup": individual_time / batch_time if batch_time > 0 else 0,
                    "batch_successful": len(batch_result),
                    "individual_successful": len(individual_results)
                }
                
                print(f"✅ {model_type.upper()}: Batch {batch_time:.3f}s vs Individual {individual_time:.3f}s")
                
            except Exception as e:
                batch_results[model_type] = {"error": str(e)}
                print(f"❌ {model_type.upper()}: Batch test failed - {e}")
        
        return batch_results
    
    def test_edge_cases(self) -> Dict[str, Any]:
        """Test edge cases and error handling"""
        print("\n🧪 Edge Cases and Error Handling")
        print("-" * 40)
        
        edge_cases = [
            ("", "empty_string"),
            ("   ", "whitespace_only"),
            ("Tek", "single_word"),
            ("123", "numbers_only"),
            ("!!!", "punctuation_only"),
            ("çok çok çok uzun bir cümle " * 10, "very_long_sentence"),
            ("Çok çeşitli özel karakterler: @#$%^&*()", "special_characters")
        ]
        
        edge_results = {}
        
        for model_type in self.models_to_test:
            try:
                tagger = ModernTurkishPOSTagger(model_type=model_type)
                model_edge_results = {}
                
                for test_input, test_name in edge_cases:
                    try:
                        result = tagger.tag(test_input)
                        model_edge_results[test_name] = {
                            "status": "success",
                            "input_length": len(test_input),
                            "output_tokens": len(result),
                            "result": result
                        }
                    except Exception as e:
                        model_edge_results[test_name] = {
                            "status": "error",
                            "error": str(e),
                            "input_length": len(test_input)
                        }
                
                edge_results[model_type] = model_edge_results
                print(f"✅ {model_type.upper()}: Edge cases tested")
                
            except Exception as e:
                edge_results[model_type] = {"error": str(e)}
                print(f"❌ {model_type.upper()}: Edge case testing failed - {e}")
        
        return edge_results
    
    def analyze_pos_tag_coverage(self, tagging_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze POS tag coverage and distribution"""
        print("\n📊 POS Tag Coverage Analysis")
        print("-" * 40)
        
        coverage_analysis = {}
        
        for model_type, results in tagging_results.items():
            if "error" in results:
                continue
            
            unique_tags = set(results.get("unique_pos_tags", []))
            expected_coverage = len(unique_tags & self.expected_pos_types)
            total_expected = len(self.expected_pos_types)
            
            coverage_analysis[model_type] = {
                "unique_tags_found": len(unique_tags),
                "expected_tags_covered": expected_coverage,
                "total_expected_tags": total_expected,
                "coverage_percentage": (expected_coverage / total_expected) * 100,
                "tags_found": list(unique_tags),
                "missing_expected_tags": list(self.expected_pos_types - unique_tags),
                "unexpected_tags": list(unique_tags - self.expected_pos_types)
            }
            
            print(f"✅ {model_type.upper()}: {coverage_analysis[model_type]['coverage_percentage']:.1f}% coverage "
                  f"({expected_coverage}/{total_expected} expected tags)")
        
        return coverage_analysis
    
    def generate_summary_statistics(self, all_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics for the report"""
        print("\n📈 Summary Statistics")
        print("-" * 40)
        
        summary = {
            "test_execution_time": time.time() - self.start_time,
            "models_tested": len(self.models_to_test),
            "test_sentences": len(self.test_sentences),
            "timestamp": datetime.now().isoformat(),
            "successful_models": [],
            "failed_models": [],
            "performance_comparison": {},
            "recommendation": ""
        }
        
        # Analyze which models succeeded
        for model_type in self.models_to_test:
            init_result = all_results.get("initialization", {}).get(model_type, {})
            if init_result.get("status") == "success":
                summary["successful_models"].append(model_type)
            else:
                summary["failed_models"].append(model_type)
        
        # Performance comparison
        performance_data = all_results.get("performance", {})
        for model_type, perf in performance_data.items():
            if "error" not in perf:
                avg_tokens_per_sec = 0
                count = 0
                for test_type, metrics in perf.items():
                    if isinstance(metrics, dict) and "tokens_per_second" in metrics:
                        avg_tokens_per_sec += metrics["tokens_per_second"]
                        count += 1
                
                if count > 0:
                    summary["performance_comparison"][model_type] = avg_tokens_per_sec / count
        
        # Generate recommendation
        if summary["successful_models"]:
            best_model = max(summary["performance_comparison"], 
                           key=summary["performance_comparison"].get, 
                           default=summary["successful_models"][0])
            summary["recommendation"] = f"Recommended model: {best_model}"
        else:
            summary["recommendation"] = "No models successfully initialized"
        
        print(f"✅ Test completed in {summary['test_execution_time']:.2f} seconds")
        print(f"✅ {len(summary['successful_models'])} models successful, {len(summary['failed_models'])} failed")
        print(f"✅ {summary['recommendation']}")
        
        return summary
    
    def save_results_to_file(self, all_results: Dict[str, Any], filename: str = "simulation_results.json"):
        """Save all results to a JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
            print(f"\n💾 Results saved to {filename}")
        except Exception as e:
            print(f"⚠️  Could not save results: {e}")
    
    def run_complete_simulation(self) -> Dict[str, Any]:
        """Run the complete test simulation"""
        print("\n🎯 Running Complete Turkish POS Tagger Simulation")
        print("=" * 60)
        
        all_results = {}
        
        # Run all test categories
        all_results["initialization"] = self.test_model_initialization()
        all_results["basic_tagging"] = self.test_basic_tagging_functionality()
        all_results["performance"] = self.test_performance_analysis()
        all_results["batch_processing"] = self.test_batch_processing()
        all_results["edge_cases"] = self.test_edge_cases()
        all_results["pos_coverage"] = self.analyze_pos_tag_coverage(all_results["basic_tagging"])
        all_results["summary"] = self.generate_summary_statistics(all_results)
        
        # Save results
        self.save_results_to_file(all_results)
        
        print("\n🎉 Simulation Complete!")
        print("=" * 60)
        print(f"Total execution time: {all_results['summary']['test_execution_time']:.2f} seconds")
        print(f"Models tested: {', '.join(self.models_to_test)}")
        print(f"Test sentences: {len(self.test_sentences)}")
        print(f"Recommendation: {all_results['summary']['recommendation']}")
        
        return all_results

def main():
    """Main function to run the simulation"""
    simulation = TurkishPOSTaggerReportSimulation()
    results = simulation.run_complete_simulation()
    
    print("\n📋 Quick Results Summary:")
    print("-" * 30)
    
    # Display key metrics
    for model_type in simulation.models_to_test:
        init_status = results["initialization"].get(model_type, {}).get("status", "unknown")
        basic_tokens = results["basic_tagging"].get(model_type, {}).get("total_tokens", 0)
        pos_coverage = results["pos_coverage"].get(model_type, {}).get("coverage_percentage", 0)
        
        print(f"{model_type.upper():>12}: Init={init_status:>7}, Tokens={basic_tokens:>3}, Coverage={pos_coverage:>5.1f}%")
    
    print("\n💡 Use 'simulation_results.json' for detailed report data")
    return results

if __name__ == "__main__":
    main() 