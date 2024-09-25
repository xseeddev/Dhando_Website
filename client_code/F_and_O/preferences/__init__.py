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
    return self.trade_entry_preferences
    
  def get_trade_exit(self):
    return self.trade_exit_preferences
  
  def get_auto_exit(self):
    return self.auto_exit_preferences
    