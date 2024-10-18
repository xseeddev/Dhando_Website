from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.users
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..StockData import StockData


class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def show_click(self, **event_args):
    """This method is called when the button is clicked"""
    stock_name = self.item["stock_name"]
    stock_data_form = StockData(stock_name=stock_name)
    alert(stock_data_form, large=True)

