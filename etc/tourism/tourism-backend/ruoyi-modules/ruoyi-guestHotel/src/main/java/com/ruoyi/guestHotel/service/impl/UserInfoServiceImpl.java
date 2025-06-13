package com.ruoyi.guestHotel.service.impl;

import com.ruoyi.common.core.constant.CacheConstants;
import com.ruoyi.common.core.constant.Constants;
import com.ruoyi.common.core.constant.SecurityConstants;
import com.ruoyi.common.core.constant.UserConstants;
import com.ruoyi.common.core.domain.R;
import com.ruoyi.common.core.enums.UserStatus;
import com.ruoyi.common.core.exception.ServiceException;
import com.ruoyi.common.core.text.Convert;
import com.ruoyi.common.core.utils.StringUtils;
import com.ruoyi.common.core.utils.ip.IpUtils;
import com.ruoyi.guestHotel.domain.SysUserInfo;
import com.ruoyi.guestHotel.mapper.SysUserInfoMapper;
import com.ruoyi.guestHotel.service.IUserInfoService;
import com.ruoyi.system.api.domain.SysUser;
import com.ruoyi.system.api.model.LoginUser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UserInfoServiceImpl implements IUserInfoService {
    @Autowired
    private SysUserInfoMapper sysUserInfoMapper;
    /**
     * 登录
     */
    public SysUserInfo login(String username, String password)
    {
        SysUserInfo sysUser = new SysUserInfo();
        sysUser.setUser_name(username);
        sysUser.setAvatar(sysUserInfoMapper.selectUserInfoByName(username).getAvatar());
        sysUser.setUser_id(sysUserInfoMapper.selectUserInfoByName(username).getUser_id());
        sysUser.setPassword(password);
        return sysUser;
    }
    /**
     * 注册
     */
    public void register(String username, String password)
    {
// 用户名或密码为空 错误
        if (StringUtils.isAnyBlank(username, password))
        {
            throw new ServiceException("用户/密码必须填写");
        }
        if (username.length() < UserConstants.USERNAME_MIN_LENGTH
                || username.length() > UserConstants.USERNAME_MAX_LENGTH)
        {
            throw new ServiceException("账户长度必须在2到20个字符之间");
        }
        if (password.length() < UserConstants.PASSWORD_MIN_LENGTH
                || password.length() > UserConstants.PASSWORD_MAX_LENGTH)
        {
            throw new ServiceException("密码长度必须在5到20个字符之间");
        }
        SysUserInfo sysUser = new SysUserInfo();
        sysUser.setUser_name(username);
        sysUser.setPassword(password);
        sysUserInfoMapper.insertUser(sysUser);
    }

    public int updateUser(SysUser user){
        return 0;
    }
}
