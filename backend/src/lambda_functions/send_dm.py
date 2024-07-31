import asyncio
import os
import gspread
from ..automation.instagram import InstagramAutomation
from ..automation.twitter import TwitterAutomation
from ..automation.linkedin import LinkedInAutomation  # Uncomment when implemented

async def main(messages_list):
    sa = gspread.service_account(filename='your-service-account-file.json')
    sheet = sa.open("MultiPlatformDMs")

    platforms = {
        'Instagram': InstagramAutomation('instagram_session.json'),
        'Twitter': TwitterAutomation('twitter_session.json'),
        'LinkedIn': LinkedInAutomation('linkedin_session.json'),  # Uncomment when implemented
    }

    for platform_name, automation in platforms.items():
        print(f"Starting {platform_name} automation...")
        await automation.setup()

        work_sheet = sheet.worksheet(platform_name)
        usernames = [row[0] for row in work_sheet.get_all_values()[1:] if row[0]]  # Skip header

        for username in usernames:
            message = random.choice(messages_list)
            success = await automation.send_dm(username, message)
            
            if success:
                print(f"Message sent to {username} on {platform_name}")
                update_sheet(sheet, f"{platform_name} DM Sent", username)
            else:
                print(f"Failed to send message to {username} on {platform_name}")
                update_sheet(sheet, f"{platform_name} Can't Send DM", username)
            
            remove_from_sheet(work_sheet, username)

        await automation.close()

def update_sheet(sheet, worksheet_name, username):
    work_sheet = sheet.worksheet(worksheet_name)
    work_sheet.append_row([username])

def remove_from_sheet(work_sheet, username):
    cell = work_sheet.find(username)
    if cell:
        work_sheet.delete_rows(cell.row)

if __name__ == "__main__":
    message_var_count = int(os.getenv("NUM_VARIATIONS", 1))
    messages = [os.getenv(f"DM_MESSAGE_{i+1}", f"Default message {i+1}") for i in range(message_var_count)]

    asyncio.run(main(messages))