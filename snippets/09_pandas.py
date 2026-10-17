# Part 10 - pandas quick start (the build runs this in a temp folder)

# %% pd_options hidden
import pandas as pd

pd.set_option("display.width", 90)
pd.set_option("display.max_columns", 10)

# %% pd_create
import pandas as pd

df = pd.DataFrame({
    "task":    ["Spec", "Design", "Build", "Test", "Docs", "Review"],
    "owner":   ["Ali", "Sara", "Ali", "Mia", "Sara", "Mia"],
    "status":  ["done", "done", "open", "open", "done", None],
    "planned": [8, 16, 40, 24, 6, 4],
    "actual":  [10, 15, 52, None, 6, 5],
    "due":     ["2026-10-01", "2026-10-05", "2026-10-20",
                "2026-10-10", "2026-10-12", "2026-10-15"],
})
df.to_csv("tasks.csv", index=False)
df = pd.read_csv("tasks.csv")        # in the interview you start here
print(df.head(3))
print(df.shape)

# %% pd_inspect
print(df.dtypes)
print(df.isna().sum()[lambda s: s > 0])      # only columns with gaps
print(df["owner"].value_counts())
print(df["planned"].describe()[["mean", "min", "max"]])

# %% pd_select
print(df["task"].tolist())
print(df.loc[df["owner"] == "Ali", ["task", "planned"]])
print(df.iloc[0]["task"], df.loc[2, "owner"])
print(df[(df["status"] == "open") & (df["planned"] > 30)]["task"].tolist())
print(df[df["owner"].isin(["Mia", "Sara"])].shape)

# %% pd_clean
df["status"] = df["status"].fillna("unknown")
df["actual"] = df["actual"].fillna(df["planned"])     # assume on plan
df["due"] = pd.to_datetime(df["due"])
df["overrun_pct"] = ((df["actual"] - df["planned"])
                     / df["planned"] * 100).round(1)
print(df[["task", "status", "actual", "overrun_pct"]])

# %% pd_group
summary = (df.groupby("owner")
             .agg(tasks=("task", "count"),
                  planned=("planned", "sum"),
                  actual=("actual", "sum"))
             .sort_values("actual", ascending=False))
print(summary)
print(df.groupby("status")["planned"].mean().round(1))

# %% pd_dates
today = pd.Timestamp("2026-10-17")
overdue = df[(df["status"] != "done") & (df["due"] < today)]
print(overdue[["task", "owner", "due"]])

df["days_left"] = (df["due"] - today).dt.days
df["weekday"] = df["due"].dt.day_name()
upcoming = df[(df["status"] != "done") & (df["days_left"] >= 0)]
print(upcoming[["task", "days_left", "weekday"]])

# %% pd_apply_merge
df["size"] = df["planned"].apply(lambda h: "large" if h >= 20 else "small")
teams = pd.DataFrame({"owner": ["Ali", "Sara", "Mia"],
                      "team": ["Dev", "UX", "QA"]})
merged = df.merge(teams, on="owner", how="left")       # like SQL JOIN
print(merged[["task", "owner", "team", "size"]].head(4))
print(pd.pivot_table(merged, index="team", columns="status",
                     values="planned", aggfunc="sum", fill_value=0))
