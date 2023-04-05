# -*- encoding: utf-8 -*-
'''
@File    :   streamlit_ABM.py   
@Contact :   jshmxwc@gmail.com/gy22wx@leeds.ac.uk
@License :   (C)Copyright
 
@Modify Time        @Author     @Version    @Desciption
------------      ----------    --------    -----------
2023/4/4 20:54   Wanchen Xu      1.0         None
'''

import streamlit as st

def intro():
    import streamlit as st

    st.write("# Welcome to Agent Based Model made by Wanchen Xu!")
    st.sidebar.success("Select a feature above.")

    st.markdown(
        """
        This test attempts to build a visual demonstration of the ABM model 
        using python's streamlit library
        
        ### Want to learn more about Agent Based Model?
        - Learn about ABM through Wikipedia(https://en.wikipedia.org/wiki/Agent-based_model)
        - Search ABM in ChatGPT(http://chat.openai.com/chat)

        ### Want to learn more about Streamlit?

        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)
        """
    )

def mapping_demo():
    import streamlit as st
    import pandas as pd
    import pydeck as pdk

    from urllib.error import URLError

    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
    st.write(
        """
        This demo shows how to use
[`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
to display geospatial data.
"""
    )

    @st.cache_data
    def from_data_file(filename):
        url = (
            "http://raw.githubusercontent.com/streamlit/"
            "example-data/master/hello/v1/%s" % filename
        )
        return pd.read_json(url)

    try:
        ALL_LAYERS = {
            "Bike Rentals": pdk.Layer(
                "HexagonLayer",
                data=from_data_file("bike_rental_stats.json"),
                get_position=["lon", "lat"],
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                extruded=True,
            ),
            "Bart Stop Exits": pdk.Layer(
                "ScatterplotLayer",
                data=from_data_file("bart_stop_stats.json"),
                get_position=["lon", "lat"],
                get_color=[200, 30, 0, 160],
                get_radius="[exits]",
                radius_scale=0.05,
            ),
            "Bart Stop Names": pdk.Layer(
                "TextLayer",
                data=from_data_file("bart_stop_stats.json"),
                get_position=["lon", "lat"],
                get_text="name",
                get_color=[0, 0, 0, 200],
                get_size=15,
                get_alignment_baseline="'bottom'",
            ),
            "Outbound Flow": pdk.Layer(
                "ArcLayer",
                data=from_data_file("bart_path_stats.json"),
                get_source_position=["lon", "lat"],
                get_target_position=["lon2", "lat2"],
                get_source_color=[200, 30, 0, 160],
                get_target_color=[200, 30, 0, 160],
                auto_highlight=True,
                width_scale=0.0001,
                get_width="outbound",
                width_min_pixels=3,
                width_max_pixels=30,
            ),
        }
        st.sidebar.markdown("### Map Layers")
        selected_layers = [
            layer
            for layer_name, layer in ALL_LAYERS.items()
            if st.sidebar.checkbox(layer_name, True)
        ]
        if selected_layers:
            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/light-v9",
                    initial_view_state={
                        "latitude": 37.76,
                        "longitude": -122.4,
                        "zoom": 11,
                        "pitch": 50,
                    },
                    layers=selected_layers,
                )
            )
        else:
            st.error("Please choose at least one layer above.")
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**

            Connection error: %s
        """
            % e.reason
        )

def plotting_demo():
    import streamlit as st
    import time
    import numpy as np

    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    st.write(
        """
        This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!
"""
    )

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.05)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")


def data_frame_demo():
    import streamlit as st
    import pandas as pd
    import altair as alt

    from urllib.error import URLError

    st.markdown(f"# {list(page_names_to_funcs.keys())[3]}")
    st.write(
        """
        This demo shows how to use `st.write` to visualize Pandas DataFrames.

(Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)
"""
    )

    @st.cache_data
    def get_UN_data():
        AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
        df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
        return df.set_index("Region")

    try:
        df = get_UN_data()
        countries = st.multiselect(
            "Choose countries", list(df.index), ["China", "United States of America"]
        )
        if not countries:
            st.error("Please select at least one country.")
        else:
            data = df.loc[countries]
            data /= 1000000.0
            st.write("### Gross Agricultural Production ($B)", data.sort_index())

            data = data.T.reset_index()
            data = pd.melt(data, id_vars=["index"]).rename(
                columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
            )
            chart = (
                alt.Chart(data)
                .mark_area(opacity=0.3)
                .encode(
                    x="year:T",
                    y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                    color="Region:N",
                )
            )
            st.altair_chart(chart, use_container_width=True)
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**

            Connection error: %s
        """
            % e.reason
        )

def test():
    import streamlit as st
    import pandas as pd
    import numpy as np

    st.title('Uber pickups in NYC')

    DATE_COLUMN = 'date/time'
    DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
                'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

    @st.cache_data
    def load_data(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
        return data

    data_load_state = st.text('Loading data...')
    data = load_data(10000)
    data_load_state.text("Done! (using st.cache_data)")

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    st.subheader('Number of pickups by hour')
    hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
    st.bar_chart(hist_values)

    # Some number in the range 0-23
    hour_to_filter = st.slider('hour', 0, 23, 17)
    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

    st.subheader('Map of all pickups at %s:00' % hour_to_filter)
    st.map(filtered_data)

def test1():
    import streamlit as st
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from io import StringIO
    import agentframework as af
    import operator
    import geometry
    import requests
    import bs4

    def sum_environment(environment):
        return np.sum(environment)

    def sum_agent_stores(agents):
        sum_store = 0
        for agent in agents:
            sum_store += agent.store
        return sum_store

    st.title('Agent Based Model in class')

    environment = []
    agents = []
    n_agents = 1
    n_iterations = 1
    x_max_color = '#ff3633'
    x_min_color = '#3355ff'
    y_max_color = '#33ff3f'
    y_min_color = '#f6ff33'

    uploaded_file = st.file_uploader("Choose a environment")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        # st.write(bytes_data)

        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # st.write(stringio)

        # To read file as string:
        string_data = stringio.read()
        # st.write(string_data)

        # Can be used wherever a "file-like" object is accepted:
        dataframe = pd.read_csv(uploaded_file)
        dataframe.columns = ('col %d' % i for i in range(len(dataframe.columns)))
        environment = dataframe.values
        n_rows, n_cols = environment.shape

    if st.checkbox('Show raw data'):
        if environment == []:
            st.error("No data uploaded.")
        else:
            st.subheader('Environment data')
            st.write(environment)
            st.write("Rows: %d, Columns: %d" % (n_rows, n_cols))

    if st.checkbox('Environment Editor'):
        if environment == []:
            st.error("No data uploaded.")
        else:
            edited_df = st.experimental_data_editor(environment)

    if st.checkbox('Show image of environment'):
        if environment == []:
            st.error("No data uploaded.")
        else:
            plt.imshow(environment)
            plt.colorbar()
            st.pyplot()

    if st.checkbox('Input number of agents and iterations'):
        if environment == []:
            st.error("No data uploaded.")
        else:
            if st.checkbox("Use Slider"):
                n_agents = st.sidebar.slider('Number of agents', 1, 1000, 1)
                n_iterations = st.sidebar.slider('Number of iterations', 1, 1000, 1)
                st.write("There are %d agents" % n_agents)
                st.write("Current iteration number %d" % n_iterations)
            else:
                n_agents = int(st.sidebar.number_input('Insert agent number'))
                n_iterations = int(st.sidebar.number_input('Insert iteration number'))
                st.write('The agent number is ', n_agents)
                st.write('The iteration number is ', n_iterations)

    if st.checkbox('Color Choice'):
        if environment == []:
            st.error("No data uploaded.")
        else:
            x_max_color = st.sidebar.color_picker('Pick x_max color','#ff3633')
            x_min_color = st.sidebar.color_picker('Pick x_min color','#3355ff')
            y_max_color = st.sidebar.color_picker('Pick y_max color','#33ff3f')
            y_min_color = st.sidebar.color_picker('Pick y_min color','#f6ff33')
            st.sidebar.write("X_max_color is", x_max_color)
            st.sidebar.write("X_min_color is", x_min_color)
            st.sidebar.write("Y_max_color is", y_max_color)
            st.sidebar.write("Y_min_color is", y_min_color)


    if st.checkbox('Run ABM'):
        if environment == []:
            st.error("No data uploaded.")
        else:
            x_min = 0
            x_max = n_cols - 1
            y_min = 0
            y_max = n_rows - 1
            neighbourhood = 100
            r = requests.get('http://agdturner.github.io/resources/abm9/data.html', verify=False)
            content = r.text
            soup = bs4.BeautifulSoup(content, 'html.parser')
            td_ys = soup.find_all(attrs={"class": "y"})
            td_xs = soup.find_all(attrs={"class": "x"})
            agents = []
            progress_bar = st.sidebar.progress(0)
            frame_text = st.sidebar.empty()
            image = st.empty()

            for i in range(n_agents):
                # Create an agent
                y = int(td_ys[i].text) + 99
                x = int(td_xs[i].text) + 99
                agents.append(af.Agent(agents, i, environment, n_rows, n_cols, x, y))
                print(agents[i].agents[i])

            for ite in range(n_iterations):
                progress_bar.progress(ite)
                frame_text.text("Iteration %d" % (ite+1))
                st.write("Iteration", ite+1)
                # Move agents
                st.write("Move")
                for i in range(n_agents):
                    agents[i].move(x_min, x_max, y_min, y_max)
                    agents[i].eat()
                    # print(agents[i])
                # Share store
                # Distribute shares
                for i in range(n_agents):
                    agents[i].share(neighbourhood)
                # Add store_shares to store and set store_shares back to zero
                for i in range(n_agents):
                    print(agents[i])
                    agents[i].store = agents[i].store_shares
                    agents[i].store_shares = 0
                st.write(agents)
                # Print the maximum distance between all the agents
                st.write("Maximum distance between all the agents", geometry.get_max_distance(agents))
                # Print the total amount of resource
                sum_as = sum_agent_stores(agents)
                st.write("sum_agent_stores", sum_as)
                sum_e = sum_environment(environment)
                st.write("sum_environment", sum_e)
                st.write("total resource", (sum_as + sum_e))
                plt.ylim(y_max / 3, y_max * 2 / 3)
                plt.xlim(x_max / 3, x_max * 2 / 3)
                plt.imshow(environment)
                for i in range(n_agents):
                    plt.scatter(agents[i].x, agents[i].y, color='black')
                # Plot the coordinate with the largest x red
                lx = max(agents, key=operator.attrgetter('x'))
                plt.scatter(lx.x, lx.y, color=x_max_color)
                # Plot the coordinate with the smallest x blue
                sx = min(agents, key=operator.attrgetter('x'))
                plt.scatter(sx.x, sx.y, color=x_min_color)
                # Plot the coordinate with the largest y yellow
                ly = max(agents, key=operator.attrgetter('y'))
                plt.scatter(ly.x, ly.y, color=y_max_color)
                # Plot the coordinate with the smallest y green
                sy = min(agents, key=operator.attrgetter('y'))
                plt.scatter(sy.x, sy.y, color=y_min_color)
                st.pyplot()

            progress_bar.empty()
            frame_text.empty()

            st.button("Re-run")

page_names_to_funcs = {
    "Introduction": intro,
    "Plotting Demo": plotting_demo,
    "Mapping Demo": mapping_demo,
    "DataFrame Demo": data_frame_demo,
    "Test": test,
    "Agent Based Model": test1
}

demo_name = st.sidebar.selectbox("Choose a feature", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()



