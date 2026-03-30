{
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api/index.py" },
    { "source": "/dashboard", "destination": "/public/dashboard.html" },
    { "source": "/(.*)", "destination": "/public/index.html" }
  ]
}
