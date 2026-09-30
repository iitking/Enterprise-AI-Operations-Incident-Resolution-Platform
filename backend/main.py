"""
OpsPilot AI - Enterprise AI Operations & Incident Resolution Platform
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

import os
import sys
from contextlib import asynccontextmanager

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.config import settings
from backend.models.database import engine, Base
from backend.api.auth_routes import router as auth_router
from backend.api.incident_routes import router as incident_router, simulate_payment_api_incident
from backend.api.approval_routes import router as approval_router
from backend.api.webhook_routes import router as webhook_router
from backend.api.rag_routes import router as rag_router
from backend.api.service_routes import router as service_router
from backend.api.analytics_routes import router as analytics_router
from backend.tools.mcp_server import mcp_server

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse, JSONResponse
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

if HAS_FASTAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Create DB schema tables
        Base.metadata.create_all(bind=engine)
        # Automatically seed the benchmark P1 payment-api incident on startup
        try:
            simulate_payment_api_incident()
        except Exception as e:
            print(f"Initial seed warning: {e}")
        yield

    app = FastAPI(
        title=settings.APP_NAME,
        description=(
            "OpsPilot AI is an autonomous multi-agent AI platform for enterprise incident investigation, "
            "root-cause analysis, workflow automation, and human-approved remediation.\n\n"
            "**Author & Creator:** Nivesh Kumar Meena\n"
            "**Copyright © 2026 Nivesh Kumar Meena. All Rights Reserved.**"
        ),
        version="1.0.0",
        lifespan=lifespan
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API Routers
    app.include_router(auth_router)
    app.include_router(incident_router)
    app.include_router(approval_router)
    app.include_router(webhook_router)
    app.include_router(rag_router)
    app.include_router(service_router)
    app.include_router(analytics_router)

    @app.get("/health")
    def health_check():
        return {
            "status": "healthy",
            "app": settings.APP_NAME,
            "author": settings.PROJECT_AUTHOR,
            "environment": settings.APP_ENV,
            "version": "1.0.0"
        }

    @app.get("/api/mcp/tools")
    def get_mcp_tools():
        """MCP endpoint returning tool schema declarations."""
        return mcp_server.list_tools()

    # Mount frontend if build directory exists
    frontend_dist_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
    frontend_static_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "static")

    if os.path.exists(frontend_dist_path):
        app.mount("/", StaticFiles(directory=frontend_dist_path, html=True), name="frontend")
    elif os.path.exists(frontend_static_path):
        app.mount("/", StaticFiles(directory=frontend_static_path, html=True), name="frontend")

else:
    # Minimal fallback dummy app so modules can import backend.main safely
    class DummyApp:
        def __init__(self):
            self.routes = []
        def get(self, *args, **kwargs): return lambda f: f
        def post(self, *args, **kwargs): return lambda f: f
        def include_router(self, *args, **kwargs): pass
        def add_middleware(self, *args, **kwargs): pass
        def mount(self, *args, **kwargs): pass
    app = DummyApp()

if __name__ == "__main__":
    if not HAS_FASTAPI:
        print("=" * 80)
        print("🚀 OpsPilot AI - Enterprise AI Operations & Incident Resolution Platform")
        print("Author: Nivesh Kumar Meena | All Rights Reserved © 2026")
        print("=" * 80)
        print("[NOTICE] FastAPI & Uvicorn are not installed in the active environment.")
        print("To start the full production server, please install dependencies:")
        print("  pip install -r requirements.txt")
        print("  python3 backend/main.py")
        print("\nAll unit tests and benchmarks run out-of-the-box with standard library:")
        print("  python3 evaluation/benchmarks/benchmark_runner.py")
        print("  python3 tests/test_agents.py")
        print("=" * 80)
    else:
        import uvicorn
        uvicorn.run("backend.main:app", host="0.0.0.0", port=settings.APP_PORT, reload=True)

