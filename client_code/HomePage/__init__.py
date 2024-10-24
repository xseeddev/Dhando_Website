'''
  Todo:
    - FIX: reload issue
'''

from ._anvil_designer import HomePageTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Navbar import Navbar
from ..ToolsPage import ToolsPage
from ..StockScreener import StockScreener
from ..F_and_O import F_and_O
from ..UserProfile import UserProfile


class HomePage(HomePageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = None

    # Save default content of homepage (this will be restored on logout)
    self.default_content_title = self.content_title.text
    self.default_content_text = self.content_text.text

    # Add Navbar
    navbar_component = Navbar()
    self.home_navbar.add_component(navbar_component, full_width_row=True)

  def set_user(self, user):
    self.user = user
    
  def get_home_page_content(self):
    """This method will bring back the original homepage when logout is clicked."""
    
    # Clear the homepage body (removing any additional pages added)
    self.homepage_body.clear()
    open_form('HomePage')

  def get_tools(self):
    """Load the ToolsPage component into the homepage body"""
    self.content_title.visible = False
    self.content_text.visible = False
    tools_page = ToolsPage()
    self.homepage_body.clear()
    self.homepage_body.add_component(tools_page, full_width_row=True)

  def get_stock_screener(self):
    """Load the StockScreener component into the homepage body"""
    self.content_title.visible = False
    self.content_text.visible = False
    stock_screener_page = StockScreener()
    self.homepage_body.clear()
    self.homepage_body.add_component(stock_screener_page, full_width_row=True)

  def get_F_and_O(self):
    """Load the F_and_O component into the homepage body"""
    self.content_title.visible = False
    self.content_text.visible = False
    f_and_o = F_and_O()
    self.homepage_body.clear()
    self.homepage_body.add_component(f_and_o, full_width_row=True)

  def get_profile(self):
    self.content_title.visible = False
    self.content_text.visible = False
    profile = UserProfile()
    self.homepage_body.clear()
    self.homepage_body.add_component(profile, full_width_row=True)
