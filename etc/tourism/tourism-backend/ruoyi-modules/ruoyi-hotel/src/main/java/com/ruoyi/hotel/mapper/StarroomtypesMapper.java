package com.ruoyi.hotel.mapper;

import java.util.List;
import com.ruoyi.hotel.domain.Starroomtypes;

/**
 * 星级酒店房型Mapper接口
 * 
 * @author ningf
 * @date 2024-07-12
 */
public interface StarroomtypesMapper 
{
    /**
     * 查询星级酒店房型
     * 
     * @param id 星级酒店房型主键
     * @return 星级酒店房型
     */
    public Starroomtypes selectStarroomtypesById(Long id);

    /**
     * 查询星级酒店房型列表
     * 
     * @param starroomtypes 星级酒店房型
     * @return 星级酒店房型集合
     */
    public List<Starroomtypes> selectStarroomtypesList(Starroomtypes starroomtypes);

    /**
     * 新增星级酒店房型
     * 
     * @param starroomtypes 星级酒店房型
     * @return 结果
     */
    public int insertStarroomtypes(Starroomtypes starroomtypes);

    /**
     * 修改星级酒店房型
     * 
     * @param starroomtypes 星级酒店房型
     * @return 结果
     */
    public int updateStarroomtypes(Starroomtypes starroomtypes);

    /**
     * 删除星级酒店房型
     * 
     * @param id 星级酒店房型主键
     * @return 结果
     */
    public int deleteStarroomtypesById(Long id);

    /**
     * 批量删除星级酒店房型
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteStarroomtypesByIds(Long[] ids);
}
