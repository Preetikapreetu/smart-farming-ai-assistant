import gradio as gr
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_recommendation(farmer_id):
    conn = sqlite3.connect("sustainable_farming_demo.db")
    cursor = conn.cursor()
    cursor.execute("SELECT recommendation FROM recommendations WHERE farmer_id = ? ORDER BY date DESC LIMIT 1", (farmer_id,))
    rec = cursor.fetchone()
    conn.close()
    return rec[0] if rec else "No recommendation found."

def show_weather_summary(location):
    conn = sqlite3.connect("sustainable_farming_demo.db")
    weather_df = pd.read_sql_query("SELECT * FROM weather WHERE location = ?", conn, params=(location,))
    conn.close()
    if weather_df.empty:
        return "No weather data found.", None
    fig, ax = plt.subplots()
    sns.lineplot(data=weather_df, x="date", y="rainfall_mm", marker="o", ax=ax)
    ax.set_title(f"Rainfall Trend in {location}")
    ax.set_ylabel("Rainfall (mm)")
    ax.set_xlabel("Date")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return "Weather data loaded!", fig

with gr.Blocks() as demo:
    gr.Markdown("## 🌾 Smart Farming AI Assistant Dashboard")
    with gr.Tab("📌 Get AI Recommendation"):
        farmer_input = gr.Number(label="Enter Farmer ID")
        rec_btn = gr.Button("Get Recommendation")
        rec_output = gr.Textbox(label="AI Recommendation")
        rec_btn.click(fn=get_recommendation, inputs=farmer_input, outputs=rec_output)
    with gr.Tab("🌧 Weather Summary"):
        location_input = gr.Textbox(label="Enter Location")
        weather_btn = gr.Button("Show Summary")
        weather_msg = gr.Textbox(label="Message")
        weather_plot = gr.Plot()
        weather_btn.click(fn=show_weather_summary, inputs=location_input, outputs=[weather_msg, weather_plot])

demo.launch()
