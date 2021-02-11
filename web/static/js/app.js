// preventing the browser window from opening dropped files
window.addEventListener("dragover",function(e){
    e.preventDefault();
  },false);

window.addEventListener("drop",function(e){
    e.preventDefault();
  },false);

// drag and drop

// dz_container is for styling
let dz_container = document.querySelector('.dz_container');
// dropzone has for event listener
let dropzone = document.querySelector('.dropzone');
// prediction banner
let prediction = document.querySelector('.banner');

// adding dropzone event listeners
dropzone.addEventListener("dragenter", dragenter, false);
dropzone.addEventListener("dragover", dragover, false);
dropzone.addEventListener("dragleave", dragleave, false);
dropzone.addEventListener("drop", drop, false);

// when file dragged into dropzone
function dragenter(e) {
    e.stopPropagation()
    e.preventDefault()
    //highlight
    dz_container.style.backgroundColor = "#1F4045";
}

// just stop default behavior and stop propogation here
function dragover(e) {
    e.stopPropagation()
    e.preventDefault() 
}

// when file is dragged out of dropzone
function dragleave(e) {
    e.stopPropagation()
    e.preventDefault()
    // remove highlight
    dz_container.style.backgroundColor = "#1F2833";
}

// if file dropped in dropzone
//TODO: File validation
function drop(e) {
    e.stopPropagation();
    e.preventDefault();

    //gets file and appends it to FormData() object
    const dt = e.dataTransfer;
    const files = dt.files;
    const file = files[0];

    // checks file size, makes sure <= 10MB
    const fsize = file.size;
    const mbsize = Math.round((fsize/1048576));
    var isUnder10Mb = (mbsize <= 10);

    // check if file is wav (only type currently supported)
    var isWav = (file.type == 'audio/wav');
    
    // if size and type checks pass
    if (isUnder10Mb && isWav) {

        // wrap file in formData object for fetch body
        const formData = new FormData();
        formData.append('audioFile', files[0]);
    
        // uses fetch to POST file to URL
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            
            // uncomment to see returned data
            //console.log(data)

            // get index of maximum value in prediction array
            // this will be the predicted genre
            let maxIndex = data['predictions'][0].indexOf(Math.max(data['predictions'][0]));

            let genre_labels = new Map([
                [0, "Jaxx"],
                [1, "Reggae"],
                [2, "Rock"],
                [3, "Blues"],
                [4, "HipHop"],
                [5, "Country"],
                [6, "Metal"],
                [7, "Classical"],
                [8, "Disco"],
                [9, "Pop"]
            ]);

            //show the prediction banner
            prediction.innerHTML = `Prediction: ${genre_labels[maxIndex]}`
            prediction.classList.remove('hide');
    
            // CHART for CanvasJS
            var chart = new CanvasJS.Chart("dz", {
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
        // fetch error
        .catch(error => {
            console.error(error)
        })

    // if wav file too big
    } else if (isWav) {
        dz_container.style.backgroundColor = "#1F2833";
        console.log("File too Large")
    // if not a wav file (or both not wav and too big)
    } else {
        dz_container.style.backgroundColor = "#1F2833";
        console.log("Invalid File Type.")
    }
}
