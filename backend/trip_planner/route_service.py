"""
Route calculation service using real-world road routing
Supports OpenRouteService (with API key) and OSRM (free, no key needed)
"""
import requests
import os
from typing import List, Dict, Tuple, Optional
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


class RouteService:
    """Service for calculating routes using real-world roads"""
    
    def __init__(self):
        self.geocoder = Nominatim(user_agent="eld_trip_planner")
        # OpenRouteService API key (get free key from https://openrouteservice.org/)
        self.ors_api_key = os.environ.get('ORS_API_KEY', None)
        # OSRM public instance (free, no key needed)
        self.osrm_base_url = "http://router.project-osrm.org/route/v1/driving"
    
    def geocode_location(self, location: str) -> Optional[Tuple[float, float]]:
        """
        Convert location string to coordinates
        
        Args:
            location: Location string (address, city, etc.)
            
        Returns:
            Tuple of (latitude, longitude) or None
        """
        try:
            location_data = self.geocoder.geocode(location)
            if location_data:
                return (location_data.latitude, location_data.longitude)
        except Exception as e:
            print(f"Geocoding error: {e}")
        return None
    
    def calculate_distance(
        self, 
        start_coords: Tuple[float, float], 
        end_coords: Tuple[float, float]
    ) -> float:
        """
        Calculate distance between two coordinates
        
        Args:
            start_coords: Starting coordinates (lat, lon)
            end_coords: Ending coordinates (lat, lon)
            
        Returns:
            Distance in miles
        """
        distance_km = geodesic(start_coords, end_coords).kilometers
        distance_miles = distance_km * 0.621371
        return distance_miles
    
    def get_route_with_waypoints(
        self,
        current_location: str,
        pickup_location: str,
        dropoff_location: str
    ) -> Dict:
        """
        Calculate route with real-world road routing
        
        Args:
            current_location: Current location string
            pickup_location: Pickup location string
            dropoff_location: Dropoff location string
            
        Returns:
            Dictionary with route information including real road paths
        """
        # Geocode all locations
        current_coords = self.geocode_location(current_location)
        pickup_coords = self.geocode_location(pickup_location)
        dropoff_coords = self.geocode_location(dropoff_location)
        
        if not all([current_coords, pickup_coords, dropoff_coords]):
            raise ValueError("Could not geocode one or more locations")
        
        # Get real-world routing for both legs
        leg1_route = self._get_road_route(current_coords, pickup_coords)
        leg2_route = self._get_road_route(pickup_coords, dropoff_coords)
        
        # Calculate total distance from road routes
        distance_to_pickup = leg1_route['distance']
        distance_pickup_to_dropoff = leg2_route['distance']
        total_distance = distance_to_pickup + distance_pickup_to_dropoff
        
        # Combine waypoints from both legs
        waypoints = leg1_route['waypoints'] + leg2_route['waypoints']
        
        return {
            'total_distance': total_distance,
            'distance_to_pickup': distance_to_pickup,
            'distance_pickup_to_dropoff': distance_pickup_to_dropoff,
            'duration_hours': (leg1_route['duration'] + leg2_route['duration']) / 3600,
            'coordinates': {
                'current': current_coords,
                'pickup': pickup_coords,
                'dropoff': dropoff_coords
            },
            'waypoints': waypoints,
            'route_geometry': waypoints  # Full route for map display
        }
    
    def _get_road_route(self, start: Tuple[float, float], end: Tuple[float, float]) -> Dict:
        """
        Get real-world road route between two points
        
        Args:
            start: Start coordinates (lat, lon)
            end: End coordinates (lat, lon)
            
        Returns:
            Dictionary with distance (miles), duration (seconds), and waypoints
        """
        # Try OSRM first (free, no key needed)
        try:
            route = self._get_osrm_route(start, end)
            if route:
                return route
        except Exception as e:
            print(f"OSRM routing failed: {e}")
        
        # Fallback to OpenRouteService if API key is available
        if self.ors_api_key:
            try:
                route = self._get_ors_route(start, end)
                if route:
                    return route
            except Exception as e:
                print(f"ORS routing failed: {e}")
        
        # Ultimate fallback: geodesic distance with interpolated waypoints
        print("Using geodesic fallback routing")
        return self._get_geodesic_route(start, end)
    
    def _get_osrm_route(self, start: Tuple[float, float], end: Tuple[float, float]) -> Optional[Dict]:
        """
        Get route from OSRM (Open Source Routing Machine)
        Public instance - no API key needed
        """
        # OSRM uses lon,lat format (opposite of normal)
        url = f"{self.osrm_base_url}/{start[1]},{start[0]};{end[1]},{end[0]}"
        params = {
            'overview': 'full',
            'geometries': 'geojson',
            'steps': 'false'
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 'Ok' and data.get('routes'):
                route = data['routes'][0]
                
                # Extract coordinates from geometry
                coordinates = route['geometry']['coordinates']
                # Convert from [lon, lat] to (lat, lon)
                waypoints = [(coord[1], coord[0]) for coord in coordinates]
                
                # Distance in meters, convert to miles
                distance_miles = route['distance'] * 0.000621371
                duration_seconds = route['duration']
                
                return {
                    'distance': distance_miles,
                    'duration': duration_seconds,
                    'waypoints': waypoints
                }
        return None
    
    def _get_ors_route(self, start: Tuple[float, float], end: Tuple[float, float]) -> Optional[Dict]:
        """
        Get route from OpenRouteService (requires API key)
        """
        url = "https://api.openrouteservice.org/v2/directions/driving-car"
        headers = {
            'Authorization': self.ors_api_key,
            'Content-Type': 'application/json'
        }
        body = {
            'coordinates': [[start[1], start[0]], [end[1], end[0]]]
        }
        
        response = requests.post(url, json=body, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('routes'):
                route = data['routes'][0]
                
                # Extract coordinates from geometry
                coordinates = route['geometry']['coordinates']
                waypoints = [(coord[1], coord[0]) for coord in coordinates]
                
                # Distance in meters, convert to miles
                distance_miles = route['summary']['distance'] * 0.000621371
                duration_seconds = route['summary']['duration']
                
                return {
                    'distance': distance_miles,
                    'duration': duration_seconds,
                    'waypoints': waypoints
                }
        return None
    
    def _get_geodesic_route(self, start: Tuple[float, float], end: Tuple[float, float]) -> Dict:
        """
        Fallback: Calculate geodesic distance with interpolated waypoints
        """
        distance_km = geodesic(start, end).kilometers
        distance_miles = distance_km * 0.621371
        
        # Estimate duration assuming 55 mph average
        duration_seconds = (distance_miles / 55) * 3600
        
        # Generate interpolated waypoints
        waypoints = [start]
        segments = 20
        for i in range(1, segments):
            ratio = i / segments
            lat = start[0] + (end[0] - start[0]) * ratio
            lon = start[1] + (end[1] - start[1]) * ratio
            waypoints.append((lat, lon))
        waypoints.append(end)
        
        return {
            'distance': distance_miles,
            'duration': duration_seconds,
            'waypoints': waypoints
        }
    
    def calculate_rest_stop_locations(
        self,
        route_waypoints: List[Tuple[float, float]],
        rest_intervals_miles: List[float]
    ) -> List[Dict]:
        """
        Calculate approximate locations for rest stops along route
        
        Args:
            route_waypoints: List of waypoint coordinates
            rest_intervals_miles: List of distances where rest stops should occur
            
        Returns:
            List of rest stop information
        """
        rest_stops = []
        total_distance = 0
        rest_index = 0
        
        for i in range(len(route_waypoints) - 1):
            segment_distance = self.calculate_distance(
                route_waypoints[i], 
                route_waypoints[i + 1]
            )
            total_distance += segment_distance
            
            # Check if rest stop needed at this segment
            if rest_index < len(rest_intervals_miles):
                if total_distance >= rest_intervals_miles[rest_index]:
                    rest_stops.append({
                        'location': route_waypoints[i + 1],
                        'distance_from_start': total_distance,
                        'type': 'rest_stop'
                    })
                    rest_index += 1
        
        return rest_stops
