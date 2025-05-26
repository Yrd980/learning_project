from mcp.server.fastmcp import FastMCP
import logging

mcp = FastMCP("MathTools")

@mcp.tool()
def add(a: int, b: int) -> int:
    """加法运算：返回两数之和"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """乘法运算：返回两数之积"""
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")
