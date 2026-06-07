# Holiday Date Checker API

Check if dates fall on US federal holidays. Essential for business apps, scheduling tools, and payroll systems.

## Endpoints

### GET /health
Health check endpoint (no auth required).

### POST /check
Check if a specific date is a US federal holiday.

```bash
curl -X POST https://holiday-checker-pink.vercel.app/check \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_KEY" \
  -d '{"date": "2024-07-04"}'
```

**Response:**
```json
{
  "date": "2024-07-04",
  "formatted_date": "July 04, 2024",
  "is_holiday": true,
  "holiday_name": "Independence",
  "day_of_week": "Thursday"
}
```

### POST /month
Get all holidays in a specific month.

```bash
curl -X POST https://holiday-checker-pink.vercel.app/month \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_KEY" \
  -d '{"year": 2024, "month": 12}'
```

### POST /range
Get all holidays in a date range.

```bash
curl -X POST "https://holiday-checker-pink.vercel.app/range?start_date=2024-11-01&end_date=2024-12-31" \
  -H "X-API-Key: YOUR_KEY"
```

### GET /years/{year}
Get all holidays for a specific year.

```bash
curl https://holiday-checker-pink.vercel.app/years/2024 \
  -H "X-API-Key: YOUR_KEY"
```

## Holidays Covered

- New Year's Day (Jan 1)
- Martin Luther King Jr. Day (3rd Monday in January)
- Presidents' Day (3rd Monday in February)
- Memorial Day (Last Monday in May)
- Juneteenth (June 19)
- Independence Day (July 4)
- Labor Day (1st Monday in September)
- Columbus Day (2nd Monday in October)
- Veterans Day (November 11)
- Thanksgiving (4th Thursday in November)
- Christmas Day (December 25)

## Monetize

List on RapidAPI for $15-29/month. Target: payroll services, HR software, scheduling apps, small business tools.

## Postman
[![Run in Postman](https://run.pstmn.io/button.svg)](https://raw.githubusercontent.com/BT-Builds/holiday-checker/main/postman_collection.json)
