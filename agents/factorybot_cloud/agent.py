"""FactoryBot Cloud - Factory operations AI agent."""

from google.adk.agents import Agent


def get_system_status(component: str) -> dict:
    """Returns the current status of a factory component.

    Args:
        component: Name of the factory component to check (e.g. 'assembly_line', 'inventory', 'quality_control').

    Returns:
        A dictionary with the component status.
    """
    statuses = {
        "assembly_line": {"status": "running", "efficiency": "94%", "units_today": 1247},
        "inventory": {"status": "ok", "low_stock_items": 3, "total_items": 892},
        "quality_control": {"status": "warning", "defect_rate": "2.1%", "threshold": "1.5%"},
    }
    return statuses.get(component, {"status": "unknown", "message": f"Component '{component}' not found"})


def get_all_statuses() -> dict:
    """Returns the status of all factory components at once.

    Returns:
        A dictionary with all component statuses.
    """
    components = ["assembly_line", "inventory", "quality_control"]
    return {c: get_system_status(c) for c in components}


def create_work_order(task: str, priority: str = "normal") -> dict:
    """Creates a new work order for the factory floor.

    Args:
        task: Description of the work to be done.
        priority: Priority level - 'low', 'normal', 'high', or 'critical'.

    Returns:
        A dictionary confirming the work order creation.
    """
    return {
        "status": "created",
        "work_order_id": "WO-2026-0042",
        "task": task,
        "priority": priority,
        "estimated_completion": "2 hours",
    }


root_agent = Agent(
    model="gemini-2.5-flash",
    name="factorybot",
    description="An AI agent that monitors and manages factory operations.",
    instruction="""You are FactoryBot, an intelligent factory operations assistant.

You help operators monitor production lines, check inventory levels, track quality metrics,
and create work orders. Be concise, data-driven, and proactive about flagging issues.

When reporting status, highlight any warnings or anomalies first.""",
    tools=[get_system_status, get_all_statuses, create_work_order],
)
