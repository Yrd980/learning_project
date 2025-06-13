package com.ruoyi.guestHotel.domain;

import com.ruoyi.common.core.web.domain.BaseEntity;

import java.time.LocalDateTime;

public class StarhotelReviews extends BaseEntity {
    /** 评论信息ID */
    private Long id;
    /** 酒店信息ID */
    private Long hotel_id;

    /** 评论内容 */
    private String content;
    /** 游客ID */
    private Long guest_id;
    /** 评分 */
    private Long rating;
    /** 房间信息ID */
    private Long room_type_id;
    /** 评论发布日期 */
    private LocalDateTime review_date;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Long getHotel_id() {
        return hotel_id;
    }

    public void setHotel_id(Long hotel_id) {
        this.hotel_id = hotel_id;
    }

    public Long getRoom_type_id() {
        return room_type_id;
    }

    public void setRoom_type_id(Long room_type_id) {
        this.room_type_id = room_type_id;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public Long getGuest_id() {
        return guest_id;
    }

    public void setGuest_id(Long guest_id) {
        this.guest_id = guest_id;
    }

    public Long getRating() {
        return rating;
    }

    public void setRating(Long rating) {
        this.rating = rating;
    }

    public LocalDateTime getReview_date() {
        return review_date;
    }

    public void setReview_date(LocalDateTime review_date) {
        this.review_date = review_date;
    }
}
