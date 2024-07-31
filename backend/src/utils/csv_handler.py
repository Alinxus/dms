import csv

def read_recipients(file_path):
    recipients = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            recipients.append({
                'platform': row['platform'],
                'username': row['username']
            })
    return recipients