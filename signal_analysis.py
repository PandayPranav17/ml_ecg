import pandas as pd
import numpy as np
import asyncio
from fastapi import FastAPI, WebSocket
from scipy.signal import butter, filtfilt
from fastapi.responses import FileResponse

app = FastAPI()

# ------------------------
# Load ECG CSV
# ------------------------
file_name = '/Users/pranavpanday/Downloads/100_ekg.csv'
df = pd.read_csv(file_name)
y = df.iloc[:, 1].values
fs = 360

# ------------------------
# Bandpass Filter
# ------------------------
def bandpass_filter(signal, fs=360, lowcut=0.5, highcut=40.0, order=3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, signal)

y_filtered = bandpass_filter(y)

# ------------------------
# WebSocket Endpoint
# ------------------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    chunk_size = 20
    delay = chunk_size / fs

    for i in range(0, len(y_filtered), chunk_size):
        chunk = y_filtered[i:i+chunk_size]
        time_chunk = np.arange(i, i+len(chunk)) / fs

        await websocket.send_json({
            "time": time_chunk.tolist(),
            "voltage": chunk.tolist()
        })

        await asyncio.sleep(delay)

# ------------------------
# Serve HTML File
# ------------------------
@app.get("/")
async def get_html():
    return FileResponse("display.html")
