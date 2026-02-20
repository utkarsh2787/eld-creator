# 🚚 ELD Trip Planner

A full-stack application for planning HOS (Hours of Service) compliant trucking trips with automated route planning and ELD log generation.

## Features

- ✅ **HOS Compliance**: Automatic calculation based on 70-hour/8-day rule for property-carrying drivers
- 🛣️ **Real-World Road Routing**: Uses OSRM for actual driving routes (not straight lines!)
- 📏 **Accurate Distances**: Calculates trip distance based on real road networks
- 📊 **ELD Log Generation**: Automatically generate graphical daily log sheets
- ⏱️ **Smart Scheduling**: Calculate required rest stops, breaks, and fuel stops
- 🎨 **Modern UI/UX**: Beautiful, responsive interface built with React
- 📍 **Interactive Maps**: Visual route display with actual road paths

## Tech Stack

### Backend
- Django 4.2.7
- Django REST Framework
- Python 3.8+
- Pillow (for ELD log image generation)
- Geopy (for geocoding)

### Frontend
- React 18
- Leaflet & React-Leaflet (for maps)
- Axios (for API calls)
- Modern CSS with gradient designs

## Project Structure

```
eld/
├── backend/
│   ├── eld_backend/          # Django project settings
│   ├── trip_planner/         # Main app
│   │   ├── hos_calculator.py # HOS calculation logic
│   │   ├── route_service.py  # Route and geocoding service
│   │   ├── eld_log_generator.py # ELD log image generation
│   │   └── views.py          # API endpoints
│   ├── manage.py
│   └── requirements.txt
└── frontend/
    ├── public/
    ├── src/
    │   ├── components/       # React components
    │   ├── App.js
    │   └── App.css
    └── package.json
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the Django development server:
```bash
python manage.py runserver
```

The backend will be running at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The frontend will be running at `http://localhost:3000`

## Usage

1. Open the application in your browser at `http://localhost:3000`

2. Fill in the trip details:
   - **Current Location**: Your starting point (e.g., "Los Angeles, CA")
   - **Pickup Location**: Where you'll pick up the load (e.g., "Phoenix, AZ")
   - **Dropoff Location**: Final destination (e.g., "Dallas, TX")
   - **Current Cycle Used**: Hours already used in your 8-day cycle (0-70)
   - **Driver Name**: Your name (optional)

3. Click "Plan Trip" to generate:
   - Route map with waypoints
   - Detailed schedule with all stops
   - ELD daily log sheets
   - Trip summary statistics

## HOS Rules Implemented

The application enforces the following HOS regulations for property-carrying drivers:

- **70-hour/8-day rule**: Maximum 70 hours on duty in 8 consecutive days
- **11-hour driving limit**: Maximum 11 hours of driving per shift
- **14-hour on-duty limit**: Maximum 14 hours on duty per shift
- **10-hour off-duty**: Required rest period between shifts
- **30-minute break**: Required after 8 hours of driving
- **Fuel stops**: Automatically scheduled every 1,000 miles
- **Pickup/Dropoff time**: 1 hour allocated for each

## API Endpoints

### POST `/api/plan-trip/`

Plan a trip with HOS compliance.

**Request Body:**
```json
{
  "current_location": "Los Angeles, CA",
  "pickup_location": "Phoenix, AZ",
  "dropoff_location": "Dallas, TX",
  "current_cycle_used": 15.5,
  "driver_name": "John Doe"
}
```

**Response:**
```json
{
  "route": {
    "total_distance": 1234.5,
    "coordinates": {...},
    "waypoints": [...],
    "rest_stops": [...]
  },
  "schedule": [...],
  "summary": {
    "total_distance_miles": 1234.5,
    "total_driving_hours": 22.4,
    "total_trip_hours": 45.2,
    "hos_compliant": true
  },
  "eld_logs": ["base64_image_1", "base64_image_2"]
}
```

### GET `/api/health/`

Health check endpoint.

## Deployment

### Deploying Backend

1. **Heroku** (Recommended):
```bash
# Install Heroku CLI
heroku create your-app-name
git push heroku main
```

2. **Railway**:
- Connect your GitHub repository
- Railway will auto-detect Django
- Add environment variables

3. **PythonAnywhere**:
- Upload code via Git or web interface
- Configure WSGI file
- Set up virtualenv

### Deploying Frontend

1. **Vercel** (Recommended):
```bash
cd frontend
npm install -g vercel
vercel
```

2. **Netlify**:
```bash
cd frontend
npm run build
# Drag and drop the build folder to Netlify
```

3. Update the API URL in `package.json` proxy or create a `.env` file:
```
REACT_APP_API_URL=https://your-backend-url.com
```

## Environment Variables

### Backend (.env)
```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-domain.com
```

### Frontend (.env)
```
REACT_APP_API_URL=https://your-backend-url.com
```

## Testing

Try these example trips:

1. **Short Trip**:
   - Current: Los Angeles, CA
   - Pickup: San Diego, CA
   - Dropoff: Phoenix, AZ
   - Cycle Used: 10

2. **Long Trip**:
   - Current: New York, NY
   - Pickup: Chicago, IL
   - Dropoff: Los Angeles, CA
   - Cycle Used: 20

3. **Multi-Day Trip**:
   - Current: Miami, FL
   - Pickup: Atlanta, GA
   - Dropoff: Seattle, WA
   - Cycle Used: 5

## Routing Features

### Real-World Road Routing
The app uses actual road networks for route calculation:

- **OSRM (Primary)**: Free public instance, no API key needed
- **OpenRouteService**: Optional, for enhanced accuracy (requires free API key)
- **Geodesic Fallback**: Straight-line distance if routing services unavailable

### Optional: OpenRouteService API Key
For potentially better routing in some regions:

1. Get free API key: https://openrouteservice.org/dev/#/signup
2. Add to backend `.env`:
   ```
   ORS_API_KEY=your-api-key-here
   ```
3. Restart backend server

## Known Limitations

- Geocoding uses Nominatim (OpenStreetMap) which has rate limits
- OSRM public instance may have occasional downtime (fallback to geodesic)
- ELD logs use default system fonts (install DejaVu fonts for better appearance)

## Future Enhancements

- [ ] Real-time traffic integration
- [ ] Weather conditions
- [ ] Truck stop database integration
- [ ] Multiple driver support
- [ ] Historical trip tracking
- [ ] Export logs as PDF
- [ ] Mobile app version

## License

MIT License - Feel free to use for personal or commercial projects.

## Support

For issues or questions, please create an issue on GitHub.

## Credits

- Built with Django & React
- Maps powered by OpenStreetMap & Leaflet
- Geocoding by Nominatim
