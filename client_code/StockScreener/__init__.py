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
    self.stock_name = None
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

  def update_recommended_stock(self):
    recommend_stock = anvil.server.call('get_recommended_stock')
    self.stock_name = recommend_stock['stock_name']
    
    self.update_stock_field('stock_name', f"**{recommend_stock['stock_name']}**: **{recommend_stock['stock_symbol']}**", recommend_stock)
    self.update_stock_field('stock_cmp', f"**Current Market Price**: {recommend_stock['stock_cmp']}", recommend_stock)
    self.update_stock_field('buy_price', f"**Recommended Buy Price**: {recommend_stock['buy_price']}", recommend_stock)
    self.update_stock_field('sell_price', f"**Recommended Sell Price**: {recommend_stock['sell_price']}", recommend_stock)

  def update_stock_field(self, field_name, content, data):
    rich_text = RichText(content=content)
    rich_text.data = data
    getattr(self, f'field_{field_name}').add_component(rich_text)

  def predefined_scans_button_click(self, **event_args):
    self.toggle_scan_visibility(True)

  def custom_scan_button_click(self, **event_args):
    self.toggle_scan_visibility(False)

  def toggle_scan_visibility(self, show_predefined):
    self.custom_scans_body.visible = not show_predefined
    self.predefined_scans_body.visible = show_predefined

  def _toggle_scan(self, scan_name, checkbox_checked):
    if checkbox_checked and scan_name not in self.chosen_scans:
      self.chosen_scans.append(scan_name)
    elif not checkbox_checked and scan_name in self.chosen_scans:
      self.chosen_scans.remove(scan_name)

  def pitrosk_change(self, **event_args):
    self._toggle_scan("Pitroski", self.pitrosk.checked)

  def darvas_change(self, **event_args):
    self._toggle_scan("Darvas", self.darvas.checked)

  def stevenson_change(self, **event_args):
    self._toggle_scan("Stevenson", self.stevenson.checked)
    
  def predefined_display_button_click(self, **event_args):
    if not self.chosen_scans:
      alert("No scans selected.")
      return
    
    alert(f"Selected Scans: {', '.join(self.chosen_scans)}")
    stocks = anvil.server.call('get_chosen_stocks', self.chosen_scans)
    self.predefined_display_stocks_rows.items = stocks

  def custom_display_button_click(self, **event_args):
    thresholds = self.get_thresholds()
    alert(self.format_thresholds(thresholds))
    results = anvil.server.call('get_custom_stocks', thresholds)
    self.custom_display_stocks_rows.items = self.add_show_buttons(results)

  def get_thresholds(self):
    default_values = {
      'marketcap': 10, 'yoy_sales': 20, 'yoy_profit': 30,
      'net_profit': 40, 'pe_ratio': 50, 'roce': 60
    }
    return {field: self.get_threshold_value(getattr(self, f'field_{field}'), default)
            for field, default in default_values.items()}

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

  @staticmethod
  def add_show_buttons(results):
    return [{**result, 'show_button': Button(text="Show", tag=result['stock_name'])}
            for result in results]

  def show_stock_click(self, stock_name=None, **event_args):
    stock_details = StockData(self.stock_name)
    alert(stock_details, large=True)