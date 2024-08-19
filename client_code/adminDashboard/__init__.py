from ._anvil_designer import adminDashboardTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class adminDashboard(adminDashboardTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
        # Set initial visibility when the form opens
        self.strategyTabs.visible = True
        self.strategyFieldWindow.visible = True

        # Simulate the StrategyTab1 click and tradeEntry click when the form loads
        self.strategyTab1_click()  # Simulate click on StrategyTab1
        self.tradeEntry_click()    # Simulate click on tradeEntry

    def strategyTab1_click(self, **event_args):
      """This method is called when the StrategyTab1 button is clicked"""
      self.strategy1_card.visible = True
      self.strategy2_card.visible = False
      self.strategy3_card.visible = False
          
      self.tradeEntry_click()

    def tradeEntry_click(self, **event_args):
      """This method is called when the tradeEntry button is clicked"""
      self.tradeEntryCard.visible = True
      self.tradeExitCard.visible = False
      self.autoExitCard.visible = False
      

    def tradeExit_click(self, **event_args):
      """This method is called when the tradeExit button is clicked"""
      self.tradeEntryCard.visible = False
      self.tradeExitCard.visible = True
      self.autoExitCard.visible = False


    def autoExit_click(self, **event_args):
      """This method is called when the autoExit button is clicked"""
      self.tradeEntryCard.visible = False
      self.tradeExitCard.visible = False
      self.autoExitCard.visible = True

  
    def strategyTab2_click(self, **event_args):
      """This method is called when the StrategyTab2 button is clicked"""
      self.strategy1_card.visible = False
      self.strategy2_card.visible = True
      self.strategy3_card.visible = False
      

    def strategyTab3_click(self, **event_args):
      """This method is called when the StrategyTab3 button is clicked"""
      self.strategy1_card.visible = False
      self.strategy2_card.visible = False
      self.strategy3_card.visible = True
  

