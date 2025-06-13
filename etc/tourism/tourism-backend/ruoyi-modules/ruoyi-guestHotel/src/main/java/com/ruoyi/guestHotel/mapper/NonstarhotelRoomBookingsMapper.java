package com.ruoyi.guestHotel.mapper;

import com.ruoyi.guestHotel.domain.NonstarBookings;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface NonstarhotelRoomBookingsMapper {
    /**
     * 新增星级酒店预订信息
     *
     * @return 结果
     */
    public int insertNonstarhotelBookingMsg(NonstarBookings nonstarBookings);
}
