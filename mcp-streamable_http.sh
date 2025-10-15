#!/usr/bin/env bash
# Example script to interact with an streamable-http MCP server over HTTP using curl.

set -euo pipefail


S=http://127.0.0.1:8000/mcp
ACCEPT='application/json, text/event-stream'
CT='application/json'

# Check if jq is available for pretty JSON output
if command -v jq &> /dev/null; then
  USE_JQ=true
else
  USE_JQ=false
  echo "Note: jq not found. Install jq for pretty JSON output (brew install jq)"
  echo ""
fi


# 1) initialize (added -L to follow redirects)
echo "=== initialize ==="
SID=$(curl -sS -L -D - -o /dev/null \
  -H "Accept: $ACCEPT" -H "Content-Type: $CT" \
  -X POST $S \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{
        "protocolVersion":"2025-03-26",
        "capabilities":{},
        "clientInfo":{"name":"bash","version":"1.0"}
      }}' | sed -nE 's/^Mcp-Session-Id:[[:space:]]*//Ip' | tr -d '\r')
echo "SID=$SID"

# 2) notifications/initialized
echo "=== notifications/initialized response ==="
if [ "$USE_JQ" = true ]; then
  curl -sS --no-buffer -L \
    -H "Accept: $ACCEPT" \
    -H "Content-Type: $CT" \
    -H "Mcp-Session-Id: $SID" \
    -X POST $S \
    -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' | jq '.'
else
  curl -sS --no-buffer -L \
    -H "Accept: $ACCEPT" \
    -H "Content-Type: $CT" \
    -H "Mcp-Session-Id: $SID" \
    -X POST $S \
    -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}'
fi
echo

# 3) tools/call
echo "=== tools/call response ==="
if [ "$USE_JQ" = true ]; then
  curl -sS --no-buffer -N -L \
    -H "Accept: $ACCEPT" -H "Content-Type: $CT" -H "Mcp-Session-Id: $SID" \
    -X POST $S \
    -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{
          "name":"add","arguments":{"a":2,"b":3}}}' | grep '^data: ' | sed 's/^data: //' | jq '.'
else
  curl -sS --no-buffer -N -L \
    -H "Accept: $ACCEPT" -H "Content-Type: $CT" -H "Mcp-Session-Id: $SID" \
    -X POST $S \
    -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{
          "name":"add","arguments":{"a":2,"b":3}}}'
fi
echo

# 4) tools/list
echo "=== tools/list response ==="
if [ "$USE_JQ" = true ]; then
  curl -sS --no-buffer -L \
    -H "Accept: $ACCEPT" -H "Content-Type: $CT" -H "Mcp-Session-Id: $SID" \
    -X POST $S \
    -d '{"jsonrpc":"2.0","id":3,"method":"tools/list","params":{}}' | grep '^data: ' | sed 's/^data: //' | jq '.'
else
  curl -sS --no-buffer -L \
    -H "Accept: $ACCEPT" -H "Content-Type: $CT" -H "Mcp-Session-Id: $SID" \
    -X POST $S \
    -d '{"jsonrpc":"2.0","id":3,"method":"tools/list","params":{}}'
fi
echo

# 5) resources/list
echo "=== resources/list response ==="
if [ "$USE_JQ" = true ]; then
  curl -sS --no-buffer -L \
    -H "Accept: $ACCEPT" -H "Content-Type: $CT" -H "Mcp-Session-Id: $SID" \
    -X POST $S \
    -d '{"jsonrpc":"2.0","id":4,"method":"resources/list","params":{}}' | grep '^data: ' | sed 's/^data: //' | jq '.'
else
  curl -sS --no-buffer -L \
    -H "Accept: $ACCEPT" -H "Content-Type: $CT" -H "Mcp-Session-Id: $SID" \
    -X POST $S \
    -d '{"jsonrpc":"2.0","id":4,"method":"resources/list","params":{}}'
fi
echo

# 6) resources/read - greeting
echo "=== resources/read (greeting://hello) response ==="
if [ "$USE_JQ" = true ]; then
  curl -sS --no-buffer -L \
    -H "Accept: $ACCEPT" -H "Content-Type: $CT" -H "Mcp-Session-Id: $SID" \
    -X POST $S \
    -d '{"jsonrpc":"2.0","id":5,"method":"resources/read","params":{"uri":"greeting://hello"}}' | grep '^data: ' | sed 's/^data: //' | jq '.'
else
  curl -sS --no-buffer -L \
    -H "Accept: $ACCEPT" -H "Content-Type: $CT" -H "Mcp-Session-Id: $SID" \
    -X POST $S \
    -d '{"jsonrpc":"2.0","id":5,"method":"resources/read","params":{"uri":"greeting://hello"}}'
fi
echo

# 7) resources/read - math constants
echo "=== resources/read (math://constants) response ==="
if [ "$USE_JQ" = true ]; then
  curl -sS --no-buffer -L \
    -H "Accept: $ACCEPT" -H "Content-Type: $CT" -H "Mcp-Session-Id: $SID" \
    -X POST $S \
    -d '{"jsonrpc":"2.0","id":6,"method":"resources/read","params":{"uri":"math://constants"}}' | grep '^data: ' | sed 's/^data: //' | jq '.'
else
  curl -sS --no-buffer -L \
    -H "Accept: $ACCEPT" -H "Content-Type: $CT" -H "Mcp-Session-Id: $SID" \
    -X POST $S \
    -d '{"jsonrpc":"2.0","id":6,"method":"resources/read","params":{"uri":"math://constants"}}'
fi
echo

# 8) prompts/list
echo "=== prompts/list response ==="
if [ "$USE_JQ" = true ]; then
  curl -sS --no-buffer -L \
    -H "Accept: $ACCEPT" -H "Content-Type: $CT" -H "Mcp-Session-Id: $SID" \
    -X POST $S \
    -d '{"jsonrpc":"2.0","id":7,"method":"prompts/list","params":{}}' | grep '^data: ' | sed 's/^data: //' | jq '.'
else
  curl -sS --no-buffer -L \
    -H "Accept: $ACCEPT" -H "Content-Type: $CT" -H "Mcp-Session-Id: $SID" \
    -X POST $S \
    -d '{"jsonrpc":"2.0","id":7,"method":"prompts/list","params":{}}'
fi
echo

# 9) prompts/get - math problem
echo "=== prompts/get (math_problem) response ==="
if [ "$USE_JQ" = true ]; then
  curl -sS --no-buffer -L \
    -H "Accept: $ACCEPT" -H "Content-Type: $CT" -H "Mcp-Session-Id: $SID" \
    -X POST $S \
    -d '{"jsonrpc":"2.0","id":8,"method":"prompts/get","params":{"name":"math_problem","arguments":{"operation":"+","num1":10,"num2":20}}}' | grep '^data: ' | sed 's/^data: //' | jq '.'
else
  curl -sS --no-buffer -L \
    -H "Accept: $ACCEPT" -H "Content-Type: $CT" -H "Mcp-Session-Id: $SID" \
    -X POST $S \
    -d '{"jsonrpc":"2.0","id":8,"method":"prompts/get","params":{"name":"math_problem","arguments":{"operation":"+","num1":10,"num2":20}}}'
fi
echo

# 10) prompts/get - greeting prompt
echo "=== prompts/get (greeting_prompt) response ==="
if [ "$USE_JQ" = true ]; then
  curl -sS --no-buffer -L \
    -H "Accept: $ACCEPT" -H "Content-Type: $CT" -H "Mcp-Session-Id: $SID" \
    -X POST $S \
    -d '{"jsonrpc":"2.0","id":9,"method":"prompts/get","params":{"name":"greeting_prompt","arguments":{"name":"Alice"}}}' | grep '^data: ' | sed 's/^data: //' | jq '.'
else
  curl -sS --no-buffer -L \
    -H "Accept: $ACCEPT" -H "Content-Type: $CT" -H "Mcp-Session-Id: $SID" \
    -X POST $S \
    -d '{"jsonrpc":"2.0","id":9,"method":"prompts/get","params":{"name":"greeting_prompt","arguments":{"name":"Alice"}}}'
fi
echo