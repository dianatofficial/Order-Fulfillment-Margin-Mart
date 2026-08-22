def calculate_margin(revenue: float, cost: float) -> float:
    return (revenue - cost) / revenue if revenue else 0.0
