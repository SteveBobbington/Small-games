import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.event.EventHandler;
import javafx.scene.Scene;
import javafx.scene.canvas.*;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.input.*;
import javafx.scene.paint.Color;
import javafx.scene.image.*;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import javafx.scene.media.*;

import java.io.*;
import java.util.*;

public class Main extends Application {
    //canvas
    private Canvas canvas = new Canvas(600, 600);
    private GraphicsContext gc = canvas.getGraphicsContext2D();
    //whole screen
    private VBox root = new VBox();
    //the buttons at the top
    private HBox buttons1 = new HBox(5);
    //the buttons at the bottom
    private HBox fontPane = new HBox(5);
    //the grid
    private Pane game = new Pane();
    //win screen
    private StackPane winPane = new StackPane();
    private Canvas winCanvas = new Canvas(600, 600);
    private GraphicsContext winGc = winCanvas.getGraphicsContext2D();
    //pane for the winning screen and the game
    private StackPane stack = new StackPane();
    private Scene scene = new Scene(stack);
    private Stage stage;
    //the array for the board
    private Box[] board;
    //the boards size
    private Integer boardSize;
    //list of groups in the puzzle
    private HashMap<ArrayList<Integer>, String> groups = new HashMap<ArrayList<Integer>, String>();
    //the correct answers
    private Integer[] answers;
    //whether mistakes are being shown
    private Boolean showMistakes = false;
    //the stack for undo
    //the first item is the index of the cell (or -1 if the board was cleared)
    //and the other elements is the value of the cell (or all the cells) before they were changed
    private Stack<Integer[]> actions = new Stack<Integer[]>();
    //the same, for redo
    private Stack<Integer[]> undos = new Stack<Integer[]>();
    //the drop down menu for font size
    private ComboBox fontSize = new ComboBox(FXCollections.observableArrayList("small", "medium", "large"));
    //whether the code was imported or not

    public void start(Stage stage) {
        //the font label
        Label fontL = new Label("Font size: ");
        //create the buttons
        Button undoB = new Button("undo");
        Button redoB = new Button("redo");
        Button clearBoardB = new Button("clear the board");
        Button showCorrectAnswersB = new Button("Show correct answers");
        Button hintB = new Button("Hint");
        Button showMistakesB = new Button("show mistakes");
        //add them to the pane
        this.buttons1.getChildren().addAll(undoB, redoB, clearBoardB, showCorrectAnswersB, hintB, showMistakesB);
        this.fontPane.getChildren().addAll(fontL, this.fontSize);

        //functions for buttons
        undoB.setOnAction(undo -> {
            Integer[] actionToRedo = this.actions.pop();
            for (Integer i :actionToRedo) {
            }
            if (actionToRedo[0]==-1) {
                //add the undo to undos
                Integer[] action = new Integer[this.boardSize*this.boardSize+1];
                action[0] = -1;
                for (int i=1; i<this.boardSize*this.boardSize+1; i++) {
                    action[i] = this.board[i-1].getValue();
                }
                this.undos.push(action);
                //undo the action
                for (int i=0; i<this.boardSize*this.boardSize; i++) {
                    this.board[i].setValue(actionToRedo[i+1]);
                }
            }
            else {
                //add the undo to undos
                this.undos.push(new Integer[]{this.board[actionToRedo[0]].getBoardPos(), this.board[actionToRedo[0]].getValue()});
                //undo the action
                this.board[actionToRedo[0]].setValue(actionToRedo[1]);
            }
            redraw();
        });
        redoB.setOnAction(redo -> {
            Integer[] undo = this.undos.pop();
            for (Integer i : undo) {
            }
            if (undo[0]==-1) {
                //add the redo to actions
                Integer[] action = new Integer[this.boardSize*this.boardSize+1];
                action[0] = -1;
                for (int i=1; i<this.boardSize*this.boardSize+1; i++) {
                    action[i] = this.board[i-1].getValue();
                }
                //redo the action
                for (int i=0; i<this.boardSize*this.boardSize; i++) {
                    this.board[i].setValue(undo[i+1]);
                }
            }
            else {
                //add the redo to actions
                this.actions.push(new Integer[]{this.board[undo[0]].getBoardPos(), this.board[undo[0]].getValue()});
                //redo the action
                this.board[undo[0]].setValue(undo[1]);
            }
            redraw();
        });
        clearBoardB.setOnAction(clearBoard -> {
            //make an alert to check if you want to clear the board
            Alert alert = new Alert(Alert.AlertType.CONFIRMATION);
            alert.setTitle("Clear board");
            alert.setHeaderText(null);
            alert.setContentText("Are you sure?");

            Optional<ButtonType> result = alert.showAndWait();
            if (result.get() == ButtonType.OK){
                //add this to the array of actions
                Integer[] action = new Integer[this.boardSize*this.boardSize+1];
                action[0] = -1;
                for (int i=1; i<this.boardSize*this.boardSize+1; i++) {
                    action[i] = this.board[i-1].getValue();
                }
                //add this action to actions
                this.actions.push(action);
                //clear the undos stack
                this.undos.clear();
                //clear the board
                for (Box box : this.board) {
                    box.setValue(0);
                }
                redraw();
            }
        });
        showCorrectAnswersB.setOnAction(showCorrectAnswers -> {
            //show all the correct answers for each box
            for (int i = 0; i<this.boardSize*this.boardSize; i++) {
                this.board[i].setValue(this.answers[i]);
            }
            redraw();
        });
        hintB.setOnAction(hint -> {
            Random r = new Random();
            //find a box with value 0
            Integer hintIndex = r.nextInt(this.boardSize*this.boardSize);
            while (this.board[hintIndex].getValue()!=0) {
                hintIndex = r.nextInt(this.boardSize*this.boardSize);
            }
            //reveal the correct answer for it
            Integer[] action = {hintIndex, this.board[hintIndex].getValue()};
            this.actions.push(action);
            this.board[hintIndex].setValue(this.answers[hintIndex]);
            redraw();
        });
        showMistakesB.setOnAction(changeShowMistakes -> {
            if (this.showMistakes==true) {
                this.showMistakes = false;
            }
            else {
                this.showMistakes = true;
            }
            redraw();
        });

        this.stage = stage;
        this.stack.getChildren().addAll(this.root, this.winPane);

        //dont show the win pane
        this.winPane.setVisible(false);

        //set the default value for the combo box
        this.fontSize.setValue("medium");

        //make an alert to check what type of game to play
        Alert gameType = new Alert(Alert.AlertType.CONFIRMATION);
        gameType.setTitle("Game type");
        gameType.setHeaderText(null);
        gameType.setContentText("How do you want the puzzle created?");
        ButtonType importTextB = new ButtonType("Import some text");
        ButtonType importFileB = new ButtonType("Import a file");
        ButtonType generateB = new ButtonType("Generate it randomly");
        gameType.getButtonTypes().setAll(importTextB, importFileB, generateB);
        Optional<ButtonType> result = gameType.showAndWait();
        //if the choice was import
        if (result.get() == importTextB || result.get() == importFileB){
            showCorrectAnswersB.setVisible(false);
            hintB.setVisible(false);
            //if youre importing text
            if (result.get() == importTextB) {
                //input the text to an alert
                TextInputDialog textImport = new TextInputDialog("Enter here");
                textImport.setTitle("Text import");
                textImport.setHeaderText(null);
                textImport.setContentText("Enter the text to import (use ; to separate lines)");

                Optional<String> optionalText = textImport.showAndWait();
                //the indexes added
                ArrayList<Integer> indexesAdded = new ArrayList<Integer>();
                //if its a valid grouping
                Boolean isValid = false;
                while (!isValid) {
                    try {
                        if (optionalText.isPresent()) {
                            //the board size
                            Double tempBoardSize = 0.0;
                            isValid = true;
                            String[] text = optionalText.get().split(";");
                            HashMap<ArrayList<Integer>, String> finalGroups = new HashMap<ArrayList<Integer>, String>();
                            //for each group in the text
                            for (String group : text) {
                                String[] groupSplit = group.split(" ");
                                //get the indexes and the target
                                String target = groupSplit[0];
                                ArrayList<Integer> indexes = new ArrayList<Integer>();
                                //for each index in the group
                                for (String index : groupSplit[1].split(",")) {
                                    //check if the index has already been added
                                    if (indexesAdded.contains(Integer.parseInt(index) - 1)) {
                                        isValid = false;
                                    }
                                    else {
                                        //add it to the board, and the list of added ones
                                        tempBoardSize++;
                                        indexes.add(Integer.parseInt(index) - 1);
                                        indexesAdded.add(Integer.parseInt(index) - 1);
                                    }
                                }
                                finalGroups.put(indexes, target);
                            }
                            //if the board size is a square number then set it, if not, isValid is false
                            if (Math.round(Math.sqrt(tempBoardSize)) == Math.sqrt(tempBoardSize)) {
                                this.boardSize = (int) Math.round(Math.sqrt(tempBoardSize));
                            } else {
                                isValid = false;
                            }
                            this.groups = finalGroups;
                            //check if all the indexes in the group are adjacent
                            for (ArrayList<Integer> group : this.groups.keySet()) {
                                //if the whole group is adjacent
                                Boolean groupAdjacent = true;
                                for (Integer i : group) {
                                    //if this node is adjacent
                                    Boolean nodeAdjacent = false;
                                    for (Integer j : group) {
                                        //if the node is adjacent to something set it to true
                                        if (Box.isAdjacent(i, j, this.boardSize)) {
                                            nodeAdjacent = true;
                                            break;
                                        }
                                    }
                                    //if there are any nodes that arent adjacent, the group isnt adjacent
                                    if (!nodeAdjacent) {
                                        groupAdjacent = false;
                                    }
                                }
                                //if there are any groups which arent adjacent its not valid
                                if (!groupAdjacent) {
                                    isValid = false;
                                }
                            }
                        }
                        //if cancel was clicked exit the program
                        else {
                            System.exit(0);
                        }
                    }
                    catch (Exception e) {
                        isValid = false;
                    }
                    if (!isValid) {
                        textImport.setHeaderText("that wasnt valid");
                        optionalText = textImport.showAndWait();
                    }
                }
            }
            //youre importing from file
            else {
                //get the file
                FileChooser fileChooser = new FileChooser();
                //only allow text files
                fileChooser.getExtensionFilters().addAll(new FileChooser.ExtensionFilter("Text Files", "*.txt"));
                File selectedFile = fileChooser.showOpenDialog(this.stage);;
                ArrayList<Integer> indexesAdded = new ArrayList<Integer>();
                Boolean isValid = false;
                while (!isValid) {
                    isValid = true;
                    //the board size
                    Double tempBoardSize = 0.0;
                    String text = "";
                    try {
                        //if the window was closed instead
                        if (selectedFile==null) {
                            System.exit(0);
                        }
                        FileReader reader = new FileReader(selectedFile);
                        BufferedReader bReader = new BufferedReader(reader);
                        String temp = bReader.readLine();
                        while (temp != null) {
                            text += temp + ";";
                            temp = bReader.readLine();
                        }
                        String[] textSplit = text.split(";");
                        HashMap<ArrayList<Integer>, String> finalGroups = new HashMap<ArrayList<Integer>, String>();
                        //for each group in the file
                        for (String group : textSplit) {
                            String[] groupSplit = group.split(" ");
                            //get the indexes and the target
                            String target = groupSplit[0];
                            ArrayList<Integer> indexes = new ArrayList<Integer>();
                            //for each index in the group
                            for (String index : groupSplit[1].split(",")) {
                                //check if the index has already been added
                                if (indexesAdded.contains(Integer.parseInt(index)-1)) {
                                    isValid = false;
                                }
                                else {
                                    //add it to the board, and the list of added ones
                                    tempBoardSize++;
                                    indexes.add(Integer.parseInt(index) - 1);
                                    indexesAdded.add(Integer.parseInt(index) - 1);
                                }
                            }
                            finalGroups.put(indexes, target);
                        }
                        //if the board size is a square number then set it, if not re-try
                        if (Math.round(Math.sqrt(tempBoardSize)) == Math.sqrt(tempBoardSize)) {
                            this.boardSize = (int) Math.round(Math.sqrt(tempBoardSize));
                        }
                        else {
                            isValid = false;
                        }
                        this.groups = finalGroups;
                        //check if all the indexes in the group are adjacent
                        for (ArrayList<Integer> group : this.groups.keySet()) {
                            ArrayList<Integer> boxesChecked = new ArrayList<Integer>();
                            //if the whole group is adjacent
                            Boolean groupAdjacent = true;
                            for (Integer i : group) {
                                //if this node is adjacent
                                Boolean nodeAdjacent = false;
                                if (boxesChecked.size()==0) {
                                    boxesChecked.add(i);
                                    nodeAdjacent = true;
                                }
                                else {
                                    for (Integer j : boxesChecked) {
                                        //if the node is adjacent to something set it to true
                                        if (Box.isAdjacent(i, j, this.boardSize)) {
                                            boxesChecked.add(i);
                                            nodeAdjacent = true;
                                            break;
                                        }
                                    }
                                }
                                //if there are any nodes that arent adjacent, the group isnt adjacent
                                if (!nodeAdjacent) {
                                    groupAdjacent = false;
                                }
                            }
                            //if there are any groups which arent adjacent its not valid
                            if (!groupAdjacent) {
                                isValid = false;
                            }
                        }
                    }
                    catch (Exception e) {
                        isValid = false;
                    }
                    if (!isValid) {
                        selectedFile = fileChooser.showOpenDialog(this.stage);
                    }
                }
            }
            //generate boxes
            this.board = new Box[this.boardSize*this.boardSize];
            for (int i = 0; i<this.boardSize*this.boardSize; i++) {
                this.board[i] = new Box(i);
            }
            //check which box in each group should be displaying the target
            generateTargetDisplays();
        }
        //if the choice was generate
        else if (result.get() == generateB) {
            TextInputDialog boardSizeAlert = new TextInputDialog("Enter here");
            boardSizeAlert.setTitle("Board size");
            boardSizeAlert.setHeaderText(null);
            boardSizeAlert.setContentText("How large do you want the board to be (going too high will not be fun for anyone involved)");

            Optional<String> size = boardSizeAlert.showAndWait();
            if (size.isPresent()){
                Boolean isInt = false;
                while (!isInt) {
                    try {
                        this.boardSize = Integer.parseInt(size.get());
                        isInt = true;
                    } catch (java.lang.NumberFormatException e) {
                        size = boardSizeAlert.showAndWait();
                    }
                }
                //generate boxes
                this.board = new Box[this.boardSize*this.boardSize];
                for (int i = 0; i<this.boardSize*this.boardSize; i++) {
                    this.board[i] = new Box(i);
                }
                //generate the answer and the groups
                answers = new Integer[this.boardSize*this.boardSize];
                generateAnswer();
                generateGroups();
                //check which box in each group should be displaying the target
                generateTargetDisplays();
            }
        }
        //if it was closed
        else {
            System.exit(0);
        }

        //set the style for the drawing
        this.gc.setLineWidth(4);
        this.gc.setStroke(Color.BLACK);

        this.game.setStyle("-fx-padding: 10;" +
                "-fx-border-width: 3;" +
                "-fx-border-insets: 10;" +
                "-fx-border-radius: 15;" +
                "-fx-border-color: orange;");

        //winning gif
        FileInputStream gifFile = null;
        try {
            gifFile = new FileInputStream("noice.gif");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        Image gif = new Image(gifFile);
        ImageView gifView = new ImageView(gif);

        //add the canvas to the game pane
        this.game.getChildren().addAll((this.canvas));
        //add the 2 sub-panes to the root pane
        this.root.getChildren().addAll(buttons1, this.game, fontPane);
        //add the winning screen canvas to its pane
        this.winPane.getChildren().addAll(gifView, winCanvas);

        //add mouse event handler to screen
        this.game.addEventHandler(MouseEvent.MOUSE_CLICKED, new MouseHandler());

        //add keypress event handler
        this.scene.setOnKeyPressed(new EventHandler<KeyEvent>()
        {
            public void handle(KeyEvent e)
            {
                //if the key wasnt a number it will throw an error when i try to convert it
                try {
                    //find the selected (if any) box
                    for (Box i : Main.this.board) {
                        if (i.getSelected()) {
                            //if the number size wasnt too big
                            if (Integer.parseInt((e.getText()))<=Main.this.boardSize) {
                                //add this action to the stack
                                Main.this.actions.push(new Integer[]{i.getBoardPos(), i.getValue()});
                                //clear the redo stack
                                undos.clear();
                                //change its value
                                i.setValue(Integer.parseInt(e.getText()));
                                //redraw the screen
                                Main.this.redraw();
                            }
                        }
                    }
                } catch(NumberFormatException e2){
                    //if the key was backspace
                    if (e.getCode().toString().equals("BACK_SPACE")) {
                        for (Box i : Main.this.board) {
                            if (i.getSelected()) {
                                //add this action to the stack
                                Main.this.actions.push(new Integer[]{i.getBoardPos(), i.getValue()});
                                //clear the redo stack
                                undos.clear();
                                //change the value to 0
                                i.setValue(0);
                            }
                        }
                        Main.this.redraw();
                    }
                }
            }
        });

        //draws the screen and sets listeners to redraw when the screen or font size is changed
        redraw();
        this.scene.heightProperty().addListener(observable -> redraw());
        this.scene.widthProperty().addListener(observable -> redraw());
        this.fontSize.valueProperty().addListener(observable -> redraw());

        this.stage.setScene(this.scene);
        this.stage.setTitle("mathdoku");
        this.stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }

    //handles the mouse click event
    class MouseHandler implements EventHandler<MouseEvent> {
        public void handle(MouseEvent e) {
            //selects a box depending on which is clicked
            for (Box box : Main.this.board) {
                //if the selected one was clicked increase the value by one
                if (box.getSelected() && box.isInBox(e.getX(), e.getY(), Main.this.scene, Main.this.boardSize)) {
                    if (e.getButton()==MouseButton.PRIMARY) {
                        //add this action to actions
                        Main.this.actions.push(new Integer[]{box.getBoardPos(), box.getValue()});
                        //clear the redo stack
                        Main.this.undos.clear();
                        box.increaseValue(Main.this.boardSize);
                    }
                    if (e.getButton()==MouseButton.SECONDARY) {
                        //add this action to actions
                        Main.this.actions.push(new Integer[]{box.getBoardPos(), box.getValue()});
                        //clear the redo stack
                        Main.this.undos.clear();
                        box.decreaseValue(Main.this.boardSize);
                    }
                }
                box.changeSelected(false);
                if (box.isInBox(e.getX(), e.getY(), Main.this.scene, Main.this.boardSize)) {
                    box.changeSelected(true);
                }

            }
            Main.this.redraw();
        }
    }

    //redraws the screen
    public void redraw() {
        //only display undo and redo buttons if the function if possible
        this.buttons1.getChildren().get(0).setVisible(true);
        this.buttons1.getChildren().get(1).setVisible(true);
        if (this.actions.isEmpty()) {
            this.buttons1.getChildren().get(0).setVisible(false);
        }
        if (this.undos.isEmpty()) {
            this.buttons1.getChildren().get(1).setVisible(false);
        }
        //clears the canvas
        this.gc.clearRect(0, 0, this.canvas.getWidth(), this.canvas.getHeight());
        //resets the canvas' dimensions depending on window size
        if (this.scene.getWidth()>200 || this.scene.getHeight()>200) {
            this.canvas.setWidth(this.scene.getWidth());
            this.canvas.setHeight(this.scene.getHeight());
        }
        //initialises it to the first one in case there are no selected boxes
        Box temp = this.board[0];
        //i iterate through the boxes via the groups so i can use information about the boxes group without searching seperately
        for (ArrayList<Integer> group : this.groups.keySet()) {
            for (Integer i : group) {
                this.board[i].rescale(this.boardSize, this.scene);
                //check if this box should be drawing a red fill
                Boolean redFill = false;
                if (this.showMistakes && ((checkGroupCorrect(group)==0) || getLinesWithDuplicates().contains(i))) {
                    redFill = true;
                }
                //draw the box to the screen
                this.board[i].draw(this.gc, this.scene, this.boardSize, this.groups, redFill, (String) this.fontSize.getValue());
                //store the box if its selected
                if (this.board[i].getSelected()) {
                    temp = this.board[i];
                }
            }
        }
        //draw the selected box last so it doesnt get overlapped
        temp.draw(this.gc, this.scene, this.boardSize, this.groups, false, (String) this.fontSize.getValue());
        //checks if the player has won
        Boolean won = true;
        if (getLinesWithDuplicates().size()!=0) {
            won = false;
        }
        for (ArrayList<Integer> group : this.groups.keySet()) {
            if (checkGroupCorrect(group)==0 || checkGroupCorrect(group)==2) {
                won = false;
            }
        }
        if (won) {
            this.root.setVisible(false);
            this.winPane.setVisible(true);
            //the style
            this.gc.setLineWidth(4);
            this.gc.setStroke(Color.BLACK);
            //setting the size of the image
            ((ImageView) this.winPane.getChildrenUnmodifiable().get(0)).setFitHeight(this.scene.getHeight());
            ((ImageView) this.winPane.getChildrenUnmodifiable().get(0)).setFitWidth(this.scene.getWidth());
            //playing a party horn noise
            String hornFile = "party horn.mp3";
            Media hornSound = new Media(new File(hornFile).toURI().toString());
            MediaPlayer mediaPlayer = new MediaPlayer(hornSound);
            mediaPlayer.play();
            //clears the canvas
            this.winGc.clearRect(0, 0, this.winCanvas.getWidth(), this.winCanvas.getHeight());
            //resets the canvas' dimensions depending on window size
            if (this.scene.getWidth()>200 || this.scene.getHeight()>200) {
                this.winCanvas.setWidth(this.scene.getWidth());
                this.winCanvas.setHeight(this.scene.getHeight());
            }
            for (Box box : this.board) {
                box.changeSelected(false);
                box.draw(this.winGc, this.scene, this.boardSize, this.groups, false, (String) this.fontSize.getValue());
            }
            //i redraw the first box because otherwise it does a smaller size line at the top right
            this.board[0].draw(this.winGc, this.scene, this.boardSize, this.groups, false, (String) this.fontSize.getValue());
        }
    }

    //check if there is anything in the same row or column with the same value
    public ArrayList<Integer> getLinesWithDuplicates() {
        //the indexes of boxes in lines with duplicate values
        ArrayList<Integer> indexes = new ArrayList<Integer>();
        //the values found so far in a line
        ArrayList<Integer> values = new ArrayList<Integer>();
        //go through all the columns
        //the top row of boxes
        for (int i=0; i<this.boardSize; i++) {
            //every box below each of them
            for (int j=0; j<this.boardSize; j++) {
                //if the value is already in the array
                if (values.contains(this.board[i+this.boardSize*j].getValue())) {
                    //add all boxes in this column to the array
                    for (int k=0; k<this.boardSize; k++) {
                        indexes.add(i+this.boardSize*k);
                    }
                    break;
                }
                //if the value in this box isnt 0 add it to the array
                if (this.board[i+j*this.boardSize].getValue()!=0) {
                    values.add(this.board[i+j*this.boardSize].getValue());
                }
            }
            values.clear();
        }
        //go through all the rows
        for (int i=0; i<this.boardSize; i++) {
            //every box to the right of each of them
            for (int j=0; j<this.boardSize; j++) {
                //if the value is already in the array
                if (values.contains(this.board[i*this.boardSize+j].getValue())) {
                    //add all boxes in this column to the array
                    for (int k=0; k<this.boardSize; k++) {
                        indexes.add(i*this.boardSize+k);
                    }
                    break;
                }
                //if the value in this box isnt 0 add it to the array
                if (this.board[i*this.boardSize+j].getValue()!=0) {
                    values.add(this.board[i*this.boardSize+j].getValue());
                }
            }
            values.clear();
        }
        return indexes;
    }

    //check if a groups boxes make the correct answer (for the show mistakes mode)
    public Integer checkGroupCorrect(ArrayList<Integer> groupToCheck) {
        //if the group is not all full in return true, as this method is only used for the red fill
        //and if it returns false then the draw method will add red
        Boolean groupFull = true;
        for (Integer i : groupToCheck) {
            if (this.board[i].getValue()==0) {
                groupFull = false;
            }
        }
        if (!groupFull) {
            return 2;
        }
        //if the group is only 1 large
        if (groupToCheck.size()==1) {
            //check the correct number is in it
            if (this.board[groupToCheck.get(0)].getValue()==this.answers[groupToCheck.get(0)]) {
                return 1;
            }
            else {
                return 0;
            }
        }
        //split the target into operation and answer
        String target = this.groups.get(groupToCheck);
        String operation = target.substring(target.length()-1);
        Integer groupAnswer = Integer.parseInt(target.substring(0, target.length()-1));
        //make an ArrayList of the answers in the group
        ArrayList<Integer> groupValues = new ArrayList<Integer>();
        for (Integer i : groupToCheck) {
            groupValues.add(this.board[i].getValue());
        }
        switch (operation) {
            case "+":
                Integer addition = 0;
                for (Integer value : groupValues) {
                    addition+=value;
                }
                if (addition == groupAnswer) {
                    return 1;
                }
            case "-":
                Integer subtraction = 0;
                subtraction += Collections.max(groupValues) * 2;
                for (Integer value : groupValues) {
                    subtraction -= value;
                }
                if (subtraction == groupAnswer) {
                    return 1;
                }
            case "x":
                Integer multiply = 1;
                for (Integer value : groupValues) {
                    multiply*=value;
                }
                //this has to be .equals because java will only return the chached instance
                // //of the Integer class when its between -128 and 127 and this could go over
                if (multiply.equals(groupAnswer)) {
                    return 1;
                }
            case "÷":
                //the highest answer in the group
                Double divide = Collections.max(groupValues)+0.0;
                //divide it by all the other numbers
                for (Integer value : groupValues) {
                    if (value+0.0!=Collections.max(groupValues)+0.0) {
                        divide /= value;
                    }
                }
                if ((int) Math.round(divide)==groupAnswer) {
                    return 1;
                }
        }
        return 0;
    }

    //generates the correct answer
    public void generateAnswer() {
        //a 2D array for the answers
        Integer[][] twoDanswers = new Integer[this.boardSize][this.boardSize];
        //add a known complete solution
        ArrayList<Integer> numbersToAdd = new ArrayList<Integer>();
        //add the top row in order
        for (int column=1; column<this.boardSize+1; column++) {
            numbersToAdd.add(column);
            twoDanswers[0][column-1] = column;
        }
        Integer temp;
        //add all other rows moving the first digit each time
        for (int row=1; row<this.boardSize; row++) {
            temp = numbersToAdd.get(0);
            numbersToAdd.remove(0);
            numbersToAdd.add(numbersToAdd.size(), temp);
            for (int i=0; i<numbersToAdd.size(); i++) {
                twoDanswers[row][i] = numbersToAdd.get(i);
            }
        }
        Random r = new Random();
        Integer[] tempArray;
        //with 1000 repititions
        for (int i=0; i<1000; i++) {
            //swap 2 random rows
            Integer firstRow = r.nextInt(this.boardSize);
            Integer secondRow = r.nextInt(this.boardSize);
            tempArray = twoDanswers[firstRow];
            twoDanswers[firstRow] = twoDanswers[secondRow];
            twoDanswers[secondRow] = tempArray;
            //transpose the array
            for (int row=0; row<this.boardSize; row++) {
                for (int column=row+1; column<this.boardSize; column++) {
                    temp = twoDanswers[row][column];
                    twoDanswers[row][column] = twoDanswers[column][row];
                    twoDanswers[column][row] = temp;
                }
            }
        }
        //add the answers from the 2d array to the member variable (1 dimensional)
        for (Integer i=0; i<this.boardSize; i++) {
            for (Integer j=0; j<this.boardSize; j++) {
                this.answers[this.boardSize*i+j] = twoDanswers[i][j];
            }
        }
    }

    //generates the groups for the boxes to be arranged in
    public void generateGroups() {
        //get all the boxes to be added to a group in a list
        ArrayList<Integer> boxes = new ArrayList<Integer>();
        for (int i=0; i<this.boardSize*this.boardSize; i++) {
            boxes.add(i);
        }
        Random r = new Random();
        Integer groupSize;
        ArrayList<Integer> groupToAdd = new ArrayList<Integer>();
        while (boxes.size()>0) {
            //get a random number no bigger than the board size and no bigger than the number of boxes left
            groupSize = r.nextInt(this.boardSize-1)+2;
            while (groupSize>boxes.size()) {
                groupSize = r.nextInt(this.boardSize);
            }
            //how many times the same number has been picked in a row
            Integer inARow = 0;
            for (int i=0; i<groupSize; i++) {
                //the random value chosen to be added to the group
                Integer nextToAdd = boxes.get(r.nextInt(boxes.size()));
                //check if the new value is adjacent to old ones (or the list is empty)
                Boolean adjacent = false;
                if (groupToAdd.size()==0) {
                    adjacent=true;
                }
                //the last value it tried to add (if it picks the same 4 times in a row the chances are it doesnt fit in a group
                Integer lastPick=nextToAdd;
                while (adjacent==false) {
                    for (Integer node : groupToAdd) {
                        if (this.board[node].isAdjacent(nextToAdd, this.boardSize)) {
                            adjacent=true;
                        }
                    }
                    lastPick=nextToAdd;
                    nextToAdd = boxes.get(r.nextInt(boxes.size()));
                    //just add the group to the list if the target been chosen 4 times in a row (chances are theres no other boxes that fit)
                    if (lastPick==nextToAdd && adjacent==false) {
                        inARow++;
                    }
                    if (inARow>3) {
                        //if the group size is 1, and the box in it is adjacent to the last one added, add it to the last group
                        //this is to prevent it doing as many single groups
                        if (groupToAdd.size()==1) {
                            for (ArrayList<Integer> group : this.groups.keySet()) {
                                if (group.size() == 1 && this.board[groupToAdd.get(0)].isAdjacent(group.get(0), this.boardSize)) {
                                    groupToAdd.add(group.get(0));
                                    this.groups.remove(group);
                                    break;
                                }
                            }
                        }
                        Collections.sort(groupToAdd);
                        this.groups.put((ArrayList<Integer>) groupToAdd.clone(), makeTarget((ArrayList<Integer>) groupToAdd.clone()));
                        groupToAdd.clear();
                        break;
                    }
                }
                groupToAdd.add(lastPick);
                boxes.remove(lastPick);
            }
            if (groupToAdd.size()!=0) {
                //if the group size is 1, and the box in it is adjacent to the last one added, add it to the last group
                //this is to prevent it doing as many single groups
                if (groupToAdd.size()==1) {
                    for (ArrayList<Integer> group : this.groups.keySet()) {
                        if (group.size() == 1 && this.board[groupToAdd.get(0)].isAdjacent(group.get(0), this.boardSize)) {
                            groupToAdd.add(group.get(0));
                            this.groups.remove(group);
                            break;
                        }
                    }
                }
                Collections.sort(groupToAdd);
                this.groups.put((ArrayList<Integer>) groupToAdd.clone(), makeTarget((ArrayList<Integer>) groupToAdd.clone()));
                groupToAdd.clear();
            }
        }
    }

    //generate a target for a given group
    public String makeTarget(ArrayList<Integer> group) {
        //if the group is only 1 large
        if (group.size()==1) {
            return this.answers[group.get(0)].toString();
        }
        //make an ArrayList of the answers in the group
        ArrayList<Integer> groupAnswers = new ArrayList<Integer>();
        for (Integer i : group) {
            groupAnswers.add(this.answers[i]);
        }
        String operation = "";
        //give a bias for division as most of the time an integer wont be possible
        //the highest answer in the group
        Double decimalAnswer = Collections.max(groupAnswers)+0.0;
        //divide it by all the other numbers
        for (Integer i : groupAnswers) {
            if (i+0.0!=decimalAnswer) {
                decimalAnswer /= i;
            }
        }
        if (decimalAnswer == (int) Math.round(decimalAnswer)) {
            return Math.round(decimalAnswer)+"÷";
        }
        //then a second bias to minus as that sometimes will be negative
        //for each number, minus add the others and return the answer if its positive
        //the first one has to be added though, i decided to add it twice first so it can be taken off once
        Integer answer = 0;
        answer += Collections.max(groupAnswers) * 2;
        for (Integer i : groupAnswers) {
            answer -= i;
        }
        if (answer > 0) {
            return answer+"-";
        }
        answer = 0;
        //pick a random multiply or add
        Random r = new Random();
        Integer operationID = r.nextInt(2);
        switch (operationID) {
            case 0:
                //add all the numbers in the group
                for (Integer i : groupAnswers) {
                    answer+=i;
                }
                return answer+"+";
            case 1:
                answer=1;
                //multiply the numbers together
                for (Integer i : groupAnswers) {
                    answer*=i;
                }
                return answer+"x";
        }
        return operation;
    }

    //work out which box in each group should be displaying the target
    public void generateTargetDisplays() {
        for (ArrayList<Integer> group :this.groups.keySet()) {
            this.board[group.get(0)].setDisplayingTarget(this.groups.get(group));
        }
    }
}
