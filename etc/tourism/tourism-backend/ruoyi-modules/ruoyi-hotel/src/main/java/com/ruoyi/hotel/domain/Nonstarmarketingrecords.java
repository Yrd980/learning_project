package com.ruoyi.hotel.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.core.annotation.Excel;
import com.ruoyi.common.core.web.domain.BaseEntity;

/**
 * 非星级酒店营销记录对象 nonstarmarketingrecords
 * 
 * @author ningf
 * @date 2024-07-14
 */
public class Nonstarmarketingrecords extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 营销记录id */
    private Long id;

    /** 酒店id */
    @Excel(name = "酒店id")
    private Long hotelId;

    /** 房型id */
    @Excel(name = "房型id")
    private Long roomTypeId;

    /** 总销量 */
    @Excel(name = "总销量")
    private Long totalSales;

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
    public void setRoomTypeId(Long roomTypeId) 
    {
        this.roomTypeId = roomTypeId;
    }

    public Long getRoomTypeId() 
    {
        return roomTypeId;
    }
    public void setTotalSales(Long totalSales) 
    {
        this.totalSales = totalSales;
    }

    public Long getTotalSales() 
    {
        return totalSales;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("hotelId", getHotelId())
            .append("roomTypeId", getRoomTypeId())
            .append("totalSales", getTotalSales())
            .toString();
    }
}
