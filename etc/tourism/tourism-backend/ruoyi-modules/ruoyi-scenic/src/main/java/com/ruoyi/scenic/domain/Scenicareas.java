package com.ruoyi.scenic.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.core.annotation.Excel;
import com.ruoyi.common.core.web.domain.BaseEntity;

/**
 * 景区信息对象 scenicareas
 * 
 * @author ningf
 * @date 2024-07-17
 */
public class Scenicareas extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 景区id */
    private Long id;

    /** 城市 */
    @Excel(name = "城市")
    private String city;

    /** 景区名称 */
    @Excel(name = "景区名称")
    private String name;

    /** 地址 */
    @Excel(name = "地址")
    private String address;

    /** 图片 */
    @Excel(name = "图片")
    private String picUrl;

    /** 评分 */
    @Excel(name = "评分")
    private Long score;

    /** 描述 */
    @Excel(name = "描述")
    private String description;

    public void setId(Long id) 
    {
        this.id = id;
    }

    public Long getId() 
    {
        return id;
    }
    public void setCity(String city) 
    {
        this.city = city;
    }

    public String getCity() 
    {
        return city;
    }
    public void setName(String name) 
    {
        this.name = name;
    }

    public String getName() 
    {
        return name;
    }
    public void setAddress(String address) 
    {
        this.address = address;
    }

    public String getAddress() 
    {
        return address;
    }
    public void setPicUrl(String picUrl) 
    {
        this.picUrl = picUrl;
    }

    public String getPicUrl() 
    {
        return picUrl;
    }
    public void setScore(Long score) 
    {
        this.score = score;
    }

    public Long getScore() 
    {
        return score;
    }
    public void setDescription(String description) 
    {
        this.description = description;
    }

    public String getDescription() 
    {
        return description;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("city", getCity())
            .append("name", getName())
            .append("address", getAddress())
            .append("picUrl", getPicUrl())
            .append("score", getScore())
            .append("description", getDescription())
            .toString();
    }
}
