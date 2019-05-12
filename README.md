# Automation
# web自动化测试工具WebAutomation测试用例使用说明

| 作者 | 个人邮箱 | 个人主页 |
| ------ | ------ | ------ |
| xjin | xjin@che300.com | [Github主页](https://github.com/holyrocklee) |
*************************************
# 项目介绍
WebAutomation是一个基于java语言开发的自动化测试工具。本页面是web自动化测试用例使用说明，app自动化测试用例使用说明见[APP自动化测试](https://github.com/holyrocklee)
*************************************
# 一.执行前提

-	安装java，安装完成后CMD下输入java -version检查环境变量是否添加。
![](https://github.com/holyrocklee/readmefile/blob/master/images/java.png)
-	本地安装的chrome（64位）或火狐版本与conf\webdriver中的driver匹配  
版本对应：https://blog.csdn.net/yaya_1q2w/article/details/80053316  
如不匹配可到下列网址进行下载  
http://chromedriver.storage.googleapis.com/index.html  
https://npm.taobao.org/mirrors/chromedriver/  
https://github.com/mozilla/geckodriver/releases
-	火狐浏览器执行需要到conf\properties\conf.properties中修改firefoxpath的值为本地Firefox的绝对路径

*************************************
# 二.用例文档说明：web_testcase.xlsx

- **case_name**：用例的名称，必填，同一条用例case_name需要合并
- **category**：非必填
- **action_name**：必填，描述该步骤名称
- **location_type**：寻找控件的方式，默认为xpath，并且尽量使用xpath相对路径以防版本改动后会提示找不到该控件。另外支持id，text。建议使用默认。  
&emsp;&emsp;如果对于一个xpath定位方法能匹配到两个控件，则使用xpath->2的方法，比如贷前-资产录入-人加车全要素下关于地址的定位方法，//li[@title='江苏']->2  
&emsp;&emsp;还有碰到一个操作页面下多个下拉框操作的，应该注意是否有div相互影响的问题，见“批量导入”操作。
- **function_name**：支持的操作有：  
1.　open：打开网址；  
2.　input：清除原有字符内容，然后输入新字符。新字符在data一栏输入。  
&emsp;&emsp;input方法还提供输入随机字符串的功能，在data一栏输入，格式为：random(1,2,3)  
&emsp;&emsp;其中1表示输入字符串的类型：n为数字，l为字母，m为数字与字母混合；2表示长度；3表示参数名称。如：random(m,6,name)。  
&emsp;&emsp;引用上述输入的随机字符串，可以输入startswith(test)、endswith(${a})、${a}、a等。在同一次运行中，后面的测试用例可以引用前面的参数，如${name}；如果再次输入random(m,7,name)，则前面的参数name会被后面的name覆盖。  
&emsp;&emsp;其中：startswith(test)表示以test字符串开头的元素；endswith(${a})表示以参数a结尾的元素；${a}表示参数；a表示字符串。只有以${}表示的才是参数。  
3.　click：模拟鼠标点击。  
4.　check：检查控件是否存在或者文字是否相等。  
5.　db：数据库的操作。  
&emsp;&emsp;先在conf\properties\conf.properties文件里修改相关配置信息，如mysql_ip=192.168.0.225，账号：mysql_user=sa 密码：mysql_password=sa@1234，该主体所在SQL表：mysql_db=gamma_rc  
&emsp;&emsp;在贷前监控选择主体的时候显示的都是主体的简称，而新建主体后简称不能在页面进行查看，需要用到数据库查询。方法为在tasks的location_value里面写SQL语句，data写存储的参数名称。如下图所示: 
![](https://github.com/holyrocklee/readmefile/blob/master/images/db.png)
6.　hover：鼠标移动到哪个控件上。  
7.　keyboard：模拟键盘回车键，同时在data一栏输入enter。  
8.　switchto：两种用法，一种是在data里面直接填url，这时会切换到指定的url，另外一种是直接切换到对应的标签页，在data栏输入文本类数字即可。注意第一次切换是从原来的页面切换到新打开的页面。  
9.　close：关闭当前展示的页面。  
&emsp;&emsp;注意：在贷前反欺诈里点击查看，会打开第二个页面，但这时自动化工具仍在原来的页面上操作（此时浏览器展示的是第二个页面）。因此若需校验第二个页面的内容，需要先切换swtichto到第二个页面进行校验。  为了避免页面多开，需关闭close第二个页面；尽管第二个页面已经关闭，但是自动化工具仍停留在第二个页面上，因此还需要切换switchto回第一个页面。
![](https://github.com/holyrocklee/readmefile/blob/master/images/switch.png)
10.　print：打印详情，主要用于打印所使用的xpath定位到的控件数组。  
11.　Debug：调试。  
12.　file:添加从本地上传文件的功能。  
&emsp;&emsp;用法为：data一栏输入文件本地路径。
![](https://github.com/holyrocklee/readmefile/blob/master/images/uploadfile.png)
13.　addparam：location_value可以是参数的值，data是参数的名称，用于设置公共参数；location_value也可以是控件的xpath定位，对应data是从该控件下获取到的文本。引用方法同上。  
![](https://github.com/holyrocklee/readmefile/blob/master/images/addparam.png)
&emsp;&emsp;第一个表格cases的function_name能调用第二个表格task sheet中的task，名称必须在task列表中存在（多个操作的集合）。

-	**location_value**：function_name为open时不填，其他为必填。寻找控件用到的值，xpath方式为xpath值，id方式为id值，text方式的值为"tagname:文字"。tagname为html标签，不到万不得已不要使用。  
&emsp;&emsp;location_value还提供了如//span[contains(text(),'${name}')]的xpath定位方式；多用于下图校验某角色名在新建用户时是否存在，以及点击该角色名前的复选框，将其选中。
![](https://github.com/holyrocklee/readmefile/blob/master/images/frame.png)
-	**data**：找到控件以后需要输入的内容或打开的网址。
-	**wait**：支持两种输入方式：
1.	输入数字123，表示做完本条操作后等待的秒数为123s；
2.	输入xpath，表示等待该控件显示出来；xpath同样支持参数调用。  
&emsp;&emsp;注意：有下拉框的控件响应速度比较慢；有的操作完成后页面会自动刷新，因此上述操作的等待时间最好设置为2秒及以上。开发在改代码时响应也会很慢，注意心态不要爆炸。
-	**author**：用例作者
-	**enabled**：为0不执行该步骤，其他均执行
-	**新增公共参数功能**：新增第三个表格，名为parameters。里面有两个表头keys和values，表示公共参数及其值，主要用来存放需要被引用的电话号码及身份证号码等。用法为：${phone}，在tasks表格的data一栏中输入。
-	**新增了给task传入参数的功能**：
第一步：写task的时候，需要传入参数的步骤在data字段写以！开头的参数名称。一个task内的参数名称不能相同，如!name。不需要传入参数的直接写固定值。用法如下：
![](https://github.com/holyrocklee/readmefile/blob/master/images/!name.png)
第二步：
![](https://github.com/holyrocklee/readmefile/blob/master/images/!name2.png)
&emsp;&emsp;case调用的时候在data下写出该task中所有需要传入的参数，传参格式为：key1=value1, ey2=value2，其中通过!key1进行调用，value1可以是固定值，可以是参数调用。  
-	新增每条用例执行失败自动重置为初始页面功能，若执行成功则在该用例执行完成后重置页面。

**************************************
# 三.执行结果

- 命令提示符CMD下，会显示脚本运行的每一步，因此用例出错后，可以到命令提示符环境下查看相应的出错提示，也可以到log文件夹下查看info.log等日志文件，还可以进入伽马构建记录页面http://118.190.91.189:5021/#/ 查看相应的提示。
**************************************
# 四.用例说明

- 保证每一个用例的独立性，如：新增机构是一个单独的测试用例，用来检验“新增”这一功能是否正确；查看机构也是一个单独的用例，但在查看之前必须先新增机构。每设计一个用例都要考虑到前后的因果关系,把测试用例思维导图的说明考虑进去。
- 遇到错误多查看log日志。
- 点击“搜索”、“提交”、“确认删除”、“确认上传”等提交表单操作，可能会加载的比较慢，建议设置2秒的等待时间，不然的话可能会出现表单还没提交成功，页面就刷新的情况，同时用例不会提示错误（比如删除操作）。
- 关于用到的数据库语句：  
**1.查询账户余额**：  
SELECT balance FROM inf_account_balance_history ORDER BY entry_time DESC LIMIT 1  
SELECT balance FROM inf_account_balance_history WHERE org_id=(SELECT org_id FROM inf_admin_organization WHERE org_name='${addinstitution}' )  
**2.查询资产编号**：  
SELECT assets_id FROM inf_preloan_assets_detail WHERE borrower_name='王二麻·买买提' ORDER BY update_time DESC LIMIT 1  
**3.查询主体简称**：  
SELECT short_name FROM gamma_rc.inf_financial_owner WHERE full_name='${fullname}'  
**4.删除机构相关的表格**  
#删除机构
DELETE FROM inf_admin_organization WHERE org_id IN ();  
#删除机构下面的主体关联关系表  
DELETE from inf_admin_organization_owner WHERE org_id IN ();  
#删除主体  
DELETE from inf_financial_owner WHERE OWNER_id IN();  
#删除这些机构下的用户  
DELETE FROM inf_admin_user WHERE org_id IN ();
