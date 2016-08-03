# -*- coding:utf8 -*-

# author          :haiyang.song
# email           :meishild@gmail.com
# datetime        :16/7/21
# version         :1.0
# python_version  :2.7.7
# description     :
# ==============================================================================
import win32serviceutil
import win32service
import win32event

from ddns_dnspod import DDNSLoader
from log_config import logger


class DDNSServer(win32serviceutil.ServiceFramework):
    # 服务名
    _svc_name_ = "PythonDDNS"
    # 服务显示名称
    _svc_display_name_ = "Python Service DDNS."
    # 服务描述
    _svc_description_ = "Python service DDNS."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.isAlive = True
        self._ddns_Loader = DDNSLoader()

    def SvcStop(self):
        logger.info("[WIN SERVICE]stop service ddns....")
        # 先告诉SCM停止这个过程
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # 设置事件
        win32event.SetEvent(self.hWaitStop)
        self.isAlive = False
        self._ddns_Loader.stop()

    def SvcDoRun(self):
        logger.info("[WIN SERVICE]start service ddns....")
        self._ddns_Loader.start()
        while self.isAlive:
            # time.sleep(1)
            # 等待服务被停止
            win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(DDNSServer)
