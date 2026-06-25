#!/usr/bin/env python3
"""
FastMCP Server for querying inventory from ksqlDB in Confluent Cloud.

This server provides a tool to query the current inventory availability
from the ksqlDB table that aggregates inventory transactions in real-time.

Features:
- Robust multi-strategy response parsing
- Handles multiple ksqlDB response formats
- Comprehensive error handling
- Uses environment variables from .env file
"""

import os
import json
import base64
import re
import urllib.request
import urllib.error
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("Inventory Query Server")


class KsqlDBError(Exception):
    """Custom exception for ksqlDB-related errors."""
    pass


def get_ksqldb_config() -> tuple[str, str, str]:
    """
    Get ksqlDB configuration from environment variables.
    
    Returns:
        Tuple of (endpoint, api_key, api_secret)
        
    Raises:
        KsqlDBError: If required configuration is missing
    """
    endpoint = os.getenv("KSQLDB_QUERY_ENDPOINT")
    api_key = os.getenv("KSQLDB_API_KEY")
    api_secret = os.getenv("KSQLDB_API_SECRET")
    
    if not all([endpoint, api_key, api_secret]):
        raise KsqlDBError(
            "Missing ksqlDB configuration. Please set KSQLDB_QUERY_ENDPOINT, "
            "KSQLDB_API_KEY, and KSQLDB_API_SECRET in .env file"
        )
    
    return endpoint, api_key, api_secret


def get_auth_header() -> str:
    """
    Generate Basic Auth header for ksqlDB API.
    
    Returns:
        Authorization header value
    """
    _, api_key, api_secret = get_ksqldb_config()
    credentials = f"{api_key}:{api_secret}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"


def _escape_sql_literal(value: str) -> str:
    """
    Escape single quotes in SQL string literals by doubling them.
    
    Args:
        value: String value to escape
        
    Returns:
        Escaped string safe for SQL literal
    """
    return value.replace("'", "''")


def _extract_json_objects(raw_output: str) -> List[Dict[str, Any]]:
    """
    Extract JSON objects from text output using multiple strategies.
    
    First tries line-by-line parsing, then falls back to regex extraction.
    This is the proven approach for handling various response formats.
    
    Args:
        raw_output: Raw response text from ksqlDB
        
    Returns:
        List of extracted JSON objects
    """
    records: List[Dict[str, Any]] = []

    # Strategy 1: Line-by-line parsing
    for line in raw_output.splitlines():
        candidate = line.strip()
        if not candidate or not candidate.startswith("{") or not candidate.endswith("}"):
            continue
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            records.append(parsed)

    if records:
        return records

    # Strategy 2: Regex-based extraction for malformed responses
    for candidate in re.findall(r"\{.*?\}", raw_output, flags=re.DOTALL):
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            records.append(parsed)

    return records


def parse_query_output(raw_output: str) -> List[Dict[str, Any]]:
    """
    Normalize text output that contains row-shaped JSON.
    
    Handles both streaming format with {"row": {"columns": [...]}}
    and direct format with {"sku": ..., "branch": ..., "available_quantity": ...}
    
    This is the proven text-based parsing approach.
    
    Args:
        raw_output: Raw response text from ksqlDB
        
    Returns:
        List of normalized row dictionaries
    """
    payloads = _extract_json_objects(raw_output)
    rows: List[Dict[str, Any]] = []

    for item in payloads:
        # Format 1: Streaming format with row.columns
        if "row" in item and isinstance(item["row"], dict):
            columns = item["row"].get("columns", [])
            if len(columns) >= 3:
                rows.append({
                    "sku": columns[0],
                    "branch": columns[1],
                    "available_quantity": columns[2],
                })
            continue

        # Format 2: Direct format with named fields
        if {"sku", "branch", "available_quantity"}.issubset(item.keys()):
            rows.append({
                "sku": item["sku"],
                "branch": item["branch"],
                "available_quantity": item["available_quantity"],
            })

    return rows


def parse_ksqldb_response(payload: Any) -> List[Dict[str, Any]]:
    """
    Normalize ksqlDB REST API responses into availability rows.
    
    Handles both list and single object responses, checks for errors,
    and extracts data in multiple formats.
    
    This is the proven JSON-based parsing approach.
    
    Args:
        payload: Parsed JSON response from ksqlDB API
        
    Returns:
        List of normalized row dictionaries
        
    Raises:
        KsqlDBError: If response contains error information
    """
    items = payload if isinstance(payload, list) else [payload]
    rows: List[Dict[str, Any]] = []

    for item in items:
        if not isinstance(item, dict):
            continue

        # Check for error responses
        # Only treat as error if error_code is present, or if message contains error-like content
        if "error_code" in item:
            message = item.get("message") or item.get("error_code") or "Unknown ksqlDB API error"
            raise KsqlDBError(str(message))

        # Format 1: Streaming format with row.columns
        if "row" in item and isinstance(item["row"], dict):
            columns = item["row"].get("columns", [])
            if len(columns) >= 3:
                rows.append({
                    "sku": columns[0],
                    "branch": columns[1],
                    "available_quantity": columns[2],
                })
            continue

        # Format 2: Direct format with named fields
        if {"sku", "branch", "available_quantity"}.issubset(item.keys()):
            rows.append({
                "sku": item["sku"],
                "branch": item["branch"],
                "available_quantity": item["available_quantity"],
            })

    return rows


def execute_ksqldb_query(query: str) -> List[Dict[str, Any]]:
    """
    Execute a ksqlDB query via REST API using stdlib urllib.
    
    Uses robust parsing with multiple fallback strategies to handle
    various response formats from ksqlDB:
    1. First tries to parse response as JSON
    2. If that fails, falls back to line-by-line text parsing
    3. Includes regex-based extraction as final fallback
    
    This matches the proven approach from existing implementations.
    
    Args:
        query: SQL query string (must end with semicolon)
        
    Returns:
        List of result rows
        
    Raises:
        KsqlDBError: If query fails or connection issues occur
    """
    endpoint, _, _ = get_ksqldb_config()
    
    # Prepare request payload
    payload = json.dumps({
        "ksql": query,
        "streamsProperties": {}
    }).encode("utf-8")
    
    # Build request with proper headers
    request = urllib.request.Request(
        endpoint,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/vnd.ksql.v1+json; charset=utf-8",
            "Accept": "application/vnd.ksql.v1+json",
            "Authorization": get_auth_header()
        }
    )
    
    # Execute request
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            response_text = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise KsqlDBError(f"ksqlDB API HTTP {exc.code}: {error_body}") from exc
    except urllib.error.URLError as exc:
        raise KsqlDBError(f"Failed to reach ksqlDB API: {exc.reason}") from exc
    
    # Parse response with multiple strategies
    # Strategy 1: Try JSON parsing first
    try:
        parsed = json.loads(response_text)
        return parse_ksqldb_response(parsed)
    except json.JSONDecodeError:
        # Strategy 2: Fall back to text-based parsing for streaming responses
        return parse_query_output(response_text)


@mcp.tool()
async def query_inventory(
    sku: Optional[str] = None,
    branch: Optional[str] = None,
    min_quantity: Optional[int] = None,
    max_quantity: Optional[int] = None
) -> str:
    """
    Query current inventory availability from ksqlDB.
    
    This tool queries the inventory_availability table in ksqlDB which contains
    real-time aggregated inventory levels for each SKU at each branch location.
    
    Args:
        sku: Filter by specific SKU (e.g., 'Dell XPS 15'). Optional.
        branch: Filter by specific branch (e.g., 'Mall Of Egypt'). Optional.
        min_quantity: Filter items with quantity >= this value. Optional.
        max_quantity: Filter items with quantity <= this value. Optional.
    
    Returns:
        JSON string containing inventory data with SKU, branch, and available quantity.
        Returns empty list if no matching inventory found.
    
    Examples:
        - query_inventory() - Get all inventory
        - query_inventory(sku="Dell XPS 15") - Get inventory for specific SKU
        - query_inventory(branch="Mall Of Egypt") - Get inventory at specific branch
        - query_inventory(max_quantity=10) - Get low stock items (quantity <= 10)
        - query_inventory(sku="Dell XPS 15", branch="Mall Of Egypt") - Get specific SKU at specific branch
    """
    try:
        # Build the query with filters
        query = "SELECT sku, branch, available_quantity FROM inventory_availability"
        
        conditions = []
        
        # Normalize and escape inputs
        if sku:
            normalized_sku = sku.strip()
            if normalized_sku:
                escaped_sku = _escape_sql_literal(normalized_sku)
                conditions.append(f"sku = '{escaped_sku}'")
        
        if branch:
            normalized_branch = branch.strip()
            if normalized_branch:
                escaped_branch = _escape_sql_literal(normalized_branch)
                conditions.append(f"branch = '{escaped_branch}'")
        
        if min_quantity is not None:
            conditions.append(f"available_quantity >= {min_quantity}")
        
        if max_quantity is not None:
            conditions.append(f"available_quantity <= {max_quantity}")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += ";"
        
        # Execute the query
        results = execute_ksqldb_query(query)
        
        # Calculate total available quantity
        total_available = sum(
            int(row.get("available_quantity", 0)) 
            for row in results
        )
        
        return json.dumps({
            "success": True,
            "count": len(results),
            "total_available_quantity": total_available,
            "filters": {
                "sku": sku,
                "branch": branch,
                "min_quantity": min_quantity,
                "max_quantity": max_quantity
            },
            "inventory": results
        }, indent=2)
        
    except KsqlDBError as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "error_type": "KsqlDBError",
            "inventory": []
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "inventory": []
        }, indent=2)


@mcp.tool()
async def get_low_stock_items(threshold: int = 10) -> str:
    """
    Get all inventory items with stock below a specified threshold.
    
    This is a convenience tool that queries items that may need restocking.
    
    Args:
        threshold: The quantity threshold (default: 10). Items with quantity
                  below this value will be returned.
    
    Returns:
        JSON string containing low stock items with SKU, branch, and available quantity.
    
    Example:
        - get_low_stock_items() - Get items with quantity < 10
        - get_low_stock_items(threshold=5) - Get items with quantity < 5
    """
    return await query_inventory(max_quantity=threshold - 1)


@mcp.tool()
async def get_inventory_summary() -> str:
    """
    Get a summary of the entire inventory across all branches.
    
    Returns:
        JSON string containing all inventory items with their current quantities.
    """
    return await query_inventory()


@mcp.tool()
async def get_inventory_by_sku(sku: str) -> str:
    """
    Get inventory availability for a specific SKU across all branches.
    
    Args:
        sku: The SKU identifier (e.g., "Dell XPS 15")
    
    Returns:
        JSON string containing inventory data for the specified SKU.
    """
    return await query_inventory(sku=sku)


@mcp.tool()
async def get_inventory_by_branch(branch: str) -> str:
    """
    Get inventory availability for a specific branch.
    
    Args:
        branch: The branch name (e.g., "Mall Of Egypt", "Dubai Mall")
               Note: Branch names are case-sensitive.
    
    Returns:
        JSON string containing inventory data for the specified branch.
    """
    return await query_inventory(branch=branch)


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()

# Made with Bob