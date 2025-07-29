#!/usr/bin/env python3
"""
Debug script to verify if the exact token is being used
"""
import requests
import json

def test_real_token():
    """Test with the EXACT token provided by user"""
    
    real_token = "EAAHUCvWVsdgBPBYPZBBM5wfGDmPCguYTbcmmWlQFGFukbGn5ArSLx2UNcY5KA3Ogb9AJOfAN1OpOoRrfWdNQLlAh9MRs3lreupw2P7JXJiNGTeSN5Y6nWKUM7Alx0rTsscDEIboFWBY62lZCqbKAZBgdZA2RSPMwO94nTrdFEygZAPSMrikHZCJZBuNZBYNujxaZA2lqHKK1pi3lPGTpMhIXpXMTnpZBcKZCmRZAJJNFH9w98565JQZDZD"
    
    print("🔍 TESTANDO TOKEN EXATO DO USUÁRIO...")
    print(f"🔑 Token: {real_token[:50]}...")
    print(f"📏 Comprimento: {len(real_token)} caracteres")
    
    # Test 1: Validate token directly with Facebook API
    test_url = "https://graph.facebook.com/v22.0/me"
    headers = {
        'Authorization': f'Bearer {real_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        print("\n🧪 TEST 1: Validating token with Facebook API...")
        response = requests.get(test_url, headers=headers, timeout=10)
        print(f"📊 STATUS: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ TOKEN VÁLIDO: {data}")
        else:
            error_data = response.json() if response.text else {}
            print(f"❌ TOKEN INVÁLIDO: {error_data}")
            
            # Check specific error
            if 'error' in error_data:
                error_code = error_data['error'].get('code', 'unknown')
                error_message = error_data['error'].get('message', 'unknown')
                print(f"🚨 ERRO {error_code}: {error_message}")
                
                if error_code == 190:
                    print("🔴 TOKEN EXPIRADO OU INVÁLIDO!")
                    return False
        
    except Exception as e:
        print(f"❌ ERRO NA REQUISIÇÃO: {e}")
        return False
    
    # Test 2: Send test request to local system
    print("\n🧪 TEST 2: Testing with local system...")
    test_data = {
        "leads": "5561999114066,Pedro,065.370.801-77",
        "template_names": ["ricardo_template_1753485866_2620345a"],
        "phone_number_ids": ["764495823408049"],
        "whatsapp_connection": {
            "access_token": real_token,
            "business_manager_id": "2089992404820473"
        }
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/api/ultra-speed',
            headers={'Content-Type': 'application/json'},
            json=test_data,
            timeout=30
        )
        
        print(f"📊 SISTEMA STATUS: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            session_id = result.get('session_id')
            print(f"✅ SISTEMA ACEITOU TOKEN: Session {session_id}")
            return True
        else:
            print(f"❌ SISTEMA REJEITOU: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERRO NO SISTEMA: {e}")
        return False

if __name__ == "__main__":
    success = test_real_token()
    print(f"\n🏁 TOKEN TEST RESULT: {'VÁLIDO' if success else 'INVÁLIDO'}")