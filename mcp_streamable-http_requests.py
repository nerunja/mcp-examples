#!/usr/bin/env python3
"""
Python client to interact with a streamable-http MCP server over HTTP.
This script performs the same operations as mcp-streamable_http.sh
"""

import requests
import json
import sys

class MCPClient:
    def __init__(self, base_url="http://127.0.0.1:8000/mcp"):
        self.base_url = base_url
        self.session_id = None
        self.headers = {
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, payload, stream=False):
        """Make a request to the MCP server"""
        headers = self.headers.copy()
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        
        response = requests.post(
            self.base_url,
            headers=headers,
            json=payload,
            stream=stream,
            allow_redirects=True
        )
        return response
    
    def _parse_streamable_response(self, response):
        """Parse streamable-http response (line-delimited JSON)"""
        results = []
        for line in response.iter_lines(decode_unicode=True):
            if line.startswith('data: '):
                data = line[6:]  # Remove 'data: ' prefix
                try:
                    results.append(json.loads(data))
                except json.JSONDecodeError:
                    results.append(data)
        return results
    
    def _print_response(self, title, data):
        """Pretty print response"""
        print(f"=== {title} ===")
        if isinstance(data, list):
            for item in data:
                print(json.dumps(item, indent=2))
        else:
            print(json.dumps(data, indent=2))
        print()
    
    def initialize(self):
        """Initialize the MCP session"""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "python", "version": "1.0"}
            }
        }
        
        response = self._make_request(payload, stream=True)
        
        # Extract session ID from headers
        self.session_id = response.headers.get('Mcp-Session-Id')
        print(f"=== initialize ===")
        print(f"SID={self.session_id}")
        
        # Parse streamable-http response
        results = self._parse_streamable_response(response)
        if results:
            print(json.dumps(results[0], indent=2))
        print()
        
        return results[0] if results else None
    
    def notifications_initialized(self):
        """Send initialized notification"""
        payload = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {}
        }
        
        response = self._make_request(payload)
        print(f"=== notifications/initialized response ===")
        if response.text.strip():
            try:
                data = response.json()
                print(json.dumps(data, indent=2))
            except json.JSONDecodeError as e:
                print(f"Response text: {response.text}")
                print(f"JSON decode error: {e}")
        else:
            print("Empty response (notification acknowledged)")
        print()
    
    def tools_call(self, tool_name, arguments):
        """Call a tool"""
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        response = self._make_request(payload, stream=True)
        results = self._parse_streamable_response(response)
        self._print_response(f"tools/call response", results)
        return results
    
    def tools_list(self):
        """List available tools"""
        payload = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/list",
            "params": {}
        }
        
        response = self._make_request(payload, stream=True)
        results = self._parse_streamable_response(response)
        self._print_response("tools/list response", results)
        return results
    
    def resources_list(self):
        """List available resources"""
        payload = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "resources/list",
            "params": {}
        }
        
        response = self._make_request(payload, stream=True)
        results = self._parse_streamable_response(response)
        self._print_response("resources/list response", results)
        return results
    
    def resources_read(self, uri):
        """Read a resource"""
        payload = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "resources/read",
            "params": {"uri": uri}
        }
        
        response = self._make_request(payload, stream=True)
        results = self._parse_streamable_response(response)
        self._print_response(f"resources/read ({uri}) response", results)
        return results
    
    def prompts_list(self):
        """List available prompts"""
        payload = {
            "jsonrpc": "2.0",
            "id": 7,
            "method": "prompts/list",
            "params": {}
        }
        
        response = self._make_request(payload, stream=True)
        results = self._parse_streamable_response(response)
        self._print_response("prompts/list response", results)
        return results
    
    def prompts_get(self, name, arguments):
        """Get a prompt"""
        payload = {
            "jsonrpc": "2.0",
            "id": 8,
            "method": "prompts/get",
            "params": {
                "name": name,
                "arguments": arguments
            }
        }
        
        response = self._make_request(payload, stream=True)
        results = self._parse_streamable_response(response)
        self._print_response(f"prompts/get ({name}) response", results)
        return results


def main():
    """Main function to run all MCP operations"""
    client = MCPClient()
    
    # 1. Initialize
    client.initialize()
    
    # 2. Send initialized notification
    client.notifications_initialized()
    
    # 3. Call add tool
    client.tools_call("add", {"a": 2, "b": 3})
    
    # 4. List tools
    client.tools_list()
    
    # 5. List resources
    client.resources_list()
    
    # 6. Read greeting resource
    client.resources_read("greeting://hello")
    
    # 7. Read math constants resource
    client.resources_read("math://constants")
    
    # 8. List prompts
    client.prompts_list()
    
    # 9. Get math problem prompt
    client.prompts_get("math_problem", {
        "operation": "+",
        "num1": "10",
        "num2": "20"
    })
    
    # 10. Get greeting prompt
    client.prompts_get("greeting_prompt", {"name": "Alice"})


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
