#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Demo Script for Modern Turkish POS Tagger
Demonstrates the capabilities of both legacy and modern taggers
"""

import time
import sys
from typing import List, Tuple
import traceback

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_colored(text: str, color: str = Colors.OKBLUE):
    """Print colored text to terminal"""
    print(f"{color}{text}{Colors.ENDC}")

def print_header(text: str):
    """Print header with decoration"""
    print_colored("=" * 60, Colors.HEADER)
    print_colored(text.center(60), Colors.HEADER)
    print_colored("=" * 60, Colors.HEADER)

def print_section(text: str):
    """Print section header"""
    print_colored(f"\n{text}", Colors.BOLD)
    print_colored("-" * len(text), Colors.OKCYAN)

def demonstrate_tagger(tagger_name: str, tag_function, test_sentences: List[str]):
    """Demonstrate a single tagger"""
    print_section(f"🏷️  {tagger_name}")
    
    total_time = 0
    total_tokens = 0
    successful_tags = 0
    
    for i, sentence in enumerate(test_sentences, 1):
        try:
            print(f"\n{i}. {Colors.OKBLUE}Input:{Colors.ENDC} {sentence}")
            
            start_time = time.time()
            result = tag_function(sentence)
            elapsed_time = time.time() - start_time
            
            total_time += elapsed_time
            total_tokens += len(result)
            successful_tags += 1
            
            print(f"   {Colors.OKGREEN}Output:{Colors.ENDC} {result}")
            print(f"   {Colors.OKCYAN}Time:{Colors.ENDC} {elapsed_time:.4f}s | {Colors.OKCYAN}Tokens:{Colors.ENDC} {len(result)}")
            
        except Exception as e:
            print(f"   {Colors.FAIL}Error:{Colors.ENDC} {str(e)}")
            continue
    
    # Summary statistics
    if successful_tags > 0:
        avg_time = total_time / successful_tags
        tokens_per_sec = total_tokens / total_time if total_time > 0 else 0
        
        print(f"\n{Colors.BOLD}📊 Summary Statistics:{Colors.ENDC}")
        print(f"   ✅ Successful tags: {successful_tags}/{len(test_sentences)}")
        print(f"   ⏱️  Average time: {avg_time:.4f}s per sentence")
        print(f"   🚀 Processing speed: {tokens_per_sec:.1f} tokens/second")
        print(f"   📊 Total tokens processed: {total_tokens}")
    else:
        print(f"\n{Colors.FAIL}❌ No successful tags completed{Colors.ENDC}")

def compare_taggers_side_by_side(test_sentence: str):
    """Compare different taggers on the same sentence"""
    print_section(f"🆚 Side-by-Side Comparison")
    print(f"{Colors.BOLD}Test sentence:{Colors.ENDC} {test_sentence}\n")
    
    # Try to import and test different taggers
    taggers_to_test = []
    
    # Legacy tagger
    try:
        from pos_tagger import tag as legacy_tag
        taggers_to_test.append(("Legacy Brill", legacy_tag))
    except ImportError:
        print(f"{Colors.WARNING}⚠️  Legacy tagger not available{Colors.ENDC}")
    
    # Modern taggers
    try:
        from modern_pos_tagger import ModernTurkishPOSTagger
        
        # Legacy mode
        legacy_modern = ModernTurkishPOSTagger(model_type="legacy")
        taggers_to_test.append(("Modern (Legacy)", legacy_modern.tag))
        
        # BERTurk mode
        berturk_tagger = ModernTurkishPOSTagger(model_type="berturk")
        taggers_to_test.append(("Modern (BERTurk)", berturk_tagger.tag))
        
    except Exception as e:
        print(f"{Colors.FAIL}❌ Modern tagger failed to load: {e}{Colors.ENDC}")
    
    # Run comparisons
    results = {}
    for tagger_name, tagger_func in taggers_to_test:
        try:
            start_time = time.time()
            result = tagger_func(test_sentence)
            elapsed_time = time.time() - start_time
            
            results[tagger_name] = {
                'result': result,
                'time': elapsed_time,
                'success': True
            }
            
        except Exception as e:
            results[tagger_name] = {
                'error': str(e),
                'success': False
            }
    
    # Display results
    for tagger_name, data in results.items():
        print(f"{Colors.BOLD}{tagger_name}:{Colors.ENDC}")
        if data['success']:
            print(f"   Result: {data['result']}")
            print(f"   Time: {data['time']:.4f}s")
        else:
            print(f"   {Colors.FAIL}Error: {data['error']}{Colors.ENDC}")
        print()

def interactive_demo():
    """Interactive demo where user can input sentences"""
    print_section("🎮 Interactive Demo")
    print("Enter Turkish sentences to tag (type 'quit' to exit)")
    
    # Initialize tagger
    try:
        from modern_pos_tagger import ModernTurkishPOSTagger
        tagger = ModernTurkishPOSTagger(model_type="berturk")
        print(f"{Colors.OKGREEN}✅ BERTurk tagger loaded successfully{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}❌ Failed to load BERTurk tagger: {e}{Colors.ENDC}")
        try:
            from modern_pos_tagger import ModernTurkishPOSTagger
            tagger = ModernTurkishPOSTagger(model_type="legacy")
            print(f"{Colors.WARNING}⚠️  Using legacy tagger as fallback{Colors.ENDC}")
        except Exception as e2:
            print(f"{Colors.FAIL}❌ All taggers failed to load: {e2}{Colors.ENDC}")
            return
    
    while True:
        try:
            sentence = input(f"\n{Colors.OKBLUE}Enter sentence:{Colors.ENDC} ").strip()
            
            if sentence.lower() in ['quit', 'exit', 'q']:
                print(f"{Colors.OKGREEN}👋 Goodbye!{Colors.ENDC}")
                break
            
            if not sentence:
                continue
            
            start_time = time.time()
            result = tagger.tag(sentence)
            elapsed_time = time.time() - start_time
            
            print(f"{Colors.OKGREEN}Result:{Colors.ENDC} {result}")
            print(f"{Colors.OKCYAN}Time:{Colors.ENDC} {elapsed_time:.4f}s | {Colors.OKCYAN}Tokens:{Colors.ENDC} {len(result)}")
            
        except KeyboardInterrupt:
            print(f"\n{Colors.OKGREEN}👋 Goodbye!{Colors.ENDC}")
            break
        except Exception as e:
            print(f"{Colors.FAIL}❌ Error: {e}{Colors.ENDC}")

def main():
    """Main demo function"""
    print_header("🔤 MODERN TURKISH POS TAGGER DEMO")
    print_colored("Welcome to the comprehensive demonstration!", Colors.OKGREEN)
    print_colored("This demo showcases both legacy and modern tagging approaches.\n", Colors.OKBLUE)
    
    # Test sentences
    test_sentences = [
        "Bunu başından beri biliyordum zaten .",
        "Ali koştu ve parkta oynadı .",
        "Türkiye güzel bir ülkedir .",
        "Bu kitabı okumak çok zevkli .",
        "Çocuklar bahçede top oynuyor ."
    ]
    
    # Demo mode selection
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        print("Demo modes:")
        print("  1. Full demo (all taggers)")
        print("  2. Quick comparison")
        print("  3. Interactive mode")
        
        try:
            choice = input(f"\n{Colors.OKBLUE}Select mode (1-3):{Colors.ENDC} ").strip()
            mode_map = {'1': 'full', '2': 'quick', '3': 'interactive'}
            mode = mode_map.get(choice, 'full')
        except KeyboardInterrupt:
            print(f"\n{Colors.OKGREEN}👋 Goodbye!{Colors.ENDC}")
            return
    
    if mode == 'interactive':
        interactive_demo()
        return
    elif mode == 'quick':
        compare_taggers_side_by_side("Bunu başından beri biliyordum zaten .")
        return
    
    # Full demo
    print_section("🎯 Testing Multiple Taggers")
    
    # Test legacy tagger
    try:
        from pos_tagger import tag as legacy_tag
        demonstrate_tagger("Legacy Brill Tagger", legacy_tag, test_sentences)
    except ImportError:
        print_colored("⚠️  Legacy tagger not available", Colors.WARNING)
    except Exception as e:
        print_colored(f"❌ Legacy tagger failed: {e}", Colors.FAIL)
    
    # Test modern taggers
    try:
        from modern_pos_tagger import ModernTurkishPOSTagger
        
        # Test legacy mode
        legacy_modern = ModernTurkishPOSTagger(model_type="legacy")
        demonstrate_tagger("Modern Tagger (Legacy Mode)", legacy_modern.tag, test_sentences)
        
        # Test BERTurk mode
        berturk_tagger = ModernTurkishPOSTagger(model_type="berturk")
        demonstrate_tagger("Modern Tagger (BERTurk Mode)", berturk_tagger.tag, test_sentences)
        
    except Exception as e:
        print_colored(f"❌ Modern tagger failed: {e}", Colors.FAIL)
        print_colored("Detailed error:", Colors.FAIL)
        traceback.print_exc()
    
    # Side-by-side comparison
    compare_taggers_side_by_side("Bunu başından beri biliyordum zaten .")
    
    # Final summary
    print_header("🎉 DEMO COMPLETED")
    print_colored("Thank you for trying the Modern Turkish POS Tagger!", Colors.OKGREEN)
    print_colored("", Colors.ENDC)
    print_colored("Next steps:", Colors.BOLD)
    print_colored("• Try the web interface: python web_service.py", Colors.OKBLUE)
    print_colored("• Run comprehensive evaluation: python evaluate_and_compare.py", Colors.OKBLUE)
    print_colored("• Explore the code in modern_pos_tagger.py", Colors.OKBLUE)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.OKGREEN}👋 Demo interrupted. Goodbye!{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Unexpected error: {e}{Colors.ENDC}")
        print(f"{Colors.FAIL}Please report this issue on GitHub{Colors.ENDC}")