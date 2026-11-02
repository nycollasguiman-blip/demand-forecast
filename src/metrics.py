import numpy as np

def wape(y, yhat):
    """
    Total absolute error divided by total sales. 0.20 = an error of 20% of the volume.
    """
    return np.abs(y - yhat).sum() / y.sum()
    
def rmsle(y, yhat):
    """
    Official competition metric. It penalizes relative error, not absolute error.
    """
    yhat = np.clip(yhat, 0, None)
    return np.sqrt(np.mean((np.log1p(yhat) - np.log1p(y)) ** 2))
    
def stock_simulation(y, yhat, safety=0.10, cost_stockout=3.0, cost_excess=1.0):
    """
    Replenish stock = forecast x (1 + safety margin), and measure shortages and surpluses.
    cost_stockout: cost of a unit that is out of stock (lost sale, dissatisfied customer).
    cost_excess: cost of a unit that is in surplus (tied-up capital, loss of perishable goods).
    """
    stock = np.clip(yhat, 0, None) * (1 + safety)

    shortage = np.clip(y - stock, 0, None).sum()
    surplus = np.clip(stock - y, 0, None).sum()

    return {
        "shortage_units": round(shortage),
        "surplus_units": round(surplus),
        "total_cost": round(cost_stockout * shortage + cost_excess * surplus),
    }