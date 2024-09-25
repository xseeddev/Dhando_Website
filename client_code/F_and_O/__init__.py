from ._anvil_designer import F_and_OTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class F_and_O(F_and_OTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def trade_entry_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.display_trade_entry_section()

  def trade_exit_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.display_trade_exit_section()

  def auto_exit_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.display_auto_exit_section()

  
  
