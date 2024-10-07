//All longitude has been scaled and shifted with certain number to better fit the screen: (LON - 24) * 90 + 50 
//All longitude has been scaled and shifted with certain number to better fit the screen: (LAT - 35) * 180 + 300 
Table MinardTable; 
String[] Temp_Dates = {"N/A", "10/24", "11/ 7", "11/14", "N/A", "11/28", "12/ 1", "12/ 7", "12/ 7"};
final float axisX = 1280;
final float axisTop = 620;
final float axisBottom = 770;


void setup(){
  size(1600, 900);
  MinardTable = loadTable("minard-data.csv","header");
}

void draw(){
  background(224, 224, 224);
  PFont title = createFont("Georgia", 25, true);  // Changed font
  textFont(title);
  textAlign(CENTER, CENTER);
  fill(0, 0, 0);
  text("FIGURATIVE MAP of the successive losses in men of the French Army in the RUSSIAN CAMPAIGN OF 1812-1813", 800, 40);
  text("GRAPHIC TABLE OF THE TEMPERATURE IN DEGREE OF CELSIUS THERMOMETER", 800, 550);
  
  // Drawing the legend
  fill(243, 156, 18);
  rect(1350, 200, 50, 10, 3);
  fill(0, 0, 0);
  rect(1350, 250, 50, 10, 3);
  PFont legend = createFont("Georgia", 14, true);
  textFont(legend);
  fill(33, 47, 60);
  text("Attack", 1440, 205);
  text("Return", 1440, 255);
  
  drawTroop();     // Draw the army paths
  drawCity();        // Draw cities
  tempCurve();    // Temperature curve
}

// Draw City with their name as a circle (Total Number 20)
void drawCity(){
  for (int i = 0; i < 20; i++){
    TableRow row = MinardTable.getRow(i);
    float cityLON = (row.getFloat("LONC") - 24.0) * 90 + 50;
    float cityLAT = (90 - row.getFloat("LATC") - 35) * 180 + 300;
    fill(128,128,128);
    circle(cityLON, cityLAT, 10);
    
    PFont cityLabel = createFont("Georgia", 12, true); 
    textFont(cityLabel);
    fill(96, 96, 96);
    text(row.getString("CITY"), cityLON, cityLAT+10);
  }
}

void drawTroop() {
  // Draw all retreating routes (DIR == "R") first
  for (int i = 0; i < MinardTable.getRowCount() - 1; i++) {
    TableRow row = MinardTable.getRow(i);
    if (row.getString("DIR").equals("R")) {
      drawTroopRectangle(row, i);
    }
  }

  // Draw all attacking routes (DIR == "A") on top
  for (int i = 0; i < MinardTable.getRowCount() - 1; i++) {
    TableRow row = MinardTable.getRow(i);
    if (row.getString("DIR").equals("A")) {
      drawTroopRectangle(row, i);
    }
  }
  
  // Draw number of people in the troop
  for (int i = 0; i < MinardTable.getRowCount(); i++) {
    TableRow row = MinardTable.getRow(i);
    float startLON = (row.getFloat("LONP") - 24.0) * 90 + 50;
    float startLAT = (90 - row.getFloat("LATP") - 35) * 180 + 300;
    int troopNum = row.getInt("SURV");
    fill(255, 0, 0);
    PFont numLabelFont = createFont("Georgia", 8, true);
    textFont(numLabelFont);
    text(troopNum, startLON + 2, startLAT + 11);
  }
}

// Helper function to draw each troop's rectangle
void drawTroopRectangle(TableRow row, int i) {
  int troopNum = row.getInt("SURV");
  float rectHeight = map(troopNum, 1000, 340000, 2, 50);  // Scaled rectangle height
  float rectWidth = 10;  // Fixed width for all rectangles
  noStroke();

  // Set fill color based on direction of travel
  if (row.getString("DIR").equals("A")) {
    fill(243, 156, 18);  // Orange for attacking
  } else if (row.getString("DIR").equals("R")) {
    fill(0, 0, 0);  // Black for retreating
  }

  // Get the coordinates of the current point
  float startLON = (row.getFloat("LONP") - 24.0) * 90 + 50; 
  float startLAT = (90 - row.getFloat("LATP") - 35) * 180 +300; 

  // Get the coordinates of the next point
  float endLON = (MinardTable.getRow(i + 1).getFloat("LONP") - 24.0) * 90 + 50; 
  float endLAT = (90 - MinardTable.getRow(i + 1).getFloat("LATP") - 35) * 180 + 300; 

  // Compute the angle to rotate the rectangles to match the direction of travel
  float angle = atan2(endLAT - startLAT, endLON - startLON);

  // Adjust the distance between rectangles by slightly overlapping them
  float rectDistance = dist(startLON, startLAT, endLON, endLAT);
  float overlap = rectWidth * 0.8;  // Slight overlap to fill gaps

  // Calculate the number of rectangles needed to fill the gap between points
  int numRects = int(rectDistance / (rectWidth - overlap));

  // Draw rectangles along the path from start to end, with slight overlap
  for (int j = 0; j < numRects; j++) {
    float x = lerp(startLON, endLON, j / float(numRects));
    float y = lerp(startLAT, endLAT, j / float(numRects));
    // Push and pop matrix to rotate each rectangle individually
    pushMatrix();
    translate(x, y);
    rotate(angle);
    rect(0, -rectHeight / 2, rectWidth, rectHeight);
    popMatrix();
  }
}

void tempCurve(){
  // Set font for temperature labels
  PFont title = createFont("Georgia", 14, true);
  textFont(title);
  fill(33, 47, 60);
  textAlign(CENTER, CENTER);
  
  // Draw Y-axis line
  stroke(0, 0, 0);
  line(axisX, axisTop, axisX, axisBottom);  // Vertical line for the Y-axis
  // Label for the Y-axis title
  fill(0, 0, 0);
  text("Temperature [°C]", axisX + 60, axisTop - 30);  // Title positioned above Y-axis
  
  // Draw temperature ticks and labels on Y-axis from 0°C to -30°C
  for (int i = 0; i <= 6; i++) {
    int temp = -5 * i;  // Temperature values from 0°C to -30°C
    float posY = axisTop + i * 25;  // Calculate tick position
    stroke(0, 0, 0);
    line(axisX - 5, posY, axisX, posY);  // Short horizontal lines for ticks
    fill(0, 0, 0);
    text(temp, axisX + 20, posY);  // Labels for temperature values
  }
  
  // Temperature point curve (Total Number 9)
  for (int i = 0; i < 9; i++) {              
    TableRow row = MinardTable.getRow(i);
    float tempLONG = (row.getFloat("LONT") - 24.0) * 90 + 50;
    float tempLAT = row.getFloat("TEMP");
    float nextLONG = (MinardTable.getRow(i + 1).getFloat("LONT") - 24.0) * 90 + 50;
    float nextLAT = MinardTable.getRow(i + 1).getFloat("TEMP");
    
    stroke(96, 96, 96);  // Red color for temperature curve
    strokeWeight(3);
    line(tempLONG, 620 - tempLAT * 5, nextLONG, 620 - nextLAT * 5);  // Scale factor for temp height
    
    // Labels for temperature at each data point
    fill(255, 0, 0);
    text(tempLAT + "°C", tempLONG, 620 - tempLAT * 5 - 10);
    
    // Display the date label
    fill(0, 0, 0);
    text(Temp_Dates[i], tempLONG, 820);
    
    // Match longitude of temperature with the army data and draw corresponding lines
    for (int j = 0; j < MinardTable.getRowCount(); j++) {
      TableRow armyRow = MinardTable.getRow(j);
      float armyLONG = (armyRow.getFloat("LONC") - 24.0) * 90 + 50;
      
      if (tempLONG == armyLONG) { 
        float armyLAT = (90 - armyRow.getFloat("LATC") - 35) * 180 + 300;
        stroke(0, 0, 0);
        strokeWeight(1);
        line(tempLONG, 620 - tempLAT * 5, armyLONG, armyLAT); 
      }
    }
  }
}
