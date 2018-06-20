import sys, json

def do_cregister(self, *args):
    ret = False
    if len(args) < 2:
        print('args len is less than 2!')
        return False
    userName = args[0]
    passWord = args[1]
    if not userName or not passWord:
        print('user name or password is null!')
        return False

    msgDict = {
        'directive': 'register',
        'user_name': userName,
        'pass_word': passWord
    }
    self.client.send(json.dumps(msgDict).encode())
    msgRect = self.client.recv(1024).decode()
    if not msgRect:
        ret = False
    else:
        retDict = json.loads(msgRect)
        if retDict['register_result'] == 'OK':
            ret = True
    print('%s %d: ' % (sys._getframe().f_code.co_name, sys._getframe().f_lineno), \
          msgRect, ret)

    return ret