import faust

class AttackLog(faust.Record, serializer='json'):
    uri: str
    method: str
    rule_id: int
    http_version: float
    attack_content: list
    server_host: str
    server_port: int
    attack_time: float
    rule_action: str
    attack_category: str
    attack_severity: str
    attack_ip: str