from ._anvil_designer import preferencesTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class preferences(preferencesTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

  def get_trade_entry(self):
    self.load_accounts()
    self.setup_event_handlers()
    return self.trade_entry_preferences
    
  def get_trade_exit(self):
    return self.trade_exit_preferences
  
  def get_auto_exit(self):
    self.load_accounts_autoexit()
    self.setup_event_handlers_autoexit()
    return self.auto_exit_preferences

  def load_accounts(self):
    self.accounts = anvil.server.call('get_all_accounts')
    print(f"Accounts: {self.accounts}")
    self.accounts_dropdown.items = [account['user_name'] for account in self.accounts]
    
  def setup_event_handlers(self):
    self.accounts_dropdown.set_event_handler('change', self.accounts_dropdown_change)
  
  def accounts_dropdown_change(self, **event_args):
    selected_user = self.accounts_dropdown.selected_value
    self.current_account = selected_user
    print(f"Selected user: {selected_user}")
    
  def submit_preferences_entry_click(self, **event_args):
    """This method is called when the button is clicked"""
    properties = {
      "account_user": self.accounts_dropdown.selected_value,
      "buy_strike": self.buy_strike_field.text,
      "sell_strike": self.sell_strike_field.text,
      "option_type": self.option_type_dropdown.selected_value,
      "expiry_preference": self.expiry_field.selected_value
    }
    print("Trade entry properties:", properties)
    anvil.server.call('trade_entry_submit', properties)
    
  def exit_trade_click(self, **event_args):
    """This method is called when the button is clicked"""
    exit_trade_id = self.field_trade_id.text
    print("Exiting trade:", exit_trade_id)
    anvil.server.call('exit_trade', exit_trade_id)
    print("Trade exited.")

  def load_accounts_autoexit(self):
    self.accounts = anvil.server.call('get_all_accounts')
    print(f"Accounts: {self.accounts}")
    self.accounts_dropdown_autoexit.items = [account['user_name'] for account in self.accounts]
    
  def setup_event_handlers_autoexit(self):
    self.accounts_dropdown_autoexit.set_event_handler('change', self.accounts_dropdown_change_autoexit)

  def accounts_dropdown_change_autoexit(self, **event_args):
    selected_user = self.accounts_dropdown_autoexit.selected_value
    self.current_account = selected_user
    print(f"Selected user: {selected_user}")
  
  def submit_preferences_autoexit_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    properties = {
      "account_user": self.accounts_dropdown_autoexit.selected_value,
      "nifty_target": self.nifty_target_field.text,
      "nifty_stoploss": self.nifty_stoploss_field.text,
      "pnl_target": self.target_field.text,
      "pnl_stoploss": self.nifty_stoploss_field.text
    }
    print("autoexit properties:", properties)
    anvil.server.call('autoexit_submit', properties)
    