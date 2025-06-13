package com.ruoyi.emergency.domain;

import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.core.annotation.Excel;
import com.ruoyi.common.core.web.domain.BaseEntity;

/**
 * 应急信息对象 emergencyinfo
 * 
 * @author ningf
 * @date 2024-07-12
 */
public class Emergencyinfo extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 应急信息id */
    private Long id;

    /** 优先级 */
    @Excel(name = "优先级")
    private Long priority;

    /** 截止日期 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "截止日期", width = 30, dateFormat = "yyyy-MM-dd")
    private Date validity;

    /** 文本内容 */
    @Excel(name = "文本内容")
    private String content;

    /** 状态 */
    @Excel(name = "状态")
    private Long status;

    public void setId(Long id) 
    {
        this.id = id;
    }

    public Long getId() 
    {
        return id;
    }
    public void setPriority(Long priority) 
    {
        this.priority = priority;
    }

    public Long getPriority() 
    {
        return priority;
    }
    public void setValidity(Date validity) 
    {
        this.validity = validity;
    }

    public Date getValidity() 
    {
        return validity;
    }
    public void setContent(String content) 
    {
        this.content = content;
    }

    public String getContent() 
    {
        return content;
    }
    public void setStatus(Long status) 
    {
        this.status = status;
    }

    public Long getStatus() 
    {
        return status;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("priority", getPriority())
            .append("validity", getValidity())
            .append("content", getContent())
            .append("status", getStatus())
            .toString();
    }
}
