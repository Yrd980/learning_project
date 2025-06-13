package com.ruoyi.guestHotel.service;

import com.ruoyi.guestHotel.domain.SysUserInfo;
import com.ruoyi.system.api.domain.SysUser;

public interface IUserInfoService {
    public SysUserInfo login(String username, String password);
    public void register(String username, String password);
    public int updateUser(SysUser user);
}
