Table gapminderTable;
float minGDP, maxGDP, minLifeExp, maxLifeExp, minPop, maxPop;
color irelandColor = color(0, 0, 255); // Ireland color (blue)
int[] popValues = {100000, 1000000, 10000000, 100000000};
int[] popValuesColor = {50000,100000, 5000000, 10000000, 250000000, 500000000, 1000000000};
float legendX = 750;
float legendY = 500;
int chartNumber = 1;  // Track the current chart

void setup() {
  size(900, 700);
  gapminderTable = loadTable("gapminder.csv", "header");
  noLoop(); // Only draw once

  // Calculate min/max for scaling by iterating over rows
  for (TableRow row : gapminderTable.rows()) {
    float gdp = row.getFloat("gdpPercap");
    float lifeExp = row.getFloat("lifeExp");
    float pop = row.getFloat("pop");

    if (gdp < minGDP) minGDP = gdp;
    if (gdp > maxGDP) maxGDP = gdp;
    if (lifeExp < minLifeExp) minLifeExp = lifeExp;
    if (lifeExp > maxLifeExp) maxLifeExp = lifeExp;
    if (pop < minPop) minPop = pop;
    if (pop > maxPop) maxPop = pop;
  }
}

void draw() {
  background(255);
  if (chartNumber == 1) {
    chart1();
  } else if (chartNumber == 2) {
    chart2();
  } else if (chartNumber == 3) {
    chart3();
  }
}

// Use a key press to switch between charts
void keyPressed() {
  if (key == ' ') {  // Press the spacebar to switch charts
    chartNumber++;
    if (chartNumber > 3) {
      chartNumber = 1;
    }
    redraw();  // Call draw() again after the key press
  }
}

void chart1() {
  fill(0);
  textSize(20);
  text("GDP vs Life Expectancy by Circle Size", 300, 20);
  
  textSize(12);
  stroke(0);
  line(50, 650, 800, 650); // X-axis Length 750
  line(50, 650, 50, 50);  // Y-axis Length 600
  text("GDP per capita", 820, 650); // X-axis label
  text("Life Expectancy", 40, 30); // Y-axis label
  
  // Add tick marks and labels for axes
  for (int i = 0; i <= 10; i++) {
    // GDP x-axis tick marks and labels
    float gdpValue = map(i, 0, 10, minGDP, maxGDP);
    float xPos = map(i, 0, 10, 50, 800);
    line(xPos, 640, xPos, 650);
    text(nf(gdpValue, 0, 0), xPos-25, 670);
    
    // Life expectancy y-axis tick marks and labels
    float lifeExpValue = map(i, 0, 10, minLifeExp, maxLifeExp);
    float yPos = map(i, 0, 10, 650, 50);
    line(50, yPos, 60, yPos);
    text(nf(lifeExpValue, 0, 0), 15, yPos + 5);
  }
  
  // Plot the circles representing countries
  for (TableRow row : gapminderTable.rows()) {
    if (row.getInt("year") == 2002) {
      float x = map(row.getFloat("gdpPercap"), minGDP, maxGDP, 100, 1900);
      float y = map(row.getFloat("lifeExp"), minLifeExp, maxLifeExp, 1050, 50);
      float popSize = map(row.getFloat("pop"), minPop, maxPop, 5, 100); // Population as circle size
      
      // Differentiate Ireland
      if (row.getString("country").equals("Ireland")) {
        fill(irelandColor);
        ellipse(x, y, popSize, popSize);
        text("Ireland", x - 20, y + 20); // Label "Ireland"
      } else {
        fill(100, 100, 255, 150);
        noStroke();
        ellipse(x, y, popSize, popSize);
      }
    }
  }

  // Draw each circle and corresponding population label in the legend
  for (int i = 0; i < popValues.length; i++) {
    // Map the population value to the circle size
    float popSize = map(popValues[i], 100000, 100000000, 5, 100); // 5 to 100 size range
    
    // Draw the circle
    fill(0, 0, 255);
    ellipse(legendX, legendY - i * 80 + 100, popSize, popSize);
    
    // Display the population label next to the circle
    fill(0);
    textAlign(LEFT, CENTER);
    text(nfc(popValues[i]), legendX + 50, legendY - i * 80 + 100);
  }

  textSize(18);
  text("legend", legendX, legendY - 200);
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void chart2() {
  fill(0); 
  textSize(20);
  text("Population as Color Brightness",300, 20);
  
  textSize(12);
  stroke(0);
  line(50, 650, 800, 650); // X-axis Length 750
  line(50, 650, 50, 50);  // Y-axis Length 600
  text("GDP per capita", 845, 650); // X-axis label
  text("Life Expectancy", 50, 40); // Y-axis label
  
  // Add tick marks and labels for axes
  for (int i = 0; i <= 10; i++) {
    // GDP x-axis tick marks and labels
    float gdpValue = map(i, 0, 10, minGDP, maxGDP);
    float xPos = map(i, 0, 10, 50, 800);
    line(xPos, 640, xPos, 650);
    text(nf(gdpValue, 0, 0), xPos-25, 670);
    
    // Life expectancy y-axis tick marks and labels
    float lifeExpValue = map(i, 0, 10, minLifeExp,maxLifeExp);
    float yPos = map(i, 0, 10, 650, 50);
    line(50, yPos, 60, yPos);
    text(nf(lifeExpValue, 0, 0), 15, yPos + 5);
  }
  
  // Plot the circles with color brightness representing population
  for (TableRow row : gapminderTable.rows()) {
    if (row.getInt("year") == 2002) {
      float x = map(row.getFloat("gdpPercap"), minGDP, maxGDP, 100, 1900);
      float y = map(row.getFloat("lifeExp"), minLifeExp, maxLifeExp, 1050, 50);
      float popColor = map(row.getFloat("pop"), minPop, maxPop, 0, 255); // Population as color brightness
      
      if (row.getString("country").equals("Ireland")) {
        fill(0, 0, 255);
        stroke(0);
        ellipse(x, y, 10, 10);
        text("Ireland", x - 20, y + 20); // Label "Ireland
      } else {
        fill(popColor, 0, 0, 200); // Vary brightness based on population
        noStroke();
        ellipse(x, y, 10, 10);
      }
    }
  }
  
  // Draw the gradient for color brightness
  for (int i = 0; i < popValuesColor.length; i++) {
    // Map the population value to the color brightness
    float popColor = map(popValuesColor[i], 50000, 1000000000, 0, 255); 
    
    // Draw the color bar for population
    fill(popColor, 0, 0, 200);
    rect(legendX, legendY - i * 20, 20, 20);
    
    // Display the population label next to the color bar
    fill(0);
    textAlign(LEFT, CENTER);
    text(nfc(popValuesColor[i]), legendX + 30, legendY - i * 20 + 10);
  }

  textSize(18);
  text("Population", legendX, legendY - 140);
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
void chart3() {
  fill(0);
  textSize(20);
  text("Population as Texture Complexity", 300, 20); 
  
  textSize(12);
  stroke(0);
  line(50, 650, 800, 650); // X-axis Length 750
  line(50, 650, 50, 50);  // Y-axis Length 600
  text("GDP per capita", 845, 650); // X-axis label
  text("Life Expectancy", 50, 40); // Y-axis label
  
  // Add tick marks and labels for axes
  for (int i = 0; i <= 10; i++) {
    // GDP x-axis tick marks and labels
    float gdpValue = map(i, 0, 10, minGDP, maxGDP);
    float xPos = map(i, 0, 10, 50, 800);
    line(xPos, 640, xPos, 650);
    text(nf(gdpValue, 0, 0), xPos-25, 670);
    
    // Life expectancy y-axis tick marks and labels
    float lifeExpValue = map(i, 0, 10, minLifeExp, maxLifeExp);
    float yPos = map(i, 0, 10, 650, 50);
    line(50, yPos, 60, yPos);
    text(nf(lifeExpValue, 0, 0), 15, yPos + 5);
  }
  
  // Plot circles with different textures representing population
  for (TableRow row : gapminderTable.rows()) {
    if (row.getInt("year") == 2002) {
      float x = map(row.getFloat("gdpPercap"), minGDP, maxGDP, 100, 1900);
      float y = map(row.getFloat("lifeExp"), minLifeExp, maxLifeExp, 1050, 50);
      float popValue = row.getFloat("pop");

      // Highlight Ireland with a black circle
      if (row.getString("country").equals("Ireland")) {
        fill(0);
        ellipse(x, y, 10, 10);
        text("Ireland", x - 20, y + 20); // Label "Ireland
        continue; // Skip the texture drawing for Ireland
      }

      // Draw different textures based on population
      stroke(0);
      fill(255); // White color for other countries
      if (popValue < 100000) {
        ellipse(x, y, 10, 10); 
      } else if (popValue < 5000000) {
        ellipse(x, y, 10, 10);
        line(x - 5, y, x + 5, y); 
      } else if (popValue < 10000000) {
        ellipse(x, y, 10, 10);
        line(x - 5, y, x + 5, y); 
        line(x, y - 5, x, y + 5); 
      } else if (popValue < 250000000) {
        ellipse(x, y, 10, 10);
        for (float i = -5; i <= 5; i += 2) {
            line(x - 5, y + i, x + 5, y + i);
        } 
      } else if (popValue < 500000000) {
        ellipse(x, y, 10, 10);
        for (float i = -5; i <= 5; i += 3) {
            line(x - 5, y + i, x + 5, y + i); // Horizontal lines
            line(x + i, y - 5, x + i, y + 5); // Vertical lines
        } 
      } else if (popValue < 1000000000) {
        ellipse(x, y, 10, 10);
        for (float i = -5; i <= 5; i += 1.5) {
            line(x - 5, y + i, x + 5, y + i); // Horizontal lines
            line(x + i, y - 5, x + i, y + 5); // Vertical lines
        }
      }
    }
  }
  drawTextureLegend();
}

// Draw texture legend
void drawTextureLegend() {
  fill(0);
  textSize(18);
  stroke(0);
  text("Population", legendX - 20, legendY - 250);
  text("100000", legendX + 30, legendY + 5);
  text("5000000", legendX + 30, legendY - 35);
  text("10000000", legendX + 30, legendY - 75);
  text("250000000", legendX + 30, legendY -115);
  text("500000000", legendX + 30, legendY - 155);
  text("1000000000", legendX + 30, legendY - 195);
  
  fill(255);
  ellipse(legendX, legendY, 20, 20);
  
  ellipse(legendX, legendY - 40, 20, 20);
  line(legendX - 10, legendY - 40, legendX + 10, legendY - 40);
  
  ellipse(legendX, legendY - 80, 20, 20);
  line(legendX - 10, legendY - 80, legendX + 10, legendY - 80);
  line(legendX, legendY - 90 , legendX, legendY - 70);
  
  ellipse(legendX, legendY - 120, 20, 20);
  for (float i = -10; i <= 10; i += 2) {
      line(legendX - 10, legendY - 120 + i, legendX + 10, legendY - 120 + i);
  } 
  
  ellipse(legendX, legendY - 160, 20, 20);
  for (float i = -10; i <= 10; i += 4) {
    line(legendX - 10, legendY - 160 + i, legendX + 10, legendY - 160 + i); // Horizontal lines
    line(legendX + i, legendY - 170, legendX + i, legendY - 150); // Vertical lines
  }
  
  ellipse(legendX, legendY - 200, 20, 20);
  for (float i = -10; i <= 10; i += 2) {
    line(legendX - 10, legendY - 200 + i, legendX + 10, legendY - 200 + i); // Horizontal lines
    line(legendX + i, legendY - 210, legendX + i, legendY - 190); // Vertical lines
  }
}
