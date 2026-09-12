"""
OpsPilot AI - FastAPI Compatibility Adapter
Author: Nivesh Kumar Meena
Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.
"""

try:
    from fastapi import APIRouter, Depends, HTTPException, Query, status, Header, Security
except ImportError:
    class APIRouter:
        def __init__(self, prefix="", tags=None):
            self.prefix = prefix
            self.tags = tags or []
            self.routes = []

        def get(self, path, **kwargs):
            def decorator(f):
                self.routes.append(("GET", f"{self.prefix}{path}", f))
                return f
            return decorator

        def post(self, path, **kwargs):
            def decorator(f):
                self.routes.append(("POST", f"{self.prefix}{path}", f))
                return f
            return decorator

        def put(self, path, **kwargs):
            def decorator(f):
                self.routes.append(("PUT", f"{self.prefix}{path}", f))
                return f
            return decorator

        def delete(self, path, **kwargs):
            def decorator(f):
                self.routes.append(("DELETE", f"{self.prefix}{path}", f))
                return f
            return decorator

    def Depends(f=None): return f
    def Query(default=None, **kwargs): return default
    def Header(default=None, **kwargs): return default
    def Security(f=None, **kwargs): return f

    class HTTPException(Exception):
        def __init__(self, status_code=400, detail=""):
            self.status_code = status_code
            self.detail = detail
            super().__init__(detail)

    class status:
        HTTP_401_UNAUTHORIZED = 401
        HTTP_403_FORBIDDEN = 403
        HTTP_404_NOT_FOUND = 404
