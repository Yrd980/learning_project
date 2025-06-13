package com.ruoyi.hotel.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.hotel.mapper.NonstarroomtypesMapper;
import com.ruoyi.hotel.domain.Nonstarroomtypes;
import com.ruoyi.hotel.service.INonstarroomtypesService;

/**
 * 非星级酒店房型Service业务层处理
 * 
 * @author ningf
 * @date 2024-07-14
 */
@Service
public class NonstarroomtypesServiceImpl implements INonstarroomtypesService 
{
    @Autowired
    private NonstarroomtypesMapper nonstarroomtypesMapper;

    /**
     * 查询非星级酒店房型
     * 
     * @param id 非星级酒店房型主键
     * @return 非星级酒店房型
     */
    @Override
    public Nonstarroomtypes selectNonstarroomtypesById(Long id)
    {
        return nonstarroomtypesMapper.selectNonstarroomtypesById(id);
    }

    /**
     * 查询非星级酒店房型列表
     * 
     * @param nonstarroomtypes 非星级酒店房型
     * @return 非星级酒店房型
     */
    @Override
    public List<Nonstarroomtypes> selectNonstarroomtypesList(Nonstarroomtypes nonstarroomtypes)
    {
        return nonstarroomtypesMapper.selectNonstarroomtypesList(nonstarroomtypes);
    }

    /**
     * 新增非星级酒店房型
     * 
     * @param nonstarroomtypes 非星级酒店房型
     * @return 结果
     */
    @Override
    public int insertNonstarroomtypes(Nonstarroomtypes nonstarroomtypes)
    {
        return nonstarroomtypesMapper.insertNonstarroomtypes(nonstarroomtypes);
    }

    /**
     * 修改非星级酒店房型
     * 
     * @param nonstarroomtypes 非星级酒店房型
     * @return 结果
     */
    @Override
    public int updateNonstarroomtypes(Nonstarroomtypes nonstarroomtypes)
    {
        return nonstarroomtypesMapper.updateNonstarroomtypes(nonstarroomtypes);
    }

    /**
     * 批量删除非星级酒店房型
     * 
     * @param ids 需要删除的非星级酒店房型主键
     * @return 结果
     */
    @Override
    public int deleteNonstarroomtypesByIds(Long[] ids)
    {
        return nonstarroomtypesMapper.deleteNonstarroomtypesByIds(ids);
    }

    /**
     * 删除非星级酒店房型信息
     * 
     * @param id 非星级酒店房型主键
     * @return 结果
     */
    @Override
    public int deleteNonstarroomtypesById(Long id)
    {
        return nonstarroomtypesMapper.deleteNonstarroomtypesById(id);
    }
}
