package com.ruoyi.hotel.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.hotel.mapper.StarhotelsMapper;
import com.ruoyi.hotel.domain.Starhotels;
import com.ruoyi.hotel.service.IStarhotelsService;

/**
 * 星级酒店信息Service业务层处理
 * 
 * @author ningf
 * @date 2024-07-11
 */
@Service
public class StarhotelsServiceImpl implements IStarhotelsService 
{
    @Autowired
    private StarhotelsMapper starhotelsMapper;

    /**
     * 查询星级酒店信息
     * 
     * @param id 星级酒店信息主键
     * @return 星级酒店信息
     */
    @Override
    public Starhotels selectStarhotelsById(Long id)
    {
        return starhotelsMapper.selectStarhotelsById(id);
    }

    /**
     * 查询星级酒店信息列表
     * 
     * @param starhotels 星级酒店信息
     * @return 星级酒店信息
     */
    @Override
    public List<Starhotels> selectStarhotelsList(Starhotels starhotels)
    {
        return starhotelsMapper.selectStarhotelsList(starhotels);
    }

    /**
     * 新增星级酒店信息
     * 
     * @param starhotels 星级酒店信息
     * @return 结果
     */
    @Override
    public int insertStarhotels(Starhotels starhotels)
    {
        return starhotelsMapper.insertStarhotels(starhotels);
    }

    /**
     * 修改星级酒店信息
     * 
     * @param starhotels 星级酒店信息
     * @return 结果
     */
    @Override
    public int updateStarhotels(Starhotels starhotels)
    {
        return starhotelsMapper.updateStarhotels(starhotels);
    }

    /**
     * 批量删除星级酒店信息
     * 
     * @param ids 需要删除的星级酒店信息主键
     * @return 结果
     */
    @Override
    public int deleteStarhotelsByIds(Long[] ids)
    {
        return starhotelsMapper.deleteStarhotelsByIds(ids);
    }

    /**
     * 删除星级酒店信息信息
     * 
     * @param id 星级酒店信息主键
     * @return 结果
     */
    @Override
    public int deleteStarhotelsById(Long id)
    {
        return starhotelsMapper.deleteStarhotelsById(id);
    }
}
