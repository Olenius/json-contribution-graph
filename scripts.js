/**
 * Tooltip functionality for contribution graph
 */

document.addEventListener('DOMContentLoaded', function() {
    const tooltip = document.getElementById('tooltip');
    const days = document.querySelectorAll('.day:not(.day-empty)');
    
    // Month names in English
    const monthNames = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];
    
    /**
     * Format date in readable format
     * @param {string} dateStr - Date string in YYYY-MM-DD format
     * @returns {string} Formatted date string
     */
    function formatDate(dateStr) {
        const date = new Date(dateStr + 'T00:00:00');
        const day = date.getDate();
        const month = monthNames[date.getMonth()];
        const year = date.getFullYear();
        
        return `${day} ${month} ${year}`;
    }
    
    /**
     * Format events for tooltip display
     * @param {Object} events - Object with event names as keys and counts as values
     * @returns {string} HTML string for events display
     */
    function formatEvents(events) {
        if (!events || Object.keys(events).length === 0) {
            return '<div class="tooltip-empty">No events</div>';
        }
        
        const eventList = Object.entries(events).map(([name, count]) => {
            if (count > 1) {
                return `<div class="tooltip-event">${name} × ${count}</div>`;
            } else {
                return `<div class="tooltip-event">${name}</div>`;
            }
        });
        
        return `<div class="tooltip-events">${eventList.join('')}</div>`;
    }
    
    /**
     * Show tooltip
     * @param {Event} event - Mouse event
     */
    function showTooltip(event) {
        const day = event.currentTarget;
        const date = day.getAttribute('data-date');
        const eventsStr = day.getAttribute('data-events');
        
        if (!date) return;
        
        // Parse events
        let events = {};
        try {
            events = JSON.parse(eventsStr);
        } catch (e) {
            events = {};
        }
        
        // Build tooltip content
        const formattedDate = formatDate(date);
        const eventsHtml = formatEvents(events);
        
        tooltip.innerHTML = `
            <div class="tooltip-date">${formattedDate}</div>
            ${eventsHtml}
        `;
        
        // Position tooltip
        positionTooltip(event);
        
        // Show tooltip
        tooltip.classList.add('visible');
    }
    
    /**
     * Position tooltip near cursor
     * @param {Event} event - Mouse event
     */
    function positionTooltip(event) {
        const offset = 15;
        let x = event.clientX + offset;
        let y = event.clientY + offset;
        
        // Get tooltip dimensions
        const tooltipRect = tooltip.getBoundingClientRect();
        const tooltipWidth = tooltipRect.width;
        const tooltipHeight = tooltipRect.height;
        
        // Check if tooltip goes off right edge
        if (x + tooltipWidth > window.innerWidth) {
            x = event.clientX - tooltipWidth - offset;
        }
        
        // Check if tooltip goes off bottom edge
        if (y + tooltipHeight > window.innerHeight) {
            y = event.clientY - tooltipHeight - offset;
        }
        
        // Ensure tooltip doesn't go off left or top edge
        x = Math.max(offset, x);
        y = Math.max(offset, y);
        
        tooltip.style.left = x + 'px';
        tooltip.style.top = y + 'px';
    }
    
    /**
     * Hide tooltip
     */
    function hideTooltip() {
        tooltip.classList.remove('visible');
    }
    
    /**
     * Update tooltip position on mouse move
     * @param {Event} event - Mouse event
     */
    function updateTooltipPosition(event) {
        if (tooltip.classList.contains('visible')) {
            positionTooltip(event);
        }
    }
    
    // Attach event listeners to all day cells
    days.forEach(day => {
        day.addEventListener('mouseenter', showTooltip);
        day.addEventListener('mousemove', updateTooltipPosition);
        day.addEventListener('mouseleave', hideTooltip);
    });
    
    // Hide tooltip when scrolling
    window.addEventListener('scroll', hideTooltip);
});
