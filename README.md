# MCP Streamable HTTP Example

A comprehensive example demonstrating how to build an MCP (Model Context Protocol) server using [FastMCP](https://github.com/jlowin/fastmcp) with streamable HTTP transport.

## Overview

This project showcases the three main MCP primitives:
- **Tools**: Mathematical operations (add, subtract, multiply, divide)
- **Resources**: Static content endpoints (greeting, mathematical constants)
- **Prompts**: Template generators (math problems, personalized greetings)

## Requirements

- Python >= 3.13
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- curl (for testing)
- jq (optional, for pretty JSON output)

## Installation

### Using uv (recommended)

```bash
uv sync
```

### Using pip

```bash
pip install -r requirements.txt
```

## Running the Server

Start the MCP server with streamable HTTP transport:

### Using uv (recommended)

```bash
uv run mcp-streamable_http.py
```

### Using python directly

```bash
python mcp-streamable_http.py
```

The server will start on `http://127.0.0.1:8000/mcp` by default.

## Testing the Server

A comprehensive test script is provided that demonstrates all MCP capabilities:

```bash
./mcp-streamable_http.sh
```

This script will:
1. Initialize a session with the MCP server
2. List and call tools
3. List and read resources
4. List and retrieve prompts

### Example Output

The test script output is saved to [mcp-streamable_http.sh.log](mcp-streamable_http.sh.log) which shows:
- Session initialization
- Tool execution results
- Available resources
- Prompt templates

## API Endpoints

### Tools

| Tool | Description | Parameters | Returns |
|------|-------------|------------|---------|
| `add` | Add two integers | `a: int, b: int` | `int` |
| `subtract` | Subtract two integers | `a: int, b: int` | `int` |
| `multiply` | Multiply two integers | `a: int, b: int` | `int` |
| `divide` | Divide two integers | `a: int, b: int` | `float` |

### Resources

| URI | Description | Returns |
|-----|-------------|---------|
| `greeting://hello` | Simple greeting message | Plain text |
| `math://constants` | Mathematical constants (Pi, e, Golden ratio, sqrt(2)) | Plain text |

### Prompts

| Prompt | Description | Arguments |
|--------|-------------|-----------|
| `math_problem` | Generate math problem | `operation: str, num1: int, num2: int` |
| `greeting_prompt` | Generate personalized greeting | `name: str` |

## Project Structure

```
.
├── mcp-streamable_http.py      # Main MCP server implementation
├── mcp-streamable_http.sh      # Test script using curl
├── mcp-streamable_http.sh.log  # Example test output
├── pyproject.toml              # Project dependencies
├── uv.lock                     # Dependency lock file
└── README.md                   # This file
```

## Implementation Details

The server is built using [FastMCP](https://github.com/jlowin/fastmcp), which provides:
- Simple decorator-based API for defining tools, resources, and prompts
- Built-in support for multiple transport protocols (stdio, SSE, streamable HTTP)
- Automatic JSON-RPC handling
- Type-safe parameter validation

### Key Features

- **Streamable HTTP Transport**: Uses HTTP with Server-Sent Events (SSE) for real-time communication
- **Session Management**: Each client gets a unique session ID via `Mcp-Session-Id` header
- **JSON-RPC 2.0**: All communication follows the JSON-RPC 2.0 specification
- **Type Safety**: Full type hints for all functions and parameters

## Manual Testing with curl

### Initialize Session

```bash
SID=$(curl -sS -L -D - -o /dev/null \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -X POST http://127.0.0.1:8000/mcp \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{
        "protocolVersion":"2025-03-26",
        "capabilities":{},
        "clientInfo":{"name":"test","version":"1.0"}
      }}' | sed -nE 's/^Mcp-Session-Id:[[:space:]]*//Ip' | tr -d '\r')
```

### Call a Tool

```bash
curl -sS --no-buffer -N \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SID" \
  -X POST http://127.0.0.1:8000/mcp \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{
        "name":"add","arguments":{"a":2,"b":3}}}'
```

### List Resources

```bash
curl -sS --no-buffer \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SID" \
  -X POST http://127.0.0.1:8000/mcp \
  -d '{"jsonrpc":"2.0","id":3,"method":"resources/list","params":{}}'
```

## License

This is an example project for demonstration purposes.

## References

- [MCP Specification](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
