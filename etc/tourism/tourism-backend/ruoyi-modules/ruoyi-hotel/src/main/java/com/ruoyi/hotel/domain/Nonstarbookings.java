package com.ruoyi.hotel.domain;

import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.core.annotation.Excel;
import com.ruoyi.common.core.web.domain.BaseEntity;

/**
 * 非星级酒店预定信息对象 nonstarbookings
 * 
 * @author ningf
 * @date 2024-07-14
 */
public class Nonstarbookings extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 预定信息id */
    private Long id;

    /** 酒店id */
    @Excel(name = "酒店id")
    private Long hotelId;

    /** 房型id */
    @Excel(name = "房型id")
    private Long roomTypeId;

    /** 预定人id */
    @Excel(name = "预定人id")
    private Long guestId;

    /** 联系方式 */
    @Excel(name = "联系方式")
    private String contactNumber;

    /** 是否确认 */
    @Excel(name = "是否确认")
    private Integer recorded;

    /** 入住时间 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "入住时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date checkInTime;

    /** 退房时间 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "退房时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date checkOutTime;

    /** 住客名称 */
    @Excel(name = "住客名称")
    private String guestName;

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
    public void setRoomTypeId(Long roomTypeId) 
    {
        this.roomTypeId = roomTypeId;
    }

    public Long getRoomTypeId() 
    {
        return roomTypeId;
    }
    public void setGuestId(Long guestId) 
    {
        this.guestId = guestId;
    }

    public Long getGuestId() 
    {
        return guestId;
    }
    public void setContactNumber(String contactNumber) 
    {
        this.contactNumber = contactNumber;
    }

    public String getContactNumber() 
    {
        return contactNumber;
    }
    public void setRecorded(Integer recorded) 
    {
        this.recorded = recorded;
    }

    public Integer getRecorded() 
    {
        return recorded;
    }
    public void setCheckInTime(Date checkInTime) 
    {
        this.checkInTime = checkInTime;
    }

    public Date getCheckInTime() 
    {
        return checkInTime;
    }
    public void setCheckOutTime(Date checkOutTime) 
    {
        this.checkOutTime = checkOutTime;
    }

    public Date getCheckOutTime() 
    {
        return checkOutTime;
    }
    public void setGuestName(String guestName) 
    {
        this.guestName = guestName;
    }

    public String getGuestName() 
    {
        return guestName;
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
            .append("roomTypeId", getRoomTypeId())
            .append("guestId", getGuestId())
            .append("contactNumber", getContactNumber())
            .append("recorded", getRecorded())
            .append("checkInTime", getCheckInTime())
            .append("checkOutTime", getCheckOutTime())
            .append("guestName", getGuestName())
            .append("ownerId", getOwnerId())
            .toString();
    }
}
