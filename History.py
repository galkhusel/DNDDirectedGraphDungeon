import datetime

def dungeon_crawl_logger(msg):
    """
    Logs messages related to the dungeon crawl.
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('dungeon_crawl.log', 'a') as log_file:
        log_file.write(f'{timestamp} - {msg}\n')