package com.ruoyi.hotel.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.core.annotation.Excel;
import com.ruoyi.common.core.web.domain.BaseEntity;

/**
 * 非星级酒店房型对象 nonstarroomtypes
 * 
 * @author ningf
 * @date 2024-07-14
 */
public class Nonstarroomtypes extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 房型id */
    private Long id;

    /** 酒店id */
    @Excel(name = "酒店id")
    private Long hotelId;

    /** 房型名称 */
    @Excel(name = "房型名称")
    private String name;

    /** 价格 */
    @Excel(name = "价格")
    private Long price;

    /** 剩余量 */
    @Excel(name = "剩余量")
    private Long quantity;

    /** 销量 */
    @Excel(name = "销量")
    private Long sales;

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
    public void setHotelId(Long hotelId) 
    {
        this.hotelId = hotelId;
    }

    public Long getHotelId() 
    {
        return hotelId;
    }
    public void setName(String name) 
    {
        this.name = name;
    }

    public String getName() 
    {
        return name;
    }
    public void setPrice(Long price) 
    {
        this.price = price;
    }

    public Long getPrice() 
    {
        return price;
    }
    public void setQuantity(Long quantity) 
    {
        this.quantity = quantity;
    }

    public Long getQuantity() 
    {
        return quantity;
    }
    public void setSales(Long sales) 
    {
        this.sales = sales;
    }

    public Long getSales() 
    {
        return sales;
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
            .append("hotelId", getHotelId())
            .append("name", getName())
            .append("price", getPrice())
            .append("quantity", getQuantity())
            .append("sales", getSales())
            .append("imageUrl", getImageUrl())
            .append("ownerId", getOwnerId())
            .toString();
    }
}
