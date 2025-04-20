from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app=FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"])

@app.get("/api/incidents")
def get_incidents():
    conn=sqlite3.connect("incident_logs.db")
    rows=conn.execute("SELECT id,incident_name,timestamp,modules,secure FROM incidents ORDER BY id DESC").fetchall()
    conn.close()
    return [{"id":r[0],"name":r[1],"timestamp":r[2],"modules":r[3].split(","),"secure":bool(r[4])} for r in rows]
