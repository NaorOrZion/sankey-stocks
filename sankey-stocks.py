import plotly.graph_objects as go

# Using https://plotly.com/python/sankey-diagram/ for documentation

"""
     המספרים במקור וביעד הם מספרים שמציינים את המיקום של איברים במשתנה
       label
"""
fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 50,
      thickness = 40,
      label = ["A1", "A2", "B1", "B2", "C1", "C2"],
      color = "blue"
    ),
    link = dict(
      source = [0, 1, 0, 2, 3, 3],
      target = [1, 3, 3, 4, 4, 5],
      value = [8, 4, 2, 8, 4, 2]
  ))])

fig.update_layout(title_text="Basic Sankey Diagram", font_size=50)
fig.show()