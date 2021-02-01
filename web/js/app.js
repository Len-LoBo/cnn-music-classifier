window.addEventListener("dragover",function(e){
    e.preventDefault();
  },false);

window.addEventListener("drop",function(e){
    e.preventDefault();
  },false);


let dropzone;
let dropzone_bg;

dropzone_bg = document.querySelector('.dropzone');

dropzone = document.querySelector('.dz_overlay');
dropzone.addEventListener("dragenter", dragenter, false);
dropzone.addEventListener("dragover", dragover, false);
dropzone.addEventListener("dragleave", dragleave, false);
dropzone.addEventListener("drop", drop, false);

function dragenter(e) {
    e.stopPropagation();
    e.preventDefault();
    dropzone_bg.style.backgroundColor = "rgb(133, 133, 133, 1)";
}

function dragover(e) {
    e.stopPropagation();
    e.preventDefault();   
}

function dragleave(e) {
    e.stopPropagation();
    e.preventDefault

    dropzone_bg.style.backgroundColor = "rgb(133, 133, 133, .8)";
}

function drop(e) {
    e.stopPropagation();
    e.preventDefault();

    const dt = e.dataTransfer;
    const files = dt.files;

    var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        theme: "dark1", // "light1", "light2", "dark1", "dark2"
        title:{
            text: "Genre Confidence"
        },
        axisY: {
            title: "Confidence"
        },
        data: [{        
            type: "column",  
            showInLegend: true, 
            legendMarkerColor: "grey",
            legendText: "Genres",
            dataPoints: [      
                { y: .9, label: "Jazz" },
                { y: .3,  label: "Blues" },
                { y: .1,  label: "Rock" },
                { y: .05,  label: "Country" },
                { y: .003,  label: "Classical" },
                { y: .0021, label: "Pop" },
                { y: .0021,  label: "Disco" },
                { y: .001,  label: "HipHop" },
                { y: .0001,  label: "Metal" },
                { y: .000001,  label: "Reggae" },
            ]
        }]
    });
    chart.render();
}
