# Tech Momentum Arbitrage Engine - Web Dashboard

Beautiful, responsive web interface for the Tech Momentum Arbitrage Engine.

## 🚀 Quick Start

### Option 1: Simple Python Server (Recommended)

```bash
# From the web directory
python3 server.py

# Open browser to: http://localhost:8000/index.html
```

### Option 2: Direct File Access

Simply open `index.html` in your web browser. Note: The data loads from the `outputs/reports/` directory, so make sure you've run the engine first to generate the reports.

## ✨ Features

- **Clean, Modern Design** - Sharp UI that's intuitive and not overwhelming
- **Real-time Data** - Loads live data from generated JSON reports
- **Responsive** - Works beautifully on desktop, tablet, and mobile
- **Interactive Tables** - Sortable, filterable company signals
- **Visual Momentum Scoring** - Clear visual representation of Hype vs Build
- **Bottleneck Discovery Cards** - Easy-to-scan emerging opportunities

## 📊 Dashboard Components

### 1. Executive Summary Stats
- Total signals generated
- High-conviction play count
- Average momentum score
- Active sectors

### 2. Top 10 Momentum Plays Table
- Company ranking by conviction
- Momentum scores with visual progress bars
- Hype/Build split view
- Moat scores
- Buy/Sell recommendations

### 3. Emerging Bottlenecks Grid
- Critical infrastructure opportunities
- Confidence scoring
- Evidence bullets
- Private companies & public proxies

## 🎨 Design Philosophy

**Not Busy, Not Simple - Perfectly Balanced**

- Clean white space for breathing room
- Strategic use of color for emphasis
- Hierarchical typography for easy scanning
- Subtle shadows and borders for depth
- Smooth transitions for polish

## 🔧 Technical Details

- **Pure HTML/CSS/JavaScript** - No build step required
- **Standalone** - Works offline with generated data
- **Lightweight** - Fast load times, no dependencies
- **Accessible** - Semantic HTML, proper contrast ratios
- **Modern CSS** - Flexbox, Grid, CSS Variables

## 📁 File Structure

```
web/
├── index.html       # Main dashboard (all-in-one file)
├── server.py        # Simple Python HTTP server
└── README.md        # This file
```

## 🎯 Usage Flow

1. **Generate Data** - Run the main engine to create JSON reports:
   ```bash
   PYTHONPATH=/home/user/Tsunami python src/engine.py
   ```

2. **Start Server** - Launch the web dashboard:
   ```bash
   cd web && python3 server.py
   ```

3. **View Dashboard** - Open http://localhost:8000/index.html in your browser

4. **Explore Signals** - Navigate through top plays, bottlenecks, and insights

## 🔄 Updating Data

The dashboard automatically loads the latest data from:
```
../outputs/reports/weekly_alpha_report_YYYYMMDD.json
```

To update:
1. Run the engine again to generate new reports
2. Refresh your browser
3. New data appears instantly

## 💡 Tips

- **Hover Effects**: Hover over table rows and cards for interactivity
- **Responsive Design**: Try resizing your browser - works at all sizes
- **Print-Friendly**: Dashboard is optimized for printing/PDF export
- **Fast Navigation**: Use browser search (Ctrl+F) to find specific companies

## 🎨 Color Scheme

- **Primary Blue**: `#2563eb` - Actions, momentum bars
- **Success Green**: `#10b981` - High conviction, positive metrics
- **Warning Amber**: `#f59e0b` - Medium priority items
- **Danger Red**: `#ef4444` - Critical priority, bubble risks
- **Gray Scale**: Professional, clean backgrounds and text

## 📱 Browser Support

- Chrome/Edge 90+
- Firefox 90+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🚀 Future Enhancements

Potential additions (not yet implemented):
- Real-time data streaming via WebSocket
- Interactive charts (Chart.js/D3.js)
- Company detail modal dialogs
- Export to PDF/Excel
- Dark mode toggle
- Custom filtering and sorting
- Historical trend views

---

**Status**: Production-Ready ✅
**Version**: 1.0.0
**Last Updated**: November 5, 2025
