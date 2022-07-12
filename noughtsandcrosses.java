package lab3;

import javafx.application.Application;
import javafx.event.EventHandler;
import javafx.scene.Scene;
import javafx.scene.canvas.*;
import javafx.scene.layout.*;
import javafx.scene.image.*;
import javafx.scene.input.*;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.stage.Stage;

public class Main extends Application {
	private Integer[] board= {0, 0, 0, 0, 0, 0, 0, 0, 0};
	private boolean cross = true;
	private Canvas canvas = new Canvas(400, 400);
	private GraphicsContext gc = canvas.getGraphicsContext2D();
	private Pane root = new Pane();
	private Scene scene = new Scene(root);
	private Stage stage;
	
	public void start(Stage stage) {
		this.stage = stage;
		
		this.gc.setLineWidth(2);
		this.gc.setFill(Color.BLUE);
		
		root.setStyle("-fx-padding: 10;" +
                "-fx-border-width: 3;" +
                "-fx-border-insets: 10;" +
                "-fx-border-radius: 15;" +
                "-fx-border-color: orange;");
		
		this.gc.setFont(new Font("Verdana", 25));
		
        root.getChildren().add(this.canvas);
        
        root.addEventHandler(MouseEvent.MOUSE_CLICKED, new MouseHandler());
        
        redraw();
        this.scene.heightProperty().addListener(observable -> redraw());
		this.scene.widthProperty().addListener(observable -> redraw());
        
        this.stage.setScene(this.scene);
        this.stage.setTitle("noughts and crosses");
        this.stage.show();
	}
	
	public static void main(String[] args) {
		launch(args);
	}
	
	public void changeTurn() {
		if (this.cross==true) {
			this.cross=false;
		}
		else {
			this.cross=true;
		}
	}
	
	public Integer hasWon() {
		//check vertical wins
		for (int i=0; i<3; i++) {
			if (this.board[i]!=0 && this.board[i]==this.board[i+3] && this.board[i]==this.board[i+6]) {
				return this.board[i];
			}
		}
		//check horizontal wins
		for (int i=0; i<9; i=i+3) {
			if (this.board[i]!=0 && this.board[i]==this.board[i+1] && this.board[i]==this.board[i+2]) {
				return this.board[i];
			}
		}
		//check diagonal wins
		if (this.board[0]!=0 && this.board[0]==this.board[4] && this.board[0]==this.board[8]) {
			return this.board[0];
		}
		if (this.board[2]!=0 && this.board[2]==this.board[4] && this.board[2]==this.board[6]) {
			return this.board[2];
		}
		return 0;
	}
	
	class MouseHandler implements EventHandler<MouseEvent> {
    	public void handle(MouseEvent e) {
    		//the winning player (if there is one)
    		Integer won = 0;
    		//not off the right or bottom
    		if (e.getX()<Main.this.rescale(390.0, true) && e.getY()<Main.this.rescale(390.0, false)) {
    			//right side
    			if (e.getX()>Main.this.rescale(280.0, true)) {
    				if (e.getY()>Main.this.rescale(280.0, false)) {
    					//if the square clicked in is empty
    					if (Main.this.board[8]==0) {
    						//whos turn is it
	    					if (Main.this.cross==true) {
	    						//set a cross
	    						Main.this.board[8]=1;
	    					}
	    					else {
	    						//set a nought
	    						Main.this.board[8]=2;
	    					}
	    					//change which turn it is and check if theres a winner
	    					Main.this.changeTurn();
	    					won = Main.this.hasWon();
    					}
    				}
    				else if (e.getY()>Main.this.rescale(170.0, false)) {
    					if (Main.this.board[5]==0) {
	    					if (Main.this.cross==true) {
	    						Main.this.board[5]=1;
	    					}
	    					else {
	    						Main.this.board[5]=2;
	    					}
	    					//change which turn it is and check if theres a winner
	    					Main.this.changeTurn();
	    					won = Main.this.hasWon();
    					}
    				}
    				else if (e.getY()>Main.this.rescale(75.0, false)) {
    					if (Main.this.board[2]==0) {
	    					if (Main.this.cross==true) {
	    						Main.this.board[2]=1;
	    					}
	    					else {
	    						Main.this.board[2]=2;
	    					}
	    					//change which turn it is and check if theres a winner
	    					Main.this.changeTurn();
	    					won = Main.this.hasWon();
    					}
    				}
    			}
    			//middle
    			else if (e.getX()>Main.this.rescale(170.0, true)) {
    				if (e.getY()>Main.this.rescale(280.0, false)) {
    					if (Main.this.board[7]==0) {
	    					if (Main.this.cross==true) {
	    						Main.this.board[7]=1;
	    					}
	    					else {
	    						Main.this.board[7]=2;
	    					}
	    					//change which turn it is and check if theres a winner
	    					Main.this.changeTurn();
	    					won = Main.this.hasWon();
    					}
    				}
    				else if (e.getY()>Main.this.rescale(170.0, false)) {
    					if (Main.this.board[4]==0) {
	    					if (Main.this.cross==true) {
	    						Main.this.board[4]=1;
	    					}
	    					else {
	    						Main.this.board[4]=2;
	    					}
	    					//change which turn it is and check if theres a winner
	    					Main.this.changeTurn();
	    					won = Main.this.hasWon();
    					}
    				}
    				else if (e.getY()>Main.this.rescale(75.0, false)) {
    					if (Main.this.board[1]==0) {
	    					if (Main.this.cross==true) {
	    						Main.this.board[1]=1;
	    					}
	    					else {
	    						Main.this.board[1]=2;
	    					}
	    					//change which turn it is and check if theres a winner
	    					Main.this.changeTurn();
	    					won = Main.this.hasWon();
    					}
    				}
    			}
    			//left side
    			else if (e.getX()>Main.this.rescale(55.0, true)) {
    				if (e.getY()>Main.this.rescale(280.0, false)) {
    					if (Main.this.board[6]==0) {
	    					if (Main.this.cross==true) {
	    						Main.this.board[6]=1;
	    					}
	    					else {
	    						Main.this.board[6]=2;
	    					}
	    					//change which turn it is and check if theres a winner
	    					Main.this.changeTurn();
	    					won = Main.this.hasWon();
    					}
    				}
    				else if (e.getY()>Main.this.rescale(170.0, false)) {
    					if (Main.this.board[3]==0) {
	    					if (Main.this.cross==true) {
	    						Main.this.board[3]=1;
	    					}
	    					else {
	    						Main.this.board[3]=2;
	    					}
	    					//change which turn it is and check if theres a winner
	    					Main.this.changeTurn();
	    					won = Main.this.hasWon();
    					}
    				}
    				else if (e.getY()>Main.this.rescale(75.0, false)) {
    					if (Main.this.board[0]==0) {
	    					if (Main.this.cross==true) {
	    						Main.this.board[0]=1;
	    					}
	    					else {
	    						Main.this.board[0]=2;
	    					}
	    					//change which turn it is and check if theres a winner
	    					Main.this.changeTurn();
	    					won = Main.this.hasWon();
    					}
    				}
    			}
    		}
    		//redraw the screen
    		Main.this.redraw();
    		//has a player won
    		if (won!=0) {
    			String winner;
    			if (won == 1) {
    				winner = "crosses";
    			}
    			else {
    				winner = "noughts";
    			}
    			Main.this.gc.fillText(winner + " has won the game", Main.this.rescale(50.0, true), Main.this.rescale(40.0, false));
    			//remove the listeners
    			Main.this.root.removeEventHandler(MouseEvent.MOUSE_CLICKED, this);
    		}
    	}
    }
	
	public Double rescale(Double number, Boolean xaxis) {
		Double scale;
		if (xaxis) {
			scale = this.scene.getWidth();
		}
		else {
			scale = this.scene.getHeight();
		}
		return (number/446.0)*scale;
	}
	
	public void redraw() {
		this.gc.clearRect(0, 0, this.canvas.getWidth(), this.canvas.getHeight());
		if (this.scene.getWidth()>200 || this.scene.getHeight()>200) {
			this.canvas.setWidth(this.scene.getWidth());
			this.canvas.setHeight(this.scene.getHeight());
		}
		Double[][][] lines = {
			{{50.0, 150.0}, {350.0, 150.0}},
			{{150.0, 65.0}, {150.0, 350.0}},
			{{50.0, 250.0}, {350.0, 250.0}},
			{{250.0, 65.0}, {250.0, 350.0}}};
		for (Double[][] line : lines) {
			for (Double[] coord : line) {
				coord[0] = (coord[0]/400.0)*this.scene.getWidth();
				coord[1] = (coord[1]/400.0)*this.scene.getHeight();
			}
		}
		this.gc.strokeLine(lines[0][0][0], lines[0][0][1], lines[0][1][0], lines[0][1][1]);
		this.gc.strokeLine(lines[1][0][0], lines[1][0][1], lines[1][1][0], lines[1][1][1]);
		this.gc.strokeLine(lines[2][0][0], lines[2][0][1], lines[2][1][0], lines[2][1][1]);
		this.gc.strokeLine(lines[3][0][0], lines[3][0][1], lines[3][1][0], lines[3][1][1]);
		
		Image X = new Image("file:X.png");
        Image O = new Image("file:O.png");
        Image empty = new Image("file:empty.png");
        Image imageToDraw = empty;
        
        Double[] coords = {60.0, 65.0, 100.0, 100.0};
        coords[0] = rescale(coords[0], true);
        coords[1] = rescale(coords[1], false);
        coords[2] = rescale(coords[2], true);
        coords[3] = rescale(coords[3], false);
        for (int i : this.board) {
			switch (i) {
				case 0:
					imageToDraw = empty;
					break;
				case 1:
					imageToDraw = X;
					break;
				case 2:
					imageToDraw = O;
			}
			this.gc.drawImage(imageToDraw, coords[0], coords[1], coords[2], coords[3]);
			coords[0] = coords[0] + rescale(110.0, true);
			if (coords[0]>rescale(300.0, true)) {
				coords[0]=rescale(60.0, true);
				coords[1]=coords[1]+rescale(110.0, false);
			}
		}
	}
}
