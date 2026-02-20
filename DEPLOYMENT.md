# Deployment Guide

This guide will help you deploy the ELD Trip Planner to production.

## Option 1: Vercel (Frontend) + Railway (Backend)

### Backend on Railway

1. Create a Railway account at https://railway.app
2. Create a new project
3. Connect your GitHub repository
4. Add the backend folder as the root directory
5. Add environment variables:
   ```
   DEBUG=False
   SECRET_KEY=your-random-secret-key
   ALLOWED_HOSTS=*
   ```
6. Railway will auto-detect Django and deploy

### Frontend on Vercel

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

3. Update `package.json` to remove proxy and create `.env.production`:
   ```
   REACT_APP_API_URL=https://your-backend-url.railway.app
   ```

4. Deploy:
   ```bash
   vercel --prod
   ```

5. Update Django ALLOWED_HOSTS and CORS settings with your Vercel domain

## Option 2: Both on Heroku

### Backend

1. Create Heroku app:
   ```bash
   cd backend
   heroku create eld-trip-planner-backend
   ```

2. Add buildpack:
   ```bash
   heroku buildpacks:add heroku/python
   ```

3. Set environment variables:
   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-random-secret-key
   ```

4. Add gunicorn to requirements.txt:
   ```
   gunicorn==21.2.0
   ```

5. Deploy:
   ```bash
   git push heroku main
   ```

### Frontend

1. Create separate Heroku app:
   ```bash
   cd frontend
   heroku create eld-trip-planner-frontend
   ```

2. Add Node.js buildpack:
   ```bash
   heroku buildpacks:add heroku/nodejs
   ```

3. Create Procfile in frontend:
   ```
   web: npm start
   ```

4. Set API URL:
   ```bash
   heroku config:set REACT_APP_API_URL=https://eld-trip-planner-backend.herokuapp.com
   ```

5. Deploy:
   ```bash
   git push heroku main
   ```

## Option 3: Netlify (Frontend) + PythonAnywhere (Backend)

### Backend on PythonAnywhere

1. Create account at https://www.pythonanywhere.com
2. Upload code via Git or web interface
3. Create virtual environment
4. Configure WSGI file
5. Set static files path

### Frontend on Netlify

1. Build the frontend:
   ```bash
   cd frontend
   npm run build
   ```

2. Drag and drop `build` folder to Netlify or use CLI:
   ```bash
   npm install -g netlify-cli
   netlify deploy --prod
   ```

## Post-Deployment Checklist

- [ ] Update ALLOWED_HOSTS in Django settings
- [ ] Update CORS_ALLOWED_ORIGINS with frontend URL
- [ ] Set DEBUG=False in production
- [ ] Use strong SECRET_KEY
- [ ] Test all API endpoints
- [ ] Test frontend-backend connection
- [ ] Verify map rendering
- [ ] Test ELD log generation
- [ ] Check all routes work correctly

## Environment Variables Summary

### Backend
- `DEBUG`: False for production
- `SECRET_KEY`: Random string for security
- `ALLOWED_HOSTS`: Your domain(s)
- `CORS_ALLOWED_ORIGINS`: Frontend URL(s)

### Frontend
- `REACT_APP_API_URL`: Backend API URL

## Troubleshooting

### CORS Errors
- Ensure CORS_ALLOWED_ORIGINS includes your frontend URL
- Check that corsheaders is in INSTALLED_APPS

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Verify STATIC_ROOT and STATIC_URL settings

### Map Not Rendering
- Check browser console for errors
- Verify Leaflet CSS is loaded
- Check network tab for tile loading

### API Connection Failed
- Verify backend URL is correct
- Check CORS settings
- Test API endpoint directly in browser

## Performance Optimization

1. Enable Django caching
2. Use CDN for static files
3. Compress images
4. Enable gzip compression
5. Use production build of React (`npm run build`)

## Security Recommendations

1. Never commit `.env` files
2. Use environment variables for secrets
3. Enable HTTPS (most platforms do this automatically)
4. Set secure CORS policies
5. Regularly update dependencies
