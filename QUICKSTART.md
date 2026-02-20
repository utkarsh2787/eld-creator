# Quick Start Guide

Get the ELD Trip Planner running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ installed
- Git (optional)

## Step 1: Backend Setup (2 minutes)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start Django server
python manage.py runserver
```

✅ Backend should now be running at http://localhost:8000

Test it: http://localhost:8000/api/health/

## Step 2: Frontend Setup (3 minutes)

Open a **new terminal window** and:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start React app
npm start
```

✅ Frontend should automatically open at http://localhost:3000

## Step 3: Try It Out!

1. Fill in the form with example data:
   - **Current Location**: Los Angeles, CA
   - **Pickup Location**: Phoenix, AZ
   - **Dropoff Location**: Dallas, TX
   - **Current Cycle Used**: 10
   - **Driver Name**: Test Driver

2. Click "Plan Trip"

3. Wait 10-15 seconds for geocoding and calculations

4. View your results:
   - Trip summary with statistics
   - Interactive route map
   - Detailed schedule table
   - ELD daily log sheets

## Troubleshooting

### Backend won't start
- Make sure virtual environment is activated
- Check Python version: `python --version` (should be 3.8+)
- Try: `pip install -r requirements.txt --upgrade`

### Frontend won't start
- Check Node version: `node --version` (should be 16+)
- Delete `node_modules` and run `npm install` again
- Check port 3000 isn't in use

### API connection fails
- Ensure backend is running on port 8000
- Check `package.json` has `"proxy": "http://localhost:8000"`
- Check browser console for errors

### Geocoding errors
- The app uses Nominatim (free) which has rate limits
- Wait a few seconds between requests
- Use full addresses: "City, State" format

### Map not displaying
- Check browser console for errors
- Ensure Leaflet CSS is loaded
- Check internet connection (map tiles load from internet)

## Example Test Cases

### Short Trip (< 1 day)
- Current: San Diego, CA
- Pickup: Los Angeles, CA  
- Dropoff: San Francisco, CA
- Cycle Used: 5

### Medium Trip (1-2 days)
- Current: Los Angeles, CA
- Pickup: Phoenix, AZ
- Dropoff: Dallas, TX
- Cycle Used: 15

### Long Trip (3+ days)
- Current: New York, NY
- Pickup: Chicago, IL
- Dropoff: Los Angeles, CA
- Cycle Used: 20

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for hosting instructions
- Customize the UI in `frontend/src/App.css`
- Modify HOS rules in `backend/trip_planner/hos_calculator.py`

## Common Questions

**Q: Can I use real addresses?**
A: Yes! Use format: "123 Main St, City, State" or just "City, State"

**Q: How accurate is the route calculation?**
A: Currently uses straight-line distance. For production, integrate Google Maps or similar.

**Q: Can I export the ELD logs?**
A: Right-click on the log images and "Save Image As..."

**Q: Does this comply with FMCSA regulations?**
A: This is a demo app. For real compliance, consult with regulatory experts.

**Q: Can I add more stops?**
A: Currently supports 1 pickup and 1 dropoff. Modify the API to support multiple stops.

## Support

Having issues? Check:
1. Browser console (F12) for errors
2. Terminal output for backend errors
3. Network tab to see API requests/responses

Happy trucking! 🚚
