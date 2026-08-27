import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import yfinance as yf
from datetime import datetime

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="E-Commerce Business Dashboard",
    page_icon="🛒",
    layout="wide"
)

# =========================================================
# SAMPLE DATA
# =========================================================

@st.cache_data
def generate_data():

    np.random.seed(42)

    products = [
        "Laptop",
        "Smartphone",
        "Headphones",
        "Smart Watch",
        "Keyboard",
        "Mouse",
        "Tablet",
        "Monitor",
        "Shoes",
        "Backpack"
    ]

    brands = {
        "Laptop": ["Dell", "HP", "Lenovo", "Apple"],
        "Smartphone": ["Samsung", "Apple", "OnePlus", "Xiaomi"],
        "Headphones": ["Sony", "JBL", "Boat", "Sennheiser"],
        "Smart Watch": ["Apple", "Samsung", "Noise", "Boat"],
        "Keyboard": ["Logitech", "HP", "Dell", "Razer"],
        "Mouse": ["Logitech", "HP", "Dell", "Razer"],
        "Tablet": ["Apple", "Samsung", "Lenovo", "Xiaomi"],
        "Monitor": ["Dell", "LG", "Samsung", "Acer"],
        "Shoes": ["Nike", "Adidas", "Puma", "Reebok"],
        "Backpack": ["Wildcraft", "Skybags", "American Tourister", "Nike"]
    }

    categories = {
        "Laptop": "Electronics",
        "Smartphone": "Electronics",
        "Headphones": "Electronics",
        "Smart Watch": "Electronics",
        "Keyboard": "Accessories",
        "Mouse": "Accessories",
        "Tablet": "Electronics",
        "Monitor": "Electronics",
        "Shoes": "Fashion",
        "Backpack": "Fashion"
    }

    n = 1000

    dates = pd.date_range(
        start="2025-01-01",
        end="2025-12-31",
        periods=n
    )

    product_data = np.random.choice(products, n)

    brand_data = [
        np.random.choice(brands[product])
        for product in product_data
    ]

    data = pd.DataFrame({
        "Order_ID": [
            f"ORD{i+1:04d}" for i in range(n)
        ],

        "Order_Date": dates,

        "Customer_ID": [
            f"CUST{np.random.randint(1, 251):03d}"
            for _ in range(n)
        ],

        "Product": product_data,

        "Brand": brand_data,

        "Category": [
            categories[p]
            for p in product_data
        ],

        "Quantity": np.random.randint(1, 6, n),

        "Unit_Price": np.random.randint(
            500,
            50000,
            n
        ),

        "Location": np.random.choice(
            [
                "Chennai",
                "Bangalore",
                "Hyderabad",
                "Mumbai",
                "Delhi",
                "Kochi"
            ],
            n
        )
    })

    data["Total_Sales"] = (
        data["Quantity"] *
        data["Unit_Price"]
    )

    data["Month"] = (
        data["Order_Date"]
        .dt.strftime("%b")
    )

    data["Month_Number"] = (
        data["Order_Date"]
        .dt.month
    )

    return data


df = generate_data()

# =========================================================
# SESSION STATE
# =========================================================

if "reviews" not in st.session_state:

    st.session_state.reviews = [
        {
            "Customer": "CUST001",
            "Product": "Laptop",
            "Brand": "Dell",
            "Rating": 5,
            "Review": "Good performance and build quality."
        },

        {
            "Customer": "CUST002",
            "Product": "Smartphone",
            "Brand": "Samsung",
            "Rating": 4,
            "Review": "Good phone with useful features."
        },

        {
            "Customer": "CUST003",
            "Product": "Headphones",
            "Brand": "Sony",
            "Rating": 5,
            "Review": "Excellent sound quality."
        }
    ]


if "proposals" not in st.session_state:

    st.session_state.proposals = []


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🛒 Dashboard Menu")

page = st.sidebar.radio(
    "Select Section",
    [
        "📊 Sales Dashboard",
        "🏷️ Brand Analysis",
        "⭐ Product Reviews",
        "🤝 Business Proposals",
        "📈 Stock Market Analysis"
    ]
)

# =========================================================
# SALES DASHBOARD
# =========================================================

if page == "📊 Sales Dashboard":

    st.title(
        "🛒 E-Commerce Sales Analytics Dashboard"
    )

    st.write(
        "Analyse sales, customers, products and "
        "shopping trends."
    )

    # -----------------------------------------------------
    # FILTERS
    # -----------------------------------------------------

    st.sidebar.subheader("Dashboard Filters")

    category_options = [
        "All"
    ] + sorted(
        df["Category"].unique().tolist()
    )

    selected_category = st.sidebar.selectbox(
        "Category",
        category_options
    )

    filtered_df = df.copy()

    if selected_category != "All":

        filtered_df = filtered_df[
            filtered_df["Category"] ==
            selected_category
        ]

    brand_options = [
        "All"
    ] + sorted(
        filtered_df["Brand"].unique().tolist()
    )

    selected_brand = st.sidebar.selectbox(
        "Brand",
        brand_options
    )

    if selected_brand != "All":

        filtered_df = filtered_df[
            filtered_df["Brand"] ==
            selected_brand
        ]

    # -----------------------------------------------------
    # KPIs
    # -----------------------------------------------------

    total_revenue = (
        filtered_df["Total_Sales"].sum()
    )

    total_orders = (
        filtered_df["Order_ID"].nunique()
    )

    total_customers = (
        filtered_df["Customer_ID"].nunique()
    )

    if total_orders > 0:

        average_order_value = (
            total_revenue /
            total_orders
        )

    else:

        average_order_value = 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Revenue",
        f"₹{total_revenue:,.0f}"
    )

    col2.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

    col3.metric(
        "Customers",
        f"{total_customers:,}"
    )

    col4.metric(
        "Average Order Value",
        f"₹{average_order_value:,.0f}"
    )

    st.divider()

    # -----------------------------------------------------
    # MONTHLY SALES
    # -----------------------------------------------------

    st.subheader("📈 Monthly Revenue Trend")

    monthly_sales = (
        filtered_df
        .groupby(
            ["Month_Number", "Month"]
        )["Total_Sales"]
        .sum()
        .reset_index()
        .sort_values("Month_Number")
    )

    fig_monthly = px.line(
        monthly_sales,
        x="Month",
        y="Total_Sales",
        markers=True,
        title="Monthly Revenue"
    )

    fig_monthly.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue (₹)"
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )

    # -----------------------------------------------------
    # CATEGORY AND PRODUCT
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "📊 Revenue by Category"
        )

        category_sales = (
            filtered_df
            .groupby("Category")[
                "Total_Sales"
            ]
            .sum()
            .reset_index()
            .sort_values(
                "Total_Sales",
                ascending=False
            )
        )

        fig_category = px.bar(
            category_sales,
            x="Category",
            y="Total_Sales",
            title="Revenue by Category"
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )

    with col2:

        st.subheader(
            "🏆 Top Products"
        )

        product_sales = (
            filtered_df
            .groupby("Product")[
                "Total_Sales"
            ]
            .sum()
            .reset_index()
            .sort_values(
                "Total_Sales",
                ascending=False
            )
            .head(10)
        )

        fig_products = px.bar(
            product_sales,
            x="Total_Sales",
            y="Product",
            orientation="h",
            title="Top Products"
        )

        st.plotly_chart(
            fig_products,
            use_container_width=True
        )

    # -----------------------------------------------------
    # CUSTOMER LIFETIME VALUE
    # -----------------------------------------------------

    st.subheader(
        "👥 Customer Lifetime Value"
    )

    customer_value = (
        filtered_df
        .groupby("Customer_ID")
        .agg(
            Total_Spent=(
                "Total_Sales",
                "sum"
            ),

            Number_of_Orders=(
                "Order_ID",
                "nunique"
            ),

            Average_Order_Value=(
                "Total_Sales",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            "Total_Spent",
            ascending=False
        )
    )

    st.dataframe(
        customer_value.head(10),
        use_container_width=True
    )

    # -----------------------------------------------------
    # LOCATION
    # -----------------------------------------------------

    st.subheader(
        "📍 Sales by Location"
    )

    location_sales = (
        filtered_df
        .groupby("Location")[
            "Total_Sales"
        ]
        .sum()
        .reset_index()
    )

    fig_location = px.bar(
        location_sales,
        x="Location",
        y="Total_Sales",
        title="Revenue by Location"
    )

    st.plotly_chart(
        fig_location,
        use_container_width=True
    )


# =========================================================
# BRAND ANALYSIS
# =========================================================

elif page == "🏷️ Brand Analysis":

    st.title(
        "🏷️ Brand-wise Product Analysis"
    )

    st.write(
        "Compare products and sales performance "
        "across different brands."
    )

    # -----------------------------------------------------
    # BRAND SALES
    # -----------------------------------------------------

    brand_sales = (
        df
        .groupby("Brand")[
            "Total_Sales"
        ]
        .sum()
        .reset_index()
        .sort_values(
            "Total_Sales",
            ascending=False
        )
    )

    fig_brand = px.bar(
        brand_sales,
        x="Brand",
        y="Total_Sales",
        title="Revenue by Brand"
    )

    fig_brand.update_layout(
        xaxis_title="Brand",
        yaxis_title="Revenue (₹)"
    )

    st.plotly_chart(
        fig_brand,
        use_container_width=True
    )

    # -----------------------------------------------------
    # PRODUCT + BRAND
    # -----------------------------------------------------

    st.subheader(
        "Product Performance by Brand"
    )

    product_brand = (
        df
        .groupby(
            ["Brand", "Product"]
        )["Total_Sales"]
        .sum()
        .reset_index()
    )

    fig_product_brand = px.bar(
        product_brand,
        x="Product",
        y="Total_Sales",
        color="Brand",
        title="Products Differentiated by Brand",
        barmode="group"
    )

    st.plotly_chart(
        fig_product_brand,
        use_container_width=True
    )

    # -----------------------------------------------------
    # BRAND FILTER
    # -----------------------------------------------------

    selected_brand = st.selectbox(
        "Select a Brand",
        sorted(df["Brand"].unique())
    )

    brand_products = df[
        df["Brand"] == selected_brand
    ]

    st.subheader(
        f"Products available from {selected_brand}"
    )

    product_summary = (
        brand_products
        .groupby("Product")
        .agg(
            Orders=(
                "Order_ID",
                "nunique"
            ),

            Quantity=(
                "Quantity",
                "sum"
            ),

            Revenue=(
                "Total_Sales",
                "sum"
            )
        )
        .reset_index()
        .sort_values(
            "Revenue",
            ascending=False
        )
    )

    st.dataframe(
        product_summary,
        use_container_width=True
    )


# =========================================================
# PRODUCT REVIEWS
# =========================================================

elif page == "⭐ Product Reviews":

    st.title(
        "⭐ Product Review System"
    )

    st.write(
        "Customers can review products they have purchased. "
        "Other customers can read these reviews before buying."
    )

    # -----------------------------------------------------
    # EXISTING REVIEWS
    # -----------------------------------------------------

    st.subheader(
        "Customer Reviews"
    )

    if len(st.session_state.reviews) > 0:

        reviews_df = pd.DataFrame(
            st.session_state.reviews
        )

        for _, review in reviews_df.iterrows():

            st.markdown(
                f"### {review['Product']} "
                f"({review['Brand']})"
            )

            st.write(
                f"**Customer:** "
                f"{review['Customer']}"
            )

            st.write(
                f"**Rating:** "
                f"{'⭐' * int(review['Rating'])}"
            )

            st.write(
                f"**Review:** "
                f"{review['Review']}"
            )

            st.divider()

    else:

        st.info(
            "No reviews have been submitted yet."
        )

    # -----------------------------------------------------
    # WRITE REVIEW
    # -----------------------------------------------------

    st.subheader(
        "✍️ Write a Review"
    )

    customer_id = st.text_input(
        "Customer ID",
        placeholder="Example: CUST001"
    )

    # Only customers in the transaction dataset
    customer_list = sorted(
        df["Customer_ID"].unique()
    )

    if customer_id:

        customer_orders = df[
            df["Customer_ID"] ==
            customer_id
        ]

        if len(customer_orders) == 0:

            st.warning(
                "Customer ID not found. "
                "Please enter a valid customer ID."
            )

        else:

            purchased_products = (
                customer_orders[
                    [
                        "Product",
                        "Brand"
                    ]
                ]
                .drop_duplicates()
            )

            st.success(
                "Customer verified. "
                "You can review a purchased product."
            )

            product_choice = st.selectbox(
                "Select Purchased Product",
                purchased_products[
                    "Product"
                ].tolist()
            )

            selected_product = (
                purchased_products[
                    purchased_products["Product"] ==
                    product_choice
                ]
            )

            selected_brand = (
                selected_product[
                    "Brand"
                ].iloc[0]
            )

            rating = st.slider(
                "Rating",
                min_value=1,
                max_value=5,
                value=5
            )

            review_text = st.text_area(
                "Write your review",
                placeholder="Share your experience with this product..."
            )

            if st.button(
                "Submit Review"
            ):

                if review_text.strip() == "":

                    st.error(
                        "Please write a review before submitting."
                    )

                else:

                    new_review = {
                        "Customer": customer_id,
                        "Product": product_choice,
                        "Brand": selected_brand,
                        "Rating": rating,
                        "Review": review_text
                    }

                    st.session_state.reviews.append(
                        new_review
                    )

                    st.success(
                        "Your review has been submitted successfully!"
                    )

                    st.rerun()


# =========================================================
# BUSINESS PROPOSALS
# =========================================================

elif page == "🤝 Business Proposals":

    st.title(
        "🤝 Local Dealer Business Proposal System"
    )

    st.write(
        "Local dealers can contact larger companies "
        "and submit business proposals through this section."
    )

    # -----------------------------------------------------
    # COMPANY LIST
    # -----------------------------------------------------

    companies = [
        "Samsung",
        "Apple",
        "Dell",
        "HP",
        "Lenovo",
        "Sony",
        "LG",
        "Nike",
        "Adidas",
        "Logitech"
    ]

    st.subheader(
        "🏢 Select a Company"
    )

    selected_company = st.selectbox(
        "Company",
        companies
    )

    st.write(
        f"Selected company: **{selected_company}**"
    )

    # -----------------------------------------------------
    # DEALER DETAILS
    # -----------------------------------------------------

    st.subheader(
        "Dealer Information"
    )

    dealer_name = st.text_input(
        "Dealer / Business Name"
    )

    dealer_location = st.text_input(
        "Business Location"
    )

    dealer_email = st.text_input(
        "Business Email"
    )

    dealer_phone = st.text_input(
        "Contact Number"
    )

    # -----------------------------------------------------
    # BUSINESS PROPOSAL
    # -----------------------------------------------------

    st.subheader(
        "Business Proposal"
    )

    proposal_title = st.text_input(
        "Proposal Title",
        placeholder="Example: Regional Distribution Partnership"
    )

    proposal_text = st.text_area(
        "Proposal Details",
        placeholder=(
            "Describe your business, "
            "the partnership you are proposing, "
            "expected order volume, "
            "target market and other relevant information."
        ),
        height=200
    )

    expected_quantity = st.number_input(
        "Expected Monthly Order Quantity",
        min_value=1,
        value=100
    )

    if st.button(
        "📨 Submit Business Proposal"
    ):

        if (
            dealer_name.strip() == "" or
            dealer_email.strip() == "" or
            proposal_title.strip() == "" or
            proposal_text.strip() == ""
        ):

            st.error(
                "Please fill in all required fields."
            )

        else:

            proposal = {
                "Company": selected_company,
                "Dealer": dealer_name,
                "Location": dealer_location,
                "Email": dealer_email,
                "Phone": dealer_phone,
                "Title": proposal_title,
                "Proposal": proposal_text,
                "Expected Monthly Quantity":
                    expected_quantity,
                "Date":
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    )
            }

            st.session_state.proposals.append(
                proposal
            )

            st.success(
                f"Business proposal sent to "
                f"{selected_company} successfully!"
            )

    # -----------------------------------------------------
    # SUBMITTED PROPOSALS
    # -----------------------------------------------------

    st.divider()

    st.subheader(
        "📋 Submitted Business Proposals"
    )

    if len(st.session_state.proposals) == 0:

        st.info(
            "No business proposals have been submitted yet."
        )

    else:

        proposals_df = pd.DataFrame(
            st.session_state.proposals
        )

        st.dataframe(
            proposals_df,
            use_container_width=True
        )
    # =========================================================
# STOCK MARKET ANALYSIS
# =========================================================

elif page == "📈 Stock Market Analysis":


    st.title("📈 Company Stock Market Analysis")

    st.write(
        "View historical stock-price fluctuations of selected "
        "companies for informational reference."
    )

    st.warning(
        "This section displays historical market data only. "
        "It is not financial advice and does not predict future stock prices."
    )

    # -----------------------------------------------------
    # COMPANY STOCK LIST
    # -----------------------------------------------------

    stock_companies = {
        "Apple": "AAPL",
        "Samsung Electronics": "005930.KS",
        "Dell Technologies": "DELL",
        "HP Inc.": "HPQ",
        "Lenovo": "0992.HK",
        "Sony": "6758.T",
        "Nike": "NKE",
        "Adidas": "ADS.DE",
        "Logitech": "LOGI",
        "LG Electronics": "066570.KS"
    }

    selected_company = st.selectbox(
        "Select Company",
        list(stock_companies.keys())
    )

    ticker_symbol = stock_companies[
        selected_company
    ]

    # -----------------------------------------------------
    # TIME PERIOD
    # -----------------------------------------------------

    period_options = {
        "1 Month": "1mo",
        "3 Months": "3mo",
        "6 Months": "6mo",
        "1 Year": "1y",
        "2 Years": "2y",
        "5 Years": "5y"
    }

    selected_period = st.selectbox(
        "Select Historical Period",
        list(period_options.keys()),
        index=3
    )

    period = period_options[
        selected_period
    ]

    # -----------------------------------------------------
    # DOWNLOAD STOCK DATA
    # -----------------------------------------------------

    try:

        stock_data = yf.download(
            ticker_symbol,
            period=period,
            interval="1d",
            auto_adjust=True,
            progress=False
        )

        if stock_data.empty:

            st.error(
                "Stock data could not be retrieved "
                "for this company."
            )

        else:

            # Handle possible multi-level columns
            if isinstance(
                stock_data.columns,
                pd.MultiIndex
            ):

                stock_data.columns = (
                    stock_data.columns
                    .get_level_values(0)
                )

            stock_data = stock_data.reset_index()

            # -------------------------------------------------
            # CALCULATE STOCK METRICS
            # -------------------------------------------------

            first_price = float(
                stock_data["Close"].iloc[0]
            )

            latest_price = float(
                stock_data["Close"].iloc[-1]
            )

            highest_price = float(
                stock_data["High"].max()
            )

            lowest_price = float(
                stock_data["Low"].min()
            )

            price_change = (
                latest_price -
                first_price
            )

            percentage_change = (
                (price_change / first_price)
                * 100
            )

            # -------------------------------------------------
            # KPI CARDS
            # -------------------------------------------------

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Latest Price",
                f"{latest_price:,.2f}"
            )

            col2.metric(
                "Period Change",
                f"{price_change:,.2f}",
                f"{percentage_change:.2f}%"
            )

            col3.metric(
                "Highest Price",
                f"{highest_price:,.2f}"
            )

            col4.metric(
                "Lowest Price",
                f"{lowest_price:,.2f}"
            )

            st.divider()

            # -------------------------------------------------
            # STOCK PRICE FLUCTUATION GRAPH
            # -------------------------------------------------

            st.subheader(
                f"📊 {selected_company} Stock Price Fluctuation"
            )

            fig_stock = px.line(
                stock_data,
                x="Date",
                y="Close",
                title=(
                    f"{selected_company} "
                    f"Historical Closing Price"
                )
            )

            fig_stock.update_layout(
                xaxis_title="Date",
                yaxis_title="Closing Price"
            )

            st.plotly_chart(
                fig_stock,
                use_container_width=True
            )

            # -------------------------------------------------
            # HIGH / LOW RANGE
            # -------------------------------------------------

            st.subheader(
                "📉 Daily High and Low Price Range"
            )

            fig_range = px.line(
                stock_data,
                x="Date",
                y=["High", "Low"],
                title="Daily High vs Low"
            )

            fig_range.update_layout(
                xaxis_title="Date",
                yaxis_title="Price"
            )

            st.plotly_chart(
                fig_range,
                use_container_width=True
            )

            # -------------------------------------------------
            # DAILY CHANGE
            # -------------------------------------------------

            stock_data["Daily Change %"] = (
                stock_data["Close"]
                .pct_change()
                * 100
            )

            st.subheader(
                "📈 Daily Percentage Fluctuation"
            )

            fig_change = px.bar(
                stock_data,
                x="Date",
                y="Daily Change %",
                title="Daily Stock Price Change (%)"
            )

            fig_change.update_layout(
                xaxis_title="Date",
                yaxis_title="Change (%)"
            )

            st.plotly_chart(
                fig_change,
                use_container_width=True
            )

            # -------------------------------------------------
            # STOCK DATA TABLE
            # -------------------------------------------------

            with st.expander(
                "View Historical Stock Data"
            ):

                display_data = stock_data.copy()

                display_data = display_data.sort_values(
                    "Date",
                    ascending=False
                )

                st.dataframe(
                    display_data,
                    use_container_width=True
                )

    except Exception as e:

        st.error(
            "Unable to retrieve stock information. "
            "Please check your internet connection "
            "or try again later."
        )

        st.caption(
            f"Technical information: {e}"
        )


# =========================================================
# FOOTER
# =========================================================

st.sidebar.divider()

st.sidebar.info(
    "E-Commerce Business Analytics System\n\n"
    "Features:\n"
    "• Sales Analytics\n"
    "• Brand Comparison\n"
    "• Customer Reviews\n"
    "• Business Proposals"
)
