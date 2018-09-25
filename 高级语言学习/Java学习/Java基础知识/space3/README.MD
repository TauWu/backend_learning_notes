# SPACE2
## SPACE2命令行执行

```sh
# spacepath
cd {spacepath}/space2

# 编译打包
javac -d class @srclist
jar -cvf ./sys.jar ./class

# 执行
java -classpath class cc.tau.sys.Applet
```