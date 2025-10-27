#!/usr/bin/env python3
"""
FastMCP client to interact with a streamable-http MCP server over HTTP.
This script performs the same operations as mcp-streamable_http.sh using FastMCP's Client/ClientSession.
"""

import asyncio
import json
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
import httpx


async def main():
    """Main function to run all MCP operations using FastMCP Client"""
    
    # Connect to the MCP server using streamable-http transport
    server_url = "http://127.0.0.1:8000/mcp"
    
    print(f"Connecting to MCP server at {server_url}...")
    print("Make sure the server is running with: uv run python mcp_streamable-http.py")
    print()
    
    try:
        # streamablehttp_client yields (read_stream, write_stream, session_manager)
        async with streamablehttp_client(server_url) as (read, write, _):
            async with ClientSession(read, write) as session:
                
                # 1. Initialize the session
                print("=== initialize ===")
                await session.initialize()
                print("Session initialized successfully")
                print()
                
                # 2. List available tools
                print("=== tools/list ===")
                tools_result = await session.list_tools()
                print(json.dumps(tools_result.model_dump(mode='json'), indent=2))
                print()
                
                # 3. Call the 'add' tool
                print("=== tools/call (add) ===")
                call_result = await session.call_tool("add", arguments={"a": 2, "b": 3})
                print(json.dumps(call_result.model_dump(mode='json'), indent=2))
                print(f"Result: {call_result.content[0].text if call_result.content else 'No content'}")
                print()
                
                # 4. List available resources
                print("=== resources/list ===")
                resources_result = await session.list_resources()
                print(json.dumps(resources_result.model_dump(mode='json'), indent=2))
                print(f"Resources: {[r.uri for r in resources_result.resources]}")
                print()
                
                # 5. Read greeting resource
                print("=== resources/read (greeting://hello) ===")
                greeting_result = await session.read_resource("greeting://hello")
                print(json.dumps(greeting_result.model_dump(mode='json'), indent=2))
                print(f"Content: {greeting_result.contents[0].text if greeting_result.contents else 'No content'}")
                print()
                
                # 6. Read math constants resource
                print("=== resources/read (math://constants) ===")
                math_result = await session.read_resource("math://constants")
                print(json.dumps(math_result.model_dump(mode='json'), indent=2))
                print(f"Content: {math_result.contents[0].text if math_result.contents else 'No content'}")
                print()
                
                # 7. List available prompts
                print("=== prompts/list ===")
                prompts_result = await session.list_prompts()
                print(json.dumps(prompts_result.model_dump(mode='json'), indent=2))
                print(f"Prompts: {[p.name for p in prompts_result.prompts]}")
                print()
                
                # 8. Get math problem prompt
                print("=== prompts/get (math_problem) ===")
                math_prompt_result = await session.get_prompt(
                    "math_problem",
                    arguments={
                        "operation": "+",
                        "num1": "10",
                        "num2": "20"
                    }
                )
                print(json.dumps(math_prompt_result.model_dump(mode='json'), indent=2))
                print(f"Prompt: {math_prompt_result.messages[0].content.text if math_prompt_result.messages else 'No messages'}")
                print()
                
                # 9. Get greeting prompt
                print("=== prompts/get (greeting_prompt) ===")
                greeting_prompt_result = await session.get_prompt(
                    "greeting_prompt",
                    arguments={"name": "Alice"}
                )
                print(json.dumps(greeting_prompt_result.model_dump(mode='json'), indent=2))
                print(f"Prompt: {greeting_prompt_result.messages[0].content.text if greeting_prompt_result.messages else 'No messages'}")
                print()
                
                # 10. Demonstrate additional tool calls
                print("=== Additional tool calls ===")
                
                # Subtract
                subtract_result = await session.call_tool("subtract", arguments={"a": 10, "b": 3})
                print(f"Subtract: {json.dumps(subtract_result.model_dump(mode='json'), indent=2)}")
                print(f"Result: {subtract_result.content[0].text if subtract_result.content else 'No content'}")
                print()
                
                # Multiply
                multiply_result = await session.call_tool("multiply", arguments={"a": 4, "b": 5})
                print(f"Multiply: {json.dumps(multiply_result.model_dump(mode='json'), indent=2)}")
                print(f"Result: {multiply_result.content[0].text if multiply_result.content else 'No content'}")
                print()
                
                # Divide
                divide_result = await session.call_tool("divide", arguments={"a": 20, "b": 4})
                print(f"Divide: {json.dumps(divide_result.model_dump(mode='json'), indent=2)}")
                print(f"Result: {divide_result.content[0].text if divide_result.content else 'No content'}")
                print()
    except httpx.ConnectError:
        print("❌ ERROR: Cannot connect to MCP server!")
        print(f"   Server URL: {server_url}")
        print("   Please ensure the server is running in another terminal:")
        print("   $ uv run python mcp_streamable-http.py")
        return
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
