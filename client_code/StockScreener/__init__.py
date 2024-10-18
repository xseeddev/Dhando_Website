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
    self.init_components(**properties)
    self.chosen_scans = []
    self.stock_name = ""
    self.setup_initial_values()
    self.predefined_scans_button_click()
    self.update_recommended_stock()

  def setup_initial_values(self):
    default_values = {
      'marketcap': '10', 'yoy_sales': '20', 'yoy_profit': '30',
      'net_profit': '40', 'pe_ratio': '50', 'roce': '60'
    }
    for field, value in default_values.items():
      getattr(self, f'field_{field}').text = value


  
  # <---------------------------- Recommended Stock ---------------------------------------->
  def update_recommended_stock(self):
    recommended_stock = anvil.server.call('get_recommended_stock')
    if recommended_stock is None:
        # Handle the case when no stock is recommended for today
        self.clear_stock_fields()
        return

    self.stock_name = recommended_stock['stock_name'].strip()
    
    self.update_stock_field('stock_name', f"{recommended_stock['stock_name']} : **{recommended_stock['stock_symbol']}**", recommended_stock)
    self.update_stock_field('stock_cmp', f"**Current Market Price**: {recommended_stock['stock_cmp']}", recommended_stock)
    self.update_stock_field('buy_price', f"**Recommended Buy Price**: {recommended_stock['buy_price']}", recommended_stock)
    self.update_stock_field('sell_price', f"**Recommended Sell Price**: {recommended_stock['sell_price']}", recommended_stock)

  def clear_stock_fields(self):
      for field in ['stock_name', 'stock_cmp', 'buy_price', 'sell_price']:
          self.update_stock_field(field, "No recommendation for today", {})
  
  def update_stock_field(self, field_name, content, data):
      field = getattr(self, f'field_{field_name}')
      field.content = content
      field.data = data

  def show_recommended_stock_click(self, **event_args):
    print(self.stock_name)
    stock_details = StockData(stock_name=self.stock_name)
    alert(stock_details, large=True)

  # <----------------------------- Predefined Scans ---------------------------------------->
  def toggle_scan_visibility(self, show_predefined):
    self.custom_scans_body.visible = not show_predefined
    self.predefined_scans_body.visible = show_predefined

  
  def predefined_scans_button_click(self, **event_args):
    self.toggle_scan_visibility(True)

  def _toggle_scan(self, scan_name, checkbox_checked):
    if checkbox_checked and scan_name not in self.chosen_scans:
      self.chosen_scans.append(scan_name)
    elif not checkbox_checked and scan_name in self.chosen_scans:
      self.chosen_scans.remove(scan_name)

  def piotroski_change(self, **event_args):
    self._toggle_scan("Piotroski", self.piotroski.checked)

  def darvas_change(self, **event_args):
    self._toggle_scan("Darvas", self.darvas.checked)

  def stevenson_change(self, **event_args):
    self._toggle_scan("Stevenson", self.stevenson.checked)
    
  def predefined_display_button_click(self, **event_args):
    alert(f"Selected Scans: {', '.join(self.chosen_scans)}")
    results = anvil.server.call('get_scanned_stocks', self.chosen_scans)
    print("Recieved stocks:", results)
    self.predefined_search_results_panel.items = results

    
    

  
  # <---------------------------- Custom Scans ---------------------------------------->
  def get_thresholds(self):
    default_values = {
      'marketcap': 10, 'yoy_sales': 20, 'yoy_profit': 30,
      'net_profit': 40, 'pe_ratio': 50, 'roce': 60
    }
    return {field: self.get_threshold_value(getattr(self, f'field_{field}'), default)
            for field, default in default_values.items()}
    
  def custom_scan_button_click(self, **event_args):
    self.toggle_scan_visibility(False)

  @staticmethod
  def get_threshold_value(field, default):
    try:
      return float(field.text) if field.text else default
    except ValueError:
      return default

  @staticmethod
  def format_thresholds(thresholds):
    return "\n".join(f"{key.replace('_', ' ').title()}: {value}" 
                     for key, value in thresholds.items())

  def custom_display_button_click(self, **event_args):
    thresholds = self.get_thresholds()
    alert(self.format_thresholds(thresholds))
    results = anvil.server.call('get_custom_stocks', thresholds)
    print("Recieved stocks:", results)
    self.custom_search_results_panel.items = results



  
  @staticmethod
  def add_show_buttons(results):
    return [{**result, 'show_button': Button(text="Show", tag=result['stock_name'])}
            for result in results]

  