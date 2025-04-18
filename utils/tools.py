import asyncio
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from utils.config import load_config

async def get_tools_async():
    """Gets tools from the mobile MCP server."""
    config = load_config()
    
    # Default to using the released version via npx
    command = 'npx'
    args = ['-y', 'mobilenext/mobile-mcp@latest']
    
    # Override with local version if specified in config
    if config.get('mobile_mcp_path'):
        command = 'node'
        args = [config.get('mobile_mcp_path')]
    
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=StdioServerParameters(
            command=command,
            args=args,
        )
    )
    return tools, exit_stack