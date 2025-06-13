package com.ruoyi.complaint.domain;

import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.core.annotation.Excel;
import com.ruoyi.common.core.web.domain.BaseEntity;

/**
 * 投诉信息对象 complaints
 * 
 * @author ningf
 * @date 2024-07-15
 */
public class Complaints extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 投诉id */
    private Long id;

    /** 内容 */
    @Excel(name = "内容")
    private String content;

    /** 投诉时间 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "投诉时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date submitTime;

    /** 状态 */
    @Excel(name = "状态")
    private String status;

    /** 投诉人id */
    @Excel(name = "投诉人id")
    private Long userId;

    public void setId(Long id) 
    {
        this.id = id;
    }

    public Long getId() 
    {
        return id;
    }
    public void setContent(String content) 
    {
        this.content = content;
    }

    public String getContent() 
    {
        return content;
    }
    public void setSubmitTime(Date submitTime) 
    {
        this.submitTime = submitTime;
    }

    public Date getSubmitTime() 
    {
        return submitTime;
    }
    public void setStatus(String status) 
    {
        this.status = status;
    }

    public String getStatus() 
    {
        return status;
    }
    public void setUserId(Long userId) 
    {
        this.userId = userId;
    }

    public Long getUserId() 
    {
        return userId;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("content", getContent())
            .append("submitTime", getSubmitTime())
            .append("status", getStatus())
            .append("userId", getUserId())
            .toString();
    }
}
