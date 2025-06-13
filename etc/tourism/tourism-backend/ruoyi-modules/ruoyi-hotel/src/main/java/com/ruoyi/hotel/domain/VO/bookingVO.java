package com.ruoyi.hotel.domain.VO;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.ruoyi.common.core.annotation.Excel;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;

import java.util.Date;

/**
 * @description:
 * @author: Lenovo
 * @time: 2024/7/17 上午8:33
 */
public class bookingVO {

    /** 酒店id */
    @Excel(name = "酒店id")
    private String hotelName;

    /** 房型id */
    @Excel(name = "房型id")
    private String roomTypeName;

    /** 预约人id */
    @Excel(name = "预约人id")
    private Long guestId;

    /** 联系方式 */
    @Excel(name = "联系方式")
    private String contactNumber;

    /** 是否确认 */
    @Excel(name = "是否确认")
    private Integer recorded;

    /** 开房时间 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "开房时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date checkInTime;

    /** 退房时间 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "退房时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date checkOutTime;

    /** 住客姓名 */
    @Excel(name = "住客姓名")
    private String guestName;

    public String getGuestName() {
        return guestName;
    }

    public void setGuestName(String guestName) {
        this.guestName = guestName;
    }

    public Date getCheckOutTime() {
        return checkOutTime;
    }

    public void setCheckOutTime(Date checkOutTime) {
        this.checkOutTime = checkOutTime;
    }

    public Date getCheckInTime() {
        return checkInTime;
    }

    public void setCheckInTime(Date checkInTime) {
        this.checkInTime = checkInTime;
    }

    public Integer getRecorded() {
        return recorded;
    }

    public void setRecorded(Integer recorded) {
        this.recorded = recorded;
    }

    public String getContactNumber() {
        return contactNumber;
    }

    public void setContactNumber(String contactNumber) {
        this.contactNumber = contactNumber;
    }

    public Long getGuestId() {
        return guestId;
    }

    public void setGuestId(Long guestId) {
        this.guestId = guestId;
    }

    public String getRoomTypeName() {
        return roomTypeName;
    }

    public void setRoomTypeName(String roomTypeName) {
        this.roomTypeName = roomTypeName;
    }

    public String getHotelName() {
        return hotelName;
    }

    public void setHotelName(String hotelName) {
        this.hotelName = hotelName;
    }

    @Override
    public String toString() {
        return "bookingVO{" +
                "hotelName='" + hotelName + '\'' +
                ", roomTypeName='" + roomTypeName + '\'' +
                ", guestId=" + guestId +
                ", contactNumber='" + contactNumber + '\'' +
                ", recorded=" + recorded +
                ", checkInTime=" + checkInTime +
                ", checkOutTime=" + checkOutTime +
                ", guestName='" + guestName + '\'' +
                '}';
    }
}
