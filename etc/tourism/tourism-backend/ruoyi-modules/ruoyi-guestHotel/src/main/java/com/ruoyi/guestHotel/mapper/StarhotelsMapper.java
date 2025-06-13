package com.ruoyi.guestHotel.mapper;

import java.util.List;
import com.ruoyi.guestHotel.domain.Starhotels;

/**
 * 星级酒店Mapper接口
 * 
 * @author ruoyi
 * @date 2024-07-06
 */
public interface StarhotelsMapper 
{
    /**
     * 查询星级酒店
     * 
     * @param id 星级酒店主键
     * @return 星级酒店
     */
    public Starhotels selectStarhotelsById(Long id);

    /**
     * 查询星级酒店列表
     * 
     * @param starhotels 星级酒店
     * @return 星级酒店集合
     */
    public List<Starhotels> selectStarhotelsList(Starhotels starhotels);

}
