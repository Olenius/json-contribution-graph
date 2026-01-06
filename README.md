# JSON Contribution Graph

Generator for HTML page with GitHub-style contribution graph based on JSON data.

## Project Structure

```
JsonContributionGraph/
├── generate.py          # HTML generation script
├── requirements.txt     # Python dependencies
├── .env                 # Configuration (create from .env.example)
├── .env.example         # Configuration example
├── data.json           # Event data
├── styles.css          # CSS styles
├── scripts.js          # JavaScript for tooltip
├── index.html          # Generated HTML page
└── venv/               # Python virtual environment
```

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy `.env.example` to `.env` and configure parameters:

```bash
cp .env.example .env
```

Parameters in `.env`:
- `TITLE` - page title
- `DESCRIPTION` - description below the title
- `JSON_FILE_PATH` - path to JSON file with data
- `YEAR` - year to display (e.g., 2026)
- `START_DAY` - week start day: `monday` or `sunday`

### 3. Prepare Data

Edit `data.json` with your events and dates:

```json
{
  "events": [
    {
      "name": "Math",
      "code": "m",
      "color": "#1e88e5"
    },
    {
      "name": "Video",
      "code": "v",
      "color": "#43a047"
    }
  ],
  "dates": [
    {
      "date": "2026-01-05",
      "codes": ["m", "m", "v"]
    },
    {
      "date": "2026-01-04",
      "codes": ["m"]
    }
  ]
}
```

#### Data Format

**events** - list of event types:
- `name` - event name (displayed in tooltip)
- `code` - short event code (used in dates)
- `color` - primary color in hex format (#RRGGBB)

**dates** - list of dates with activity:
- `date` - date in YYYY-MM-DD format
- `codes` - array of event codes for this day (can repeat)

### 4. Generate HTML

```bash
# Activate virtual environment (if not activated)
source venv/bin/activate

# Run generator
python3 generate.py
```

After successful generation, open `index.html` in your browser.

## Features

### Visualization

1. **Same event multiple times in one day**
   - Event color with increasing opacity
   - 1 time = 0.4 opacity
   - 2 times = 0.6 opacity
   - 3 times = 0.8 opacity
   - 4+ times = 1.0 opacity (fully opaque)

2. **Different events on the same day**
   - Diagonal stripes
   - Stripe width proportional to event count
   - Example: 2× "Math" + 1× "Video" = 2/3 first color + 1/3 second color

3. **Empty days**
   - Gray color like GitHub (#ebedf0)

### Tooltip

When hovering over a square, it shows:
- Date (e.g., "January 5, 2026")
- List of events with count (e.g., "Math × 2")

### Responsiveness

- Automatic adjustment of square sizes on mobile devices
- Correct display of all 365/366 days of the year
- Horizontal scrolling when needed

## Usage Examples

### Study Tracking

```json
{
  "events": [
    {"name": "Mathematics", "code": "m", "color": "#1e88e5"},
    {"name": "Physics", "code": "p", "color": "#e53935"},
    {"name": "Programming", "code": "c", "color": "#43a047"}
  ],
  "dates": [
    {"date": "2026-01-05", "codes": ["m", "m", "c"]},
    {"date": "2026-01-04", "codes": ["p", "c", "c"]}
  ]
}
```

### Habit Tracking

```json
{
  "events": [
    {"name": "Sports", "code": "s", "color": "#ff6f00"},
    {"name": "Reading", "code": "r", "color": "#7b1fa2"},
    {"name": "Meditation", "code": "m", "color": "#0288d1"}
  ],
  "dates": [
    {"date": "2026-01-05", "codes": ["s", "r", "m"]},
    {"date": "2026-01-04", "codes": ["r", "r"]}
  ]
}
```

## Technical Details

- **Python**: 3.7+
- **Dependencies**: python-dotenv
- **Browsers**: Modern browsers with CSS Grid and ES6+ support

## License

MIT
