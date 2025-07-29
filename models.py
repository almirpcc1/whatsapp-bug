from app import db
from datetime import datetime

class Campaign(db.Model):
    """Message campaign model"""
    id = db.Column(db.Integer, primary_key=True)
    template = db.Column(db.Text, nullable=False)
    buttons = db.Column(db.JSON, default=[])
    total_leads = db.Column(db.Integer, default=0)
    sent_count = db.Column(db.Integer, default=0)
    success_count = db.Column(db.Integer, default=0)
    error_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='pending')  # pending, sending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationship to messages
    messages = db.relationship('Message', backref='campaign', lazy=True, cascade='all, delete-orphan')

class Message(db.Model):
    """Individual message model"""
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    
    # Lead data
    phone_number = db.Column(db.String(20), nullable=False)
    lead_name = db.Column(db.String(100))
    lead_cpf = db.Column(db.String(14))
    
    # Message content
    message_text = db.Column(db.Text, nullable=False)
    buttons = db.Column(db.JSON, default=[])
    
    # WhatsApp Business API response
    whatsapp_message_id = db.Column(db.String(100))
    
    # Status tracking
    status = db.Column(db.String(20), default='pending')  # pending, sent, delivered, read, failed
    error_message = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sent_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    read_at = db.Column(db.DateTime)

class ButtonInteraction(db.Model):
    """Model para armazenar interações com botões"""
    id = db.Column(db.Integer, primary_key=True)
    
    # Identificadores da mensagem
    message_id = db.Column(db.String(200), nullable=False)
    from_phone = db.Column(db.String(20), nullable=False)
    phone_number_id = db.Column(db.String(50), nullable=False)
    
    # Dados da interação
    interaction_type = db.Column(db.String(50), nullable=False)  # button_reply, list_reply, etc.
    button_id = db.Column(db.String(100))
    button_title = db.Column(db.String(200))
    button_payload = db.Column(db.Text)
    
    # Dados do usuário que clicou
    user_name = db.Column(db.String(200))
    user_cpf = db.Column(db.String(14))
    
    # Timestamps
    interaction_timestamp = db.Column(db.String(50))  # Timestamp do WhatsApp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'message_id': self.message_id,
            'from_phone': self.from_phone,
            'phone_number_id': self.phone_number_id,
            'interaction_type': self.interaction_type,
            'button_id': self.button_id,
            'button_title': self.button_title,
            'button_payload': self.button_payload,
            'user_name': self.user_name,
            'user_cpf': self.user_cpf,
            'interaction_timestamp': self.interaction_timestamp,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class MessageStatus(db.Model):
    """Model para armazenar status de mensagens"""
    id = db.Column(db.Integer, primary_key=True)
    
    # Identificadores
    message_id = db.Column(db.String(200), nullable=False)
    recipient_phone = db.Column(db.String(20), nullable=False)
    phone_number_id = db.Column(db.String(50), nullable=False)
    
    # Status da mensagem
    status = db.Column(db.String(50), nullable=False)  # sent, delivered, read, failed
    status_timestamp = db.Column(db.String(50))
    
    # Dados de erro (se houver)
    error_code = db.Column(db.String(50))
    error_title = db.Column(db.String(200))
    error_message = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Converter para dicionário"""
        return {
            'id': self.id,
            'message_id': self.message_id,
            'recipient_phone': self.recipient_phone,
            'phone_number_id': self.phone_number_id,
            'status': self.status,
            'status_timestamp': self.status_timestamp,
            'error_code': self.error_code,
            'error_title': self.error_title,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class SentNumber(db.Model):
    """Model para rastrear números que já receberam mensagens com sucesso"""
    __tablename__ = 'sent_numbers'
    
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    lead_name = db.Column(db.String(100))
    lead_cpf = db.Column(db.String(14))
    first_sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    total_sent = db.Column(db.Integer, default=1)
    last_campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    last_message_id = db.Column(db.String(100))  # WhatsApp message ID
    
    def __repr__(self):
        return f'<SentNumber {self.phone_number}>'
    
    @classmethod
    def add_sent_number(cls, phone_number, lead_name=None, lead_cpf=None, campaign_id=None, message_id=None):
        """Adiciona ou atualiza um número enviado"""
        existing = cls.query.filter_by(phone_number=phone_number).first()
        
        if existing:
            # Atualizar registro existente
            existing.last_sent_at = datetime.utcnow()
            existing.total_sent += 1
            if lead_name:
                existing.lead_name = lead_name
            if lead_cpf:
                existing.lead_cpf = lead_cpf
            if campaign_id:
                existing.last_campaign_id = campaign_id
            if message_id:
                existing.last_message_id = message_id
            return existing
        else:
            # Criar novo registro
            sent_number = cls(
                phone_number=phone_number,
                lead_name=lead_name,
                lead_cpf=lead_cpf,
                last_campaign_id=campaign_id,
                last_message_id=message_id
            )
            return sent_number
    
    @classmethod
    def is_sent(cls, phone_number):
        """Verifica se um número já recebeu mensagem"""
        return cls.query.filter_by(phone_number=phone_number).first() is not None
    
    @classmethod
    def get_sent_numbers(cls):
        """Retorna lista de todos os números que já receberam mensagens"""
        return {record.phone_number for record in cls.query.all()}
