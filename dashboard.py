import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


def create_byseason_byworkingday(df):
    season_map = {1: "springer", 2: "summer", 3: "fall", 4: "winter"}
    wokingday_map = {1: "Working", 0: "Holidays"}
    create_season_workingday_df = df[["dteday", "season", "workingday", "cnt"]]
    create_season_workingday_df["season"] = create_season_workingday_df["season"].map(season_map)
    create_season_workingday_df["workingday"] = create_season_workingday_df["workingday"].map(
        wokingday_map
    )
    return create_season_workingday_df


def create_rfm_df(df):
    create_rfm_df = df.groupby(by="registered", as_index=False).agg(
        {
            "dteday": "max",  # mengambil tanggal order terakhir
            "instant": "nunique",
            "cnt": "sum",
        }
    )
    create_rfm_df.columns = ["users", "max_used_timestamp", "frequency", "monetary"]

    create_rfm_df["max_used_timestamp"] = create_rfm_df["max_used_timestamp"].dt.date
    recent_date = df["dteday"].dt.date.max()
    create_rfm_df["recency"] = create_rfm_df["max_used_timestamp"].apply(
        lambda x: (recent_date - x).days
    )
    create_rfm_df.drop("max_used_timestamp", axis=1, inplace=True)

    return create_rfm_df

all_df = pd.read_csv("./Belajar_Analisis_Dengan_Python/Tugas/day.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    st.image("./Belajar_Analisis_Dengan_Python/Tugas/logo_toko.png")

    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

main_df = all_df[
    (all_df["dteday"] >= str(start_date)) & (all_df["dteday"] <= str(end_date))
]

season_workingday_df = create_byseason_byworkingday(main_df)
rfm_df = create_rfm_df(main_df)


st.header("Sharing Bike Analisis")
st.subheader("Jumlah penyewaan sepeda Berdasarkan Berdasarkan berbagai musim")
col1, col2, col3, col4 = st.columns(4)
with col1:
    season_df = (
        main_df.groupby(["season"])
        .agg(cnt_sum=("cnt", "sum"))
        .reset_index()
        .query("season == 1")
    )
    season_name = season_df.season.map(
        {1: "springer", 2: "summer", 3: "fall", 4: "winter"}
    ).values[0]
    st.metric(f"Total Users in {season_name}", value=season_df.cnt_sum)

with col2:
    season_df = (
        main_df.groupby(["season"])
        .agg(cnt_sum=("cnt", "sum"))
        .reset_index()
        .query("season == 2")
    )
    season_name = season_df.season.map(
        {1: "springer", 2: "summer", 3: "fall", 4: "winter"}
    ).values[0]
    st.metric(f"Total Users in {season_name}", value=season_df.cnt_sum)

with col3:
    season_df = (
        main_df.groupby(["season"])
        .agg(cnt_sum=("cnt", "sum"))
        .reset_index()
        .query("season == 3")
    )
    season_name = season_df.season.map(
        {1: "springer", 2: "summer", 3: "fall", 4: "winter"}
    ).values[0]
    st.metric(f"Total Users in {season_name}", value=season_df.cnt_sum)

with col4:
    season_df = (
        main_df.groupby(["season"])
        .agg(cnt_sum=("cnt", "sum"))
        .reset_index()
        .query("season == 4")
    )
    season_name = season_df.season.map(
        {1: "springer", 2: "summer", 3: "fall", 4: "winter"}
    ).values[0]
    st.metric(f"Total Users in {season_name}", value=season_df.cnt_sum)


g = sns.catplot(data=season_workingday_df, x="season", y="cnt", kind="bar")

g.figure.subplots_adjust(top=0.85)
g.figure.suptitle("Jumlah penyewaan sepeda Berdasarkan Berdasarkan berbagai musim")
st.pyplot(g)

st.subheader("Jumlah penyewaan sepeda Berdasarkan Berdasarkan Hari Kerja dan Libur")
col1, col2 = st.columns(2)
with col1:
    workingday_df = (
        main_df.groupby(["workingday"])
        .agg(cnt_sum=("cnt", "sum"))
        .reset_index()
        .query("workingday == 0")
    )
    workingday_name = workingday_df.workingday.map(
        {1: "Working", 0: "Holidays"}
    ).values[0]
    st.metric(f"Total Users on {workingday_name}", value=workingday_df.cnt_sum)

with col2:
    workingday_df = (
        main_df.groupby(["workingday"])
        .agg(cnt_sum=("cnt", "sum"))
        .reset_index()
        .query("workingday == 1")
    )
    workingday_name = workingday_df.workingday.map(
        {1: "Working", 0: "Holidays"}
    ).values[0]
    st.metric(f"Total Users on {workingday_name}", value=workingday_df.cnt_sum)

g = sns.catplot(data=season_workingday_df, x="workingday", y="cnt", kind="bar")

g.figure.subplots_adjust(top=0.85)
g.figure.suptitle(
    "Jumlah penyewaan sepeda Berdasarkan Berdasarkan Hari Kerja dan Libur"
)
st.pyplot(g)

st.subheader("Best User Based on RFM Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_monetary = rfm_df.monetary.mean()
    st.metric("Average Monetary", value=avg_monetary)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

sns.barplot(
    y="recency",
    x="users",
    data=rfm_df.sort_values(by="recency", ascending=True).head(5),
    palette=colors,
    ax=ax[0],
)
ax[0].set_ylabel(None)
ax[0].set_xlabel("users", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis="y", labelsize=30)
ax[0].tick_params(axis="x", labelsize=35)

sns.barplot(
    y="frequency",
    x="users",
    data=rfm_df.sort_values(by="frequency", ascending=False).head(5),
    palette=colors,
    ax=ax[1],
)
ax[1].set_ylabel(None)
ax[1].set_xlabel("users", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis="y", labelsize=30)
ax[1].tick_params(axis="x", labelsize=35)

sns.barplot(
    y="monetary",
    x="users",
    data=rfm_df.sort_values(by="monetary", ascending=False).head(5),
    palette=colors,
    ax=ax[2],
)
ax[2].set_ylabel(None)
ax[2].set_xlabel("users", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis="y", labelsize=30)
ax[2].tick_params(axis="x", labelsize=35)

st.pyplot(fig)

st.caption("Copyright © Alichwan 2024")
