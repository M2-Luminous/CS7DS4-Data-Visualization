Table gapminderTable;
int chartNumber = 1;  // Track the current chart

void setup() {
  size(900, 700);
  gapminderTable = loadTable("gapminder.csv", "header");
  noLoop();
}

void draw() {
  background(255);
  
  // Chart 4: Color Encoding
  if (chartNumber == 1) {
    visualizeLifeExpectancyByColor();
  }
  
  // Chart 5: Shape Encoding
  else if (chartNumber == 2) {
    visualizeLifeExpectancyByShape();
  }
  
  // Chart 6: Opacity Encoding
  else if (chartNumber == 3) {
    visualizeLifeExpectancyByOrientation();
  }
}

void keyPressed() {
  if (key == ' ') {
    chartNumber++;
    if (chartNumber > 3) {
      chartNumber = 1;
    }
    redraw();
  }
}

// Chart 4: Color Encoding
void visualizeLifeExpectancyByColor() {
  text("Life Expectancy over Time (Color Encoding for Continent)", 200, 20);
  drawAxes();

  for (TableRow row : gapminderTable.rows()) {
    float year = row.getFloat("year");
    float lifeExp = row.getFloat("lifeExp");
    String country = row.getString("country");
    String continent = row.getString("continent");

    float x = map(year, 1952, 2007, 100, 800);
    float y = map(lifeExp, 20, 90, 650, 50);

    // Color encoding based on continent
    if (continent.equals("Europe")) {
      fill(255, 0, 0, 100); // Red for Europe
    } else if (continent.equals("Asia")) {
      fill(0, 255, 0, 100); // Green for Asia
    } else if (continent.equals("Africa")) {
      fill(0, 0, 255, 100); // Blue for Africa
    } else if (continent.equals("Americas")) {
      fill(255, 165, 0, 100); // Orange for Americas
    } else {
      fill(128, 0, 128, 100); // Purple for Oceania
    }

    // Differentiate Ireland
    if (country.equals("Ireland")) {
      fill(0, 0, 0); // Highlight Ireland in black
      ellipse(x, y, 20, 20);
    }
    noStroke();
    ellipse(x, y, 10, 10);
  }

  // Draw Legend
  drawLegend("Color");
}



// Chart 5: Shape Encoding with Transparency
void visualizeLifeExpectancyByShape() {
  text("Life Expectancy over Time (Shape Encoding for Continent)", 200, 20);
  drawAxes();

  for (TableRow row : gapminderTable.rows()) {
    float year = row.getFloat("year");
    float lifeExp = row.getFloat("lifeExp");
    String country = row.getString("country");
    String continent = row.getString("continent");

    float x = map(year, 1952, 2007, 100, 800);
    float y = map(lifeExp, 20, 90, 650, 50);
    
    // Set transparency (alpha) value to 150
    fill(100, 100, 255, 100); // Blue-ish with alpha 150

    // Shape encoding based on continent
    if (continent.equals("Europe")) {
      // Triangle for Europe
      float halfSize = 10 / 2;
      beginShape();
      vertex(x, y - halfSize);
      vertex(x + halfSize, y + halfSize);
      vertex(x - halfSize, y + halfSize);
      endShape(CLOSE);
    } else if (continent.equals("Asia")) {
      // Square for Asia
      rectMode(CENTER);
      rect(x, y, 10, 10);
    } else if (continent.equals("Africa")) {
      // Pentagon for Africa
      beginShape();
      for (int i = 0; i < 5; i++) {
        float angle = TWO_PI * i / 5;
        float px = x + cos(angle) * 10;
        float py = y + sin(angle) * 10;
        vertex(px, py);
      }
      endShape(CLOSE);
    } else if (continent.equals("Americas")) {
      // Star for Americas
      beginShape();
      for (int i = 0; i < 10; i++) {
        float angle = TWO_PI * i / 10;
        float r = (i % 2 == 0) ? 10 : 5;
        float px = x + cos(angle) * r;
        float py = y + sin(angle) * r;
        vertex(px, py);
      }
      endShape(CLOSE);
    } else {
      // Semi-circle for Oceania
      arc(x, y, 20, 20, PI, TWO_PI);
    }

    // Differentiate Ireland with a black circle (also semi-transparent)
    if (country.equals("Ireland")) {
      fill(0, 0, 0); // Black with alpha 150
      ellipse(x, y, 20, 20);
    }
  }
  
  // Draw Legend
  drawLegend("Shape");
}


// Chart 6: Orientation Encoding
void visualizeLifeExpectancyByOrientation() {
  text("Life Expectancy over Time (Orientation Encoding for Continent)", 200, 20);
  drawAxes();

  for (TableRow row : gapminderTable.rows()) {
    float year = row.getFloat("year");
    float lifeExp = row.getFloat("lifeExp");
    String country = row.getString("country");
    String continent = row.getString("continent");

    float x = map(year, 1952, 2007, 100, 800);
    float y = map(lifeExp, 20, 90, 650, 50);
    
    stroke(0);
    float length = 10;

    // Orientation encoding based on continent
    if (continent.equals("Europe")) {
      line(x - length, y - length, x + length, y + length); // Diagonal line for Europe
    } else if (continent.equals("Asia")) {
      line(x, y - length, x, y + length); // Vertical line for Asia
    } else if (continent.equals("Africa")) {
      line(x - length, y, x + length, y); // Horizontal line for Africa
    } else if (continent.equals("Americas")) {
      line(x - length, y - length, x + length, y + length);
      line(x - length, y + length, x + length, y - length); // Cross for Americas
    } else {
      line(x - length, y + length, x + length, y - length); // Diagonal line for Oceania
    }

    // Differentiate Ireland
    if (country.equals("Ireland")) {
      fill(0, 0, 0); // Highlight Ireland
      ellipse(x, y, 20, 20);
    }
  }
  
  // Draw Legend
  drawLegend("Orientation");
}

void drawAxes() {
  stroke(0);
  fill(0);
  line(50, 650, 800, 650); // X-axis
  line(50, 50, 50, 650); // Y-axis
  text("Year", 845, 650); // X-axis label
  text("Life Expectancy", 50, 40); // Y-axis label

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

void drawLegend(String encodingType) {
  float legendX = 700;
  float legendY = 500;
  
  textAlign(LEFT);
  textSize(12);
  
  // Color Encoding Legend
  if (encodingType.equals("Color")) {
    fill(0);
    text("Color Encoding", legendX, legendY);
    fill(255, 0, 0); // Red
    ellipse(legendX, legendY + 20, 10, 10);
    fill(0);
    text("Europe", legendX + 20, legendY + 25);
    
    fill(0, 255, 0); // Green
    ellipse(legendX, legendY + 40, 10, 10);
    fill(0);
    text("Asia", legendX + 20, legendY + 45);
    
    fill(0, 0, 255); // Blue
    ellipse(legendX, legendY + 60, 10, 10);
    fill(0);
    text("Africa", legendX + 20, legendY + 65);
    
    fill(255, 165, 0); // Orange
    ellipse(legendX, legendY + 80, 10, 10);
    fill(0);
    text("Americas", legendX + 20, legendY + 85);
    
    fill(128, 0, 128); // Purple
    ellipse(legendX, legendY + 100, 10, 10);
    fill(0);
    text("Oceania", legendX + 20, legendY + 105);
    
    fill(0); // Black
    ellipse(legendX, legendY + 120, 10, 10);
    fill(0);
    text("Ireland", legendX + 20, legendY + 125);
  }
  
  // Shape Encoding Legend
  else if (encodingType.equals("Shape")) {
    fill(0);
    text("Shape Encoding", legendX, legendY);
    
    fill(100, 100, 255, 150); // Triangle for Europe
    beginShape();
    vertex(legendX, legendY + 25);
    vertex(legendX + 5, legendY + 35);
    vertex(legendX - 5, legendY + 35);
    endShape(CLOSE);
    fill(0);
    text("Europe", legendX + 20, legendY + 35);
    
    rectMode(CENTER);
    fill(100, 100, 255, 150); // Square for Asia
    rect(legendX, legendY + 50, 10, 10);
    fill(0);
    text("Asia", legendX + 20, legendY + 55);
    
    beginShape(); // Pentagon for Africa
    fill(100, 100, 255, 150);
    for (int i = 0; i < 5; i++) {
      float angle = TWO_PI * i / 5;
      float px = legendX + cos(angle) * 10;
      float py = legendY + 70 + sin(angle) * 10;
      vertex(px, py);
    }
    endShape(CLOSE);
    fill(0);
    text("Africa", legendX + 20, legendY + 75);
    
    beginShape(); // Star for Americas
    fill(100, 100, 255, 150);
    for (int i = 0; i < 10; i++) {
      float angle = TWO_PI * i / 10;
      float r = (i % 2 == 0) ? 10 : 5;
      float px = legendX + cos(angle) * r;
      float py = legendY + 90 + sin(angle) * r;
      vertex(px, py);
    }
    endShape(CLOSE);
    fill(0);
    text("Americas", legendX + 20, legendY + 95);
    
    fill(100, 100, 255, 150);
    arc(legendX, legendY + 120, 10 * 2, 10 * 2, PI, TWO_PI); // Semi-circle for Oceania
    fill(0);
    text("Oceania", legendX + 20, legendY + 115);
    
    fill(0); // Black Circle for Ireland
    ellipse(legendX, legendY + 130, 10, 10);
    text("Ireland", legendX + 20, legendY + 135);
  }
  
  // Orientation Encoding Legend
  else if (encodingType.equals("Orientation")) {
    text("Legend (Orientation Encoding)", legendX, legendY);
    
    line(legendX - 10, legendY + 10, legendX + 10, legendY + 30); // Diagonal line for Europe
    fill(0);
    text("Europe", legendX + 20, legendY + 25);
    
    line(legendX, legendY + 30, legendX, legendY + 50); // Vertical line for Asia
    fill(0);
    text("Asia", legendX + 20, legendY + 45);
    
    line(legendX - 10, legendY + 60, legendX + 10, legendY + 60); // Horizontal line for Africa
    fill(0);
    text("Africa", legendX + 20, legendY + 65);
    
    // Cross for Americas
    line(legendX - 10, legendY + 70, legendX + 10, legendY + 90);
    line(legendX - 10, legendY + 90, legendX + 10, legendY + 70);
    fill(0);
    text("Americas", legendX + 20, legendY + 85);
    
    line(legendX - 10, legendY + 115, legendX + 10, legendY + 95);
    fill(0);
    text("Oceania", legendX + 20, legendY + 110);
    
    fill(0, 0, 0); // Black Circle for Ireland
    ellipse(legendX, legendY + 125, 10, 10);
    fill(0);
    text("Ireland", legendX + 20, legendY + 130);
  }
}
