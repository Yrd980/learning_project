package com.ruoyi.file.service;

import com.aliyun.oss.OSS;
import com.aliyun.oss.OSSClientBuilder;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.ruoyi.file.utils.FileUploadUtils;

/**
 * @description:
 * @author: Lenovo
 * @time: 2024/7/8 下午7:20
 */

@Primary
@Service
public class OssSysFileServiceImpl implements ISysFileService{
    /**
     * oss公钥
     */
    public String accessKey="";

    /**
     * oss私钥
     */
    public String secretKey="";

    /**
     * oss存储桶域名地址
     */
    public String endpoint="oss-cn-beijing.aliyuncs.com";

    /**
     * oss存储桶名称
     */
    public String bucketName="tourism-oss";

    /**
     * OSS文件上传接口
     *
     * @param file 上传的文件
     * @return 访问地址
     */
    @Override
    public String uploadFile(MultipartFile file) throws Exception {
        // 创建OSSClient实例。
        OSS ossClient = new OSSClientBuilder().build(endpoint, accessKey, secretKey);
        String filePath = FileUploadUtils.uploadFileByOss(ossClient, bucketName, file);
        return "https://"+bucketName+"."+endpoint+"/"+filePath;
    }
}
