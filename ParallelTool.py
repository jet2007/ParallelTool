#!/usr/bin/env python
# -*- coding:utf-8 -*-

#######################################################################
# 功能描述： 并发程序
# 创建日期：201906
# 创 建 人：Caihm
# 处理说明：
# 修改历史：
#######################################################################

# 导入功能模块
import getopt
import sys,os
import copy_reg,types
import multiprocessing
import time,datetime
import logging
import uuid

console = logging.StreamHandler()
logging.getLogger().setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

reload(sys)
sys.setdefaultencoding('utf8')

re_succ = multiprocessing.Manager().list()
re_fail = multiprocessing.Manager().list()

LOG_MSG_LEV1_PREV = '##总作业##'
LOG_MSG_LEV2_PREV = '##单作业##'

DEFAULT_PARALLEL_NUM = 3
DEFAULT_PARALLEL_PARA = 'param'
DEFAULT_PARALLEL_VALUES_SPLIT = ','

#单个执行脚本任务的日志文件，相关默认值
PARALLEL_LOG_FILE_FORMAT = '{0}.{1}{2}'
    # 0：前缀名，如任务名;
    # 1: 并行值；
    # 2：后缀名如.log
    # 示例: dwd_pkg_order.20190501.log
# 并行执行的默认值
DEFAULT_PARALLEL_LOG_FILE_DIR = '/tmp/'      #  日志文件的目录
DEFAULT_PARALLEL_LOG_FILE_SUFFIX = '.log'    #  日志文件的后缀名

# 方法：使用copy_reg将MethodType注册为可序列化的方法
def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)


copy_reg.pickle(types.MethodType, _pickle_method)


class RunScriptParallel(object):
    """
    并发处理程序
    """
    def __init__(self, script, parallel_num=None, parallel_para=None, parallel_values=None , log_path=None):
        self.script = script
        self.parallel_num = int(parallel_num)
        self.parallel_para = parallel_para
        self.parallel_values = parallel_values
        self.log_path = log_path

    def run(self, paral_value_of_task):
        """
        执行单个任务
        :param paral_value_of_task，单个任务的取值
        :return:
        """
        cmd_log_path = self.log_path.format(paral_value_of_task)
        cmd = self.script.replace(self.parallel_para, paral_value_of_task) + ' > ' + cmd_log_path

        #nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.info(LOG_MSG_LEV2_PREV+"并行作业[" + paral_value_of_task + "]执行开始......")
        re = os.system(cmd)
        if (re == 0):
            logging.info(LOG_MSG_LEV2_PREV + "并行作业[" + paral_value_of_task + "]执行成功!!!")
            re_succ.append(paral_value_of_task)
        else:
            #nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logging.error(LOG_MSG_LEV2_PREV + "并行作业[" + paral_value_of_task + "]执行失败!!!")
            re_fail.append(paral_value_of_task)
            raise

    def parallel(self, sleep_dur=1):
        pool = multiprocessing.Pool(processes=self.parallel_num)
        result = []
        for i in self.parallel_values.split(DEFAULT_PARALLEL_VALUES_SPLIT):
            if len(re_fail) > 0:
                logging.info(LOG_MSG_LEV1_PREV + "并行作业执行成功的作业个数：" + str(len(re_succ)) + ",明细作业=[" + ','.join(sorted(re_succ)) + "]")
                logging.info(LOG_MSG_LEV1_PREV + "并行作业执行失败的作业个数：" + str(len(re_fail)) + ",明细作业=[" + ','.join(sorted(re_fail)) + "]")
                raise Exception()
            exec_res = pool.apply_async(self.run, (i,))
            result.append(i + "," + str(exec_res))
            time.sleep(sleep_dur)
        pool.close()
        pool.join()
        logging.info(LOG_MSG_LEV1_PREV + "并行作业执行成功的作业个数：" + str(len(re_succ)) + ",明细作业=[" + ','.join(sorted(re_succ)) + "]")
        logging.info(LOG_MSG_LEV1_PREV + "并行作业执行失败的作业个数：" + str(len(re_fail)) + ",明细作业=[" + ','.join(sorted(re_fail)) + "]")
        if len(re_fail) > 0:
            raise

def exitinfo():
    descinfo = """
    参数
        -s,--script    必选；单个任务的脚本，必选包含并行param参数；示例[sh /app/import-data.sh 'param']
        -n,--num       可选；并行同时执行的个数
        -v,--val       必选；取值范围,默认逗号隔开
        -p,--param     可选；并行参数，默认为param
        -j,--job       可选；单个作业的日志文件名，默认为UUID值
        -h,--help      帮助
     示例1:   python ParallelTool.py -s "sh ./single_task_demo.sh 'param'" -v '16,12,13,14,15'
                # 相当于执行[sh ./single_task_demo.sh '12'等5个]
     示例2： python ParallelTool.py -s "sh ./single_task_demo.sh 'parameter'" -v '11,12,13,14,15' -p 'parameter' -n 3 -j 'single_task_demo_job'
    """
    logging.warn(descinfo)
    sys.exit(1)


def main(argv):
    DWP_BIN_PARA1 = "hs:n:v:p:j:"
    DWP_BIN_PARA2 = ["help", "script=", "num=", "val=", "param=", "job="]
    try:
        opts, args = getopt.getopt(argv,DWP_BIN_PARA1,DWP_BIN_PARA2)
    except getopt.GetoptError:
        exitinfo()
    job_name = ''.join(str(uuid.uuid4()))
    parallel_dict = {}
    for i in range(len(opts)):
        (opt, arg) = opts[i]
        if opt in ("-n", "--num"):
            parallel_dict['parallel_num'] = arg
        elif opt in ("-p", "--param"):
            parallel_dict['parallel_para'] = arg
        elif opt in ("-v", "--val"):
            parallel_dict['parallel_values'] = arg
        elif opt in ("-s", "--script"):
            parallel_dict['script'] = arg
        elif opt in ("-j", "--job"):
            job_name = arg
        elif opt in ("-h", "--help"):
            exitinfo()

    if not parallel_dict.has_key('parallel_num'):
        parallel_dict['parallel_num'] = DEFAULT_PARALLEL_NUM
    if not parallel_dict.has_key('parallel_para'):
        parallel_dict['parallel_para'] = DEFAULT_PARALLEL_PARA
    if (not parallel_dict.has_key('script')) or (not parallel_dict.has_key('parallel_values')) :
        exitinfo()

    single_file_log_path = DEFAULT_PARALLEL_LOG_FILE_DIR + PARALLEL_LOG_FILE_FORMAT.format(job_name,'{0}',DEFAULT_PARALLEL_LOG_FILE_SUFFIX)
    parallel_dict['log_path'] = single_file_log_path
    
    msg = LOG_MSG_LEV1_PREV + "并行作业开始......" + ",并发数："+str(parallel_dict['parallel_num'])
    logging.info(msg)
    logging.info(LOG_MSG_LEV1_PREV + "生成单个作业的日志文件形如：" + single_file_log_path.format('xxxxxx'))
    run_parallel = RunScriptParallel(**parallel_dict)
    try:
        run_parallel.parallel()
        logging.info(LOG_MSG_LEV1_PREV + "并发作业完成!!!")
    except Exception, e:
        logging.error(LOG_MSG_LEV1_PREV + "并发作业失败!!!")
        raise

if __name__ == "__main__":
    main(sys.argv[1:])