package com.ruoyi.guestHotel.mapper;

import com.ruoyi.guestHotel.domain.StarhotelRooms;
import org.apache.ibatis.annotations.Mapper;


import java.util.List;
@Mapper
public interface StarhotelRoomsMapper {
    /**
     * 查询星级酒店房间
     *
     * @param id 星级酒店ID
     * @return 星级酒店房间
     */
    public StarhotelRooms selectStarhotelRoomsById(Long id);

    /**
     * 查询星级酒店房间列表
     *
     * @param id 星级酒店ID
     * @return 指定星级酒店房间集合
     */
    public List<StarhotelRooms> selectStarhotelRoomsList(Long id);

}
