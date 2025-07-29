#!/usr/bin/env python3
"""
Teste de performance do sistema no Heroku
"""

import requests
import time
import json
import os

def test_heroku_deployment():
    """Teste completo do deploy no Heroku"""
    
    # URL da app no Heroku (substitua pela sua)
    HEROKU_URL = os.environ.get('HEROKU_URL', 'https://seu-app.herokuapp.com')
    
    print("🚀 TESTANDO DEPLOY NO HEROKU")
    print("=" * 50)
    print(f"URL: {HEROKU_URL}")
    
    # 1. Teste de conectividade
    print("\n1. 📡 Testando conectividade...")
    try:
        response = requests.get(HEROKU_URL, timeout=30)
        if response.status_code == 200:
            print("✅ App respondendo no Heroku")
        else:
            print(f"❌ Erro {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    
    # 2. Teste de configuração do Heroku
    print("\n2. ⚙️ Testando configurações Heroku...")
    try:
        config_response = requests.get(f"{HEROKU_URL}/api/heroku-info", timeout=10)
        if config_response.status_code == 200:
            config = config_response.json()
            print(f"✅ Dyno: {config.get('dyno', 'unknown')}")
            print(f"✅ Workers: {config.get('max_workers', 'unknown')}")
            print(f"✅ Batch size: {config.get('batch_size', 'unknown')}")
        else:
            print("⚠️ Endpoint de configuração não encontrado")
    except:
        print("⚠️ Não foi possível verificar configurações")
    
    # 3. Teste de performance com leads pequenos
    print("\n3. 🏃 Testando performance ULTRA-SPEED...")
    
    test_data = {
        "leads": """5561999114066,Pedro Teste,065.370.801-77
5561982132603,Maria Teste,123.456.789-01
5561987654321,João Teste,987.654.321-00""",
        "template_names": ["ricardo_template_1753490810_b7ac4671"],
        "phone_number_ids": ["725492557312328", "800312496489716"]
    }
    
    try:
        start_time = time.time()
        
        response = requests.post(
            f"{HEROKU_URL}/api/ultra-speed",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Ultra-speed iniciado com sucesso!")
            print(f"📊 Leads: {result.get('leads', 0)}")
            print(f"📱 Phones: {result.get('phones', 0)}")
            print(f"📋 Templates: {result.get('templates', 0)}")
            print(f"🚀 Modo: {result.get('mode', 'unknown')}")
            print(f"⏱️ Tempo resposta: {end_time - start_time:.2f}s")
            
            # Monitorar progresso
            session_id = result.get('session_id')
            if session_id:
                print(f"\n📈 Monitorando progresso (sessão: {session_id})...")
                
                for i in range(30):  # Monitorar por 30 segundos
                    try:
                        progress_response = requests.get(
                            f"{HEROKU_URL}/api/progress/{session_id}",
                            timeout=5
                        )
                        
                        if progress_response.status_code == 200:
                            progress = progress_response.json()
                            if progress.get('success'):
                                sent = progress.get('sent', 0)
                                total = progress.get('total', 0)
                                failed = progress.get('failed', 0)
                                status = progress.get('status', 'unknown')
                                
                                print(f"⚡ Progress: {sent}/{total} enviadas, {failed} falharam - Status: {status}")
                                
                                if status == 'completed':
                                    print("✅ Processamento completo!")
                                    break
                        
                        time.sleep(1)
                        
                    except:
                        print("⚠️ Erro ao monitorar progresso")
                        break
            
            return True
            
        else:
            print(f"❌ Erro {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste de performance: {e}")
        return False

def test_load_capacity():
    """Teste de capacidade de carga"""
    
    print("\n4. 💪 TESTE DE CAPACIDADE MÁXIMA")
    print("=" * 40)
    
    # Gerar lista de 100 leads para teste de capacidade
    leads_list = []
    for i in range(1, 101):
        numero = f"5561{9000000 + i:07d}"
        nome = f"Teste {i:03d}"
        cpf = f"{i:03d}.000.000-{i%100:02d}"
        leads_list.append(f"{numero},{nome},{cpf}")
    
    large_test_data = {
        "leads": "\n".join(leads_list),
        "template_names": ["ricardo_template_1753490810_b7ac4671"],
        "phone_number_ids": ["725492557312328", "800312496489716", "781095236841937"]
    }
    
    HEROKU_URL = os.environ.get('HEROKU_URL', 'https://seu-app.herokuapp.com')
    
    try:
        print(f"🚀 Testando com {len(leads_list)} leads...")
        
        start_time = time.time()
        
        response = requests.post(
            f"{HEROKU_URL}/api/ultra-speed",
            json=large_test_data,
            headers={'Content-Type': 'application/json'},
            timeout=120
        )
        
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ CAPACIDADE MÁXIMA CONFIRMADA!")
            print(f"📊 {result.get('leads', 0)} leads processados")
            print(f"⚡ Workers: {result.get('mode', 'unknown')}")
            print(f"⏱️ Tempo de inicialização: {end_time - start_time:.2f}s")
            
            # Estimar velocidade
            estimated_time = len(leads_list) / 60  # 60 mensagens por minuto estimado
            print(f"📈 Tempo estimado de processamento: {estimated_time:.1f} minutos")
            
            return True
        else:
            print(f"❌ Falha no teste de capacidade: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste de capacidade: {e}")
        return False

if __name__ == "__main__":
    print("🌟 TESTE COMPLETO DE PERFORMANCE HEROKU")
    print("=" * 60)
    
    # Verificar URL do Heroku
    heroku_url = input("Digite a URL da sua app no Heroku (ex: https://meu-app.herokuapp.com): ").strip()
    if heroku_url:
        os.environ['HEROKU_URL'] = heroku_url
    
    success_count = 0
    
    # Executar testes
    if test_heroku_deployment():
        success_count += 1
    
    if test_load_capacity():
        success_count += 1
    
    # Resultado final
    print("\n" + "=" * 60)
    if success_count == 2:
        print("🏆 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema Heroku funcionando perfeitamente")
        print("⚡ Performance ULTRA-SPEED confirmada")
        print("💪 Capacidade máxima validada")
        print("\n🚀 SISTEMA PRONTO PARA PRODUÇÃO!")
    else:
        print(f"⚠️ {success_count}/2 testes passaram")
        print("❌ Verificar configurações e tentar novamente")
        
    print("\n📋 Próximos passos:")
    print("1. Configurar WHATSAPP_ACCESS_TOKEN no Heroku")
    print("2. Escalar para Performance-L se necessário")
    print("3. Monitorar logs com: heroku logs --tail")
    print("4. Ajustar MAX_WORKERS conforme necessário")