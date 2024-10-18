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
    def __init__(self, stock_name=None, **properties):
        """
        This form displays stock details for a given stock name.

        Components:
            - page_title (RichText): Displays the stock name as a heading.
            - field_stock_name (RichText): Displays the stock name in bold.
            - field_stock_symbol (RichText): Displays the stock symbol.
            - field_stock_cmp (RichText): Displays the company name (assumed to be in 'stock_cmp' key).
            - stock_details_table (Grid): Displays additional details from the 'details' list.
        """

        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        column = [c for c in self.stock_details_table.columns if c['title'] == 'Column 3']
        self.stock_details_table.columns.remove(column[0])
      
        self.stock_name = stock_name.strip() if stock_name else None  # Handle empty stock_name

        if self.stock_name:
            # Fetch stock details from server
            stock_details = anvil.server.call('get_stock_details', self.stock_name)

            # Update content with RichText components for better formatting
            self.update_content(stock_details)
        else:
            # Handle case where no stock name is provided
            print("No stock name provided. Please specify a stock name to display details.")

    def update_content(self, stock_details):
        # Create RichText components with bold formatting
        stock_name_text = f"**{stock_details['stock_name']}**"
        stock_name_component = RichText(content=stock_name_text, align="center")
        
        stock_symbol_component = RichText(content=stock_details['stock_symbol'], align="center")
        stock_cmp_component = RichText(content=stock_details['stock_cmp'], align="center")

# ... rest of your code

        # Update title and add components to designated fields
        self.page_title.add_component(RichText(content=f"## {stock_details['stock_name']}", align="center"))
        self.field_stock_name.add_component(stock_name_component)
        self.field_stock_symbol.add_component(stock_symbol_component)
        self.field_stock_cmp.add_component(stock_cmp_component)

        # Set table items if details are available
        self.stock_details_table_row.items = stock_details.get('details', [])

    def favorite_button_click(self, **event_args):
      """This method is called when the button is clicked"""
      user_email = anvil.users.get_user()["email"]
      anvil.server.call('add_favorite', self.stock_name, user_email)
