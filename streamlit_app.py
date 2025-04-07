import streamlit as st
import duckdb
import altair as alt

st.set_page_config(layout="wide")
DUCKDB_FILE = "dev.duckdb"


# ----------------------
# Data Loading
# ----------------------
@st.cache_data
def load_table(query):
    with duckdb.connect(DUCKDB_FILE) as conn:
        return conn.execute(query).fetchdf()


# ----------------------
# Visuals
# ----------------------
def render_metrics(total_rev, total_res, avg_rev, currency):
    cols = st.columns(3)
    cols[0].metric(f"Total Revenue ({currency})", f"{total_rev / 1e6:,.2f}M")
    cols[1].metric("Total Reservations", f"{total_res / 1000:,.1f}K")
    cols[2].metric("Avg Rev/Reservation", f"{avg_rev:,.2f}")


def common_line_chart(df, value_col, chart_title, currency):
    if df.empty:
        st.write("No data available.")
        return
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X("stay_date:T", title="Stay Date"),
        y=alt.Y(f"{value_col}:Q", title=f"{chart_title} ({currency})"),
        tooltip=["stay_date:T", f"{value_col}:Q"]
    ).interactive()
    st.altair_chart(chart, use_container_width=True)


def area_chart(df, category, value_col, currency, title):
    if df.empty:
        st.write("No data available.")
        return
    chart = alt.Chart(df).mark_area(opacity=0.8).encode(
        x=alt.X("stay_date:T", title="Stay Date"),
        y=alt.Y(f"{value_col}:Q", stack="zero", title=f"{title} ({currency})"),
        color=alt.Color(f"{category}:N", legend=alt.Legend(orient='right', direction='vertical')),
        tooltip=["stay_date:T", f"{category}:N", f"{value_col}:Q"]
    ).interactive()
    st.altair_chart(chart, use_container_width=True)


# ----------------------
# Main Sections
# ----------------------
def group_analytics_section(df_group, df_property):
    if df_group.empty or df_property.empty:
        st.write("No data available.")
        return
    st.header("Group Revenue Analytics")
    group_choice = st.selectbox("Select Property Group:", sorted(df_group["property_group_name"].unique()))

    df_filtered = df_group[df_group["property_group_name"] == group_choice]

    total_rev = df_filtered["total_revenue_base_currency"].sum()
    total_res = df_filtered["reservations"].sum()
    avg_rev = total_rev / total_res if total_res else 0
    base_currency = df_filtered["base_currency"].iloc[0]

    render_metrics(total_rev, total_res, avg_rev, base_currency)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Group Revenue")
        common_line_chart(df_filtered, "total_revenue_base_currency", "Group Revenue", base_currency)

    with col2:
        st.subheader("Revenue by Property")
        prop_df = df_property[df_property["property_group_name"] == group_choice]
        area_chart(prop_df, "property_name", "total_revenue_base_currency", base_currency, "Revenue by Property")


def property_analytics_section(df_property, df_inventory):
    if df_property.empty or df_inventory.empty:
        st.write("No data available.")
        return

    st.header("Property Revenue Analytics")
    property_choice = st.selectbox("Select Property:", sorted(df_property["property_name"].unique()))

    df_prop_filtered = df_property[df_property["property_name"] == property_choice]

    base_currency = df_prop_filtered["base_currency"].iloc[0]
    local_currency = df_prop_filtered["local_currency"].iloc[0]

    disable_checkbox = (base_currency == local_currency)
    show_local_currency = st.checkbox(f"Show Revenue in Local Currency ({local_currency})", disabled=disable_checkbox)

    revenue_col = "total_revenue_base_currency"
    select_currency = base_currency
    if show_local_currency:
        select_currency = local_currency
        revenue_col = "total_revenue_local_currency"

    total_rev = df_prop_filtered[revenue_col].sum()
    total_res = df_prop_filtered["reservations"].sum()
    avg_rev = total_rev / total_res if total_res else 0

    render_metrics(total_rev, total_res, avg_rev, select_currency)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Property Revenue")
        common_line_chart(df_prop_filtered, revenue_col, "Property Revenue", select_currency)

    with col2:
        st.subheader("Revenue by Inventory")
        inv_df = df_inventory[df_inventory["property_name"] == property_choice]
        area_chart(inv_df, "inventory_name", revenue_col, select_currency, "Revenue by Inventory")


# ----------------------
# Main
# ----------------------
def main():
    df_group = load_table("""
        SELECT 
            stay_date, 
            property_group_name, 
            total_revenue_base_currency, 
            reservations, 
            base_currency 
        FROM agg__revenue_by_property_group
    """)
    df_property = load_table("""
        SELECT 
            stay_date, 
            property_group_name, 
            property_name, 
            total_revenue_local_currency, 
            total_revenue_base_currency, 
            reservations, 
            local_currency,
            base_currency
        FROM agg__revenue_by_property
    """)
    df_inventory = load_table("""
        SELECT 
            stay_date, 
            property_name, 
            inventory_name, 
            total_revenue_base_currency,
            total_revenue_local_currency
        FROM agg__revenue_by_inventory
    """)

    if df_group.empty or df_property.empty or df_inventory.empty:
        st.write("No data available.")
        return

    min_date = df_property["stay_date"].min().date()
    max_date = df_property["stay_date"].max().date()

    dates = st.date_input("Select Date Range", value=(min_date, max_date))

    start_date = min_date
    end_date = max_date

    if isinstance(dates, tuple) and len(dates) == 2:
        start_date, end_date = dates

    for df in [df_group, df_property, df_inventory]:
        df.query("@start_date <= stay_date <= @end_date", inplace=True)

    group_analytics_section(df_group, df_property)
    st.markdown("---")
    property_analytics_section(df_property, df_inventory)


if __name__ == "__main__":
    main()
