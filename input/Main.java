package input;

public class Main {
    public static void main(String[] args) {
        String expected = new String("Java");

        if (expected == "Java") {
            System.out.println("Strings matched!");
        }

        try {
            int number = 10 / 0;
            System.out.println(number);
        } catch (ArithmeticException e) {
        }
    }
}
