"""
Hours of Service (HOS) Calculator for Property-Carrying Drivers
70-hour/8-day rule implementation
"""
from datetime import datetime, timedelta
from typing import List, Dict, Tuple


class HOSCalculator:
    """Calculate HOS compliance for 70-hour/8-day rule"""
    
    # HOS limits for property-carrying drivers (70/8 rule)
    MAX_DRIVING_HOURS = 11  # Maximum driving hours per day
    MAX_ON_DUTY_HOURS = 14  # Maximum on-duty hours per day
    MAX_CYCLE_HOURS = 70    # Maximum hours in 8-day cycle
    CYCLE_DAYS = 8
    REQUIRED_BREAK_HOURS = 0.5  # 30-minute break after 8 hours driving
    REQUIRED_OFF_DUTY_HOURS = 10  # Required off-duty time between shifts
    
    def __init__(self, current_cycle_used: float):
        """
        Initialize HOS calculator
        
        Args:
            current_cycle_used: Hours already used in current 8-day cycle
        """
        self.current_cycle_used = current_cycle_used
        self.available_cycle_hours = self.MAX_CYCLE_HOURS - current_cycle_used
    
    def calculate_available_drive_time(self, hours_on_duty_today: float = 0) -> float:
        """
        Calculate available driving time considering all HOS rules
        
        Args:
            hours_on_duty_today: Hours already on duty today
            
        Returns:
            Available driving hours
        """
        # Daily driving limit
        daily_drive_limit = self.MAX_DRIVING_HOURS
        
        # Daily on-duty limit
        on_duty_limit = self.MAX_ON_DUTY_HOURS - hours_on_duty_today
        
        # Cycle limit
        cycle_limit = self.available_cycle_hours
        
        # Return minimum of all limits
        return min(daily_drive_limit, on_duty_limit, cycle_limit)
    
    def calculate_trip_schedule(
        self, 
        distance_to_pickup: float,
        distance_pickup_to_dropoff: float,
        average_speed: float = 55.0,
        pickup_time: float = 1.0,
        dropoff_time: float = 1.0
    ) -> List[Dict]:
        """
        Calculate trip schedule with required breaks and rest periods
        
        Flow: Current Location -> Drive -> Pickup Location -> Pickup Activity -> Drive -> Dropoff Location -> Dropoff Activity
        
        Args:
            distance_to_pickup: Distance from current location to pickup location
            distance_pickup_to_dropoff: Distance from pickup to dropoff location
            average_speed: Average driving speed in mph
            pickup_time: Time for pickup in hours
            dropoff_time: Time for dropoff in hours
            
        Returns:
            List of schedule segments with timing and activities
        """
        schedule = []
        remaining_cycle_hours = self.available_cycle_hours
        current_day = 0
        current_time = 0  # Cumulative hours from trip start
        time_of_day = 0  # Hours within current day (0-24)
        daily_on_duty = 0
        daily_driving = 0  # Total driving hours today (max 11, resets after 10hr rest)
        continuous_driving = 0  # Continuous driving (max 8, resets after 30min break)
        
        # === LEG 1: Drive to pickup location ===
        remaining_distance = distance_to_pickup
        
        while remaining_distance > 0:
            # Calculate available driving time for current shift
            available_drive_time = min(
                self.MAX_DRIVING_HOURS - daily_driving,  # 11hr daily limit
                8 - continuous_driving,  # 8hr continuous limit
                self.MAX_ON_DUTY_HOURS - daily_on_duty,  # 14hr on-duty limit
                remaining_cycle_hours  # 70hr cycle limit
            )
            
            if available_drive_time <= 0.1:  # Need rest or break
                if daily_driving >= self.MAX_DRIVING_HOURS or daily_on_duty >= self.MAX_ON_DUTY_HOURS:
                    # Need 10-hour rest
                    schedule.append({
                        'activity': 'required_rest',
                        'duration': self.REQUIRED_OFF_DUTY_HOURS,
                        'start_time': time_of_day,
                        'end_time': time_of_day + self.REQUIRED_OFF_DUTY_HOURS,
                        'day': current_day,
                        'distance_covered': 0,
                        'status': 'off_duty'
                    })
                    current_time += self.REQUIRED_OFF_DUTY_HOURS
                    time_of_day = 0  # Reset to start of new day
                    current_day += 1
                    daily_on_duty = 0
                    daily_driving = 0
                    continuous_driving = 0
                elif continuous_driving >= 8:
                    # Need 30-minute break
                    schedule.append({
                        'activity': 'required_break',
                        'duration': self.REQUIRED_BREAK_HOURS,
                        'start_time': time_of_day,
                        'end_time': time_of_day + self.REQUIRED_BREAK_HOURS,
                        'day': current_day,
                        'distance_covered': 0,
                        'status': 'on_duty'
                    })
                    current_time += self.REQUIRED_BREAK_HOURS
                    time_of_day += self.REQUIRED_BREAK_HOURS
                    daily_on_duty += self.REQUIRED_BREAK_HOURS
                    continuous_driving = 0  # Reset continuous only
                continue
            
            # Calculate distance for this segment
            distance_this_segment = min(remaining_distance, available_drive_time * average_speed)
            actual_drive_time = distance_this_segment / average_speed
            
            # Add driving segment
            schedule.append({
                'activity': 'driving_to_pickup',
                'duration': actual_drive_time,
                'start_time': time_of_day,
                'end_time': time_of_day + actual_drive_time,
                'day': current_day,
                'distance_covered': distance_this_segment,
                'status': 'driving'
            })
            current_time += actual_drive_time
            time_of_day += actual_drive_time
            daily_on_duty += actual_drive_time
            daily_driving += actual_drive_time
            continuous_driving += actual_drive_time
            remaining_distance -= distance_this_segment
            remaining_cycle_hours -= actual_drive_time
        
        # === PICKUP ACTIVITY ===
        schedule.append({
            'activity': 'pickup',
            'duration': pickup_time,
            'start_time': time_of_day,
            'end_time': time_of_day + pickup_time,
            'day': current_day,
            'distance_covered': 0,
            'status': 'on_duty'
        })
        current_time += pickup_time
        time_of_day += pickup_time
        daily_on_duty += pickup_time
        
        # === LEG 2: Drive from pickup to dropoff location ===
        remaining_distance = distance_pickup_to_dropoff
        
        while remaining_distance > 0:
            # Calculate available driving time for current shift
            available_drive_time = min(
                self.MAX_DRIVING_HOURS - daily_driving,  # 11hr daily limit
                8 - continuous_driving,  # 8hr continuous limit
                self.MAX_ON_DUTY_HOURS - daily_on_duty,  # 14hr on-duty limit
                remaining_cycle_hours  # 70hr cycle limit
            )
            
            if available_drive_time <= 0.1:  # Need rest or break
                if daily_driving >= self.MAX_DRIVING_HOURS or daily_on_duty >= self.MAX_ON_DUTY_HOURS:
                    # Need 10-hour rest
                    schedule.append({
                        'activity': 'required_rest',
                        'duration': self.REQUIRED_OFF_DUTY_HOURS,
                        'start_time': time_of_day,
                        'end_time': time_of_day + self.REQUIRED_OFF_DUTY_HOURS,
                        'day': current_day,
                        'distance_covered': 0,
                        'status': 'off_duty'
                    })
                    current_time += self.REQUIRED_OFF_DUTY_HOURS
                    time_of_day = 0  # Reset to start of new day
                    current_day += 1
                    daily_on_duty = 0
                    daily_driving = 0
                    continuous_driving = 0
                elif continuous_driving >= 8:
                    # Need 30-minute break
                    schedule.append({
                        'activity': 'required_break',
                        'duration': self.REQUIRED_BREAK_HOURS,
                        'start_time': time_of_day,
                        'end_time': time_of_day + self.REQUIRED_BREAK_HOURS,
                        'day': current_day,
                        'distance_covered': 0,
                        'status': 'on_duty'
                    })
                    current_time += self.REQUIRED_BREAK_HOURS
                    time_of_day += self.REQUIRED_BREAK_HOURS
                    daily_on_duty += self.REQUIRED_BREAK_HOURS
                    continuous_driving = 0  # Reset continuous only
                continue
            
            # Calculate distance for this segment
            distance_this_segment = min(remaining_distance, available_drive_time * average_speed)
            actual_drive_time = distance_this_segment / average_speed
            
            # Add driving segment
            schedule.append({
                'activity': 'driving_to_dropoff',
                'duration': actual_drive_time,
                'start_time': time_of_day,
                'end_time': time_of_day + actual_drive_time,
                'day': current_day,
                'distance_covered': distance_this_segment,
                'status': 'driving'
            })
            current_time += actual_drive_time
            time_of_day += actual_drive_time
            daily_on_duty += actual_drive_time
            daily_driving += actual_drive_time
            continuous_driving += actual_drive_time
            remaining_distance -= distance_this_segment
            remaining_cycle_hours -= actual_drive_time
        
        # === DROPOFF ACTIVITY ===
        schedule.append({
            'activity': 'dropoff',
            'duration': dropoff_time,
            'start_time': time_of_day,
            'end_time': time_of_day + dropoff_time,
            'day': current_day,
            'distance_covered': 0,
            'status': 'on_duty'
        })
        
        return schedule
    
    def add_fuel_stops(
        self, 
        route_segments: List[Dict], 
        fuel_interval: float = 1000.0,
        fuel_time: float = 0.5
    ) -> List[Dict]:

        updated_segments = []
        total_distance = 0
        last_fuel_distance = 0
        time_shift = 0  # cumulative shift in hours

        for segment in route_segments:
            # Shift current segment by any previous fuel stops
            shifted_segment = segment.copy()
            shifted_segment['start_time'] += time_shift
            shifted_segment['end_time'] += time_shift

            updated_segments.append(shifted_segment)

            # Only count driving distance
            if shifted_segment['activity'] in ['driving_to_pickup', 'driving_to_dropoff']:
                distance_covered = shifted_segment['distance_covered']
                total_distance += distance_covered

                if total_distance - last_fuel_distance >= fuel_interval:
                    fuel_start = shifted_segment['end_time']
                    fuel_end = fuel_start + fuel_time

                    updated_segments.append({
                        'activity': 'fuel_stop',
                        'duration': fuel_time,
                        'start_time': fuel_start,
                        'end_time': fuel_end,
                        'day': shifted_segment['day'],
                        'distance_covered': 0,
                        'status': 'on_duty'
                    })

                    last_fuel_distance = total_distance
                    time_shift += fuel_time  # ⬅️ push all future segments
        return updated_segments