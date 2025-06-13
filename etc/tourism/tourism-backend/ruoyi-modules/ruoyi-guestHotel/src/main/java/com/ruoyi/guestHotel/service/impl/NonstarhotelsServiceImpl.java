package com.ruoyi.guestHotel.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.guestHotel.mapper.NonstarhotelsMapper;
import com.ruoyi.guestHotel.domain.Nonstarhotels;
import com.ruoyi.guestHotel.service.INonstarhotelsService;

/**
 * 非星级酒店Service业务层处理
 * 
 * @author ruoyi
 * @date 2024-07-11
 */
@Service
public class NonstarhotelsServiceImpl implements INonstarhotelsService 
{
    @Autowired
    private NonstarhotelsMapper nonstarhotelsMapper;

    /**
     * 查询非星级酒店
     * 
     * @param id 非星级酒店主键
     * @return 非星级酒店
     */
    @Override
    public Nonstarhotels selectNonstarhotelsById(Long id)
    {
        return nonstarhotelsMapper.selectNonstarhotelsById(id);
    }

    /**
     * 查询非星级酒店列表
     * 
     * @param nonstarhotels 非星级酒店
     * @return 非星级酒店
     */
    @Override
    public List<Nonstarhotels> selectNonstarhotelsList(Nonstarhotels nonstarhotels)
    {
        return nonstarhotelsMapper.selectNonstarhotelsList(nonstarhotels);
    }
}
