import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

public class Main extends Application {

    @Override
    public void start(Stage primaryStage) {
        primaryStage.setTitle("Minkowski Distance Calculator");

        TextField point1Field = new TextField();
        point1Field.setPromptText("Point 1 (e.g., 1,2,3)");

        TextField point2Field = new TextField();
        point2Field.setPromptText("Point 2 (e.g., 4,5,6)");

        TextField pField = new TextField();
        pField.setPromptText("Value of p");

        Label resultLabel = new Label();

        Button calculateButton = new Button("Calculate");
        calculateButton.setOnAction(e -> {
            try {
                String[] point1Str = point1Field.getText().split(",");
                String[] point2Str = point2Field.getText().split(",");

                if (point1Str.length != point2Str.length) {
                    resultLabel.setText("Error: Points must have the same dimension.");
                    return;
                }

                double[] point1 = new double[point1Str.length];
                double[] point2 = new double[point2Str.length];
                double p = Double.parseDouble(pField.getText());

                for (int i = 0; i < point1Str.length; i++) {
                    point1[i] = Double.parseDouble(point1Str[i]);
                    point2[i] = Double.parseDouble(point2Str[i]);
                }

                double distance = calculateMinkowskiDistance(point1, point2, p);
                resultLabel.setText("Minkowski Distance: " + distance);
            } catch (Exception ex) {
                resultLabel.setText("Error: Invalid input.");
            }
        });

        VBox vbox = new VBox(10, point1Field, point2Field, pField, calculateButton, resultLabel);
        vbox.setPadding(new Insets(10));

        Scene scene = new Scene(vbox, 400, 200);
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    private double calculateMinkowskiDistance(double[] point1, double[] point2, double p) {
        double sum = 0.0;
        for (int i = 0; i < point1.length; i++) {
            sum += Math.pow(Math.abs(point1[i] - point2[i]), p);
        }
        return Math.pow(sum, 1 / p);
    }

    public static void main(String[] args) {
        launch(args);
    }
}
