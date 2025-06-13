package com.ruoyi.guestHotel.service;

import com.ruoyi.guestHotel.domain.StarBookings;
import com.ruoyi.guestHotel.domain.StarhotelReviews;
import com.ruoyi.guestHotel.domain.StarhotelRooms;
import com.ruoyi.guestHotel.domain.SysUserInfo;

import java.util.List;

public interface IStarhotelRoomsService {
    /**
     * 查询星级酒店
     *
     * @param id 星级酒店ID
     * @return 星级酒店房间
     */
    public StarhotelRooms selectStarhotelRoomsById(Long id);

    /**
     * 查询星级酒店列表
     *
     * @param id 星级酒店ID
     * @return 指定星级酒店房间集合
     */
    public List<StarhotelRooms> selectStarhotelRoomsList(Long id);

    /**
     * 新增星级酒店预订信息
     *
     * @return 结果
     */
    public int insertStarhotelBookingMsg(StarBookings starBookings);
    /**
     * 查询星级酒店评论列表
     *
     * @param id 星级酒店ID
     * @return 指定星级酒店评论集合
     */
    public List<StarhotelReviews> selectStarhotelReviewsList(Long id);
    /**
     * 查询游客信息
     *
     * @param id 游客ID
     * @return 游客信息
     */
    public SysUserInfo selectUserInfoById(Long id);

}
