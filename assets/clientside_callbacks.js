window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        update_daterange: function(start, end) {
            /*
            Updates the message and stores the range data all on the client
            side.
            */

            let triggered = dash_clientside.callback_context.triggered[0]
            if (triggered != null) {
                if ('prop_id' in triggered) {
                    if (triggered['prop_id'] === 'reset_graphs_button.n_clicks') {
                        let today = new Date().toLocaleDateString('en-CA')
                        let message = 'You are viewing dates 2020-01-26 to ' + today;
                        let range = {
                            'start': '2020-01-26',
                            'end': today,
                        }

                        return [message, range]
                    }
                }
            }

            let message = 'You are viewing dates ' + start + ' to ' + end;
            let range = {
                'start': start,
                'end': end,
            }

            return [message, range]
        },

        update_graphs: function(data, range) {

            // Retrieve neccessary data
            let start = range['start']
            let end = range['end']
            let today = new Date().toLocaleDateString('en-CA')

            // Duplicate the array of figure dictionaries from the data store
            let figs = JSON.parse(JSON.stringify(data))

            // If the requested dates are 2020-01-26 - today (most recent)
            // return the unchanged figures
            if (start == '2020-01-26' && end == today) {
                return figs
            }

            // Functions to find the start and end index 
            const findstartindex = (element) => element == start;
            const findendindex = (element) => element == end;

            // Find the start and end index
            let startIndex = figs[0].data[0].x.findIndex(findstartindex);
            let endIndex = figs[0].data[0].x.findIndex(findendindex) + 1;

            // Loop through the list of figures (dictionaries)
            for (newfig of figs) {
                // Loop through the 'data' portion of the figures dict
                for (data of newfig.data) {
                    // Slice the x and y data according to the calculated 
                    // start and end index
                    data.x = data.x.slice(startIndex, endIndex);
                    data.y = data.y.slice(startIndex, endIndex);
                }
            }

            // Return the array with updated figure dicts
            return figs
        }, 

        reset_daterange: function() {
            let today = new Date().toLocaleDateString('en-CA')
            return ['2020-01-26', today]
        }
    }
});