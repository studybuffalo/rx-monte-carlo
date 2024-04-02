"""Module to hold all the different scenarios for testing."""
from .combined_teams import scenario as scenario_combined
from .current import scenario as scenario_current
from .no_im import scenario as scenario_no_im
from .status_quo import scenario as scenario_status_quo
from .utils import cycle_length, Stats

scenarios = [
    scenario_current, 
    scenario_status_quo,
    scenario_combined, 
    scenario_no_im,
]
cycle_length = cycle_length