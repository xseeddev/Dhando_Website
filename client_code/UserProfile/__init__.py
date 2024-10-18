from ._anvil_designer import UserProfileTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .favourites import favourites

class UserProfile(UserProfileTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    user = anvil.users.get_user()
    profile_title = RichText(content=f"Welcome **{user['email']}**!")
    self.welcome_text.add_component(profile_title)

  def favourites_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.body.clear()
    favourites_section = favourites()
    self.body.add_component(favourites_section, full_width_row=True)
    
