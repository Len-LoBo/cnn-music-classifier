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
    e.stopPropagation()
    e.preventDefault()
    dropzone_bg.style.backgroundColor = "rgb(133, 133, 133, 1)";
}

function dragover(e) {
    e.stopPropagation()
    e.preventDefault() 
}

function dragleave(e) {
    e.stopPropagation()
    e.preventDefault

    dropzone_bg.style.backgroundColor = "rgb(133, 133, 133, .8)";
}

function drop(e) {
    e.stopPropagation();
    e.preventDefault();

    const dt = e.dataTransfer;
    const files = dt.files;
    const formData = new FormData() 
    formData.append('audioFile', files[0])

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        console.log(data['predictions'][0][0])

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
                    { y: data['predictions'][0][0], label: "Jazz" },
                    { y: data['predictions'][0][1],  label: "Reggae" },
                    { y: data['predictions'][0][2],  label: "Rock" },
                    { y: data['predictions'][0][3],  label: "Blues" },
                    { y: data['predictions'][0][4],  label: "HipHop" },
                    { y: data['predictions'][0][5], label: "Country" },
                    { y: data['predictions'][0][6],  label: "Metal" },
                    { y: data['predictions'][0][7],  label: "Classical" },
                    { y: data['predictions'][0][8],  label: "Disco" },
                    { y: data['predictions'][0][9],  label: "Pop" },
                ]
            }]
        });
        chart.render();
        
    })
    .catch(error => {
        console.error(error)
    })
    
}
