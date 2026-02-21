"""
DataTransform Pro – Streamlit Deployment
Banking & Finance Dataset Operations
"""
import streamlit as st
import pandas as pd
import io

st.set_page_config(
    page_title="DataTransform Pro",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="auto",
)

# Session state for original and transformed datasets
if "df_original" not in st.session_state:
    st.session_state.df_original = None
if "df_transformed" not in st.session_state:
    st.session_state.df_transformed = None
if "math_results" not in st.session_state:
    st.session_state.math_results = []


def load_file(file):
    """Load CSV or Excel file into DataFrame."""
    name = (file.name or "").lower()
    if name.endswith(".csv"):
        return pd.read_csv(file)
    if name.endswith((".xls", ".xlsx")):
        return pd.read_excel(file)
    raise ValueError("Unsupported format. Use CSV, XLS, or XLSX.")


# ----- Header -----
st.markdown(
    """
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="margin: 0;">DataTransform Pro ✨</h1>
        <p style="color: #64748b; margin: 0.5rem 0 0 0;">Banking & Finance Dataset Operations</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

# ----- Step 1: Upload -----
st.subheader("1️⃣ Upload Dataset")
uploaded = st.file_uploader(
    "Drag & drop or browse",
    type=["csv", "xls", "xlsx"],
    help="CSV, XLS, or XLSX",
)

if uploaded:
    try:
        df = load_file(uploaded)
        st.session_state.df_original = df.copy()
        st.session_state.df_transformed = df.copy()
        st.session_state.math_results = []
        st.success(f"Loaded **{len(df)}** rows × **{len(df.columns)}** columns.")
    except Exception as e:
        st.error(f"Upload failed: {e}")
        st.session_state.df_original = None
        st.session_state.df_transformed = None

df = st.session_state.df_transformed
if df is None:
    st.info("Upload a file to continue.")
    st.stop()

# View toggle: Original vs Transformed
view = st.radio(
    "View",
    ["Transformed", "Original"],
    horizontal=True,
    key="view_toggle",
)
display_df = st.session_state.df_original if view == "Original" else st.session_state.df_transformed
st.caption(f"Showing: **{view}** · {display_df.shape[0]} rows × {display_df.shape[1]} columns")
st.dataframe(display_df.head(100), use_container_width=True)

st.divider()

# ----- Step 2: Cleaning -----
st.subheader("2️⃣ Cleaning Operations")
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    if st.button("Remove Nulls", use_container_width=True):
        df_clean = st.session_state.df_transformed.dropna()
        st.session_state.df_transformed = df_clean
        st.success(f"Removed nulls. Rows: {len(df_clean)}")
        st.rerun()

with c2:
    if st.button("Remove Duplicates", use_container_width=True):
        df_clean = st.session_state.df_transformed.drop_duplicates()
        st.session_state.df_transformed = df_clean
        st.success(f"Duplicates removed. Rows: {len(df_clean)}")
        st.rerun()

with c3:
    if st.button("Trim Whitespaces", use_container_width=True):
        t = st.session_state.df_transformed
        for col in t.columns:
            if t[col].dtype == "object":
                t[col] = t[col].astype(str).str.strip()
        st.session_state.df_transformed = t
        st.success("Whitespaces trimmed.")
        st.rerun()

with c4:
    rename_click = st.button("Rename Columns", use_container_width=True)

with c5:
    dtype_click = st.button("Change Data Types", use_container_width=True)

if rename_click:
    with st.expander("Rename columns", expanded=True):
        rcols = list(st.session_state.df_transformed.columns)
        renames = {}
        for col in rcols:
            new_name = st.text_input(f"Rename: {col}", value=col, key=f"rename_{col}")
            if new_name and new_name != col:
                renames[col] = new_name
        if renames and st.button("Apply renames", key="apply_rename"):
            st.session_state.df_transformed = st.session_state.df_transformed.rename(columns=renames)
            st.success("Columns renamed.")
            st.rerun()

if dtype_click:
    with st.expander("Change data types", expanded=True):
        dcols = list(st.session_state.df_transformed.columns)
        dtypes = {}
        for col in dcols:
            dtypes[col] = st.selectbox(
                f"Type: {col}",
                ["string", "int", "float", "date"],
                key=f"dtype_{col}",
            )
        if st.button("Apply types", key="apply_dtype"):
            t = st.session_state.df_transformed.copy()
            for col, dtype in dtypes.items():
                try:
                    if dtype == "date":
                        t[col] = pd.to_datetime(t[col], errors="coerce")
                    elif dtype == "int":
                        t[col] = pd.to_numeric(t[col], errors="coerce").astype("Int64")
                    elif dtype == "float":
                        t[col] = pd.to_numeric(t[col], errors="coerce")
                    elif dtype == "string":
                        t[col] = t[col].astype(str)
                except Exception:
                    pass
            st.session_state.df_transformed = t
            st.success("Data types updated.")
            st.rerun()

st.divider()

# ----- Step 3: Mathematical Operations -----
st.subheader("3️⃣ Mathematical Operations")
df = st.session_state.df_transformed
cols = list(df.columns)

tab1, tab2, tab3 = st.tabs(["Single column", "Two columns (Add/Sub/Mul/Div)", "Results"])

with tab1:
    sc1, sc2, sc3 = st.columns([2, 2, 1])
    with sc1:
        col_single = st.selectbox("Column", cols, key="math_col")
    with sc2:
        op_single = st.selectbox(
            "Operation",
            ["sum", "average", "min", "max", "count"],
            key="math_op",
        )
    with sc3:
        if st.button("Calculate"):
            if col_single not in df.columns:
                st.error("Column not found.")
            else:
                s = pd.to_numeric(df[col_single], errors="coerce")
                if op_single == "sum":
                    val = s.sum()
                elif op_single == "average":
                    val = s.mean()
                elif op_single == "min":
                    val = s.min()
                elif op_single == "max":
                    val = s.max()
                else:
                    val = df[col_single].notna().sum()
                st.session_state.math_results.append(
                    {"op": op_single, "column": col_single, "value": val}
                )
                st.success(f"{op_single.title()}({col_single}) = {val}")
                st.rerun()

with tab2:
    tc1, tc2, tc3, tc4 = st.columns(4)
    with tc1:
        col1 = st.selectbox("Column 1", cols, key="col1")
    with tc2:
        col2 = st.selectbox("Column 2", cols, key="col2")
    with tc3:
        op2 = st.selectbox("Operation", ["add", "subtract", "multiply", "divide"], key="op2")
    with tc4:
        result_name = st.text_input("Result column name", key="result_col", placeholder="Optional")
    if st.button("Apply operation"):
        if col1 not in df.columns or col2 not in df.columns:
            st.error("Select both columns.")
        else:
            a = pd.to_numeric(df[col1], errors="coerce")
            b = pd.to_numeric(df[col2], errors="coerce")
            if op2 == "add":
                new_col = a + b
                default_name = f"{col1}_plus_{col2}"
            elif op2 == "subtract":
                new_col = a - b
                default_name = f"{col1}_minus_{col2}"
            elif op2 == "multiply":
                new_col = a * b
                default_name = f"{col1}_times_{col2}"
            else:
                new_col = a / b.replace(0, pd.NA)
                default_name = f"{col1}_div_{col2}"
            name = (result_name or default_name).strip() or default_name
            st.session_state.df_transformed = st.session_state.df_transformed.copy()
            st.session_state.df_transformed[name] = new_col
            st.success(f"Added column **{name}**.")
            st.rerun()

with tab3:
    for r in st.session_state.math_results:
        st.metric(label=f"{r['op'].title()} ({r['column']})", value=r["value"])
    if not st.session_state.math_results:
        st.caption("Single-column results appear here after you click Calculate.")

st.divider()

# ----- Step 4: Advanced Financial -----
st.subheader("4️⃣ Advanced Financial Operations")
df = st.session_state.df_transformed
cols = list(df.columns)

ar1, ar2, ar3, ar4 = st.columns(4)
with ar1:
    rev_col = st.selectbox("Revenue column", [""] + cols, key="rev")
with ar2:
    cost_col = st.selectbox("Cost column", [""] + cols, key="cost")
with ar3:
    tax_col = st.selectbox("Tax column", [""] + cols, key="tax")
with ar4:
    date_col = st.selectbox("Date column", [""] + cols, key="date")

f1, f2, f3, f4 = st.columns(4)
with f1:
    if st.button("Gross Profit"):
        if rev_col and cost_col and rev_col in df.columns and cost_col in df.columns:
            r = pd.to_numeric(df[rev_col], errors="coerce")
            c = pd.to_numeric(df[cost_col], errors="coerce")
            gp = (r - c).sum()
            st.metric("Total Gross Profit", f"{gp:,.2f}")
            st.metric("Total Revenue", f"{r.sum():,.2f}")
            st.metric("Total Cost", f"{c.sum():,.2f}")
        else:
            st.warning("Select Revenue and Cost columns.")
with f2:
    if st.button("Net Profit"):
        if rev_col and cost_col and tax_col and all(c in df.columns for c in [rev_col, cost_col, tax_col]):
            r = pd.to_numeric(df[rev_col], errors="coerce")
            c = pd.to_numeric(df[cost_col], errors="coerce")
            t = pd.to_numeric(df[tax_col], errors="coerce")
            gp = (r - c).sum()
            np_ = (r - c - t).sum()
            st.metric("Total Net Profit", f"{np_:,.2f}")
            st.metric("Total Gross Profit", f"{gp:,.2f}")
        else:
            st.warning("Select Revenue, Cost, and Tax columns.")
with f3:
    if st.button("Monthly P&L"):
        if rev_col and cost_col and date_col and all(c in df.columns for c in [rev_col, cost_col, date_col]):
            d = df.copy()
            d[date_col] = pd.to_datetime(d[date_col], errors="coerce")
            d = d.dropna(subset=[date_col])
            d[rev_col] = pd.to_numeric(d[rev_col], errors="coerce")
            d[cost_col] = pd.to_numeric(d[cost_col], errors="coerce")
            d["_month"] = d[date_col].dt.to_period("M").astype(str)
            monthly = d.groupby("_month").agg({rev_col: "sum", cost_col: "sum"}).reset_index()
            monthly["Profit"] = monthly[rev_col] - monthly[cost_col]
            monthly = monthly.rename(columns={rev_col: "Revenue", cost_col: "Cost"})
            st.dataframe(monthly, use_container_width=True)
        else:
            st.warning("Select Revenue, Cost, and Date columns.")
with f4:
    if st.button("Quarterly P&L"):
        if rev_col and cost_col and date_col and all(c in df.columns for c in [rev_col, cost_col, date_col]):
            d = df.copy()
            d[date_col] = pd.to_datetime(d[date_col], errors="coerce")
            d = d.dropna(subset=[date_col])
            d[rev_col] = pd.to_numeric(d[rev_col], errors="coerce")
            d[cost_col] = pd.to_numeric(d[cost_col], errors="coerce")
            d["_q"] = d[date_col].dt.year.astype(str) + "-Q" + d[date_col].dt.quarter.astype(str)
            q = d.groupby("_q").agg({rev_col: "sum", cost_col: "sum"}).reset_index()
            q["Profit"] = q[rev_col] - q[cost_col]
            q = q.rename(columns={"_q": "Quarter", rev_col: "Revenue", cost_col: "Cost"})
            st.dataframe(q, use_container_width=True)
        else:
            st.warning("Select Revenue, Cost, and Date columns.")

st.divider()

# ----- Results & Download -----
st.subheader("Results")
df_out = st.session_state.df_transformed
buf = io.BytesIO()
with pd.ExcelWriter(buf, engine="openpyxl") as writer:
    df_out.to_excel(writer, index=False, sheet_name="TransformedData")
buf.seek(0)

st.download_button(
    label="Download Transformed Dataset (Excel)",
    data=buf,
    file_name="transformed_dataset.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    type="primary",
)
st.caption("Download the current transformed dataset as an Excel file.")
