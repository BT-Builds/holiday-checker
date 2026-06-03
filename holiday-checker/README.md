# Holiday Date Checker API

Check if dates fall on US federal holidays. Essential for business apps, scheduling tools, and payroll systems.

## Endpoints

### GET /health
Health check endpoint (no auth required).

### POST /check
Check if a specific date is a US federal holiday.

```bash
curl -X POST https://holiday-checker.vercel.app/check \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_KEY" \
  -d '{"date": "2024-07-04"}'
```

### POST /month
Get all holidays in a specific month.

### POST /range
Get all holidays in a date range.

### GET /years/{year}
Get all holidays for a specific year.

## Holidays Covered

- New Year's Day
- Martin Luther King Jr. Day
- Presidents' Day  
- Memorial Day
- Juneteenth
- Independence Day
- Labor Day
- Columbus Day
- Veterans Day
- Thanksgiving
- Christmas Day