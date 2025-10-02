# app/api/events_sse.py
# SSE endpoint for kiosks. Push-only (server -> client) event stream.
# Auth via your existing kiosk JWT dependency.
#
# Notes:
# - Native EventSource cannot set Authorization header. If you use plain
#   EventSource in the browser, consider: (a) cookie-based auth, or
#   (b) a tiny EventSource polyfill that adds the header, or
#   (c) later we can add a `?token=` fallback here.
# - We send heartbeat comments (": ping") every 15s to keep proxies/load
#   balancers from closing the idle connection.
# - Each message is JSON encoded and sent as a standard SSE "data:" frame.

import asyncio
import json
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import StreamingResponse

from ..auth.kiosk_dependencies import get_current_kiosk_user, get_current_kiosk_token_data
from ..database.models import User
from ..websockets.event_bus import bus

router = APIRouter(prefix="/api/kiosk", tags=["Kiosk Events"])


@router.get("/events")
async def kiosk_events_sse(
    request: Request,
    current_user: User = Depends(get_current_kiosk_user),
    _token=Depends(get_current_kiosk_token_data),  # forces token validation
):
    """
    Long-lived SSE connection for a kiosk.
    We route events by kiosk username (unique per kiosk account).

    Client usage example (with header-capable polyfill):
        const es = new EventSourcePolyfill('/api/kiosk/events', {
          headers: { Authorization: 'Bearer <JWT>' }
        });
        es.onmessage = (ev) => { const msg = JSON.parse(ev.data); ... };

    IMPORTANT:
    - This endpoint never completes under normal conditions.
    - Client should auto-reconnect on network errors.
    """
    kiosk_username = current_user.username

    async def event_stream():
        # Optional initial "retry" hint (ms) for client auto-reconnect
        yield b"retry: 3000\n\n"

        async def heartbeat():
            # SSE "comment" lines are valid and ignored by clients
            while True:
                yield b": ping\n\n"
                await asyncio.sleep(15)

        hb_iter = heartbeat().__aiter__()
        sub_iter = bus.subscribe(kiosk_username).__aiter__()

        try:
            while True:
                # Wait for either a new event or the next heartbeat tick
                done, _ = await asyncio.wait(
                    {
                        asyncio.create_task(sub_iter.__anext__()),
                        asyncio.create_task(hb_iter.__anext__()),
                    },
                    return_when=asyncio.FIRST_COMPLETED,
                )

                # Write all ready chunks
                for task in done:
                    chunk = task.result()
                    if isinstance(chunk, (bytes, bytearray)):
                        # Heartbeat frame (already properly formatted)
                        yield chunk
                    else:
                        # Normal data message as JSON
                        payload = json.dumps(chunk, ensure_ascii=False).encode("utf-8")
                        yield b"data: " + payload + b"\n\n"

                # Stop if client closed the connection
                if await request.is_disconnected():
                    break

        except asyncio.CancelledError:
            # Server/app shutdown or task cancellation — just exit silently
            pass

    headers = {
        "Content-Type": "text/event-stream; charset=utf-8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        # If you run behind nginx, consider:  "X-Accel-Buffering": "no"
    }
    return StreamingResponse(event_stream(), headers=headers)