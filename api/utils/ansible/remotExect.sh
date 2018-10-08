#!/usr/bin/expect

set timeout 1
set port [lindex $argv 0]
set username [lindex $argv 1]
set password [lindex $argv 2]
set hostname [lindex $argv 3]
 
spawn ssh-copy-id -p $port $username@$hostname
expect {
#"yes/no"#是为了捕获首次登录，要手动输入yes/no的情况
#{send "yes\r";}
"password:"#为例捕获需要输入密码的行为
{send "$password\r";}
}
expect eof
