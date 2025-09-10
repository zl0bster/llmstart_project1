#!/usr/bin/env python3
"""
Тест для итерации 5: Системный промт из файла
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_system_prompt_loading():
    """Тестирует загрузку системного промта из файла."""
    print("=== Тест загрузки системного промта ===")
    
    # Проверяем существование файла
    prompt_path = os.getenv('SYSTEM_PROMPT_PATH', 'docs/system_prompt.md')
    print(f"Путь к промту: {prompt_path}")
    print(f"Файл существует: {os.path.exists(prompt_path)}")
    
    if os.path.exists(prompt_path):
        with open(prompt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"Длина промта: {len(content)} символов")
        
        import hashlib
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        print(f"Хеш промта: {content_hash}")
    
    # Тестируем инициализацию LLM клиента
    print("\n=== Тест инициализации LLM клиента ===")
    try:
        from llm_client import LLMClient
        client = LLMClient()
        print(f"LLM клиент инициализирован успешно")
        print(f"Длина загруженного промта: {len(client.system_prompt)} символов")
        print(f"Промт начинается с: {client.system_prompt[:100]}...")
        return True
    except Exception as e:
        print(f"Ошибка инициализации LLM клиента: {e}")
        return False

if __name__ == "__main__":
    success = test_system_prompt_loading()
    if success:
        print("\n✅ Тест пройден успешно!")
    else:
        print("\n❌ Тест не пройден!")
