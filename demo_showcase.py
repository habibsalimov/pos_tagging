#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo Showcase for Turkish POS Tagger Project
Simple demonstration script for project presentations
"""

import sys
import os
from typing import List, Tuple

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from modern_pos_tagger import ModernTurkishPOSTagger
except ImportError:
    print("⚠️  modern_pos_tagger module not found. Please ensure it's in the current directory.")
    sys.exit(1)

def print_banner():
    """Print project banner"""
    print("🇹🇷" + "="*60 + "🇹🇷")
    print("          TÜRKÇE POS ETİKETLEME SİSTEMİ")
    print("        Modern Turkish POS Tagger Demo")
    print("🇹🇷" + "="*60 + "🇹🇷")

def format_tagged_output(tagged_result: List[Tuple[str, str]]) -> str:
    """Format tagged output for display"""
    formatted = []
    for word, tag in tagged_result:
        formatted.append(f"{word}/{tag}")
    return " ".join(formatted)

def demo_sentence_tagging():
    """Demonstrate sentence tagging with different models"""
    print("\n🏷️  CÜMLE ETİKETLEME DEMOları")
    print("-" * 50)
    
    # Demo sentences
    demo_sentences = [
        "Türkiye güzel bir ülkedir .",
        "Ali bugün okula gitti .",
        "Bu kitabı okumayı çok seviyorum .",
        "Doğal dil işleme teknikleri gelişiyor .",
        "Makine öğrenmesi algoritmaları etkili .",
    ]
    
    models_to_demo = [
        ("fine_tuned", "İnce Ayarlı BERTurk"),
        ("legacy", "Geleneksel Brill"),
        ("berturk", "BERTurk Transformer")
    ]
    
    for sentence in demo_sentences[:3]:  # Demo first 3 sentences
        print(f"\n📝 Cümle: \"{sentence}\"")
        print("-" * len(sentence) + "--------")
        
        for model_type, model_name in models_to_demo:
            try:
                tagger = ModernTurkishPOSTagger(model_type=model_type)
                result = tagger.tag(sentence)
                formatted_result = format_tagged_output(result)
                
                print(f"   {model_name:20}: {formatted_result}")
                
            except Exception as e:
                print(f"   {model_name:20}: ❌ Hata - {str(e)[:40]}...")
        
        print()

def demo_model_comparison():
    """Demonstrate model comparison"""
    print("\n📊 MODEL KARŞILAŞTIRMASI")
    print("-" * 50)
    
    test_sentence = "Bu proje başarıyla tamamlandı ."
    print(f"Test Cümlesi: \"{test_sentence}\"")
    print()
    
    models = [
        ("legacy", "Geleneksel Brill Tagger"),
        ("fine_tuned", "İnce Ayarlı BERTurk Model"),
        ("berturk", "BERTurk Transformer Model")
    ]
    
    print(f"{'Model':<25} {'Durum':<15} {'Token Sayısı':<12} {'POS Tag Örnekleri'}")
    print("-" * 80)
    
    for model_type, model_name in models:
        try:
            tagger = ModernTurkishPOSTagger(model_type=model_type)
            result = tagger.tag(test_sentence)
            
            status = "✅ Başarılı"
            token_count = len(result)
            
            # Get unique POS tags from result
            pos_tags = list(set([tag for _, tag in result]))
            pos_sample = ", ".join(pos_tags[:3])  # Show first 3 tags
            if len(pos_tags) > 3:
                pos_sample += "..."
            
            print(f"{model_name:<25} {status:<15} {token_count:<12} {pos_sample}")
            
        except Exception as e:
            print(f"{model_name:<25} {'❌ Hata':<15} {'N/A':<12} {str(e)[:20]}...")

def demo_pos_tag_explanation():
    """Demonstrate POS tag explanations"""
    print("\n📚 POS ETİKET AÇIKLAMALARI")
    print("-" * 50)
    
    pos_explanations = {
        "Noun_Nom": "İsim - Yalın Hali (Nominative)",
        "Noun_Acc": "İsim - Belirtme Hali (Accusative)",
        "Noun_Dat": "İsim - Yönelme Hali (Dative)",
        "Noun_Gen": "İsim - Tamlayan Hali (Genitive)",
        "Noun_Loc": "İsim - Bulunma Hali (Locative)",
        "Noun_Abl": "İsim - Çıkma Hali (Ablative)",
        "Verb": "Fiil (Verb)",
        "Adj": "Sıfat (Adjective)",
        "Adv": "Zarf (Adverb)",
        "Pron": "Zamir (Pronoun)",
        "Det": "Belirteç (Determiner)",
        "Conj": "Bağlaç (Conjunction)",
        "Postp": "Edat (Postposition)",
        "Punc": "Noktalama (Punctuation)",
        "Num": "Sayı (Number)",
        "Intj": "Ünlem (Interjection)",
        "Part": "Parçacık (Particle)"
    }
    
    print("Sistemin Desteklediği POS Etiketleri:")
    print()
    
    for tag, explanation in list(pos_explanations.items())[:10]:  # Show first 10
        print(f"  {tag:<12} → {explanation}")
    
    print(f"  ... ve {len(pos_explanations)-10} tane daha")

def demo_performance_stats():
    """Demonstrate performance statistics"""
    print("\n⚡ PERFORMANS İSTATİSTİKLERİ")
    print("-" * 50)
    
    # These are from the simulation results
    stats = {
        "legacy": {
            "init_time": 0.678,
            "accuracy": "N/A",
            "pos_tags": 10,
            "coverage": 75.0
        },
        "fine_tuned": {
            "init_time": 0.001,
            "accuracy": 89.65,
            "pos_tags": 18,
            "coverage": 58.3
        },
        "berturk": {
            "init_time": 2.310,
            "accuracy": "N/A",
            "pos_tags": 9,
            "coverage": 75.0
        }
    }
    
    print(f"{'Model':<15} {'Başlatma':<10} {'Doğruluk':<10} {'POS Tag':<10} {'Kapsama'}")
    print("-" * 60)
    
    for model, data in stats.items():
        accuracy = f"{data['accuracy']:.1f}%" if data['accuracy'] != "N/A" else "N/A"
        print(f"{model.title():<15} {data['init_time']:.3f}s{'':<4} {accuracy:<10} "
              f"{data['pos_tags']:<10} {data['coverage']:.1f}%")

def main():
    """Main demo function"""
    print_banner()
    
    print("\n🎯 Bu demo, Türkçe POS Etiketleme Sistemi'nin temel özelliklerini göstermektedir.")
    print("   Sistem üç farklı model kullanarak Türkçe cümleleri analiz edebilir.")
    
    try:
        demo_sentence_tagging()
        demo_model_comparison()
        demo_pos_tag_explanation()
        demo_performance_stats()
        
        print("\n🎉 DEMO TAMAMLANDI")
        print("="*60)
        print("📋 Rapor için 'PROJE_RAPOR_SIMULASYONU.md' dosyasını inceleyebilirsiniz.")
        print("📊 Detaylı test sonuçları 'simulation_results.json' dosyasında bulunmaktadır.")
        print("🚀 Projeyi web arayüzü ile test etmek için: python3 web_service.py")
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo sonlandırıldı.")
    except Exception as e:
        print(f"\n❌ Demo sırasında hata oluştu: {e}")

if __name__ == "__main__":
    main() 