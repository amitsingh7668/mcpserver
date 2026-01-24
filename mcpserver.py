from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from typing import Dict, Any
import inspect
import json

app = FastAPI(title="My MCP Server")

# Tool registry
TOOLS = {}

def register_tool(func):
    """Register a function as an MCP tool"""
    sig = inspect.signature(func)
    
    # Build input schema from function signature
    properties = {}
    required = []
    
    for param_name, param in sig.parameters.items():
        param_type = "string"
        if param.annotation == int:
            param_type = "integer"
        elif param.annotation == float:
            param_type = "number"
        elif param.annotation == bool:
            param_type = "boolean"
            
        properties[param_name] = {"type": param_type}
        if param.default == inspect.Parameter.empty:
            required.append(param_name)
    
    TOOLS[func.__name__] = {
        "name": func.__name__,
        "description": func.__doc__ or "",
        "inputSchema": {
            "type": "object",
            "properties": properties,
            "required": required
        },
        "function": func
    }
    return func

# ---- MCP TOOLS ----
@register_tool
def hello(name: str) -> str:
    """Say hello to a user."""
    return f"Hello {name}, MCP server is working 🚀"

@register_tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

# ---- MCP MESSAGE HANDLER ----

async def handle_mcp_message(message: Dict[str, Any]) -> Dict[str, Any]:
    """Handle incoming MCP messages"""
    method = message.get("method")
    
    if method == "initialize":
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "my-mcp-server",
                "version": "1.0.0"
            }
        }
    
    elif method == "tools/list":
        return {
            "tools": [
                {
                    "name": tool["name"],
                    "description": tool["description"],
                    "inputSchema": tool["inputSchema"]
                }
                for tool in TOOLS.values()
            ]
        }
    
    elif method == "tools/call":
        params = message.get("params", {})
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name not in TOOLS:
            return {"error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}}
        
        try:
            result = TOOLS[tool_name]["function"](**arguments)
            return {
                "content": [
                    {
                        "type": "text",
                        "text": str(result)
                    }
                ]
            }
        except Exception as e:
            return {"error": {"code": -32603, "message": str(e)}}
    
    return {"error": {"code": -32601, "message": f"Unknown method: {method}"}}

# ---- MCP ENDPOINTS ----

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """Main MCP endpoint for JSON-RPC messages"""
    try:
        body = await request.json()
        result = await handle_mcp_message(body)
        
        # JSON-RPC response format
        response = {
            "jsonrpc": "2.0",
            "id": body.get("id"),
            "result": result
        }
        
        if "error" in result:
            response = {
                "jsonrpc": "2.0",
                "id": body.get("id"),
                "error": result["error"]
            }
        
        return response
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(e)}
            }
        )

@app.get("/mcp")
async def mcp_sse():
    """SSE endpoint for MCP"""
    async def event_generator():
        # Send initial connection event
        yield f"data: {json.dumps({'type': 'connected'})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

# Backward compatible endpoints
@app.post("/mcp/initialize")
async def initialize(request: Request):
    """MCP initialize endpoint"""
    result = await handle_mcp_message({"method": "initialize"})
    return result

@app.post("/mcp/tools/list")
async def list_tools():
    """List available MCP tools"""
    result = await handle_mcp_message({"method": "tools/list"})
    return result

@app.post("/mcp/tools/call")
async def call_tool(request: Request):
    """Call an MCP tool"""
    body = await request.json()
    message = {
        "method": "tools/call",
        "params": body
    }
    result = await handle_mcp_message(message)
    return result

# Normal FastAPI route
@app.get("/")
def health():
    return {"status": "ok"}
