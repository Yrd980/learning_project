package com.ruoyi.hotel.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.hotel.mapper.NonstarhotelreviewsMapper;
import com.ruoyi.hotel.domain.Nonstarhotelreviews;
import com.ruoyi.hotel.service.INonstarhotelreviewsService;

/**
 * 非星级酒店评价Service业务层处理
 * 
 * @author ningf
 * @date 2024-07-15
 */
@Service
public class NonstarhotelreviewsServiceImpl implements INonstarhotelreviewsService 
{
    @Autowired
    private NonstarhotelreviewsMapper nonstarhotelreviewsMapper;

    /**
     * 查询非星级酒店评价
     * 
     * @param id 非星级酒店评价主键
     * @return 非星级酒店评价
     */
    @Override
    public Nonstarhotelreviews selectNonstarhotelreviewsById(Long id)
    {
        return nonstarhotelreviewsMapper.selectNonstarhotelreviewsById(id);
    }

    /**
     * 查询非星级酒店评价列表
     * 
     * @param nonstarhotelreviews 非星级酒店评价
     * @return 非星级酒店评价
     */
    @Override
    public List<Nonstarhotelreviews> selectNonstarhotelreviewsList(Nonstarhotelreviews nonstarhotelreviews)
    {
        return nonstarhotelreviewsMapper.selectNonstarhotelreviewsList(nonstarhotelreviews);
    }

    /**
     * 新增非星级酒店评价
     * 
     * @param nonstarhotelreviews 非星级酒店评价
     * @return 结果
     */
    @Override
    public int insertNonstarhotelreviews(Nonstarhotelreviews nonstarhotelreviews)
    {
        return nonstarhotelreviewsMapper.insertNonstarhotelreviews(nonstarhotelreviews);
    }

    /**
     * 修改非星级酒店评价
     * 
     * @param nonstarhotelreviews 非星级酒店评价
     * @return 结果
     */
    @Override
    public int updateNonstarhotelreviews(Nonstarhotelreviews nonstarhotelreviews)
    {
        return nonstarhotelreviewsMapper.updateNonstarhotelreviews(nonstarhotelreviews);
    }

    /**
     * 批量删除非星级酒店评价
     * 
     * @param ids 需要删除的非星级酒店评价主键
     * @return 结果
     */
    @Override
    public int deleteNonstarhotelreviewsByIds(Long[] ids)
    {
        return nonstarhotelreviewsMapper.deleteNonstarhotelreviewsByIds(ids);
    }

    /**
     * 删除非星级酒店评价信息
     * 
     * @param id 非星级酒店评价主键
     * @return 结果
     */
    @Override
    public int deleteNonstarhotelreviewsById(Long id)
    {
        return nonstarhotelreviewsMapper.deleteNonstarhotelreviewsById(id);
    }
}
