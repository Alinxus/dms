# Mass DM Sender

This project allows sending direct messages to multiple recipients on various social media platforms.

## CSV Format

Your CSV should have the following columns:
- platform (either "twitter" or "instagram")
- username (the username of the recipient)

## Usage

1. Prepare your CSV file according to the format above.
2. Upload the CSV file to the designated S3 bucket.
3. The system will automatically process the CSV and store the recipients.
4. Use the bulk DM sending API to send messages to the uploaded recipients.

## API Usage

Endpoint: [Your API Gateway Invoke URL]/send-bulk-dm

Method: POST

Body:
```json
{
  "platform": "twitter",
  "message": "Your message here",
  "batch_size": 10
}