package com.ruoyi.hotel.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.core.annotation.Excel;
import com.ruoyi.common.core.web.domain.BaseEntity;

/**
 * 非星级酒店对象 nonstarhotels
 * 
 * @author ningf
 * @date 2024-07-14
 */
public class Nonstarhotels extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 非星级酒店id */
    private Long id;

    /** 酒店名称 */
    @Excel(name = "酒店名称")
    private String name;

    /** 最低价 */
    @Excel(name = "最低价")
    private Long minPrice;

    /** 总剩余量 */
    @Excel(name = "总剩余量")
    private Long totalQuantity;

    /** 地址 */
    @Excel(name = "地址")
    private String address;

    /** 图片 */
    @Excel(name = "图片")
    private String imageUrl;

    /** 所有人id */
    @Excel(name = "所有人id")
    private Long ownerId;

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
    public void setOwnerId(Long ownerId) 
    {
        this.ownerId = ownerId;
    }

    public Long getOwnerId() 
    {
        return ownerId;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("name", getName())
            .append("minPrice", getMinPrice())
            .append("totalQuantity", getTotalQuantity())
            .append("address", getAddress())
            .append("imageUrl", getImageUrl())
            .append("ownerId", getOwnerId())
            .toString();
    }
}
