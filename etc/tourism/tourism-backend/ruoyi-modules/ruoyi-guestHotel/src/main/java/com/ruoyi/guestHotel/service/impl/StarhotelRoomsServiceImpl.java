package com.ruoyi.guestHotel.service.impl;

import com.ruoyi.guestHotel.domain.*;
import com.ruoyi.guestHotel.mapper.StarhotelReviewsMapper;
import com.ruoyi.guestHotel.mapper.StarhotelRoomBookingsMapper;
import com.ruoyi.guestHotel.mapper.StarhotelRoomsMapper;
import com.ruoyi.guestHotel.mapper.SysUserInfoMapper;
import com.ruoyi.guestHotel.service.IStarhotelRoomsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
@Service
public class StarhotelRoomsServiceImpl implements IStarhotelRoomsService {
    @Autowired
    private StarhotelRoomsMapper starhotelRoomsMapper;
    @Autowired
    private StarhotelRoomBookingsMapper starhotelRoomBookingsMapper;
    @Autowired
    private StarhotelReviewsMapper starhotelReviewsMapper;
    @Autowired
    private SysUserInfoMapper sysUserInfoMapper;
    /**
     * 查询星级酒店
     *
     * @param id 星级酒店房间ID
     * @return 星级酒店房间
     */
    @Override
    public StarhotelRooms selectStarhotelRoomsById(Long id){
        return starhotelRoomsMapper.selectStarhotelRoomsById(id);
    }

    /**
     * 查询星级酒店列表
     *
     * @param id 星级酒店ID
     * @return 指定星级酒店房间集合
     */
    @Override
    public List<StarhotelRooms> selectStarhotelRoomsList(Long id) {
        return starhotelRoomsMapper.selectStarhotelRoomsList(id);
    }
    /**
     * 新增星级酒店预订信息
     *
     * @return 结果
     */
    @Override
    public int insertStarhotelBookingMsg(StarBookings starBookings)
    {
        return starhotelRoomBookingsMapper.insertStarhotelBookingMsg(starBookings);
    }

    @Override
    public List<StarhotelReviews> selectStarhotelReviewsList(Long id) {
        return starhotelReviewsMapper.selectStarhotelReviewsList(id);
    }
    /**
     * 查询游客信息
     *
     * @param id 游客ID
     * @return 游客信息
     */
    public SysUserInfo selectUserInfoById(Long id){
        return sysUserInfoMapper.selectUserInfoById(id);
    }
}
