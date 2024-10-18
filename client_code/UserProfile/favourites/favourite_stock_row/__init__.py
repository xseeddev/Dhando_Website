from ._anvil_designer import favourite_stock_rowTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class favourite_stock_row(favourite_stock_rowTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def delete_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    user_email = anvil.users.get_user()["email"]
    anvil.server.call('delete_favorite', self.item["stock_name"], user_email)
    