from ._anvil_designer import HomePageTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from



class HomePage(HomePageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def admin_login_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.login_with_form()
    user = anvil.users.get_user()
    # Places a automated privilege
    user["privilege"] = "admin"
    if user["privilege"] != "admin":
      alert("You are not an admin.")
    else:
      pass
  
  def user_login_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.login_with_form()
    user = anvil.users.get_user()
    # Places a automated privilege
    user["privilege"] = "user"
    if user["privilege"] == "admin":
      alert("You are not logging in as Admin. \n Some privileges won't be present.")
    pass
    
    
