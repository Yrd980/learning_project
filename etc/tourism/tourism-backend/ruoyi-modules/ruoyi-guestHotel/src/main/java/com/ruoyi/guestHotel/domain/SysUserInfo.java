package com.ruoyi.guestHotel.domain;

import com.ruoyi.common.core.web.domain.BaseEntity;

public class SysUserInfo extends BaseEntity {
    /** 游客ID */
    private Long user_id;
    /** 游客名字 */
    private String user_name;
    /** 头像 */
    private String avatar;
    /** 密码 */
    private String password;

    public Long getUser_id() {
        return user_id;
    }

    public void setUser_id(Long user_id) {
        this.user_id = user_id;
    }

    public String getUser_name() {
        return user_name;
    }

    public void setUser_name(String user_name) {
        this.user_name = user_name;
    }

    public String getAvatar() {
        return avatar;
    }

    public void setAvatar(String avatar) {
        this.avatar = avatar;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}
