package com.ruoyi.hotel.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.hotel.mapper.NonstarhotelsMapper;
import com.ruoyi.hotel.domain.Nonstarhotels;
import com.ruoyi.hotel.service.INonstarhotelsService;

/**
 * 非星级酒店Service业务层处理
 * 
 * @author ningf
 * @date 2024-07-14
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

    /**
     * 新增非星级酒店
     * 
     * @param nonstarhotels 非星级酒店
     * @return 结果
     */
    @Override
    public int insertNonstarhotels(Nonstarhotels nonstarhotels)
    {
        return nonstarhotelsMapper.insertNonstarhotels(nonstarhotels);
    }

    /**
     * 修改非星级酒店
     * 
     * @param nonstarhotels 非星级酒店
     * @return 结果
     */
    @Override
    public int updateNonstarhotels(Nonstarhotels nonstarhotels)
    {
        return nonstarhotelsMapper.updateNonstarhotels(nonstarhotels);
    }

    /**
     * 批量删除非星级酒店
     * 
     * @param ids 需要删除的非星级酒店主键
     * @return 结果
     */
    @Override
    public int deleteNonstarhotelsByIds(Long[] ids)
    {
        return nonstarhotelsMapper.deleteNonstarhotelsByIds(ids);
    }

    /**
     * 删除非星级酒店信息
     * 
     * @param id 非星级酒店主键
     * @return 结果
     */
    @Override
    public int deleteNonstarhotelsById(Long id)
    {
        return nonstarhotelsMapper.deleteNonstarhotelsById(id);
    }
}
