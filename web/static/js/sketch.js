//dark_teal = (69, 162, 158, 190)
//accent_teal = (102, 252, 241, 190)

let angleInc = 3;

let angleMotionSpeed = 0.2; 


let ellipseW = 2;
let ellipseH = 40;

let angle = 0;
let angleStart = 0;
let canDraw = true;

let mode = true;

let imgLeft, imgRight;

let leftPart, rightPart;

function setup() {
  let renderer = createCanvas(320, 320);
  renderer.parent("#loading_graphic")

  leftPart = createGraphics(width / 2, height);
  rightPart = createGraphics(width / 2, height);

  leftPart.ellipseMode(CENTER);
  rightPart.ellipseMode(CENTER);

  leftPart.noStroke();
  rightPart.noStroke();

}

function draw() {

  canDraw = true;
  angle = angleStart;
  mode = true;
  
  while (canDraw == true) {
    let x = cos(radians(angle)) * 60 + width / 2;
    let y = sin(radians(angle)) * 60 + height / 2;
    
    let rotation = -radians(angle)*.5;

    if (mode) {
      leftPart.fill(102, 252, 241, 70);
      rightPart.fill(102, 252, 241, 70);
    } else {
      leftPart.fill(31, 40, 51, 50);
      rightPart.fill(31, 40, 51, 50);
    }

    if (angle <= 360) {
      leftPart.push();
      leftPart.translate(x, y);
      leftPart.rotate(rotation);
      leftPart.ellipse(0, 0, ellipseW, ellipseH);
      leftPart.pop();
    }

    if (angle <= 540) {
      rightPart.push();
      rightPart.translate(x - width / 2, y);
      rightPart.rotate(rotation);
      rightPart.ellipse(0, 0, ellipseW, ellipseH);
      rightPart.pop();
    }

    angle += angleInc;
    mode = !mode;
    
    if (angle > 540) canDraw = false;
  }

  image(leftPart, 0, 0);
  image(rightPart, width / 2, 0);
  
  angleStart -= angleMotionSpeed;
}
