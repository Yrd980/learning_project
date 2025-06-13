package com.ruoyi.guestHotel.service.impl;

import com.ruoyi.guestHotel.domain.*;
import com.ruoyi.guestHotel.mapper.*;
import com.ruoyi.guestHotel.service.INonstarhotelRoomsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class NonstarhotelRoomsServiceImpl implements INonstarhotelRoomsService {
    @Autowired
    private NonstarhotelRoomsMapper nonstarhotelRoomsMapper;
    @Autowired
    private NonstarhotelRoomBookingsMapper nonstarhotelRoomBookingsMapper;
    @Autowired
    private NonstarhotelReviewsMapper nonstarhotelReviewsMapper;
    @Autowired
    private SysUserInfoMapper sysUserInfoMapper;
    /**
     * 查询星级酒店
     *
     * @param id 星级酒店房间ID
     * @return 星级酒店房间
     */
    @Override
    public NonstarhotelRooms selectNonstarhotelRoomsById(Long id){
        return nonstarhotelRoomsMapper.selectNonstarhotelRoomsById(id);
    }

    /**
     * 查询星级酒店列表
     *
     * @param id 星级酒店ID
     * @return 指定星级酒店房间集合
     */
    @Override
    public List<NonstarhotelRooms> selectNonstarhotelRoomsList(Long id) {
        return nonstarhotelRoomsMapper.selectNonstarhotelRoomsList(id);
    }
    /**
     * 新增星级酒店预订信息
     *
     * @return 结果
     */
    @Override
    public int insertNonstarhotelBookingMsg(NonstarBookings nonstarBookings)
    {
        return nonstarhotelRoomBookingsMapper.insertNonstarhotelBookingMsg(nonstarBookings);
    }

    @Override
    public List<NonstarhotelReviews> selectNonstarhotelReviewsList(Long id) {
        return nonstarhotelReviewsMapper.selectNonstarhotelReviewsList(id);
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
