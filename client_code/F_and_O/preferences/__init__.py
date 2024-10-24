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
    self.user = anvil.users.get_user()

  def get_trade_entry(self):
    self.load_accounts()
    self.setup_event_handlers()
    return self.trade_entry_preferences
    
  def get_trade_exit(self):
    return self.trade_exit_preferences
  
  def get_auto_exit(self):
    return self.auto_exit_preferences

  def load_accounts(self):
    self.accounts = anvil.server.call('get_all_accounts')
    print(f"Accounts: {self.accounts}")
    self.accounts_dropdown.items = ["All"] + [account['username'] for account in self.accounts]    
  
  def setup_event_handlers(self):
    self.accounts_dropdown.set_event_handler('change', self.accounts_dropdown_change)
  
  def accounts_dropdown_change(self, **event_args):
    selected_user = self.accounts_dropdown.selected_value
    self.current_account = selected_user
    print(f"Selected user: {selected_user}")
    
  def submit_preferences_entry_click(self, **event_args):
    """This method is called when the button is clicked"""
    properties = {
      "full_name": self.accounts_dropdown.selected_value,
      "buy_strike": self.buy_strike_field.text,
      "sell_strike": self.sell_strike_field.text,
      "option_type": self.option_type_dropdown.selected_value,
      "expiry_preference": self.expiry_field.selected_value,
      "margin_allocation": self.margin_allocation_field.text,
    }
    response = anvil.server.call('trade_entry_submit', properties)
    anvil.alert(f"From server ({response['status']}): {response['message']}")

    
  def exit_trade_click(self, **event_args):
    """This method is called when the button is clicked"""
    properties = {
      "id": self.field_trade_id.text,
      "partial_exit_percentage": self.partial_exit_field.text,
    }
    response = anvil.server.call('exit_trade', properties)
    anvil.alert(f"From server ({response['status']}): {response['message']}")

  def accounts_dropdown_change_autoexit(self, **event_args):
    selected_user = self.accounts_dropdown_autoexit.selected_value
    self.current_account = selected_user
    print(f"Selected user: {selected_user}")
  
  def submit_preferences_autoexit_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    properties = {
      "id": self.field_trade_id_auto.text,
      "nifty_target": self.nifty_target_field.text,
      "nifty_stoploss": self.nifty_stoploss_field.text,
      "partial_exit_percentage": self.partial_autoexit_field.text,
    }
    response = anvil.server.call('autoexit_submit', properties)
    anvil.alert(f"From server ({response['status']}): {response['message']}")    

  def clear_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    response = anvil.server.call('delete_exited')
    anvil.alert(f"From server ({response['status']}): {response['message']}")    

    