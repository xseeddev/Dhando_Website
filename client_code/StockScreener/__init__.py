from ._anvil_designer import StockScreenerTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class StockScreener(StockScreenerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.predefined_scans_button_click()

  def predefined_scans_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.custom_scans_body.visible = False

  def custom_scan_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.predefined_scans_body.visible = False
    self.custom_scans_body.visible = True
