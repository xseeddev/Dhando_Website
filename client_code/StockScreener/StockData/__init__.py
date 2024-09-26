'''
  Todo:
    - Put a "mark favorites" button
'''

from ._anvil_designer import StockDataTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class StockData(StockDataTemplate):
  def __init__(self, stock_name = None, **properties):
    '''
    Components: rich texts: page_title, field_stock_name, field_stock_cmp, field_stock_symbol
    grid: stock_details_table
    '''
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    stock_details = anvil.server.call('get_stock_details', stock_name)

    # Create and add a RichText component for stock name and symbol
    stock_name = RichText(content=f"{stock_details['stock_name']}")
    self.field_stock_name.add_component(stock_name)

    stock_symbol = RichText(content=f"{stock_details['stock_symbol']}")
    self.field_stock_symbol.add_component(stock_symbol)

    stock_cmp = RichText(content=f"{stock_details['stock_cmp']}")
    self.field_stock_cmp.add_component(stock_cmp)

    title = RichText(content=f"## {stock_details['stock_name']}")
    self.page_title.add_component(title)

    self.stock_details_table_row.items = stock_details.get('details')
    
    

    
    