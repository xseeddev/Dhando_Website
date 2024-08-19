from ._anvil_designer import stockScreenerTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .stockDetailsOverlay import stockDetailsOverlay

class stockScreener(stockScreenerTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.overlay = None
        self.overlay_container = None  # Add a container for the overlay

    def showStockDetailOverlay(self):
        """Display the stock details overlay."""
        if self.overlay is None:
            self.overlay = stockDetailsOverlay()
            self.overlay_container = ColumnPanel()  # Create a container to hold the overlay
            self.overlay_container.add_component(self.overlay)
            self.add_component(self.overlay_container)
            self.overlay_container.width = "100%"  # Full width
            self.overlay_container.height = "100%"  # Full height
            self.overlay_container.position = "absolute"
            self.overlay_container.z_index = 1000  # Ensure it is above other components

        self.overlay.visible = True

    def hideStockDetailOverlay(self):
        """Hide the stock details overlay."""
        if self.overlay:
            self.overlay.visible = False
            # Optionally, remove the overlay container from the parent
            self.remove_component(self.overlay_container)
            self.overlay = None
            self.overlay_container = None

    def logoutButton_click(self, **event_args):
        """Event handler for the logout button."""
        self.showStockDetailOverlay()
