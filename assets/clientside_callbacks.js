window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        update_daterange: function(start, end) {
            // let start = new Date(list[0]*1000).toLocaleDateString();
            // let end = new Date(list[1]*1000).toLocaleDateString();

            console.log(start, end)
            let message = 'You are viewing dates ' + start + ' to ' + end;

            let range = {
                'start': start,
                'end': end,
            }

            return [message, range]
        }
    }
});