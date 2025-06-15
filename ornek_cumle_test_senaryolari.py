#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Örnek Cümleler Üzerinden Test Senaryoları
Turkish POS Tagger için Detaylı Test Analizi
"""

import sys
import os
import time
import json
from typing import List, Tuple, Dict, Any
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from modern_pos_tagger import ModernTurkishPOSTagger
except ImportError:
    print("⚠️  modern_pos_tagger modülü bulunamadı.")
    sys.exit(1)

class TurkishSentenceTestScenarios:
    """Türkçe cümleler üzerinden detaylı test senaryoları"""
    
    def __init__(self):
        self.models = ["legacy", "fine_tuned", "berturk"]
        self.test_results = {}
        
        # Test senaryoları ve beklenen sonuçlar
        self.test_scenarios = {
            "basit_cumleler": {
                "description": "Basit Türkçe Cümle Yapıları",
                "sentences": [
                    {
                        "text": "Ali okula gitti .",
                        "focus": "Temel özne-nesne-yüklem yapısı",
                        "expected_pos": ["Noun", "Noun", "Verb", "Punc"]
                    },
                    {
                        "text": "Kitap masada .",
                        "focus": "Basit var cümlesi",
                        "expected_pos": ["Noun", "Noun", "Punc"]
                    },
                    {
                        "text": "Bu çok güzel .",
                        "focus": "Zamir + zarf + sıfat yapısı",
                        "expected_pos": ["Pron", "Adv", "Adj", "Punc"]
                    }
                ]
            },
            
            "karmasik_cumleler": {
                "description": "Karmaşık Cümle Yapıları",
                "sentences": [
                    {
                        "text": "Öğrenciler dersten sonra kütüphaneye giderek ders çalıştılar .",
                        "focus": "Zarf tümleci + birleşik fiil yapısı",
                        "expected_pos": ["Noun", "Noun", "Postp", "Noun", "Verb", "Noun", "Verb", "Punc"]
                    },
                    {
                        "text": "Geçen yıl Ankara'da çalışan mühendis İstanbul'a taşındı .",
                        "focus": "Sıfat tümleci + yer adları",
                        "expected_pos": ["Adj", "Noun", "Noun", "Verb", "Noun", "Noun", "Verb", "Punc"]
                    },
                    {
                        "text": "Bugün hava çok soğuk olduğu için dışarı çıkmadık .",
                        "focus": "Sebep-sonuç bağlacı",
                        "expected_pos": ["Adv", "Noun", "Adv", "Adj", "Verb", "Conj", "Adv", "Verb", "Punc"]
                    }
                ]
            },
            
            "morfological_cases": {
                "description": "Türkçe Durum Ekleri",
                "sentences": [
                    {
                        "text": "Öğretmen öğrenciye kitabı verdi .",
                        "focus": "Yönelme hali (-e/-a)",
                        "expected_pos": ["Noun", "Noun_Dat", "Noun_Acc", "Verb", "Punc"]
                    },
                    {
                        "text": "Çocuk oyuncağını çantasından çıkardı .",
                        "focus": "Çıkma hali (-den/-dan)",
                        "expected_pos": ["Noun", "Noun_Acc", "Noun_Abl", "Verb", "Punc"]
                    },
                    {
                        "text": "Ailemin evinde mutlu günler geçirdik .",
                        "focus": "Tamlayan + bulunma hali",
                        "expected_pos": ["Noun_Gen", "Noun_Loc", "Adj", "Noun", "Verb", "Punc"]
                    }
                ]
            },
            
            "academic_technical": {
                "description": "Akademik ve Teknik Metinler",
                "sentences": [
                    {
                        "text": "Bu araştırmada makine öğrenmesi algoritmaları kullanılmıştır .",
                        "focus": "Akademik terminoloji",
                        "expected_pos": ["Pron", "Noun", "Noun", "Noun", "Noun", "Verb", "Punc"]
                    },
                    {
                        "text": "Doğal dil işleme teknikleri metin analizi için geliştirildi .",
                        "focus": "Teknik terimler",
                        "expected_pos": ["Adj", "Noun", "Noun", "Noun", "Noun", "Noun", "Conj", "Verb", "Punc"]
                    },
                    {
                        "text": "Algoritmanın performansı %95 doğruluk oranında ölçüldü .",
                        "focus": "Sayısal değerler + akademik ifadeler",
                        "expected_pos": ["Noun", "Noun", "Num", "Noun", "Noun", "Verb", "Punc"]
                    }
                ]
            },
            
            "edge_cases": {
                "description": "Özel Durumlar ve Zorlayıcı Örnekler",
                "sentences": [
                    {
                        "text": "COVID-19 pandemisi 2020'de başladı .",
                        "focus": "Kısaltmalar ve sayılar",
                        "expected_pos": ["Noun", "Noun", "Num", "Verb", "Punc"]
                    },
                    {
                        "text": "E-posta adresini example@test.com olarak güncelledim .",
                        "focus": "İnternet terimleri",
                        "expected_pos": ["Noun", "Noun", "Noun", "Conj", "Verb", "Punc"]
                    },
                    {
                        "text": "Ah ! Ne kadar güzel bir manzara !",
                        "focus": "Ünlemler ve duygu ifadeleri",
                        "expected_pos": ["Intj", "Punc", "Pron", "Adv", "Adj", "Det", "Noun", "Punc"]
                    }
                ]
            },
            
            "question_forms": {
                "description": "Soru Cümleleri",
                "sentences": [
                    {
                        "text": "Bu kitabı kim yazdı ?",
                        "focus": "Kim soru kelimesi",
                        "expected_pos": ["Pron", "Noun", "Pron", "Verb", "Punc"]
                    },
                    {
                        "text": "Nereye gidiyorsun ?",
                        "focus": "Nere- soru kökü + yönelme hali",
                        "expected_pos": ["Pron", "Verb", "Punc"]
                    },
                    {
                        "text": "Hangi üniverṡitede okuyorsun ?",
                        "focus": "Hangi sıfatı + bulunma hali",
                        "expected_pos": ["Det", "Noun", "Verb", "Punc"]
                    }
                ]
            }
        }
    
    def print_scenario_header(self, scenario_name: str, description: str):
        """Test senaryosu başlığını yazdır"""
        print(f"\n{'='*80}")
        print(f"🧪 {scenario_name.upper().replace('_', ' ')}")
        print(f"📝 {description}")
        print(f"{'='*80}")
    
    def analyze_sentence_result(self, sentence_data: Dict, results: Dict[str, List[Tuple[str, str]]]) -> Dict:
        """Cümle sonuçlarını analiz et"""
        analysis = {
            "sentence": sentence_data["text"],
            "focus": sentence_data["focus"],
            "expected": sentence_data.get("expected_pos", []),
            "results": {},
            "accuracy_scores": {},
            "pos_distribution": {}
        }
        
        for model_name, tagged_result in results.items():
            if not tagged_result:
                continue
                
            # POS tag dağılımı
            pos_tags = [tag for _, tag in tagged_result]
            pos_distribution = {}
            for tag in pos_tags:
                pos_distribution[tag] = pos_distribution.get(tag, 0) + 1
            
            analysis["results"][model_name] = tagged_result
            analysis["pos_distribution"][model_name] = pos_distribution
            
            # Basit doğruluk skoru (eğer beklenen sonuç varsa)
            if sentence_data.get("expected_pos"):
                expected = sentence_data["expected_pos"]
                actual = pos_tags
                
                # Uzunluk kontrol
                min_len = min(len(expected), len(actual))
                matches = sum(1 for i in range(min_len) if expected[i] == actual[i])
                accuracy = (matches / max(len(expected), len(actual))) * 100
                analysis["accuracy_scores"][model_name] = accuracy
        
        return analysis
    
    def run_sentence_scenario(self, scenario_name: str, scenario_data: Dict) -> List[Dict]:
        """Bir senaryo grubunu çalıştır"""
        self.print_scenario_header(scenario_name, scenario_data["description"])
        
        scenario_results = []
        
        for i, sentence_data in enumerate(scenario_data["sentences"], 1):
            print(f"\n📝 Test {i}: {sentence_data['text']}")
            print(f"🎯 Odak: {sentence_data['focus']}")
            print("-" * 60)
            
            # Her model için test et
            model_results = {}
            for model_name in self.models:
                try:
                    tagger = ModernTurkishPOSTagger(model_type=model_name)
                    start_time = time.time()
                    result = tagger.tag(sentence_data["text"])
                    processing_time = time.time() - start_time
                    
                    model_results[model_name] = result
                    
                    # Sonucu formatla ve yazdır
                    formatted_result = " ".join([f"{word}/{tag}" for word, tag in result])
                    print(f"{model_name.upper():>12}: {formatted_result}")
                    print(f"{'':>12}  ⏱️  {processing_time:.4f}s")
                    
                except Exception as e:
                    print(f"{model_name.upper():>12}: ❌ Hata - {str(e)[:50]}...")
                    model_results[model_name] = []
            
            # Analiz yap
            analysis = self.analyze_sentence_result(sentence_data, model_results)
            scenario_results.append(analysis)
            
            # Doğruluk skorlarını göster (eğer varsa)
            if analysis["accuracy_scores"]:
                print("\n📊 Doğruluk Skorları:")
                for model, score in analysis["accuracy_scores"].items():
                    print(f"{'':>12}  {model.upper()}: {score:.1f}%")
        
        return scenario_results
    
    def generate_comparative_analysis(self, all_results: Dict[str, List[Dict]]) -> Dict:
        """Karşılaştırmalı analiz oluştur"""
        print(f"\n{'='*80}")
        print("📊 KARŞILAŞTIRMALI ANALİZ")
        print(f"{'='*80}")
        
        comparative_analysis = {
            "model_performance": {model: {"total_tests": 0, "total_accuracy": 0, "avg_accuracy": 0} 
                                 for model in self.models},
            "pos_tag_usage": {model: {} for model in self.models},
            "scenario_performance": {},
            "best_model_per_scenario": {}
        }
        
        # Model performansını hesapla
        for scenario_name, results in all_results.items():
            scenario_accuracy = {model: [] for model in self.models}
            
            for result in results:
                for model in self.models:
                    if model in result["accuracy_scores"]:
                        accuracy = result["accuracy_scores"][model]
                        scenario_accuracy[model].append(accuracy)
                        comparative_analysis["model_performance"][model]["total_tests"] += 1
                        comparative_analysis["model_performance"][model]["total_accuracy"] += accuracy
                
                # POS tag kullanımını topla
                for model in self.models:
                    if model in result["pos_distribution"]:
                        for tag, count in result["pos_distribution"][model].items():
                            if tag not in comparative_analysis["pos_tag_usage"][model]:
                                comparative_analysis["pos_tag_usage"][model][tag] = 0
                            comparative_analysis["pos_tag_usage"][model][tag] += count
            
            # Senaryo bazında en iyi modeli bul
            avg_scenario_accuracy = {}
            for model in self.models:
                if scenario_accuracy[model]:
                    avg_accuracy = sum(scenario_accuracy[model]) / len(scenario_accuracy[model])
                    avg_scenario_accuracy[model] = avg_accuracy
            
            if avg_scenario_accuracy:
                best_model = max(avg_scenario_accuracy, key=avg_scenario_accuracy.get)
                comparative_analysis["best_model_per_scenario"][scenario_name] = {
                    "model": best_model,
                    "accuracy": avg_scenario_accuracy[best_model]
                }
                comparative_analysis["scenario_performance"][scenario_name] = avg_scenario_accuracy
        
        # Ortalama doğruluk hesapla
        for model in self.models:
            perf = comparative_analysis["model_performance"][model]
            if perf["total_tests"] > 0:
                perf["avg_accuracy"] = perf["total_accuracy"] / perf["total_tests"]
        
        return comparative_analysis
    
    def print_comparative_results(self, analysis: Dict):
        """Karşılaştırmalı sonuçları yazdır"""
        
        # 1. Genel Model Performansı
        print("\n🏆 GENEL MODEL PERFORMANSI")
        print("-" * 50)
        print(f"{'Model':<15} {'Test Sayısı':<12} {'Ort. Doğruluk':<15} {'Değerlendirme'}")
        print("-" * 60)
        
        for model, perf in analysis["model_performance"].items():
            if perf["total_tests"] > 0:
                grade = "🥇 Mükemmel" if perf["avg_accuracy"] >= 90 else \
                       "🥈 İyi" if perf["avg_accuracy"] >= 80 else \
                       "🥉 Orta" if perf["avg_accuracy"] >= 70 else "📈 Gelişim Gerekli"
                
                print(f"{model.title():<15} {perf['total_tests']:<12} "
                      f"{perf['avg_accuracy']:.1f}%{'':<10} {grade}")
        
        # 2. Senaryo Bazında En İyi Modeller
        print("\n🎯 SENARYO BAZINDA EN İYİ MODELLER")
        print("-" * 50)
        
        for scenario, best in analysis["best_model_per_scenario"].items():
            scenario_display = scenario.replace("_", " ").title()
            print(f"{scenario_display:<25}: {best['model'].title()} ({best['accuracy']:.1f}%)")
        
        # 3. POS Tag Kullanım İstatistikleri
        print("\n🏷️  EN ÇOKKULLANILAN POS TAGLERİ")
        print("-" * 50)
        
        for model in self.models:
            if analysis["pos_tag_usage"][model]:
                print(f"\n{model.title()} Modeli:")
                # En çok kullanılan 5 tag
                sorted_tags = sorted(analysis["pos_tag_usage"][model].items(), 
                                   key=lambda x: x[1], reverse=True)[:5]
                for tag, count in sorted_tags:
                    print(f"  {tag:<12}: {count} kez")
    
    def save_detailed_results(self, all_results: Dict, analysis: Dict, filename: str = "ornek_cumle_test_sonuclari.json"):
        """Detaylı sonuçları kaydet"""
        output_data = {
            "test_date": datetime.now().isoformat(),
            "test_scenarios": all_results,
            "comparative_analysis": analysis,
            "summary": {
                "total_scenarios": len(all_results),
                "total_sentences": sum(len(results) for results in all_results.values()),
                "models_tested": self.models
            }
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False, default=str)
            print(f"\n💾 Detaylı sonuçlar '{filename}' dosyasına kaydedildi.")
        except Exception as e:
            print(f"⚠️  Sonuçlar kaydedilemedi: {e}")
    
    def run_all_scenarios(self):
        """Tüm test senaryolarını çalıştır"""
        print("🇹🇷" + "="*78 + "🇹🇷")
        print("     TÜRKÇE POS TAGGER - ÖRNEK CÜMLE TEST SENARYOLARI")
        print("🇹🇷" + "="*78 + "🇹🇷")
        
        all_results = {}
        
        # Her senaryoyu çalıştır
        for scenario_name, scenario_data in self.test_scenarios.items():
            scenario_results = self.run_sentence_scenario(scenario_name, scenario_data)
            all_results[scenario_name] = scenario_results
        
        # Karşılaştırmalı analiz
        comparative_analysis = self.generate_comparative_analysis(all_results)
        self.print_comparative_results(comparative_analysis)
        
        # Sonuçları kaydet
        self.save_detailed_results(all_results, comparative_analysis)
        
        print(f"\n🎉 TÜM TEST SENARYOLARI TAMAMLANDI!")
        print(f"{'='*80}")
        print(f"📊 {len(self.test_scenarios)} senaryo grubu test edildi")
        print(f"📝 {sum(len(scenario['sentences']) for scenario in self.test_scenarios.values())} örnek cümle analiz edildi")
        print(f"🤖 {len(self.models)} farklı model karşılaştırıldı")
        
        return all_results, comparative_analysis

def main():
    """Ana test fonksiyonu"""
    test_runner = TurkishSentenceTestScenarios()
    results, analysis = test_runner.run_all_scenarios()
    
    print("\n💡 RAPOR İÇİN ÖNERİLER:")
    print("-" * 30)
    print("1. 'ornek_cumle_test_sonuclari.json' dosyasını raporda veri kaynağı olarak kullanın")
    print("2. Senaryo bazında en iyi model performanslarını tablolar halinde sunun")
    print("3. POS tag doğruluk oranlarını grafiklerle gösterin")
    print("4. Morfological case'lerin doğru tanınma oranlarını vurgulayın")
    print("5. Edge case'lerdeki başarı oranlarını öne çıkarın")
    
    return results, analysis

if __name__ == "__main__":
    main() 