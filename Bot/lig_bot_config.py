import os

class LigBotConfig:
    group_id = int(os.environ.get('GROUP_ID', None) or 568560388)
    group_access_hash = os.environ.get('GROUP_ACCESS_HASH', None) or "-993816927678809060"
    admin_user_id = int(os.environ.get('ADMIN_USER_ID', None) or 1314892980)
    db_name = os.environ.get('POSTGRES_DB', None) or "DametGarmLig"
    db_user = os.environ.get('POSTGRES_USER', None) or "muhammad"
    db_password = os.environ.get('POSTGRES_PASSWORD', None) or "1540487768"
    report_delay = int(os.environ.get('REPORT_DELAY', None)) or 15
    bot_token = os.environ.get('BOT_TOKEN', None) or "4da1a22c3bd8f29afcc59fdcc82721c901134f1a"

