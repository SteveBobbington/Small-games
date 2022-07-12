import javafx.scene.Scene;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;

import java.util.*;

public class Box {
    private Double xPos;
    private Double yPos;
    private Integer value = 0;
    private Integer boardPos;
    private Boolean selected = false;
    private String displayingTarget = "";

    //the box to be clicked on and drawn on the screen
    public Box(Integer boardPos) {
        this.boardPos = boardPos;
    }

    //scale the box depending on screen/board size and position on the board
    public void rescale(Integer boardSize, Scene scene) {
        //takes 35 or 50 as the offset for the border, then adds the size per square (screen size/board size)
        //and multiplies it by the position on the board the box is (boardPos%boardSize)
        this.xPos = 50.0+((scene.getWidth()-100)/boardSize)*((this.boardPos%boardSize));
        this.yPos = 25.0+((scene.getHeight()-100)/boardSize)*(((this.boardPos-(this.boardPos%boardSize))/boardSize));
    }

    public void draw(GraphicsContext gc, Scene scene, Integer boardSize, HashMap<ArrayList<Integer>, String> groups, Boolean redFill, String fontSize) {
        Integer change = 0;
        if (fontSize.equals("small")) {
            change = -5;
        }
        if (fontSize.equals("large")) {
            change = 5;
        }
        gc.setFont(new Font("Verdana", 25+change));
        if (redFill) {
            gc.setFill(Color.LIGHTSALMON);
            gc.fillRect(this.xPos, this.yPos, (scene.getWidth()-100)/boardSize, (scene.getHeight()-100)/boardSize);
            gc.setFill(Color.BLACK);
        }
        if (this.displayingTarget!="") {
            //make the font smaller for the targets
            gc.setFont(new Font("Verdana", 15+change));
            gc.fillText(this.displayingTarget, (this.xPos+((scene.getWidth()-120)/boardSize)/10), (this.yPos+((scene.getHeight()-110)/boardSize)/4));
            gc.setFont(new Font("Verdana", 25+change));
        }
        //changes style if this is selected
        if (this.selected) {
            gc.setStroke(Color.RED);
            gc.setLineWidth(5);
        }
        //draws the value if there is one
        if (this.value!=0) {
            gc.fillText(this.value.toString(), (this.xPos+((scene.getWidth()-120)/boardSize)/2.1), (this.yPos+((scene.getHeight()-110)/boardSize)/1.7));
        }
        //draws 4 lines to make up the box depending on its starting position (xPos or yPos)
        //and the current screen and board size (scene.getWidth()-100)/boardSize
        //top line
        //check if the box above is in the same group
        if (isInSameGroup(groups, this.boardPos-boardSize) && !this.selected) {
            gc.setLineWidth(1);
        }
        gc.strokeLine(this.xPos, this.yPos, this.xPos+((scene.getWidth()-100)/boardSize), this.yPos);
        //set it back to 3 incase it has been changed (if not selected)
        if (!this.selected) {
            gc.setLineWidth(4);
        }
        //left line
        //check if the box to the left is in the same group
        if (isInSameGroup(groups, this.boardPos-1) && !this.selected) {
            gc.setLineWidth(1);
        }
        gc.strokeLine(this.xPos, this.yPos, this.xPos, this.yPos+((scene.getHeight()-100)/boardSize));
        //set it back to 3 incase it has been changed (if not selected)
        if (!this.selected) {
            gc.setLineWidth(4);
        }
        //right line
        //check if the box to the right is in the same group
        if (isInSameGroup(groups, this.boardPos+1) && !this.selected) {
            gc.setLineWidth(1);
        }
        gc.strokeLine(this.xPos+((scene.getWidth()-100)/boardSize), this.yPos, this.xPos+((scene.getWidth()-100)/boardSize), this.yPos+((scene.getHeight()-100)/boardSize));
        //set it back to 3 incase it has been changed (if not selected)
        if (!this.selected) {
            gc.setLineWidth(4);
        }
        //bottom line
        //check if the box below is in the same group
        if (isInSameGroup(groups, this.boardPos+boardSize) && !this.selected) {
            gc.setLineWidth(1);
        }
        gc.strokeLine(this.xPos, this.yPos+((scene.getHeight()-100)/boardSize), this.xPos+((scene.getWidth()-100)/boardSize), this.yPos+((scene.getHeight()-100)/boardSize));
        gc.setStroke(Color.BLACK);
        //default is thick lines
        gc.setLineWidth(4);
    }

    //checks if a given co-ordinate is inside this box
    public Boolean isInBox(Double x, Double y, Scene scene, Integer boardSize) {
        if (x>this.xPos && x<this.xPos+((scene.getWidth()-100)/boardSize) && y>this.yPos && y<this.yPos+((scene.getHeight()-100)/boardSize)) {
            return true;
        }
        return false;
    }

    public Boolean isInSameGroup(HashMap<ArrayList<Integer>, String> groups, Integer boxToCheck) {
        for (ArrayList<Integer> group : groups.keySet()) {
            if (group.contains(this.boardPos)) {
                if (group.contains(boxToCheck)) {
                    return true;
                }
            }
        }
        return false;
    }

    //check if this is adjacent to another given box
    public Boolean isAdjacent(Integer pos, Integer boardSize) {
        if (this.boardPos%boardSize!=boardSize-1 && this.boardPos==pos-1) {
            return true;
        }
        if (this.boardPos%boardSize!=0 && this.boardPos==pos+1) {
            return true;
        }
        if (this.boardPos==pos+boardSize) {
            return true;
        }
        if (this.boardPos==pos-boardSize) {
            return true;
        }
        return false;
    }

    //a static version to use for load checking
    public static Boolean isAdjacent(Integer thisPos, Integer pos, Integer boardSize) {
        if (thisPos%boardSize!=boardSize-1 && thisPos==pos-1) {
            return true;
        }
        if (thisPos%boardSize!=0 && thisPos==pos+1) {
            return true;
        }
        if (thisPos==pos+boardSize) {
            return true;
        }
        if (thisPos==pos-boardSize) {
            return true;
        }
        return false;
    }

    //selected getter
    public Boolean getSelected() {
        return this.selected;
    }

    //selected setter
    public void changeSelected(Boolean selected) {
        this.selected = selected;
    }

    //displayingTarget setter
    public void setDisplayingTarget(String target) {
        this.displayingTarget = target;
    }

    //value getter
    public Integer getValue() {
        return this.value;
    }

    //board pos getter
    public Integer getBoardPos() {
        return this.boardPos;
    }

    //value setter
    public void setValue(Integer value) {
        this.value = value;
    }

    //increase value by one
    public void increaseValue(Integer boardSize) {
        this.value++;
        if (this.value>boardSize) {
            this.value=1;
        }
    }

    //decrease value by one
    public void decreaseValue(Integer boardSize) {
        this.value--;
        if (this.value<1) {
            this.value=boardSize;
        }
    }
}
