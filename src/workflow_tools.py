from typing import Literal
from langchain.tools import tool, ToolRuntime
from langchain.messages import ToolMessage
from langgraph.types import Command

from states import InsuranceSupportState, InsuranceStep

@tool
def transfer_to_sales(
    interest: Literal["auto", "habitation", "sante"]
):
    pass