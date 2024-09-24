'''
  TODO:
    - Privileges
    - Alerts
    - Image
'''

from ._anvil_designer import NavbarTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Navbar(NavbarTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.homepage = None

    # Any code you write here will run before the form opens.
    self.update_login_state()

  def update_login_state(self):
    self.homepage = get_open_form()
    user = anvil.users.get_user()
    if user:
      self.login.visible = False
      self.logout.visible = True
      self.logout_title.text = f"Logged in as {user['email']}"
      self.homepage.set_user(user)
      
    else:
      self.login.visible = True
      self.logout.visible = False

  def admin_login_button_click(self, **event_args):
    anvil.users.login_with_form()
    self.update_login_state()

  def user_login_button_click(self, **event_args):
    anvil.users.login_with_form()
    self.update_login_state()

  def logout_button_click(self, **event_args):
    anvil.users.logout()
    self.update_login_state()
    self.homepage.get_home_page_content()
    
  def tools_page_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = anvil.users.get_user()
    if user:
      self.homepage.get_tools()
    else:
      alert("Please Login.")  

  def title_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert("Not working.")
    