from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio, subprocess

app=FastAPI()
html="""<html><body><pre id="log"></pre><script>
ws=new WebSocket("ws://localhost:8000/ws/logs");
ws.onmessage=e=>{document.getElementById("log").innerText+=e.data;}
</script></body></html>"""

@app.get("/")
def get(): return HTMLResponse(html)

@app.websocket("/ws/logs")
async def ws(ws:WebSocket):
    await ws.accept()
    proc=await asyncio.create_subprocess_exec("python","main.py",stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.STDOUT)
    while True:
        line=await proc.stdout.readline()
        if not line: break
        await ws.send_text(line.decode())
    await proc.wait()
