
from datetime import datetime, timedelta
from typing import List, Dict, Tuple


class HOSCalculator:
    
    
    
    MAX_DRIVING_HOURS = 11  
    MAX_ON_DUTY_HOURS = 14  
    MAX_CYCLE_HOURS = 70    
    CYCLE_DAYS = 8
    REQUIRED_BREAK_HOURS = 0.5  
    REQUIRED_OFF_DUTY_HOURS = 10  
    
    def __init__(self, current_cycle_used: float):
        
        self.current_cycle_used = current_cycle_used
        self.available_cycle_hours = self.MAX_CYCLE_HOURS - current_cycle_used
    
    def calculate_available_drive_time(self, hours_on_duty_today: float = 0) -> float:
        
        
        daily_drive_limit = self.MAX_DRIVING_HOURS
        
        
        on_duty_limit = self.MAX_ON_DUTY_HOURS - hours_on_duty_today
        
        
        cycle_limit = self.available_cycle_hours
        
        
        return min(daily_drive_limit, on_duty_limit, cycle_limit)
    
    def calculate_trip_schedule(
        self, 
        distance_to_pickup: float,
        distance_pickup_to_dropoff: float,
        average_speed: float = 55.0,
        pickup_time: float = 1.0,
        dropoff_time: float = 1.0
    ) -> List[Dict]:
        
        schedule = []
        remaining_cycle_hours = self.available_cycle_hours
        current_day = 0
        current_time = 0  
        time_of_day = 0  
        daily_on_duty = 0
        daily_driving = 0  
        continuous_driving = 0  
        
        
        remaining_distance = distance_to_pickup
        
        while remaining_distance > 0:
            
            available_drive_time = min(
                self.MAX_DRIVING_HOURS - daily_driving,  
                8 - continuous_driving,  
                self.MAX_ON_DUTY_HOURS - daily_on_duty,  
                remaining_cycle_hours  
            )
            
            if available_drive_time <= 0.1:  
                if daily_driving >= self.MAX_DRIVING_HOURS or daily_on_duty >= self.MAX_ON_DUTY_HOURS:
                    
                    schedule.append({
                        'activity': 'required_rest',
                        'duration': self.REQUIRED_OFF_DUTY_HOURS,
                        'start_time': time_of_day,
                        'end_time': time_of_day + self.REQUIRED_OFF_DUTY_HOURS,
                        'day': current_day,
                        'distance_covered': 0,
                        'status': 'sleeper'
                    })
                    schedule.append({
                        'activity': 'required_break',
                        'duration': 24-time_of_day - self.REQUIRED_OFF_DUTY_HOURS,
                        'start_time': time_of_day + self.REQUIRED_OFF_DUTY_HOURS,
                        'end_time': 24,
                        'day': current_day,
                        'distance_covered': 0,
                        'status': 'off_duty'
                    })
                    current_time += self.REQUIRED_OFF_DUTY_HOURS
                    time_of_day = 0  
                    current_day += 1
                    daily_on_duty = 0
                    daily_driving = 0
                    continuous_driving = 0
                elif continuous_driving >= 8:
                    
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
                    continuous_driving = 0  
                continue
            
            
            distance_this_segment = min(remaining_distance, available_drive_time * average_speed)
            actual_drive_time = distance_this_segment / average_speed
            
            
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
        
        
        remaining_distance = distance_pickup_to_dropoff
        
        while remaining_distance > 0:
            
            available_drive_time = min(
                self.MAX_DRIVING_HOURS - daily_driving,  
                8 - continuous_driving,  
                self.MAX_ON_DUTY_HOURS - daily_on_duty,  
                remaining_cycle_hours  
            )
            
            if available_drive_time <= 0.1:  
                if daily_driving >= self.MAX_DRIVING_HOURS or daily_on_duty >= self.MAX_ON_DUTY_HOURS:
                    
                    schedule.append({
                        'activity': 'required_rest',
                        'duration': self.REQUIRED_OFF_DUTY_HOURS,
                        'start_time': time_of_day,
                        'end_time': time_of_day + self.REQUIRED_OFF_DUTY_HOURS,
                        'day': current_day,
                        'distance_covered': 0,
                        'status': 'sleeper'
                    })
                    schedule.append({
                        'activity': 'required_break',
                        'duration': 24-time_of_day - self.REQUIRED_OFF_DUTY_HOURS,
                        'start_time': time_of_day + self.REQUIRED_OFF_DUTY_HOURS,
                        'end_time': 24,
                        'day': current_day,
                        'distance_covered': 0,
                        'status': 'off_duty'
                    })
                    current_time += self.REQUIRED_OFF_DUTY_HOURS
                    time_of_day = 0  
                    current_day += 1
                    daily_on_duty = 0
                    daily_driving = 0
                    continuous_driving = 0
                elif continuous_driving >= 8:
                    
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
                    continuous_driving = 0  
                continue
            
            
            distance_this_segment = min(remaining_distance, available_drive_time * average_speed)
            actual_drive_time = distance_this_segment / average_speed
            
            
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
        time_shift = 0  

        for segment in route_segments:
            
            shifted_segment = segment.copy()
            if( shifted_segment['start_time'] !=0):
              shifted_segment['start_time'] += time_shift
            shifted_segment['end_time'] += time_shift
            shifted_segment['end_time'] = min(shifted_segment['end_time'], 24)


            updated_segments.append(shifted_segment)

            
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
                    time_shift += fuel_time  
        return updated_segments