"""Utility classes and functions to help create different scenarios."""
import numpy as np


# The length (in weeks) to run each simulation for
cycle_length = 52

class Event:
    """Represents a type of event and its weekly rate of occurence.

        Attributes:
            name (str): the name of the event; used when outputing results.
            changes (flt): the number of schedule changes per occurence of 
                this event.
            losses (flt): the capacity lost (in number of shifts) per 
                occurrence of this event.
            rate_0 (flt): the weekly event rate between 0 to 2 weeks in
                the future.
            rate_2 (flt): the weekly event rate between 2 to 4 weeks in
                the future.
            rate_4 (flt): the weekly event rate between 4 to 12 weeks in
                the future.
            rate_12 (flt): the weekly event rate after 12 weeks in the future.
            
            cycle_max (flt): the maximum number of times this event can 
                occur within the simulation cycle.
    """
    def __init__(self, name, changes, losses, r0=0, r2=0, r4=0, r12=0, cycle_max=None):
        self.name = name
        self.changes = changes
        self.losses = losses
        self.rate_0 = r0
        self.rate_2 = r2
        self.rate_4 = r4
        self.rate_12 = r12
        self.cycle_max = cycle_max

    def __str__(self):
        """String representation for the class"""
        return f'Event: {self.name}'
    
class Shift:
    """Represents a group of shifts to be covered in a week.
    
        Attributes:
            name (str): a description of the shift group.
    """
    def __init__(self, name, number, priority=1):
        self.name = name
        self.number = number
        self.priority = priority

    def __str__(self):
        """String representation of a shift."""
        return f'Shift Group: {self.name}'
    
class ScenarioDetails:
    class _FTEDefinitions:
        """Class to define what an FTE is.
        
            HSAA Collective Agreement defines 1 FTE as 2022.75. The subsequent
            values are calculated from this assumption.
        """
        def __init__(self):
            self.fte = 1
            self.hours = 2022.75
            self.days = 261
            self.weeks = 52.2

    class _EmployeeTypeBreakdown:
            """Breaks down an attribute by different employee types."""
            def __init__(self, regular=0, bece=0, casual=0, total=0):
                self.regular = regular
                self.bece = bece
                self.casual = casual
                self.total = total

    class _FTEScenarios:
        """Defines the different types of FTE scenarios."""
        def __init__(self, data):
            try:
                self.official = ScenarioDetails._EmployeeTypeBreakdown(
                    regular=data['official']['regular'],
                    bece=data['official']['bece'],
                    casual=data['official']['casual'],
                    total=data['official']['total'],
                )
            except KeyError as e:
                raise TypeError(f'Missing argument: {e}')
            
            try:
                self.actual = ScenarioDetails._EmployeeTypeBreakdown(                    
                    regular=data['actual']['regular'],
                    bece=data['actual']['bece'],
                    casual=data['actual']['casual'],
                    total=data['actual']['total'],
                )
            except KeyError as e:
                raise TypeError(f'Missing argument: {e}')
        
    def __init__(self, name, fte, staff, events, shifts):
        self.name = name
        self.fte_definitions = self._FTEDefinitions()
        self.fte = self._FTEScenarios(fte)
        self.staff = self._EmployeeTypeBreakdown(
            staff['regular'],
            staff['bece'],
            staff['casual'],
            staff['total'],
        )
        self.events = events
        self.shifts = sorted(shifts, key=lambda x: (x.priority, x.name))
        
    def __str__(self):
        """String representation of the class for printing."""
        return f'Scenario Name: {self.name}'

class Stats:
    """Calculates and outputs statistical calculations for results."""
    def __init__(self, values):
        self.values = np.array(values)
        self.mean = np.mean(self.values)
        ci_lower, ci_upper = np.percentile(self.values, [2.5, 97.5])
        self.ci_lower = ci_lower
        self.ci_upper = ci_upper

    def __str__(self):
        """String representation of Stats."""
        return f'Mean = {np.round(self.mean, 2)} (95% CI {np.round(self.ci_lower, 2)}-{np.round(self.ci_upper, 2)})'