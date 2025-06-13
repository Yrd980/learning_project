package com.ruoyi.guestHotel.mapper;

import com.ruoyi.guestHotel.domain.Starhotels;
import com.ruoyi.guestHotel.domain.SysUserInfo;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface SysUserInfoMapper {
    /**
     * 查询游客信息
     *
     * @param id 游客ID
     * @return 游客信息
     */
    public SysUserInfo selectUserInfoById(Long id);
    /**
     * 查询游客信息
     *
     * @param name 游客name
     * @return 游客信息
     */
    public SysUserInfo selectUserInfoByName(String name);
    /**
     * 查询游客信息
     *
     * @return 游客信息
     */
    public void insertUser(SysUserInfo sysUserInfo);

}
