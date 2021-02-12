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
let prediction = document.getElementById('prediction_banner');

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
async function drop(e) {
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

        var confidences = await fetchPrediction(formData);
        
        var maxIndex = getMaxIndex(confidences)
 
        // for mapping confidence index to genre label
        let genre_labels = new Map([
            [0, "Jazz"],
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

        // store prediction (genre with highest confidence)
        let prediction = genre_labels.get(maxIndex);
        
        // configures and renders the confidence chart on the page
        displayChart(confidences, prediction)


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

//posts file and gets prediction response
async function fetchPrediction(formData) {
    const res = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    const json = await res.json();
    
    // extract first item in data object regardless of key name
    let confidence_key = `${Object.keys(json)[0]}`;

    // store confidences array
    let confidences = json[confidence_key][0];

    return confidences;
}

// gets index of max value in array
function getMaxIndex(array) {
    // get index of maximum value in prediction array
    let maxValue = 0;
    let maxIndex = 0;
    for (let i = 0; i < 10; i++) {
        if (array[i] > maxValue) {
            maxValue = array[i];
            maxIndex = i;
        }
    }
    return maxIndex;
}

//configures and renders ChartJS chart
function displayChart(confidences, prediction) {

    var chart = new CanvasJS.Chart("dz", {
        animationEnabled: true,
        theme: "dark1", // "light1", "light2", "dark1", "dark2"
        backgroundColor: "#1F2833",
        title:{
            text: `Prediction: ${prediction}`,
            fontFamily: "Rubik",
            fontColor: "#66FCF1"
        },
        axisY: {
            title: "Confidence",
            fontFamily: "Rubik",
            fontColor: "#C5C6C7",
            minimum: 0
        },
        data: [{        
            type: "column",
            indexLabelFontFamily: "Rubik",
            indexLabelFontColor: "#C5C6C7",  
            dataPoints: [      
                { y: confidences[0], label: "Jazz" },
                { y: confidences[1],  label: "Reggae" },
                { y: confidences[2],  label: "Rock" },
                { y: confidences[3],  label: "Blues" },
                { y: confidences[4],  label: "HipHop" },
                { y: confidences[5], label: "Country" },
                { y: confidences[6],  label: "Metal" },
                { y: confidences[7],  label: "Classical" },
                { y: confidences[8],  label: "Disco" },
                { y: confidences[9],  label: "Pop" },
            ]
        }]
    });
    chart.render();
}