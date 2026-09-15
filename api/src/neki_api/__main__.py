import asyncio
import sys

import uvicorn

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

uvicorn.run(
    "neki_api.main:create_app",
    factory=True,
    host="127.0.0.1",
    port=8000,
    proxy_headers=False,
    access_log=False,
)
