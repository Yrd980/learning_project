package com.ruoyi.system.domain.vo;

/**
 * @description:
 * @author: Lenovo
 * @time: 2024/7/17 下午3:47
 */
public class userVo {
    String nickName;
    String phonenumber;
    String email;
    Long userId;

    public String getNickName() {
        return nickName;
    }

    public void setNickName(String nickName) {
        this.nickName = nickName;
    }

    public String getPhonenumber() {
        return phonenumber;
    }

    public void setPhonenumber(String phonenumber) {
        this.phonenumber = phonenumber;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    @Override
    public String toString() {
        return "userVo{" +
                "nickName='" + nickName + '\'' +
                ", phonenumber='" + phonenumber + '\'' +
                ", email='" + email + '\'' +
                ", userId=" + userId +
                '}';
    }
}
