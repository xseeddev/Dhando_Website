from ._anvil_designer import StockScreenerTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .StockData import StockData


class StockScreener(StockScreenerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Initialize the list for storing selected scans
    self.chosen_scans = []
    self.field_marketcap.text = '10'
    self.field_yoy_sales.text = '20'
    self.field_yoy_profit.text = '30'
    self.field_net_profit.text = '40'
    self.field_pe_ratio.text = '50'
    self.field_roce.text = '60'

    self.stock_name = None
    
    # Any code you write here will run before the form opens.
    self.predefined_scans_button_click()
    self.update_recommended_stock()

  def update_recommended_stock(self):
    # fields (rich text): stock_name, stock_symbol, stock_cmp, buy_price, sell_price
    recommend_stock = anvil.server.call('get_recommended_stock')
    self.stock_name = recommend_stock['stock_name']
    
    stock_title = RichText(content=f"**{recommend_stock['stock_name']}**: **{recommend_stock['stock_symbol']}**")
    stock_title.data = recommend_stock
    self.field_stock_name.add_component(stock_title)
    
    stock_cmp = RichText(content=f"**Current Market Price**: {recommend_stock['stock_cmp']}")
    stock_cmp.data = recommend_stock
    self.field_stock_cmp.add_component(stock_cmp)
    
    buy_price = RichText(content=f"**Recommended Buy Price**: {recommend_stock['buy_price']}")
    buy_price.data = recommend_stock
    self.field_buy_price.add_component(buy_price)
    
    sell_price = RichText(content=f"**Recommended Sell Price**: {recommend_stock['sell_price']}")
    sell_price.data = recommend_stock
    self.field_sell_price.add_component(sell_price)

  def predefined_scans_button_click(self, **event_args):
    """This method is called when the predefined scans button is clicked."""
    # Hide custom scan body and show predefined scans
    self.custom_scans_body.visible = False
    self.predefined_scans_body.visible = True

  def custom_scan_button_click(self, **event_args):
    """This method is called when the custom scans button is clicked."""
    # Hide predefined scan body and show custom scans
    self.predefined_scans_body.visible = False
    self.custom_scans_body.visible = True

  def _toggle_scan(self, scan_name, checkbox_checked):
    """
    Adds or removes a scan from the chosen_scans list based on checkbox state.
    :param scan_name: Name of the scan to add/remove
    :param checkbox_checked: Boolean representing the checkbox state
    """
    if checkbox_checked:
      # Add the scan only if it's not already in the list
      if scan_name not in self.chosen_scans:
        self.chosen_scans.append(scan_name)
    else:
      # Remove the scan if it's unchecked
      if scan_name in self.chosen_scans:
        self.chosen_scans.remove(scan_name)

  def pitrosk_change(self, **event_args):
    """This method is called when the Pitroski checkbox is checked or unchecked."""
    self._toggle_scan("Pitroski", self.pitrosk.checked)

  def darvas_change(self, **event_args):
    """This method is called when the Darvas checkbox is checked or unchecked."""
    self._toggle_scan("Darvas", self.darvas.checked)

  def stevenson_change(self, **event_args):
    """This method is called when the Stevenson checkbox is checked or unchecked."""
    self._toggle_scan("Stevenson", self.stevenson.checked)
    
  def predefined_display_button_click(self, **event_args):
    """This method is called when the display button is clicked."""
    # Alert the user with the list of selected scans
    if self.chosen_scans:
      # Join the list into a string and display it in an alert
      alert(f"Selected Scans: {', '.join(self.chosen_scans)}")
      # call the server to get all the stocks
      stocks = anvil.server.call('get_chosen_stocks', self.chosen_scans)
      
      # display the stocks in the grid predefined_results with columns: stock_name, Recommended buy, Recommended sell
      self.predefined_display_stocks_rows.items = stocks
    else:
      alert("No scans selected.")

  def custom_display_button_click(self, **event_args):
    """This method is called when the Submit button is clicked."""
    
    # Default values for each threshold
    default_values = {
        'marketcap': 10,
        'yoy_sales': 20,
        'yoy_profit': 30,
        'net_profit': 40,
        'pe_ratio': 50,
        'roce': 60
    }

    # Function to safely retrieve threshold values with defaults
    def get_threshold_value(field, default):
        try:
            # Try to convert the text to a float
            return float(field.text) if field.text else default
        except ValueError:
            # Return the default if conversion fails
            return default

    # Collecting the values using the helper function
    thresholds = {
        'marketcap': get_threshold_value(self.field_marketcap, default_values['marketcap']),
        'yoy_sales': get_threshold_value(self.field_yoy_sales, default_values['yoy_sales']),
        'yoy_profit': get_threshold_value(self.field_yoy_profit, default_values['yoy_profit']),
        'net_profit': get_threshold_value(self.field_net_profit, default_values['net_profit']),
        'pe_ratio': get_threshold_value(self.field_pe_ratio, default_values['pe_ratio']),
        'roce': get_threshold_value(self.field_roce, default_values['roce']),
    }
    
    # Prepare a detailed response with all threshold values for alert
    result = (
        f"Threshold Values:\n"
        f"Market Cap: {thresholds['marketcap']}\n"
        f"YOY Sales: {thresholds['yoy_sales']}\n"
        f"YOY Profit: {thresholds['yoy_profit']}\n"
        f"Net Profit: {thresholds['net_profit']}\n"
        f"P/E Ratio: {thresholds['pe_ratio']}\n"
        f"ROCE: {thresholds['roce']}"
    )
    alert(result)

    results = anvil.server.call('get_custom_stocks', thresholds)
    results_with_buttons = []
    for result in results:
      show_button = Button(text="Show", tag=result['stock_name'])
      result['show_button'] = show_button
      results_with_buttons.append(result)
    
    self.custom_display_stocks_rows.items = results_with_buttons

  def show_stock_click(self, sender=None, stock_name=None, **event_args):
    """This method is called when the Show button is clicked in a row"""
    print(sender, stock_name)
    if not sender.tag and not stock_name:
      stock_name = self.stock_name
    stock_details = StockData(stock_name)
    alert(stock_details, large=True)


