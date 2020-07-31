window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        update_daterange: function(start, end) {
            let message = 'You have selected dates ' + start + ' to ' + end;

            try {
                let element = document.getElementById('output-container-range-slider');
                return element.innerHTML = message;
            } 
            catch {
                let element = document.createElement('div');
                element.setAttribute('id', 'output-container-range-slider')
                return element.innerHTML = message ;
            }
        }
    }
});