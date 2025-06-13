package com.ruoyi.entertainment.domain;

import java.math.BigDecimal;
import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.core.annotation.Excel;
import com.ruoyi.common.core.web.domain.BaseEntity;

/**
 * 演出团体信息对象 performancegroups
 * 
 * @author ningf
 * @date 2024-07-06
 */
public class Performancegroups extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 演出团体id */
    private Long id;

    /** 团体名称 */
    @Excel(name = "团体名称")
    private String name;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss", timezone = "GMT+8") // 指定时区，这里假设是 GMT+8
    @Excel(name = "开始时间", width = 30, dateFormat = "yyyy-MM-dd HH:mm:ss")
    private Date startTime;

    /** 演出单场时长 */
    @Excel(name = "演出单场时长")
    private Long duration;

    /** 演出场地 */
    @Excel(name = "演出场地")
    private String venue;

    /** 容量 */
    @Excel(name = "容量")
    private Long capacity;

    /** 票价 */
    @Excel(name = "票价")
    private BigDecimal price;

    /** 图片 */
    @Excel(name = "图片")
    private String picUrl;

    public void setId(Long id) 
    {
        this.id = id;
    }

    public Long getId() 
    {
        return id;
    }
    public void setName(String name) 
    {
        this.name = name;
    }

    public String getName() 
    {
        return name;
    }
    public void setStartTime(Date startTime) 
    {
        this.startTime = startTime;
    }

    public Date getStartTime() 
    {
        return startTime;
    }
    public void setDuration(Long duration) 
    {
        this.duration = duration;
    }

    public Long getDuration() 
    {
        return duration;
    }
    public void setVenue(String venue) 
    {
        this.venue = venue;
    }

    public String getVenue() 
    {
        return venue;
    }
    public void setCapacity(Long capacity) 
    {
        this.capacity = capacity;
    }

    public Long getCapacity() 
    {
        return capacity;
    }
    public void setPrice(BigDecimal price) 
    {
        this.price = price;
    }

    public BigDecimal getPrice() 
    {
        return price;
    }
    public void setPicUrl(String picUrl)
    {
        this.picUrl = picUrl;
    }

    public String getPicUrl()
    {
        return picUrl;
    }
    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("name", getName())
            .append("startTime", getStartTime())
            .append("duration", getDuration())
            .append("venue", getVenue())
            .append("capacity", getCapacity())
            .append("price", getPrice())
            .append("picUrl", getPicUrl())
            .toString();
    }
}
