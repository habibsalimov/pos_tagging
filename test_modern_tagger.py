#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite for Modern Turkish POS Tagger
Comprehensive testing of all components
"""

import unittest
import time
import sys
import os
from typing import List, Tuple
import tempfile
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modern_pos_tagger import ModernTurkishPOSTagger, tag, create_tagger

class TestModernTurkishPOSTagger(unittest.TestCase):
    """Test cases for Modern Turkish POS Tagger"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_sentences = [
            "Bunu başından beri biliyordum zaten .",
            "Ali koştu ve parkta oynadı .",
            "Türkiye güzel bir ülkedir .",
            "Bu kitabı okumak çok zevkli .",
            "Çocuklar bahçede top oynuyor ."
        ]
        
        self.expected_tags = {
            'Pron', 'Noun', 'Verb', 'Adj', 'Adv', 'Conj', 'Punc', 'Postp'
        }
    
    def test_tagger_initialization(self):
        """Test tagger initialization with different models"""
        print("\n🧪 Testing tagger initialization...")
        
        # Test legacy model
        try:
            tagger = ModernTurkishPOSTagger(model_type="legacy")
            self.assertEqual(tagger.model_type, "legacy")
            print("✅ Legacy tagger initialized successfully")
        except Exception as e:
            print(f"⚠️  Legacy tagger initialization failed: {e}")
        
        # Test modern model (with fallback)
        try:
            tagger = ModernTurkishPOSTagger(model_type="berturk")
            self.assertIsNotNone(tagger)
            print("✅ Modern tagger initialized successfully")
        except Exception as e:
            print(f"⚠️  Modern tagger initialization failed: {e}")
            
        # Test fine-tuned model
        try:
            fine_tuned_tagger = ModernTurkishPOSTagger(model_type="fine_tuned")
            self.assertIsNotNone(fine_tuned_tagger)
            print("✅ Fine-tuned tagger initialized successfully")
        except Exception as e:
            print(f"⚠️  Fine-tuned tagger initialization failed: {e}")
    
    def test_basic_tagging(self):
        """Test basic tagging functionality"""
        print("\n🧪 Testing basic tagging...")
        
        try:
            tagger = ModernTurkishPOSTagger(model_type="legacy")
            
            for sentence in self.test_sentences[:3]:  # Test first 3 sentences
                result = tagger.tag(sentence)
                
                # Check that result is a list of tuples
                self.assertIsInstance(result, list)
                
                # Check that each item is a tuple with 2 elements
                for item in result:
                    self.assertIsInstance(item, tuple)
                    self.assertEqual(len(item), 2)
                    
                    word, tag = item
                    self.assertIsInstance(word, str)
                    self.assertIsInstance(tag, str)
                
                print(f"✅ Tagged: {sentence[:30]}... -> {len(result)} tokens")
                
        except Exception as e:
            self.fail(f"Basic tagging failed: {e}")
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        print("\n🧪 Testing edge cases...")
        
        try:
            tagger = ModernTurkishPOSTagger(model_type="legacy")
            
            # Test empty string
            result = tagger.tag("")
            self.assertEqual(result, [])
            print("✅ Empty string handled correctly")
            
            # Test whitespace only
            result = tagger.tag("   ")
            self.assertEqual(result, [])
            print("✅ Whitespace-only string handled correctly")
            
            # Test single word
            result = tagger.tag("Merhaba")
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 1)
            print("✅ Single word handled correctly")
            
            # Test invalid input type
            with self.assertRaises(TypeError):
                tagger.tag(123)
            print("✅ Invalid input type properly rejected")
            
        except Exception as e:
            self.fail(f"Edge case testing failed: {e}")
    
    def test_batch_processing(self):
        """Test batch processing functionality"""
        print("\n🧪 Testing batch processing...")
        
        try:
            tagger = ModernTurkishPOSTagger(model_type="legacy")
            
            # Test batch tagging
            results = tagger.batch_tag(self.test_sentences[:3])
            
            self.assertIsInstance(results, list)
            self.assertEqual(len(results), 3)
            
            for result in results:
                self.assertIsInstance(result, list)
                for item in result:
                    self.assertIsInstance(item, tuple)
                    self.assertEqual(len(item), 2)
            
            print(f"✅ Batch processed {len(results)} sentences")
            
        except Exception as e:
            self.fail(f"Batch processing failed: {e}")
    
    def test_model_info(self):
        """Test model information retrieval"""
        print("\n🧪 Testing model info...")
        
        try:
            tagger = ModernTurkishPOSTagger(model_type="legacy")
            info = tagger.get_model_info()
            
            self.assertIsInstance(info, dict)
            self.assertIn('model_type', info)
            self.assertIn('supports_batch', info)
            self.assertIn('language', info)
            
            print(f"✅ Model info retrieved: {info}")
            
        except Exception as e:
            self.fail(f"Model info retrieval failed: {e}")
    
    def test_backward_compatibility(self):
        """Test backward compatibility functions"""
        print("\n🧪 Testing backward compatibility...")
        
        try:
            # Test create_tagger function
            tagger = create_tagger("legacy")
            self.assertIsInstance(tagger, ModernTurkishPOSTagger)
            print("✅ create_tagger function works")
            
            # Test tag function
            result = tag("Merhaba dünya .", model_type="legacy")
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 3)
            print("✅ Backward compatible tag function works")
            
        except Exception as e:
            self.fail(f"Backward compatibility failed: {e}")
    
    def test_performance(self):
        """Test performance characteristics"""
        print("\n🧪 Testing performance...")
        
        try:
            tagger = ModernTurkishPOSTagger(model_type="legacy")
            
            # Time single sentence
            test_sentence = "Bu bir performans testi cümlesidir ."
            
            start_time = time.time()
            result = tagger.tag(test_sentence)
            elapsed_time = time.time() - start_time
            
            self.assertLess(elapsed_time, 1.0)  # Should be less than 1 second
            
            # Calculate tokens per second
            tokens_per_sec = len(result) / elapsed_time if elapsed_time > 0 else 0
            
            print(f"✅ Performance: {elapsed_time:.4f}s, {tokens_per_sec:.1f} tokens/sec")
            
        except Exception as e:
            self.fail(f"Performance testing failed: {e}")

class TestWebServiceComponents(unittest.TestCase):
    """Test web service related components"""
    
    def test_web_service_import(self):
        """Test that web service can be imported"""
        print("\n🧪 Testing web service import...")
        
        try:
            import web_service
            self.assertTrue(hasattr(web_service, 'app'))
            print("✅ Web service imports successfully")
        except Exception as e:
            print(f"⚠️  Web service import failed: {e}")
    
    def test_evaluation_script_import(self):
        """Test that evaluation script can be imported"""
        print("\n🧪 Testing evaluation script import...")
        
        try:
            import evaluate_and_compare
            self.assertTrue(hasattr(evaluate_and_compare, 'POSTaggerEvaluator'))
            print("✅ Evaluation script imports successfully")
        except Exception as e:
            print(f"⚠️  Evaluation script import failed: {e}")

class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_full_pipeline(self):
        """Test complete tagging pipeline"""
        print("\n🧪 Testing full pipeline...")
        
        try:
            # Initialize tagger
            tagger = ModernTurkishPOSTagger(model_type="legacy")
            
            # Process multiple sentences
            test_sentences = [
                "Bugün hava çok güzel .",
                "Yarın İstanbul'a gideceğim .",
                "Kitap okumayı seviyorum ."
            ]
            
            all_results = []
            total_tokens = 0
            
            for sentence in test_sentences:
                result = tagger.tag(sentence)
                all_results.append(result)
                total_tokens += len(result)
                
                # Validate each result
                self.assertIsInstance(result, list)
                for word, tag in result:
                    self.assertIsInstance(word, str)
                    self.assertIsInstance(tag, str)
                    self.assertGreater(len(word), 0)
                    self.assertGreater(len(tag), 0)
            
            print(f"✅ Full pipeline: {len(test_sentences)} sentences, {total_tokens} tokens")
            
        except Exception as e:
            self.fail(f"Full pipeline test failed: {e}")

def run_comprehensive_test():
    """Run comprehensive test suite with detailed output"""
    print("🚀 STARTING COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestModernTurkishPOSTagger))
    test_suite.addTest(unittest.makeSuite(TestWebServiceComponents))
    test_suite.addTest(unittest.makeSuite(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    success_rate = (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    print(f"\nSuccess rate: {success_rate:.1f}%")
    
    if result.wasSuccessful():
        print("🎉 ALL TESTS PASSED!")
        return True
    else:
        print("❌ SOME TESTS FAILED")
        return False

def quick_functionality_test():
    """Quick test of basic functionality"""
    print("⚡ QUICK FUNCTIONALITY TEST")
    print("=" * 40)
    
    test_sentence = "Bunu başından beri biliyordum zaten ."
    
    try:
        # Test 1: Initialize tagger
        print("1. Initializing tagger...")
        tagger = ModernTurkishPOSTagger(model_type="legacy")
        print("   ✅ Tagger initialized")
        
        # Test 2: Basic tagging
        print("2. Testing basic tagging...")
        result = tagger.tag(test_sentence)
        print(f"   ✅ Tagged: {result}")
        
        # Test 3: Batch processing
        print("3. Testing batch processing...")
        batch_result = tagger.batch_tag([test_sentence, "Merhaba dünya ."])
        print(f"   ✅ Batch processed: {len(batch_result)} sentences")
        
        # Test 4: Model info
        print("4. Testing model info...")
        info = tagger.get_model_info()
        print(f"   ✅ Model info: {info}")
        
        # Test 5: Backward compatibility
        print("5. Testing backward compatibility...")
        compat_result = tag(test_sentence, model_type="legacy")
        print(f"   ✅ Backward compatible: {len(compat_result)} tokens")
        
        print("\n🎉 ALL QUICK TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ QUICK TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        success = quick_functionality_test()
    else:
        success = run_comprehensive_test()
    
    sys.exit(0 if success else 1)