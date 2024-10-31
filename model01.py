import gurobipy as gp
from gurobipy import GRB

# days
days = [ 0, 1, 2, 3, 4, 5, 6]

# Channels
channels = [
    "mailers",
    "influencers",
    "search"
]

# betas for a week
betas = [
        [1.8, 1.9, 1.8, 1.9, 1.8, 1.9, 1.8],
        [4.3, 4.4, 4.0, 4.4, 4.0, 4.4, 4.0],
        [1.4, 1.2, 1.0, 0.9, 1.0, 1.2, 1.0]
        ]   

# percentage of cumulative impact
time_shifts = [
        [0.0019, 0.0099, 0.0292, 0.0639, 0.1159, 0.1842, 0.2653],
        [0.3195, 0.5571, 0.7137, 0.8132, 0.8761, 0.9163, 0.9423],
        [0.8122, 0.9439, 0.9796, 0.9916, 0.9963, 0.9982, 0.9991]
        ]

saturation = [
        [0, 17.924406, 71.697626, 161.319658, 286.790504, 448.110162, 645.278634, 878.295918, 1147.162016, 1451.876926, 1792.44065, 2168.853186],
        [0, 141.308741, 548.75405, 1178.488876, 1972.462648, 2871.879947, 3826.015924, 4795.683883, 5753.048675, 6679.741193, 7564.57628, 8401.499691],
        [0, 98.371215, 392.848131, 881.533867, 1561.310734, 2427.903909, 3475.966752, 4699.184263, 6090.390621, 7641.696462, 9344.621472, 11190.228136],
        [0, 29.374948, 114.732808, 248.515354, 420.220227, 618.513547, 832.890164, 1054.600347, 1276.930335, 1495.072955, 1705.809656, 1907.150328]
        ]

# Scalars
total_budget = 1000.0


# budget

viable_spend = [
        [10, 20, 30, 40, 50, 60, 70],
        [20, 40, 60, 80, 100, 120, 140],
        [30, 60, 90, 120, 150, 180, 210]
]

# Impact calculation

def calculate_saturation(saturation, channel_index, value):
    return value

def impact(betas, time_shifts, spend, saturation):
    c = len(spend)
    d = len(spend[0])

    # Initialize detailed matrices
    detailed_impact = [[0 for i in range(d)] for j in range(c)]
    detailed_spend = [[0 for i in range(d)] for j in range(c)]
    saturated_impact = [[0 for i in range(d)] for j in range(c)]

    # Distribute spend base on time shifts
    for i in range(c):
        for j in range(d):
            local_spend = spend[i][j]
            local_impact = betas[i][j] * spend[i][j] 
            for k in (j, d - 1):
                if k - j == 0:
                    incremental_shift = time_shifts[i][0]
                else:
                    incremental_shift = time_shifts[i][k - j] - time_shifts[i][0]

                detailed_spend[i][k] += local_impact * incremental_shift


    # Calculate impact from the detailed spend observing saturation
    for i in range(c):
        for j in range(d):
            local_saturation = calculate_saturation(saturation, i, detailed_spend[i][j])
            local_impact = detailed_spend[i][j] * betas[i][j]
            detailed_impact[i][j] = local_impact
            if local_impact > local_saturation:
                saturated_impact[i][j] = local_saturation
            else:
                saturated_impact[i][j] = local_impact

    # Final total impact
    total_impact = 0
    total_saturated_impact = 0
    for i in range(c):
        for j in range(d):
            total_impact += detailed_impact[i][j]
            total_saturated_impact += saturated_impact[i][j]

    return {
        "total_impact": total_impact,
        "total_saturated_impact": total_saturated_impact,
        "detailed_impact": detailed_impact,
        "saturated_impact": saturated_impact
    }

print(impact(betas, time_shifts, viable_spend, saturation))


