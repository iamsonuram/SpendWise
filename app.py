import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------

st.set_page_config(
    page_title="SpendWise",
    page_icon="💰",
    layout="wide"
)

# ---------------------------------------
# CUSTOM CSS
# ---------------------------------------

st.markdown("""
<style>

/* ---------------- App Background ---------------- */

.stApp{
    background:#F5F7FB;
}

/* ---------------- Main Container ---------------- */

.block-container{
    padding-top:2rem;
    padding-left:2.5rem;
    padding-right:2.5rem;
}

/* Hide Streamlit Header */

header{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

/* ---------------- Metrics ---------------- */

div[data-testid="stMetric"]{

    background:white;

    padding:20px;

    border-radius:18px;

    border:1px solid #ECECEC;

    box-shadow:0px 8px 20px rgba(0,0,0,.05);

}

div[data-testid="stMetric"]:hover{

    transform:translateY(-3px);

    transition:.25s;

}

/* ---------------- Charts ---------------- */

.js-plotly-plot{

    border-radius:20px;

}

/* ---------------- Dataframe ---------------- */

div[data-testid="stDataFrame"]{

    border-radius:20px;

}

</style>
""",unsafe_allow_html=True)

# ---------------------------------------
# LOAD DATA
# ---------------------------------------

sheet_url = "https://docs.google.com/spreadsheets/d/1_OkomrlLGmqiX9lO5bb8qUBKQCLMTA6B9fMgwCVnwYQ/export?format=csv"

try:

    df = pd.read_csv(sheet_url)

    df["Date"] = pd.to_datetime(df["Date"])

except:

    st.error("Couldn't connect Google Sheet")
    st.stop()

# ---------------------------------------
# HEADER
# ---------------------------------------

col1, col2 = st.columns([6,1])

with col1:
    st.title("💰 SpendWise")
    st.caption("Track • Analyze • Save • Grow")

with col2:
    st.metric("Transactions", len(df))

st.divider()

# ---------------------------------------
# PERSON SELECTOR
# ---------------------------------------
person = st.segmented_control(
    "",
    options=["👩 Sonika", "👨 Puneeth"],
    default="👩 Sonika"
)

person = person.replace("👩 ", "").replace("👨 ", "")

filtered_df = df[df["Person"] == person]

# ---------------------------------------
# FILTERS
# ---------------------------------------

st.markdown("### 📅 Filters")
st.markdown("<br>", unsafe_allow_html=True)
c1,c2,c3 = st.columns(3)

with c1:

    month = st.selectbox(
        "Month",
        sorted(filtered_df["Month"].unique())
    )

with c2:

    year = st.selectbox(
        "Year",
        sorted(filtered_df["Year"].unique())
    )

with c3:

    expense_type = st.selectbox(
        "Expense Type",
        ["All"] +
        sorted(filtered_df["Expense Type"].unique())
    )

filtered_df = filtered_df[
    (filtered_df["Month"]==month) &
    (filtered_df["Year"]==year)
]

if expense_type!="All":

    filtered_df = filtered_df[
        filtered_df["Expense Type"]==expense_type
    ]

# ---------------------------------------
# KPI CALCULATIONS
# ---------------------------------------

total_expense = filtered_df["Amount (₹)"].sum()

transactions = len(filtered_df)

avg_spend = round(filtered_df["Amount (₹)"].mean(),2)

highest = filtered_df["Amount (₹)"].max()

# ---------------------------------------
# KPI CARDS
# ---------------------------------------

st.markdown("## 📊 Financial Overview")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "💸 Total Expense",
        f"₹ {total_expense:,.0f}"
    )

with k2:
    st.metric(
        "🧾 Transactions",
        transactions
    )

with k3:
    st.metric(
        "📈 Average Spend",
        f"₹ {avg_spend:,.0f}"
    )

with k4:
    st.metric(
        "🔥 Highest Spend",
        f"₹ {highest:,.0f}"
    )


##########################################################
# CHARTS
##########################################################

st.divider()

left,right = st.columns([2.2,1])

##########################################################
# EXPENSE TREND
##########################################################

with left:

    st.subheader("📈 Expense Trend")

    trend = (
        filtered_df
        .groupby("Date",as_index=False)["Amount (₹)"]
        .sum()
    )

    fig = px.area(

        trend,

        x="Date",

        y="Amount (₹)",

        line_shape="spline",

        markers=True,

        color_discrete_sequence=["#00AA91"]

    )

    fig.update_traces(

        line=dict(width=4),

        fillcolor="rgba(0,170,145,0.18)",

        marker=dict(size=8)

    )

    fig.update_layout(

        height=380,

        paper_bgcolor="white",

        plot_bgcolor="white",

        margin=dict(

            l=10,

            r=10,

            t=10,

            b=10

        ),

        xaxis_title="",

        yaxis_title="",

        hovermode="x unified",

        showlegend=False

    )

    fig.update_xaxes(

        showgrid=False

    )

    fig.update_yaxes(

        gridcolor="#ECECEC"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

##########################################################
# DONUT
##########################################################

with right:

    st.subheader("🍩 Category Breakdown")

    category = (

        filtered_df

        .groupby("Category")["Amount (₹)"]

        .sum()

        .reset_index()

    )

    colors = [

        "#00AA91",

        "#3B82F6",

        "#F59E0B",

        "#EF4444",

        "#8B5CF6",

        "#14B8A6",

        "#EC4899",

        "#6B7280"

    ]

    donut = px.pie(

        category,

        values="Amount (₹)",

        names="Category",

        hole=.65,

        color_discrete_sequence=colors

    )

    donut.update_traces(

        textposition="inside",

        textinfo="percent"

    )

    donut.update_layout(

        height=380,

        margin=dict(

            l=10,

            r=10,

            t=10,

            b=10

        ),

        paper_bgcolor="white",

        showlegend=True

    )

    st.plotly_chart(
        donut,
        use_container_width=True
    )

##########################################################
# SECOND ROW
##########################################################

left2, right2 = st.columns([2.2, 1])

##########################################################
# MULTIPLE TAB VISUALS
##########################################################

with left2:

    tab1, tab2, tab3 = st.tabs([
        "📅 Spending Pattern",
        "🎯 Essentials vs Lifestyle",
        "💎 Biggest Purchases"
    ])

    ##################################################
    # TAB 1 - WEEKDAY SPENDING
    ##################################################

    with tab1:

        weekday_order = [
            "Monday","Tuesday","Wednesday",
            "Thursday","Friday","Saturday","Sunday"
        ]

        weekday = (
            filtered_df
            .groupby("Day")["Amount (₹)"]
            .sum()
            .reindex(weekday_order)
            .reset_index()
        )

        fig = px.bar(
            weekday,
            x="Amount (₹)",
            y="Day",
            orientation="h",
            color="Amount (₹)",
            color_continuous_scale="Tealgrn",
            text_auto=".2s"
        )

        fig.update_layout(
            height=320,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0,r=0,t=10,b=0),
            coloraxis_showscale=False,
            xaxis_title="",
            yaxis_title=""
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar":False}
        )

    ##################################################
    # TAB 2 - EXPENSE TYPE
    ##################################################

    with tab2:

        expense = (
            filtered_df
            .groupby("Expense Type")["Amount (₹)"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            expense,
            x="Expense Type",
            y="Amount (₹)",
            color="Expense Type",
            text_auto=".2s"
        )

        fig.update_layout(
            height=320,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            margin=dict(l=0,r=0,t=10,b=0),
            xaxis_title="",
            yaxis_title=""
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar":False}
        )

    ##################################################
    # TAB 3 - TOP EXPENSES
    ##################################################

    with tab3:

        top = (
            filtered_df
            .sort_values("Amount (₹)", ascending=False)
            .head(10)
        )

        fig = px.bar(
            top,
            x="Amount (₹)",
            y="Description",
            orientation="h",
            color="Amount (₹)",
            color_continuous_scale="Tealgrn",
            hover_data={
                "Date": True,
                "Category": True,
                "Sub Category": True,
                "Related To": True,
                "Amount (₹)": ":,.0f"
            }
        )

        fig.update_layout(
            height=320,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0,r=0,t=10,b=0),
            coloraxis_showscale=False,
            xaxis_title="",
            yaxis_title=""
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar":False}
        )


##########################################################
# MONTHLY COMPARISON
##########################################################

with right2:

    st.subheader("📊 Monthly Comparison")

    monthly = (
        df[df["Person"] == person]
        .groupby("Month")["Amount (₹)"]
        .sum()
        .reset_index()
    )

    order = [
        "January","February","March",
        "April","May","June",
        "July","August",
        "September","October",
        "November","December"
    ]

    monthly["Month"] = pd.Categorical(
        monthly["Month"],
        categories=order,
        ordered=True
    )

    monthly = monthly.sort_values("Month")

    fig = px.bar(
        monthly,
        x="Month",
        y="Amount (₹)",
        color="Amount (₹)",
        text_auto=".2s",
        color_continuous_scale="Tealgrn"
    )

    fig.update_layout(
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0,r=0,t=20,b=0),
        coloraxis_showscale=False,
        xaxis_title="",
        yaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar":False}
    )

##########################################################
# TRANSACTION TABLE
##########################################################

st.divider()

st.subheader("📋 Transaction Explorer")

search = st.text_input(
    "🔍 Search Description",
    placeholder="Search for Pizza, Laptop, Temple..."
)

table_df = filtered_df.copy()

if search:
    table_df = table_df[
        table_df["Description"].str.contains(search, case=False, na=False)
    ]

st.data_editor(
    table_df.sort_values("Date", ascending=False),
    use_container_width=True,
    hide_index=True,
    disabled=True
)