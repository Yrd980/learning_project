package com.ruoyi.hotel.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.hotel.mapper.StarbookingsMapper;
import com.ruoyi.hotel.domain.Starbookings;
import com.ruoyi.hotel.service.IStarbookingsService;

/**
 * 星级酒店预定信息Service业务层处理
 * 
 * @author ningf
 * @date 2024-07-11
 */
@Service
public class StarbookingsServiceImpl implements IStarbookingsService 
{
    @Autowired
    private StarbookingsMapper starbookingsMapper;

    /**
     * 查询星级酒店预定信息
     * 
     * @param id 星级酒店预定信息主键
     * @return 星级酒店预定信息
     */
    @Override
    public Starbookings selectStarbookingsById(Long id)
    {
        return starbookingsMapper.selectStarbookingsById(id);
    }

    /**
     * 查询星级酒店预定信息列表
     * 
     * @param starbookings 星级酒店预定信息
     * @return 星级酒店预定信息
     */
    @Override
    public List<Starbookings> selectStarbookingsList(Starbookings starbookings)
    {
        return starbookingsMapper.selectStarbookingsList(starbookings);
    }

    /**
     * 新增星级酒店预定信息
     * 
     * @param starbookings 星级酒店预定信息
     * @return 结果
     */
    @Override
    public int insertStarbookings(Starbookings starbookings)
    {
        return starbookingsMapper.insertStarbookings(starbookings);
    }

    /**
     * 修改星级酒店预定信息
     * 
     * @param starbookings 星级酒店预定信息
     * @return 结果
     */
    @Override
    public int updateStarbookings(Starbookings starbookings)
    {
        return starbookingsMapper.updateStarbookings(starbookings);
    }

    /**
     * 批量删除星级酒店预定信息
     * 
     * @param ids 需要删除的星级酒店预定信息主键
     * @return 结果
     */
    @Override
    public int deleteStarbookingsByIds(Long[] ids)
    {
        return starbookingsMapper.deleteStarbookingsByIds(ids);
    }

    /**
     * 删除星级酒店预定信息信息
     * 
     * @param id 星级酒店预定信息主键
     * @return 结果
     */
    @Override
    public int deleteStarbookingsById(Long id)
    {
        return starbookingsMapper.deleteStarbookingsById(id);
    }

    @Override
    public int confirmStarbookingsByIds(Long[] ids) {
        return starbookingsMapper.confirmStarbookingsByIds(ids);
    }
}
