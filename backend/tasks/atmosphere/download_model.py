from worker import app
from celery import group
from .download_forecast import download_forecast


@app.task()
def download_model(analysis_time):
    """Download a complete model run."""
    forecast_hours = [
        0, 3, 6, 9, 12,
        15, 18, 21, 24,
        27, 30, 33, 36,
        39, 42, 45, 48,
        51, 54, 57, 60,
        63, 66, 69, 72,
        75, 78, 81, 84,
        87, 90, 93, 96,
        99, 102, 105, 108,
        111, 114, 117, 120,
        123, 126, 129, 132,
        135, 138, 141, 144,
        147, 150, 153, 156,
        159, 162, 165, 168
    ]
    # Create the task group
    job = group(
        download_forecast.s(analysis_time, hour)
        for hour in forecast_hours)
    # Execute the group
    job.apply_async()