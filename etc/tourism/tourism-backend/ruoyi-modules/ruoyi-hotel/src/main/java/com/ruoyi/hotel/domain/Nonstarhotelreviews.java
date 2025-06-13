package com.ruoyi.hotel.domain;

import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.core.annotation.Excel;
import com.ruoyi.common.core.web.domain.BaseEntity;

/**
 * 非星级酒店评价对象 nonstarhotelreviews
 * 
 * @author ningf
 * @date 2024-07-15
 */
public class Nonstarhotelreviews extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 评价id */
    private Long id;

    /** 酒店id */
    @Excel(name = "酒店id")
    private Long hotelId;

    /** 内容 */
    @Excel(name = "内容")
    private String content;

    /** 评价人id */
    @Excel(name = "评价人id")
    private Long guestId;

    /** 评分 */
    @Excel(name = "评分")
    private Long rating;

    /** 房型id */
    @Excel(name = "房型id")
    private Long roomTypeId;

    /** 评价时间 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "评价时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date reviewDate;

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
    public void setContent(String content) 
    {
        this.content = content;
    }

    public String getContent() 
    {
        return content;
    }
    public void setGuestId(Long guestId) 
    {
        this.guestId = guestId;
    }

    public Long getGuestId() 
    {
        return guestId;
    }
    public void setRating(Long rating) 
    {
        this.rating = rating;
    }

    public Long getRating() 
    {
        return rating;
    }
    public void setRoomTypeId(Long roomTypeId) 
    {
        this.roomTypeId = roomTypeId;
    }

    public Long getRoomTypeId() 
    {
        return roomTypeId;
    }
    public void setReviewDate(Date reviewDate) 
    {
        this.reviewDate = reviewDate;
    }

    public Date getReviewDate() 
    {
        return reviewDate;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("id", getId())
            .append("hotelId", getHotelId())
            .append("content", getContent())
            .append("guestId", getGuestId())
            .append("rating", getRating())
            .append("roomTypeId", getRoomTypeId())
            .append("reviewDate", getReviewDate())
            .toString();
    }
}
