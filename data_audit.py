import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# DATA AUDITING
df = pd.read_csv("data/raw/flights_july_2026.csv.csv")

df.info()

data_rows = df.shape[0]

data_columns = df.shape[1]

print(f"Total_rows: {data_rows}\n",
      f"Total_columns: {data_columns}\n")

print(df.isna().sum())

cancelled_flights = df["CANCELLED"].sum()

cancelled_missing = ((df["CANCELLED"] == 1) & (df["DEP_DELAY"].isna())).sum()

not_cancelled_missing_dep_delay = df[(df["CANCELLED"] == 0) & df["DEP_DELAY"].isna()].shape[0]

print(f"Cancelled flights: {cancelled_flights}\n",
      f"Cancelled flights with missing departure delay: {cancelled_missing}\n",
      f"Not cancelled flights with missing departure delay: {not_cancelled_missing_dep_delay}\n")

cancelled_flights_with_departure_delay = df[(df["CANCELLED"] == 1) & (df["DEP_DELAY"].notna())]

print(cancelled_flights_with_departure_delay["CANCELLATION_CODE"].value_counts())

cancelled_flights_with_departure_delay_percentage = (cancelled_flights_with_departure_delay["CANCELLATION_CODE"].value_counts() / cancelled_flights_with_departure_delay.shape[0]) * 100
print(cancelled_flights_with_departure_delay_percentage)

print(df["CANCELLATION_CODE"].value_counts())

cancelled_flights_1 = df[df.loc[:, "CANCELLED"] == 1]
cancellation_code_counts = cancelled_flights_1["CANCELLATION_CODE"].value_counts()

cancellation_code_percentages = (cancellation_code_counts / cancelled_flights_1.shape[0]) * 100

print(f"Cancelled flights: {cancellation_code_counts}\n")

print(f"Percentage of cancelled flights by cancellation code:\n{cancellation_code_percentages}\n")

cancelled_flights_without_arrival_delay = df[(df["CANCELLED"] == 1) & (df["ARR_DELAY"].isna())]

print(f"Cancelled flights without arrival delay: {cancelled_flights_without_arrival_delay.shape[0]}\n")

# MISSING DATA & CANCELLATIONS

diverted_flights_with_missing_arrival_delay = df[(df["CANCELLED"] == 0) & (df["DIVERTED"] == 1) & (df["ARR_DELAY"].isna())].shape[0]

missing_arrival_delayed_flights = df[(df["CANCELLED"] == 0) & (df["DIVERTED"] == 0) & (df["ARR_DELAY"].isna())].shape[0]

print(f"Diverted flights with missing arrival delay: {diverted_flights_with_missing_arrival_delay}\n")
print(f"Non-diverted flights with missing arrival delay: {missing_arrival_delayed_flights}\n")

duplicate_rows = df.duplicated().sum()

print("Duplicates:", duplicate_rows)

print(df.dtypes)

print("Dataset shape:", df.shape)

missing_cancellation = df["CANCELLED"].isna().sum()

print("Missing cancellation values:", missing_cancellation)

# AIRLINE PERFORMANCE ANALYSIS

airline_summary = df.groupby("OP_UNIQUE_CARRIER").agg(
      total_flights=pd.NamedAgg(column="CANCELLED", aggfunc="count"),
      cancelled_flights=pd.NamedAgg(column="CANCELLED", aggfunc="sum"),
      cancelled_rate=pd.NamedAgg(column="CANCELLED", aggfunc=lambda x: (x.sum() / x.shape[0]) * 100)
).sort_values(by="cancelled_rate", ascending=False)

print("Airline Summary:\n", airline_summary)

operated_flights = df[df["CANCELLED"] == 0]

delay_summary = operated_flights.groupby("OP_UNIQUE_CARRIER").agg(
    operated_flights = pd.NamedAgg(column="CANCELLED", aggfunc= "count"),
    average_delay = pd.NamedAgg(column="DEP_DELAY", aggfunc="mean"),
    median_delay = pd.NamedAgg(column="DEP_DELAY", aggfunc="median"),
    delayed_flights = pd.NamedAgg(column="DEP_DELAY", aggfunc= lambda x: (x >= 15).sum()),
    delay_rate = pd.NamedAgg(column="DEP_DELAY", aggfunc= lambda x :  (x >= 15).sum() / x.shape[0] * 100)
).sort_values(by="delay_rate", ascending = False)
print(delay_summary)

missing_delays = operated_flights["DEP_DELAY"].isna().sum()
print(missing_delays)

# ROUTE-LEVEL COMPARISONS

route_summary = operated_flights.groupby(["OP_UNIQUE_CARRIER", "ORIGIN", "DEST"]).agg(
    average_delay = pd.NamedAgg(column="DEP_DELAY", aggfunc="mean"),
    total_flights = pd.NamedAgg(column="OP_CARRIER_FL_NUM", aggfunc="size"),
    delayed_flights = pd.NamedAgg(column="DEP_DELAY", aggfunc= lambda x: (x >= 15).sum()),
    delay_rate = pd.NamedAgg(column="DEP_DELAY", aggfunc= lambda x :  (x >= 15).sum() / x.shape[0] * 100)
)

route_summary = route_summary[route_summary["total_flights"] >= 100]

print(route_summary.loc["B6"])
print(route_summary.loc["WN"])

b6_routes = route_summary.loc["B6"]
wn_routes = route_summary.loc["WN"]

shared_routes = b6_routes.index.intersection(wn_routes.index)

print("Qualifiying routes:" , len(route_summary))
print("Total shared routes:", len(shared_routes))
print("Shared routes:", shared_routes)

b6_comparison = b6_routes.loc[shared_routes]
wn_comparison = wn_routes.loc[shared_routes]

print("B6 Performance", b6_comparison)
print("WN Performance", wn_comparison)

b6_total_flights = b6_comparison["total_flights"].sum()
b6_total_delayed = b6_comparison["delayed_flights"].sum()

wn_total_flights = wn_comparison["total_flights"].sum()
wn_total_delayed = wn_comparison["delayed_flights"].sum()

b6_rate = (b6_total_delayed / b6_total_flights) * 100
wn_rate = (wn_total_delayed / wn_total_flights) * 100

print("B6 total flights:", b6_total_flights)
print("B6 delayed flights:", b6_total_delayed)
print("B6 combined delay rate:", b6_rate)

print("WN total flights:", wn_total_flights)
print("WN delayed flights:", wn_total_delayed)
print("WN combined delay rate:", wn_rate)

standardized_b6 = b6_comparison["delay_rate"].mean()

standardized_wn = wn_comparison["delay_rate"].mean()

print(standardized_b6)
print(standardized_wn)

# EXTREME DELAY INVESTIGATION / SENSITIVITY ANALYSIS

extremely_delay_summary = operated_flights.groupby(["OP_UNIQUE_CARRIER"]).agg(
    q90 = pd.NamedAgg(column="DEP_DELAY", aggfunc= lambda x: (x.quantile(0.90))),
    q95 = pd.NamedAgg(column="DEP_DELAY", aggfunc= lambda x: (x.quantile(0.95))),
    q99 = pd.NamedAgg(column="DEP_DELAY", aggfunc= lambda x: (x.quantile(0.99))),
    extremely_delayed = pd.NamedAgg(column="DEP_DELAY", aggfunc= lambda x: (x >= 120).sum()),
    extremely_delayed_rate = pd.NamedAgg(column="DEP_DELAY", aggfunc= lambda x :  (x >= 120).sum() / x.shape[0] * 100)
)

print(extremely_delay_summary.loc[["OH", "B6", "WN"]])

oh_flights = operated_flights[operated_flights["OP_UNIQUE_CARRIER"] == "OH"]
oh_without_extreme = oh_flights[oh_flights["DEP_DELAY"] < 120]

print("Original flights:", len(oh_flights))
print("Remaining flights:", len(oh_without_extreme))
print("Excluded flights:", len(oh_flights) - len(oh_without_extreme))

original_oh_avg = oh_flights["DEP_DELAY"].mean()
adjusted_oh_avg = oh_without_extreme["DEP_DELAY"].mean()
average_difference = original_oh_avg - adjusted_oh_avg

print("Original oh avg:", original_oh_avg)
print("Adjusted oh avg:", adjusted_oh_avg)
print("Average Difference:", average_difference)
route_delay_comparison = pd.DataFrame({
    "B6": b6_comparison["delay_rate"],
    "WN": wn_comparison["delay_rate"]
})

print(f"Route Delay Comparison: {route_delay_comparison}")

# DATA VISUALIZATION

fewer_operated_flights = delay_summary[delay_summary["operated_flights"] >= 1000].sort_values(by="delay_rate", ascending=False)

plt.figure(figsize=(12,6))
delay_summer_bar = plt.bar(fewer_operated_flights.index, fewer_operated_flights["delay_rate"])
plt.bar_label(delay_summer_bar, fmt="%.2f%%")
plt.xticks(rotation=45)
plt.title("Percentage of Flights Delayed by Airline")
plt.xlabel("Airlines")
plt.ylabel("Percentage of flights delayed by at least 15 minutes")
plt.tight_layout()
plt.savefig(
    "outputs/figures/airline_delay_rates.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()


x = np.arange(len(route_delay_comparison))
plt.figure(figsize=(12,6))
width = 0.40
plt.bar(x - width / 2, route_delay_comparison["B6"], width, label="B6")
plt.bar(x + width / 2, route_delay_comparison["WN"], width, label="WN")

route_labels = [f" {origin} - {dest}"
                for origin, dest in route_delay_comparison.index
                ]
plt.xticks(x, route_labels, rotation=45 )
plt.title("Percentage of Flights Delayed in Shared Routes Between B6 and WN")
plt.xlabel("Shared Routes")
plt.ylabel("Percentage of flights delayed by at least 15 minutes")
plt.legend()
plt.tight_layout()
plt.savefig(
    "outputs/figures/shared_route_comparison.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# Route Performance Gap Analysis

route_delay_comparison["delay_gap_pp"] = b6_comparison["delay_rate"] - wn_comparison["delay_rate"]

route_delay_comparison["absolute_gap_pp"] = route_delay_comparison["delay_gap_pp"].abs()

route_delay_comparison = route_delay_comparison.sort_values(by="absolute_gap_pp", ascending=False)


route_delay_comparison["B6_flights"] = b6_comparison["total_flights"]
route_delay_comparison["WN_flights"] = wn_comparison["total_flights"]

route_delay_comparison["B6_delayed"] = b6_comparison["delayed_flights"]
route_delay_comparison["WN_delayed"] = wn_comparison["delayed_flights"]
print(route_delay_comparison)

# Statistical Confidence Intervals

b6_delayed = b6_comparison.loc[("MCO","SJU"),  "delayed_flights"] 
b6_n = b6_comparison.loc[("MCO","SJU"), "total_flights"]
b6_p = b6_delayed / b6_n

b6_se = np.sqrt((b6_p * (1 - b6_p)) / b6_n)

b6_ci_lower = b6_p - (1.96 * b6_se)
b6_ci_upper = b6_p + (1.96 * b6_se)

print(f"B6 Confidence Lower:{b6_ci_lower * 100}")
print(f"B6 Confidence Upper:{b6_ci_upper * 100}")

wn_delayed = wn_comparison.loc[("MCO","SJU"),  "delayed_flights"] 
wn_n = wn_comparison.loc[("MCO","SJU"), "total_flights"]
wn_p = wn_delayed / wn_n

wn_se = np.sqrt((wn_p * (1 - wn_p)) / wn_n)

wn_ci_lower = wn_p - (1.96 * wn_se)
wn_ci_upper = wn_p + (1.96 * wn_se)

print(f"WN Confidence Lower:{wn_ci_lower * 100}")
print(f"WN Confidence Upper:{wn_ci_upper * 100}")

delay_difference =  ( wn_p - b6_p) 
difference_se = np.sqrt((wn_se ** 2) + (b6_se ** 2))
difference_ci_lower = delay_difference - (1.96 * difference_se)
difference_ci_upper = delay_difference + (1.96 * difference_se) 

print(f"Delay Difference: {delay_difference * 100}%\n"
      f"Difference in SE: {difference_se}\n"
      f"Difference in CI Lower: {difference_ci_lower * 100}\n"
      f"Difference in CI Upper: {difference_ci_upper * 100}\n"
       )

# Departure Time analysis

mco_sju_flights = operated_flights[(operated_flights["ORIGIN"] == "MCO") & (operated_flights["DEST"] == "SJU") & (operated_flights["OP_UNIQUE_CARRIER"].isin(["B6", "WN"]))].copy()

departure_hours = mco_sju_flights["CRS_DEP_TIME"] // 100
departure_minutes = mco_sju_flights["CRS_DEP_TIME"] % 100

missing_time = mco_sju_flights["CRS_DEP_TIME"].isna().sum()
unverified_hours = (departure_hours > 23).sum()
unverified_minutes = (departure_minutes > 59).sum()
incorrect_time = (mco_sju_flights[mco_sju_flights["CRS_DEP_TIME"] == 2400]).sum()

print("Missing scheduled times:", missing_time)
print("Invalid hours:", unverified_hours)
print("Invalid minutes:", unverified_minutes)
print("Scheduled at 2400:", incorrect_time)

mco_sju_flights["departure_hour"] = mco_sju_flights["CRS_DEP_TIME"] // 100


mco_sju_summary = mco_sju_flights.groupby(["OP_UNIQUE_CARRIER", "departure_hour"]).size()

print(f"MCO-SJU Summary: {mco_sju_summary}")

mco_sju_flights["is_late_departure"] = mco_sju_flights["departure_hour"] >= 15

departure_period_summary = mco_sju_flights.groupby(["OP_UNIQUE_CARRIER", "is_late_departure"]).agg( 
    total_flights = pd.NamedAgg(column="DEP_DELAY", aggfunc="size"),
    delayed_flights = pd.NamedAgg(column="DEP_DELAY", aggfunc=lambda x : ((x >= 15).sum())),
    delay_rate = pd.NamedAgg(column="DEP_DELAY", aggfunc= lambda x: (x >= 15).sum() / x.shape[0] * 100)
)

print(departure_period_summary)

b6_early_rate = departure_period_summary.loc[("B6", False), "delay_rate"]
b6_late_rate = departure_period_summary.loc[("B6", True), "delay_rate"]
wn_early_flights = departure_period_summary.loc[("WN", False), "total_flights"]
wn_late_flights = departure_period_summary.loc[("WN", True), "total_flights"]

adjusted_b6_rate = ((b6_early_rate * wn_early_flights) + (b6_late_rate * wn_late_flights)) / (wn_early_flights + wn_late_flights)

print(f"Adjusted B6 Rate: {adjusted_b6_rate}")


b6_rates = [departure_period_summary.loc[("B6", False), "delay_rate"], departure_period_summary.loc[("B6", True), "delay_rate"]]
wn_rates = [departure_period_summary.loc[("WN", False), "delay_rate"], departure_period_summary.loc[("WN", True), "delay_rate"]]

# Last Departure Time Visualization

time_labels = ["Before 3 PM", "3 PM or Later"]
x = np.arange(len(time_labels))
width = 0.40

plt.figure(figsize=(12,6))
plt.bar(x - width / 2, b6_rates, width, label="B6")
plt.bar(x + width / 2, wn_rates, width, label="WN")

plt.xticks(x, time_labels)
plt.title("Departure Delay Rates for MCO-SJU by Time Period")
plt.xlabel("Departure Period")
plt.ylabel("Percentage of Flights Delayed by at Least 15 Minutes")
plt.legend()
plt.tight_layout()
plt.savefig(
    "outputs/figures/Departure_Time_comparison.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
