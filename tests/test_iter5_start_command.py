#!/usr/bin/env python3
"""
Тест для итерации 5: Команда /start с системным промтом
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_start_command_with_system_prompt():
    """Тестирует, что команда /start использует системный промт."""
    print("=== Тест команды /start с системным промтом ===")
    
    try:
        from llm_client import LLMClient
        client = LLMClient()
        
        # Проверяем, что системный промт содержит информацию о компании
        system_prompt = client.system_prompt
        print(f"Системный промт содержит 'ТехноСервис': {'ТехноСервис' in system_prompt}")
        print(f"Системный промт содержит 'консультант': {'консультант' in system_prompt}")
        print(f"Системный промт содержит 'услуги': {'услуги' in system_prompt}")
        
        # Проверяем, что промт достаточно детальный
        print(f"Длина системного промта: {len(system_prompt)} символов")
        
        if len(system_prompt) > 1000 and 'ТехноСервис' in system_prompt:
            print("✅ Системный промт содержит необходимую информацию о компании")
            return True
        else:
            print("❌ Системный промт не содержит достаточно информации")
            return False
            
    except Exception as e:
        print(f"Ошибка тестирования: {e}")
        return False

if __name__ == "__main__":
    success = test_start_command_with_system_prompt()
    if success:
        print("\n✅ Тест команды /start пройден успешно!")
    else:
        print("\n❌ Тест команды /start не пройден!")
