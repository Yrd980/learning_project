package com.ruoyi.guestHotel.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.core.annotation.Excel;
import com.ruoyi.common.core.web.domain.BaseEntity;

/**
 * 星级酒店对象 starhotels
 * 
 * @author ruoyi
 * @date 2024-07-06
 */
public class Starhotels extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 星级酒店ID */
    private Long id;

    /** 星级酒店名 */
    @Excel(name = "星级酒店名")
    private String name;

    /** 星级 */
    @Excel(name = "星级")
    private Long starLevel;

    /** 最低价 */
    @Excel(name = "最低价")
    private Long minPrice;

    /** 总余量 */
    @Excel(name = "总余量")
    private Long totalQuantity;

    /** 地址 */
    @Excel(name = "地址")
    private String address;

    /** 图片 */
    @Excel(name = "图片")
    private String imageUrl;

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
    public void setStarLevel(Long starLevel) 
    {
        this.starLevel = starLevel;
    }

    public Long getStarLevel() 
    {
        return starLevel;
    }
    public void setMinPrice(Long minPrice) 
    {
        this.minPrice = minPrice;
    }

    public Long getMinPrice() 
    {
        return minPrice;
    }
    public void setTotalQuantity(Long totalQuantity) 
    {
        this.totalQuantity = totalQuantity;
    }

    public Long getTotalQuantity() 
    {
        return totalQuantity;
    }
    public void setAddress(String address) 
    {
        this.address = address;
    }

    public String getAddress() 
    {
        return address;
    }
    public void setImageUrl(String imageUrl) 
    {
        this.imageUrl = imageUrl;
    }

    public String getImageUrl() 
    {
        return imageUrl;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("name", getName())
            .append("starLevel", getStarLevel())
            .append("minPrice", getMinPrice())
            .append("totalQuantity", getTotalQuantity())
            .append("address", getAddress())
            .append("imageUrl", getImageUrl())
            .toString();
    }
}
