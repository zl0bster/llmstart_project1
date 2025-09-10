#!/usr/bin/env python3
"""
Тест для итерации 5: Проверка стратегии сбора контактов
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_contact_collection_strategy():
    """Тестирует, что системный промт содержит стратегию сбора контактов."""
    print("=== Тест стратегии сбора контактов ===")
    
    try:
        from llm_client import LLMClient
        client = LLMClient()
        
        system_prompt = client.system_prompt
        
        # Проверяем ключевые элементы стратегии сбора контактов
        checks = [
            ("ВАЖНО: В первую очередь выясни контактные данные", "Приоритет сбора контактов"),
            ("как к вам обращаться", "Запрос имени"),
            ("какая у вас компания", "Запрос компании"),
            ("для связи с менеджером", "Запрос телефона"),
            ("для отправки предложения", "Запрос email"),
            ("непринужденно", "Непринужденный стиль"),
            ("Кстати, как к вам обращаться", "Примеры фраз"),
            ("ПРИОРИТЕТ: Сначала узнай контакты", "Приоритет контактов")
        ]
        
        passed_checks = 0
        for check_text, description in checks:
            if check_text in system_prompt:
                print(f"✅ {description}: найдено")
                passed_checks += 1
            else:
                print(f"❌ {description}: не найдено")
        
        print(f"\nПройдено проверок: {passed_checks}/{len(checks)}")
        
        if passed_checks >= len(checks) * 0.8:  # 80% проверок должны пройти
            print("✅ Стратегия сбора контактов реализована корректно")
            return True
        else:
            print("❌ Стратегия сбора контактов реализована неполно")
            return False
            
    except Exception as e:
        print(f"Ошибка тестирования: {e}")
        return False

if __name__ == "__main__":
    success = test_contact_collection_strategy()
    if success:
        print("\n✅ Тест стратегии сбора контактов пройден успешно!")
    else:
        print("\n❌ Тест стратегии сбора контактов не пройден!")
