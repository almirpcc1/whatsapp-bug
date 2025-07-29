"""
Sistema MEGA LOTE VELOCIDADE SUPREMA UNIVERSAL

COMO USAR PARA MÁXIMA VELOCIDADE:
1. Se sua BM tem 5 números: Abra 5 abas do sistema
2. Em cada aba selecione um Phone Number ID diferente
3. Divida sua lista total em 5 partes (ex: 29k ÷ 5 = 5.8k por aba)
4. Execute simultaneamente em todas as abas
5. Resultado: Velocidade 5x multiplicada!

CONFIGURAÇÕES ULTRA-OTIMIZADAS:
- Batch size: 1000 mensagens por lote
- Threads: até 200 threads paralelos
- Pausas: eliminadas (0.0001s-0.01s)
- Rate limit: pausa ultra-mínima (0.1s)
- Memória: limpeza automática

UNIVERSAL: Funciona com qualquer BM (1-10+ números)
"""

import json
import time
import logging
import threading
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from services.whatsapp_business_api import WhatsAppBusinessAPI

class SimpleMegaBatch:
    """Sistema simplificado de MEGA LOTE para listas grandes"""
    
    def __init__(self):
        self.whatsapp_service = WhatsAppBusinessAPI()
        self.is_running = False
        self.total_leads = 0
        self.processed = 0
        self.success = 0
        self.errors = 0
        self.current_batch = 0
        self.total_batches = 0
        self.batch_size = 1000  # VELOCIDADE SUPREMA UNIVERSAL - lotes ultra-massivos para qualquer BM
        
    def start_mega_processing(self, leads, template_name='modelo_5', phone_number_id=None):
        """Inicia o processamento MEGA LOTE"""
        self.is_running = True
        self.total_leads = len(leads)
        self.total_batches = (len(leads) + self.batch_size - 1) // self.batch_size
        self.processed = 0
        self.success = 0
        self.errors = 0
        self.current_batch = 0
        self.phone_number_id = phone_number_id
        
        logging.info(f"MEGA LOTE INICIADO: {self.total_leads} leads em {self.total_batches} lotes")
        lead_preview = [f"{lead['nome']} - {lead['numero']}" for lead in leads[:10]]
        logging.info(f"LISTA DE LEADS RECEBIDA: {lead_preview}")  # Log primeiros 10
        
        try:
            # Processar em lotes
            for batch_index in range(self.total_batches):
                self.current_batch = batch_index + 1
                
                # Calcular range do lote
                start_idx = batch_index * self.batch_size
                end_idx = min(start_idx + self.batch_size, len(leads))
                batch_leads = leads[start_idx:end_idx]
                
                logging.info(f"PROCESSANDO LOTE {self.current_batch}/{self.total_batches}: {len(batch_leads)} leads")
                
                # Processar lote
                batch_success, batch_errors = self.process_batch(batch_leads, template_name, self.phone_number_id)
                
                # Atualizar contadores
                self.processed += len(batch_leads)
                self.success += batch_success
                self.errors += batch_errors
                
                logging.info(f"LOTE {self.current_batch} COMPLETO: {batch_success} sucessos, {batch_errors} erros")
                logging.info(f"PROGRESSO TOTAL: {self.processed}/{self.total_leads} ({(self.processed/self.total_leads)*100:.1f}%)")
                
                # VELOCIDADE SUPREMA UNIVERSAL ULTRA-OTIMIZADA - pausas eliminadas
                if self.total_leads > 10000:
                    time.sleep(0.0001)  # Pausa ultra-mínima para listas enormes (29k+)
                elif self.total_leads > 1000:
                    time.sleep(0.001)   # Pausa mínima para listas grandes
                else:
                    time.sleep(0.005)   # Pausa micro para listas pequenas
                
                # Limpeza de memória ultra-otimizada para máxima velocidade
                if self.current_batch % 50 == 0:  # Muito menos limpezas = velocidade suprema
                    import gc
                    gc.collect()
                    logging.info(f"MEGA LOTE: Limpeza de memória no lote {self.current_batch}")
                    time.sleep(0.001)  # Pausa ultra-mínima apenas durante limpeza
                
        except Exception as e:
            logging.error(f"Erro no processamento MEGA LOTE: {e}")
        finally:
            self.is_running = False
            logging.info(f"MEGA LOTE FINALIZADO: {self.success} sucessos, {self.errors} erros de {self.total_leads} total")
            
            # Manter dados por mais tempo para listas grandes
            def clear_stats_later():
                import time
                clear_time = 600 if self.total_leads > 10000 else 300  # 10 min para listas grandes, 5 min normais
                time.sleep(clear_time)
                self.total_leads = 0
                self.processed = 0
                self.success = 0
                self.errors = 0
                self.current_batch = 0
                self.total_batches = 0
            
            import threading
            clear_thread = threading.Thread(target=clear_stats_later, daemon=True)
            clear_thread.start()
    
    def process_batch(self, batch_leads, template_name, phone_number_id=None):
        """Processa um lote de leads"""
        success_count = 0
        error_count = 0
        
        def send_message(lead_data):
            try:
                phone = lead_data['numero']
                nome = lead_data['nome']
                cpf = lead_data['cpf']
                
                # USAR PHONE ID SELECIONADO PELO USUÁRIO (ABA ESPECÍFICA)
                selected_phone_id = phone_number_id or '708063449062586'  # Fallback default
                
                # ENVIAR APENAS TEMPLATES APROVADOS - SEM FALLBACK
                logging.info(f"Enviando template APROVADO {template_name} para {nome} - {phone} via Phone {selected_phone_id}")
                success, response = self.whatsapp_service.send_template_message(
                    phone=phone,
                    template_name=template_name,
                    language_code='en',
                    parameters=[cpf, nome],  # {{1}} = CPF, {{2}} = Nome
                    phone_number_id=selected_phone_id  # Phone específico da aba
                )
                
                if success:
                    logging.info(f"SUCESSO: {nome} - {phone}")
                    return True
                else:
                    # Fix error handling for both dict and string responses
                    if isinstance(response, dict):
                        error_msg = response.get('error', 'Erro desconhecido')
                        if isinstance(error_msg, dict):
                            error_msg = error_msg.get('message', 'Erro desconhecido')
                    else:
                        error_msg = str(response)
                    
                    # Rate limit detection e handling ultra-otimizado
                    if 'rate limit' in error_msg.lower() or 'application request limit' in error_msg.lower() or '403' in error_msg:
                        logging.warning(f"RATE LIMIT detectado para {nome} - {phone}, aguardando 0.1s...")
                        time.sleep(0.1)  # Pausa ultra-mínima para rate limit
                        return False
                    
                    logging.error(f"ERRO: {nome} - {phone}: {error_msg}")
                    return False
                    
            except Exception as e:
                nome = lead_data.get('nome', 'Desconhecido') if isinstance(lead_data, dict) else 'Desconhecido'
                logging.error(f"EXCEÇÃO: {nome} - {str(e)}")
                return False
        
        # VELOCIDADE SUPREMA UNIVERSAL ULTRA-OTIMIZADA - paralelismo absoluto máximo
        if self.total_leads > 10000:
            max_workers = min(200, len(batch_leads))  # ABSOLUTO MÁXIMO threads para listas enormes
        elif self.total_leads > 1000:
            max_workers = min(150, len(batch_leads))  # SUPREMO threads para listas grandes
        else:
            max_workers = min(120, len(batch_leads))  # ULTRA threads para pequenas
            
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(send_message, lead) for lead in batch_leads]
            
            for future in as_completed(futures):
                try:
                    success = future.result(timeout=30)
                    if success:
                        success_count += 1
                    else:
                        error_count += 1
                except Exception as e:
                    logging.error(f"Erro no future: {e}")
                    error_count += 1
        
        return success_count, error_count
    
    def get_status(self):
        """Retorna status atual"""
        progress_percent = 0
        if self.total_leads > 0:
            progress_percent = (self.processed / self.total_leads) * 100
        
        return {
            'is_running': self.is_running,
            'total_leads': self.total_leads,
            'processed': self.processed,
            'success': self.success,
            'errors': self.errors,
            'current_batch': self.current_batch,
            'total_batches': self.total_batches,
            'progress_percent': progress_percent
        }
        
    def get_ultra_status(self):
        """Retorna status do sistema ultra (compatibilidade)"""
        progress_percent = 0
        if self.total_leads > 0:
            progress_percent = int((self.processed / self.total_leads) * 100)
        
        return {
            'is_running': self.is_running,
            'total_leads': self.total_leads,
            'processed': self.processed,
            'success': self.success,
            'errors': self.errors,
            'current_batch': self.current_batch,
            'total_batches': self.total_batches,
            'progress_percent': progress_percent
        }

# Instância global
mega_batch = SimpleMegaBatch()