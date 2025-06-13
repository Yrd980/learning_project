package com.ruoyi.guestHotel.domain.VO;

import com.ruoyi.common.core.web.domain.BaseEntity;

import java.time.LocalDateTime;

public class StarhotelReviewsVO extends BaseEntity {
    /** 评论内容 */
    private String content;
    /** 游客name*/
    private String guest_name;
    /** 游客头像*/
    private String avatar;
    /** 评分 */
    private Long rating;
    /** 房间信息name */
    private String room_type_name;
    /** 评论发布日期 */
    private LocalDateTime review_date;

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getGuest_name() {
        return guest_name;
    }

    public void setGuest_name(String guest_name) {
        this.guest_name = guest_name;
    }

    public Long getRating() {
        return rating;
    }

    public void setRating(Long rating) {
        this.rating = rating;
    }

    public String getAvatar() {
        return avatar;
    }

    public void setAvatar(String avatar) {
        this.avatar = avatar;
    }

    public String getRoom_type_name() {
        return room_type_name;
    }

    public void setRoom_type_name(String room_type_name) {
        this.room_type_name = room_type_name;
    }

    public LocalDateTime getReview_date() {
        return review_date;
    }

    public void setReview_date(LocalDateTime review_date) {
        this.review_date = review_date;
    }
}
