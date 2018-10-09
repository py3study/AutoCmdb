#!/usr/bin/expect -f

set timeout 1
set port [lindex $argv 0]
set username [lindex $argv 1]
set password [lindex $argv 2]
set hostname [lindex $argv 3]

 
spawn ssh-copy-id -p $port $username@$hostname
expect {
"password:" { send "$password\r" }
}
expect "#"
send -- "\r"
expect eof
