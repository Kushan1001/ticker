from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    RunRealtimeReportRequest,
    DateRange,
    Metric
)
from flask import Flask, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =  '/opt/render/project/src/service_account.json'

app = Flask(__name__)

def ga4_user_summary(property_id="YOUR-GA4-PROPERTY-ID"):
    client = BetaAnalyticsDataClient()

    lifetime_request = RunReportRequest(
        property=f"properties/{property_id}",
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="newUsers")
        ],
        date_ranges=[DateRange(start_date="2015-08-14", end_date="today")]
    )
    lifetime_response = client.run_report(lifetime_request)

    total_active = lifetime_response.rows[0].metric_values[0].value
    total_new = lifetime_response.rows[0].metric_values[1].value


    realtime_request = RunRealtimeReportRequest(
        property=f"properties/{property_id}",
        metrics=[Metric(name="activeUsers")]
    )
    realtime_response = client.run_realtime_report(realtime_request)
    current_active = realtime_response.rows[0].metric_values[0].value
    
    return total_active


@app.get('/ticker_count')
def ticker_count():
    total_active_users = ga4_user_summary('386796174')
    return jsonify({"total_active_users" : total_active_users}), 200


