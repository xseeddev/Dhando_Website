from ._anvil_designer import ToolsPageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Navbar import Navbar
from ..StockScreener import StockScreener
from ..F_and_O import F_and_O


class ToolsPage(ToolsPageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.homepage = get_open_form()

  def stock_screener_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.homepage.get_stock_screener()

  def F_and_O_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.homepage.get_F_and_O()
    
