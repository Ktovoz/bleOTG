from ui import menu
from configobj import ConfigObj
from framework.configlog import LogSetup




if __name__ == '__main__':
    configFile = ConfigObj('config.ini', encoding='utf8')
    LogSetup(config=configFile['logger'])
    menu.main()