package com.ruoyi.guestHotel.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.guestHotel.mapper.StarhotelsMapper;
import com.ruoyi.guestHotel.domain.Starhotels;
import com.ruoyi.guestHotel.service.IStarhotelsService;

/**
 * 星级酒店Service业务层处理
 * 
 * @author ruoyi
 * @date 2024-07-06
 */
@Service
public class StarhotelsServiceImpl implements IStarhotelsService 
{
    @Autowired
    private StarhotelsMapper starhotelsMapper;

    /**
     * 查询星级酒店
     * 
     * @param id 星级酒店主键
     * @return 星级酒店
     */
    @Override
    public Starhotels selectStarhotelsById(Long id)
    {
        return starhotelsMapper.selectStarhotelsById(id);
    }

    /**
     * 查询星级酒店列表
     * 
     * @param starhotels 星级酒店
     * @return 星级酒店
     */
    @Override
    public List<Starhotels> selectStarhotelsList(Starhotels starhotels)
    {
        return starhotelsMapper.selectStarhotelsList(starhotels);
    }

}
