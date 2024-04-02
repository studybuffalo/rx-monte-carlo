"""Module to hold all the different scenarios for testing."""
from .combined_teams import combined_teams
from .current import current_state
from .utils import cycle_length, Stats

scenarios = [current_state, combined_teams]
cycle_length = cycle_length