package com.ruoyi.system.domain.vo;

/**
 * @description:
 * @author: Lenovo
 * @time: 2024/7/17 下午4:28
 */
public class PasswordVo {
    String oldPassword;
    String newPassword;
    Long userId;

    public String getOldPassword() {
        return oldPassword;
    }

    public void setOldPassword(String oldPassword) {
        this.oldPassword = oldPassword;
    }

    public String getNewPassword() {
        return newPassword;
    }

    public void setNewPassword(String newPassword) {
        this.newPassword = newPassword;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    @Override
    public String toString() {
        return "PasswordVo{" +
                "oldPassword='" + oldPassword + '\'' +
                ", newPassword='" + newPassword + '\'' +
                ", userId=" + userId +
                '}';
    }
}
