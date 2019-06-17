# ParallelTool

并行执行同一个shell脚本的工具

使用方法

```shell
    参数
        -s,--script    必选；单个任务的脚本，必选包含并行param参数；示例[sh /app/import-data.sh 'param']
        -n,--num       可选；并行同时执行的个数
        -v,--val       必选；取值范围,默认逗号隔开
        -p,--param     可选；并行参数，默认为param
        -j,--job       可选；默认为空，即不生成单个作业的中间日志文件；若填写时，单个作业的日志文件名部分; 
        -d,--dir       可选；默认为/tmp/，与job参数共同组成单个作业的日志文件名
        -h,--help      帮助
     示例1:   python ParallelTool.py -s "sh ./single_task_demo.sh 'param'" -v '16,12,13,14,15'
                # 功能：相当于执行[sh ./single_task_demo.sh '16'],[sh ./single_task_demo.sh '12']等5个
                #    1. 并发数=3； 2. 单个作业无中间日志； 
     示例2： python ParallelTool.py -s "sh ./single_task_demo.sh 'parameter'" -v '11,12,13,14,15' -p 'parameter' -n 2 -j 'single_task_demo_job'
                # 功能：相当于执行[sh ./single_task_demo.sh '11'],[sh ./single_task_demo.sh '12']等5个
                #    1. 并发数=3； 2. 单个作业有中间日志=/tmp/single_task_demo_job.xxxxx.log； 
```