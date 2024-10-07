Table gapminderTable;
float minGDP = Float.MAX_VALUE;
float maxGDP = Float.MIN_VALUE;
float minLifeExp = Float.MAX_VALUE;
float maxLifeExp = Float.MIN_VALUE;
float minPop = Float.MAX_VALUE;
float maxPop = Float.MIN_VALUE;

void setup() {
  size(900, 700);
  gapminderTable = loadTable("gapminder.csv", "header");
  noLoop();
}

void draw() {
  background(255);
  textSize(20);
  fill(0);
  text("Exploratory Visualization of Gapminder Data", 250, 30);
  
  // Calculate min and max for lifeExp, pop and gdpPercap
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

  drawAxes();
  drawDataPoints();
  drawLegend();
}

void drawAxes() {
  stroke(0);
  fill(0);
  line(50, 650, 800, 650); // X-axis
  text("Year", 820, 650); // X-axis label
  line(50, 50, 50, 650); // Y-axis
  text("Life Expectancy", 40, 30); // Y-axis label

  // X-axis labels (year)
  for (int i = 1952; i <= 2007; i += 5) {
    float x = map(i, 1952, 2007, 100, 800);
    line(x, 645, x, 655);
    text(i, x - 10, 670);
  }

  // Y-axis labels (life expectancy)
  for (int i = 20; i <= 90; i += 10) {
    float y = map(i, 20, 90, 650, 50);
    line(45, y, 55, y);
    text(i, 20, y + 5);
  }
}

void drawDataPoints() {
  color[] continentColors = {
    color(255, 0, 0),    // Africa - Red
    color(0, 0, 255),    // Asia - Blue
    color(0, 255, 0),    // Europe - Green
    color(255, 165, 0),  // Americas - Orange
    color(128, 0, 128)   // Oceania - Purple
  };

  for (TableRow row : gapminderTable.rows()) {
    float year = row.getFloat("year");
    float lifeExp = row.getFloat("lifeExp");
    float pop = row.getFloat("pop");
    float gdp = row.getFloat("gdpPercap");
    
    // Scale population for circle size
    float popScaled = map(pop, minPop, maxPop, 10, 60);
    
    // Determine GDP level (1 to 4)
    int gdpLevelIndex = (int)map(gdp, minGDP, maxGDP, 1, 4);
    
    // Position for year and life expectancy
    float x = map(year, 1952, 2007, 100, 800);
    float y = map(lifeExp, minLifeExp, maxLifeExp, 650, 50);

    // Set color based on continent
    color fillColor = continentColors[getContinentIndex(row.getString("continent"))];
    fill(fillColor, 150);
    
    // Draw the shape based on GDP category
    if (row.getString("country").equals("Ireland")) {
      stroke(0);
      fill(0); // Distinguishable black circle for Ireland
      ellipse(x, y, popScaled*2, popScaled*2);
    } else {
      switch (gdpLevelIndex) {

        case 1: // Level 1 (Lowest) - Circle
          noStroke();
          ellipse(x, y, popScaled, popScaled); 
          break;
        case 2: // Level 2 - Triangle
          stroke(0);
          beginShape();
          vertex(x, y - popScaled/1.2);
          vertex(x + popScaled/1.2, y + popScaled/1.2);
          vertex(x - popScaled/1.2, y + popScaled/1.2);
          endShape(CLOSE); // Triangle
          break;
        case 3: // Level 3 - Rectangle
          stroke(0);
          rectMode(CENTER);
          rect(x, y, popScaled*1.5, popScaled*1.5); 
          break;
        case 4: // Level 4 (Highest) - Star
          stroke(0);          
          beginShape();
          for (int i = 0; i < 5; i++) {
            float angle = TWO_PI / 5 * i + PI / 2; // Star shape
            float xOffset = cos(angle) * popScaled;
            float yOffset = sin(angle) * popScaled;
            vertex(x + xOffset, y - yOffset);
          }
          endShape(CLOSE);
          break;
      }
    }
  }
}

// Function to determine continent index
int getContinentIndex(String continent) {
  switch (continent) {
    case "Africa": return 0;
    case "Asia": return 1;
    case "Europe": return 2;
    case "Americas": return 3;
    case "Oceania": return 4;
    default: return 0; // Default to Africa
  }
}


// Function to draw legend
void drawLegend() {
  fill(255, 255, 255, 0);
  stroke(0);
  rect(790, 570, 200, 130); // Legend background
  textSize(12);
  
  fill(0);
  text("GDP Levels", 700, 520);
  text("Continents", 820, 520);
  ellipse(700, 540, 10, 10); // Circle 30 80
  text("Level 1 (Lowest)", 715, 545);
  
  beginShape();
  vertex(700, 560 - 5);
  vertex(700 + 5, 560 + 5);
  vertex(700 - 5, 560 + 5);
  endShape(CLOSE); // Triangle
  text("Level 2", 715, 565);
  
  rectMode(CORNER);
  rect(695, 575, 10, 10); // Rectangle
  text("Level 3", 715, 585);
  
  beginShape();
    for (int i = 0; i < 5; i++) {
      float angle = TWO_PI / 5 * i + PI / 2; // Star shape
      float xOffset = cos(angle) * 5;
      float yOffset = sin(angle) * 5;
      vertex(700 + xOffset, 600 - yOffset);
    }
    endShape(CLOSE);
  text("Level 4 (Highest)", 715, 605);
  
  // Continent colors legend
  fill(255, 0, 0);
  ellipse(820, 540, 10, 10); // Africa 150 -195
  fill(0);
  text("Africa", 830, 545);
  
  fill(0, 0, 255);
  ellipse(820, 555, 10, 10); // Asia
  fill(0);
  text("Asia", 830, 560);
  
  fill(0, 255, 0);
  ellipse(820, 570, 10, 10); // Europe
  fill(0);
  text("Europe", 830, 575);
  
  fill(255, 165, 0);
  ellipse(820, 585, 10, 10); // Americas
  fill(0);
  text("Americas", 830, 590);
  
  fill(128, 0, 128);
  ellipse(820, 600, 10, 10); // Oceania
  fill(0);
  text("Oceania", 830, 605);
  
  fill(0);
  ellipse(820, 620, 20, 20); // Ireland
  fill(0);
  text("Ireland", 835, 625);
}
