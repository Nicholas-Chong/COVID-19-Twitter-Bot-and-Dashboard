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

            let start = range['start']
            let end = range['end']
            let today = new Date().toLocaleDateString('en-CA')

            let figs = JSON.parse(JSON.stringify(data))

            if (start == '2020-01-26' && end == today) {
                return figs
            }

            const findstartindex = (element) => element == start;
            const findendindex = (element) => element == end;

            let startIndex = figs[0].data[0].x.findIndex(findstartindex);
            let endIndex = figs[0].data[0].x.findIndex(findendindex) + 1;

            for (newfig of figs) {
                for (data of newfig.data) {
                    data.x = data.x.slice(startIndex, endIndex);
                    data.y = data.y.slice(startIndex, endIndex);
                }
            }

            return figs
        }, 

        reset_daterange: function() {
            let today = new Date().toLocaleDateString('en-CA')
            
            return ['2020-01-26', today]
        }
    }
});