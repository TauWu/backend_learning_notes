/**
    * 测试打包
**/

package cc.tau.sys;

import static java.lang.Math.*;

public class FundamentalProgrammingStructres{
    
    // 'main' function, the entrance of this java programe.
    public static void main(String[] args) {
        // Double类型、常量的展示
        String string = "This is a test %f, One. \n";
		System.out.printf(string, DOUBLE_TMP);
        System.out.println("This is a test "+ DOUBLE_TMP + ", Two.");

        // Math计算
        // This is a difference between the println and sqrt method. The println method operaters
        // on an Object System.out, and the sqrt method in Math class doesn't belong any objects.
        // This sqrt method is called static method, can find simmilar definiation in Python's class.
        System.out.println("This sqrt of " + DOUBLE_TMP + " is " + getSqrt(DOUBLE_TMP) + '\n');
        System.out.println("The square of root of \u03C0 is " + sqrt(PI));

        // Strings操作
        // 文字截取切片
        // JAVA中string一旦创建便不能局部更改
        String str1 = string.substring(0,8);
        String str2 = string.substring(0,8);
        String str3 = str1 + str2;

        System.out.printf("%s\n%s\n%s\n", str1, str2, str3);
    }

    private static double getSqrt(double origin){
        double y = Math.sqrt(origin);
        return y;
    }

    // NOTE: "const" is a reserved Java key word, however it is not used anywhere. 
    // Constant in Java use "final" instead.
    public static final double DOUBLE_TMP = 3.3328;
    
}