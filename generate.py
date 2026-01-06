#!/usr/bin/env python3
"""
JSON Contribution Graph Generator
Generates an HTML page with a GitHub-style contribution graph from JSON data.
"""

import os
import json
from datetime import datetime, timedelta
from collections import Counter
from dotenv import load_dotenv


def load_config():
    """Load configuration from .env file."""
    load_dotenv()
    
    config = {
        'title': os.getenv('TITLE', 'Contribution Graph'),
        'description': os.getenv('DESCRIPTION', ''),
        'json_file_path': os.getenv('JSON_FILE_PATH', 'data.json'),
        'year': int(os.getenv('YEAR', datetime.now().year)),
        'start_day': os.getenv('START_DAY', 'monday').lower()
    }
    
    if config['start_day'] not in ['monday', 'sunday']:
        raise ValueError("START_DAY must be 'monday' or 'sunday'")
    
    return config


def load_data(json_file_path):
    """Load events and dates from JSON file."""
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create event lookup dictionary
    events_lookup = {event['code']: event for event in data['events']}
    
    # Parse dates and group by date
    dates_data = {}
    for entry in data['dates']:
        date = entry['date']
        codes = entry['codes']
        dates_data[date] = codes
    
    return events_lookup, dates_data


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color."""
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def calculate_day_style(codes, events_lookup):
    """
    Calculate the style for a day based on its event codes.
    Returns a tuple of (background_style, event_counts_dict)
    """
    if not codes:
        # Empty day - GitHub gray
        return 'background-color: #ebedf0;', {}
    
    # Count occurrences of each event code
    code_counts = Counter(codes)
    unique_events = list(code_counts.keys())
    
    # Get event names for tooltip
    event_counts = {events_lookup[code]['name']: count for code, count in code_counts.items()}
    
    if len(unique_events) == 1:
        # Single event type - use opacity based on count
        event_code = unique_events[0]
        event = events_lookup[event_code]
        count = code_counts[event_code]
        
        # Calculate opacity: 0.4 for 1, 0.6 for 2, 0.8 for 3, 1.0 for 4+
        opacity = min(0.4 + (count * 0.2), 1.0)
        
        color = event['color']
        r, g, b = hex_to_rgb(color)
        style = f'background-color: rgba({r}, {g}, {b}, {opacity});'
        
        return style, event_counts
    
    else:
        # Multiple event types - create diagonal stripes
        total_count = sum(code_counts.values())
        
        # Calculate stripe percentages
        gradients = []
        cumulative_percent = 0
        
        for event_code in unique_events:
            event = events_lookup[event_code]
            count = code_counts[event_code]
            percent = (count / total_count) * 100
            
            color = event['color']
            r, g, b = hex_to_rgb(color)
            
            # Calculate opacity based on average count
            avg_opacity = min(0.4 + (count * 0.15), 0.9)
            
            color_rgba = f'rgba({r}, {g}, {b}, {avg_opacity})'
            
            gradients.append({
                'color': color_rgba,
                'start': cumulative_percent,
                'end': cumulative_percent + percent
            })
            
            cumulative_percent += percent
        
        # Build repeating diagonal gradient
        gradient_stops = []
        stripe_size = 10  # pixels for stripe width
        
        for g in gradients:
            gradient_stops.append(f"{g['color']} {g['start']}%")
            gradient_stops.append(f"{g['color']} {g['end']}%")
        
        gradient_str = ', '.join(gradient_stops)
        style = f'background: repeating-linear-gradient(45deg, {gradient_str});'
        
        return style, event_counts


def generate_calendar_grid(year, start_day, dates_data, events_lookup):
    """Generate the calendar grid data for the entire year."""
    # Determine first day of year
    first_day = datetime(year, 1, 1)
    
    # Determine if leap year
    is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    days_in_year = 366 if is_leap else 365
    
    # Generate all days in the year
    days = []
    for day_offset in range(days_in_year):
        current_date = first_day + timedelta(days=day_offset)
        date_str = current_date.strftime('%Y-%m-%d')
        
        # Get codes for this date
        codes = dates_data.get(date_str, [])
        
        # Calculate style and event counts
        style, event_counts = calculate_day_style(codes, events_lookup)
        
        days.append({
            'date': date_str,
            'date_obj': current_date,
            'style': style,
            'event_counts': event_counts
        })
    
    # Organize into weeks
    # Determine the day of week for Jan 1
    jan_1_weekday = first_day.weekday()  # 0=Monday, 6=Sunday
    
    # Adjust based on start_day preference
    if start_day == 'sunday':
        # Convert: Python's Monday=0 to Sunday=0
        jan_1_weekday = (jan_1_weekday + 1) % 7
    
    # Add empty cells at the beginning if needed
    grid = [None] * jan_1_weekday + days
    
    return grid


def generate_html(config, grid, events_lookup):
    """Generate the HTML content."""
    title = config['title']
    description = config['description']
    year = config['year']
    
    # Calculate number of weeks (rounded up)
    num_cells = len(grid)
    num_weeks = (num_cells + 6) // 7
    
    # Calculate total event counts
    total_event_counts = {}
    for day_data in grid:
        if day_data is not None:
            for event_name, count in day_data['event_counts'].items():
                if event_name not in total_event_counts:
                    total_event_counts[event_name] = 0
                total_event_counts[event_name] += count
    
    # Build the grid HTML
    grid_html = []
    
    # Create cells
    for idx, day_data in enumerate(grid):
        if day_data is None:
            # Empty cell
            grid_html.append('<div class="day day-empty"></div>')
        else:
            date = day_data['date']
            style = day_data['style']
            event_counts = day_data['event_counts']
            
            # Format event counts for data attribute
            events_str = json.dumps(event_counts) if event_counts else '{}'
            
            grid_html.append(
                f'<div class="day" data-date="{date}" data-events=\'{events_str}\' style="{style}"></div>'
            )
    
    grid_cells = '\n            '.join(grid_html)
    
    # Build event statistics HTML
    stats_html = []
    
    # Find event colors by matching names with codes
    event_colors = {}
    for event_code, event_data in events_lookup.items():
        event_colors[event_data['name']] = event_data['color']
    
    # Sort by count descending
    sorted_events = sorted(total_event_counts.items(), key=lambda x: x[1], reverse=True)
    
    for event_name, count in sorted_events:
        color = event_colors.get(event_name, '#666')
        stats_html.append(
            f'<div class="stat-item">'
            f'<span class="stat-color" style="background-color: {color};"></span>'
            f'<span class="stat-name">{event_name}</span>'
            f'<span class="stat-count">{count}</span>'
            f'</div>'
        )
    
    stats_items = '\n                '.join(stats_html) if stats_html else '<p class="no-stats">No activity</p>'
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>{title}</h1>
            <p class="description">{description}</p>
        </header>
        
        <div class="graph-wrapper">
            <div class="graph">
                {grid_cells}
            </div>
        </div>
        
        <div class="statistics">
            <h2 class="stats-title">Event Statistics</h2>
            <div class="stats-list">
                {stats_items}
            </div>
        </div>
        
        <footer>
            <p class="year-label">{year}</p>
        </footer>
    </div>
    
    <div id="tooltip" class="tooltip"></div>
    
    <script src="scripts.js"></script>
</body>
</html>"""
    
    return html_content


def main():
    """Main function to generate the HTML page."""
    try:
        # Load configuration
        config = load_config()
        print(f"📋 Configuration loaded")
        print(f"   Title: {config['title']}")
        print(f"   Year: {config['year']}")
        print(f"   Start day: {config['start_day']}")
        
        # Load data
        events_lookup, dates_data = load_data(config['json_file_path'])
        print(f"📊 Data loaded")
        print(f"   Events: {len(events_lookup)}")
        print(f"   Dates with activity: {len(dates_data)}")
        
        # Generate calendar grid
        grid = generate_calendar_grid(
            config['year'],
            config['start_day'],
            dates_data,
            events_lookup
        )
        print(f"📅 Calendar grid generated ({len(grid)} cells)")
        
        # Generate HTML
        html_content = generate_html(config, grid, events_lookup)
        
        # Write to file
        output_file = 'index.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML generated successfully: {output_file}")
        
    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}")
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON - {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == '__main__':
    main()
