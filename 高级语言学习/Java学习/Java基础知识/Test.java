/** 
    * Test 测试程序
    * 
    * javac Test.java
    * java Test
**/

public class Test
{
    public static void main(String[] args)
    {
        String[] str = new String[3];
        str[0] = "First String";
        str[1] = "Second String";
        str[2] = "Third String";
        for (String g : str)
            System.out.println(g);
    }
}