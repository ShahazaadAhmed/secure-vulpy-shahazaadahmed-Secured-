import sys
sys.path.insert(0,'good')
import libuser
print("admin correct creds ->", libuser.login("admin", "galgate1234"))
print("SQLi payload attempt ->", libuser.login("' OR '1'='1", "whatever"))
# "D:/p&ps/Secure_web/CA-2/app/project/bad/db_users.sqlite"