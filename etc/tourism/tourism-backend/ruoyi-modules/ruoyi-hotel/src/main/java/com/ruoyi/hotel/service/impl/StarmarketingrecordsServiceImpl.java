package com.ruoyi.hotel.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.hotel.mapper.StarmarketingrecordsMapper;
import com.ruoyi.hotel.domain.Starmarketingrecords;
import com.ruoyi.hotel.service.IStarmarketingrecordsService;

/**
 * 酒店营销记录Service业务层处理
 * 
 * @author ningf
 * @date 2024-07-10
 */
@Service
public class StarmarketingrecordsServiceImpl implements IStarmarketingrecordsService 
{
    @Autowired
    private StarmarketingrecordsMapper starmarketingrecordsMapper;

    /**
     * 查询酒店营销记录
     * 
     * @param id 酒店营销记录主键
     * @return 酒店营销记录
     */
    @Override
    public Starmarketingrecords selectStarmarketingrecordsById(Long id)
    {
        return starmarketingrecordsMapper.selectStarmarketingrecordsById(id);
    }

    /**
     * 查询酒店营销记录列表
     * 
     * @param starmarketingrecords 酒店营销记录
     * @return 酒店营销记录
     */
    @Override
    public List<Starmarketingrecords> selectStarmarketingrecordsList(Starmarketingrecords starmarketingrecords)
    {
        return starmarketingrecordsMapper.selectStarmarketingrecordsList(starmarketingrecords);
    }

    /**
     * 新增酒店营销记录
     * 
     * @param starmarketingrecords 酒店营销记录
     * @return 结果
     */
    @Override
    public int insertStarmarketingrecords(Starmarketingrecords starmarketingrecords)
    {
        return starmarketingrecordsMapper.insertStarmarketingrecords(starmarketingrecords);
    }

    /**
     * 修改酒店营销记录
     * 
     * @param starmarketingrecords 酒店营销记录
     * @return 结果
     */
    @Override
    public int updateStarmarketingrecords(Starmarketingrecords starmarketingrecords)
    {
        return starmarketingrecordsMapper.updateStarmarketingrecords(starmarketingrecords);
    }

    /**
     * 批量删除酒店营销记录
     * 
     * @param ids 需要删除的酒店营销记录主键
     * @return 结果
     */
    @Override
    public int deleteStarmarketingrecordsByIds(Long[] ids)
    {
        return starmarketingrecordsMapper.deleteStarmarketingrecordsByIds(ids);
    }

    /**
     * 删除酒店营销记录信息
     * 
     * @param id 酒店营销记录主键
     * @return 结果
     */
    @Override
    public int deleteStarmarketingrecordsById(Long id)
    {
        return starmarketingrecordsMapper.deleteStarmarketingrecordsById(id);
    }
}
