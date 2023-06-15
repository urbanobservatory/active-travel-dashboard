import plotly.graph_objects as go

def ani(df):
    times = df['dt'].unique()
    locations = df['location'].unique()

    # make figure
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }

    # fill in most of layout
    fig_dict["layout"]["xaxis"] = {"range": [30, 85], "title": "Life Expectancy"}
    fig_dict["layout"]["yaxis"] = {"title": "GDP per Capita", "type": "log"}
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 500, "redraw": False},
                                    "fromcurrent": True, "transition": {"duration": 300,
                                                                        "easing": "quadratic-in-out"}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]

    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Year:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }

    # make data
    time = times[0]
    for location in locations:
        dataset_by_time = df[df["dt"] == time]
        dataset_by_time_and_location = dataset_by_time[
            dataset_by_time["location"] == location]

        data_dict = {
            # "x": list(dataset_by_time_and_location["lifeExp"]),
            # "y": list(dataset_by_time_and_location["gdpPercap"]),
            "mode": "markers",
            # "text": list(dataset_by_time_and_location["country"]),
            "marker": {
                "sizemode": "area",
                "sizeref": 200000,
                # "size": list(dataset_by_time_and_location["pop"])
            },
            "name": location
        }
        fig_dict["data"].append(data_dict)

    # make frames
    for time in times:
        frame = {"data": [], "name": str(time)}
        for location in locations:
            dataset_by_time = df[df["dt"] == time]
            dataset_by_time_and_location = dataset_by_time[
                dataset_by_time["location"] == location]

            data_dict = {
                # "x": list(dataset_by_time_and_location["lifeExp"]),
                # "y": list(dataset_by_time_and_location["gdpPercap"]),
                "mode": "markers",
                # "text": list(dataset_by_time_and_location["country"]),
                "marker": {
                    "sizemode": "area",
                    "sizeref": 200000,
                    # "size": list(dataset_by_time_and_location["pop"])
                },
                "name": location
            }
            frame["data"].append(data_dict)

        fig_dict["frames"].append(frame)
        slider_step = {"args": [
            [time],
            {"frame": {"duration": 300, "redraw": False},
            "mode": "immediate",
            "transition": {"duration": 300}}
        ],
            "label": time,
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)


    fig_dict["layout"]["sliders"] = [sliders_dict]

    return go.Figure(fig_dict)