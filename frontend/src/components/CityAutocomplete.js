import React, { useState, useRef, useEffect } from 'react';

// ── Famous cities (US-focused for trucking + major world cities) ──
const CITIES = [
  // USA — by state
  'Atlanta, GA', 'Augusta, GA', 'Savannah, GA',
  'Birmingham, AL', 'Mobile, AL', 'Huntsville, AL',
  'Anchorage, AK', 'Fairbanks, AK',
  'Phoenix, AZ', 'Tucson, AZ', 'Mesa, AZ', 'Scottsdale, AZ', 'Flagstaff, AZ',
  'Little Rock, AR', 'Fort Smith, AR',
  'Los Angeles, CA', 'San Francisco, CA', 'San Diego, CA', 'Sacramento, CA',
  'San Jose, CA', 'Fresno, CA', 'Oakland, CA', 'Long Beach, CA', 'Bakersfield, CA',
  'Denver, CO', 'Colorado Springs, CO', 'Aurora, CO', 'Fort Collins, CO',
  'Hartford, CT', 'New Haven, CT', 'Bridgeport, CT',
  'Wilmington, DE', 'Dover, DE',
  'Jacksonville, FL', 'Miami, FL', 'Tampa, FL', 'Orlando, FL',
  'St. Petersburg, FL', 'Tallahassee, FL', 'Fort Lauderdale, FL',
  'Honolulu, HI',
  'Boise, ID', 'Idaho Falls, ID',
  'Chicago, IL', 'Aurora, IL', 'Rockford, IL', 'Naperville, IL',
  'Indianapolis, IN', 'Fort Wayne, IN', 'Evansville, IN',
  'Des Moines, IA', 'Cedar Rapids, IA', 'Davenport, IA',
  'Wichita, KS', 'Overland Park, KS', 'Kansas City, KS',
  'Louisville, KY', 'Lexington, KY',
  'New Orleans, LA', 'Baton Rouge, LA', 'Shreveport, LA',
  'Portland, ME', 'Augusta, ME',
  'Baltimore, MD', 'Rockville, MD', 'Annapolis, MD',
  'Boston, MA', 'Worcester, MA', 'Springfield, MA', 'Cambridge, MA',
  'Detroit, MI', 'Grand Rapids, MI', 'Ann Arbor, MI', 'Lansing, MI',
  'Minneapolis, MN', 'St. Paul, MN', 'Rochester, MN', 'Duluth, MN',
  'Jackson, MS', 'Gulfport, MS', 'Biloxi, MS',
  'Kansas City, MO', 'St. Louis, MO', 'Springfield, MO', 'Columbia, MO',
  'Billings, MT', 'Missoula, MT', 'Great Falls, MT',
  'Omaha, NE', 'Lincoln, NE',
  'Las Vegas, NV', 'Reno, NV', 'Henderson, NV',
  'Manchester, NH', 'Concord, NH',
  'Newark, NJ', 'Jersey City, NJ', 'Paterson, NJ', 'Trenton, NJ',
  'Albuquerque, NM', 'Santa Fe, NM', 'Las Cruces, NM',
  'New York City, NY', 'Buffalo, NY', 'Rochester, NY', 'Yonkers, NY',
  'Syracuse, NY', 'Albany, NY',
  'Charlotte, NC', 'Raleigh, NC', 'Greensboro, NC', 'Durham, NC',
  'Fargo, ND', 'Bismarck, ND',
  'Columbus, OH', 'Cleveland, OH', 'Cincinnati, OH', 'Toledo, OH', 'Akron, OH',
  'Oklahoma City, OK', 'Tulsa, OK', 'Norman, OK',
  'Portland, OR', 'Salem, OR', 'Eugene, OR',
  'Philadelphia, PA', 'Pittsburgh, PA', 'Allentown, PA', 'Erie, PA',
  'Providence, RI', 'Warwick, RI',
  'Columbia, SC', 'Charleston, SC', 'Greenville, SC',
  'Sioux Falls, SD', 'Rapid City, SD',
  'Memphis, TN', 'Nashville, TN', 'Knoxville, TN', 'Chattanooga, TN',
  'Dallas, TX', 'Houston, TX', 'San Antonio, TX', 'Austin, TX',
  'Fort Worth, TX', 'El Paso, TX', 'Arlington, TX', 'Corpus Christi, TX',
  'Lubbock, TX', 'Laredo, TX', 'Amarillo, TX',
  'Salt Lake City, UT', 'Provo, UT', 'Ogden, UT',
  'Burlington, VT', 'Montpelier, VT',
  'Virginia Beach, VA', 'Norfolk, VA', 'Richmond, VA', 'Arlington, VA',
  'Alexandria, VA', 'Roanoke, VA',
  'Seattle, WA', 'Spokane, WA', 'Tacoma, WA', 'Vancouver, WA',
  'Charleston, WV', 'Huntington, WV',
  'Milwaukee, WI', 'Madison, WI', 'Green Bay, WI',
  'Cheyenne, WY', 'Casper, WY',
  // Canada
  'Toronto, ON', 'Montreal, QC', 'Vancouver, BC', 'Calgary, AB',
  'Edmonton, AB', 'Ottawa, ON', 'Winnipeg, MB', 'Quebec City, QC',
  // Mexico
  'Mexico City, MX', 'Guadalajara, MX', 'Monterrey, MX', 'Tijuana, MX',
  // Europe
  'London, UK', 'Paris, France', 'Berlin, Germany', 'Madrid, Spain',
  'Rome, Italy', 'Amsterdam, Netherlands', 'Brussels, Belgium',
  'Vienna, Austria', 'Zurich, Switzerland', 'Stockholm, Sweden',
  'Oslo, Norway', 'Copenhagen, Denmark', 'Helsinki, Finland',
  'Lisbon, Portugal', 'Athens, Greece', 'Warsaw, Poland', 'Prague, Czech Republic',
  'Budapest, Hungary', 'Bucharest, Romania', 'Kiev, Ukraine',
  // Asia
  'Tokyo, Japan', 'Beijing, China', 'Shanghai, China', 'Hong Kong, China',
  'Seoul, South Korea', 'Mumbai, India', 'Delhi, India', 'Bangalore, India',
  'Singapore', 'Bangkok, Thailand', 'Kuala Lumpur, Malaysia',
  'Jakarta, Indonesia', 'Manila, Philippines', 'Dubai, UAE', 'Riyadh, Saudi Arabia',
  'Istanbul, Turkey', 'Karachi, Pakistan', 'Dhaka, Bangladesh',
  // Australia
  'Sydney, Australia', 'Melbourne, Australia', 'Brisbane, Australia',
  'Perth, Australia', 'Adelaide, Australia',
  // South America
  'São Paulo, Brazil', 'Rio de Janeiro, Brazil', 'Buenos Aires, Argentina',
  'Bogotá, Colombia', 'Lima, Peru', 'Santiago, Chile', 'Caracas, Venezuela',
  // Africa
  'Cairo, Egypt', 'Lagos, Nigeria', 'Nairobi, Kenya', 'Johannesburg, South Africa',
  'Cape Town, South Africa', 'Casablanca, Morocco', 'Accra, Ghana',
].sort();

// ── Component ─────────────────────────────────────────────
export default function CityAutocomplete({ id, name, value, onChange, placeholder }) {
  const [open,     setOpen]     = useState(false);
  const [query,    setQuery]    = useState(value || '');
  const [active,   setActive]   = useState(-1);
  const wrapRef  = useRef(null);
  const inputRef = useRef(null);
  const listRef  = useRef(null);

  // Keep internal query in sync when parent resets
  useEffect(() => { setQuery(value || ''); }, [value]);

  // Close on outside click
  useEffect(() => {
    const handler = (e) => {
      if (wrapRef.current && !wrapRef.current.contains(e.target)) setOpen(false);
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  // Scroll active item into view
  useEffect(() => {
    if (active >= 0 && listRef.current) {
      const item = listRef.current.children[active];
      item?.scrollIntoView({ block: 'nearest' });
    }
  }, [active]);

  const filtered = query.length >= 1
    ? CITIES.filter(c => c.toLowerCase().includes(query.toLowerCase())).slice(0, 8)
    : [];

  const select = (city) => {
    setQuery(city);
    setOpen(false);
    setActive(-1);
    onChange({ target: { name, value: city } });
  };

  const handleInput = (e) => {
    const v = e.target.value;
    setQuery(v);
    setOpen(true);
    setActive(-1);
    onChange({ target: { name, value: v } });
  };

  const handleKey = (e) => {
    if (!open || filtered.length === 0) return;
    if (e.key === 'ArrowDown') { e.preventDefault(); setActive(i => Math.min(i + 1, filtered.length - 1)); }
    if (e.key === 'ArrowUp')   { e.preventDefault(); setActive(i => Math.max(i - 1, 0)); }
    if (e.key === 'Enter' && active >= 0) { e.preventDefault(); select(filtered[active]); }
    if (e.key === 'Escape')    { setOpen(false); }
  };

  return (
    <div ref={wrapRef} style={{ position: 'relative' }}>
      <div style={{ position: 'relative' }}>
        <input
          ref={inputRef}
          id={id}
          name={name}
          type="text"
          value={query}
          onChange={handleInput}
          onFocus={() => query.length >= 1 && setOpen(true)}
          onKeyDown={handleKey}
          placeholder={placeholder}
          autoComplete="off"
          required
        />
        {/* Dropdown chevron */}
        <span style={{
          position: 'absolute', right: 12, top: '50%', transform: 'translateY(-50%)',
          color: open ? '#00d4ff' : '#1e4a64',
          fontSize: 11, pointerEvents: 'none',
          transition: 'color 0.2s, transform 0.2s',
          display: 'inline-block',
        }}>
          {open ? '▲' : '▼'}
        </span>
      </div>

      {open && filtered.length > 0 && (
        <ul ref={listRef} style={{
          position: 'absolute', zIndex: 9999,
          top: 'calc(100% + 6px)', left: 0, right: 0,
          background: '#030b16',
          border: '1px solid rgba(0, 212, 255, 0.3)',
          borderRadius: 10,
          maxHeight: 240, overflowY: 'auto',
          margin: 0, padding: 0, listStyle: 'none',
          boxShadow: '0 8px 40px rgba(0,0,0,0.7), 0 0 0 1px rgba(0,212,255,0.08)',
        }}>
          {filtered.map((city, i) => (
            <li
              key={city}
              onMouseDown={() => select(city)}
              onMouseEnter={() => setActive(i)}
              style={{
                padding: '10px 14px',
                fontSize: '0.88rem',
                fontFamily: 'Inter, sans-serif',
                cursor: 'pointer',
                borderBottom: '1px solid rgba(0,212,255,0.06)',
                color: i === active ? '#00d4ff' : '#c8e8f8',
                background: i === active ? 'rgba(0, 212, 255, 0.07)' : 'transparent',
                transition: 'background 0.15s, color 0.15s',
                display: 'flex', alignItems: 'center', gap: 8,
              }}
            >
              <span style={{
                color: i === active ? '#00d4ff' : '#1e4a64',
                fontSize: 10, flexShrink: 0,
              }}>◈</span>
              {/* Highlight matching part */}
              {highlightMatch(city, query)}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function highlightMatch(city, query) {
  if (!query) return city;
  const idx = city.toLowerCase().indexOf(query.toLowerCase());
  if (idx === -1) return city;
  return (
    <>
      {city.slice(0, idx)}
      <strong style={{ color: '#00d4ff' }}>{city.slice(idx, idx + query.length)}</strong>
      {city.slice(idx + query.length)}
    </>
  );
}
