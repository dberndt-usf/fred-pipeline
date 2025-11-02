# Streamlit Hints and Tips

## Widgets
- `st.slider(label, min, max, default)` → interactive numeric control.
- `st.checkbox(label, value=False)` → toggle visibility for detailed data.
- `st.selectbox(label, options)` → choose between lag lengths or datasets.

## Layout
- `st.columns(n)` → align metrics side-by-side.
- `st.metric(label, value)` → display a KPI card.

## Charts
- `st.line_chart(df)` → quick time-series visualization.
- `st.bar_chart(df)` → categorical comparisons.
- `st.pyplot()` → custom Matplotlib visuals.

💡 *Hint:* Always use `df.set_index("quarter_start")` before plotting time-series.
