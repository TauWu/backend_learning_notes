/** 
    * Test 测试程序
    * 
    * 编译：javac Test.java
    * 执行： java Test
**/

// 类的名要和文件名一致
public class Test{
    // main函数
    public static void main(String[] args){
        String[] str = new String[3];
        str[0] = "First String";
        str[1] = "Second String";
        str[2] = "Third String";
        // for循环语法1
        for (String s : str)
            System.out.println(s);
        // for循环语法2
        for (int i = 0; i < str.length; i++){
            // if语法
            if (i != 1) {
                System.out.println(str[i]);
            }
        }
    }
}