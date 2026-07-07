"""
mock_server.py — 模拟"外部数据接收服务器"。
全程仅监听 localhost，不涉及任何真实网络通信。
"""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

from payloads import PAYLOAD_WEBPAGES

app = FastAPI(title="Prebunking Experiment Mock Server")

# 日志文件路径
EGRESS_LOG = Path(__file__).parent / "results" / "egress_log.jsonl"


def ensure_log_dir():
    EGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)


@app.on_event("startup")
async def startup():
    ensure_log_dir()


@app.post("/collect")
async def collect_data(request: Request):
    """接收外发数据，记录到 JSONL 日志。"""
    ensure_log_dir()
    try:
        body = await request.json()
    except Exception:
        body = {"raw": await request.body()}

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "experiment_id": body.get("experiment_id", "unknown"),
        "payload": body,
        "client_ip": request.client.host if request.client else "unknown",
    }

    with open(EGRESS_LOG, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return JSONResponse({"status": "received"})


@app.get("/webpage/{variant}")
async def serve_webpage(variant: str):
    """返回指定 variant 的注入网页内容。"""
    content = PAYLOAD_WEBPAGES.get(variant)
    if content is None:
        return HTMLResponse(
            f"<html><body><h1>404</h1><p>Unknown variant: {variant}</p></body></html>",
            status_code=404,
        )
    return HTMLResponse(content)


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
