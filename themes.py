def one(fig):
    fig.update_xaxes(gridcolor='#ececec')
    fig.update_yaxes(gridcolor='#ececec')
    # Transparent background
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 
                       'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    return fig