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
        }
    }
});