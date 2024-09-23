import anvil
from anvil import *
import anvil.server
from ..Navbar import Navbar
from ..ToolsPage import ToolsPage
from ..StockScreener import StockScreener
from ..F_and_O import FandO

class HomePage(HomePageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.navbar = Navbar()
    self.content_panel.add_component(self.navbar)
    self.show_home_content()
    
    # Set up event handlers
    self.navbar.login_event.add_handler(self.show_tools_page)
    self.navbar.logout_event.add_handler(self.show_home_content)

  def show_home_content(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(self.navbar)
    self.body_title.text = "Welcome to Finance Tools"
    self.body_text.text = "Please log in to access our tools."
    self.body_section.visible = True

  def show_tools_page(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(self.navbar)
    tools_page = ToolsPage()
    tools_page.stock_screener_click.add_handler(self.show_stock_screener)
    tools_page.f_and_o_click.add_handler(self.show_f_and_o)
    self.content_panel.add_component(tools_page)

  def show_stock_screener(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(self.navbar)
    self.content_panel.add_component(StockScreener())

  def show_f_and_o(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(self.navbar)
    self.content_panel.add_component(FandO())