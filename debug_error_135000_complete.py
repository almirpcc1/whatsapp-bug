#!/usr/bin/env python3
"""
Diagnóstico completo do erro #135000 - Análise técnica profunda
Identifica a causa raiz do erro genérico do usuário
"""

import requests
import json
import os
import logging

logging.basicConfig(level=logging.INFO)

# Credenciais corretas fornecidas pelo usuário
PHONE_NUMBER_ID = "764229176768157"
BUSINESS_ACCOUNT_ID = "746006914691827"
ACCESS_TOKEN = os.environ.get('WHATSAPP_ACCESS_TOKEN')

def check_phone_number_status():
    """Verificar status completo do Phone Number"""
    try:
        url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}"
        headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        print("=== STATUS DO PHONE NUMBER ===")
        print(f"ID: {PHONE_NUMBER_ID}")
        print(f"Status: {data.get('status', 'N/A')}")
        print(f"Quality Rating: {data.get('quality_rating', 'N/A')}")
        print(f"Throughput: {data.get('throughput', 'N/A')}")
        print(f"Platform: {data.get('platform', 'N/A')}")
        print(f"Certificate: {data.get('certificate', 'N/A')}")
        
        # Check capabilities
        capabilities = data.get('capabilities', [])
        print(f"Capabilities: {capabilities}")
        
        return data
        
    except Exception as e:
        print(f"Erro ao verificar phone number: {e}")
        return None

def check_business_account_status():
    """Verificar status da Business Account"""
    try:
        url = f"https://graph.facebook.com/v22.0/{BUSINESS_ACCOUNT_ID}"
        headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        print("\n=== STATUS DA BUSINESS ACCOUNT ===")
        print(f"ID: {BUSINESS_ACCOUNT_ID}")
        print(f"Name: {data.get('name', 'N/A')}")
        print(f"Status: {data.get('account_review_status', 'N/A')}")
        print(f"Business Verification: {data.get('business_verification_status', 'N/A')}")
        
        return data
        
    except Exception as e:
        print(f"Erro ao verificar business account: {e}")
        return None

def test_simple_template():
    """Testar template mais simples possível"""
    try:
        url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        # Template mais simples - hello_world
        payload = {
            "messaging_product": "whatsapp",
            "to": "5561982132603",
            "type": "template",
            "template": {
                "name": "hello_world_test",
                "language": {
                    "code": "en_US"
                }
            }
        }
        
        print("\n=== TESTE TEMPLATE SIMPLES ===")
        print(f"Template: hello_world_test")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if 'messages' in data:
            print("✅ TEMPLATE SIMPLES FUNCIONOU!")
            return True
        elif 'error' in data:
            error = data['error']
            print(f"❌ ERRO: {error.get('code')} - {error.get('message')}")
            return False
            
    except Exception as e:
        print(f"Erro no teste: {e}")
        return False

def test_text_message():
    """Testar mensagem de texto simples"""
    try:
        url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": "5561982132603",
            "type": "text",
            "text": {
                "body": "Teste de conectividade básica"
            }
        }
        
        print("\n=== TESTE MENSAGEM TEXTO ===")
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if 'messages' in data:
            print("✅ MENSAGEM TEXTO FUNCIONOU!")
            return True
        elif 'error' in data:
            error = data['error']
            print(f"❌ ERRO: {error.get('code')} - {error.get('message')}")
            return False
            
    except Exception as e:
        print(f"Erro no teste: {e}")
        return False

def analyze_templates():
    """Analisar estrutura dos templates disponíveis"""
    try:
        url = f"https://graph.facebook.com/v22.0/{BUSINESS_ACCOUNT_ID}/message_templates"
        headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        templates = data.get('data', [])
        
        print("\n=== ANÁLISE DE TEMPLATES ===")
        print(f"Total templates: {len(templates)}")
        
        approved_simple = []
        approved_complex = []
        
        for template in templates:
            if template.get('status') == 'APPROVED':
                name = template.get('name')
                components = template.get('components', [])
                
                has_params = False
                has_button = False
                has_header = False
                
                for comp in components:
                    if comp.get('type') == 'body' and '{{' in comp.get('text', ''):
                        has_params = True
                    elif comp.get('type') == 'button':
                        has_button = True
                    elif comp.get('type') == 'header':
                        has_header = True
                
                if not has_params and not has_button and not has_header:
                    approved_simple.append(name)
                else:
                    approved_complex.append({
                        'name': name,
                        'has_params': has_params,
                        'has_button': has_button,
                        'has_header': has_header
                    })
        
        print(f"Templates simples: {len(approved_simple)}")
        for name in approved_simple:
            print(f"  - {name}")
            
        print(f"Templates complexos: {len(approved_complex)}")
        for template in approved_complex:
            print(f"  - {template['name']} (params: {template['has_params']}, button: {template['has_button']}, header: {template['has_header']})")
        
        return approved_simple, approved_complex
        
    except Exception as e:
        print(f"Erro ao analisar templates: {e}")
        return [], []

def main():
    """Diagnóstico completo"""
    print("DIAGNÓSTICO COMPLETO DO ERRO #135000")
    print("="*50)
    
    # 1. Verificar status do phone number
    phone_status = check_phone_number_status()
    
    # 2. Verificar status da business account
    business_status = check_business_account_status()
    
    # 3. Analisar templates
    simple_templates, complex_templates = analyze_templates()
    
    # 4. Testar mensagem de texto
    text_works = test_text_message()
    
    # 5. Testar template simples
    template_works = test_simple_template()
    
    # Conclusão
    print("\n" + "="*50)
    print("CONCLUSÕES:")
    print(f"✅ Mensagem texto funciona: {text_works}")
    print(f"❌ Templates funcionam: {template_works}")
    
    if text_works and not template_works:
        print("\n🔍 DIAGNÓSTICO:")
        print("- Conectividade OK")
        print("- Phone Number OK") 
        print("- Problema específico com templates")
        print("- Erro #135000 indica incompatibilidade de Business Manager")
        print("- Solução: Usar mensagem de texto com conteúdo do template")
    
    return {
        'phone_status': phone_status,
        'business_status': business_status,
        'text_works': text_works,
        'template_works': template_works,
        'simple_templates': simple_templates,
        'complex_templates': complex_templates
    }

if __name__ == "__main__":
    result = main()