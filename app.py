from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    RunRealtimeReportRequest,
    DateRange,
    Metric
)
from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/etc/secrets/service_account.json'

app = Flask(__name__)
CORS(app)

def ga4_user_summary(property_id="YOUR-GA4-PROPERTY-ID"):
    client = BetaAnalyticsDataClient()

    # Lifetime total users
    lifetime_request = RunReportRequest(
        property=f"properties/{property_id}",
        metrics=[
            Metric(name="totalUsers"),   # ✅ total unique users since inception
            Metric(name="activeUsers"),
            Metric(name="newUsers")
        ],
        date_ranges=[DateRange(start_date="2020-01-01", end_date="today")]
    )

    lifetime_response = client.run_report(lifetime_request)

    total_users = lifetime_response.rows[0].metric_values[0].value
    active_users = lifetime_response.rows[0].metric_values[1].value
    total_users = 16400000 + int(active_users)
    new_users = lifetime_response.rows[0].metric_values[2].value

    # Real-time currently active users
    realtime_request = RunRealtimeReportRequest(
        property=f"properties/{property_id}",
        metrics=[Metric(name="activeUsers")]
    )
    realtime_response = client.run_realtime_report(realtime_request)
    current_active = realtime_response.rows[0].metric_values[0].value

    return {
        "total_users": total_users
    }

@app.get('/ticker_count')
def ticker_count():
    summary = ga4_user_summary('509714378')
    return jsonify(summary), 200

