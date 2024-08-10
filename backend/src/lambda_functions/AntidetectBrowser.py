class AntiDetectBrowser:
    def __init__(self, account_manager):
        self.account_manager = account_manager
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()

    def create_context_for_account(self, account_id):
        account_data = self.account_manager.get_account(account_id)
        context = self.browser.new_context(
            proxy={"server": account_data['proxy']},
            user_agent=account_data['user_agent'],
            storage_state=account_data['session_data']
        )
        return context

    def perform_action_for_account(self, account_id, action):
        context = self.create_context_for_account(account_id)
        page = context.new_page()
        try:
            # Perform the specified action
            action(page)
            # Save updated session data
            self.account_manager.update_session(account_id, context.storage_state())
        finally:
            context.close()