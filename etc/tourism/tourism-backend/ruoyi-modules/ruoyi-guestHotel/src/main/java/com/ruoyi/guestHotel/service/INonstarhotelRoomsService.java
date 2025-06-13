package com.ruoyi.guestHotel.service;

import com.ruoyi.guestHotel.domain.*;

import java.util.List;

public interface INonstarhotelRoomsService {
    /**
     * 查询星级酒店
     *
     * @param id 星级酒店ID
     * @return 星级酒店房间
     */
    public NonstarhotelRooms selectNonstarhotelRoomsById(Long id);

    /**
     * 查询星级酒店列表
     *
     * @param id 星级酒店ID
     * @return 指定星级酒店房间集合
     */
    public List<NonstarhotelRooms> selectNonstarhotelRoomsList(Long id);

    /**
     * 新增星级酒店预订信息
     *
     * @return 结果
     */
    public int insertNonstarhotelBookingMsg(NonstarBookings nonstarBookings);
    /**
     * 查询星级酒店评论列表
     *
     * @param id 星级酒店ID
     * @return 指定星级酒店评论集合
     */
    public List<NonstarhotelReviews> selectNonstarhotelReviewsList(Long id);
    /**
     * 查询游客信息
     *
     * @param id 游客ID
     * @return 游客信息
     */
    public SysUserInfo selectUserInfoById(Long id);
}
