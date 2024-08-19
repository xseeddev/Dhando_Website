from ._anvil_designer import stockDetailsOverlayTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class stockDetailsOverlay(stockDetailsOverlayTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.visible = False  # Start as hidden
        self.width = "100%"  # Full width
        self.height = "100%"  # Full height
        self.position = "absolute"
        self.z_index = 1000  # Ensure it is above other components

    def close_button_click(self, **event_args):
        """Event handler for closing the overlay."""
        self.visible = False
        if self.parent:
            self.parent.remove_component(self)  # Remove from parent
        self.parent = None  # Clean up the reference
