import java.util.Arrays;

public class Shimon {

    static int D;
    static int M;
    static int C;


    public static void main(String[] args) throws Exception {
        ArmState current = new ArmState(1, 2, 3, 4);
        for (int i = 1;;i++) {
            System.out.println(current);
            ArmState transition = null;
            do {
                transition = shift(current);
            } while (verify(transition, i));
            current = transition;
            Thread.sleep(4000);
        }
    }

    static ArmState shift(ArmState a) {
        int ind = (int) (Math.random() * 4);
        int val = (int) (Math.random() * 2 * D - D);
        return a.modify(ind, val);
    }

    static boolean verify(ArmState a, int in) {
        var arms = a.arms;
        boolean flag = true;
        for (int i = 0; i < arms.length - 1; i++) {
            if (arms[i] >= arms[i + 1]) flag = false;
        }
        boolean flag2 = false;
        for (int w: arms) {
            if (w == (M * in + C)) flag2 = true;
        }
        return flag && flag2;
    }

    static class ArmState {
        int[] arms;
        ArmState(int... arms) {
            if (arms.length != 4) throw new RuntimeException();
            this.arms = arms;
        }
        ArmState modify(int index, int val) {
            if (index < 0 || index > 3) throw new RuntimeException();
            var s = Arrays.copyOf(arms, 4);
            s[index] = val;
            return new ArmState(s);
        }

        @Override
        public String toString() {
            return String.format("v1 - v4: %s", Arrays.toString(arms));
        }
    }
}
