"""Defines a scenario where the two IM teams are removed.

    All details are based on calculations from the
    2023-08-07 2024-03-24 schedule unless noted otherwise.
"""
from .utils import ScenarioDetails, Event, Shift, cycle_length

# FTE Scenarios
# ----------------------------------------------------------------------------
# - This provides details on the official and actual FTE in the scenario.
# - These numbers may differ because part time staff may pick up more than 
#   their stated FTE/availablility
fte = {
    'official': {
        'regular': 35.7, # Based on position FTE + 2 FTE
        'bece': 2.4, # Based on minimum FTE requirements
        'casual': 1.4, # Based on stated availability
    },
    'actual': {
        'regular': 36.5748, # + 2 FTE
        'bece': 3.2551,
        'casual': 1.5102,

    },
}
fte['official']['total'] = (
    fte['official']['regular'] + fte['official']['bece'] + fte['official']['casual']
)
fte['actual']['total'] = (
    fte['actual']['regular'] + fte['actual']['bece'] + fte['actual']['casual']
)

# This is the number of possible shifts in the cycle
number_of_shifts = fte['actual']['total'] * cycle_length * 5
                    
# Staff Scenario
# ----------------------------------------------------------------------------
# - This provides the number of each type of staff in the scenario.
staff = {
    'regular': 37,
    'bece': 4,
    'casual': 4,
    'total': 37 + 4 + 4,
}

# Standard Rates
# ----------------------------------------------------------------------------
# - These variables are standard shift change rate and loss rate due to the
#   occurrence of an event.
# - Theses values may be overriden for any individual event as needed.
standard_change_rate = 1.5
standard_loss_rate = 1

# Vacation Events
# ----------------------------------------------------------------------------
# - This event tracks vacation occurrences
# - Note that in general, at least 75% of vacation should occur more than 12 
#   weeks out. This is because the HSAA Collective Agreement requires that 75%
#   of vacation is booked during the Vacation by Seniority process.

# This is the calculated vacation accumulation rate for all staff. On average,
# staff will use all the vacation accumulated.
calculated_vacation_rate = 0.0681

# Assumptions for this scenario:
# - 80% of vacation is booked in advance
# - The remaining 20% is used at least 4 weeks out
# - All requests between 0 to 4 weeks would be denied unless they created no
#   shift changes. Rate here is set for 0 as a "worst case" scenario.
vacation = Event(
    name='Vacation Days',
    changes=standard_change_rate,
    losses=standard_loss_rate,
    r4=calculated_vacation_rate * 0.2,
    r12=calculated_vacation_rate * 0.8,
)


# Bereavement Events
# ----------------------------------------------------------------------------
# - This event tracks bereavement occurrences
# - In general, can assume that all events occur on short notice (0-2 weeks)
# - Do not need to calculate a maximum, as it is unlikely such an event could
#   ever occur.
calculated_bereavement_rate = 0.0058

bereavement = Event(
    name='Bereavement Leave Days',
    changes=standard_change_rate,
    losses=standard_loss_rate,
    r0=calculated_bereavement_rate,
)

# Sick Day Events
# ----------------------------------------------------------------------------
# - This event tracks sick day occurrences
# - Can assume all sick days occur on short notice.
# - Do not need a maximum as it is highly unlikely all sick day banks would be
#   used up.
calculated_sick_rate = 0.0366

sick = Event(
    name='Sick Days',
    changes=standard_change_rate,
    losses=standard_loss_rate,
    r0=calculated_sick_rate,
)

# Medical Leave Events
# ----------------------------------------------------------------------------
# - This event tracks medical leave occurrences.
# - Due to the length of these events, some will occur on short notice and 
#   continue into longer periods of time. Some people also will have scheduled
#   events (e.g. elective surgery).
# - Do not need a maximum as staff can usually take up to several years for 
#   medical leaves.
calculated_medical_rate = 0.0035

# Current rates are best guesses
medical = Event(
    name='Medical Leaves',
    changes=standard_change_rate,
    losses=standard_loss_rate,
    r0=calculated_medical_rate * 0.4,
    r2=calculated_medical_rate * 0.2,
    r4=calculated_medical_rate * 0.1,
    r12=calculated_medical_rate * 0.3,
)

# Personal Leave Day Events
# ----------------------------------------------------------------------------
# - This event tracks personal leave day occurrences.
# - Maximum would generally be 3 * number of regular employees. The true 
#   number is slightly lower as new staff will not have any PL days loaded in 
#   their bank, but this is a good worst-case scenario to use.
# - If estimating the PL rate, can use number of PL days for all staff
#   divided by the number of shifts for the simulation cycle.
max_pl = (staff['regular'] * 3)
estimated_pl_rate = max_pl / number_of_shifts

# Current rates are estimates; worst case assumption that all are used with 
# < 4 weeks notice
personal_leave = Event(
    name='Personal Leave Days',
    changes=standard_change_rate,
    losses=standard_loss_rate,
    r0=estimated_pl_rate * 0.5,
    r2=estimated_pl_rate * 0.5,
    cycle_max=max_pl,
)

# Project Events
# ----------------------------------------------------------------------------
# - This event tracks any type of project day occurrences.
calculated_project_rate = 0.0163

# Current rates are best guesses
project = Event(
    name='Project Days',
    changes=standard_change_rate,
    losses=standard_loss_rate,
    r0=calculated_project_rate * 0.1,
    r2=calculated_project_rate * 0.2,
    r4=calculated_project_rate * 0.3,
    r12=calculated_project_rate * 0.5,
)

# Education Days
# ----------------------------------------------------------------------------
# - This event tracks any type of education day.
# - A maximum of 2 per staff member is likely reasonable, as that is the 
#   standard number of Professional Development days given to each staff member
calculated_education_rate = 0.0147
education_max = 2 * (staff['regular'] + staff['bece'] + staff['casual'])

# Current rates are best guesses; assume we'll not approve anything with less
# than 4 weeks notice in current state
education = Event(
    name='Education Days',
    changes=standard_change_rate,
    losses=standard_loss_rate,
    r4=calculated_education_rate * 0.3,
    r12=calculated_education_rate * 0.7,
    cycle_max=education_max,
)

# New Hire Orientation Events
# ----------------------------------------------------------------------------
# - This event tracks New Hire Orientation Event occurrences. These are the
#   schedule changes to other staff members to support the new hire's 
#   orientation.

# Assumptions for the rate of shift changes:
# - Each new staff member requires the following orientation days:
#   - 15 days with a trainer at the start of orientation
#   - 23 indirect days
#   - 5 direct days with trainer for PN training
#   - 20 days for clinical orientation
#   - 2 days for float training
# - Can calculate the total orientation changes required by using the
#   above assumptions divided by number of shifts in the cycle.
# - We have a slighty lower rate of shift changes because we try to find
#   swaps that minimize changes overall.
orientation_shifts_per_new_hire = 15 + 13 + 5 + 10 + 1
new_hires = 6
new_hire_orientation_shifts = orientation_shifts_per_new_hire * new_hires
new_hire_rate = new_hire_orientation_shifts / number_of_shifts

# Current rates are estimates
new_hire = Event(
    name='New Hire Changes',
    changes=1,
    losses=standard_loss_rate,
    r2=new_hire_rate * 0.1,
    r4=new_hire_rate * 0.6,
    r12=new_hire_rate * 0.3,
)

# Departure Events
# ----------------------------------------------------------------------------
# - This event tracks when an employee leaves. This only is the time between 
#   them leaving and until a new person is hired to take their position (at 
#   which point, they are tracked as a New Hire Orientation event).

# Assumptions for the rate of shift changes:
# - We will get ~4 weeks notice when someone is departing
# - It will take ~8 weeks from the point of notice to a new staff member starts
# - Therefore, approximately 20 shifts are lost per each departure
shifts_lost_per_departure = 20
number_of_departures = 4
departure_shifts = shifts_lost_per_departure * number_of_departures
departure_rate = departure_shifts / number_of_shifts

# Current rates are estimates
departures = Event(
    name='Depatures',
    changes=standard_change_rate,
    losses=standard_loss_rate,
    r4=new_hire_rate,
)

# Internal Unit Swap Events
# ----------------------------------------------------------------------------
# - This event tracks Internal Unit swaps event occurrences. These are the 
#   schedule changes to other staff members to support a pharmacist moving to
#   a new unit.

# Assumptions for the rate of shift changes:
# - Each swap requires adjustments to schedules to build an orientation
#   schedules for that staff member
# - Assume that staff will need 15 days of orientation and 8 of those
#   changes will require schedule changes.
# - Can calculate the total swap changes required by using the
#   above assumptions * number of swaps, divided by number of shifts 
#   in the cycle.
# - We have a slighty lower rate of shift changes because we try to find
#   swaps that minimize changes overall.

orientation_shifts_per_internal_swap = 8
internal_swaps = 6
internal_swap_orientation_shifts = orientation_shifts_per_internal_swap * internal_swaps
internal_swap_rate = internal_swap_orientation_shifts / number_of_shifts

# Current rates are estimates
internal_swap = Event(
    name='Internal Swap Changes',
    changes=1,
    losses=standard_loss_rate,
    r2=internal_swap_rate * 0.1,
    r4=internal_swap_rate * 0.9,
)


# Returning Work Reorientation
# ----------------------------------------------------------------------------
# - This event tracks employees returning from an extended leave and require
#   reorientation

# Assumptions for the rate of shift changes:
# - The rate of changes will mimic that for a new hire orientation, but with
#   reduced numbers of days:
#   - ~5 days direct in dispensary
#   - ~10 days indirect in dispensary
#   - ~10 days for clinical
# - Assume ~50% of those shifts result in shift changes

orientation_shifts_per_reorientation = 13
return_to_works = 2
reorientation_shifts = orientation_shifts_per_reorientation * return_to_works
reorientation_rate = reorientation_shifts / number_of_shifts

# Current rates are estimates
reorientation = Event(
    name='Returning to Work Reorientation',
    changes=1,
    losses=standard_loss_rate,
    r4=reorientation_rate,
)

# Learner Rotation Change Events
# ----------------------------------------------------------------------------
# - This event tracks learning rotation changes. These are schedule changes to
#   accommodate an unexpected change to a learner's rotation.

# Assumptions for the rate of shift changes:
# - Each swap requires adjustments to schedules to have a consistent preceptor
#   in the area.
# - Rotations last on average 20-40 working days
# - Assume from that, ~15 days will need to be changed to accommodate a change
# - Can calculate the total changes required by using the above 
#   assumptions * number of swaps, divided by number of shifts in the cycle
# - No shift capacity lost due to this, as the learning is not part of our
#   normal shift capacity.

changes_per_learner_swap = 15
learner_swaps = 4
learner_changes = changes_per_learner_swap * learner_swaps
learner_swap_changes_rate = learner_changes / number_of_shifts

# Current rates are estimates
learner_swap = Event(
    name='Learner Rotation Swap Changes',
    changes=standard_change_rate,
    losses=0,
    r4=learner_swap_changes_rate * 0.5,
    r12=learner_swap_changes_rate * 0.5,
)

# Shift Declarations
# ----------------------------------------------------------------------------
# - Shift declarations outline all the shifts in the proposed scenario.
# - Shifts are assigned a numerical priority, where the lower the integer, the
#   higher priority the shift is to cover. This is used to model how well the
#   scenario handles different priorities for areas to cover.

# The following declarations are based on estimates of current state
# Dispensary Shift Assumptions:
# - 2 AM shifts every day of the week
# - 3 PM shifts every weekday
# - 2 PM shifts every weekend
# - 1 Night shift every day of the week
shift_dispensary = Shift(
    name='Dispensary',
    number=(2 * 7) + (3 * 5) + (2 * 2) + (1 * 7),
    priority=1,
)

# HPT Shift Assumptions:
# - 1 shift every weekday
shift_hpt = Shift(
    name='HPT',
    number=1 * 5,
    priority=1,
)

# ED Shift Assumptions:
# - Shifts will be normalized to a 7.75 workday to streamline calculations
# - 2 x 9.4 hour shifts each weekday
# - 1 x 11.7 hour shift each weekend
shift_ed = Shift(
    name='ED',
    number=((2 * 5 * 9.4) / 7.75) + ((1 * 2 * 11.7) / 7.75),
    priority=2,
)

# ICU Shift Assumptions:
# - Shifts will be normalized to a 7.75 workday to streamline calculations
# - 2 x 9.4 hour shifts each weekday
# - 1 x 9.4 hour shift each weekend
shift_icu = Shift(
    name='ICU',
    number=((2 * 5 * 9.4) / 7.75) + ((1 * 2 * 9.4) / 7.75),
    priority=2,
)

# Ambulatory Shift Assumptions:
# - Using actual FTE provided, as we have routinely upstaffed at their 
#   the ambulatory pharmacists' request. Actual FTE would be 4.0 or 20 
#   shifts per week.
shift_ambulatory = Shift(
    name='Ambulatory',
    number=20.2424,
    priority=2,
)

# ID & ASP Assumptions
# - 5 shifts per week for ID inpatient
# - 5 shifts per week for ID outpatient
# - 5 shifts per week for ASP
shift_id_asp = Shift(
    name='ID & ASP',
    number=5 * 3,
    priority=2,
)

# Acute Care Shift Assumptions
# - 5 shifts per week on Unit 21 (1 shift each weekday)
# - 5 shifts per week on Unit 22 (1 shifts each weekday)
# - 5 shifts per week on Unit 23 (1 shift each weekday)
# - 5 shifts per week on Unit 24 (1 shift each weekday)
# - 5 shifts per week on Unit 26 (1 shift each weekday)
# - 5 shifts per week on Unit 31 (1 shift each weekday)
# - 5 shifts per week on Unit 32 (1 shift each weekday)
# - 5 shifts per week on Unit 33 (1 shifts each weekday)
# - 5 shifts per week on Unit 34/36 (1 shift each weekday)
shift_acute_care = Shift(
    name='Acute Care',
    number=5*9,
    priority=3,
)

# Scenario Declaration
# ----------------------------------------------------------------------------
# - Create your scenario by providing the require class initialization 
#   arguments
# - Make sure to include your variable in the scenarios package's "scenario"
#   variable (found in the __init__.py file); if you don't do this, your 
#   scenario will not be included in the Monte Carlo simulation.
scenario = ScenarioDetails(
    name='No IM Teams',
    fte=fte,
    staff=staff,
    events=[
        vacation,
        bereavement,
        sick,
        medical,
        personal_leave,
        project,
        education,
        new_hire,
        departures,
        internal_swap,
        reorientation,
        learner_swap,
    ],
    shifts=[
        shift_dispensary,
        shift_hpt,
        shift_ed,
        shift_icu,
        shift_ambulatory,
        shift_id_asp,
        shift_acute_care,
    ]
)
