from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
from pathlib import Path
import subprocess

app=FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

@app.get("/api/incidents")
def list_incidents():
    return [d.name for d in sorted(Path("output").glob("incident_*")) if d.is_dir()]

@app.post("/api/incidents/{name}/delete")
def delete(name:str):
    p=Path("output")/name
    if p.exists(): shutil.rmtree(p); return{"msg":"deleted"}
    raise HTTPException(404,"Not found")

@app.post("/api/incidents/{name}/run")
def run(name:str):
    res=subprocess.run(["python","main.py"],capture_output=True,text=True)
    return {"output":res.stdout}
