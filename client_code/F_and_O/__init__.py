from ._anvil_designer import F_and_OTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .preferences import preferences
import json 

class F_and_O(F_and_OTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.accounts = None
    self.setup_trades_grid()
    self.load_accounts()
    self.setup_event_handlers()

  def setup_trades_grid(self):
    self.trades_grid.columns = [c for c in self.trades_grid.columns if c['title'] != 'Column 3']

  def load_accounts(self):
    self.accounts = anvil.server.call('get_all_accounts')
    self.accounts_dropdown.items = [account['user_name'] for account in self.accounts]

  def setup_event_handlers(self):
    self.accounts_dropdown.set_event_handler('change', self.accounts_dropdown_change)

  def update_strategy_preferences(self, preference_type):
    self.strategy_preferences_section.clear()
    preference = getattr(preferences(), f"get_{preference_type}")()
    preference.remove_from_parent()
    self.strategy_preferences_section.add_component(preference, full_width_row=True)

  def trade_entry_click(self, **event_args):
    self.update_strategy_preferences('trade_entry')

  def trade_exit_click(self, **event_args):
    self.update_strategy_preferences('trade_exit')

  def auto_exit_click(self, **event_args):
    self.update_strategy_preferences('auto_exit')

  def update_strategy_visibility(self, strategy_number):
    self.strategy_1_section.visible = (strategy_number == 1)

  def strategy_1_click(self, **event_args):
    self.update_strategy_visibility(1)

  def strategy_2_click(self, **event_args):
    self.update_strategy_visibility(2)

  def strategy_3_click(self, **event_args):
    self.update_strategy_visibility(3)

  def accounts_dropdown_change(self, **event_args):
    self.trades_title.clear()
    self.log_section.clear()
    
    selected_user = self.accounts_dropdown.selected_value
    selected_user_data = next((account for account in self.accounts if account['user_name'] == selected_user), None)

    if selected_user_data:
      self.update_trades_title(selected_user_data)
      self.update_trades_grid(selected_user_data)
      self.update_logs(selected_user_data)
    else:
      self.clear_user_data()

  def update_trades_title(self, user_data):
    trade_title = RichText(content=f"### Trades for {user_data['user_name']}")
    trade_title.data = user_data
    self.trades_title.add_component(trade_title)

  def update_trades_grid(self, user_data):
    trades = json.loads(user_data['trades'])
    self.trades_grid_rows.items = trades

  def update_logs(self, user_data):
    logs = json.loads(user_data['logs'])
    logs_text = "Logs:\n" + "\n".join(logs)
    self.log_section.content = logs_text

  def clear_user_data(self):
    self.log_section.content = ""