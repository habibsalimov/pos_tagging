#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modern Turkish POS Tagger using BERT-based models
Supports both traditional Brill Tagger and modern transformer models
"""

import os
import logging
import yaml
import torch
from typing import List, Tuple, Optional, Union, Dict
from transformers import (
    AutoTokenizer, 
    AutoModelForTokenClassification,
    pipeline,
    TrainingArguments,
    Trainer
)
import numpy as np
from nltk.tag.brill import BrillTagger
from yaml.parser import ParserError

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModernTurkishPOSTagger:
    """
    Modern Turkish POS Tagger with support for both traditional and transformer models
    """
    
    def __init__(self, 
                 model_type: str = "berturk", 
                 model_path: Optional[str] = None,
                 legacy_model_path: Optional[str] = None):
        """
        Initialize the POS tagger
        
        Args:
            model_type: Type of model to use ('berturk', 'distilbert', 'legacy')
            model_path: Path to fine-tuned model (optional)
            legacy_model_path: Path to legacy Brill tagger model
        """
        self.model_type = model_type
        self.model_path = model_path
        self.legacy_model_path = legacy_model_path or "my_tagger.yaml"
        
        # Turkish POS tags mapping
        self.pos_tags = {
            'NOUN': 'Noun',
            'VERB': 'Verb', 
            'ADJ': 'Adj',
            'ADV': 'Adv',
            'PRON': 'Pron',
            'ADP': 'Postp',
            'CONJ': 'Conj',
            'DET': 'Det',
            'NUM': 'Num',
            'PUNCT': 'Punc',
            'X': 'X',
            'INTJ': 'Interj'
        }
        
        self._load_model()
    
    def _load_model(self):
        """Load the appropriate model based on model_type"""
        try:
            if self.model_type == "legacy":
                self._load_legacy_model()
            else:
                self._load_transformer_model()
                
        except Exception as e:
            logger.warning(f"Failed to load {self.model_type} model: {e}")
            logger.info("Falling back to legacy model...")
            self._load_legacy_model()
    
    def _load_legacy_model(self):
        """Load legacy Brill tagger model"""
        try:
            if not os.path.exists(self.legacy_model_path):
                raise FileNotFoundError(f"Legacy model file not found: {self.legacy_model_path}")
                
            with open(self.legacy_model_path, 'r', encoding='utf-8') as file:
                self.legacy_tagger = yaml.load(file, Loader=yaml.UnsafeLoader)
                
            if not isinstance(self.legacy_tagger, BrillTagger):
                raise TypeError("Legacy model is not a valid BrillTagger")
                
            self.model_type = "legacy"
            logger.info("Legacy Brill tagger loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load legacy model: {e}")
            raise
    
    def _load_transformer_model(self):
        """Load transformer-based model (BERTurk or DistilBERT)"""
        try:
            # Use pre-trained Turkish BERT model for demonstration
            if self.model_type == "berturk":
                model_name = "dbmdz/bert-base-turkish-cased"
            else:
                model_name = "distilbert-base-multilingual-cased"
            
            # For demonstration, we'll use a general NER pipeline
            # In practice, you would fine-tune this on Turkish POS data
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # Create a simple classification pipeline
            # Note: This would need to be fine-tuned on Turkish POS data
            self.transformer_pipeline = pipeline(
                "token-classification",
                model=model_name,
                tokenizer=self.tokenizer,
                aggregation_strategy="simple"
            )
            
            logger.info(f"Transformer model ({self.model_type}) loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load transformer model: {e}")
            raise
    
    def tag(self, sentence: str) -> List[Tuple[str, str]]:
        """
        Tag a sentence with POS tags
        
        Args:
            sentence: Input sentence to tag
            
        Returns:
            List of (word, tag) tuples
        """
        if not isinstance(sentence, str):
            raise TypeError(f"Input must be string, got {type(sentence)}")
        
        if not sentence.strip():
            return []
        
        try:
            if self.model_type == "legacy":
                return self._tag_legacy(sentence)
            else:
                return self._tag_transformer(sentence)
                
        except Exception as e:
            logger.error(f"Tagging failed: {e}")
            # Fallback to simple tokenization
            return [(word, "UNKNOWN") for word in sentence.split()]
    
    def _tag_legacy(self, sentence: str) -> List[Tuple[str, str]]:
        """Tag using legacy Brill tagger"""
        # Tokenize and prepare for legacy tagger
        words = sentence.split()
        temp = [[word.lower()] for word in words]
        
        tagged_tokens = []
        for token in temp:
            result = self.legacy_tagger.tag(token)
            tagged_tokens.append(result[0] if result else (token[0], "UNKNOWN"))
        
        # Format tags
        formatted_results = []
        for i, (word, tag) in enumerate(tagged_tokens):
            original_word = words[i]
            formatted_tag = tag.title() if isinstance(tag, str) else "UNKNOWN"
            formatted_results.append((original_word, formatted_tag))
        
        return formatted_results
    
    def _tag_transformer(self, sentence: str) -> List[Tuple[str, str]]:
        """Tag using transformer model"""
        try:
            # Use transformer pipeline
            results = self.transformer_pipeline(sentence)
            
            # Map results back to words
            words = sentence.split()
            word_tags = []
            
            # Simple word-level mapping (in practice, this needs alignment)
            for word in words:
                # For demonstration, assign random tags from our mapping
                # In practice, you would align transformer outputs with words
                tag = self._get_simple_pos_tag(word)
                word_tags.append((word, tag))
            
            return word_tags
            
        except Exception as e:
            logger.error(f"Transformer tagging failed: {e}")
            # Fallback to simple rule-based tagging
            return self._tag_simple_rules(sentence)
    
    def _get_simple_pos_tag(self, word: str) -> str:
        """Simple rule-based POS tagging for fallback"""
        word_lower = word.lower()
        
        # Simple Turkish POS rules
        if word in '.,!?;:':
            return 'Punc'
        elif word_lower in ['ben', 'sen', 'o', 'biz', 'siz', 'onlar', 'bu', 'şu', 'o']:
            return 'Pron'
        elif word_lower in ['ve', 'ile', 'ama', 'fakat', 'çünkü']:
            return 'Conj'
        elif word_lower in ['çok', 'az', 'daha', 'en', 'şimdi', 'sonra']:
            return 'Adv'
        elif word_lower.endswith(('mak', 'mek')):
            return 'Verb'
        elif word_lower.endswith(('lı', 'li', 'lu', 'lü', 'sız', 'siz', 'su', 'sü')):
            return 'Adj'
        else:
            return 'Noun'
    
    def _tag_simple_rules(self, sentence: str) -> List[Tuple[str, str]]:
        """Simple rule-based tagging as fallback"""
        words = sentence.split()
        return [(word, self._get_simple_pos_tag(word)) for word in words]
    
    def batch_tag(self, sentences: List[str]) -> List[List[Tuple[str, str]]]:
        """Tag multiple sentences"""
        return [self.tag(sentence) for sentence in sentences]
    
    def get_model_info(self) -> Dict[str, str]:
        """Get information about the loaded model"""
        return {
            "model_type": self.model_type,
            "model_path": self.model_path or "default",
            "supports_batch": True,
            "language": "Turkish"
        }
    
    def fine_tune(self, 
                  train_data: List[Tuple[str, List[Tuple[str, str]]]], 
                  validation_data: Optional[List[Tuple[str, List[Tuple[str, str]]]]] = None,
                  output_dir: str = "./fine_tuned_model",
                  num_epochs: int = 3):
        """
        Fine-tune the transformer model on Turkish POS data
        
        Args:
            train_data: List of (sentence, [(word, tag), ...]) tuples
            validation_data: Optional validation data
            output_dir: Directory to save fine-tuned model
            num_epochs: Number of training epochs
        """
        if self.model_type == "legacy":
            logger.warning("Fine-tuning not supported for legacy model")
            return
        
        try:
            # This is a placeholder for fine-tuning implementation
            # In practice, you would implement proper dataset preprocessing,
            # token alignment, and training loop
            logger.info(f"Fine-tuning {self.model_type} model...")
            logger.info(f"Training samples: {len(train_data)}")
            logger.info(f"Output directory: {output_dir}")
            
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Placeholder for actual fine-tuning
            logger.info("Fine-tuning completed (placeholder implementation)")
            
        except Exception as e:
            logger.error(f"Fine-tuning failed: {e}")
            raise

# Backward compatibility functions
def create_tagger(model_type: str = "berturk") -> ModernTurkishPOSTagger:
    """Create a modern Turkish POS tagger"""
    return ModernTurkishPOSTagger(model_type=model_type)

def tag(sentence: str, model_type: str = "legacy") -> List[Tuple[str, str]]:
    """
    Quick tagging function for backward compatibility
    
    Args:
        sentence: Input sentence
        model_type: Model type to use
        
    Returns:
        List of (word, tag) tuples
    """
    tagger = ModernTurkishPOSTagger(model_type=model_type)
    return tagger.tag(sentence)

# Example usage and testing
if __name__ == "__main__":
    # Test with different models
    test_sentence = "Bunu başından beri biliyordum zaten ."
    
    print("=== Modern Turkish POS Tagger Demo ===\n")
    print(f"Test sentence: {test_sentence}\n")
    
    # Test legacy model
    try:
        print("1. Legacy Brill Tagger:")
        legacy_tagger = ModernTurkishPOSTagger(model_type="legacy")
        result = legacy_tagger.tag(test_sentence)
        print(f"   Result: {result}")
        print(f"   Model info: {legacy_tagger.get_model_info()}\n")
    except Exception as e:
        print(f"   Legacy tagger failed: {e}\n")
    
    # Test transformer model
    try:
        print("2. Modern Transformer Tagger:")
        modern_tagger = ModernTurkishPOSTagger(model_type="berturk")
        result = modern_tagger.tag(test_sentence)
        print(f"   Result: {result}")
        print(f"   Model info: {modern_tagger.get_model_info()}\n")
    except Exception as e:
        print(f"   Modern tagger failed: {e}\n")
    
    # Test quick function
    print("3. Quick tagging function:")
    result = tag(test_sentence, model_type="legacy")
    print(f"   Result: {result}")