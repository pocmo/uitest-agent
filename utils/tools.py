import asyncio
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from utils.config import load_config

async def get_mobile_tools_async():
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

async def get_web_tools_async():
    """Gets tools from the web (Playwright) MCP server."""
    config = load_config()
    
    # Use Playwright MCP for web testing
    command = 'npx'
    args = ['@playwright/mcp@latest']
    
    # Override with local version if specified in config
    if config.get('web_mcp_path'):
        command = 'node'
        args = [config.get('web_mcp_path')]
    
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=StdioServerParameters(
            command=command,
            args=args,
        )
    )
    return tools, exit_stack

async def get_tools_async(target="mobile"):
    """Gets tools from the appropriate MCP server based on the target.
    
    Args:
        target: The target platform, either "mobile" or "web".
        
    Returns:
        A tuple of (tools, exit_stack).
        
    Raises:
        ValueError: If the target is not one of "mobile" or "web".
    """
    if target.lower() == "mobile":
        return await get_mobile_tools_async()
    elif target.lower() == "web":
        return await get_web_tools_async()
    else:
        raise ValueError(f"Unsupported target: {target}. Must be 'mobile' or 'web'.")