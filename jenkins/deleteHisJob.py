#!/usr/bin/env python
# -*- coding:utf-8 -*-


import datetime
import jenkins
import time
from jenkinsapi.jenkins import Jenkins


def deleteJobHis(url, username, password):
    server_jenkins = jenkins.Jenkins(url, username, password)
    server_Jenkins = Jenkins(url, username, password)

    # 获取所有job列表
    job_list = server_Jenkins.keys()

    # 获取任务名称及id
    for job_name in job_list:
    # for job_name in ["VehicleModelManagement/oldjob/CI_gvdm_dev"]:
        # print(job_name)
        job_info = server_jenkins.get_job_info(job_name, fetch_all_builds=True)['builds']
        # print(job_info)
        job_id_list = []
        for job in job_info:
            job_id_list.append(job['number'])

        save_days = (datetime.datetime.now() - datetime.timedelta(minutes=43200)).strftime("%Y-%m-%d %H:%M:%S")
        # print(save_days)
        save_days = time.strptime(save_days, "%Y-%m-%d %H:%M:%S")

        # 判断构建历史记录，大于5次的保留，其余删除
        if len(job_id_list) > 10:
            job_id_list = job_id_list[10:]
            job_id_list.reverse()

            for job_id in job_id_list:
                job_time = time.localtime(server_jenkins.get_build_info(job_name, job_id, depth=0)['timestamp'] / 1000)
                job_time_format = time.strftime("%Y-%m-%d", job_time)
                print(job_name, job_id, job_time_format)
                server_jenkins.delete_build(job_name, job_id)
         elif len(job_id_list) <= 5:
             # 判断构建历史记录，小于5次的判断job id的执行时间，超过保留天数的删除
             for job_id in job_id_list:
                 job_time = time.localtime(server_jenkins.get_build_info(job_name, job_id, depth=0)['timestamp'] / 1000)
                 job_time_format = time.strftime("%Y-%m-%d", job_time)
        
                if job_time < save_days:
                    print(job_name, job_id, job_time_format)
                    server_jenkins.delete_build(job_name, job_id)


deleteJobHis(
    url='',
    username='',
    password='',
)
