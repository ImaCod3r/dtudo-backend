import re

def validate_angolan_phone(phone: str) -> bool:
    """
    Valida números de telefone de Angola.
    Formatos aceitos:
    - 9XXXXXXXX (9 dígitos começando com 9)
    - +2449XXXXXXXX
    - 2449XXXXXXXX
    """
    # Remove espaços, parênteses e traços
    clean_phone = re.sub(r'[\s\(\)\-]', '', phone)
    
    # Regex para validar o formato angolano
    # Explicação: 
    # ^(?:\+244|244)? -> Opcionalmente começa com +244 ou 244
    # (9[1-9][0-9]{7})$ -> Seguido de 9 dígitos, começando com 9 e o segundo dígito de 1-9
    pattern = r'^(?:\+244|244)?(9[1-9][0-9]{7})$'
    
    return bool(re.match(pattern, clean_phone))

def format_angolan_phone(phone: str) -> str:
    """
    Formata o número para o padrão internacional +244XXXXXXXXX
    """
    if not validate_angolan_phone(phone):
        return phone
        
    clean_phone = re.sub(r'[\s\(\)\-]', '', phone)
    match = re.search(r'(9[1-9][0-9]{7})$', clean_phone)
    
    if match:
        return f"+244{match.group(1)}"
    
    return phone
