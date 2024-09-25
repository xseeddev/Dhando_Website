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

class F_and_O(F_and_OTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def trade_entry_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.strategy_preferences_section.clear()
    trade_entry = preferences().get_trade_entry()
    trade_entry.remove_from_parent()
    self.strategy_preferences_section.add_component(trade_entry, full_width_row=True)

  def trade_exit_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.strategy_preferences_section.clear()
    trade_exit = preferences().get_trade_exit()
    trade_exit.remove_from_parent()
    self.strategy_preferences_section.add_component(trade_exit, full_width_row=True)

  def auto_exit_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.strategy_preferences_section.clear()
    auto_exit = preferences().get_auto_exit()
    auto_exit.remove_from_parent()
    self.strategy_preferences_section.add_component(auto_exit, full_width_row=True)

  def strategy_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.strategy_1_section.visible = True

  def strategy_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.strategy_1_section.visible = False

  def strategy_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.strategy_1_section.visible = False
    

  
  
