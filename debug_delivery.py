#!/usr/bin/env python3
"""
Debug da entrega de mensagens - Por que não chegam aos destinatários?
"""

import requests
import logging

logging.basicConfig(level=logging.INFO)

def debug_delivery():
    """Debug completo da entrega de mensagens"""
    
    # Token atual
    access_token = "EAAKYElksPsEBPN6szHJFCl6WsxZBW2kHnqve8RLTOUCyKS99j0UCZAOslWZCGbTXZA4k0QFeZBJ3cNBKnuqDGfJxlNNld2Rz7Cm0863RzMRJBk7HkwuvbZA7TSAy30OlGjQHpRihPCCzyMuGaVoombue544bCEC9bhv12wFu3K8fbiSPkWjvrGWGe5z8vQQyvKuPZBonZAGwyslwlqGbIpwosTcYKtupJ6LXDzHneXyv8oaQpUkPHDgecYmeWDMRHLIZD"
    
    business_account_id = "639849885789886"
    api_version = "v22.0"
    base_url = f"https://graph.facebook.com/{api_version}"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    print("🔍 DEBUGGING DELIVERY ISSUES...")
    
    # 1. Verificar status da conta WhatsApp Business
    print("\n1️⃣ Verificando status da conta WhatsApp Business...")
    
    account_response = requests.get(
        f"{base_url}/{business_account_id}",
        headers=headers,
        timeout=10
    )
    
    print(f"Status: {account_response.status_code}")
    if account_response.status_code == 200:
        account_data = account_response.json()
        print(f"Account Status: {account_data}")
    
    # 2. Verificar status detalhado dos phone numbers
    print("\n2️⃣ Verificando status detalhado dos phone numbers...")
    
    phones_response = requests.get(
        f"{base_url}/{business_account_id}/phone_numbers",
        headers=headers,
        timeout=10
    )
    
    if phones_response.status_code == 200:
        phones_data = phones_response.json()
        for phone in phones_data.get('data', []):
            phone_id = phone.get('id')
            display_number = phone.get('display_phone_number')
            quality_rating = phone.get('quality_rating')
            throughput = phone.get('throughput', {})
            platform_type = phone.get('platform_type')
            
            print(f"\n📱 Phone ID: {phone_id}")
            print(f"   📞 Number: {display_number}")
            print(f"   ⭐ Quality: {quality_rating}")
            print(f"   🚀 Throughput: {throughput}")
            print(f"   💻 Platform: {platform_type}")
            
            # Verificar status específico do phone number
            phone_detail_response = requests.get(
                f"{base_url}/{phone_id}",
                headers=headers,
                timeout=10
            )
            
            if phone_detail_response.status_code == 200:
                phone_detail = phone_detail_response.json()
                print(f"   📋 Status Detalhado: {phone_detail}")
    
    # 3. Testar com número próprio (conhecido)
    print("\n3️⃣ Testando entrega para número conhecido...")
    
    test_phone_id = "743171782208180"  # Primeiro número
    target_number = "+5561999114066"  # Número de teste
    
    # Enviar mensagem de texto simples
    text_payload = {
        "messaging_product": "whatsapp",
        "to": target_number,
        "type": "text",
        "text": {
            "body": "Teste de entrega - Sistema WhatsApp"
        }
    }
    
    print(f"📤 Enviando mensagem de texto para {target_number}...")
    
    send_response = requests.post(
        f"{base_url}/{test_phone_id}/messages",
        headers=headers,
        json=text_payload,
        timeout=15
    )
    
    print(f"Status: {send_response.status_code}")
    print(f"Response: {send_response.text}")
    
    if send_response.status_code == 200:
        response_data = send_response.json()
        message_id = response_data.get('messages', [{}])[0].get('id')
        print(f"✅ Message ID: {message_id}")
        
        # 4. Consultar status da mensagem
        print("\n4️⃣ Consultando status da mensagem...")
        
        # Aguardar um pouco antes de consultar
        import time
        time.sleep(3)
        
        # Consultar status via Message ID não é disponível diretamente
        # Mas podemos verificar analytics
        analytics_response = requests.get(
            f"{base_url}/{business_account_id}/conversation_analytics",
            headers=headers,
            params={
                'start': '1753720000',  # Timestamp de hoje
                'end': '1753730000',
                'granularity': 'DAILY',
                'metric_types': 'SENT,DELIVERED,READ'
            },
            timeout=10
        )
        
        print(f"Analytics Status: {analytics_response.status_code}")
        if analytics_response.status_code == 200:
            print(f"Analytics: {analytics_response.text}")
    
    # 5. Verificar limitações da conta
    print("\n5️⃣ Verificando limitações da conta...")
    
    limits_response = requests.get(
        f"{base_url}/{business_account_id}?fields=messaging_api_rate_limit_hit,account_review_status",
        headers=headers,
        timeout=10
    )
    
    print(f"Limits Status: {limits_response.status_code}")
    if limits_response.status_code == 200:
        print(f"Limits: {limits_response.text}")

if __name__ == "__main__":
    debug_delivery()