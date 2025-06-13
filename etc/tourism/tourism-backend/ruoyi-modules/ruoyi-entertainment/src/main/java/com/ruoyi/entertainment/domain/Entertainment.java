package com.ruoyi.entertainment.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.core.annotation.Excel;
import com.ruoyi.common.core.web.domain.BaseEntity;

/**
 * 娱乐信息对象 entertainment
 * 
 * @author ningf
 * @date 2024-07-09
 */
public class Entertainment extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 娱乐id */
    private Long id;

    /** 名称 */
    @Excel(name = "名称")
    private String name;

    /** 开店时间 */
    @Excel(name = "开店时间")
    private String openingTime;

    /** 地址 */
    @Excel(name = "地址")
    private String address;

    /** 打烊时间 */
    @Excel(name = "打烊时间")
    private String closingTime;

    /** 附图 */
    @Excel(name = "附图")
    private String picUrl;

    /** 评分 */
    @Excel(name = "评分")
    private Long score;

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
    public void setOpeningTime(String openingTime) 
    {
        this.openingTime = openingTime;
    }

    public String getOpeningTime() 
    {
        return openingTime;
    }
    public void setAddress(String address) 
    {
        this.address = address;
    }

    public String getAddress() 
    {
        return address;
    }
    public void setClosingTime(String closingTime) 
    {
        this.closingTime = closingTime;
    }

    public String getClosingTime() 
    {
        return closingTime;
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

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("name", getName())
            .append("openingTime", getOpeningTime())
            .append("address", getAddress())
            .append("closingTime", getClosingTime())
            .append("picUrl", getPicUrl())
            .append("score", getScore())
            .toString();
    }
}
