import datetime

DATETIME = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
BUFFER_PATH = '/home/backup/'
BACKUPS_SIZE = 40
LOGS = True
LOG_FILE = open(BUFFER_PATH+'log.txt', 'a')

SERVICES = [
    {
        'name': f'mysql_{DATETIME}.sql',
        'command': 'mysqldump -uuser -psecret --all-databases>{BUFFER_PATH}{NAME}',
        'bucket': '8z41b7woknwpd02pmvgjjp5muva714',
        'bucket_path': 'mysql/'
    },
    {
        'name': f'forum_{DATETIME}.tar.gz',
        'command': 'tar -cf {BUFFER_PATH}{NAME} /var/www/html/xf',
        'bucket': '8z41b7woknwpd02pmvgjjp5muva714',
        'bucket_path': 'forum/'
    }
]
