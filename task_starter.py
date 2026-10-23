# TASK: the 30-minute data story app run: streamlit run task_starter.py
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="My data story", layout="wide")

df = px.data.tips() # B: restaurant owner
st.title("Sunday showed the highest average party size and tip of $3.26")
story, explore = st.tabs(["The story", "Explore it yourself"])

with story:
    by_day = df.groupby(['day', 'size'], as_index=False)['tip'].mean()
    fig = px.line(by_day, x="size", y="tip", color="day",
                  labels={"size": "Party Size", "tip": "Average tip ($)", "day": "Day of the Week"})
    st.plotly_chart(fig)
    st.markdown("Generally as party size increases, average tip increases. Sunday has the highest average part size and average tip.")
    st.caption("Source: Tips, via plotly.express. Restaurant bill tips.")



with explore:
    st.header("How Party Size and Day Affect Tips")

    # Dropdown filters
    col1, col2 = st.columns(2)

    with col1:
        selected_day = st.selectbox(
            "Day of the Week",
            ["All"] + sorted(df["day"].unique().tolist()),
            key="day_filter"
        )

    with col2:
        selected_size = st.selectbox(
            "Party Size",
            ["All"] + sorted(df["size"].unique().tolist()),
            key="size_filter"
        )

    # Apply filters
    filtered = df.copy()

    if selected_day != "All":
        filtered = filtered[filtered["day"] == selected_day]

    if selected_size != "All":
        filtered = filtered[
            filtered["size"] == int(selected_size)
        ] if selected_size != "All" else filtered

    # Check filtered data
    st.write(f"Number of matching bills: {len(filtered)}")

    if filtered.empty:
        st.warning("No data matches these filters.")
    else:
        # Recalculate average tips using filtered data
        avg_tips = filtered.groupby(
            ["day", "size"], as_index=False
        )["tip"].mean()

        # Update bar chart
        fig = px.bar(
            avg_tips,
            x="size",
            y="tip",
            color="day",
            barmode="group",
            labels={
                "size": "Party Size",
                "tip": "Average Tip ($)",
                "day": "Day of Week"
            },
            title="Average Tip by Party Size and Day"
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            key="tips_bar_chart"
        )
