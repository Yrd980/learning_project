package com.ruoyi.entertainment.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.core.annotation.Excel;
import com.ruoyi.common.core.web.domain.BaseEntity;

/**
 * 餐饮娱乐评价对象 reviews
 * 
 * @author ningf
 * @date 2024-07-15
 */
public class Reviews extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 评价id */
    private Long id;

    /** 餐饮娱乐id */
    @Excel(name = "餐饮娱乐id")
    private Long diningEntertainmentId;

    /** 内容 */
    @Excel(name = "内容")
    private String content;

    /** 评价人 */
    @Excel(name = "评价人")
    private Long guestName;

    /** 评分 */
    @Excel(name = "评分")
    private Long rating;

    public void setId(Long id) 
    {
        this.id = id;
    }

    public Long getId() 
    {
        return id;
    }
    public void setDiningEntertainmentId(Long diningEntertainmentId) 
    {
        this.diningEntertainmentId = diningEntertainmentId;
    }

    public Long getDiningEntertainmentId() 
    {
        return diningEntertainmentId;
    }
    public void setContent(String content) 
    {
        this.content = content;
    }

    public String getContent() 
    {
        return content;
    }
    public void setGuestName(Long guestName) 
    {
        this.guestName = guestName;
    }

    public Long getGuestName() 
    {
        return guestName;
    }
    public void setRating(Long rating) 
    {
        this.rating = rating;
    }

    public Long getRating() 
    {
        return rating;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("diningEntertainmentId", getDiningEntertainmentId())
            .append("content", getContent())
            .append("guestName", getGuestName())
            .append("rating", getRating())
            .toString();
    }
}
