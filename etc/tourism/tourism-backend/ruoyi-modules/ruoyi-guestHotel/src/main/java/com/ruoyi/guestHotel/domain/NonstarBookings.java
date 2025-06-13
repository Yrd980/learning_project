package com.ruoyi.guestHotel.domain;

import com.ruoyi.common.core.web.domain.BaseEntity;

import java.time.LocalDateTime;

public class NonstarBookings extends BaseEntity {
    /** 预订信息ID */
    private Long id;
    /** 星级酒店ID */
    private Long hotel_id;
    /** 星级酒店房间ID */
    private Long room_type_id;
    /** 游客ID */
    private Long guest_id;
    /** 联系电话 */
    private String contact_number ;
    /** 是否已录入 */
    private int recorded;
    /** 入住时间 */
    private LocalDateTime check_in_time;
    /** 离开时间 */
    private LocalDateTime check_out_time;
    /** 入住人姓名 */
    private String guest_name;

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

    public Long getGuest_id() {
        return guest_id;
    }

    public void setGuest_id(Long guest_id) {
        this.guest_id = guest_id;
    }

    public String getContact_number() {
        return contact_number;
    }

    public void setContact_number(String contact_number) {
        this.contact_number = contact_number;
    }

    public int getRecorded() {
        return recorded;
    }

    public void setRecorded(int recorded) {
        this.recorded = recorded;
    }

    public LocalDateTime getCheck_in_time() {
        return check_in_time;
    }

    public void setCheck_in_time(LocalDateTime check_in_time) {
        this.check_in_time = check_in_time;
    }

    public LocalDateTime getCheck_out_time() {
        return check_out_time;
    }

    public void setCheck_out_time(LocalDateTime check_out_time) {
        this.check_out_time = check_out_time;
    }

    public String getGuest_name() {
        return guest_name;
    }

    public void setGuest_name(String guest_name) {
        this.guest_name = guest_name;
    }
}
