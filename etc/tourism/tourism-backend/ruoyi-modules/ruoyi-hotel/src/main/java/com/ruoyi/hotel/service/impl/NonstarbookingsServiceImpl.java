package com.ruoyi.hotel.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.hotel.mapper.NonstarbookingsMapper;
import com.ruoyi.hotel.domain.Nonstarbookings;
import com.ruoyi.hotel.service.INonstarbookingsService;

/**
 * 非星级酒店预定信息Service业务层处理
 * 
 * @author ningf
 * @date 2024-07-14
 */
@Service
public class NonstarbookingsServiceImpl implements INonstarbookingsService 
{
    @Autowired
    private NonstarbookingsMapper nonstarbookingsMapper;

    /**
     * 查询非星级酒店预定信息
     * 
     * @param id 非星级酒店预定信息主键
     * @return 非星级酒店预定信息
     */
    @Override
    public Nonstarbookings selectNonstarbookingsById(Long id)
    {
        return nonstarbookingsMapper.selectNonstarbookingsById(id);
    }

    /**
     * 查询非星级酒店预定信息列表
     * 
     * @param nonstarbookings 非星级酒店预定信息
     * @return 非星级酒店预定信息
     */
    @Override
    public List<Nonstarbookings> selectNonstarbookingsList(Nonstarbookings nonstarbookings)
    {
        return nonstarbookingsMapper.selectNonstarbookingsList(nonstarbookings);
    }

    /**
     * 新增非星级酒店预定信息
     * 
     * @param nonstarbookings 非星级酒店预定信息
     * @return 结果
     */
    @Override
    public int insertNonstarbookings(Nonstarbookings nonstarbookings)
    {
        return nonstarbookingsMapper.insertNonstarbookings(nonstarbookings);
    }

    /**
     * 修改非星级酒店预定信息
     * 
     * @param nonstarbookings 非星级酒店预定信息
     * @return 结果
     */
    @Override
    public int updateNonstarbookings(Nonstarbookings nonstarbookings)
    {
        return nonstarbookingsMapper.updateNonstarbookings(nonstarbookings);
    }

    /**
     * 批量删除非星级酒店预定信息
     * 
     * @param ids 需要删除的非星级酒店预定信息主键
     * @return 结果
     */
    @Override
    public int deleteNonstarbookingsByIds(Long[] ids)
    {
        return nonstarbookingsMapper.deleteNonstarbookingsByIds(ids);
    }

    /**
     * 删除非星级酒店预定信息信息
     * 
     * @param id 非星级酒店预定信息主键
     * @return 结果
     */
    @Override
    public int deleteNonstarbookingsById(Long id)
    {
        return nonstarbookingsMapper.deleteNonstarbookingsById(id);
    }

    @Override
    public int confirmNonstarbookingsByIds(Long[] ids) {
        return nonstarbookingsMapper.confirmNonstarbookingsByIds(ids);
    }
}
