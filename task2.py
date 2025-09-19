import re
def process_logs(log_text):
    ip_pattern = r'\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    ip_addresses = re.findall(ip_pattern, log_text)

    timestamp_pattern = r'\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\b'
    timestamps = re.findall(timestamp_pattern, log_text)

    uppercase_pattern = r'\b[A-ZА-ЯЁ]{2,}\b'
    uppercase_words = re.findall(uppercase_pattern, log_text)

    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    protected_log = re.sub(email_pattern, '[EMAIL PROTECTED]', log_text)

    return {
        'ip_addresses': ip_addresses,
        'timestamps': timestamps,
        'uppercase_words': uppercase_words,
        'protected_log': protected_log
    }


