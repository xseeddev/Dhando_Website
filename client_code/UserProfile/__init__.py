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
    self.user = None

    # Any code you write here will run before the form opens.
    user = anvil.users.get_user()
    self.user = user
    self.email_field.text = self.user["email"]
    profile_title = RichText(content=f"Welcome **{user['email']}**!")
    self.welcome_text.add_component(profile_title)

  def favourites_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.body.clear()
    favourites_section = favourites()
    self.body.add_component(favourites_section, full_width_row=True)

  def submit_details_click(self, **event_args):
    """This method is called when the button is clicked"""
    properties = {
        'full_name': self.full_name_field.text,
        'email': self.user["email"],
        'api_key': self.api_key_field.text,
        'api_secret': self.api_secret_field.text,
        'login_pin': self.login_pin_field.date,
    }
    
    # Validate inputs (you may want to add more comprehensive validation)
    if not properties['full_name'] or not properties['email'] or not properties['password']:
        anvil.alert("Please fill in all required fields.")
        return
    
    # Call the server function to register the user
    success = anvil.server.call('register_user', properties)
    
    if success:
        anvil.alert("User registered successfully!")
        # You might want to navigate to a different form or clear the inputs here
    else:
        anvil.alert("Registration failed. Please try again.")
    
