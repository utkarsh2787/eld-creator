"""
API Views for Trip Planner
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .hos_calculator import HOSCalculator
from .route_service import RouteService
from .eld_log_generator import ELDLogGenerator


@api_view(["POST"])
def plan_trip(request):
    """
    Plan a trip with HOS compliance and generate ELD logs

    Expected input:
    {
        "current_location": "Los Angeles, CA",
        "pickup_location": "Phoenix, AZ",
        "dropoff_location": "Dallas, TX",
        "current_cycle_used": 15.5,
        "driver_name": "John Doe"
    }
    """
    try:
        print(request.data)
        # Extract input data
        current_location = request.data.get("current_location")
        pickup_location = request.data.get("pickup_location")
        dropoff_location = request.data.get("dropoff_location")
        current_cycle_used = float(request.data.get("current_cycle_used", 0))
        driver_name = request.data.get("driver_name", "Driver")

        # Validate inputs
        if not all([current_location, pickup_location, dropoff_location]):
            return Response(
                {"error": "Missing required location fields"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Initialize services
        route_service = RouteService()
        hos_calculator = HOSCalculator(current_cycle_used)
        eld_generator = ELDLogGenerator()

        # Get route information
        try:
            route_info = route_service.get_route_with_waypoints(
                current_location, pickup_location, dropoff_location
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        distance_to_pickup = route_info["distance_to_pickup"]
        distance_pickup_to_dropoff = route_info["distance_pickup_to_dropoff"]
        total_distance = route_info["total_distance"]

        # Calculate trip schedule with HOS compliance
        # Flow: Current -> Drive -> Pickup Location -> Pickup -> Drive -> Dropoff Location -> Dropoff
        schedule = hos_calculator.calculate_trip_schedule(
            distance_to_pickup=distance_to_pickup,
            distance_pickup_to_dropoff=distance_pickup_to_dropoff,
            average_speed=55.0,
            pickup_time=1.0,
            dropoff_time=1.0,
        )

        # Add fuel stops (every 1000 miles)
        schedule_with_fuel = hos_calculator.add_fuel_stops(
            schedule, fuel_interval=1000.0, fuel_time=0.5
        )

        # Calculate rest stop locations
        rest_distances = []
        cumulative_distance = 0
        for segment in schedule_with_fuel:
            if segment["activity"] == "required_rest":
                rest_distances.append(cumulative_distance)
            cumulative_distance += segment.get("distance_covered", 0)

        rest_stops = route_service.calculate_rest_stop_locations(
            route_info["waypoints"], rest_distances
        )
        print(schedule_with_fuel)

        # Generate ELD logs
        eld_logs = eld_generator.generate_multiple_logs(schedule_with_fuel, driver_name)

        # Calculate trip summary
        total_driving_time = sum(
            s["duration"] for s in schedule_with_fuel if s["status"] == "driving"
        )
        total_trip_time = (
            schedule_with_fuel[-1]["day"] * 24 + schedule_with_fuel[-1]["end_time"]
            if schedule_with_fuel
            else 0
        )
        num_rest_stops = sum(
            1 for s in schedule_with_fuel if s["activity"] == "required_rest"
        )
        num_fuel_stops = sum(
            1 for s in schedule_with_fuel if s["activity"] == "fuel_stop"
        )

        # Prepare response
        response_data = {
            "route": {
                "total_distance": round(total_distance, 2),
                "distance_to_pickup": round(route_info["distance_to_pickup"], 2),
                "distance_pickup_to_dropoff": round(
                    route_info["distance_pickup_to_dropoff"], 2
                ),
                "coordinates": route_info["coordinates"],
                "waypoints": route_info["waypoints"],
                "rest_stops": rest_stops,
            },
            "schedule": schedule_with_fuel,
            "summary": {
                "total_distance_miles": round(total_distance, 2),
                "total_driving_hours": round(total_driving_time, 2),
                "total_trip_hours": round(total_trip_time, 2),
                "total_trip_days": max(s["day"] for s in schedule_with_fuel) + 1,
                "number_of_rest_stops": num_rest_stops,
                "number_of_fuel_stops": num_fuel_stops,
                "hos_compliant": True,
                "cycle_hours_used": round(current_cycle_used + total_driving_time, 2),
                "cycle_hours_remaining": round(
                    70 - (current_cycle_used + total_driving_time), 2
                ),
            },
            "eld_logs": eld_logs,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": f"Internal server error: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def health_check(request):
    """Health check endpoint"""
    return Response({"status": "ok"}, status=status.HTTP_200_OK)
