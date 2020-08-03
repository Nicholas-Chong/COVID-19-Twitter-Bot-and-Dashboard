function scrollToSmoothly(pos, time){
    /*Time is only applicable for scrolling upwards*/
    /*Code written by hev1*/
    /*pos is the y-position to scroll to (in pixels)*/
    if(isNaN(pos)){
        throw "Position must be a number";
    }
    if(pos<0){
        throw "Position can not be negative";
    }

    var currentPos = window.scrollY||window.screenTop;
    if(currentPos<pos){
        var t = 10;
        for(let i = currentPos; i <= pos; i+=10){
            t+=10;
            setTimeout(function(){
            window.scrollTo(0, i);
            }, t/3.5);
        }
    } else {
        time = time || 2;
        var i = currentPos;
        var x;
        x = setInterval(function(){
            window.scrollTo(0, i);
            i -= 10;
            if(i<=pos){
                clearInterval(x);
            }
        }, time);
    }
}


function scrollSmoothlyToElementById(id){
    var elem = document.getElementById(id);
    scrollToSmoothly(elem.offsetTop);
 }


function make_clickable() {
    boxes = [
        document.getElementById('box1'),
        document.getElementById('box2'),
        document.getElementById('box3'),
        // document.getElementById('box4'),
    ]

    for (box of boxes) {
        box.style.cursor = 'pointer';
    }

    graphs = [
        document.getElementById('graph1').getBoundingClientRect().top - 125,
        document.getElementById('graph2').getBoundingClientRect().top - 125,
        document.getElementById('graph3').getBoundingClientRect().top - 125,
        document.getElementById('graph4').getBoundingClientRect().top - 125,
    ]

    boxes[0].onclick = function() { scrollToSmoothly(graphs[0], 0); }
    boxes[1].onclick = function() { scrollToSmoothly(graphs[2], 0); }
    boxes[2].onclick = function() { scrollToSmoothly(graphs[1], 0); }
    // boxes[3].onclick = function() { scrollToSmoothly(1857, 50); }

}

setTimeout(make_clickable, 1000);