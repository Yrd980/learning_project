package com.ruoyi.hotel.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.hotel.mapper.StarroomtypesMapper;
import com.ruoyi.hotel.domain.Starroomtypes;
import com.ruoyi.hotel.service.IStarroomtypesService;

/**
 * 星级酒店房型Service业务层处理
 * 
 * @author ningf
 * @date 2024-07-12
 */
@Service
public class StarroomtypesServiceImpl implements IStarroomtypesService 
{
    @Autowired
    private StarroomtypesMapper starroomtypesMapper;

    /**
     * 查询星级酒店房型
     * 
     * @param id 星级酒店房型主键
     * @return 星级酒店房型
     */
    @Override
    public Starroomtypes selectStarroomtypesById(Long id)
    {
        return starroomtypesMapper.selectStarroomtypesById(id);
    }

    /**
     * 查询星级酒店房型列表
     * 
     * @param starroomtypes 星级酒店房型
     * @return 星级酒店房型
     */
    @Override
    public List<Starroomtypes> selectStarroomtypesList(Starroomtypes starroomtypes)
    {
        return starroomtypesMapper.selectStarroomtypesList(starroomtypes);
    }

    /**
     * 新增星级酒店房型
     * 
     * @param starroomtypes 星级酒店房型
     * @return 结果
     */
    @Override
    public int insertStarroomtypes(Starroomtypes starroomtypes)
    {
        return starroomtypesMapper.insertStarroomtypes(starroomtypes);
    }

    /**
     * 修改星级酒店房型
     * 
     * @param starroomtypes 星级酒店房型
     * @return 结果
     */
    @Override
    public int updateStarroomtypes(Starroomtypes starroomtypes)
    {
        return starroomtypesMapper.updateStarroomtypes(starroomtypes);
    }

    /**
     * 批量删除星级酒店房型
     * 
     * @param ids 需要删除的星级酒店房型主键
     * @return 结果
     */
    @Override
    public int deleteStarroomtypesByIds(Long[] ids)
    {
        return starroomtypesMapper.deleteStarroomtypesByIds(ids);
    }

    /**
     * 删除星级酒店房型信息
     * 
     * @param id 星级酒店房型主键
     * @return 结果
     */
    @Override
    public int deleteStarroomtypesById(Long id)
    {
        return starroomtypesMapper.deleteStarroomtypesById(id);
    }
}
