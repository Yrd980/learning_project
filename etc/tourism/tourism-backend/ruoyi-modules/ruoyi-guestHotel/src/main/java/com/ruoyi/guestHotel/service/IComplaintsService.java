package com.ruoyi.guestHotel.service;

import com.ruoyi.guestHotel.domain.Complaints;
import com.ruoyi.guestHotel.domain.StarhotelRooms;

import java.util.List;

public interface IComplaintsService {
    /**
     * 查询投诉信息
     *
     * @param id 投诉信息主键
     * @return 投诉信息
     */
    public List<Complaints> selectComplaintsById(Long id);
}
