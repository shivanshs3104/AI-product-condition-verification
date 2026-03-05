def calculate_price(base_price, severity_score):
    """
    Reduce price based on damage severity.
    """

    if severity_score <= 2:
        discount = 0.05   # 5%
    elif severity_score <= 4:
        discount = 0.10   # 10%
    elif severity_score <= 6:
        discount = 0.20   # 20%
    elif severity_score <= 8:
        discount = 0.35   # 35%
    else:
        discount = 0.50   # 50%

    final_price = base_price * (1 - discount)

    return round(final_price, 2)