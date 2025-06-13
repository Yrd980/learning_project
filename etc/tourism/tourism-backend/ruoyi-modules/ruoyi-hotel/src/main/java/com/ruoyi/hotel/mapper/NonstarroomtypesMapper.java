package com.ruoyi.hotel.mapper;

import java.util.List;
import com.ruoyi.hotel.domain.Nonstarroomtypes;

/**
 * 非星级酒店房型Mapper接口
 * 
 * @author ningf
 * @date 2024-07-14
 */
public interface NonstarroomtypesMapper 
{
    /**
     * 查询非星级酒店房型
     * 
     * @param id 非星级酒店房型主键
     * @return 非星级酒店房型
     */
    public Nonstarroomtypes selectNonstarroomtypesById(Long id);

    /**
     * 查询非星级酒店房型列表
     * 
     * @param nonstarroomtypes 非星级酒店房型
     * @return 非星级酒店房型集合
     */
    public List<Nonstarroomtypes> selectNonstarroomtypesList(Nonstarroomtypes nonstarroomtypes);

    /**
     * 新增非星级酒店房型
     * 
     * @param nonstarroomtypes 非星级酒店房型
     * @return 结果
     */
    public int insertNonstarroomtypes(Nonstarroomtypes nonstarroomtypes);

    /**
     * 修改非星级酒店房型
     * 
     * @param nonstarroomtypes 非星级酒店房型
     * @return 结果
     */
    public int updateNonstarroomtypes(Nonstarroomtypes nonstarroomtypes);

    /**
     * 删除非星级酒店房型
     * 
     * @param id 非星级酒店房型主键
     * @return 结果
     */
    public int deleteNonstarroomtypesById(Long id);

    /**
     * 批量删除非星级酒店房型
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteNonstarroomtypesByIds(Long[] ids);
}
