package com.ruoyi.guestHotel.mapper;



import com.ruoyi.guestHotel.domain.Complaints;

import java.util.List;

/**
 * 投诉信息Mapper接口
 * 
 * @author ningf
 * @date 2024-07-15
 */
public interface ComplaintsMapper 
{
    /**
     * 查询投诉信息
     * 
     * @param id 投诉信息主键
     * @return 投诉信息
     */
    public List<Complaints> selectComplaintsById(Long id);

}
