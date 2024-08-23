# Sample multiselect widget
dbutils.widgets.multiselect("selected_columns", "", ["col1", "col2", "col3_long_value", "col4_really_long_value"], "Select Columns")

# Injecting custom CSS and JavaScript to widen the widget
html_content = """
<style>
  .input-widget-multiselect { 
    width: 500px !important;  /* Adjust the width as needed */
  }
</style>
"""

# Display the custom CSS to override the default widget width
displayHTML(html_content)