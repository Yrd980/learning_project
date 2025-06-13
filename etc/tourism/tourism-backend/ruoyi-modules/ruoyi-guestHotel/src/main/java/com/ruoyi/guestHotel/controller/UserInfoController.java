package com.ruoyi.guestHotel.controller;

import com.ruoyi.common.core.domain.R;
import com.ruoyi.common.core.utils.StringUtils;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.security.utils.SecurityUtils;
import com.ruoyi.guestHotel.domain.LoginBody;
import com.ruoyi.guestHotel.domain.RegisterBody;
import com.ruoyi.guestHotel.domain.StarBookings;
import com.ruoyi.guestHotel.domain.SysUserInfo;
import com.ruoyi.guestHotel.service.IUserInfoService;
import com.ruoyi.system.api.domain.SysUser;
import com.ruoyi.system.api.model.LoginUser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;


@RestController
@RequestMapping("/guest")
public class UserInfoController {
    @Autowired
    private IUserInfoService userInfoService;
    /**
     * 新增星级酒店预订信息
     */
    @PostMapping ("/login")
    public SysUserInfo add(@RequestBody LoginBody form)
    {
        // 用户登录
        SysUserInfo userInfo = userInfoService.login(form.getUsername(), form.getPassword());
        return userInfo;
    }
    /**
     * 新增星级酒店预订信息
     */
    @PostMapping("/register")
    public R<?> register(@RequestBody RegisterBody registerBody)
    {
        // 用户注册
        userInfoService.register(registerBody.getUsername(), registerBody.getPassword());
        return R.ok();
    }
}
