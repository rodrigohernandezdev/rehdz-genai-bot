from datetime import datetime

from langchain_core.tools import tool


@tool
async def get_actual_date() -> str:
    """
    Get the actual date from the system.
    Returns:
        str: The actual date in a human-readable format.
    """

    now = datetime.now()
    formatted_date = now.strftime("%A, %d %B %Y")
    return formatted_date

date_tools = [get_actual_date]