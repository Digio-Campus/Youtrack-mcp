# server.py
from mcp.server.fastmcp import FastMCP


# Create the MCP server instance
mcp = FastMCP("Youtrack MCP Server")

# Timestamp tool
@mcp.tool()
def getTasksInformation() -> str:
    """
    Read the Agile Panel from Youtrack, obtaining information about all the tasks and returns a markdown detailing it.
    
    Returns:
        str: A string containing information about all tasks in markdown format.
    """
    return "Task information in markdown format"



if __name__ == "__main__":
    mcp.run(transport="stdio")