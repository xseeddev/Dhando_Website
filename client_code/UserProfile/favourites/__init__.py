from ._anvil_designer import favouritesTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json


class favourites(favouritesTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.populate_favourites()

  def populate_favourites(self):
    # Call the server function to get favourites
    user_email = anvil.users.get_user()["email"]
    favourites_json = anvil.server.call('get_favourites', user_email)
    
    # Parse the JSON string into a Python object
    favourites = json.loads(favourites_json)
    
    # Prepare the data for the grid
    grid_items = []
    for stock in favourites:
        grid_item = {
            'stock_name': stock['stock_name'],
            'stock_cmp': f"${stock['stock_cmp']:.2f}",
            'stock_percentage_change': f"{stock['stock_percentage_change']:.1f}%",
            'stock_price_difference': f"${stock['stock_price_difference']:.2f}"
        }
        grid_items.append(grid_item)
    
    # Update the grid with the prepared items
    self.favourite_stock_grid_rows.items = grid_items