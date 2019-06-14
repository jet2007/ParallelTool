# ParallelTool

并行执行同一个shell脚本的工具

使用方法

```shell

    参数
        -s,--script    必选；单个任务的脚本，必选包含并行param参数；示例[sh /app/import-data.sh 'param']
        -n,--num       可选；并行同时执行的个数
        -v,--val       必选；取值范围,默认逗号隔开
        -p,--param     可选；并行参数，默认为param
        -j,--job       可选；单个作业的日志文件名，默认为UUID值
        -h,--help      帮助
    示例1:   python ParallelTool.py -s "sh ./single_task_demo.sh 'param'" -v '16,12,13,14,15'
                # 相当于执行[sh /app/import-data.sh   '12'等5个]
     示例2： python ParallelTool.py -s "sh ./single_task_demo.sh 'parameter'" -v '11,12,13,13,15' -p 'parameter' -n 3 -j 'single_task_demo_job'

```

- 示例1：
  - 执行sh /app/import-data.sh 'param' 脚本(分别用16,12,13,14,15代替param值，执行5个)；并发数为3；每个作业的日志在/tmp目录下
- 示例2：
  - 与示例类似
    - 指定参数名为parameter
    - 指定并发数为3
    - 指定生成日志的文件名为single_task_demo_job