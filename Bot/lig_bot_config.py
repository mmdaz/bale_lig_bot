import os


class LigBotConfig:
    group_id = int(os.environ.get('GROUP_ID', None) or 568560388)
    group_access_hash = os.environ.get('GROUP_ACCESS_HASH', None) or "-993816927678809060"
    admin_user_id = int(os.environ.get('ADMIN_USER_ID', None) or 1314892980)
    db_name = os.environ.get('POSTGRES_DB', None) or "DametGarmLig"
    db_user = os.environ.get('POSTGRES_USER', None) or "muhammad"
    db_password = os.environ.get('POSTGRES_PASSWORD', None) or ""
    report_delay1 = int(os.environ.get('REPORT_DELAY1', None) or 15)
    report_delay2 = int(os.environ.get('REPORT_DELAY2', None) or 10)
    bot_token = os.environ.get('BOT_TOKEN', None) or ""
    db_host = os.environ.get('DB_HOST', None) or "localhost"
